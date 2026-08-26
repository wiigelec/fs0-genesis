---
doc_id: DP-010
title: Framework Contract Architecture Proposal
status: planning-ready
depends_on: []
artifact_type: design-proposal
canonical_format: markdown
---

# Framework Contract Architecture Proposal

## Status

**Section ID:** `STATUS`

**DP010-STATUS-001**
Planning-ready Design Proposal.

## Purpose

**Section ID:** `PURPOSE`

**DP010-PURPOSE-001**
Define the foundational authority topology of the repository framework.

## Context

**Section ID:** `CONTEXT`

**DP010-CONTEXT-001**
The framework requires explicit authority boundaries among Governance, Conformance, Assurance, implementation, and product authority.

## Goals

**Section ID:** `GOALS`

**DP010-GOALS-001**
- Preserve the domain architecture and authority boundaries defined by this proposal.
- Make the proposal consumable by incremental functional-set Planning.
- Keep Design statement identity distinct from repository normative identity.

## Non-Goals

**Section ID:** `NON-GOALS`

**DP010-NON-GOALS-001**
- Define one complete implementation plan for the entire proposal.
- Assign repository normative IDs during Design.
- Define file-level pseudo-code in Design unless it is itself a semantic constraint.

## Requirements

**Section ID:** `REQUIREMENTS`

**DP010-REQUIREMENTS-001**
The detailed Design below contains addressable Design statements. Statement IDs are non-normative proposal references. `functional-set.json` selects them; `plan.json` owns decomposition and normative distillation.

## Constraints

**Section ID:** `CONSTRAINTS`

**DP010-CONSTRAINTS-001**
This proposal remains subordinate to its declared Design dependencies and shall not silently assume authority outside them.

## Architecture

**Section ID:** `ARCHITECTURE`

**DP010-ARCHITECTURE-001**
The detailed Design below is semantic input to Planning and may be realized over multiple functional sets.

## Behavior

**Section ID:** `BEHAVIOR`

**DP010-BEHAVIOR-001**
Planning may consume a bounded subset of this proposal in one functional set; implementation of the entire proposal in one pass is not required.

## Interfaces and Boundaries

**Section ID:** `INTERFACES`

**DP010-INTERFACES-001**
Design defines meaning. `functional-set.json` defines selected Design scope. `plan.json` defines normative decomposition and exact implementation intent. Build produces syntactically correct, validated, operational code.

## Invariants

**Section ID:** `INVARIANTS`

**DP010-INVARIANTS-001**
- Design statement IDs remain non-normative.
- Planning owns normative distillation and implementation intent.
- Build shall not invent missing Design semantics or missing Plan intent.

## Detailed Design

**Section ID:** `DETAIL`

### Objective

**DP010-DETAIL-001**
The repository framework shall define one foundational Framework Contract that authorizes and bounds three authority-bearing keystones:

**DP010-DETAIL-002**
1. Governance
2. Conformance
3. Assurance
The Framework Contract shall establish:

**DP010-DETAIL-003**
- where framework authority resides;
- what powers each keystone may exercise;
- what powers each keystone may not exercise;
- how persistent normative authority may change;
- how mechanical enforcement remains subordinate to accepted authority;
- how semantic review remains subordinate to accepted authority;
- how derived framework behavior remains traceable to accepted authority;
- how product authority remains subordinate to framework authority; and
- how authority relationships remain explicit and machine-resolvable.
The primary architectural objective is separation of responsibility under explicit accepted authority.

### Foundational Model

**DP010-DETAIL-004**
`repo/` contains accepted repository-framework normative authority.

**DP010-DETAIL-005**
The Framework Contract is the foundational normative layer within `repo/`.

**DP010-DETAIL-006**
The Framework Contract authorizes and bounds:

**DP010-DETAIL-007**
- Governance;
- Conformance; and
- Assurance.
Those keystones collectively support the governed framework and maintained product.

**DP010-DETAIL-008**
The authority topology is:

**DP010-DETAIL-009**
**repo/**
→ Framework Contract
→ Governance / Conformance / Assurance
→ governed framework and maintained product
Implementation does not acquire authority merely because it exists.

### Framework Authority

**DP010-DETAIL-010**
Framework authority is accepted normative authority that defines the repository framework.

**DP010-DETAIL-011**
Accepted repository-framework normative authority shall reside within `repo/`.

**DP010-DETAIL-012**
Framework authority may define:

**DP010-DETAIL-013**
- authority relationships;
- framework structure;
- artifact roles;
- keystone powers;
- provenance obligations;
- framework/product relationships; and
- framework evolution constraints.
Implementation may realize framework authority but shall not independently establish, extend, or amend it.

**DP010-DETAIL-014**
Normative authority shall not arise solely from:

**DP010-DETAIL-015**
- implementation behavior;
- validation behavior;
- review findings;
- generated artifacts;
- workflow convention;
- historical repository state; or
- product behavior.

### Framework Contract

**DP010-DETAIL-016**
The Framework Contract defines the foundational authority topology of the repository framework.

**DP010-DETAIL-017**
It shall establish:

**DP010-DETAIL-018**
- `repo/` as the authoritative framework namespace;
- Governance, Conformance, and Assurance as the three authority-bearing keystones;
- the authority delegated to each keystone;
- the authority prohibited to each keystone;
- the separation of keystone responsibilities;
- the permitted direction of normative authority flow;
- foundational provenance obligations;
- the prohibition against implicit authority creation;
- the relationship between framework authority and product authority; and
- requirements for explicit, resolvable authority representation;
- default-deny authorization of maintained governed state;
- single controlling semantic ownership; and
- acyclic normative authority dependency.
The Framework Contract shall remain intentionally compact.

**DP010-DETAIL-019**
It shall define authority and boundaries rather than detailed operating mechanics.

**DP010-DETAIL-020**
Subordinate framework specifications shall define how the keystones perform their authorized responsibilities.

### Authority-Bearing Keystones

**DP010-DETAIL-021**
The repository framework shall define exactly three authority-bearing keystones:

**DP010-DETAIL-022**
1. Governance
2. Conformance
3. Assurance
Supporting mechanisms may exist.

**DP010-DETAIL-023**
Supporting mechanisms shall operate only under authority delegated through accepted repository-framework authority.

**DP010-DETAIL-024**
A supporting mechanism shall not independently acquire authority equivalent to a keystone.

### Governance

**DP010-DETAIL-025**
Governance is the framework mechanism responsible for persistent normative change.

**DP010-DETAIL-026**
Governance answers:

**DP010-DETAIL-027**
**What accepted normative authority may be created, changed, superseded, or withdrawn?**
Governance may:

**DP010-DETAIL-028**
- create or change accepted framework authority;
- create or change accepted product authority; and
- consume Conformance or Assurance findings when persistent normative change is required.
Governance shall not:

**DP010-DETAIL-029**
- derive normative authority from implementation behavior;
- derive normative authority from validation behavior;
- treat Assurance findings as persistent normative authority without governed acceptance; or
- substitute workflow completion for required Conformance or Assurance.
Persistent changes to accepted normative authority shall occur only through Governance.

**DP010-DETAIL-030**
Because repository-framework authority is normative authority, persistent changes to the Framework Contract or keystone authority are themselves subject to Governance.

**DP010-DETAIL-031**
Detailed Governance lifecycle, stage, artifact, transition, and acceptance mechanics belong in the Governance Architecture Proposal.

### Conformance

**DP010-DETAIL-032**
Conformance is the framework mechanism responsible for mechanical enforcement of accepted normative authority.

**DP010-DETAIL-033**
Conformance answers:

**DP010-DETAIL-034**
**Does observable state satisfy the mechanically decidable obligations established by accepted normative authority?**
Conformance may:

**DP010-DETAIL-035**
- mechanically evaluate observable state;
- reject mechanically nonconforming state; and
- produce mechanical findings and evidence.
Conformance shall not:

**DP010-DETAIL-036**
- create normative requirements;
- extend accepted normative semantics;
- convert implementation preference into normative enforcement;
- infer normative authority from historical behavior; or
- claim semantic certainty where mechanical evaluation cannot decide the matter.
Mechanical enforcement of accepted normative authority shall occur only through Conformance.

**DP010-DETAIL-037**
Detailed validation hierarchy, packages, primitives, tests, fixtures, runners, evidence, correspondence, and enforcement-provenance mechanics belong in the Conformance Architecture Proposal.

### Assurance

**DP010-DETAIL-038**
Assurance is the framework mechanism responsible for governed semantic review and case-specific semantic judgment.

**DP010-DETAIL-039**
Assurance answers:

**DP010-DETAIL-040**
**Is the authority, realization, evidence, or application under review semantically adequate and sufficiently justified?**
Assurance may:

**DP010-DETAIL-041**
- evaluate semantic properties that Conformance cannot decide;
- evaluate the sufficiency of evidence;
- identify ambiguity, contradiction, omission, or inappropriate interpretation; and
- issue case-specific semantic findings.
Assurance shall not:

**DP010-DETAIL-042**
- create persistent normative authority;
- amend accepted normative authority;
- extend accepted normative semantics through review;
- replace Governance as the mechanism for persistent normative change; or
- replace Conformance for mechanically decidable enforcement.
Governed semantic review and case-specific semantic judgment shall occur only through Assurance.

**DP010-DETAIL-043**
An Assurance finding may affect disposition of the specific case under review where authorized by accepted framework authority.

**DP010-DETAIL-044**
An Assurance finding shall not independently create or amend persistent normative authority.

**DP010-DETAIL-045**
A finding that shows intended Design meaning must change shall route to Design; a finding that shows accepted normative distillation is defective while Design meaning remains sound shall route to Planning through Governance.

**DP010-DETAIL-046**
Detailed Assurance artifacts, reviewer roles, finding taxonomy, interpretation rules, review lifecycle, evidence requirements, and adjudication mechanics belong in the Assurance Architecture Proposal.

### Keystone Separation

**DP010-DETAIL-047**
Each keystone has one primary authority domain.

**DP010-DETAIL-048**
| Keystone | Authority Domain |
| --- | --- |
| Governance | persistent normative change |
| Conformance | mechanical normative enforcement |
| Assurance | governed semantic review and case-specific judgment |
A keystone shall exercise only authority delegated by accepted repository-framework authority.

**DP010-DETAIL-049**
A keystone shall not independently exercise authority reserved to another keystone.

**DP010-DETAIL-050**
A supporting mechanism shall not bypass keystone separation by exercising equivalent authority under another name.

### Authority Flow

**DP010-DETAIL-051**
Normative authority flows through the framework as follows:

**DP010-DETAIL-052**
**Framework Contract**
→ delegates authority to Governance, Conformance, and Assurance
**Governance**
→ creates or changes accepted normative authority
**Accepted normative authority**
→ governs realization
→ authorizes mechanical Conformance
→ provides the semantic basis for Assurance
**Conformance**
→ produces mechanical findings and evidence
**Assurance**
→ produces semantic findings
**Persistent normative change**
→ returns through Governance
Authority flow and implementation dependency flow are distinct.

**DP010-DETAIL-053**
Implementation structure shall not obscure, replace, or invert normative authority.

### Authority Inversion

**DP010-DETAIL-054**
Authority inversion occurs when a subordinate or derived artifact or mechanism is treated as normative authority without Governance having established that authority.

**DP010-DETAIL-055**
The framework shall prohibit the following authority inversions:

**DP010-DETAIL-056**
**implementation behavior → normative authority**
**validation behavior → normative authority**
**review finding → persistent normative authority**
**generated artifact → normative authority**
**workflow convention → normative authority**
**historical repository state → normative authority**
**product behavior → framework authority**
Existing behavior may be incorporated into normative authority only through Governance.

**DP010-DETAIL-057**
Historical or bootstrap behavior shall not become normative solely because preserving it is convenient.

### Framework Authority and Product Authority

**DP010-DETAIL-058**
Framework authority and product authority are distinct.

**DP010-DETAIL-059**
Framework authority defines how the repository framework operates.

**DP010-DETAIL-060**
Product authority defines accepted normative semantics for the maintained product.

**DP010-DETAIL-061**
Framework authority defines how product authority is:

**DP010-DETAIL-062**
- created or changed;
- mechanically enforced;
- semantically reviewed; and
- related to product realization.
Neither product authority nor product implementation shall independently define or amend repository-framework authority.

**DP010-DETAIL-063**
Product implementation remains subordinate to applicable framework authority and product authority.

### Provenance

**DP010-DETAIL-064**
Every maintained derived framework primitive shall resolve to accepted normative authority that authorizes its existence or use.

**DP010-DETAIL-065**
For a derived framework primitive, it shall be possible to determine:

**DP010-DETAIL-066**
- that the primitive is derived rather than normative;
- which accepted normative authority authorizes it; and
- which keystone responsibility it serves.
The absence of resolvable provenance shall be treated as a framework defect.

**DP010-DETAIL-067**
Missing provenance shall not permit authority to be inferred from implementation, convention, or historical behavior.

**DP010-DETAIL-068**
Detailed primitive identity, provenance representation, and correspondence mechanics belong in subordinate framework specifications.

### Explicit Authority Representation

**DP010-DETAIL-069**
Accepted repository-framework authority shall have stable machine-resolvable identities.

**DP010-DETAIL-070**
Delegated authority relationships shall be resolvable without inference from non-authoritative repository state.

**DP010-DETAIL-071**
A human or automated consumer shall not be required to infer authority from:

**DP010-DETAIL-072**
- implementation behavior;
- file proximity;
- historical convention;
- generated output;
- reviewer preference; or
- other non-authoritative context.
Automated tooling and AI agents are subject to the same authority boundaries as human contributors.

**DP010-DETAIL-073**
The ability to inspect or modify repository state does not grant additional authority.

### Framework Contract and Keystone Specifications

**DP010-DETAIL-074**
The Framework Contract defines:

**DP010-DETAIL-075**
- framework authority;
- keystone delegation;
- authority boundaries;
- authority flow;
- provenance obligations;
- framework/product authority separation; and
- explicit authority representation.
The Governance Architecture Proposal shall define how persistent normative change operates.

**DP010-DETAIL-076**
The Conformance Architecture Proposal shall define how mechanical normative enforcement operates.

**DP010-DETAIL-077**
The Assurance Architecture Proposal shall define how governed semantic review operates.

**DP010-DETAIL-078**
A subordinate framework specification shall not redefine or exceed authority delegated by the Framework Contract.

**DP010-DETAIL-079**
Maintained governed framework state shall require accepted authorization or an explicitly governed extension point.

**DP010-DETAIL-080**
Each independently governed framework semantic invariant shall have one controlling normative owner.

**DP010-DETAIL-081**
Normative authority shall not depend for its authority on a cycle of normative dependencies.

### Candidate Foundational Requirements

**DP010-DETAIL-082**
The following proposal-local statements are Design input. Their labels are non-normative; Planning may distill repository normative requirements from any combination of selected Design statements.

### Framework Authority Location

**DP010-DETAIL-083**
**Accepted repository-framework normative authority SHALL reside within `repo/`.**

### Framework Contract Role

**DP010-DETAIL-084**
**The Framework Contract SHALL define the foundational authority topology of the repository framework.**

### Keystone Set

**DP010-DETAIL-085**
**The repository framework SHALL define Governance, Conformance, and Assurance as its three authority-bearing keystones.**

### Delegated Authority

**DP010-DETAIL-086**
**A keystone SHALL exercise only authority delegated by accepted repository-framework authority.**

### Governance Exclusivity

**DP010-DETAIL-087**
**Persistent changes to accepted normative authority SHALL occur only through Governance.**

### Conformance Exclusivity

**DP010-DETAIL-088**
**Mechanical enforcement of accepted normative authority SHALL occur only through Conformance.**

### Assurance Exclusivity

**DP010-DETAIL-089**
**Governed semantic review and case-specific semantic judgment SHALL occur only through Assurance.**

### Assurance Persistence Boundary

**DP010-DETAIL-090**
**An Assurance finding SHALL NOT independently create or amend persistent normative authority.**

### Keystone Separation

**DP010-DETAIL-091**
**A keystone SHALL NOT independently exercise authority reserved to another keystone.**

### Derived Provenance

**DP010-DETAIL-092**
**Every maintained derived framework primitive SHALL resolve to accepted normative authority that authorizes its existence or use.**

### No Implicit Authority

**DP010-DETAIL-093**
**Normative authority SHALL NOT arise solely from the existence or behavior of a non-normative repository artifact or mechanism.**

### Product Subordination

**DP010-DETAIL-094**
**Neither product authority nor product implementation SHALL independently define or amend repository-framework authority.**

### Authority Identity

**DP010-DETAIL-095**
**Accepted repository-framework authority SHALL have stable machine-resolvable identities.**

### Delegation Resolution

**DP010-DETAIL-096**
**Delegated authority relationships SHALL be resolvable without inference from non-authoritative repository state.**

### Default-Deny Maintained State

**DP010-DETAIL-097**
**Maintained governed framework state SHALL require accepted authorization or an explicitly governed extension point.**

### Single Semantic Owner

**DP010-DETAIL-098**
**Each independently governed framework semantic invariant SHALL have one controlling normative owner.**

### Acyclic Normative Dependency

**DP010-DETAIL-099**
**Normative authority SHALL NOT depend for its authority on a cycle of normative dependencies.**

### Primary Design Invariant

**DP010-DETAIL-100**
**The authoritative `repo/` framework SHALL define and bound Governance, Conformance, and Assurance such that persistent normative authority changes only through Governance, mechanical normative enforcement occurs only through Conformance, governed semantic review occurs only through Assurance, maintained governed state is positively authorized, each independently governed semantic invariant has one controlling normative owner, normative authority does not depend on circular normative dependencies, and derived framework behavior remains subordinate and traceable to accepted normative authority.**
All subordinate framework design shall preserve this invariant.

### Audit Questions

**DP010-DETAIL-101**
The current repository should be audited against this proposal by determining:

**DP010-DETAIL-102**
1. Which current `repo/` specifications already express candidate Framework Contract authority.
2. Which framework semantics exist only in implementation, validation, workflow automation, review behavior, generated artifacts, or historical convention.
3. Which existing normative requirements combine Framework Contract concerns with Governance, Conformance, Assurance, or product-specific mechanics.
4. Which current authority relationships permit authority inversion.
5. Which current mechanisms exercise authority reserved to another keystone.
6. Which artifacts or behaviors function as de facto normative authority without an accepted normative owner.
7. Which derived framework primitives lack resolvable provenance to accepted normative authority.
8. Which product authority or implementation improperly defines framework authority.
9. Which current normative requirements are too compound, ambiguous, or implementation-specific to serve as clean authority anchors.
10. Which current framework behaviors represent intended target semantics and which represent bootstrap or historical behavior.
11. Whether each candidate foundational requirement represents one independently identifiable obligation.
12. Whether any candidate foundational requirement duplicates or logically subsumes another.
13. Which candidate foundational requirements are mechanically enforceable through Conformance.
14. Which candidate foundational requirements require Assurance.
15. What minimum Framework Contract authority must be accepted before Governance, Conformance, and Assurance can be normalized without circular authority.

### Explicitly Deferred Concerns

**DP010-DETAIL-103**
The following concerns are intentionally outside the Framework Contract:

**DP010-DETAIL-104**
- detailed normative-requirement quality rules;
- Governance lifecycle details;
- Design, Plan, and Build stage mechanics;
- governed-work issue structure;
- Conformance hierarchy details;
- validation package design;
- validation primitive taxonomy;
- test and fixture architecture;
- Assurance review mechanics;
- reviewer assignment;
- finding taxonomy;
- migration mechanics;
- bootstrap accommodations; and
- successor-generation construction mechanics.
These concerns may be governed by subordinate framework authority but shall remain consistent with the Framework Contract.

### Follow-On Design Proposals

**DP010-DETAIL-105**
This proposal establishes the authority boundaries for three follow-on proposals:

**DP010-DETAIL-106**
1. Governance Architecture Proposal
2. Conformance Architecture Proposal
3. Assurance Architecture Proposal
Those proposals shall not assume authority that the Framework Contract does not delegate.

**DP010-DETAIL-107**
The Framework Contract should therefore be normalized before the keystone architectures are accepted.

## Alternatives Considered

**Section ID:** `ALTERNATIVES`

**DP010-ALTERNATIVES-001**
Domain-specific alternatives remain in the detailed Design. The revised workflow rejects collapsing Design, Planning, and Build into one artifact or stage.

## Risks and Tradeoffs

**Section ID:** `RISKS`

**DP010-RISKS-001**
Incremental realization may expose missing or ambiguous Design later; those defects must route to Design rather than being silently invented during Planning or Build.

## Open Questions

**Section ID:** `OPEN-QUESTIONS`

**DP010-OPEN-QUESTIONS-001**
No blocking workflow-format questions remain. Domain-specific open questions are retained in the detailed Design.

## Acceptance Criteria

**Section ID:** `ACCEPTANCE`

**DP010-ACCEPTANCE-001**
This proposal is planning-ready when its required sections are complete, its detailed semantics remain coherent with declared dependencies, and its Design statements are addressable.
