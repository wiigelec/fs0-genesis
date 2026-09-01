---
doc_id: DP-020
title: Planning Architecture
depends_on:
  - DP-001
  - DP-010
---

# Planning Architecture

## Purpose

Planning is the technical bridge between Design and Build.

Planning consumes the available Design corpus and existing repository state, selects a bounded piece of work, and develops the technical artifacts needed to implement that work without forcing Build to resolve consequential semantic or architectural decisions.

## Functional Set

The Functional Set is the bounded unit of work produced by Planning.

A Functional Set is distilled from Design; Design does not originate from a Functional Set.

Planning may select only part of the available Design corpus for one Functional Set. The selected work should form a coherent and manageable end-to-end change rather than requiring the entire Design corpus to be implemented at once.

A Functional Set provides the context that groups the Planning outputs for one bounded change.

## Planning Outputs

Planning develops several related outputs for a Functional Set.

### Plan

The Plan is the technical specification for what is to be built.

It translates selected Design into concrete technical structure, interfaces, behavior, constraints, affected implementation areas, sequencing where consequential, and other technical detail needed for Build.

The Plan should resolve consequential technical decisions while leaving ordinary code-level implementation decisions to Build.

The Plan should not become exhaustive pseudocode or file-by-file instruction unless that level of detail is materially necessary to preserve correctness or intended architecture.

### Normative Requirements

Planning develops normative requirements for the selected Functional Set.

Normative requirements express precise obligations that Build and Validation can be held against. They are derived from Design and Planning's technical interpretation of that Design.

Normative requirements do not live in the Plan. They are a distinct Planning output.

Planning may derive zero, one, or multiple normative requirements from a Design concept, and one normative requirement may represent meaning drawn from multiple Design concepts.

Normative requirement identities are assigned during Planning, not Design.

### Validation Mapping

Planning develops the intended mapping between normative requirements and their mechanical enforcement.

The canonical relationship is:

    normative requirement <-> validation task(s)

The mapping should be simple enough that a reader of a requirement can determine how it is enforced and a reader of an enforcement task can determine which requirement justifies it.

## Design Traceability

Planning must remain traceable to the Design meaning it realizes.

Traceability should be sufficient to answer where a Functional Set and its normative requirements came from without forcing Design into normative requirement syntax or requiring statement identities on every Design sentence.

The exact mechanism for Design-to-Planning traceability may be refined later, but it should remain direct and lightweight.

## Planning Boundary

Planning owns technical specification, normative distillation, and Functional Set scope.

Planning does not own unresolved product meaning. If a consequential semantic choice is missing or ambiguous, work returns to Design.

Planning also does not own ordinary implementation correctness. Build realizes the Plan and may choose ordinary code-level details that do not alter the intended technical or semantic result.

## Plan Review

Plan Review evaluates the complete Planning result against Design.

Review determines whether the Functional Set is appropriately bounded, the Plan faithfully translates the selected Design, the normative requirements capture the obligations needed to realize that Design, and the planned validation is sufficient for mechanically enforceable requirements.

Plan Review is iterative. Findings are corrected in Planning or routed back to Design when the defect is semantic.
