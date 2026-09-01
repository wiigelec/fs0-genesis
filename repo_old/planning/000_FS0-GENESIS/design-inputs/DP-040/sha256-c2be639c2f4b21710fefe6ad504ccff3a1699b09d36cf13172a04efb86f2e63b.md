---
doc_id: DP-040
title: Assurance Architecture Proposal
status: planning-ready
depends_on:
  - DP-010
  - DP-020
  - DP-030
artifact_type: design-proposal
canonical_format: markdown
---

# Assurance Architecture Proposal

## Status

**Section ID:** `STATUS`

**DP040-STATUS-001**
Planning-ready Design Proposal.

## Purpose

**Section ID:** `PURPOSE`

**DP040-PURPOSE-001**
Define governed semantic review for Design readiness, Plan sufficiency, Build fidelity, and evidence sufficiency.

## Context

**Section ID:** `CONTEXT`

**DP040-CONTEXT-001**
Assurance must review semantic properties that cannot be decided mechanically while remaining subordinate to accepted authority.

## Goals

**Section ID:** `GOALS`

**DP040-GOALS-001**
- Preserve the domain architecture and authority boundaries defined by this proposal.
- Make the proposal consumable by incremental functional-set Planning.
- Keep Design statement identity distinct from repository normative identity.

## Non-Goals

**Section ID:** `NON-GOALS`

**DP040-NON-GOALS-001**
- Define one complete implementation plan for the entire proposal.
- Assign repository normative IDs during Design.
- Define file-level pseudo-code in Design unless it is itself a semantic constraint.

## Requirements

**Section ID:** `REQUIREMENTS`

**DP040-REQUIREMENTS-001**
The detailed Design below contains addressable Design statements. Statement IDs are non-normative proposal references. `functional-set.json` selects them; `plan.json` owns decomposition and normative distillation.

## Constraints

**Section ID:** `CONSTRAINTS`

**DP040-CONSTRAINTS-001**
This proposal remains subordinate to its declared Design dependencies and shall not silently assume authority outside them.

## Architecture

**Section ID:** `ARCHITECTURE`

**DP040-ARCHITECTURE-001**
The detailed Design below is semantic input to Planning and may be realized over multiple functional sets.

## Behavior

**Section ID:** `BEHAVIOR`

**DP040-BEHAVIOR-001**
Planning may consume a bounded subset of this proposal in one functional set; implementation of the entire proposal in one pass is not required.

## Interfaces and Boundaries

**Section ID:** `INTERFACES`

**DP040-INTERFACES-001**
Design defines meaning. `functional-set.json` defines selected Design scope. `plan.json` defines normative decomposition and exact implementation intent. Build produces syntactically correct, validated, operational code.

## Invariants

**Section ID:** `INVARIANTS`

**DP040-INVARIANTS-001**
- Design statement IDs remain non-normative.
- Planning owns normative distillation and implementation intent.
- Build shall not invent missing Design semantics or missing Plan intent.

## Detailed Design

**Section ID:** `DETAIL`

### Framework Contract Basis

**DP040-DETAIL-001**
This proposal assumes the Framework Contract Design statements:

**DP040-DETAIL-002**
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
Assurance shall not assume authority beyond that delegated by the Framework Contract.

### Governance Basis

**DP040-DETAIL-003**
This proposal assumes the Governance lifecycle:

**DP040-DETAIL-004**
**Design**
→ **Design Proposal**
→ **Planning**
→ **Plan**
→ **Build**
Governance owns persistent normative change.

**DP040-DETAIL-005**
Assurance may provide semantic findings to Governance where accepted Governance authority requires review.

**DP040-DETAIL-006**
An Assurance finding does not itself create or amend persistent normative authority.

**DP040-DETAIL-007**
A persistent semantic correction identified through Assurance shall route to Design when intended semantics must change, or to Planning when Design remains sound but normative distillation or implementation intent must change.

### Conformance Basis

**DP040-DETAIL-008**
Conformance mechanically evaluates objectively decidable obligations.

**DP040-DETAIL-009**
Conformance may provide Assurance with:

**DP040-DETAIL-010**
- mechanical findings;
- correspondence;
- assertion identities;
- evidence;
- closure results; and
- observed state.
Assurance may evaluate the semantic adequacy of those results.

**DP040-DETAIL-011**
Assurance shall not replace Conformance for mechanically decidable enforcement.

### Objective

**DP040-DETAIL-012**
Assurance shall provide one governed semantic-review architecture in which:

**DP040-DETAIL-013**
- every governed semantic review derives from accepted authority;
- review responsibility is explicit;
- review scope is explicit;
- evidence is identifiable;
- findings are attributable and traceable;
- interpretation remains within accepted normative semantics;
- semantic judgment remains bounded to the reviewed case;
- ambiguity and insufficiency are exposed rather than silently converted into persistent semantics; and
- persistent semantic change returns through Governance.
The primary relationship is:

**DP040-DETAIL-014**
**accepted normative authority**
→ **canonical Assurance correspondence**
→ **review obligation**
→ **review case**
→ **evidence**
→ **finding**
→ **case disposition or Governance routing**

### Assurance Boundary

**DP040-DETAIL-015**
Assurance owns governed semantic review and case-specific semantic judgment.

Assurance authority and reviewed subject are distinct. The accepted framework may authorize an Assurance review of a non-authoritative candidate artifact. In Design Assurance, the authorizing authority is accepted framework Assurance/Governance authority while the reviewed subject is the candidate Design Proposal; the Design Proposal does not need to be normative authority in order to be reviewed.

**DP040-DETAIL-016**
Assurance may:

**DP040-DETAIL-017**
- evaluate semantic clarity;
- evaluate normative requirement quality;
- identify ambiguity;
- identify contradiction;
- identify omission;
- identify overlap;
- identify inappropriate implementation leakage;
- evaluate evidence sufficiency;
- evaluate Conformance interpretation;
- evaluate realization fidelity;
- issue case-specific findings; and
- identify defects requiring Governance action.
Assurance shall not:

**DP040-DETAIL-018**
- create persistent normative authority;
- amend accepted normative authority;
- extend or narrow accepted normative semantics;
- convert reviewer preference into authority;
- mechanically enforce obligations reserved to Conformance;
- redefine Conformance predicates directly;
- redefine Governance authority; or
- convert prior findings into persistent precedent without accepted authority.

### Assurance Terminology

### Assurance Primitive

**DP040-DETAIL-019**
A maintained artifact whose purpose participates in governed semantic review.

**DP040-DETAIL-020**
Assurance primitives may include:

**DP040-DETAIL-021**
- Assurance correspondence;
- review obligations;
- review cases;
- evidence manifests;
- reviewer instructions;
- rubrics;
- findings;
- dispositions;
- semantic checklists;
- Assurance schemas; and
- generated Assurance views.

### Assurance Correspondence

**DP040-DETAIL-022**
The governed relationship between accepted authority and Assurance responsibility.

**DP040-DETAIL-023**
Assurance correspondence identifies whether semantic-review responsibility exists and, where applicable, the review obligations derived from that authority.

**DP040-DETAIL-024**
Correspondence does not independently own normative semantics.

### Review Obligation

**DP040-DETAIL-025**
An independently identifiable semantic-review responsibility derived from accepted authority.

**DP040-DETAIL-026**
A review obligation defines why governed semantic review is required.

### Review Case

**DP040-DETAIL-027**
A bounded invocation of one or more review obligations against identified subject matter and evidence.

**DP040-DETAIL-028**
A review case provides the context within which Assurance judgment is valid.

### Evidence

**DP040-DETAIL-029**
Information considered by Assurance in a review case.

**DP040-DETAIL-030**
Evidence may include:

**DP040-DETAIL-031**
- accepted normative authority;
- Governance artifacts;
- Conformance findings;
- Conformance correspondence;
- implementation;
- repository state;
- generated artifacts;
- historical provenance; and
- prior Assurance findings.
Evidence does not acquire normative authority merely because it is considered during review.

### Finding

**DP040-DETAIL-032**
A governed semantic conclusion produced for a review case.

**DP040-DETAIL-033**
A finding remains bounded to that case unless persistent semantics are subsequently established through Governance.

### Closed Assurance Hierarchy

**DP040-DETAIL-034**
Governed semantic review shall occur only through the authorized Assurance hierarchy.

**DP040-DETAIL-035**
A maintained artifact whose purpose participates in governed semantic review shall participate in that hierarchy.

**DP040-DETAIL-036**
Applicable artifacts may include:

**DP040-DETAIL-037**
- Assurance correspondence;
- review obligations;
- review cases;
- evidence manifests;
- reviewer instructions;
- rubrics;
- findings;
- dispositions;
- semantic checklists;
- Assurance schemas; and
- generated Assurance views.
Artifacts outside the governed Assurance hierarchy shall not independently produce governed Assurance findings.

**DP040-DETAIL-038**
General analysis may inform Assurance.

**DP040-DETAIL-039**
It does not acquire Assurance authority merely because it exists.

### Purpose of the Closed Hierarchy

**DP040-DETAIL-040**
The closed Assurance hierarchy is an authority-control mechanism.

**DP040-DETAIL-041**
It prevents:

**DP040-DETAIL-042**
- reviewer preference becoming policy;
- AI interpretation becoming implicit authority;
- findings with no normative basis;
- reviews with undefined scope;
- findings disconnected from evidence;
- findings disconnected from authority;
- repeated conclusions becoming undeclared precedent;
- ad hoc semantic gates; and
- semantic obligations hidden outside governed review structure.
The expected relationship is:

**DP040-DETAIL-043**
**accepted authority**
→ **canonical Assurance correspondence**
→ **review obligation**
→ **review case**
→ **evidence**
→ **finding**

### Canonical Assurance Correspondence

**DP040-DETAIL-044**
Each active normative requirement shall have exactly one canonical Assurance correspondence record.

**DP040-DETAIL-045**
The correspondence shall identify:

**DP040-DETAIL-046**
- normative requirement identity;
- Assurance applicability; and
- applicable review obligations where Assurance is required.
The correspondence record shall not restate normative requirement semantics as independent authority.

### Assurance Applicability

**DP040-DETAIL-047**
Each active normative requirement shall have exactly one canonical Assurance applicability determination.

**DP040-DETAIL-048**
The candidate vocabulary is:

### `required`

**DP040-DETAIL-049**
The normative requirement has governed semantic-review responsibility.

**DP040-DETAIL-050**
At least one review obligation shall exist.

### `none`

**DP040-DETAIL-051**
No Assurance responsibility exists for the normative requirement under accepted authority.

**DP040-DETAIL-052**
A rationale may be required where absence of Assurance responsibility is not self-evident.

**DP040-DETAIL-053**
Assurance applicability describes only Assurance responsibility.

**DP040-DETAIL-054**
It does not encode Conformance responsibility.

### Cross-Keystone Applicability

**DP040-DETAIL-055**
Conformance and Assurance applicability are independent dimensions.

**DP040-DETAIL-056**
A requirement may therefore be:

**DP040-DETAIL-057**
| Conformance | Assurance | Meaning |
| --- | --- | --- |
| mechanical | none | mechanical enforcement only |
| none | required | semantic review only |
| mechanical | required | both mechanical and semantic responsibility |
| none | none | neither keystone directly evaluates the requirement |
The final combination should be explicitly justified where meaningful enforcement or review might otherwise be expected.

**DP040-DETAIL-058**
This model replaces overloaded concepts such as `partial` or `semantic-review` dispositions spanning multiple keystones.

### Review Obligation Model

**DP040-DETAIL-059**
A review obligation represents one independently identifiable semantic-review responsibility.

**DP040-DETAIL-060**
Examples may include:

**DP040-DETAIL-061**
- ambiguity review;
- requirement-quality review;
- Conformance-applicability review;
- assertion-interpretation review;
- evidence-sufficiency review;
- realization-fidelity review;
- conflict review; and
- Governance-stage review.
A normative requirement or other accepted framework authority may derive multiple review obligations.

**DP040-DETAIL-062**
Review-obligation identity is distinct from:

**DP040-DETAIL-063**
- normative requirement identity;
- review-case identity;
- reviewer identity; and
- finding identity.

### Review Obligation Authority

**DP040-DETAIL-064**
Every maintained review obligation shall resolve to accepted authority requiring or authorizing the review.

**DP040-DETAIL-065**
Assurance shall not create mandatory semantic-review obligations merely because additional review appears useful.

**DP040-DETAIL-066**
Exploratory analysis may occur without becoming governed Assurance responsibility.

### Assurance Provenance

**DP040-DETAIL-067**
Every maintained Assurance primitive shall resolve through governed provenance to accepted authority.

**DP040-DETAIL-068**
The provenance chain shall permit resolution of:

**DP040-DETAIL-069**
**accepted authority**
→ **review obligation**
→ **review case**
→ **finding**
Evidence used by a finding shall also be identifiable.

**DP040-DETAIL-070**
No orphan Assurance finding is permitted.

### Review Case Identity

**DP040-DETAIL-071**
Each governed Assurance review case shall have a stable unique identity.

**DP040-DETAIL-072**
Case identity shall be distinct from:

**DP040-DETAIL-073**
- normative requirement identity;
- review-obligation identity;
- reviewer identity; and
- finding identity.
This permits repeated reviews against the same authority without conflating their conclusions.

### Review Scope

**DP040-DETAIL-074**
Every review case shall explicitly define its scope.

**DP040-DETAIL-075**
A review case shall distinguish:

**DP040-DETAIL-076**
- **authorizing authority** — accepted authority that requires or permits Assurance to perform the review; and
- **review subject** — the candidate authority, accepted authority, Governance artifact, Conformance artifact, implementation, repository state, or other material being evaluated.
This distinction permits Assurance to review non-authoritative candidates without allowing the candidate to authorize its own review.

**DP040-DETAIL-077**
Scope shall identify, as applicable:

**DP040-DETAIL-078**
- authorizing authority;
- reviewed subject matter;
- review obligations being exercised;
- Governance artifact or stage under review;
- Conformance correspondence or assertions under review;
- implementation or repository state under review;
- relevant evidence; and
- relevant exclusions.
A finding shall not silently claim semantic effect outside the defined review scope.

### Finding Identity

**DP040-DETAIL-079**
Each maintained Assurance finding shall have a stable identity within its review case.

**DP040-DETAIL-080**
A finding identity shall not be reused for an unrelated conclusion.

**DP040-DETAIL-081**
Findings participating in Governance lineage or later evidence shall remain historically resolvable.

### Finding Traceability

**DP040-DETAIL-082**
Each Assurance finding shall resolve to:

**DP040-DETAIL-083**
- its review case;
- applicable review obligation;
- authorizing authority;
- reviewed subject matter; and
- evidence basis.
A finding should distinguish:

**DP040-DETAIL-084**
- observation;
- semantic analysis;
- conclusion; and
- recommended action.
The exact representation belongs in subordinate Assurance authority.

### Review Execution Closure

**DP040-DETAIL-085**
A review obligation may exist without being continuously active.

**DP040-DETAIL-086**
When accepted authority triggers a review obligation for a governed decision, that obligation shall be realized by a governed review case before the decision may be accepted.

**DP040-DETAIL-087**
A declared review obligation that is triggered but never instantiated does not satisfy Assurance responsibility.

### Assurance Semantic Boundary

**DP040-DETAIL-088**
Assurance judgment is bounded to the authorized review case in which it is issued.

**DP040-DETAIL-089**
An Assurance finding shall not independently:

**DP040-DETAIL-090**
- create normative authority;
- amend normative authority;
- supersede normative authority;
- withdraw normative authority;
- establish persistent normative semantics beyond the reviewed case; or
- establish persistent precedent.
A case-specific finding may affect disposition of the reviewed case where accepted authority grants that effect.

**DP040-DETAIL-091**
Persistent semantic effect requires Governance.

### Interpretation Boundary

**DP040-DETAIL-092**
Assurance may interpret accepted authority when necessary to decide a bounded review case.

**DP040-DETAIL-093**
Interpretation shall remain anchored to accepted normative semantics.

**DP040-DETAIL-094**
Assurance shall not independently:

**DP040-DETAIL-095**
- manufacture missing obligations;
- broaden accepted obligations;
- narrow accepted obligations;
- convert implementation preference into semantics; or
- permanently settle unresolved ambiguity.
Where materially different interpretations remain reasonable, Assurance should identify ambiguity rather than create persistent resolution.

### Governance Routing

**DP040-DETAIL-096**
A finding requiring persistent normative semantic change shall route through Governance Design.

**DP040-DETAIL-097**
Examples include:

**DP040-DETAIL-098**
- ambiguous accepted authority;
- contradictory authority;
- missing normative semantics;
- requirement-quality defects requiring rewritten authority;
- persistent interpretation disputes; and
- desired precedent not already established by accepted authority.
Assurance identifies the semantic defect.

**DP040-DETAIL-099**
Governance owns its persistent resolution.

### Finding Classes

**DP040-DETAIL-100**
Assurance may distinguish finding classes such as:

### `satisfied`

**DP040-DETAIL-101**
The reviewed semantic responsibility is adequately satisfied for the bounded case.

### `concern`

**DP040-DETAIL-102**
A semantic issue exists but does not necessarily prevent disposition.

### `insufficient`

**DP040-DETAIL-103**
Available evidence or reasoning is insufficient to establish the required conclusion.

### `ambiguous`

**DP040-DETAIL-104**
Accepted authority supports materially different relevant interpretations.

### `contradictory`

**DP040-DETAIL-105**
Applicable accepted authority contains incompatible semantics.

### `defect`

**DP040-DETAIL-106**
The reviewed realization, correspondence, or interpretation conflicts with accepted authority.

### `governance-required`

**DP040-DETAIL-107**
Persistent normative action is required before the semantic issue can be properly resolved.

**DP040-DETAIL-108**
The exact vocabulary belongs in subordinate Assurance design.

### Evidence Sufficiency

**DP040-DETAIL-109**
Assurance may evaluate whether evidence is semantically sufficient for a governed claim.

**DP040-DETAIL-110**
Evidence sufficiency is distinct from evidence existence.

**DP040-DETAIL-111**
Conformance may mechanically determine:

**DP040-DETAIL-112**
- whether evidence exists;
- whether required evidence categories are present; and
- whether evidence conforms structurally.
Assurance may determine:

**DP040-DETAIL-113**
- whether evidence meaningfully supports the claimed conclusion;
- whether evidence scope matches the claim;
- whether relevant cases are omitted;
- whether evidence relies on incorrect semantic interpretation; and
- whether the evidence is sufficient for the governed review purpose.
Detailed evidence-sufficiency policies belong in subordinate Assurance authority.

### Normative Requirement Quality

**DP040-DETAIL-114**
Assurance may evaluate semantic properties of normative requirements that cannot be reliably decided mechanically.

**DP040-DETAIL-115**
Examples include:

**DP040-DETAIL-116**
- atomicity;
- clarity;
- ambiguity;
- contradiction;
- overlap;
- duplication;
- inappropriate implementation leakage;
- undefined subjective qualifiers;
- hidden obligations inside rationale; and
- inappropriate coupling of independent obligations.
Assurance findings about requirement quality do not themselves amend the requirement.

**DP040-DETAIL-117**
Persistent correction occurs through Governance.

### Mechanical Quality and Semantic Quality

**DP040-DETAIL-118**
Requirement quality spans multiple keystones.

**DP040-DETAIL-119**
**Governance** owns creation and acceptance of normative authority.
**Conformance** may mechanically enforce objectively decidable structural quality rules.
**Assurance** may evaluate semantic quality requiring judgment.
No keystone gains the authority of another merely because all three participate in requirement quality.

### Conformance Review

**DP040-DETAIL-120**
Where authorized, Assurance may evaluate whether Conformance faithfully represents accepted normative authority.

**DP040-DETAIL-121**
Assurance may review:

**DP040-DETAIL-122**
- Conformance applicability;
- assertion decomposition;
- assertion interpretation;
- evidence sufficiency;
- over-enforcement;
- under-enforcement; and
- claims of mechanical decidability.
Assurance may issue findings about Conformance.

**DP040-DETAIL-123**
It shall not directly create persistent Conformance semantics.

**DP040-DETAIL-124**
Persistent correction routes through Governance.

### Realization Fidelity

**DP040-DETAIL-125**
Where authorized, Assurance may review whether realization faithfully reflects accepted normative intent.

**DP040-DETAIL-126**
This review may identify semantic defects not completely captured by mechanical assertions.

**DP040-DETAIL-127**
Examples include:

**DP040-DETAIL-128**
- semantic omission;
- inappropriate abstraction;
- unintended interpretation;
- misleading derived documentation; and
- mechanically valid but semantically inadequate realization.
Assurance shall not rewrite authority to conform to existing implementation.

### Governance Stage Review

**DP040-DETAIL-129**
Governance may require Assurance at defined stage gates.

### Design Assurance

**DP040-DETAIL-130**
May evaluate:

**DP040-DETAIL-131**
- requirement quality;
- semantic clarity;
- atomicity;
- internal consistency;
- authority boundaries; and
- unresolved ambiguity.

### Plan Assurance

**DP040-DETAIL-132**
May evaluate:

**DP040-DETAIL-133**
- fidelity to accepted Design;
- semantic completeness of realization intent;
- inappropriate reinterpretation; and
- adequacy of planned semantic evidence.

### Build Assurance

**DP040-DETAIL-134**
May evaluate:

**DP040-DETAIL-135**
- realization fidelity;
- evidence sufficiency;
- semantic fidelity of Conformance; and
- unresolved semantic defects.
Governance decides whether review is required.

**DP040-DETAIL-136**
Assurance produces the finding.

**DP040-DETAIL-137**
Governance performs acceptance.

### Reviewer Attribution

**DP040-DETAIL-138**
Assurance findings shall be attributable to the actor or governed actor class responsible for review.

**DP040-DETAIL-139**
Reviewers may include:

**DP040-DETAIL-140**
- humans;
- AI agents;
- automated semantic systems; or
- governed combinations of actors.
Reviewer identity does not create authority.

**DP040-DETAIL-141**
The reviewer's ability, expertise, confidence, or implementation access does not independently enlarge Assurance authority.

### Human and AI Review

**DP040-DETAIL-142**
Human and AI reviewers are subject to the same accepted Assurance boundaries.

**DP040-DETAIL-143**
AI-assisted review may be useful for:

**DP040-DETAIL-144**
- ambiguity detection;
- requirement-decomposition analysis;
- cross-specification consistency review;
- provenance review;
- evidence analysis; and
- implementation-to-authority comparison.
An AI reviewer shall not:

**DP040-DETAIL-145**
- treat confidence as authority;
- invent persistent semantics;
- create undeclared precedent;
- infer authority from implementation;
- waive Governance obligations; or
- waive Conformance obligations.
Human reviewers shall not acquire those powers merely through judgment or expertise either.

### Prior Findings

**DP040-DETAIL-146**
Prior Assurance findings may be evidence in later review cases.

**DP040-DETAIL-147**
Prior findings are not automatically binding precedent.

**DP040-DETAIL-148**
Absent accepted authority establishing a precedent model, a prior finding remains a case-specific conclusion.

**DP040-DETAIL-149**
Repeated identical findings do not independently transform the conclusion into persistent normative authority.

### Conflicting Findings

**DP040-DETAIL-150**
Multiple Assurance cases may produce materially conflicting findings.

**DP040-DETAIL-151**
Conflict shall remain explicit until resolved through an authorized governed mechanism.

**DP040-DETAIL-152**
Assurance shall not hide the conflict by selecting one preferred interpretation as persistent semantics.

**DP040-DETAIL-153**
If persistent semantic resolution is required, the conflict shall route through Governance.

### Single Assurance Correspondence Authority

**DP040-DETAIL-154**
Assurance shall define one canonical authority for requirement-to-Assurance correspondence.

**DP040-DETAIL-155**
Independently maintained mappings shall not be allowed to silently diverge.

**DP040-DETAIL-156**
Operational representations may exist in:

**DP040-DETAIL-157**
- correspondence records;
- governed-work metadata;
- review manifests;
- reviewer tooling;
- generated reports; and
- documentation.
Where multiple representations are required, they shall be generated from canonical correspondence or mechanically verified against it.

### Assurance Correspondence Integrity

**DP040-DETAIL-158**
Canonical Assurance correspondence shall remain consistent with the maintained review-obligation graph.

**DP040-DETAIL-159**
Examples of defects include:

**DP040-DETAIL-160**
- `required` applicability with no review obligation;
- review obligation referencing unknown authority;
- review case referencing nonexistent obligations;
- finding with no review case;
- finding with no authority reference; and
- divergent duplicate mappings.
Objectively decidable integrity properties may themselves be mechanically enforced through Conformance.

### Generated Assurance Views

**DP040-DETAIL-161**
Generated Assurance views may expose:

**DP040-DETAIL-162**
- normative requirement identity;
- Assurance applicability;
- review obligations;
- review cases;
- findings;
- unresolved ambiguity;
- Governance routing; and
- historical findings.
Generated views remain subordinate derived artifacts.

**DP040-DETAIL-163**
They do not independently establish semantic authority.

### Assurance Defects

**DP040-DETAIL-164**
Examples of Assurance defects include:

**DP040-DETAIL-165**
- review obligation with no accepted authority;
- required review responsibility with no review obligation;
- review case with undefined scope;
- finding without evidence basis;
- finding without accepted authority;
- finding exceeding case scope;
- interpretation extending or narrowing accepted semantics;
- reviewer preference treated as authority;
- repeated findings treated as precedent without authorization;
- semantic review occurring outside the governed hierarchy;
- divergent correspondence mappings; and
- persistent ambiguity being silently resolved without Governance.
An Assurance defect shall not be repaired by inventing normative authority.

### Relationship to Governance

**DP040-DETAIL-166**
Governance changes accepted normative authority.

**DP040-DETAIL-167**
Assurance consumes accepted authority and produces semantic findings.

**DP040-DETAIL-168**
Routing follows the responsibility owning the defect.

### Semantic Authority Defect

**DP040-DETAIL-169**
**Assurance → Design**

### Realization-Intent Defect

**DP040-DETAIL-170**
**Assurance → Planning**
when accepted semantics remain sound.

### Realization Defect

**DP040-DETAIL-171**
**Assurance → Build**
when Design and Plan remain sound.

### Case-Specific Finding

**DP040-DETAIL-172**
Return to the governed consumer or Governance stage requesting the review.

**DP040-DETAIL-173**
Governance determines persistent disposition.

### Relationship to Conformance

**DP040-DETAIL-174**
Conformance establishes mechanically decidable facts.

**DP040-DETAIL-175**
Assurance evaluates semantic matters requiring judgment.

**DP040-DETAIL-176**
Assurance may conclude that Conformance:

**DP040-DETAIL-177**
- faithfully represents authority;
- over-enforces;
- under-enforces;
- incompletely represents authority;
- uses semantically insufficient evidence; or
- claims mechanical determinacy where ambiguity remains.
Assurance shall not directly rewrite persistent Conformance semantics.

**DP040-DETAIL-178**
Persistent correction routes through Governance.

### Assurance Design Statements

**DP040-DETAIL-179**
The following proposal-local statements are Design input. Their labels are non-normative; Planning may distill repository normative requirements from any combination of selected Design statements.

### Governed Assurance Hierarchy

**DP040-DETAIL-180**
**Governed semantic review and case-specific semantic judgment SHALL occur only through the authorized Assurance hierarchy.**

### Assurance Provenance

**DP040-DETAIL-181**
**Every maintained Assurance primitive SHALL resolve through governed provenance to accepted authority.**

### Canonical Assurance Correspondence

**DP040-DETAIL-182**
**Each active normative requirement SHALL have exactly one canonical Assurance correspondence record.**

### Assurance Applicability

**DP040-DETAIL-183**
**Each active normative requirement SHALL have exactly one canonical Assurance applicability determination.**

### Required Review Coverage

**DP040-DETAIL-184**
**Each normative requirement with required Assurance applicability SHALL resolve to at least one governed review obligation.**

### Review Obligation Identity

**DP040-DETAIL-185**
**Each maintained Assurance review obligation SHALL have a stable unique identity.**

### Review Case Identity

**DP040-DETAIL-186**
**Each governed Assurance review case SHALL have a stable unique identity.**

### Review Case Scope

**DP040-DETAIL-187**
**Each governed Assurance review case SHALL explicitly identify its authorizing authority, review obligations, and reviewed subject matter.**

### Finding Identity

**DP040-DETAIL-188**
**Each maintained Assurance finding SHALL have a stable identity within its review case.**

### Finding Traceability

**DP040-DETAIL-189**
**Each Assurance finding SHALL resolve to its review case, applicable review obligation, authorizing authority, reviewed subject matter, and evidence basis.**

### Assurance Semantic Boundary

**DP040-DETAIL-190**
**An Assurance finding SHALL NOT independently create, amend, supersede, withdraw, or establish persistent normative semantics beyond its authorized review case.**

### Governance Routing

**DP040-DETAIL-191**
**An Assurance finding showing that intended Design meaning must change SHALL route to Design; a finding showing defective normative distillation while Design meaning remains sound SHALL route to Planning.**

### Interpretation Boundary

**DP040-DETAIL-192**
**Assurance interpretation SHALL remain within accepted normative semantics and SHALL NOT independently extend or narrow those semantics.**

### Single Correspondence Authority

**DP040-DETAIL-193**
**Requirement-to-Assurance correspondence SHALL NOT depend on independently maintained mappings that may silently diverge.**

### Review Execution Closure

**DP040-DETAIL-194**
**Each triggered Assurance review obligation SHALL be realized by a governed review case before the governed decision requiring that review may be accepted.**

### Primary Design Invariant

**DP040-DETAIL-195**
**Assurance SHALL provide governed semantic review through a closed provenance model in which every maintained Assurance primitive derives from accepted authority, every triggered review obligation is realized by a traceable and explicitly scoped review case, every finding resolves to its authorizing authority, reviewed subject matter, and evidence basis, interpretation remains within accepted normative semantics, findings remain bounded to their authorized cases, and persistent semantic change returns through Governance.**
All detailed Assurance design shall preserve this invariant.

### Audit Questions

**DP040-DETAIL-196**
The current repository should be audited against this proposal by determining:

**DP040-DETAIL-197**
1. Which current semantic review practices qualify as Assurance.
2. Which semantic review practices exist only as informal convention.
3. Which active normative requirements require Assurance responsibility.
4. Which active normative requirements have no meaningful Assurance responsibility.
5. Which existing `semantic-review` validation dispositions should become Assurance applicability.
6. Which existing `partial` dispositions should become independent Conformance and Assurance relationships.
7. Which review obligations currently have no accepted authority.
8. Which required Assurance relationships have no identifiable review obligation.
9. Which current reviews lack stable review-case identity.
10. Which review cases lack explicit scope.
11. Which findings lack stable identity.
12. Which findings lack resolvable review obligations.
13. Which findings lack resolvable normative authority.
14. Which findings lack identifiable evidence basis.
15. Which current findings exceed the semantic scope of their review cases.
16. Which reviewer conclusions have become de facto persistent semantics without Governance.
17. Which prior findings are being treated as precedent without accepted precedent authority.
18. Which current semantic interpretations broaden or narrow accepted authority.
19. Which current requirement-quality checks belong to Conformance because they are mechanically decidable.
20. Which requirement-quality checks require Assurance judgment.
21. Which current Conformance applicability decisions require Assurance review.
22. Which current assertions may over-enforce or under-enforce accepted authority.
23. Which mechanically complete evidence sets may remain semantically insufficient.
24. Which Governance stage gates should require Assurance.
25. Which Assurance correspondence mappings are duplicated across metadata, review tooling, templates, or generated documentation.
26. Whether each Planning-distilled normative requirement selected for Assurance represents one independently identifiable obligation.
27. Whether any Planning-distilled normative requirement selected for Assurance duplicates or logically follows from another.
28. Which Planning-distilled normative requirements selected for Assurance also have mechanically decidable Conformance obligations.
29. What framework authority must authorize Assurance at Design-readiness, Planning-acceptance, or Build-acceptance decisions.

### Explicitly Deferred Concerns

**DP040-DETAIL-198**
The following concerns are intentionally outside this Assurance proposal:

**DP040-DETAIL-199**
- exact Assurance correspondence schema;
- exact review-obligation schema;
- exact review-case schema;
- exact finding schema;
- exact finding vocabulary;
- exact reviewer-assignment rules;
- exact reviewer cardinality;
- exact reviewer-independence rules;
- exact AI/human reviewer composition;
- exact confidence representation;
- exact semantic review rubrics;
- exact evidence-manifest representation;
- exact precedent model;
- exact generated report format;
- migration sequencing from current review practices; and
- bootstrap accommodations.
These concerns may be defined by later Design or by Planning when they are implementation choices rather than Design semantics.

### Relationship to the Framework

**DP040-DETAIL-200**
The proposed framework model is:

**DP040-DETAIL-201**
**Framework Contract**
→ defines authority topology
**Governance**
→ controls persistent normative change
**Conformance**
→ mechanically enforces accepted normative authority
**Assurance**
→ performs governed semantic review and case-specific judgment
The three keystones interact without absorbing one another's powers.

**DP040-DETAIL-202**
Governance changes authority.

**DP040-DETAIL-203**
Conformance mechanically evaluates authority.

**DP040-DETAIL-204**
Assurance semantically evaluates authority, realization, and evidence.

**DP040-DETAIL-205**
Persistent semantic change returns through Governance.

### Workflow Assurance

**DP040-DETAIL-206**
Assurance evaluates semantic questions that cannot be decided mechanically in the Design → Planning → Build workflow.

#### Design Assurance

**DP040-DETAIL-207**
Design Assurance evaluates whether a Design Proposal is semantically ready for Planning.

**DP040-DETAIL-208**
Review includes:

**DP040-DETAIL-209**
- clarity and coherence;
- completeness relative to the proposal's stated scope;
- internal consistency;
- architecture and boundary quality;
- unresolved ambiguity;
- material omissions;
- alternatives and tradeoffs;
- risks; and
- whether blocking Design questions remain.
Design Assurance does not assign repository normative identities or perform Planning decomposition.

#### Planning Assurance

**DP040-DETAIL-210**
Planning Assurance evaluates the selected functional set and Plan.

**DP040-DETAIL-211**
Review includes:

**DP040-DETAIL-212**
- fidelity to the exact Design Proposal revisions consumed;
- functional-set coherence and end-to-end usefulness;
- functional-set manageability for one implementation cycle;
- appropriate normative distillation;
- absence of semantic invention;
- exact file-scope completeness;
- pseudo-code or implementation-specification sufficiency;
- invariant sufficiency;
- validation sufficiency; and
- evidence that the Plan is executable against the accepted predecessor.
Normative requirement quality is reviewed where Planning distills normative requirements, not as an output of Design.

#### Build Assurance

**DP040-DETAIL-213**
Build Assurance evaluates semantic realization fidelity.

**DP040-DETAIL-214**
Review includes:

**DP040-DETAIL-215**
- fidelity to the accepted Plan;
- fidelity to the selected Design through the Plan;
- operational adequacy;
- handling of edge and failure behavior where semantically material;
- absence of unauthorized improvisation; and
- evidence sufficiency.
Assurance findings remain case-specific. Persistent semantic correction returns to Design when intended meaning must change, or to Planning when Design remains sound but functional-set scope, normative distillation, or implementation intent must change.

### FS0 Bootstrap Assurance

**DP040-DETAIL-216**
Before the candidate FS0-Core Assurance runtime exists, authorized bootstrap Assurance MAY perform Design Assurance and Planning Assurance for FS0-Core.

**DP040-DETAIL-217**
Bootstrap Design Assurance SHALL apply the Design Assurance criteria to the exact Design Proposal revisions selected by FS0-Core.

**DP040-DETAIL-218**
Bootstrap Planning Assurance SHALL apply the Planning Assurance criteria to the complete FS0-Core functional set and resolved logical Plan.

**DP040-DETAIL-219**
Candidate FS0-Core Assurance results SHALL NOT be prerequisites for accepting the Plan that creates the candidate FS0-Core Assurance runtime.


## Alternatives Considered

**Section ID:** `ALTERNATIVES`

**DP040-ALTERNATIVES-001**
Domain-specific alternatives remain in the detailed Design. The revised workflow rejects collapsing Design, Planning, and Build into one artifact or stage.

## Risks and Tradeoffs

**Section ID:** `RISKS`

**DP040-RISKS-001**
Incremental realization may expose missing or ambiguous Design later; those defects must route to Design rather than being silently invented during Planning or Build.

## Open Questions

**Section ID:** `OPEN-QUESTIONS`

**DP040-OPEN-QUESTIONS-001**
No blocking workflow-format questions remain. Domain-specific open questions are retained in the detailed Design.

## Acceptance Criteria

**Section ID:** `ACCEPTANCE`

**DP040-ACCEPTANCE-001**
This proposal is planning-ready when its required sections are complete, its detailed semantics remain coherent with declared dependencies, and its Design statements are addressable.
