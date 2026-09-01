---
functional_set: FS-001
title: Framework Lifecycle Substrate
design_revision: c1012693f67584ec723c572fcce8d4c5ae7e12a8
---

# FS-001 — Framework Lifecycle Substrate

## Purpose

Establish the minimum durable repository substrate needed to operate the redesigned Design → Planning → Build → Validation → Semantic Review → Acceptance lifecycle without recreating the retired Governance, Conformance, or Assurance framework machinery.

## Design Binding

Planning is bound to Design revision:

`c1012693f67584ec723c572fcce8d4c5ae7e12a8`

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

The complete lifecycle scope is selected because this Functional Set establishes the minimal repository substrate through which later Functional Sets will traverse that lifecycle.

This does not authorize generalized framework machinery beyond what the selected Design requires.

## Existing Repository State

The development branch currently contains:

- the redesigned canonical Design corpus under `repo/design/`;
- historical framework implementation and planning state under `repo_old/`;
- `README.md` describing the former Governance / Conformance / Assurance architecture;
- `AGENTS.md` containing former authority and Governance terminology; and
- `.github/workflows/fs0-conformance.yml`, which invokes the former Conformance runtime.

`repo_old/` is implementation history and design evidence only. It is not normative input to FS-001.

Existing behavior shall not be retained merely because the previous framework implemented it.

## Functional Set Boundary

FS-001 establishes only what is required to make the redesigned lifecycle operational:

- preserve `repo/design/` as the canonical Design corpus;
- establish durable storage for Functional Set Planning outputs;
- establish durable representation of normative requirements and their evaluation classifications;
- establish the Requirement Evaluation Manifest location and representation;
- establish one project-native Validation entry point;
- align repository orientation and agent guidance with the redesigned lifecycle;
- align CI with Validation terminology and the canonical Validation entry point; and
- prevent obsolete active-path Governance, Conformance, Assurance, and Genesis-runtime descriptions from being mistaken for current framework behavior.

## Out of Scope

FS-001 does not:

- recreate generalized authority databases;
- recreate provenance or correspondence graphs;
- recreate governed evidence stores;
- recreate adjudication machinery;
- recreate the former Conformance runtime;
- migrate old normative requirements automatically;
- make `repo_old/` authoritative;
- require statement-level Design identities;
- introduce a universal test or validation framework;
- define future product functionality;
- establish independent approval roles;
- create durable Semantic Review findings;
- create a separate Acceptance record; or
- delete `repo_old/` merely for cosmetic cleanup.

## Planning Outputs

FS-001 produces:

- `functional-set.md` — selected scope and exact Design binding;
- `plan.md` — consequential technical realization decisions; and
- `repo/specs/FS-001-framework-lifecycle-substrate.md` — canonical normative specification and evaluation classifications.

The Functional Set and Plan are durable Planning artifacts.

The normative specification is a Planning output stored in the canonical specification corpus under `repo/specs/`.

These outputs remain in repository history after Acceptance.

They record how accepted repository state was planned and specified but do not become Design and do not acquire authority from implementation behavior.
