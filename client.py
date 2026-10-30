# -*- coding: utf-8 -*-
"""
OpenClaw GenPark Latent Action Engine - Speculative Tree-Search Action Predictor & Prefetch Engine
Standard Library only: math, typing.
Calculates Laplace-smoothed Markov transition probabilities for speculative next-tool call prediction,
evaluates speculative draft acceptance ratios and speedup factors, and triggers automated prefetching.
"""

import math
from typing import Dict, List, Any

class OpenClawGenParkLatentActionEngine:
    def __init__(self, prefetch_confidence_threshold: float = 0.75):
        self.thresh = prefetch_confidence_threshold

    def predict_next_action_sequence(self, action_history: List[str],
                                    transition_counts: Dict[str, Dict[str, int]],
                                    top_k: int = 3) -> Dict[str, Any]:
        """
        Predicts next agent action given preceding action using Laplace-smoothed transition probabilities:
        P(a_{t+1} | a_t) = (Count(a_t, a_{t+1}) + 1) / ( sum_{a'} (Count(a_t, a') + 1) )
        """
        if not action_history:
            return {"predicted_next_actions": []}

        last_action = action_history[-1]
        transitions = transition_counts.get(last_action, {})

        # Vocabulary of observed actions
        all_actions = set(transitions.keys())
        for sub in transition_counts.values():
            all_actions.update(sub.keys())

        V = max(1, len(all_actions))
        total_counts = sum(transitions.values()) + V # denominator with +1 per action

        probs = []
        for act in all_actions:
            c = transitions.get(act, 0)
            p = (c + 1.0) / total_counts
            probs.append({"action": act, "probability": round(p, 4), "empirical_count": c})

        probs.sort(key=lambda x: x["probability"], reverse=True)

        return {
            "last_action_executed": last_action,
            "vocabulary_size": V,
            "top_predicted_actions": probs[:top_k],
            "highest_confidence_prediction": probs[0] if probs else None
        }

    def evaluate_speculative_acceptance(self, draft_probability: float,
                                        target_probability: float,
                                        draft_latency_ms: float = 15.0,
                                        target_latency_ms: float = 120.0) -> Dict[str, Any]:
        """
        Evaluates speculative execution acceptance probability:
        alpha = min(1.0, P_target / max(1e-6, P_draft))
        Speedup factor: S = TargetLatency / (DraftLatency + (1 - alpha) * TargetLatency)
        """
        p_d = max(1e-6, min(1.0, draft_probability))
        p_t = max(0.0, min(1.0, target_probability))

        alpha = min(1.0, p_t / p_d)
        expected_latency_ms = draft_latency_ms + (1.0 - alpha) * target_latency_ms
        theoretical_speedup = target_latency_ms / max(1.0, expected_latency_ms)

        return {
            "draft_probability": p_d,
            "target_probability": p_t,
            "acceptance_probability_alpha": round(alpha, 4),
            "expected_execution_latency_ms": round(expected_latency_ms, 2),
            "baseline_target_latency_ms": target_latency_ms,
            "speculative_speedup_ratio": round(theoretical_speedup, 2),
            "is_speculation_favorable": theoretical_speedup > 1.25
        }

    def evaluate_prefetch_trigger(self, predicted_actions: List[Dict[str, Any]],
                                  confidence_threshold: float = None) -> Dict[str, Any]:
        """
        Decides whether to trigger asynchronous background data prefetching based on top action probability.
        """
        thresh = confidence_threshold if confidence_threshold is not None else self.thresh
        if not predicted_actions:
            return {"trigger_prefetch": False, "reason": "No predictions"}

        top = predicted_actions[0]
        prob = top.get("probability", 0.0)
        action_name = top.get("action", "unknown")

        trigger = prob >= thresh

        return {
            "candidate_action": action_name,
            "confidence_probability": prob,
            "threshold": thresh,
            "trigger_prefetch": trigger,
            "action_dispatch": f"DISPATCH_ASYNC_PREFETCH_{action_name.upper()}" if trigger else "DEFER_PREFETCH_UNTIL_CONFIRMED"
        }
