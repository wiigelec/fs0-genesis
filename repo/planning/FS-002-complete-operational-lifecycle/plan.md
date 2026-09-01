# FS-002 Plan — Complete Operational Lifecycle

## Technical Objective

Complete the accepted repository lifecycle for normal repeated use by removing bootstrap-only assumptions and making the existing project-native mechanisms operate over current Functional Sets generically.

This is intended to be the final planned framework Functional Set for the current Design. Build should prefer direct repository-specific logic over new abstractions.

## Canonical Functional Set Representation

A current Functional Set is represented by a matching pair of canonical surfaces:

```text
repo/planning/FS-NNN-name/
  functional-set.md
  plan.md

repo/specs/FS-NNN-name.md
```

The shared `FS-NNN-name` basename provides direct correspondence between the Planning directory and normative specification.

Functional Set discovery should derive from these surfaces deterministically. No separate registry is required.

## Functional Set Identity

Each `functional-set.md` records:

- `functional_set: FS-NNN`
- a title;
- `design_revision: <40-character lowercase Git commit SHA>`

The `FS-NNN` identity must agree with:

- the containing Planning directory;
- the corresponding specification;
- every normative requirement identity owned by that specification.

The descriptive name suffix is organizational text, not a second identity system.

## Exact Design Binding

For every discovered Functional Set, Validation should mechanically verify that:

- `design_revision` is a well-formed 40-character lowercase Git SHA;
- the declared revision resolves to a Git commit.

Planning remains responsible for whether that revision is the correct Design state for the selected work. Validation verifies only mechanically decidable properties of the binding.

## Normative Requirement Parsing

Normative specification headings use:

```text
### FS-NNN-NR-NNN — <title>

**Classification: M|S|B**
```

A requirement is active by default. Planning marks an inactive requirement in its canonical normative specification with the separate line:

```text
**State: Inactive**
```

Removing that marker reactivates the requirement. Active/inactive state is not an evaluation classification.

The parser should operate generically over every discovered current specification.

Validation should enforce:

- valid `FS-NNN-NR-NNN` identity form;
- Functional Set prefix agreement;
- requirement identity uniqueness across current specifications;
- exactly one evaluation classification of `M`, `S`, or `B`;
- at most one requirement-state marker, whose only valid explicit value is `Inactive`.

Validation must not carry a per-Functional-Set requirement-count constant merely to recognize a valid Functional Set.

## Requirement Evaluation Manifest

`repo/validation/requirement-evaluation.json` remains the direct current mapping from mechanically applicable requirements to project-native Validation tasks.

Manifest integrity is checked against the aggregate normative requirement set from all discovered Functional Sets together with the current requirement state recorded in each canonical normative specification.

Normative specifications retain the durable requirement identity and requirement text, record evaluation classification as `M`, `S`, or `B`, and may separately mark a requirement `Inactive`.

A requirement is active when no `State` marker is present. `**State: Inactive**` means the requirement remains defined but has no current implementation, mechanical-evaluation, or semantic-evaluation obligation. Planning may reactivate the requirement by removing that marker without changing its identity or normative text.

The manifest is the direct representation of current mechanical enforcement. Every active requirement classified `M` or `B` requires a manifest binding for its mechanically decidable portion. Active requirements classified `S` and all inactive requirements have no manifest binding.

It must ensure:

- every active normative requirement classified `M` or `B` has a manifest binding;
- every inactive normative requirement has no manifest binding;
- every manifest requirement reference resolves to exactly one active normative requirement classified `M` or `B`;
- duplicate requirement bindings are rejected;
- every referenced task resolves to a registered required Validation task;
- every registered required Validation task remains justified by at least one currently active mechanically evaluated requirement represented in the manifest.

Semantic-only requirements are never represented in the manifest merely because they exist.

The manifest remains repository state and does not become a source of Design or Planning authority. Planning determines requirement state and whether obligations change; Build realizes the corresponding current mechanical bindings.

## Validation Execution

`repo/scripts/validate` remains the canonical Validation entry point.

The project-native validator may be refactored as necessary to:

- discover Functional Sets;
- parse their Planning/specification state;
- aggregate mechanically applicable requirements;
- execute required project-native Validation tasks;
- preserve failure propagation.

Build should not introduce a plugin system, universal task framework, or registry architecture merely to make the existing validator generic.

## CI

CI continues to invoke only the canonical Validation entry point for required lifecycle mechanical gating.

CI should not maintain:

- its own Functional Set list;
- its own requirement list;
- independent lifecycle predicates that bypass the canonical validator.

## Operational Documentation

README and AGENTS already describe the accepted lifecycle at a useful level.

Build should change them only if the completed implementation introduces an operational fact that users or agents must know to use the lifecycle correctly.

Documentation should not become a procedural bureaucracy or duplicate normative Planning content.

## FS-001 Continuity

FS-001 remains accepted historical Planning and current applicable normative state.

Generalizing the implementation must preserve:

- FS-001 Planning/specification discoverability;
- FS-001 normative requirement parsing;
- FS-001 mechanical requirement bindings;
- FS-001 Validation obligations;
- the exact historical state preserved in Git.

Removing FS-001-specific implementation constants is not permission to weaken FS-001.

## Regression Strategy

Build should provide focused regression coverage demonstrating at least:

- canonical Validation passes with FS-001 and FS-002 present;
- Planning/specification correspondence failures are detected;
- malformed and nonexistent Design revisions are rejected;
- Functional Set identity mismatches are rejected;
- invalid requirement identity or evaluation classification is rejected;
- duplicate requirement identities are rejected;
- invalid or duplicate requirement-state markers are rejected;
- an inactive requirement remains discoverable with its `M`, `S`, or `B` evaluation classification intact;
- inactive requirements are excluded from current mechanical enforcement and a manifest binding for one fails manifest integrity;
- reactivation by removing the inactive marker restores ordinary evaluation applicability without changing requirement identity or text;
- manifest references to unknown requirements or semantic-only requirements fail manifest integrity;
- unknown task references fail manifest integrity;
- semantic-only requirements are not forced into mechanical binding;
- omission of any active `M` or `B` requirement fails manifest integrity;
- a conforming later Functional Set can be added without adding FS-specific validator constants, paths, parsers, or requirement counts;
- canonical Validation still executes all registered required tasks and propagates failure;
- CI continues to delegate to `repo/scripts/validate`;
- `git diff --check` passes.

Temporary fixtures or equivalent direct project-native regression mechanisms are preferred over durable test-framework machinery when sufficient.

## Build Review Focus

Build Review should challenge whether the result is actually the smallest completed operational lifecycle.

In particular, review should reject:

- new registries or authority layers;
- generalized plugin architecture;
- lifecycle databases;
- duplicate sources of current Functional Set identity;
- implementation abstractions not justified by current repository behavior;
- framework work that could instead remain an ordinary local implementation detail.

## Framework Completion

If this Plan and its normative requirements are fully realized and accepted, no further lifecycle-framework Functional Set is planned by default.

The next Functional Set should normally be selected because it delivers actual repository or product behavior using the lifecycle.
