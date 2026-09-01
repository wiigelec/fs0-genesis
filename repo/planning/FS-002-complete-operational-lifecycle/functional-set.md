---
functional_set: FS-002
title: Complete Operational Lifecycle
design_revision: 70be6472ee3f77ecc8f91ef325af4a855679b6bf
---

# FS-002 — Complete Operational Lifecycle

## Purpose

FS-001 established and accepted the repository lifecycle substrate.

FS-002 completes that substrate for normal repeated use. It removes bootstrap-only assumptions that tie the implementation to FS-001 and ensures that subsequent Functional Sets can move through Planning, Build, Validation, Semantic Review, and Acceptance without requiring framework changes merely to participate in the lifecycle.

The goal is not to add another framework layer. The goal is to finish the smallest operational mechanism implied by the accepted Design so the repository can stop developing lifecycle infrastructure and start using it.

## Selected Design

Planning consumes Design at repository revision `70be6472ee3f77ecc8f91ef325af4a855679b6bf`.

Selected Design scope:

- DP-001 — Repository Development Lifecycle
- DP-010 — Design Architecture
- DP-011 — Semantic Decomposition Architecture
- DP-012 — Design Corpus Architecture
- DP-020 — Planning Architecture
- DP-021 — Functional Set Architecture
- DP-022 — Plan Architecture
- DP-023 — Normative Requirements Architecture
- DP-030 — Build Architecture
- DP-031 — Mechanical Enforcement Construction Architecture
- DP-040 — Validation Architecture
- DP-050 — Semantic Review Architecture
- DP-051 — Stage Review Architecture
- DP-052 — Review Convergence Architecture
- DP-060 — Acceptance Architecture

## Existing Repository State

At the selected Design state:

- FS-001 is accepted and provides the canonical lifecycle surfaces.
- `main` represents accepted state.
- `repo/design/`, `repo/planning/`, and `repo/specs/` provide canonical Design and Planning state.
- `repo/validation/requirement-evaluation.json` provides direct mechanical requirement-to-task bindings.
- `repo/scripts/validate` is the canonical mechanical Validation entry point.
- CI delegates to the canonical Validation entry point.
- the current project-native validator is still bootstrap-specific in several places, including direct FS-001 Planning/specification paths and FS-001-specific requirement parsing/count assumptions.
- no separate Functional Set registry, lifecycle database, review database, or acceptance database exists.

## Functional Set Boundary

FS-002 includes all remaining framework work needed for ordinary repeated lifecycle use:

- discover current Functional Sets directly from canonical Planning/specification surfaces;
- validate Planning/specification correspondence and Functional Set identity generically;
- validate exact Design bindings generically;
- parse normative requirements and evaluation classifications generically across current Functional Sets;
- evaluate Requirement Evaluation Manifest integrity across the aggregate current requirement set;
- preserve direct requirement-to-project-native-task bindings without adding registry or provenance layers;
- preserve one canonical Validation entry point and CI delegation;
- remove remaining validator assumptions that require source changes merely to recognize a later conforming Functional Set;
- ensure lifecycle documentation and agent guidance describe the completed operational behavior where clarification is actually needed;
- provide regression coverage sufficient to demonstrate that a later Functional Set can participate without modifying framework source merely to name it;
- retain FS-001 as accepted historical Planning and current applicable normative state.

FS-002 excludes:

- new product functionality unrelated to lifecycle operation;
- automatic generation or approval of Design, Planning, Build, review, or Acceptance artifacts;
- a Functional Set registry or lifecycle authority database;
- provenance graphs, correspondence graphs, evidence stores, adjudication systems, or parallel acceptance records;
- mechanical evaluation of semantic-only requirements;
- migration or revival of `repo_old/` behavior;
- universal validation/plugin/framework infrastructure;
- implementation abstractions whose only purpose is anticipated future extensibility;
- rewriting the historical meaning of accepted FS-001 requirements.

## Completion Criterion

After FS-002 is accepted, the lifecycle framework should be considered operationally complete for the current Design.

A subsequent Functional Set should normally represent actual repository/product work rather than additional lifecycle-framework construction.

Further lifecycle-framework work should occur only when real use exposes a concrete missing or defective capability that cannot be corrected as an ordinary implementation detail.

## Planning Outputs

This Functional Set produces:

- `repo/planning/FS-002-complete-operational-lifecycle/functional-set.md`
- `repo/planning/FS-002-complete-operational-lifecycle/plan.md`
- `repo/specs/FS-002-complete-operational-lifecycle.md`
