---
doc_id: DP-024
title: Requirement Evaluation Architecture
depends_on:
  - DP-020
  - DP-023
  - DP-040
  - DP-050
---

# Requirement Evaluation Architecture

## Purpose

Requirement evaluation connects normative requirements to the way their satisfaction is determined.

Planning classifies evaluation intent. Build establishes exact mechanical bindings. Validation and Semantic Review perform the evaluation.

## Evaluation Modes

A normative requirement may require mechanical evaluation, semantic evaluation, or both.

Mechanical evaluation is used only when an obligation or portion of an obligation can be decided reliably through executable checks.

Semantic evaluation is used when satisfaction depends on meaning, interpretation, completeness, coherence, or other judgment that should not be reduced to an artificial mechanical predicate.

## Planning Responsibility

Planning assigns the evaluation mode for each normative requirement.

Planning does not need to identify exact test files, callable names, or other mechanical validator implementation details before Build creates them.

Semantic classification simply indicates that Semantic Review must evaluate the applicable obligation.

## Build Responsibility

Build implements the mechanical Validation tasks required by Planning's classification.

Build records the exact binding between each mechanically evaluated normative requirement and the actual task or tasks that enforce it.

These bindings form the mechanical portion of the canonical Requirement Evaluation Manifest.

Build carries forward semantic classification without creating a separate semantic-review artifact hierarchy.

## Requirement Evaluation Manifest

The Requirement Evaluation Manifest is the canonical record of requirement evaluation routing and exact mechanical enforcement bindings.

It should answer:

- how is this normative requirement evaluated?; and
- which normative requirement justifies this mechanical enforcement task?

The manifest should remain a direct mapping rather than becoming a generalized provenance graph, review database, or validation ontology.

## Mixed Evaluation

A requirement may legitimately use both mechanical and semantic evaluation.

The mechanical portion should enforce what can be determined reliably by executable checks.

Semantic Review should evaluate the remaining meaning without treating the mechanical result as proof of semantic completeness.

## Simplicity

Evaluation machinery should remain proportional to the obligations it protects.

New metadata or framework mechanisms should be added only when the direct requirement-to-evaluation mapping is insufficient for a concrete need.
