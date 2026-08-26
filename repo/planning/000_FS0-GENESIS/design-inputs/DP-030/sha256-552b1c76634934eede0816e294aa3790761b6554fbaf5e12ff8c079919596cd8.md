---
doc_id: DP-030
title: Conformance Architecture Proposal
status: planning-ready
depends_on:
  - DP-010
  - DP-020
artifact_type: design-proposal
canonical_format: markdown
---

# Conformance Architecture Proposal

## Status

**Section ID:** `STATUS`

**DP030-STATUS-001**
Planning-ready Design Proposal.

## Purpose

**Section ID:** `PURPOSE`

**DP030-PURPOSE-001**
Define mechanical enforcement for accepted authority and for objective Design, Plan, and Build checks.

## Context

**Section ID:** `CONTEXT`

**DP030-CONTEXT-001**
Conformance must mechanically validate not only accepted normative authority but also the structural and executable contracts needed by the revised workflow.

## Goals

**Section ID:** `GOALS`

**DP030-GOALS-001**
- Preserve the domain architecture and authority boundaries defined by this proposal.
- Make the proposal consumable by incremental functional-set Planning.
- Keep Design statement identity distinct from repository normative identity.

## Non-Goals

**Section ID:** `NON-GOALS`

**DP030-NON-GOALS-001**
- Define one complete implementation plan for the entire proposal.
- Assign repository normative IDs during Design.
- Define file-level pseudo-code in Design unless it is itself a semantic constraint.

## Requirements

**Section ID:** `REQUIREMENTS`

**DP030-REQUIREMENTS-001**
The detailed Design below contains addressable Design statements. Statement IDs are non-normative proposal references. `functional-set.json` selects them; `plan.json` owns decomposition and normative distillation.

## Constraints

**Section ID:** `CONSTRAINTS`

**DP030-CONSTRAINTS-001**
This proposal remains subordinate to its declared Design dependencies and shall not silently assume authority outside them.

## Architecture

**Section ID:** `ARCHITECTURE`

**DP030-ARCHITECTURE-001**
The detailed Design below is semantic input to Planning and may be realized over multiple functional sets.

## Behavior

**Section ID:** `BEHAVIOR`

**DP030-BEHAVIOR-001**
Planning may consume a bounded subset of this proposal in one functional set; implementation of the entire proposal in one pass is not required.

## Interfaces and Boundaries

**Section ID:** `INTERFACES`

**DP030-INTERFACES-001**
Design defines meaning. `functional-set.json` defines selected Design scope. `plan.json` defines normative decomposition and exact implementation intent. Build produces syntactically correct, validated, operational code.

## Invariants

**Section ID:** `INVARIANTS`

**DP030-INVARIANTS-001**
- Design statement IDs remain non-normative.
- Planning owns normative distillation and implementation intent.
- Build shall not invent missing Design semantics or missing Plan intent.

## Detailed Design

**Section ID:** `DETAIL`

### Framework Contract Basis

**DP030-DETAIL-001**
This proposal assumes the Framework Contract Design statements:

**DP030-DETAIL-002**
- Framework Authority Location
- Framework Contract Role
- Keystone Set
- Delegated Authority
- Governance Exclusivity
- Conformance Exclusivity
- Assurance Exclusivity
- Assurance Persistence Boundary
- Keystone Separation
- Derived Provenance
- No Implicit Authority
- Product Subordination
- Authority Identity
- Delegation Resolution
Conformance shall not assume authority beyond that delegated by the Framework Contract.

### Governance Basis

**DP030-DETAIL-003**
This proposal assumes the candidate Governance lifecycle:

**DP030-DETAIL-004**
**Design**
→ **Design Proposal**
→ **Planning**
→ **Plan**
→ **Build**
Design produces planning-ready Markdown Design Proposals.

**DP030-DETAIL-005**
Planning selects one bounded functional set and produces a durable Plan containing normative distillation and exact implementation intent.

**DP030-DETAIL-006**
Build produces syntactically correct, validated, operational source from the accepted Plan.

**DP030-DETAIL-007**
Conformance may provide mechanical findings and evidence to Governance.

**DP030-DETAIL-008**
Conformance shall not create Governance authority or constitute Governance acceptance.

### Objective

**DP030-DETAIL-009**
Conformance shall provide one closed mechanical-enforcement architecture in which:

**DP030-DETAIL-010**
- every maintained Conformance primitive derives from accepted normative authority;
- every mechanically applicable accepted requirement resolves to executable enforcement;
- every executable assertion has required evidence;
- every gating assertion participates in authorized canonical execution; and
- no Conformance primitive or finding independently creates normative semantics.
The primary relationship is:

**DP030-DETAIL-011**
**accepted normative requirement**
↔ **canonical Conformance correspondence**
↔ **Conformance primitive graph**
↔ **mechanical findings and evidence**
The architecture shall establish four closure properties:

**DP030-DETAIL-012**
1. authority closure;
2. coverage closure;
3. evidence closure; and
4. execution closure.

### Conformance Boundary

**DP030-DETAIL-013**
Conformance owns mechanical evaluation of objectively decidable obligations derived from accepted normative authority.

**DP030-DETAIL-014**
Conformance may:

**DP030-DETAIL-015**
- inspect observable state;
- evaluate mechanical predicates;
- reject mechanically nonconforming state;
- produce mechanical findings;
- produce deterministic evidence;
- maintain canonical Conformance correspondence;
- maintain Conformance primitives;
- maintain canonical execution surfaces;
- mechanically verify its own closure properties; and
- expose subordinate generated views.
Conformance shall not:

**DP030-DETAIL-016**
- create normative requirements;
- amend normative requirements;
- extend accepted normative semantics;
- choose among materially ambiguous interpretations;
- convert implementation preference into normative enforcement;
- infer normative authority from historical behavior;
- treat implementation as normative authority;
- perform semantic adjudication reserved to Assurance; or
- establish Governance acceptance.

### Conformance Terminology

### Normative Requirement

**DP030-DETAIL-017**
An identified accepted normative obligation.

**DP030-DETAIL-018**
The normative requirement is the semantic authority.

**DP030-DETAIL-019**
Conformance references the requirement but shall not independently restate, replace, or extend its semantics.

### Conformance Correspondence

**DP030-DETAIL-020**
The governed relationship between one accepted normative requirement and the Conformance responsibility derived from that requirement.

**DP030-DETAIL-021**
Correspondence records:

**DP030-DETAIL-022**
- requirement identity;
- Conformance applicability; and
- direct assertion relationships where applicable.
Correspondence does not independently own normative semantics.

### Conformance Primitive

**DP030-DETAIL-023**
A maintained executable, declarative, evidentiary, supporting, or orchestration element whose purpose participates in normative mechanical enforcement.

### Assertion

**DP030-DETAIL-024**
A Conformance primitive representing one independently identifiable mechanically decidable predicate derived from accepted normative authority.

**DP030-DETAIL-025**
An assertion is the primary executable unit of mechanical enforcement correspondence.

### Evidence Primitive

**DP030-DETAIL-026**
A Conformance primitive whose purpose is to demonstrate the behavior of an assertion or enforcement path.

### Supporting Primitive

**DP030-DETAIL-027**
A Conformance primitive that supports enforcement without itself representing a complete normative predicate.

### Orchestration Primitive

**DP030-DETAIL-028**
A Conformance primitive responsible for composing, discovering, dispatching, loading, or executing other Conformance primitives.

### Closed Conformance Hierarchy

**DP030-DETAIL-029**
Normative mechanical enforcement shall occur only through the governed Conformance hierarchy.

**DP030-DETAIL-030**
A maintained artifact whose purpose is normative mechanical enforcement shall participate in that hierarchy.

**DP030-DETAIL-031**
Applicable artifacts include:

**DP030-DETAIL-032**
- assertions;
- schemas;
- helpers;
- adapters;
- fixtures;
- tests;
- runners;
- dispatchers;
- loaders;
- registries;
- generators; and
- other enforcement-supporting artifacts.
An artifact outside the governed Conformance hierarchy shall not independently impose normative mechanical enforcement.

**DP030-DETAIL-033**
Conformance may consume general implementation outside the hierarchy.

**DP030-DETAIL-034**
Such implementation does not become normative authority merely because Conformance depends on it.

### Purpose of the Closed Hierarchy

**DP030-DETAIL-035**
The closed hierarchy is an authority-control mechanism rather than merely a directory convention.

**DP030-DETAIL-036**
It prevents:

**DP030-DETAIL-037**
- ad hoc validation;
- hidden enforcement in unrelated implementation;
- ungoverned AI-generated validators;
- orphan tests;
- orphan fixtures;
- helpers that silently introduce constraints;
- schemas that become de facto semantic authorities;
- duplicate requirement-to-validator registries; and
- enforcement derived from historical implementation rather than accepted authority.
When mechanical enforcement is required, the governed relationship is:

**DP030-DETAIL-038**
**accepted normative requirement**
→ **canonical Conformance correspondence**
→ **assertion**
→ **supporting and evidence primitives**
→ **canonical execution**
If no accepted normative requirement authorizes an enforcement behavior, Conformance shall not invent that behavior.

### Primitive Classes

**DP030-DETAIL-039**
Conformance shall distinguish at least four functional primitive classes:

**DP030-DETAIL-040**
1. assertions;
2. supporting primitives;
3. evidence primitives; and
4. orchestration primitives.
A subordinate controlled taxonomy may further distinguish:

**DP030-DETAIL-041**
- helper;
- adapter;
- schema;
- fixture;
- positive case;
- rejection case;
- boundary case;
- regression case;
- mutation case;
- unit test;
- integration test;
- self-test;
- runner;
- dispatcher;
- loader;
- registry; and
- generator.
Primitive class identifies Conformance role.

**DP030-DETAIL-042**
Primitive class does not grant normative authority.

### Assertion Model

**DP030-DETAIL-043**
An assertion represents one independently identifiable mechanically decidable predicate.

**DP030-DETAIL-044**
Assertion identity shall be distinct from implementation-callable identity.

**DP030-DETAIL-045**
One normative requirement may derive multiple assertions.

**DP030-DETAIL-046**
Multiple assertions may share one callable where their identities and provenance remain distinguishable.

**DP030-DETAIL-047**
For example:

**DP030-DETAIL-048**
**Requirement R**
→ **Assertion A1**
→ callable X
**Requirement R**
→ **Assertion A2**
→ callable X
The callable is implementation.

**DP030-DETAIL-049**
A1 and A2 are independently identifiable enforcement predicates.

**DP030-DETAIL-050**
This permits precise correspondence without requiring one trivial implementation function per assertion.

### Assertion Ownership

**DP030-DETAIL-051**
Each assertion shall directly resolve to exactly one accepted normative requirement.

**DP030-DETAIL-052**
If one implementation callable checks predicates derived from multiple requirements, separate assertion identities shall represent those predicates.

**DP030-DETAIL-053**
This preserves deterministic semantic ownership while permitting shared implementation.

### Supporting Primitive Sharing

**DP030-DETAIL-054**
Supporting primitives may serve multiple assertions.

**DP030-DETAIL-055**
A shared primitive does not require one direct normative owner when its transitive provenance remains resolvable.

**DP030-DETAIL-056**
Examples include:

**DP030-DETAIL-057**
- helper libraries;
- parsers;
- adapters;
- shared fixtures;
- common runners; and
- common infrastructure.
Shared support shall not be duplicated merely to create artificial one-requirement-per-function correspondence.

### Direct and Transitive Provenance

**DP030-DETAIL-058**
Conformance shall distinguish direct provenance from transitive provenance.

### Direct Provenance

**DP030-DETAIL-059**
A primitive directly corresponds to a requirement-derived enforcement or evidence obligation.

**DP030-DETAIL-060**
Typical examples include:

**DP030-DETAIL-061**
- assertion;
- requirement-specific rejection case;
- requirement-specific boundary case; and
- requirement-specific fixture.

### Transitive Provenance

**DP030-DETAIL-062**
A primitive supports another Conformance primitive that ultimately resolves to accepted normative authority.

**DP030-DETAIL-063**
Typical examples include:

**DP030-DETAIL-064**
- shared helper;
- parser;
- adapter;
- runner;
- loader; and
- common fixture.
Both relationships shall be mechanically resolvable.

### Authority Closure

**DP030-DETAIL-065**
Every maintained Conformance primitive shall resolve through governed provenance to at least one accepted normative requirement.

**DP030-DETAIL-066**
Conceptually:

**DP030-DETAIL-067**
**∀ maintained primitive P: ∃ accepted requirement R such that R →* P**
No orphan Conformance primitive is permitted.

**DP030-DETAIL-068**
An orphan primitive is a Conformance defect.

**DP030-DETAIL-069**
Normative provenance shall not be inferred solely from:

**DP030-DETAIL-070**
- file location;
- naming;
- nearby tests;
- implementation behavior;
- historical use; or
- apparent usefulness.

### Canonical Correspondence

**DP030-DETAIL-071**
Each active normative requirement shall have exactly one canonical Conformance correspondence record.

**DP030-DETAIL-072**
The correspondence record shall identify:

**DP030-DETAIL-073**
- the normative requirement;
- its canonical Conformance applicability; and
- its direct assertion relationships where applicable.
If Conformance applicability is `none`, the correspondence shall identify the governed rationale for that determination.

**DP030-DETAIL-074**
Correspondence shall not duplicate normative requirement text as independent semantic authority.

### Conformance Applicability

**DP030-DETAIL-075**
Each active normative requirement shall have exactly one canonical Conformance applicability determination.

**DP030-DETAIL-076**
The candidate vocabulary is:

### `mechanical`

**DP030-DETAIL-077**
The requirement has mechanically enforceable responsibility within Conformance scope.

**DP030-DETAIL-078**
A mechanically applicable requirement shall resolve to executable assertion coverage.

### `none`

**DP030-DETAIL-079**
The requirement has no meaningful mechanical enforcement responsibility within Conformance scope.

**DP030-DETAIL-080**
A governed rationale is required.

**DP030-DETAIL-081**
Conformance applicability describes only Conformance responsibility.

**DP030-DETAIL-082**
It shall not encode Assurance responsibility.

**DP030-DETAIL-083**
Terms such as:

**DP030-DETAIL-084**
- `partial`; and
- `semantic-review`
shall therefore not be primary Conformance dispositions.

**DP030-DETAIL-085**
A requirement may independently have:

**DP030-DETAIL-086**
- mechanical Conformance responsibility; and
- Assurance responsibility.
Cross-keystone conditions should be derived from those separate relationships.

### Requirement Quality and Mechanical Decomposition

**DP030-DETAIL-087**
Conformance shall not silently decompose ambiguous normative authority into invented normative predicates.

**DP030-DETAIL-088**
If selected Design contains multiple independently governed obligations, Planning should distill those obligations into appropriate repository normative requirements.

**DP030-DETAIL-089**
If an assertion requires choosing among materially different semantic interpretations, Conformance shall not make that choice independently.

**DP030-DETAIL-090**
The issue shall route through Governance and, where semantic judgment is required, Assurance.

**DP030-DETAIL-091**
Conformance shall not alter normative meaning merely to make enforcement easier to implement.

### Coverage Closure

**DP030-DETAIL-092**
Each accepted normative requirement with mechanical Conformance applicability shall resolve to at least one executable assertion.

**DP030-DETAIL-093**
Conceptually:

**DP030-DETAIL-094**
**∀ mechanical requirement R: ∃ executable assertion A such that R → A**
A mechanical applicability determination with zero executable assertions is incomplete Conformance.

**DP030-DETAIL-095**
Correspondence metadata alone does not satisfy coverage closure.

### Evidence Model

**DP030-DETAIL-096**
Executable enforcement requires governed evidence demonstrating that enforcement behaves correctly.

**DP030-DETAIL-097**
Evidence classes may include:

**DP030-DETAIL-098**
- rejection evidence;
- positive evidence;
- boundary evidence;
- regression evidence;
- mutation evidence;
- unit evidence;
- integration evidence; and
- self-test evidence.
The exact evidence obligations applicable to an assertion belong in subordinate Conformance authority.

### Evidence Closure

**DP030-DETAIL-099**
Each executable assertion shall satisfy the governed evidence obligations applicable to that assertion.

**DP030-DETAIL-100**
Conceptually:

**DP030-DETAIL-101**
**∀ executable assertion A: required evidence obligations(A) are satisfied**
Evidence should be sufficient to demonstrate that the assertion behaves as intended as mechanical enforcement.

**DP030-DETAIL-102**
An assertion shall not be considered adequately evidenced merely because its implementation executes successfully.

### Rejection Evidence

**DP030-DETAIL-103**
Rejection evidence demonstrates that representative violating state is rejected.

**DP030-DETAIL-104**
Rejection evidence is the expected baseline for most enforcement assertions because it demonstrates that the targeted violation changes the Conformance result.

**DP030-DETAIL-105**
The exact exceptions and required rejection-evidence rules belong in subordinate Conformance authority.

### Positive Evidence

**DP030-DETAIL-106**
Positive evidence demonstrates that representative conforming state is accepted.

**DP030-DETAIL-107**
It primarily protects against over-enforcement.

**DP030-DETAIL-108**
Positive evidence is especially useful for:

**DP030-DETAIL-109**
- permitted alternatives;
- optional structures;
- extension points;
- valid namespace locations; and
- permitted lifecycle transitions.

### Boundary Evidence

**DP030-DETAIL-110**
Boundary evidence demonstrates behavior at transitions between permitted and prohibited state.

**DP030-DETAIL-111**
It is especially useful for:

**DP030-DETAIL-112**
- cardinality;
- path roots;
- namespaces;
- lifecycle transitions;
- exact sets;
- optional versus required structures; and
- minimum or maximum values.

### Regression Evidence

**DP030-DETAIL-113**
Regression evidence demonstrates continued protection against a previously observed defect.

**DP030-DETAIL-114**
Historical issue, defect, or revision references may accompany regression evidence.

**DP030-DETAIL-115**
Historical provenance remains evidence only.

**DP030-DETAIL-116**
It does not become normative authority.

### Mutation Evidence

**DP030-DETAIL-117**
Mutation evidence intentionally alters otherwise conforming state to create a targeted violation.

**DP030-DETAIL-118**
Mutation evidence may demonstrate that:

**DP030-DETAIL-119**
- an assertion is actually executed;
- a targeted violation changes the result;
- canonical execution does not silently skip enforcement; and
- an evidence fixture meaningfully exercises the intended predicate.
Detailed mutation policy belongs in subordinate Conformance authority.

### Schemas

**DP030-DETAIL-120**
A schema used for normative mechanical enforcement is a Conformance primitive.

**DP030-DETAIL-121**
Its normative provenance follows the same rule as every other Conformance primitive.

**DP030-DETAIL-122**
A schema does not become normative authority merely because validators consume it.

**DP030-DETAIL-123**
Schema behavior imposing constraints absent from accepted normative authority is over-enforcement.

**DP030-DETAIL-124**
Schema behavior omitting mechanically required constraints is under-enforcement.

### Fixtures

**DP030-DETAIL-125**
A maintained fixture used by Conformance is a Conformance primitive.

**DP030-DETAIL-126**
Its provenance shall resolve directly or transitively to the enforcement or evidence responsibility it serves.

**DP030-DETAIL-127**
Fixture meaning shall not depend solely on file naming or directory placement.

**DP030-DETAIL-128**
Where fixture role affects Conformance behavior, that role should be mechanically resolvable.

### Unit Tests

**DP030-DETAIL-129**
A maintained unit test of Conformance implementation is a Conformance primitive.

**DP030-DETAIL-130**
It shall resolve to the primitive or responsibility whose behavior it verifies.

**DP030-DETAIL-131**
Through that relationship it shall resolve to accepted normative authority.

**DP030-DETAIL-132**
Unit tests demonstrate implementation behavior.

**DP030-DETAIL-133**
They do not by themselves satisfy coverage closure unless they also represent identified executable assertions.

### Integration Tests

**DP030-DETAIL-134**
An integration test is a Conformance evidence primitive that verifies behavior through maintained execution boundaries.

**DP030-DETAIL-135**
It may verify:

**DP030-DETAIL-136**
- runner composition;
- dispatch;
- public validation surfaces;
- failure propagation; and
- repository-wide execution.
Integration evidence remains subordinate to accepted normative authority.

### Self-Tests

**DP030-DETAIL-137**
Conformance self-tests verify the Conformance architecture and implementation itself.

**DP030-DETAIL-138**
Self-tests may verify:

**DP030-DETAIL-139**
- provenance closure;
- correspondence integrity;
- assertion execution;
- evidence relationships;
- canonical execution;
- schema behavior;
- runner behavior;
- generated projections; and
- failure propagation.
Self-tests are themselves Conformance primitives.

**DP030-DETAIL-140**
They shall satisfy the same provenance obligations as other maintained Conformance primitives.

**DP030-DETAIL-141**
Conformance shall not exempt its own infrastructure from its authority model.

### Orchestration Primitives

**DP030-DETAIL-142**
Runners, dispatchers, loaders, registries, and similar orchestration mechanisms are Conformance primitives.

**DP030-DETAIL-143**
Their provenance may be transitive through the assertions and Conformance responsibilities they serve.

**DP030-DETAIL-144**
They do not need to claim direct ownership of every normative requirement whose enforcement they orchestrate.

### Canonical Execution

**DP030-DETAIL-145**
Conformance shall define authorized canonical execution surfaces.

**DP030-DETAIL-146**
Each gating assertion shall be reachable from an authorized canonical Conformance execution surface.

**DP030-DETAIL-147**
Canonical execution may be hierarchical.

**DP030-DETAIL-148**
For example:

**DP030-DETAIL-149**
**repository Conformance runner**
→ **framework Conformance runner**
→ **product Conformance runner**
The exact orchestration model belongs in subordinate design.

### Execution Closure

**DP030-DETAIL-150**
Each gating assertion shall participate in authorized canonical execution.

**DP030-DETAIL-151**
Conceptually:

**DP030-DETAIL-152**
**∀ gating assertion A: canonical execution →* A**
An assertion may have correct authority, correspondence, and evidence while still failing to provide actual enforcement if it is not executed through the required gating path.

**DP030-DETAIL-153**
Execution closure prevents that condition.

### The Four Closure Properties

**DP030-DETAIL-154**
The architecture centers on four closure properties.

### Authority Closure

**DP030-DETAIL-155**
**accepted normative authority → every maintained Conformance primitive**
No orphan Conformance behavior.

### Coverage Closure

**DP030-DETAIL-156**
**mechanically applicable requirement → executable assertion**
No mechanically applicable requirement without enforcement.

### Evidence Closure

**DP030-DETAIL-157**
**executable assertion → required evidence**
No unsupported enforcement predicate.

### Execution Closure

**DP030-DETAIL-158**
**authorized canonical execution → every gating assertion**
No required enforcement silently omitted from execution.

**DP030-DETAIL-159**
Together:

**DP030-DETAIL-160**
**Authority explains why enforcement exists.**
**Coverage establishes that required enforcement exists.**
**Evidence demonstrates that enforcement behaves correctly.**
**Execution establishes that required enforcement actually runs.**

### Bidirectional Correspondence

**DP030-DETAIL-161**
Canonical Conformance correspondence and primitive provenance shall support mechanically resolvable forward and reverse navigation.

**DP030-DETAIL-162**
Forward:

**DP030-DETAIL-163**
**normative requirement**
→ **canonical correspondence**
→ **assertion**
→ **evidence/supporting/orchestration primitives**
Reverse:

**DP030-DETAIL-164**
**Conformance primitive**
→ **provenance path**
→ **accepted normative requirement**
Reverse provenance may be:

**DP030-DETAIL-165**
- direct for assertions;
- direct or transitive for evidence;
- transitive for shared infrastructure.

### Primitive Identity

**DP030-DETAIL-166**
Each Conformance primitive requiring independent correspondence shall have an identity appropriate to its governed role.

**DP030-DETAIL-167**
Assertion identities shall be stable and unique.

**DP030-DETAIL-168**
Other primitive identities shall be stable where required by correspondence, provenance, evidence, or historical resolution.

**DP030-DETAIL-169**
Primitive identity should remain distinct from mutable implementation coordinates where practical.

**DP030-DETAIL-170**
A stable primitive identity may survive:

**DP030-DETAIL-171**
- source movement;
- function renaming;
- helper extraction;
- runner reorganization; and
- implementation refactoring
when its governed Conformance role remains unchanged.

**DP030-DETAIL-172**
A Conformance primitive identity shall not be reused for unrelated behavior.

### Single Correspondence Authority

**DP030-DETAIL-173**
Conformance shall define one canonical authority for requirement-to-Conformance correspondence.

**DP030-DETAIL-174**
Independently maintained mappings shall not be allowed to silently diverge.

**DP030-DETAIL-175**
Requirement relationships shall not be separately redefined without verification in:

**DP030-DETAIL-176**
- correspondence records;
- source annotations;
- registries;
- runner lists;
- test manifests;
- schemas;
- generated documentation; or
- dispatch logic.
Where multiple operational representations are required, they shall be:

**DP030-DETAIL-177**
- generated from canonical correspondence; or
- mechanically verified against it.

### Correspondence Package Evolution

**DP030-DETAIL-178**
The current validation-package concept may remain as the canonical requirement-level correspondence container.

**DP030-DETAIL-179**
Its role should change from a flat validation-task registry to an entry point into the Conformance graph.

**DP030-DETAIL-180**
A conceptual package may resemble:

**DP030-DETAIL-181**
{
"normative_requirement_id": "<planning-assigned-normative-requirement-id>",
"conformance_applicability": "mechanical",
"assertions": [
"<assertion-id-a>",
"<assertion-id-b>"
]
}

**DP030-DETAIL-182**
The exact representation remains subject to detailed design.

**DP030-DETAIL-183**
The architectural requirement is one canonical correspondence authority, not one particular file format.

### Correspondence Integrity

**DP030-DETAIL-184**
Canonical Conformance correspondence shall remain mechanically consistent with the maintained primitive graph.

**DP030-DETAIL-185**
Conformance shall detect stale or contradictory relationships such as:

**DP030-DETAIL-186**
- correspondence referencing nonexistent assertions;
- assertions whose direct requirement ownership disagrees with correspondence;
- removed primitives still referenced by canonical correspondence; and
- duplicate operational mappings that diverge from canonical correspondence.

### Findings

**DP030-DETAIL-187**
A Conformance finding is a mechanical result produced through governed Conformance execution.

**DP030-DETAIL-188**
A violation finding shall identify:

**DP030-DETAIL-189**
- the assertion from which it derives; and
- the accepted normative requirement owning that assertion.
A finding should additionally identify:

**DP030-DETAIL-190**
- the observed subject;
- the mechanical outcome; and
- sufficient diagnostic context.
Findings shall be suitable for machine resolution and human remediation.

**DP030-DETAIL-191**
A finding shall not create, amend, or extend normative semantics.

### Finding Classes

**DP030-DETAIL-192**
Conformance may distinguish findings such as:

**DP030-DETAIL-193**
- pass;
- violation;
- Conformance-system defect; and
- mechanically undecidable.
`Mechanically undecidable` means Conformance cannot establish the result mechanically under current authority and implementation.

**DP030-DETAIL-194**
It shall not be used as a substitute for Assurance judgment.

**DP030-DETAIL-195**
If undecidability results from ambiguous authority, the issue routes toward Assurance and Governance.

**DP030-DETAIL-196**
If undecidability results from missing or defective mechanical enforcement, it is a Conformance defect.

### Determinism

**DP030-DETAIL-197**
Equivalent accepted authority and equivalent observable state should produce equivalent Conformance outcomes.

**DP030-DETAIL-198**
Material enforcement outcomes should not depend on incidental nondeterminism such as:

**DP030-DETAIL-199**
- traversal order;
- filesystem order;
- hash ordering;
- locale;
- unstable defaults; or
- irrelevant environment state.
Where external state is normatively relevant, accepted authority shall establish that relevance.

### Generated Views

**DP030-DETAIL-200**
Generated Conformance coverage and correspondence views may be derived from canonical correspondence and primitive provenance.

**DP030-DETAIL-201**
Derived views may include:

**DP030-DETAIL-202**
- requirement identity;
- applicability;
- assertion relationships;
- evidence relationships;
- execution reachability;
- supporting primitives; and
- closure defects.
Generated views remain subordinate derived artifacts.

**DP030-DETAIL-203**
They shall not become competing correspondence or semantic authority.

**DP030-DETAIL-204**
A declaration such as `validated: true` shall not substitute for closure.

### Conformance Self-Validation

**DP030-DETAIL-205**
Conformance shall mechanically verify the integrity of its own governed model.

**DP030-DETAIL-206**
At minimum, Conformance self-validation shall enforce required:

**DP030-DETAIL-207**
- authority closure;
- coverage closure;
- evidence closure; and
- execution closure.
It should additionally verify:

**DP030-DETAIL-208**
- assertion identity integrity;
- primitive identity integrity where applicable;
- correspondence integrity; and
- hierarchy integrity.
Self-validation enforces accepted Conformance authority.

**DP030-DETAIL-209**
It does not independently create that authority.

### Closure Enforcement

**DP030-DETAIL-210**
A governed Conformance state that violates required closure shall be mechanically nonconforming.

**DP030-DETAIL-211**
Examples include:

### Authority Closure Defect

**DP030-DETAIL-212**
A maintained Conformance primitive has no provenance path to accepted normative authority.

### Coverage Closure Defect

**DP030-DETAIL-213**
A mechanically applicable normative requirement has no executable assertion.

### Evidence Closure Defect

**DP030-DETAIL-214**
An executable assertion does not satisfy its governed evidence obligations.

### Execution Closure Defect

**DP030-DETAIL-215**
A gating assertion is unreachable from authorized canonical execution.

**DP030-DETAIL-216**
Conformance shall mechanically reject such states.

### Other Conformance Defects

**DP030-DETAIL-217**
Other defects may include:

**DP030-DETAIL-218**
- assertion with no direct normative owner;
- invalid provenance edge;
- duplicate assertion identity;
- unrelated identity reuse;
- stale canonical correspondence;
- divergent duplicate mapping;
- enforcement outside the governed hierarchy;
- schema behavior imposing unauthorized constraints;
- helper behavior introducing undeclared constraints;
- finding semantics exceeding accepted authority; and
- canonical execution silently skipping required enforcement.
A Conformance defect shall not be repaired by inventing normative authority.

**DP030-DETAIL-219**
If accepted authority is insufficient, the issue shall route through Governance and, where semantic judgment is necessary, Assurance.

### Relationship to Governance

**DP030-DETAIL-220**
Governance creates and changes accepted normative authority.

**DP030-DETAIL-221**
Conformance consumes accepted normative authority.

**DP030-DETAIL-222**
Governance may require Conformance findings or evidence for stage acceptance.

**DP030-DETAIL-223**
Conformance results do not themselves constitute Governance acceptance.

**DP030-DETAIL-224**
When Conformance exposes a defect:

### Normative Semantic Defect

**DP030-DETAIL-225**
Route to Design when intended Design meaning is defective.

### Realization-Intent Defect

**DP030-DETAIL-226**
Route to Planning when Design meaning remains sound but normative distillation or implementation intent is defective.

### Realization Defect

**DP030-DETAIL-227**
Route to Build when Design and Planning intent remain sound but realization is defective.

**DP030-DETAIL-228**
Conformance reports mechanically established facts.

**DP030-DETAIL-229**
Governance determines persistent change and lifecycle disposition.

### Relationship to Assurance

**DP030-DETAIL-230**
Assurance may evaluate:

**DP030-DETAIL-231**
- whether Conformance applicability is semantically justified;
- whether an assertion correctly interprets accepted authority;
- whether mechanical decomposition introduces unintended semantics;
- whether evidence is semantically sufficient where mechanical criteria cannot decide sufficiency;
- whether a requirement is too ambiguous for mechanical enforcement; and
- whether a claimed `none` applicability is semantically justified.
Assurance shall not independently rewrite Conformance semantics into persistent authority.

**DP030-DETAIL-232**
Persistent semantic corrections shall route through Governance.

### Human and Automated Actors

**DP030-DETAIL-233**
Humans, automated tooling, and AI agents may perform Conformance work where authorized.

**DP030-DETAIL-234**
Actor capability does not determine authority.

**DP030-DETAIL-235**
When adding or changing mechanical enforcement, the governed sequence should be:

**DP030-DETAIL-236**
1. identify accepted normative authority;
2. identify canonical Conformance correspondence;
3. establish assertion identity;
4. implement or reuse supporting primitives;
5. provide required evidence;
6. connect gating assertions to canonical execution;
7. preserve primitive provenance; and
8. verify closure.
An automated actor shall not:

**DP030-DETAIL-237**
- add ad hoc enforcement outside the hierarchy;
- infer normative constraints from implementation;
- invent missing requirements;
- create orphan tests or fixtures;
- treat schemas as independent semantic authority;
- claim coverage from correspondence existence alone; or
- bypass canonical execution.

### Conformance Design Statements

**DP030-DETAIL-238**
The following proposal-local statements are Design input. Their labels are non-normative; Planning may distill repository normative requirements from any combination of selected Design statements.

### Closed Conformance Hierarchy

**DP030-DETAIL-239**
**Normative mechanical enforcement SHALL occur only through the governed Conformance hierarchy.**

### Primitive Provenance

**DP030-DETAIL-240**
**Every maintained Conformance primitive SHALL resolve through governed provenance to at least one accepted normative requirement.**

### Canonical Correspondence

**DP030-DETAIL-241**
**Each active normative requirement SHALL have exactly one canonical Conformance correspondence record.**

### Conformance Applicability

**DP030-DETAIL-242**
**Each active normative requirement SHALL have exactly one canonical Conformance applicability determination.**

### Mechanical Coverage

**DP030-DETAIL-243**
**Each normative requirement with mechanical Conformance applicability SHALL resolve to at least one executable assertion.**

### Assertion Identity

**DP030-DETAIL-244**
**Each maintained Conformance assertion SHALL have a stable unique identity.**

### Assertion Ownership

**DP030-DETAIL-245**
**Each maintained Conformance assertion SHALL directly resolve to exactly one accepted normative requirement.**

### Conformance Semantic Boundary

**DP030-DETAIL-246**
**A Conformance primitive or finding SHALL NOT independently create, amend, or extend normative semantics.**

### Non-Mechanical Rationale

**DP030-DETAIL-247**
**A normative requirement with no mechanical Conformance applicability SHALL have a governed rationale for that determination.**

### Evidence Closure

**DP030-DETAIL-248**
**Each executable Conformance assertion SHALL satisfy the governed evidence obligations applicable to that assertion.**

### Execution Closure

**DP030-DETAIL-249**
**Each gating Conformance assertion SHALL be reachable from an authorized canonical Conformance execution surface.**

### Correspondence Integrity

**DP030-DETAIL-250**
**Canonical Conformance correspondence SHALL remain mechanically consistent with the maintained Conformance primitive graph.**

### Single Correspondence Authority

**DP030-DETAIL-251**
**Requirement-to-Conformance correspondence SHALL NOT depend on independently maintained mappings that may silently diverge.**

### Primitive Identity Preservation

**DP030-DETAIL-252**
**A Conformance primitive identity SHALL NOT be reused for unrelated Conformance behavior.**

### Finding Traceability

**DP030-DETAIL-253**
**A Conformance violation finding SHALL identify the assertion and accepted normative requirement from which it derives.**

### Closure Enforcement

**DP030-DETAIL-254**
**Conformance SHALL mechanically reject governed Conformance state that violates required authority, coverage, evidence, or execution closure.**

### Primary Design Invariant

**DP030-DETAIL-255**
**Conformance SHALL mechanically enforce accepted normative authority through a closed and self-validating provenance graph in which every maintained Conformance primitive is authorized by accepted normative requirements, every mechanically applicable requirement resolves to executable assertions, every executable assertion satisfies required evidence obligations, every gating assertion participates in authorized canonical execution, and no Conformance primitive or finding independently creates normative semantics.**
All detailed Conformance design shall preserve this invariant.

### Audit Questions

**DP030-DETAIL-256**
The current repository should be audited against this proposal by determining:

**DP030-DETAIL-257**
1. Which maintained validation artifacts are Conformance primitives.
2. Which current Conformance primitives lack resolvable provenance to accepted normative authority.
3. Which active normative requirements should have `mechanical` applicability.
4. Which active normative requirements should have `none` applicability.
5. Which current `none` or `not-applicable` decisions lack adequate rationale.
6. Which mechanically applicable requirements lack executable assertions.
7. Which current validation functions contain multiple independently identifiable assertions.
8. Which current tagged entry points identify implementation callables rather than independently governed assertions.
9. Which assertions directly map to more than one normative requirement and therefore require decomposition of assertion identity.
10. Which shared helpers, fixtures, schemas, runners, loaders, registries, or generators require transitive provenance.
11. Which unit tests, integration tests, self-tests, and other evidence primitives lack provenance.
12. Which executable assertions fail governed evidence obligations.
13. Which gating assertions are unreachable from canonical execution.
14. Which enforcement behavior exists outside the governed Conformance hierarchy.
15. Which schemas or helpers enforce constraints not clearly authorized by accepted normative authority.
16. Which current validation-package dispositions combine Conformance and Assurance responsibilities.
17. Which `partial` relationships should instead be represented by independent Conformance and Assurance correspondence.
18. Which `semantic-review` relationships belong entirely to Assurance.
19. Which validation task categories should become evidence classes rather than primary correspondence identities.
20. Which existing validator callables should expose multiple assertion identities.
21. Which current mappings are duplicated across packages, source metadata, runners, scripts, registries, or generated artifacts.
22. Which generated artifacts should remain subordinate projections of canonical correspondence.
23. Which current findings fail to identify both assertion and normative requirement identity.
24. Which existing self-tests already verify authority, coverage, evidence, or execution closure.
25. Whether each Planning-distilled normative requirement selected for Conformance represents one independently identifiable obligation.
26. Whether any Planning-distilled normative requirement selected for Conformance duplicates or logically follows from another.
27. Which Planning-distilled normative requirements selected for Conformance also require Assurance for semantic evaluation.
28. What minimum Conformance authority must be accepted before Governance may require closure at Build acceptance.

### Explicitly Deferred Concerns

**DP030-DETAIL-258**
The following concerns are intentionally outside this Conformance proposal:

**DP030-DETAIL-259**
- exact directory layout;
- exact correspondence-package schema;
- exact primitive metadata syntax;
- exact assertion identifier format;
- exact decorator or source-tag syntax;
- exact evidence-policy matrix;
- exact fixture naming convention;
- exact runner implementation;
- exact programming language;
- exact diagnostic serialization;
- exact failure aggregation policy;
- exact generated Markdown format;
- exact mutation-testing framework;
- exact Assurance correspondence model;
- migration sequencing from the current validation architecture; and
- bootstrap accommodations.
These concerns may be defined by later Design or by Planning when they are implementation choices rather than Design semantics.

### Relationship to Assurance

**DP030-DETAIL-260**
The Assurance Architecture Proposal shall define semantic review of:

**DP030-DETAIL-261**
- normative requirement quality;
- ambiguous or incompletely mechanical obligations;
- Conformance applicability decisions;
- assertion interpretation;
- semantic sufficiency of evidence; and
- case-specific semantic conclusions.
Conformance shall establish mechanically decidable facts.

**DP030-DETAIL-262**
Assurance shall evaluate matters requiring semantic judgment.

**DP030-DETAIL-263**
Neither shall independently create persistent normative authority.

**DP030-DETAIL-264**
Persistent semantic change shall return through Governance.

### Workflow Artifact Conformance

**DP030-DETAIL-265**
Conformance mechanically validates the objective contracts required by the Design → Planning → Build workflow.

#### Design Proposal Conformance

**DP030-DETAIL-266**
Design Proposal Conformance verifies mechanically decidable properties of a Design Proposal, including:

**DP030-DETAIL-267**
- parseable metadata;
- a valid `DP-NNN` document identity;
- the canonical top-level header set and order;
- the canonical stable section identities;
- valid and unique Design statement identities;
- resolvable declared proposal dependencies;
- absence of proposed repository normative identities in Design; and
- objective planning-readiness conditions.
Conformance does not decide whether Design semantics are good, complete, or appropriate; those are Assurance questions.

#### Functional-Set Conformance

**DP030-DETAIL-268**
Functional-set Conformance verifies that `functional-set.json`:

**DP030-DETAIL-269**
- identifies exactly one functional set;
- resolves its implementation-order directory identity;
- resolves every Design Proposal and exact revision it declares;
- resolves every selected Design statement ID; and
- contains no selected Design reference outside its declared Design inputs.

#### Plan Conformance

**DP030-DETAIL-270**
Plan Conformance verifies the complete logical Plan document graph rooted at `plan.json`:

**DP030-DETAIL-271**
- has a schema-valid `plan.json` root manifest and schema-valid explicitly referenced Plan subdocuments;
- resolves the functional set it realizes;
- resolves the exact accepted repository predecessor;
- contains valid Planning-assigned normative identities where normative requirements are created;
- identifies every planned create, modify, delete, and regenerate path through authorized file-realization Plan documents;
- contains required pseudo-code or equivalent implementation detail through authorized file-realization Plan documents;
- contains required invariants and validation intent through their authorized Plan document classes;
- contains no missing, duplicate, conflicting, unreachable, unauthorized, or structurally invalid Plan documents or target paths; and
- is mechanically executable against the accepted predecessor and current mutation constraints.
A Plan that is known to require an unauthorized or impossible mutation shall not conform.

#### Build Conformance

**DP030-DETAIL-272**
Build Conformance verifies that:

**DP030-DETAIL-273**
- actual mutated paths are within the accepted Plan;
- generated outputs correspond to declared regeneration consequences;
- syntax, parse, compile, or equivalent language checks pass where applicable;
- Plan-prescribed validation passes;
- canonical repository validation passes; and
- the planned end-to-end operational checks for the functional set pass.
Conformance failure blocks acceptance but does not itself create Design or Planning semantics.

### FS0 Bootstrap Conformance

**DP030-DETAIL-274**
Before the candidate FS0-Core Conformance runtime exists, authorized bootstrap Conformance MAY mechanically evaluate FS0-Core Design, functional-set, and Plan artifacts.

**DP030-DETAIL-275**
Bootstrap Conformance SHALL apply the same objective Design, functional-set, Plan-graph, reference-resolution, mutation-scope, and predecessor-executability contracts that the FS0-Core runtime is required to enforce for later functional sets.

**DP030-DETAIL-276**
Candidate FS0-Core Conformance results SHALL NOT be prerequisites for accepting the Plan that creates the candidate FS0-Core Conformance runtime.

**DP030-DETAIL-277**
After Build, FS0-Core SHALL demonstrate that its maintained Conformance runtime can enforce the required workflow contracts for a subsequent functional set.


## Alternatives Considered

**Section ID:** `ALTERNATIVES`

**DP030-ALTERNATIVES-001**
Domain-specific alternatives remain in the detailed Design. The revised workflow rejects collapsing Design, Planning, and Build into one artifact or stage.

## Risks and Tradeoffs

**Section ID:** `RISKS`

**DP030-RISKS-001**
Incremental realization may expose missing or ambiguous Design later; those defects must route to Design rather than being silently invented during Planning or Build.

## Open Questions

**Section ID:** `OPEN-QUESTIONS`

**DP030-OPEN-QUESTIONS-001**
No blocking workflow-format questions remain. Domain-specific open questions are retained in the detailed Design.

## Acceptance Criteria

**Section ID:** `ACCEPTANCE`

**DP030-ACCEPTANCE-001**
This proposal is planning-ready when its required sections are complete, its detailed semantics remain coherent with declared dependencies, and its Design statements are addressable.
