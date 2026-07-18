"""cerebellum — SlayHot pattern-driven fast-path engine (Dual-Cognition quick path).

Design philosophy:
  The human cerebellum handles "patternized actions" — walking, typing, riding a bike.
  SlayHot's cerebellum does the same: 80% of common requests (read file, check process,
  search code) don't need LLM reasoning — they can be pattern-matched and executed directly.

Feedback loop:
  Cerebrum (LLM) success -> Cerebellum extracts "intent -> tool call" pattern -> pattern library
  Cerebellum match success -> confidence +1
  Cerebellum match failure (tool error) -> confidence -1
  Confidence below threshold -> pattern auto-disabled
"""

from __future__ import annotations

import json
import logging
import os
import re
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

_log = logging.getLogger("slayhot.cerebellum")


# ═══════════════════════════════════════════
# Data structures
# ═══════════════════════════════════════════

@dataclass
class Pattern:
    """Cerebellum pattern — maps natural language "intent" to tool calls."""

    name: str
    description: str
    keywords: list[str]
    tool: str
    params: dict[str, Any] = field(default_factory=dict)
    exclude_keywords: list[str] = field(default_factory=list)
    response_template: str = ""
    confidence: float = 0.8
    usage_count: int = 0
    success_count: int = 0
    min_confidence: float = 0.3
    enabled: bool = True
    created_at: float = 0.0
    last_used: float = 0.0

    def __post_init__(self):
        if not self.created_at:
            self.created_at = time.time()

    @property
    def success_rate(self) -> float:
        if self.usage_count == 0:
            return 0.0
        return self.success_count / self.usage_count

    def record_hit(self, success: bool):
        self.usage_count += 1
        self.last_used = time.time()
        if success:
            self.success_count += 1
            self.confidence = min(1.0, self.confidence + 0.02)
        else:
            self.confidence = max(0.0, self.confidence - 0.05)
            if self.confidence < self.min_confidence:
                self.enabled = False
                _log.info("pattern_disabled name=%s confidence=%.2f", self.name, self.confidence)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "keywords": self.keywords,
            "exclude_keywords": self.exclude_keywords,
            "tool": self.tool,
            "params": self.params,
            "response_template": self.response_template,
            "confidence": round(self.confidence, 3),
            "usage_count": self.usage_count,
            "success_count": self.success_count,
            "enabled": self.enabled,
            "created_at": self.created_at,
            "last_used": self.last_used,
        }

    @classmethod
    def from_dict(cls, d: dict) -> Pattern:
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class PatternMatchResult:
    """Result of a single pattern match attempt."""
    pattern: Pattern
    extracted_params: dict[str, Any]
    match_confidence: float


@dataclass
class CerebellumDecision:
    """Cerebellum decision output — directly executable tool calls."""
    tool_calls: list[dict]
    response: str
    pattern_name: str
    match_confidence: float
    duration_ms: float
    result: str | None = None


# ═══════════════════════════════════════════
# Parameter extractor
# ═══════════════════════════════════════════

class ParamExtractor:
    """Static methods for extracting tool params from user input."""

    @staticmethod
    def regex(text: str, pattern: str, group: int = 1) -> str | None:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            val = m.group(group)
            if val:
                return val.strip().strip('"').strip("'")
        return None

    @staticmethod
    def after_keyword(text: str, keyword: str) -> str | None:
        idx = text.lower().rfind(keyword.lower())
        if idx >= 0:
            rest = text[idx + len(keyword):].strip()
            if rest:
                return rest
        return None

    @staticmethod
    def rest(text: str, matched_span: tuple[int, int]) -> str:
        end = matched_span[1]
        rest = text[end:].strip().lstrip(".,:;!?").strip()
        return rest if rest else ""

    @staticmethod
    def static(value: Any) -> Any:
        return value

    @staticmethod
    def extract(text: str, spec: Any, matched_span: tuple[int, int] | None = None) -> Any:
        if isinstance(spec, dict):
            t = spec.get("type", "")
            if t == "regex":
                return ParamExtractor.regex(text, spec["pattern"], spec.get("group", 1))
            elif t == "after_keyword":
                return ParamExtractor.after_keyword(text, spec["keyword"])
            elif t == "rest":
                if matched_span:
                    return ParamExtractor.rest(text, matched_span)
                return None
            elif t == "static":
                return spec.get("value")
            return None
        elif isinstance(spec, str):
            return ParamExtractor.after_keyword(text, spec)
        return None


# ═══════════════════════════════════════════
# Cerebellum engine
# ═══════════════════════════════════════════

class Cerebellum:
    """Cerebellum — pattern-driven fast decision engine.

    Workflow:
      1. decide(text) -> match patterns -> extract params -> return decision | None
      2. learn(text, tool_calls) -> extract new pattern from LLM success
      3. stats -> return hit rate, performance data
    """

    def __init__(self, storage_dir: str | None = None):
        self._patterns: dict[str, Pattern] = {}
        self._stats: dict[str, Any] = {
            "total_attempts": 0,
            "hits": 0,
            "misses": 0,
            "errors": 0,
            "total_decision_time_ms": 0.0,
            "by_tool": {},
        }
        self._storage_dir = storage_dir or os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            ".slayhot", "cerebellum"
        )
        self._load_pattern_library()
        self._init_learned_patterns()

    def _load_pattern_library(self):
        """Load built-in pattern library."""
        builtins = [
            Pattern(
                name="read_file",
                description="Read file contents",
                keywords=["read", "open", "show", "display", "cat", "view"],
                tool="read",
                params={
                    "file_path": {"type": "regex", "pattern": r"(?:read|open|show|display|cat)\s+(?:file\s+)?['\"]?([^\s'\"]+(?:\.[^\s'\"]+)?)['\"]?"},
                },
                response_template="File {file_path}:\n\n{result}",
            ),
            Pattern(
                name="glob_files",
                description="Search files by glob pattern",
                keywords=["list", "ls", "dir", "find files", "search files", "glob"],
                tool="glob",
                params={
                    "pattern": {"type": "after_keyword", "keyword": "in"},
                },
                exclude_keywords=["content", "text", "code", "string"],
                response_template="Files:\n\n{result}",
            ),
            Pattern(
                name="grep_search",
                description="Search file contents",
                keywords=["search", "find", "grep", "look for", "find in"],
                tool="grep",
                params={
                    "pattern": {"type": "regex", "pattern": r"(?:search|find|grep|look for)\s+(?:for\s+|in\s+)?['\"]?(.+?)['\"]?(?:\s+in\s+.+)?$"},
                },
                exclude_keywords=["web", "internet", "online", "google"],
                response_template="Search results:\n\n{result}",
            ),
            Pattern(
                name="glob_py_files",
                description="Search Python files",
                keywords=["list py", "ls py", "find py", "python files"],
                tool="glob",
                params={
                    "pattern": {"type": "static", "value": "**/*.py"},
                },
                response_template="Python files:\n\n{result}",
            ),
            Pattern(
                name="run_command",
                description="Execute shell command",
                keywords=["run", "execute", "bash", "cmd", "command", "shell"],
                tool="bash",
                params={
                    "command": {"type": "rest"},
                    "timeout": {"type": "static", "value": 30},
                },
                response_template="```\n$ {command}\n{result}\n```",
            ),
            Pattern(
                name="web_fetch",
                description="Send HTTP request",
                keywords=["fetch", "http", "https://", "http://", "browse", "open url"],
                tool="web",
                params={
                    "url": {"type": "regex", "pattern": r"(https?://[^\s'\"]+)"},
                    "method": {"type": "static", "value": "GET"},
                },
                response_template="Web {url}:\n\n{result}",
            ),
            Pattern(
                name="web_search",
                description="Search the web",
                keywords=["search web", "google", "look up", "search online"],
                tool="web_search",
                params={
                    "query": {"type": "rest"},
                    "max_results": {"type": "static", "value": 5},
                },
                response_template="Web search:\n\n{result}",
            ),
            Pattern(
                name="system_info",
                description="Check system info",
                keywords=["system", "sysinfo", "cpu", "memory", "disk", "system info"],
                tool="monitor",
                params={
                    "action": {"type": "static", "value": "info"},
                },
                response_template="System info:\n\n{result}",
            ),
            Pattern(
                name="process_list",
                description="List processes",
                keywords=["process", "ps", "task"],
                tool="process",
                params={
                    "action": {"type": "static", "value": "list"},
                },
                response_template="Processes:\n\n{result}",
            ),
            Pattern(
                name="edit_file",
                description="Edit file contents",
                keywords=["edit", "modify", "change", "replace", "update"],
                tool="edit",
                params={
                    "file_path": {"type": "regex", "pattern": r"(?:edit|modify|change|replace|update)\s+(?:file\s+)?['\"]?([^\s'\"]+(?:\.[^\s'\"]+)?)['\"]?"},
                },
                exclude_keywords=["list", "dir", "ls", "show", "read", "cat"],
                response_template="Edited {file_path}:\n\n{result}",
            ),
            Pattern(
                name="grep_code",
                description="Search code for specific content",
                keywords=["find code", "search code", "find in code", "locate"],
                tool="grep",
                params={
                    "pattern": {"type": "rest"},
                },
                response_template="Code search:\n\n{result}",
            ),
        ]

        for p in builtins:
            self._patterns[p.name] = p

    def _init_learned_patterns(self):
        try:
            path = Path(self._storage_dir) / "learned_patterns.json"
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                count = 0
                for item in data:
                    p = Pattern.from_dict(item)
                    if p.name not in self._patterns:
                        self._patterns[p.name] = p
                        count += 1
                if count:
                    _log.info("cerebellum_learned_loaded count=%d", count)
        except Exception as e:
            _log.debug("cerebellum_load_learned error=%s", e)

    def _save_learned_patterns(self):
        try:
            os.makedirs(self._storage_dir, exist_ok=True)
            learned = [
                p.to_dict() for p in self._patterns.values()
                if not p.name.startswith("_") and p.usage_count > 0
            ]
            path = Path(self._storage_dir) / "learned_patterns.json"
            with open(path, "w", encoding="utf-8") as f:
                json.dump(learned, f, ensure_ascii=False, indent=2)
        except Exception as e:
            _log.debug("cerebellum_save_learned error=%s", e)

    @staticmethod
    def _normalize(text: str) -> str:
        return text.strip().lower()

    def decide(self, user_message: str, context: dict | None = None) -> CerebellumDecision | None:
        t0 = time.time()
        self._stats["total_attempts"] += 1
        norm = self._normalize(user_message)

        best: PatternMatchResult | None = None
        best_score = 0.0

        for pattern in self._patterns.values():
            if not pattern.enabled:
                continue
            if pattern.confidence < pattern.min_confidence:
                continue

            result = self._match_pattern(norm, user_message, pattern)
            if result is not None and result.match_confidence > best_score:
                best = result
                best_score = result.match_confidence

        if best is None:
            self._stats["misses"] += 1
            return None

        decision = self._build_decision(best, user_message, t0)
        if decision is None:
            self._stats["misses"] += 1
            return None

        self._stats["hits"] += 1
        return decision

    def _match_pattern(self, norm: str, original: str, pattern: Pattern) -> PatternMatchResult | None:
        for ek in pattern.exclude_keywords:
            if ek.lower() in norm:
                return None

        keyword_matched = False
        matched_keyword = ""
        match_span: tuple[int, int] | None = None
        for kw in pattern.keywords:
            idx = norm.find(kw.lower())
            if idx >= 0:
                keyword_matched = True
                matched_keyword = kw
                match_span = (idx, idx + len(kw))
                break

        if not keyword_matched:
            return None

        extracted = {}
        for param_name, spec in pattern.params.items():
            value = ParamExtractor.extract(original, spec, match_span)
            if value is not None:
                extracted[param_name] = value

        pos_score = 1.0 - (match_span[0] / max(len(norm), 1)) if match_span else 0.5
        kw_len_score = min(1.0, len(matched_keyword) / 10.0)
        param_score = len(extracted) / max(len(pattern.params), 1) if pattern.params else 0.8

        raw_confidence = (
            0.3 * pos_score +
            0.2 * kw_len_score +
            0.3 * param_score +
            0.2 * pattern.confidence
        )
        match_confidence = raw_confidence * pattern.confidence

        return PatternMatchResult(
            pattern=pattern,
            extracted_params=extracted,
            match_confidence=match_confidence,
        )

    def _build_decision(self, match: PatternMatchResult, original: str, t0: float) -> CerebellumDecision | None:
        p = match.pattern
        args = dict(match.extracted_params)

        for param_name, spec in p.params.items():
            if isinstance(spec, dict) and spec.get("type") == "rest":
                if param_name not in args or not args[param_name]:
                    rest = ParamExtractor.rest(original, (0, 0))
                    if rest:
                        args[param_name] = rest

        tool_call_id = f"cb_{uuid.uuid4().hex[:12]}"
        tool_calls = [{
            "id": tool_call_id,
            "name": p.tool,
            "args": args,
        }]

        response = p.response_template if p.response_template else "{result}"
        response = self._format_template(response, args)

        dur = (time.time() - t0) * 1000

        return CerebellumDecision(
            tool_calls=tool_calls,
            response=response,
            pattern_name=p.name,
            match_confidence=match.match_confidence,
            duration_ms=dur,
        )

    @staticmethod
    def _format_template(template: str, params: dict) -> str:
        result = template
        for k, v in params.items():
            placeholder = "{" + k + "}"
            if placeholder in result:
                result = result.replace(placeholder, str(v))
        return result

    def format_result(self, decision: CerebellumDecision, tool_results: dict[str, str]) -> str:
        response = decision.response
        result_text = tool_results.get(decision.tool_calls[0]["name"], str(tool_results))
        if "{result}" in response:
            response = response.replace("{result}", result_text[:2000])
        return response

    def learn(self, user_message: str, tool_calls: list[dict] | None,
              success: bool = True) -> str | None:
        if not tool_calls or not success:
            return None
        norm = self._normalize(user_message)
        if len(norm) < 5:
            return None
        if len(tool_calls) > 1:
            return None

        tc = tool_calls[0]
        tool_name = tc["name"]

        for p in self._patterns.values():
            if p.tool == tool_name and p.enabled:
                return p.name

        pattern_name = f"learned_{tool_name}_{uuid.uuid4().hex[:6]}"
        keywords = self._extract_keywords_from_message(user_message, tool_name)

        new_pattern = Pattern(
            name=pattern_name,
            description=f"Learned: {user_message[:60]}",
            keywords=keywords[:5],
            tool=tool_name,
            params=self._identify_key_parameters(tool_name, tc.get("args", {})),
            response_template=f"Tool {tool_name}:\n\n{{result}}",
            confidence=0.5,
            usage_count=1,
            success_count=1,
        )

        self._patterns[pattern_name] = new_pattern
        self._save_learned_patterns()
        _log.info("cerebellum_learned pattern=%s tool=%s", pattern_name, tool_name)
        return pattern_name

    @staticmethod
    def _identify_key_parameters(tool_name: str, args: dict) -> dict:
        key_params = {}
        param_names = list(args.keys())
        if param_names:
            first = param_names[0]
            val = args[first]
            if isinstance(val, str) and val.startswith(("/", ".", "~", "C:")):
                key_params[first] = {"type": "static", "value": val}
        return key_params

    @staticmethod
    def _extract_keywords_from_message(message: str, tool_name: str) -> list[str]:
        keywords = [tool_name]
        words = message.strip().split()
        for w in words[:3]:
            w_clean = w.strip(".,!?;:'\"()[]{}").lower()
            if len(w_clean) > 2 and w_clean not in keywords:
                keywords.append(w_clean)
        return keywords

    def report_result(self, pattern_name: str, success: bool):
        pattern = self._patterns.get(pattern_name)
        if pattern:
            pattern.record_hit(success)
            if not success:
                self._stats["errors"] += 1
            self._save_learned_patterns()

    def add_pattern(self, pattern: Pattern):
        self._patterns[pattern.name] = pattern
        _log.info("cerebellum_add_pattern name=%s tool=%s", pattern.name, pattern.tool)

    def remove_pattern(self, name: str):
        self._patterns.pop(name, None)
        self._save_learned_patterns()

    def get_pattern(self, name: str) -> Pattern | None:
        return self._patterns.get(name)

    def list_patterns(self, include_disabled: bool = False) -> list[dict]:
        result = []
        for p in sorted(self._patterns.values(), key=lambda x: x.usage_count, reverse=True):
            if not include_disabled and not p.enabled:
                continue
            d = p.to_dict()
            d["success_rate"] = round(p.success_rate, 3)
            result.append(d)
        return result

    def stats(self) -> dict:
        s = dict(self._stats)
        s["pattern_count"] = len(self._patterns)
        s["enabled_pattern_count"] = sum(1 for p in self._patterns.values() if p.enabled)
        s["hit_rate"] = round(s["hits"] / max(s["total_attempts"], 1), 3)
        s["avg_decision_time_ms"] = round(
            s["total_decision_time_ms"] / max(s["total_attempts"], 1), 2
        )
        s["by_tool"] = {}
        for p in self._patterns.values():
            if p.tool not in s["by_tool"]:
                s["by_tool"][p.tool] = {"usage": 0, "success": 0}
            s["by_tool"][p.tool]["usage"] += p.usage_count
            s["by_tool"][p.tool]["success"] += p.success_count
        return s

    def reset_stats(self):
        self._stats = {
            "total_attempts": 0, "hits": 0, "misses": 0, "errors": 0,
            "total_decision_time_ms": 0.0, "by_tool": {},
        }

    def reset_learned(self):
        to_remove = [name for name in self._patterns if name.startswith("learned_")]
        for name in to_remove:
            del self._patterns[name]
        self._save_learned_patterns()
        _log.info("cerebellum_reset_learned removed=%d", len(to_remove))
