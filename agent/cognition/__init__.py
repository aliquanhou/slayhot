"""SlayHot cognitive architecture module.

Three subsystems of the Dual-Cognition theoretical framework:

  Cerebrum (Brain)     - LLM-driven explicit reasoning (agent/core.py)
  Cerebellum            - Pattern-driven fast path (cognition/cerebellum.py)
  Router                - Dynamic routing engine (cognition/router.py)
"""

from .cerebellum import (
    Cerebellum,
    CerebellumDecision,
    Pattern,
    PatternMatchResult,
)
from .router import (
    Router,
    RoutingDecision,
    RoutingPolicy,
    RoutingMetrics,
    ComplexityScorer,
)

__all__ = [
    "Cerebellum",
    "CerebellumDecision",
    "Pattern",
    "PatternMatchResult",
    "Router",
    "RoutingDecision",
    "RoutingPolicy",
    "RoutingMetrics",
    "ComplexityScorer",
]
