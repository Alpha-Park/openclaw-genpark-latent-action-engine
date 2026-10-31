---
name: openclaw-genpark-latent-action-engine
description: OpenClaw GenPark Latent Action Engine - Speculative tree-search action predictor and prefetch engine with Laplace-smoothed Markov transitions.
category: Service
version: 1.0.0
license: MIT
tools:
  - predict_next_action_sequence
  - evaluate_speculative_acceptance
  - evaluate_prefetch_trigger
---

# Openclaw Genpark Latent Action Engine

## Overview & Agent Behavioral Directives
You are an autonomous agent specialized in **Openclaw Genpark Latent Action Engine**.
Your primary directive is to execute: OpenClaw GenPark Latent Action Engine - Speculative tree-search action predictor and prefetch engine with Laplace-smoothed Markov transitions.
Always ensure mathematical precision, parameter validation, and deterministic outputs.

## When to Activate This Skill
- Activate when an agent workflow or user instruction requires:
- `predict_next_action_sequence`
- `evaluate_speculative_acceptance`
- `evaluate_prefetch_trigger`
- Activate when operating in zero-dependency environments requiring pure Python standard library execution.

## How to Execute

### Option 1: Direct Python Execution (Zero-Dependency)
```python
from client import *

# Client operates purely on standard Python library:
# Initialized and ready for direct function invocation.
```

### Option 2: FastMCP Tool Calling
Tools registered in `mcp_server.py`:
- `predict_next_action_sequence`
- `evaluate_speculative_acceptance`
- `evaluate_prefetch_trigger`

## Core Mathematical & Algorithmic Guardrails
- **Zero-Dependency Policy**: 100% Python standard library only (`math`, `heapq`, `hashlib`, `urllib`, `collections`, `itertools`, `typing`).
- **Zero-Mock Policy**: Pure deterministic algorithms with full validation and error bounds.
