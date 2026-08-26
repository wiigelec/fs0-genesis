---
doc_id: DP-020
title: Governance Architecture Proposal
status: planning-ready
depends_on:
  - DP-010
artifact_type: design-proposal
canonical_format: markdown
---

# Governance Architecture Proposal

## Status

**Section ID:** `STATUS`

**DP020-STATUS-001**
Planning-ready Design Proposal.

## Purpose

**Section ID:** `PURPOSE`

**DP020-PURPOSE-001**
Define the controlled workflow from iterative Design through Planning and Build to accepted operational repository state.

## Context

**Section ID:** `CONTEXT`

**DP020-CONTEXT-001**
Design produces Markdown proposals; Planning selects one functional set and produces a detailed Plan; Build produces operational code.

## Goals

**Section ID:** `GOALS`

**DP020-GOALS-001**
- Preserve the domain architecture and authority boundaries defined by this proposal.
- Make the proposal consumable by incremental functional-set Planning.
- Keep Design statement identity distinct from repository normative identity.

## Non-Goals

**Section ID:** `NON-GOALS`

**DP020-NON-GOALS-001**
- Define one complete implementation plan for the entire proposal.
- Assign repository normative IDs during Design.
- Define file-level pseudo-code in Design unless it is itself a semantic constraint.

## Requirements

**Section ID:** `REQUIREMENTS`

**DP020-REQUIREMENTS-001**
The detailed Design below contains addressable Design statements. Statement IDs are non-normative proposal references. `functional-set.json` selects them; `plan.json` owns decomposition and normative distillation.

## Constraints

**Section ID:** `CONSTRAINTS`

**DP020-CONSTRAINTS-001**
This proposal remains subordinate to its declared Design dependencies and shall not silently assume authority outside them.

## Architecture

**Section ID:** `ARCHITECTURE`

**DP020-ARCHITECTURE-001**
The detailed Design below is semantic input to Planning and may be realized over multiple functional sets.

## Behavior

**Section ID:** `BEHAVIOR`

**DP020-BEHAVIOR-001**
Planning may consume a bounded subset of this proposal in one functional set; implementation of the entire proposal in one pass is not required.

## Interfaces and Boundaries

**Section ID:** `INTERFACES`

**DP020-INTERFACES-001**
Design defines meaning. `functional-set.json` defines selected Design scope. `plan.json` defines normative decomposition and exact implementation intent. Build produces syntactically correct, validated, operational code.

## Invariants

**Section ID:** `INVARIANTS`

**DP020-INVARIANTS-001**
- Design statement IDs remain non-normative.
- Planning owns normative distillation and implementation intent.
- Build shall not invent missing Design semantics or missing Plan intent.

## Detailed Design

**Section ID:** `DETAIL`

### Governance Artifact Model

**DP020-DETAIL-001**
Governance distinguishes the durable artifacts that move work through the repository framework:

**DP020-DETAIL-002**
- Design Proposal — the maintained Markdown artifact produced by Design;
- Functional Set — the bounded Design scope selected by Planning and recorded in `functional-set.json`;
- Plan — the detailed implementation contract produced by Planning and recorded in `plan.json`;
- Build realization — the repository mutation that implements the accepted Plan; and
- Accepted repository state — the operational state resulting from accepted Build realization.
These artifacts form one resolvable lineage without collapsing their responsibilities.

### Design

**DP020-DETAIL-003**
Design is the iterative user/AI process that develops semantic intent and records it in one or more maintained Markdown Design Proposals.

**DP020-DETAIL-004**
Design owns meaning. It may define requirements, constraints, architecture, behavior, interfaces, invariants, alternatives, risks, and acceptance criteria.

**DP020-DETAIL-005**
Design does not assign repository normative requirement identities, select ordinary implementation file scope, or produce file-by-file implementation pseudo-code unless a concrete implementation detail is itself an intentional semantic constraint.

**DP020-DETAIL-006**
The durable output of Design is the Design Proposal revision itself.

**DP020-DETAIL-007**
A Design Proposal may continue to evolve after an earlier exact revision has been consumed by Planning.

### Design Readiness

**DP020-DETAIL-008**
A Design Proposal becomes planning-ready when its required structure is complete, blocking Design questions are resolved, and semantic review finds its intent sufficiently coherent for Planning.

**DP020-DETAIL-009**
Planning readiness does not make the Design Proposal normative authority and does not imply that the entire product Design is complete.

### Planning

**DP020-DETAIL-010**
Planning consumes exact planning-ready Design Proposal revisions and the exact accepted repository state.

**DP020-DETAIL-011**
Planning owns implementation intent.

**DP020-DETAIL-012**
Each Planning cycle audits available Design against accepted implementation and selects one manageable end-to-end functional set. Planning is not required to decompose the entire Design corpus into a complete future implementation graph.

**DP020-DETAIL-013**
The first functional set is FS0-Core.

**DP020-DETAIL-014**
FS0-Core is the standalone core functional set that implements the minimum complete repository-framework runtime and development workflow on which every later functional set technically depends.

**DP020-DETAIL-015**
Every later functional set extends the accepted Core-based system and is identified by functionality rather than by FS1/FS2-style system generations.

### Functional Set

**DP020-DETAIL-016**
Each functional set has an implementation-ordered plan directory whose name contains a zero-padded order prefix and a functionality identifier, such as `000_FS0-CORE`.

**DP020-DETAIL-017**
Each functional-set directory contains:

**DP020-DETAIL-018**
- `functional-set.json`; and
- `plan.json`.
`functional-set.json` selects Design Proposal statement IDs that bound the Design scope being implemented.

**DP020-DETAIL-019**
Design statement IDs remain non-normative addresses. Selecting a Design statement does not create a one-to-one relationship between that statement and a repository normative requirement.

### Plan

**DP020-DETAIL-020**
The logical Plan document graph rooted at `plan.json` performs the decomposition and distillation of the selected Design scope.

**DP020-DETAIL-021**
Planning may derive zero, one, or multiple repository normative requirements from one selected Design statement and may derive one normative requirement from multiple selected Design statements.

**DP020-DETAIL-022**
Planning assigns repository normative requirement identities as needed for the selected functional set.

**DP020-DETAIL-023**
The logical Plan document graph identifies every file to be created, modified, deleted, or regenerated and provides detailed pseudo-code or equivalent implementation specification for each planned change.

**DP020-DETAIL-024**
The logical Plan document graph defines required invariants, sequencing, validation, generated consequences, and completion conditions.

**DP020-DETAIL-025**
The Plan must be sufficiently detailed and mechanically executable so Build can implement it without inventing new Design semantics, architecture, functional scope, or unplanned mutation paths.

**DP020-DETAIL-026**
If Planning discovers a missing semantic choice, work returns to Design.

### Planning Acceptance

**DP020-DETAIL-027**
Planning acceptance evaluates the functional-set boundary and Plan as one implementation contract.

**DP020-DETAIL-028**
An accepted Plan authorizes Build only for the implementation scope expressed by that Plan.

**DP020-DETAIL-029**
Plan acceptance does not retroactively alter the exact Design Proposal revisions consumed by Planning.

### Build

**DP020-DETAIL-030**
Build consumes one accepted Plan.

**DP020-DETAIL-031**
Build owns implementation correctness.

**DP020-DETAIL-032**
Build shall produce syntactically correct, validated, operational source and generated state that implement the accepted Plan.

**DP020-DETAIL-033**
Build may make language-level and integration decisions needed to correctly realize the Plan, but shall not invent new Design semantics, architectural choices reserved to Design, functional scope, normative intent, or mutation paths outside the Plan.

**DP020-DETAIL-034**
If correct implementation requires a change to Design meaning, work returns to Design.

**DP020-DETAIL-035**
If correct implementation requires a change to functional-set scope, normative distillation, planned files, pseudo-code, invariants, sequencing, or validation intent, work returns to Planning.

### Build Verification and Acceptance

**DP020-DETAIL-036**
Build verification establishes that the candidate is syntactically valid, mechanically conforming, operational for the planned functional set, and faithful to the accepted Plan.

**DP020-DETAIL-037**
Build acceptance advances the accepted repository state only after required Conformance and Assurance evidence is satisfied.

### Responsibility Routing

**DP020-DETAIL-038**
Defects route to the phase that owns the defective decision:

**DP020-DETAIL-039**
- semantic-intent defect → Design;
- functional-set, normative-distillation, or implementation-intent defect → Planning; and
- implementation-correctness defect → Build.
A downstream phase shall not repair an upstream defect by inventing missing authority or intent.

### Framework Contract Basis

**DP020-DETAIL-040**
This proposal assumes the Framework Contract Design statements:

**DP020-DETAIL-041**
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
Governance shall not assume authority beyond that delegated by the Framework Contract.

### Objective

**DP020-DETAIL-042**
Governance shall provide one controlled lifecycle through which detailed non-authoritative design intent becomes accepted repository state.

**DP020-DETAIL-043**
The primary Governance lifecycle shall be:

**DP020-DETAIL-044**
**Design**
→ **Design Proposal**
→ **Planning**
→ **Plan**
→ **Build**
The Design Proposal is the non-authoritative entry point.

**DP020-DETAIL-045**
Design, Planning, and Build are distinct governed stages.

**DP020-DETAIL-046**
Their responsibilities are:

**DP020-DETAIL-047**
**Design determines intended meaning and behavior and records it in Markdown Design Proposals.**
**Planning selects one bounded functional set, distills repository normative requirements as needed, and records exact implementation intent in a durable Plan.**
**Build produces syntactically correct, validated, operational source from the accepted Plan.**
A downstream stage shall not repair an upstream defect by inventing missing authority.

### Governance Boundary

**DP020-DETAIL-048**
Governance owns persistent normative change and governed progression between accepted stages.

**DP020-DETAIL-049**
Governance may:

**DP020-DETAIL-050**
- receive candidate design intent;
- create or amend accepted normative authority;
- establish accepted realization plans;
- authorize realization work;
- accept governed repository state;
- preserve change lineage;
- supersede or withdraw accepted normative authority;
- consume Conformance findings;
- consume Assurance findings; and
- route defects to the Governance stage responsible for resolving them.
Governance shall not:

**DP020-DETAIL-051**
- mechanically enforce normative requirements;
- replace Conformance with workflow completion;
- perform semantic review reserved to Assurance;
- treat Assurance findings as persistent normative authority without Governance acceptance;
- infer normative authority from implementation;
- allow Plan to invent missing Design authority;
- allow Build to invent missing Design authority;
- allow Build to invent missing Plan authority; or
- treat a Design Proposal as accepted authority.

### Stage Acceptance

**DP020-DETAIL-052**
Acceptance is the common Governance decision that promotes a candidate stage result into the accepted result of that stage.

**DP020-DETAIL-053**
Acceptance shall be:

**DP020-DETAIL-054**
- explicit;
- attributable;
- traceable; and
- distinguishable from incidental repository or platform activity.
Acceptance shall not arise solely because:

**DP020-DETAIL-055**
- code was merged;
- an issue was closed;
- Conformance passed;
- review approval was recorded;
- an AI agent declared completion; or
- downstream activity began.
Conformance or Assurance evidence may be required for acceptance without themselves constituting Governance acceptance.

**DP020-DETAIL-056**
The consequence of acceptance depends on the stage:

**DP020-DETAIL-057**
| Stage | Acceptance Consequence |
| --- | --- |
| Design | candidate Markdown Design Proposal revision becomes planning-ready Design input |
| Planning | candidate Plan artifact for one functional set becomes the accepted implementation contract for Build |
| Build | candidate realization becomes accepted repository state |

### Stage Rejection

**DP020-DETAIL-058**
A Governance stage may reject its candidate result.

**DP020-DETAIL-059**
Rejection shall preserve:

**DP020-DETAIL-060**
- the rejected candidate;
- the reason for rejection; and
- provenance to the governed work.
Rejected semantics, realization intent, or realization shall not become accepted merely because downstream artifacts or implementation exist.

### Feedback Routing

**DP020-DETAIL-061**
Governance shall route defects to the stage responsible for the defective responsibility.

### Design Routing

**DP020-DETAIL-062**
Work shall return to Design when:

**DP020-DETAIL-063**
- Design meaning is ambiguous;
- Design meaning is contradictory;
- required Design semantics are missing;
- a new semantic choice is required; or
- intended Design semantics require amendment.

### Planning Routing

**DP020-DETAIL-064**
Work shall return to Planning when:

**DP020-DETAIL-065**
- functional-set scope is incorrect or incomplete;
- normative distillation is incorrect or incomplete while Design meaning remains sound;
- planned implementation work is missing;
- dependency analysis is incomplete;
- sequencing is incorrect;
- implementation intent or validation intent must change; and
- intended Design semantics do not need to change.

### Build Routing

**DP020-DETAIL-066**
Work shall remain in Build when:

**DP020-DETAIL-067**
- implementation is incorrect;
- accepted Plan work is incomplete;
- generated artifacts are stale;
- implementation cleanup remains;
- required evidence has not been produced; and
- neither Design nor Plan must change.
The governing routing rule is:

**DP020-DETAIL-068**
**Semantic defect → Design**
**Planning-intent defect → Planning**
**Realization defect → Build**

### No Downstream Invention

**DP020-DETAIL-069**
A downstream Governance stage shall not create authority required from an upstream stage.

**DP020-DETAIL-070**
Plan shall not create normative semantics missing from Design.

**DP020-DETAIL-071**
Build shall not create normative semantics missing from Design.

**DP020-DETAIL-072**
Build shall not create realization intent missing from Plan.

**DP020-DETAIL-073**
Downstream discovery of an upstream defect shall cause backward routing rather than local invention.

### Governance Provenance

**DP020-DETAIL-074**
A completed Governance lifecycle shall preserve a resolvable lineage:

**DP020-DETAIL-075**
**Design Proposal**
→ **Design Proposal revision**
→ **planning-ready Design Proposal revision**
→ **Planning work**
→ **accepted Plan**
→ **Build governed work**
→ **accepted repository state**
The lineage shall make it possible to determine:

**DP020-DETAIL-076**
- why a change exists;
- what proposal initiated it;
- which Design Proposal revisions and Design statement IDs bounded the functional set;
- what normative requirements Planning distilled from that Design scope;
- what accepted Plan authorized realization;
- what Build realized that Plan; and
- what Conformance and Assurance evidence supported acceptance.

### Governed Work Provenance

**DP020-DETAIL-077**
Governed work shall not exist without resolvable authority.

**DP020-DETAIL-078**
Each governed Plan work item shall resolve through the accepted Plan to the Planning-distilled normative requirement or other explicit Plan intent that requires or authorizes it.

**DP020-DETAIL-079**
Each governed Build change shall resolve to an accepted Plan work item that authorizes the change.

**DP020-DETAIL-080**
The exact provenance representation belongs in detailed Governance authority.

### Normative Requirement Identity

**DP020-DETAIL-081**
Accepted normative obligations shall be represented by stable machine-resolvable normative requirement identities.

**DP020-DETAIL-082**
The normative requirement is the canonical addressable unit of accepted normative semantics.

**DP020-DETAIL-083**
A normative obligation shall not remain accepted only as unidentified prose that escapes Conformance and Assurance correspondence.

### Governed Identity

**DP020-DETAIL-084**
Governance artifacts participating in authoritative lineage shall have stable identities.

**DP020-DETAIL-085**
At minimum, identity shall exist for:

**DP020-DETAIL-086**
- Design Proposal;
- Design Proposal revision;
- accepted Design result;
- Planning work;
- accepted Plan result;
- Build governed work; and
- accepted Build result.
The exact identity representation belongs in detailed Governance authority.

### Evaluation Disposition

**DP020-DETAIL-087**
Each accepted normative requirement shall have governed Conformance and Assurance applicability.

**DP020-DETAIL-088**
A requirement for which Conformance applicability is `none` and Assurance applicability is `none` shall have a governed rationale explaining why neither keystone directly evaluates that requirement.

**DP020-DETAIL-089**
Governance owns acceptance of this cross-keystone disposition.

**DP020-DETAIL-090**
Neither Conformance nor Assurance shall independently determine the responsibility of the other keystone.

### Acceptance Authority

**DP020-DETAIL-091**
Governance acceptance shall depend only on authority accepted before the candidate result acquires the authority produced by that acceptance.

**DP020-DETAIL-092**
A candidate authority shall not require itself, or authority that exists only because that candidate has already been accepted, as a prerequisite for its own acceptance.

**DP020-DETAIL-093**
This prevents circular self-authorization during framework evolution and self-hosting.

### Governed State

**DP020-DETAIL-094**
Governance state shall be explicitly represented.

**DP020-DETAIL-095**
Governed authorization shall be bounded to explicitly governed scope.

**DP020-DETAIL-096**
A governed work item shall not independently authorize unrelated or successor work merely because the current work is accepted or complete.

**DP020-DETAIL-097**
A governed-work artifact shall not rely solely on surrounding platform state to determine its Governance state.

**DP020-DETAIL-098**
Detailed state vocabulary and transition rules belong in subordinate Governance authority.

### Authority Lifecycle

**DP020-DETAIL-099**
Governance shall support persistent normative-authority lifecycle operations including:

**DP020-DETAIL-100**
- creation;
- amendment;
- supersession; and
- withdrawal.
Superseded or withdrawn normative authority shall remain historically resolvable.

**DP020-DETAIL-101**
A normative identity shall not be reused in a manner that obscures previously accepted authority.

**DP020-DETAIL-102**
Authority lifecycle operations shall preserve lineage to the Governance work that authorized them.

### Relationship to Conformance

**DP020-DETAIL-103**
Governance may require Conformance evidence for stage acceptance.

**DP020-DETAIL-104**
Governance shall not define mechanical enforcement semantics merely because it requires such evidence.

**DP020-DETAIL-105**
Conformance remains responsible for mechanically evaluating observable state against accepted normative authority.

**DP020-DETAIL-106**
Passing Conformance does not create normative authority or constitute Governance acceptance.

### Relationship to Assurance

**DP020-DETAIL-107**
Governance may require Assurance findings for stage acceptance.

**DP020-DETAIL-108**
Assurance may identify:

**DP020-DETAIL-109**
- ambiguity;
- contradiction;
- semantic insufficiency;
- evidence insufficiency; and
- case-specific semantic conclusions.
Governance remains responsible for persistent normative change.

**DP020-DETAIL-110**
An Assurance finding requiring persistent semantic change shall route to Design.

**DP020-DETAIL-111**
An Assurance finding does not itself constitute Governance acceptance.

### Human and Automated Actors

**DP020-DETAIL-112**
Governance may be performed by humans, automated tooling, AI agents, or combinations of them where authorized.

**DP020-DETAIL-113**
Actor capability does not determine authority.

**DP020-DETAIL-114**
Authority derives from accepted Governance rules.

**DP020-DETAIL-115**
The ability to inspect, modify, merge, close, approve, or otherwise manipulate repository or platform state does not independently grant Governance authority.

### Governance Design Statements

**DP020-DETAIL-116**
The following proposal-local statements are Design input. Their labels are non-normative; Planning may distill repository normative requirements from any combination of selected Design statements.

### Governance Lifecycle

**DP020-DETAIL-117**
**Governance SHALL define Design, Plan, and Build as its three primary governed stages.**

### Design Proposal Entry

**DP020-DETAIL-118**
**A Governance lifecycle SHALL originate from a non-authoritative Design Proposal.**

### Distinct Governed Work

**DP020-DETAIL-119**
**Design, Plan, and Build SHALL each be represented by distinct governed work.**

### Stage Lineage

**DP020-DETAIL-120**
**Each governed stage SHALL resolve to the predecessor artifact or accepted result that authorizes it.**

### Design Authority

**DP020-DETAIL-121**
**Design SHALL be the Governance stage responsible for creating or changing accepted normative authority.**

### Plan Authority

**DP020-DETAIL-122**
**Plan SHALL be the Governance stage responsible for establishing realization intent for accepted Design authority.**

### Plan Semantic Boundary

**DP020-DETAIL-123**
**Plan SHALL NOT independently create or amend normative semantics.**

### Build Authority

**DP020-DETAIL-124**
**Build SHALL be the Governance stage responsible for realizing the accepted Plan.**

### Build Semantic Boundary

**DP020-DETAIL-125**
**Build SHALL NOT independently create or amend normative semantics.**

### Stage Separation

**DP020-DETAIL-126**
**A Governance stage SHALL NOT independently exercise authority assigned to another Governance stage.**

### Explicit Stage Acceptance

**DP020-DETAIL-127**
**A governed stage result SHALL NOT become accepted until explicitly accepted through Governance.**

### Acceptance Independence

**DP020-DETAIL-128**
**Governance acceptance SHALL NOT arise solely from incidental repository or platform activity.**

### Acceptance Consequence

**DP020-DETAIL-129**
**Acceptance SHALL promote only the candidate result belonging to the governed stage in which acceptance occurs.**

### Semantic Defect Routing

**DP020-DETAIL-130**
**A defect requiring persistent normative semantic change SHALL route to Design.**

### Plan Defect Routing

**DP020-DETAIL-131**
**A defect requiring realization-intent change without normative semantic change SHALL route to Plan.**

### No Downstream Invention

**DP020-DETAIL-132**
**A downstream Governance stage SHALL NOT create authority required from an upstream Governance stage.**

### Governance Lineage

**DP020-DETAIL-133**
**A completed Governance lifecycle SHALL preserve resolvable provenance from Design Proposal through Design, Plan, Build, and accepted repository state.**

### Governed Work Provenance

**DP020-DETAIL-134**
**Each governed realization work item SHALL resolve to accepted authority that requires or authorizes the work.**

### Design Delta

**DP020-DETAIL-135**
**An accepted Design result SHALL identify the normative authority created, amended, superseded, or withdrawn.**

### Plan Coverage

**DP020-DETAIL-136**
**An accepted Plan SHALL address each accepted Design obligation that requires governed realization work.**

### Explicit Governed State

**DP020-DETAIL-137**
**Governed-work state SHALL be explicitly represented rather than inferred solely from surrounding repository or platform state.**

### Authority Lifecycle

**DP020-DETAIL-138**
**Governance SHALL support creation, amendment, supersession, and withdrawal of accepted normative authority.**

### Historical Resolution

**DP020-DETAIL-139**
**Superseded or withdrawn normative authority SHALL remain historically resolvable.**

### Identity Preservation

**DP020-DETAIL-140**
**A normative identity SHALL NOT be reused in a manner that obscures previously accepted authority.**

### Normative Requirement Identity

**DP020-DETAIL-141**
**Each accepted normative obligation SHALL be represented by a stable machine-resolvable normative requirement identity.**

### Evaluation Disposition

**DP020-DETAIL-142**
**Each accepted normative requirement SHALL have governed Conformance and Assurance applicability, and a requirement with neither mechanical Conformance nor required Assurance SHALL have a governed rationale.**

### Acceptance Authority

**DP020-DETAIL-143**
**Governance acceptance SHALL depend only on authority accepted before the candidate result acquires the authority produced by that acceptance.**

### Bounded Governed Authorization

**DP020-DETAIL-144**
**A governed work item SHALL authorize only its explicitly governed scope and SHALL NOT independently authorize unrelated or successor work.**

### Primary Design Invariant

**DP020-DETAIL-145**
**Governance SHALL transform non-authoritative design intent into accepted repository state through a traceable Design → Plan → Build lifecycle in which accepted normative obligations have stable requirement identities and governed evaluation dispositions, Design owns normative semantics, Plan owns realization intent, Build realizes only accepted Plan work, governed authorization remains bounded to explicit scope, acceptance is explicit and depends only on previously accepted authority, and downstream stages route upstream defects rather than invent missing authority.**
All detailed Governance design shall preserve this invariant.

### Audit Questions

**DP020-DETAIL-146**
The current repository should be audited against this proposal by determining:

**DP020-DETAIL-147**
1. Which current workflows already perform Design, Plan, or Build responsibilities.
2. Which workflows combine multiple Governance stages into one governed artifact.
3. Which current mechanisms allow implementation to create de facto normative semantics.
4. Which current artifacts function as accepted authority without explicit Governance acceptance.
5. Which Plan or Build work lacks provenance to accepted authority.
6. Which processes treat merge, issue closure, Conformance success, review approval, or downstream activity as implicit acceptance.
7. Which normative changes bypass distinct Design Proposal revision.
8. Which Build activities require unresolved semantic decisions that belong in Design.
9. Which Plan activities create semantics not accepted by Design.
10. Which defects are currently repaired downstream rather than routed to the stage that owns them.
11. Which accepted Designs lack complete realization coverage in Plan.
12. Which superseded or withdrawn authority is not historically resolvable.
13. Which governed state is inferred from GitHub platform state rather than explicitly represented.
14. Whether the Audit / Normalize / Accept Design structure cleanly separates semantic discovery, normative production, and acceptance.
15. Whether the Analyze / Specify / Accept Plan structure cleanly separates impact analysis, realization planning, and acceptance.
16. Whether the Implement / Verify / Accept Build structure cleanly separates realization, evidence evaluation, and acceptance.
17. Whether each candidate GOV requirement represents one independently identifiable obligation.
18. Whether any candidate GOV requirement duplicates or logically follows from another.
19. Which GOV requirements are mechanically enforceable through Conformance.
20. Which GOV requirements require Assurance.
21. What minimum Governance authority must be accepted before Conformance and Assurance lifecycle integration can be normalized.

### Explicitly Deferred Concerns

**DP020-DETAIL-148**
The following concerns are intentionally outside this Governance proposal:

**DP020-DETAIL-149**
- exact GitHub issue schema;
- exact issue labels;
- detailed governed-state vocabulary;
- exact transition syntax;
- exact acceptance actor model;
- exact approval cardinality;
- detailed normative-requirement quality criteria;
- exact Conformance implementation;
- exact Assurance implementation;
- validation package architecture;
- review finding schema;
- implementation-language choices;
- migration execution details; and
- bootstrap sequencing.
These concerns may be defined by subordinate Governance authority or by Conformance and Assurance according to their delegated responsibilities.

### Relationship to Conformance and Assurance

**DP020-DETAIL-150**
The Conformance Architecture Proposal shall define how objective mechanical enforcement operates under accepted normative authority.

**DP020-DETAIL-151**
The Assurance Architecture Proposal shall define how governed semantic review and case-specific judgment operate under accepted normative authority.

**DP020-DETAIL-152**
Governance may consume outputs from both keystones but shall not absorb their responsibilities.

**DP020-DETAIL-153**
The Governance architecture should be normalized before lifecycle coupling to Conformance and Assurance is accepted.

### Normative Statement Contract

**DP020-DETAIL-154**
An accepted normative requirement shall represent exactly one independently governable normative rule.

**DP020-DETAIL-155**
A normative requirement statement shall be self-contained and shall identify an explicit normative subject, normative force, and required, prohibited, or expressly permitted behavior.

**DP020-DETAIL-156**
The normative force vocabulary for accepted normative requirement statements shall be `SHALL`, `SHALL NOT`, and `MAY`.

**DP020-DETAIL-157**
`SHALL` expresses required behavior, `SHALL NOT` expresses prohibited behavior, and `MAY` expresses explicit permission. Advisory or probabilistic force such as `SHOULD`, `SHOULD NOT`, `normally`, `generally`, or equivalent ambiguous obligation strength shall not be used in an accepted normative requirement unless separately defined by accepted authority.

**DP020-DETAIL-158**
A normative requirement may include conditions, scope qualifiers, and exceptions only when they are necessary to determine when the single normative rule applies.

**DP020-DETAIL-159**
A normative requirement shall not combine two or more obligations that could be independently conformed, assured, accepted, amended, superseded, or withdrawn.

**DP020-DETAIL-160**
Multiple subjects or behaviors may appear in one normative requirement only when they form one inseparable governed rule and cannot be independently dispositioned without changing that rule's meaning.

**DP020-DETAIL-161**
A normative requirement statement shall not depend on positional context such as preceding prose, following prose, section proximity, or unstated convention for its normative meaning. References required for meaning shall use stable resolvable identities.

**DP020-DETAIL-162**
A normative requirement statement shall contain normative semantics only. Rationale, explanatory commentary, examples, implementation instructions, pseudo-code, validation procedure, evidence, and review findings shall be represented outside the normative statement.

**DP020-DETAIL-163**
No arbitrary word or character count defines normative-statement validity. A normative statement shall be no longer than necessary to express its single rule unambiguously and no shorter than necessary to stand on its own.

**DP020-DETAIL-164**
Conformance may mechanically enforce structural properties of the normative-statement contract, including identity, required normative-force vocabulary, and forbidden structural forms. Assurance shall evaluate semantic atomicity, standalone sufficiency, ambiguity, inappropriate bundling, and whether splitting or combining statements would better preserve independently governable semantics.


### Modular Plan Artifact Contract

**DP020-DETAIL-165**
An accepted Plan SHALL remain one logical governed artifact even when represented by multiple physical documents.

**DP020-DETAIL-166**
`plan.json` SHALL be the canonical root manifest for a multi-document Plan.

**DP020-DETAIL-167**
Each authoritative Plan subdocument SHALL be explicitly reachable from `plan.json` through the Plan document graph.

**DP020-DETAIL-168**
A file SHALL NOT acquire Plan authority solely because it exists within a functional-set directory or adjacent to an accepted Plan document.

**DP020-DETAIL-169**
The Plan document graph SHALL be closed to documents not explicitly authorized by the accepted Plan graph.

**DP020-DETAIL-170**
A multi-document Plan SHALL separately represent normative requirements, file realization plans, execution ordering, invariants, validation, and completion conditions as governed Plan document classes.

**DP020-DETAIL-171**
Each file realization plan SHALL govern exactly one planned repository target path.

**DP020-DETAIL-172**
Each Plan subdocument SHALL resolve to the stable identity of the logical Plan to which it belongs.

**DP020-DETAIL-173**
Plan Conformance SHALL resolve and validate the complete authorized Plan document graph as one logical Plan before Planning acceptance.

**DP020-DETAIL-174**
Planning acceptance SHALL apply to the complete resolved Plan document graph rather than independently accepting individual Plan fragments.

**DP020-DETAIL-175**
Plan Conformance SHALL reject a Plan document graph containing a missing, duplicate, conflicting, unreachable, or unauthorized Plan document.


### FS0 Bootstrap Governance Contract

**DP020-DETAIL-176**
Before the FS0-Core runtime exists, authorized external human or automated actors MAY perform the Design Assurance, Planning Conformance, and Planning Assurance required to govern FS0-Core.

**DP020-DETAIL-177**
The candidate FS0-Core runtime SHALL NOT serve as an authority or evidentiary prerequisite for acceptance of the Plan that creates that runtime.

**DP020-DETAIL-178**
Bootstrap Design Assurance SHALL evaluate the exact Design Proposal revisions selected by FS0-Core.

**DP020-DETAIL-179**
Bootstrap Planning Conformance SHALL mechanically evaluate the FS0-Core Design inputs, functional-set scope, complete Plan document graph, and implementation-predecessor executability before Planning acceptance.

**DP020-DETAIL-180**
Bootstrap Planning Assurance SHALL evaluate the complete FS0-Core functional set and logical Plan using the semantic criteria required for later governed Planning Assurance.

**DP020-DETAIL-181**
Bootstrap Conformance and Assurance evidence required for FS0-Core acceptance SHALL be durable and resolvable from Governance acceptance lineage.

**DP020-DETAIL-182**
Bootstrap schemas that define functional-set and Plan artifact contracts MAY be created as governed Planning artifacts before FS0-Core Build.

**DP020-DETAIL-183**
A bootstrap Planning artifact SHALL NOT become FS0-Core implementation realization solely because the FS0-Core runtime consumes that artifact.

**DP020-DETAIL-184**
FS0-Core Build MAY consume accepted bootstrap Planning artifacts while retaining the pre-Planning accepted repository revision as its declared implementation predecessor.


### Pre-Build Design and Planning Artifact Bridge

**DP020-DETAIL-185**
Accepted Design and Planning artifacts MAY be committed after a Plan's declared implementation predecessor and before Build begins.

**DP020-DETAIL-186**
The existence of accepted Design or Planning artifact commits after the declared implementation predecessor SHALL NOT by itself change that implementation predecessor.

**DP020-DETAIL-187**
Build SHALL mechanically verify that repository changes between the declared implementation predecessor and Build start state are confined to governed Design and Planning artifact namespaces before treating those changes as pre-Build artifact-only state.

**DP020-DETAIL-188**
Build SHALL reject pre-Build artifact-only classification when any repository change between the declared implementation predecessor and Build start state mutates implementation realization outside governed Design and Planning artifact namespaces.


## Alternatives Considered

**Section ID:** `ALTERNATIVES`

**DP020-ALTERNATIVES-001**
Domain-specific alternatives remain in the detailed Design. The revised workflow rejects collapsing Design, Planning, and Build into one artifact or stage.

## Risks and Tradeoffs

**Section ID:** `RISKS`

**DP020-RISKS-001**
Incremental realization may expose missing or ambiguous Design later; those defects must route to Design rather than being silently invented during Planning or Build.

## Open Questions

**Section ID:** `OPEN-QUESTIONS`

**DP020-OPEN-QUESTIONS-001**
No blocking workflow-format questions remain. Domain-specific open questions are retained in the detailed Design.

## Acceptance Criteria

**Section ID:** `ACCEPTANCE`

**DP020-ACCEPTANCE-001**
This proposal is planning-ready when its required sections are complete, its detailed semantics remain coherent with declared dependencies, and its Design statements are addressable.
