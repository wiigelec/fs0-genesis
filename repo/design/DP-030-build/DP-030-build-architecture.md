---
doc_id: DP-030
title: Build Architecture
depends_on:
  - DP-001
  - DP-010
  - DP-020
---

# Build Architecture

## Purpose

Build is the physical realization of reviewed Design and Planning.

It transforms one Functional Set into repository state while preserving Design meaning, Planning intent, normative obligations, and Functional Set scope.

## Architecture

Build has two distinct responsibilities:

- realize the implementation; and
- construct and bind mechanical enforcement required by Planning's evaluation classification.

Build owns implementation correctness and ordinary code-level decisions.

Design remains the semantic source; the Plan is the immediate technical specification.

## Further Design

Build is decomposed into:

- DP-031 — Implementation Realization Architecture
- DP-032 — Mechanical Enforcement Construction Architecture

DP-031 owns physical implementation.

DP-032 owns creation of mechanical enforcement tasks and their exact requirement bindings. Validation owns execution of those tasks.

## Boundaries

Build does not invent missing Design meaning, consequential Planning decisions, new normative obligations, or broader Functional Set scope.

When implementation exposes an upstream defect, the work returns to the stage that owns the defective decision.

## Review

Build Review evaluates realized repository state against both Planning and Design.

It checks implementation fidelity, semantic preservation, scope, unintended additions or omissions, architectural drift, semantic normative requirements applicable to realized Build state, and completion of required mechanical bindings.
