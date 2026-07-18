"""router — Dynamic routing decision engine.

Decides between the cerebellum fast path (pattern matching) and cerebrum (LLM reasoning).
This is the core control logic of the Dual-Cognition architecture.

Flow:
  User input
    -> 1. ComplexityScorer.estimate() -> multi-dimensional complexity score
    -> 2. Policy selection (auto | fast | thorough | adaptive)
    -> 3. Routing decision (cerebellum vs cerebrum)
    -> 4. Result tracking + adaptive threshold adjustment
"""

from __future__ import annotations

import json
import logging
import os
import re
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

_log = logging.getLogger("slayhot.router")


# ═══════════════════════════════════════════
# Routing policy
# ═══════════════════════════════════════════

class RoutingPolicy(str, Enum):
    AUTO = "auto"
    CEREBELLUM = "fast"
    CEREBRUM = "thorough"
    ADAPTIVE = "adaptive"

    @classmethod
    def default(cls) -> RoutingPolicy:
        return cls.AUTO


# ═══════════════════════════════════════════
# Routing decision structure
# ═══════════════════════════════════════════

@dataclass
class RoutingDecision:
    path: str                     # "cerebellum" | "cerebrum"
    complexity_score: float
    complexity_bucket: str        # "low" | "medium" | "high"
    match_confidence: float
    threshold_used: float
    policy: str
    reason: str
    allow_fallback: bool = True
    skip_cerebellum: bool = False


# ═══════════════════════════════════════════
# Complexity scorer
# ═══════════════════════════════════════════

class ComplexityScorer:
    """Multi-dimensional task complexity estimator. Outputs 0.0-1.0."""

    LOW_KEYWORDS = frozenset([
        "read", "open", "show", "display", "cat", "view",
        "list", "ls", "dir", "find", "search", "grep", "locate",
        "run", "execute", "bash", "cmd", "shell",
        "fetch", "http", "get", "browse", "visit", "open url",
        "cpu", "memory", "disk", "system", "process", "ps", "task",
        "edit", "modify", "change", "replace", "update",
        "help", "version", "status", "info", "check",
    ])

    HIGH_KEYWORDS = frozenset([
        "write", "create", "build", "develop", "implement",
        "design", "architecture", "refactor", "restructure",
        "compare", "contrast", "analyze", "evaluate", "assess",
        "explain", "describe", "summarize", "why", "how", "what is",
        "plan", "strategy", "roadmap", "migration",
        "bug", "error", "debug", "fix", "issue", "problem",
        "optimize", "optimization", "performance",
        "configure", "setup", "install", "deploy",
        "migrate", "convert", "transform",
        "function", "class", "module", "package",
        "pipeline", "workflow", "generate",
    ])

    MULTI_STEP = frozenset([
        "first", "then", "finally", "after that", "next",
        "step 1", "step 2", "step by step",
        "for each", "for all", "every", "additionally",
    ])

    CODE_INDICATORS = frozenset([
        "```", "def ", "class ", "import ", "from ",
        "function", "return", "const ", "let ", "var ",
        "#include", "package ", "namespace",
    ])

    @classmethod
    def estimate(cls, message: str, context: dict | None = None) -> float:
        norm = message.lower().strip()
        if not norm:
            return 0.5

        scores = []

        # 1. Message length (weight 0.20)
        wc = len(norm.split())
        if wc <= 3:
            scores.append(0.10)
        elif wc <= 8:
            scores.append(0.25)
        elif wc <= 20:
            scores.append(0.45)
        elif wc <= 50:
            scores.append(0.70)
        else:
            scores.append(0.90)

        # 2. Keyword semantics (weight 0.30)
        has_low = any(kw in norm for kw in cls.LOW_KEYWORDS)
        has_high = any(kw in norm for kw in cls.HIGH_KEYWORDS)
        has_code = any(kw in norm for kw in cls.CODE_INDICATORS)
        has_multi = any(kw in norm for kw in cls.MULTI_STEP)

        if has_code:
            kw_score = 0.85
        elif has_multi:
            kw_score = 0.75
        elif has_high and not has_low:
            kw_score = 0.70
        elif has_low and not has_high:
            kw_score = 0.20
        else:
            kw_score = 0.50
        scores.append(kw_score)

        # 3. Question type (weight 0.20)
        q_words = ("what", "how", "why", "can you", "could you",
                   "would you", "explain", "describe", "tell me")
        is_question = any(norm.startswith(q) for q in q_words)
        scores.append(0.60 if is_question else 0.30)

        # 4. Session context errors (weight 0.15)
        if context:
            err_rate = context.get("tool_error_count", 0) / max(context.get("turn_count", 1), 1)
            if err_rate > 0.3:
                scores.append(0.80)
            elif err_rate > 0.1:
                scores.append(0.50)
            else:
                scores.append(0.30)
        else:
            scores.append(0.30)

        # 5. Structure complexity (weight 0.15)
        has_nums = bool(re.search(r'\d+', norm))
        has_bullets = '\n' in norm or '*' in norm or '-' in norm
        if has_bullets:
            scores.append(0.60)
        elif has_nums:
            scores.append(0.45)
        else:
            scores.append(0.30)

        weights = [0.20, 0.30, 0.20, 0.15, 0.15]
        complexity = sum(s * w for s, w in zip(scores, weights))
        return min(1.0, max(0.0, complexity))

    @classmethod
    def get_bucket(cls, score: float) -> str:
        if score < 0.3:
            return "low"
        elif score < 0.6:
            return "medium"
        return "high"


# ═══════════════════════════════════════════
# Routing metrics collector
# ═══════════════════════════════════════════

@dataclass
class RoutingMetrics:
    total_decisions: int = 0
    cerebellum_routes: int = 0
    cerebrum_routes: int = 0
    cerebellum_successes: int = 0
    cerebellum_fallbacks: int = 0

    by_bucket: dict[str, dict] = field(default_factory=lambda: {
        "low": {"attempts": 0, "success": 0, "fallback": 0},
        "medium": {"attempts": 0, "success": 0, "fallback": 0},
        "high": {"attempts": 0, "success": 0, "fallback": 0},
    })

    def record_cerebellum(self, bucket: str, success: bool, fallback: bool = False):
        self.total_decisions += 1
        self.cerebellum_routes += 1
        if success:
            self.cerebellum_successes += 1
        if fallback:
            self.cerebellum_fallbacks += 1
        if bucket in self.by_bucket:
            self.by_bucket[bucket]["attempts"] += 1
            if success:
                self.by_bucket[bucket]["success"] += 1
            if fallback:
                self.by_bucket[bucket]["fallback"] += 1

    def record_cerebrum(self, bucket: str):
        self.total_decisions += 1
        self.cerebrum_routes += 1

    def success_rate(self, bucket: str | None = None) -> float:
        if bucket:
            b = self.by_bucket.get(bucket, {})
            return b.get("success", 0) / max(b.get("attempts", 0), 1)
        return self.cerebellum_successes / max(self.cerebellum_routes, 1)

    def efficiency(self) -> float:
        return self.cerebellum_routes / max(self.total_decisions, 1)

    def adaptive_threshold(self, base: float = 0.4) -> float:
        low_rate = self.success_rate("low")
        med_rate = self.success_rate("medium")
        low_att = self.by_bucket["low"]["attempts"]
        threshold = base
        if low_rate >= 0.8 and low_att >= 5:
            threshold = max(0.20, base - 0.10)
        elif low_rate < 0.5 and low_att >= 3:
            threshold = min(0.70, base + 0.15)
        elif med_rate >= 0.7 and self.by_bucket["medium"]["attempts"] >= 5:
            threshold = max(0.30, base - 0.05)
        return threshold

    def report(self) -> dict:
        return {
            "total_decisions": self.total_decisions,
            "cerebellum_pct": round(self.efficiency() * 100, 1),
            "cerebellum_success_rate": round(self.success_rate() * 100, 1),
            "cerebellum_fallback_rate": round(
                self.cerebellum_fallbacks / max(self.cerebellum_routes, 1) * 100, 1),
            "by_bucket": {
                b: {"attempts": d["attempts"],
                    "success_rate": round(d["success"] / max(d["attempts"], 1) * 100, 1)}
                for b, d in self.by_bucket.items()
            },
        }

    def to_dict(self) -> dict:
        return {
            "total_decisions": self.total_decisions,
            "cerebellum_routes": self.cerebellum_routes,
            "cerebrum_routes": self.cerebrum_routes,
            "cerebellum_successes": self.cerebellum_successes,
            "cerebellum_fallbacks": self.cerebellum_fallbacks,
            "by_bucket": {k: dict(v) for k, v in self.by_bucket.items()},
        }

    @classmethod
    def from_dict(cls, d: dict) -> RoutingMetrics:
        return cls(**d)


# ═══════════════════════════════════════════
# Router main class
# ═══════════════════════════════════════════

class Router:
    """Dynamic routing decision engine.

    Decides between cerebellum (fast pattern match) and cerebrum (LLM reasoning).

    Usage:
        router = Router(policy="auto")
        dec = router.decide(
            user_message="read file /etc/config.json",
            cerebellum_match=0.85,
            session_context={"turn_count": 3},
        )
    """

    def __init__(
        self,
        policy: str | RoutingPolicy = "auto",
        base_threshold: float = 0.40,
        min_threshold: float = 0.15,
        max_threshold: float = 0.85,
        metrics: RoutingMetrics | None = None,
        storage_dir: str | None = None,
        workflow_mode: str = "agent",
    ):
        self.policy = policy if isinstance(policy, RoutingPolicy) else RoutingPolicy(policy)
        self.base_threshold = base_threshold
        self.min_threshold = min_threshold
        self.max_threshold = max_threshold
        self.metrics = metrics or RoutingMetrics()
        self.workflow_mode = workflow_mode
        self._storage_dir = storage_dir or os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            ".slayhot"
        )
        self._load_metrics()

    def decide(
        self,
        user_message: str,
        cerebellum_match: float | None = None,
        complexity_score: float | None = None,
        session_context: dict | None = None,
    ) -> RoutingDecision:
        if complexity_score is None:
            complexity_score = ComplexityScorer.estimate(user_message, session_context)
        bucket = ComplexityScorer.get_bucket(complexity_score)
        match_conf = cerebellum_match or 0.0

        if self.policy == RoutingPolicy.CEREBRUM:
            self.metrics.record_cerebrum(bucket)
            return RoutingDecision(
                path="cerebrum", complexity_score=complexity_score,
                complexity_bucket=bucket, match_confidence=match_conf,
                threshold_used=0.0, policy=self.policy.value,
                reason="Policy forced: thorough mode", skip_cerebellum=True,
            )

        if self.policy == RoutingPolicy.CEREBELLUM:
            if cerebellum_match is not None and cerebellum_match > self.min_threshold:
                return RoutingDecision(
                    path="cerebellum", complexity_score=complexity_score,
                    complexity_bucket=bucket, match_confidence=match_conf,
                    threshold_used=self.min_threshold, policy=self.policy.value,
                    reason="Policy forced: fast mode", allow_fallback=False,
                )
            self.metrics.record_cerebrum(bucket)
            return RoutingDecision(
                path="cerebrum", complexity_score=complexity_score,
                complexity_bucket=bucket, match_confidence=match_conf,
                threshold_used=self.min_threshold, policy=self.policy.value,
                reason="Fast mode but no cerebellum match",
            )

        threshold = self.base_threshold
        if self.policy == RoutingPolicy.ADAPTIVE:
            threshold = self.metrics.adaptive_threshold(self.base_threshold)
            threshold = max(self.min_threshold, min(self.max_threshold, threshold))

        if complexity_score >= 0.7:
            self.metrics.record_cerebrum(bucket)
            return RoutingDecision(
                path="cerebrum", complexity_score=complexity_score,
                complexity_bucket=bucket, match_confidence=match_conf,
                threshold_used=threshold, policy=self.policy.value,
                reason="High complexity ({:.2f}), needs LLM".format(complexity_score),
                skip_cerebellum=True,
            )

        if cerebellum_match is None:
            self.metrics.record_cerebrum(bucket)
            return RoutingDecision(
                path="cerebrum", complexity_score=complexity_score,
                complexity_bucket=bucket, match_confidence=0.0,
                threshold_used=threshold, policy=self.policy.value,
                reason="No cerebellum match",
            )

        if cerebellum_match >= threshold:
            return RoutingDecision(
                path="cerebellum", complexity_score=complexity_score,
                complexity_bucket=bucket, match_confidence=cerebellum_match,
                threshold_used=threshold, policy=self.policy.value,
                reason="Cerebellum match {:.3f} >= threshold {:.3f}".format(cerebellum_match, threshold),
                allow_fallback=(complexity_score >= 0.4),
            )
        else:
            self.metrics.record_cerebrum(bucket)
            return RoutingDecision(
                path="cerebrum", complexity_score=complexity_score,
                complexity_bucket=bucket, match_confidence=cerebellum_match,
                threshold_used=threshold, policy=self.policy.value,
                reason="Cerebellum match {:.3f} < threshold {:.3f}".format(cerebellum_match, threshold),
            )

    def report_cerebellum_result(self, decision: RoutingDecision, success: bool,
                                  fallback: bool = False):
        self.metrics.record_cerebellum(decision.complexity_bucket, success, fallback)
        self._save_metrics()

    def report_cerebrum_result(self, complexity_score: float):
        bucket = ComplexityScorer.get_bucket(complexity_score)
        self.metrics.record_cerebrum(bucket)
        self._save_metrics()

    def set_policy(self, policy: str | RoutingPolicy):
        self.policy = policy if isinstance(policy, RoutingPolicy) else RoutingPolicy(policy)
        _log.info("router_policy policy=%s", self.policy.value)

    def set_workflow_mode(self, mode: str):
        self.workflow_mode = mode
        if mode == "chat":
            self.set_policy(RoutingPolicy.AUTO)
        elif mode == "research":
            self.set_policy(RoutingPolicy.AUTO)
        elif mode == "coding":
            self.set_policy(RoutingPolicy.AUTO)
        elif mode == "debug":
            self.set_policy(RoutingPolicy.CEREBRUM)
        elif mode == "agent":
            self.set_policy(RoutingPolicy.AUTO)

    def metrics_report(self) -> dict:
        return self.metrics.report()

    def reset_metrics(self):
        self.metrics = RoutingMetrics()
        self._save_metrics()

    def _metrics_path(self) -> Path:
        return Path(self._storage_dir) / "routing_metrics.json"

    def _save_metrics(self):
        try:
            p = self._metrics_path()
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                json.dump(self.metrics.to_dict(), f, ensure_ascii=False, indent=2)
        except Exception as e:
            _log.debug("router_save error=%s", e)

    def _load_metrics(self):
        try:
            p = self._metrics_path()
            if p.exists():
                with open(p, "r", encoding="utf-8") as f:
                    self.metrics = RoutingMetrics.from_dict(json.load(f))
        except Exception as e:
            _log.debug("router_load error=%s", e)
