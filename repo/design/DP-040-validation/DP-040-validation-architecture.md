---
doc_id: DP-040
title: Validation Architecture
depends_on:
  - DP-001
  - DP-020
  - DP-030
---

# Validation Architecture

## Purpose

Validation mechanically evaluates the mechanically decidable portions of normative requirements and helps bound the AI agent.

Validation does not define normative intent. Its enforcement basis comes from Planning, while Build constructs the executable checks and their requirement bindings.

## Architecture

The Requirement Evaluation Manifest identifies how normative requirements are evaluated.

Planning classifies each requirement as mechanical, semantic, or both.

Build records the exact requirement-to-task bindings for mechanically evaluated obligations.

Validation executes those tasks against candidate repository state and interprets their mechanical pass or fail result.

Only reliably mechanically decidable obligations belong in mechanical Validation.

## Further Design

Validation is decomposed into:

- DP-041 — Validation Execution Architecture
- DP-042 — Validation Gate Architecture

DP-041 defines execution and failure routing.

DP-042 defines the mechanical gate that must be satisfied before acceptance is possible.

## Boundaries

Validation is proportional to the behavior and risk it protects.

Project-native test and validation mechanisms should be reused when they can enforce the required obligation reliably.

Semantic completeness, faithful interpretation, unnecessary complexity, scope meaning, and other non-mechanical judgments remain with Semantic Review.

Passing Validation is a gate condition, not acceptance and not a separate durable lifecycle result.
