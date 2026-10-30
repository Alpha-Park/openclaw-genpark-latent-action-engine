# -*- coding: utf-8 -*-
import sys, json
from client import OpenClawGenParkLatentActionEngine

client = OpenClawGenParkLatentActionEngine()

TOOLS = [
    {
        "name": "predict_next_action_sequence",
        "description": "Calculates Laplace-smoothed Markov transition probabilities for speculative action prediction.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "action_history": {"type": "array", "items": {"type": "string"}},
                "transition_counts": {"type": "object"},
                "top_k": {"type": "integer"}
            },
            "required": ["action_history", "transition_counts"]
        }
    },
    {
        "name": "evaluate_speculative_acceptance",
        "description": "Evaluates speculative draft acceptance probability and end-to-end latency speedup.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "draft_probability": {"type": "number"},
                "target_probability": {"type": "number"},
                "draft_latency_ms": {"type": "number"},
                "target_latency_ms": {"type": "number"}
            },
            "required": ["draft_probability", "target_probability"]
        }
    },
    {
        "name": "evaluate_prefetch_trigger",
        "description": "Determines whether to fire early asynchronous prefetch based on confidence threshold.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "predicted_actions": {"type": "array", "items": {"type": "object"}},
                "confidence_threshold": {"type": "number"}
            },
            "required": ["predicted_actions"]
        }
    }
]

def handle_request(req):
    method = req.get("method")
    rid = req.get("id")
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}}
    elif method == "tools/call":
        params = req.get("params", {})
        tname = params.get("name")
        args = params.get("arguments", {})
        if tname == "predict_next_action_sequence":
            res = client.predict_next_action_sequence(args["action_history"], args["transition_counts"], args.get("top_k", 3))
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "evaluate_speculative_acceptance":
            res = client.evaluate_speculative_acceptance(args["draft_probability"], args["target_probability"], args.get("draft_latency_ms", 15.0), args.get("target_latency_ms", 120.0))
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "evaluate_prefetch_trigger":
            res = client.evaluate_prefetch_trigger(args["predicted_actions"], args.get("confidence_threshold"))
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "Method not found"}}
    return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32600, "message": "Invalid Request"}}

def main():
    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
