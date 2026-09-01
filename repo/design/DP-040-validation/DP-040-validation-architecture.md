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

Planning classifies each normative requirement as mechanical, semantic, or both.

Build constructs the concrete mechanical enforcement and records exact requirement-to-task bindings in the durable Requirement Evaluation Manifest.

The manifest is repository state outside the lifecycle document hierarchy. It exists to make concrete mechanical enforcement traceable, not to contain or own Planning intent.

Validation consumes the manifest and the referenced enforcement tasks, executes the applicable checks against candidate repository state, and interprets their mechanical pass or fail result.

Only reliably mechanically decidable obligations belong in mechanical Validation.

## Further Design

Validation is decomposed into:

- DP-041 — Validation Execution Architecture

DP-041 defines execution, result meaning, and failure routing.

## Boundaries

Validation is proportional to the behavior and risk it protects.

Project-native test and validation mechanisms should be reused when they can enforce the required obligation reliably.

Semantic completeness, faithful interpretation, unnecessary complexity, scope meaning, and other non-mechanical judgments remain with Semantic Review.

Passing Validation is a gate condition, not acceptance and not a separate durable lifecycle result.

All required mechanical validation applicable to the candidate must pass before the candidate is eligible for acceptance. Optional diagnostic, exploratory, performance, development, or informational checks do not become acceptance gates unless Planning establishes a normative obligation that makes them required.
