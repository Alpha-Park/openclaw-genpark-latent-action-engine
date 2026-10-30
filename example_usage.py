# -*- coding: utf-8 -*-
from client import OpenClawGenParkLatentActionEngine

engine = OpenClawGenParkLatentActionEngine(prefetch_confidence_threshold=0.60)

# 1. Action Sequence Prediction
history = ["SEARCH_CATALOG", "PARSE_SKU"]
transitions = {
    "SEARCH_CATALOG": {"PARSE_SKU": 25, "FILTER_CATEGORY": 5},
    "PARSE_SKU": {"FETCH_PRICING": 40, "CHECK_INVENTORY": 10, "VIEW_REVIEWS": 2}
}
preds = engine.predict_next_action_sequence(history, transitions, top_k=3)
print(f"Top Next Action: {preds['highest_confidence_prediction']['action']} (P={preds['highest_confidence_prediction']['probability']})")

# 2. Speculative Execution Speedup
spec = engine.evaluate_speculative_acceptance(draft_probability=0.75, target_probability=0.70, draft_latency_ms=12.0, target_latency_ms=150.0)
print(f"\nSpeculative Speedup: {spec['speculative_speedup_ratio']}x (Acceptance Alpha: {spec['acceptance_probability_alpha']}, Favorable: {spec['is_speculation_favorable']})")

# 3. Prefetch Trigger Decision
prefetch = engine.evaluate_prefetch_trigger(preds['top_predicted_actions'])
print(f"\nPrefetch Evaluation: Trigger={prefetch['trigger_prefetch']} -> {prefetch['action_dispatch']}")
