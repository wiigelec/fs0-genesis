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

Build is the physical manifestation of Design and Planning.

Build transforms the accepted Planning result for a Functional Set into actual repository state.

## Inputs

Build consumes the Functional Set's Planning outputs, including the Plan and normative requirements.

Design remains the semantic source behind the work even though the Plan is Build's immediate technical specification.

## Responsibilities

Build produces the source code, configuration, tests, generated artifacts, documentation changes, and other repository mutations needed to realize the Functional Set.

Build owns implementation correctness and ordinary code-level decisions.

Build may make local implementation choices needed to realize the Plan correctly, including refactoring and integration decisions that do not change intended semantics, architecture, Functional Set scope, or normative obligations.

## Boundaries

Build does not own missing Design meaning.

Build does not invent consequential architecture or technical intent that Planning should have resolved.

Build does not broaden the Functional Set merely because additional work appears convenient.

When implementation exposes a defect in an upstream decision, the work is routed back to the stage that owns that decision rather than silently repaired downstream.

A semantic defect returns to Design. A technical specification defect returns to Planning. An implementation defect remains in Build.

## Build Review

Build Review evaluates the realized repository state against both Planning and Design.

The review determines whether the Build faithfully realizes the Plan, satisfies the Functional Set's intended meaning, stays within scope, and avoids accidental semantic or architectural drift.

Build Review is iterative. Implementation findings are corrected in Build, while upstream defects are routed back to Planning or Design.
