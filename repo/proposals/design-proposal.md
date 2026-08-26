---
doc_id: DP-001
title: Design Proposal Architecture
status: planning-ready
depends_on: []
artifact_type: design-proposal
canonical_format: markdown
---

# Design Proposal Architecture

## Status

**Section ID:** `STATUS`

**DP001-STATUS-001**
Planning-ready Design Proposal.

## Purpose

**Section ID:** `PURPOSE`

**DP001-PURPOSE-001**
Define the canonical durable Design artifact and the structural contract used to make Design machine-addressable without turning Design into a generated machine representation.

## Context

**Section ID:** `CONTEXT`

**DP001-CONTEXT-001**
Design is an iterative user/AI process that may span multiple interactions, sessions, and revisions. Large products may use multiple bounded Design Proposals and may add new Design Proposals after implementation has begun.

**DP001-CONTEXT-002**
Planning consumes exact Design Proposal revisions, selects a bounded functional set, and retains autonomy to distill repository normative requirements and implementation intent from the selected Design.

## Goals

**Section ID:** `GOALS`

**DP001-GOALS-001**
- Make Markdown the canonical maintained Design Proposal source.
- Give each proposal a stable `DP-NNN` document identity.
- Give addressable Design statements stable identifiers.
- Support modular, iterative Design over the lifetime of the product.
- Preserve Planning autonomy over normative decomposition and implementation intent.

## Non-Goals

**Section ID:** `NON-GOALS`

**DP001-NON-GOALS-001**
- Define the Plan schema.
- Define FS0-Core implementation scope.
- Assign repository normative requirement identities.
- Require one-to-one mapping between Design statements and normative requirements.
- Define Build implementation details.

## Requirements

**Section ID:** `REQUIREMENTS`

**DP001-REQUIREMENTS-001**
A Design Proposal shall be a maintained human-readable Markdown artifact with a machine-readable metadata header.

**DP001-REQUIREMENTS-002**
The metadata header shall contain a stable `doc_id` in the form `DP-NNN`.

**DP001-REQUIREMENTS-003**
A planning-ready Design Proposal shall contain every required top-level section defined by this proposal.

**DP001-REQUIREMENTS-004**
Each required section shall contain substantive applicable content or explicitly state why no content applies.

**DP001-REQUIREMENTS-005**
Design shall support iterative development across multiple user/AI interactions, sessions, and revisions.

**DP001-REQUIREMENTS-006**
The durable output of Design shall be the Design Proposal itself.

**DP001-REQUIREMENTS-007**
Product Design may be divided into multiple bounded Design Proposals rather than one monolithic document.

**DP001-REQUIREMENTS-008**
A Design Proposal may declare dependencies on other Design Proposals required to interpret its semantics.

**DP001-REQUIREMENTS-009**
New Design Proposals may be introduced after product implementation has begun.

**DP001-REQUIREMENTS-010**
Each addressable Design statement shall have an explicit identifier composed from the proposal document identity, a stable section identity, and a section-local sequential number.

**DP001-REQUIREMENTS-011**
A Design statement identifier shall have the form `DPnnn-HDRID-NNN`.

**DP001-REQUIREMENTS-012**
Design statement identifiers are non-normative addresses used for discussion and functional-set scoping.

**DP001-REQUIREMENTS-013**
`functional-set.json` may select Design statement identifiers to define the Design scope of one functional set.

**DP001-REQUIREMENTS-014**
The logical Plan rooted at `plan.json` owns decomposition and distillation of selected Design into repository normative requirements and implementation intent.

**DP001-REQUIREMENTS-015**
No one-to-one cardinality or mandatory hard traceability relationship exists between a Design statement and a repository normative requirement.

**DP001-REQUIREMENTS-016**
Planning may derive zero, one, or multiple normative requirements from one Design statement and may derive one normative requirement from multiple Design statements.

**DP001-REQUIREMENTS-017**
Repository normative requirement identities shall be assigned during Planning, not Design.

**DP001-REQUIREMENTS-018**
Planning shall bind to the exact revision of every Design Proposal it consumes.

**DP001-REQUIREMENTS-019**
A later Design revision shall not silently alter an already accepted Plan.

**DP001-REQUIREMENTS-020**
A Design Proposal may continue to evolve after an earlier revision has been consumed by Planning.

**DP001-REQUIREMENTS-021**
A Design Proposal shall not ordinarily define exact mutation scope or file-by-file implementation pseudo-code unless such detail is itself an intentional semantic constraint.

**DP001-REQUIREMENTS-022**
Generated structured metadata may index or validate proposals but shall not replace Markdown as the canonical Design semantic source.

**DP001-REQUIREMENTS-023**
A Design Proposal shall use the canonical top-level header set, stable section IDs, and ordering defined by this proposal.

**DP001-REQUIREMENTS-024**
Proposal-specific organization shall appear only below `Detailed Design` as level-three or deeper headings; additional top-level level-two headings are not permitted.

**DP001-REQUIREMENTS-025**
Design Proposals shall not contain proposed repository normative requirement identities. Only Design Proposal statement identities belong to Design.

**DP001-REQUIREMENTS-026**
Planning alone assigns repository normative requirement identities when distilling selected Design into a Plan.

## Constraints

**Section ID:** `CONSTRAINTS`

**DP001-CONSTRAINTS-001**
The format shall remain practical for human and AI editing without specialized authoring tools.

**DP001-CONSTRAINTS-002**
Visible heading text may evolve while its explicit stable section identity remains unchanged.

## Architecture

**Section ID:** `ARCHITECTURE`

**DP001-ARCHITECTURE-001**
The Design layer is a collection of maintained Markdown Design Proposals connected by semantic dependencies rather than by a predetermined implementation sequence.

**DP001-ARCHITECTURE-002**
Planning audits planning-ready Design against accepted implementation and selects one bounded functional set at a time.

## Behavior

**Section ID:** `BEHAVIOR`

**DP001-BEHAVIOR-001**
A Design Proposal may progress through repeated revisions until it is planning-ready.

**DP001-BEHAVIOR-002**
Planning may consume planning-ready proposals while unrelated proposals remain unfinished or do not yet exist.

## Interfaces and Boundaries

**Section ID:** `INTERFACES`

**DP001-INTERFACES-001**
Conversation and scratch analysis may inform Design but are not durable Design artifacts.

**DP001-INTERFACES-002**
`functional-set.json` identifies selected Design statement IDs.

**DP001-INTERFACES-003**
The logical Plan document graph rooted at `plan.json` performs normative distillation, exact file scoping, pseudo-code specification, sequencing, and validation planning.

**DP001-INTERFACES-004**
Build consumes the accepted Plan and produces syntactically correct, validated, operational code.

## Invariants

**Section ID:** `INVARIANTS`

**DP001-INVARIANTS-001**
Markdown remains the canonical Design semantic source.

**DP001-INVARIANTS-002**
Design statement IDs remain non-normative.

**DP001-INVARIANTS-003**
Planning owns normative distillation and implementation intent.

**DP001-INVARIANTS-004**
Build owns implementation correctness within the accepted Plan.

## Detailed Design

**Section ID:** `DETAIL`

### Canonical Top-Level Header Contract

**DP001-DETAIL-001**
Every planning-ready Design Proposal contains exactly these level-two headers in this order:

**DP001-DETAIL-002**
1. Status
2. Purpose
3. Context
4. Goals
5. Non-Goals
6. Requirements
7. Constraints
8. Architecture
9. Behavior
10. Interfaces and Boundaries
11. Invariants
12. Detailed Design
13. Alternatives Considered
14. Risks and Tradeoffs
15. Open Questions
16. Acceptance Criteria
Their stable section IDs are:

**DP001-DETAIL-003**
`STATUS`, `PURPOSE`, `CONTEXT`, `GOALS`, `NON-GOALS`, `REQUIREMENTS`, `CONSTRAINTS`, `ARCHITECTURE`, `BEHAVIOR`, `INTERFACES`, `INVARIANTS`, `DETAIL`, `ALTERNATIVES`, `RISKS`, `OPEN-QUESTIONS`, and `ACCEPTANCE`.

**DP001-DETAIL-004**
Proposal-specific structure uses level-three or deeper headings under `Detailed Design`.

### Design Identity Boundary

**DP001-DETAIL-005**
Design Proposal statement IDs are the only requirement-like identities authored in Design.

**DP001-DETAIL-006**
Design Proposals do not preassign repository normative requirement IDs, even provisionally.

**DP001-DETAIL-007**
Planning selects DP statement IDs in `functional-set.json` and independently distills and assigns repository normative requirements in the logical Plan rooted at `plan.json`.

## Alternatives Considered

**Section ID:** `ALTERNATIVES`

**DP001-ALTERNATIVES-001**
Canonical JSON with generated Markdown was rejected because it makes the machine projection primary instead of the document authored during Design.

**DP001-ALTERNATIVES-002**
A monolithic product Design Proposal was rejected because it does not scale to large evolving products or practical AI context limits.

**DP001-ALTERNATIVES-003**
Mandatory one-to-one Design-statement-to-normative-requirement mapping was rejected because it constrains Planning's required distillation autonomy.

## Risks and Tradeoffs

**Section ID:** `RISKS`

**DP001-RISKS-001**
Markdown requires explicit structural validation for metadata, headings, section identities, and statement identities.

**DP001-RISKS-002**
Modular proposals require clear dependency declarations to avoid cross-document ambiguity.

## Open Questions

**Section ID:** `OPEN-QUESTIONS`

**DP001-OPEN-QUESTIONS-001**
No blocking Design questions remain for the Design Proposal artifact contract.

## Acceptance Criteria

**Section ID:** `ACCEPTANCE`

**DP001-ACCEPTANCE-001**
This proposal is planning-ready when Markdown canonicality, metadata, required sections, stable statement addressing, modular iteration, exact revision binding, and Planning autonomy are all unambiguous.
