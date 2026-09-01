---
doc_id: DP-050
title: Semantic Review Architecture
depends_on:
  - DP-001
  - DP-010
  - DP-020
  - DP-030
  - DP-040
---

# Semantic Review Architecture

## Purpose

Semantic Review evaluates whether meaning is preserved across Design, Planning, and Build.

It addresses questions that cannot be reliably reduced to mechanical Validation, including completeness, faithful interpretation, ambiguity, unnecessary complexity, and semantic drift.

Semantic Review also evaluates normative requirements that Planning routes to semantic evaluation.

Semantic Review occurs after each major lifecycle stage and is normally iterative.

## Design Review

Design Review evaluates Design for semantic completeness.

It looks for missing meaning, ambiguity, contradiction, unresolved consequential decisions, unnecessary complexity, and failure to faithfully capture human intent.

When material issues are found, Design is revised and reviewed again.

## Plan Review

Plan Review evaluates the complete Planning result against Design.

It checks whether the Functional Set is appropriately bounded, whether the Plan completely and faithfully translates the selected Design, whether normative requirements express the obligations needed to realize that Design, and whether each normative requirement is classified for an appropriate mechanical or semantic evaluation mode.

A semantic defect is routed back to Design. A technical Planning or normative distillation defect is corrected in Planning.

## Build Review

Build Review evaluates the Build against both Planning and Design.

The Plan is the immediate technical specification, but Design remains the semantic reference.

Build Review looks for implementation drift, omissions, unintended additions, scope expansion, accidental architectural changes, and cases where a technically followed Plan still fails to realize the underlying Design meaning.

Build Review also evaluates semantic normative requirements whose subject is the realized Build.

## Semantic Requirement Evaluation

A normative requirement may be routed to Semantic Review when its obligation cannot be decided reliably by mechanical Validation.

Semantic evaluation determines whether the reviewed subject satisfies the meaning of the requirement without converting that judgment into an artificial executable predicate.

A semantic requirement may also have mechanical Validation where part of its obligation is mechanically decidable.

Semantic routing does not require persistent review-case identities, rubrics, evidence manifests, finding identities, disposition records, or a separate semantic enforcement hierarchy.

## Iteration and Convergence

Semantic Review may require several passes.

Each pass identifies material discrepancies, routes them to the stage that owns the defective decision, and re-evaluates the corrected result.

Review converges when no unresolved material semantic discrepancies remain for the stage being reviewed.

## Challenge and Simplicity

Semantic Review should challenge the proposed solution rather than merely verify internal consistency.

Review should consider whether important assumptions were invented, whether meaningful alternatives were ignored, whether unnecessary complexity has accumulated, and whether a materially simpler solution could preserve the same intent, required behavior, correctness, necessary constraints, and necessary control of the AI agent.

Agreement between user and agent is not evidence that a solution is correct.

Complexity introduced primarily to support prior framework complexity is itself a reason to reconsider the earlier mechanism.

## Records

Semantic Review is a working process, not a durable governance artifact.

Review findings may be recorded temporarily when useful for iteration, but the framework does not require review-case identities, correspondence graphs, disposition records, or persistent review histories.

If review does not converge, the work is not merged.
