---
doc_id: DP-031
title: Implementation Realization Architecture
depends_on:
  - DP-030
  - DP-021
  - DP-022
  - DP-023
---

# Implementation Realization Architecture

## Purpose

Implementation realization is the part of Build that turns the reviewed Planning result into working repository state.

It owns the physical implementation of the Functional Set without changing the meaning, scope, technical intent, or normative obligations established upstream.

## Inputs

Implementation consumes the Functional Set, Plan, and normative requirements.

The Plan is the immediate technical specification.

Design remains the semantic source and must still be preserved when implementation choices are made.

## Responsibilities

Implementation may create, modify, delete, refactor, integrate, or regenerate repository content as needed to realize the Functional Set.

This may include source code, configuration, documentation, generated artifacts, tests, packaging, build logic, and other repository state.

Build owns ordinary code-level decisions needed to produce a correct implementation.

Local implementation choices are allowed when they preserve:

- Design meaning;
- Plan intent;
- normative requirements; and
- Functional Set scope.

## Upstream Boundaries

Implementation does not invent missing semantic meaning.

Implementation does not invent consequential architecture or technical intent that Planning should have resolved.

Implementation does not create or amend normative requirements merely because repository behavior, tests, or implementation details exist.

Implementation does not broaden the Functional Set for convenience.

When correct implementation requires an upstream decision to change, the work returns to the stage that owns that decision.

## Correctness

Implementation correctness includes producing repository state that is internally coherent, technically functional, and faithful to Planning and Design.

Correctness may require local refactoring or integration work that was not enumerated by the Plan when that work is an ordinary implementation consequence rather than a new technical or semantic decision.

## Simplicity

Implementation should prefer the simplest solution that faithfully realizes the reviewed Planning result and Design intent.

Complexity is justified only when it materially preserves required behavior, correctness, constraints, architecture, or necessary agent control.
