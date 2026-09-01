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

Build transforms the reviewed Planning result for a Functional Set into actual repository state.

## Inputs

Build consumes the Functional Set's Planning outputs, including the Plan and normative requirements.

Design remains the semantic source behind the work even though the Plan is Build's immediate technical specification.

## Responsibilities

Build produces the source code, configuration, tests, generated artifacts, documentation changes, and other repository mutations needed to realize the Functional Set.

Build owns implementation correctness and ordinary code-level decisions.

Build also implements the mechanical Validation tasks required by Planning's evaluation classification, binds those tasks to the normative requirements they enforce, and records the exact bindings in the canonical Requirement Evaluation Manifest.

Build may make local implementation choices needed to realize the Plan correctly, including refactoring and integration decisions that do not change intended semantics, architecture, Functional Set scope, or normative obligations.

Build should prefer the simplest implementation that faithfully realizes the reviewed Planning result and Design intent.

## Boundaries

Build does not own missing Design meaning.

Build does not invent consequential architecture or technical intent that Planning should have resolved.

Build does not create or amend normative requirements merely through implementation behavior.

Build does not broaden the Functional Set merely because additional work appears convenient.

When implementation exposes a defect in an upstream decision, the work is routed back to the stage that owns that decision rather than silently repaired downstream.

A semantic defect returns to Design. A technical specification or normative distillation defect returns to Planning. An implementation defect remains in Build.

## Further Design

Build is decomposed into the following child Design documents:

- DP-031 — Implementation Realization Architecture
- DP-032 — Mechanical Enforcement Construction Architecture

These documents separate physical implementation from construction and binding of mechanical enforcement while leaving execution to Validation.

## Build Review

Build Review evaluates the realized repository state against both Planning and Design.

The review determines whether the Build faithfully realizes the Plan and normative requirements, preserves the underlying Design meaning, stays within Functional Set scope, avoids accidental semantic or architectural drift, and completes required mechanical requirement-to-task bindings.

Build Review is also the semantic evaluation point for normative requirements routed to Semantic Review when those requirements concern the realized Build.

Build Review is iterative. Implementation findings are corrected in Build, while upstream defects are routed back to Planning or Design.
