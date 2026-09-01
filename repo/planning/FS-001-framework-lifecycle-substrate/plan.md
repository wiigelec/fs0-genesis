---
functional_set: FS-001
artifact: plan
title: Framework Lifecycle Substrate Plan
---

# FS-001 — Framework Lifecycle Substrate Plan

## Technical Objective

Realize the minimum repository structure necessary for subsequent Functional Sets to use the redesigned lifecycle directly.

The implementation shall favor ordinary Markdown, JSON, shell/Python, Git, and project-native tests rather than creating framework-specific infrastructure where these mechanisms are sufficient.

## Repository Structure

Use the following active framework structure:

    repo/
      design/
      planning/
        FS-NNN-<name>/
          functional-set.md
          plan.md
      specs/
        FS-NNN-<name>.md
      validation/
        requirement-evaluation.json
      scripts/
        validate

Lifecycle stage names do not otherwise dictate repository storage hierarchy.

`repo/planning/` stores durable Planning results because they must remain inspectable after Acceptance.

`repo/validation/requirement-evaluation.json` is repository state outside the lifecycle hierarchy. It is the durable Requirement Evaluation Manifest required by DP-031 and DP-040.

## Functional Set Identity

Functional Sets use:

    FS-NNN

with a descriptive directory suffix for human navigation:

    FS-NNN-<name>

The identifier is the stable identity. The descriptive suffix is not semantically significant.

No generalized registry of Functional Sets is required initially.

Git and the filesystem provide sufficient discovery until demonstrated otherwise.

## Planning and Specification Representation

Each Functional Set retains two Markdown Planning artifacts under `repo/planning/FS-NNN-<name>/`:

### `functional-set.md`

Contains:

- Functional Set identity;
- purpose;
- exact Design revision;
- selected Design scope;
- existing-state context where consequential;
- included scope; and
- explicit exclusions where useful.

### `plan.md`

Contains the consequential technical decisions Build must preserve.

No universal section template beyond what is needed to make the technical intent unambiguous is required.

Normative specifications live separately under:

    repo/specs/FS-NNN-<name>.md

The specification is canonical structured Markdown. It remains human-readable while using a small stable grammar that tooling can parse deterministically:

- one Functional Set specification per file;
- normative requirement headings use `### FS-NNN-NR-NNN — <title>`;
- each requirement records exactly one `Classification` value of `M`, `S`, or `B`; and
- the normative prose following that classification is the requirement text.

The Markdown specification is the normative source. Parsers, manifests, generated data, and Validation code may consume it but do not independently create or reinterpret normative meaning.

A separate database or generated normative-authority representation is not required.

## Normative Requirement Identity

Requirement identities are local to the Functional Set and use:

    FS-NNN-NR-NNN

Example:

    FS-001-NR-001

Accepted Planning artifacts retain these identities permanently in Git history.

A later Functional Set does not mutate the historical meaning of an accepted requirement.

If later work changes an obligation, that work creates a new requirement under the later Functional Set and updates currently applicable mechanical enforcement as necessary.

This preserves historical Planning without requiring a global normative-requirement database.

## Requirement Evaluation Classification

Each requirement records one classification encoded as:

- `M` — mechanical;
- `S` — semantic; or
- `B` — both mechanical and semantic.

The classification belongs to Planning.

Planning does not prescribe an executable validator unless the validator architecture itself is consequential to correct realization.

## Requirement Evaluation Manifest

Use:

    repo/validation/requirement-evaluation.json

as the durable Requirement Evaluation Manifest.

Its purpose is deliberately narrow: represent exact bindings between currently applicable mechanically evaluated normative requirements and the Validation tasks that enforce them.

Minimum conceptual form:

    {
      "version": 1,
      "bindings": [
        {
          "requirement": "FS-NNN-NR-NNN",
          "tasks": [
            "<project-native validation task>"
          ]
        }
      ]
    }

Build owns the concrete contents.

Planning owns only this representation decision.

The manifest is not:

- a source of normative requirements;
- a provenance graph;
- an acceptance record;
- an evidence database;
- a Semantic Review database; or
- a replacement for Planning artifacts.

A requirement may bind to multiple tasks and one task may enforce multiple requirements.

## Requirement Persistence

Accepted specification files under `repo/specs/` remain immutable historical normative records except where ordinary correction before Acceptance requires modification.

Current mechanical applicability is represented through the accepted Requirement Evaluation Manifest and the actual Validation tasks.

Removing a requirement-to-task binding in later accepted work does not rewrite historical specifications.

Semantic requirements remain available through their accepted Functional Set specification and are evaluated when applicable to Semantic Review.

No global current-semantic-requirements database is introduced in FS-001.

If actual use later demonstrates that such an index is necessary, it must be designed from that concrete need.

## Validation Entry Point

The canonical repository Validation entry point is:

    repo/scripts/validate

It shall execute all mechanically required Validation tasks applicable to the candidate state.

The entry point may delegate to:

- project-native test runners;
- shell scripts;
- Python checks;
- linters;
- build commands; or
- other direct mechanisms.

It shall not define independent normative intent.

A generalized validation framework is not required.

## Bootstrap Validation

FS-001 must provide enough direct mechanical validation to protect the framework structure introduced by FS-001 itself.

At minimum Build should construct checks capable of mechanically deciding:

- required FS-001 Planning artifacts exist;
- their declared Design revision is present and well formed;
- normative requirement identities within FS-001 are unique;
- every FS-001 normative requirement has a valid evaluation classification;
- the Requirement Evaluation Manifest is syntactically valid;
- every FS-001 normative requirement classified as mechanical or `both` has at least one exact manifest binding;
- every manifest requirement reference resolves to an existing normative requirement;
- every manifest task reference resolves to an executable/valid project-native Validation task; and
- the canonical Validation entry point executes the required tasks and returns failure when a required task fails.

Build determines the smallest reliable implementation of these checks.

## CI

Replace the active Conformance-oriented GitHub Actions workflow with Validation-oriented terminology.

CI shall:

1. check out the exact candidate revision;
2. invoke `repo/scripts/validate`; and
3. propagate its result.

CI is a caller of Validation.

CI does not independently define normative predicates and does not create Acceptance.

The workflow filename may become:

    .github/workflows/validation.yml

The former:

    .github/workflows/fs0-conformance.yml

should cease to be an active framework surface.

## README

Rewrite `README.md` to describe the current lifecycle:

- Design
- Planning
- Build
- Validation
- Semantic Review
- Acceptance

It should identify:

- `repo/design/` as canonical Design;
- `repo/planning/` as durable Planning;
- `repo/scripts/validate` as the canonical mechanical Validation entry point; and
- `main` as accepted repository state.

Remove claims that the current architecture is founded on Governance, Conformance, Assurance, or a normative Framework Contract.

Historical explanation may remain only if explicitly labeled historical and genuinely useful.

## AGENTS.md

Rewrite operational agent guidance to enforce the new ownership boundaries:

- missing semantic meaning → Design;
- Functional Set, Plan, requirement, or classification defect → Planning;
- implementation or mechanical-enforcement-construction defect → Build.

Agents shall:

- consume the selected Design and Planning result;
- not infer intent from `repo_old/`;
- not treat Validation as normative authority;
- not invent semantic requirements during Build;
- return consequential unresolved decisions to their owning stage; and
- prefer the simplest implementation preserving Design, Plan, requirements, scope, and required agent control.

Remove obsolete Governance / Conformance / Assurance authority terminology.

## `repo_old/`

`repo_old/` remains outside the active framework namespace during FS-001.

Build shall not port content from it unless the Plan or selected Design independently requires the capability represented by that content.

FS-001 does not require deleting `repo_old/`.

A later cleanup Functional Set may remove it when historical comparison is no longer useful.

## Sequencing

Build should proceed in this order where practical:

1. create the active Planning, specification, and Validation repository structure;
2. add the canonical Validation entry point and minimum direct checks;
3. create the Requirement Evaluation Manifest bindings;
4. update README and AGENTS guidance;
5. replace the obsolete CI workflow;
6. run complete Validation;
7. perform Build Review against FS-001 Planning, the normative specification, and the bound Design revision.

The sequence is intended to allow the final candidate to validate itself using the newly established mechanism.

## Implementation Freedom

Build may choose ordinary code organization, helper functions, parser implementation, command-line behavior, and test structure as long as it preserves:

- the selected Design;
- this Plan;
- FS-001 normative requirements;
- the Functional Set boundary; and
- the direct requirement-to-task relationship.

No mechanism from `repo_old/` is required merely because an equivalent old mechanism exists.

## Acceptance

FS-001 becomes accepted only when:

- all required mechanical Validation passes;
- Build Review converges; and
- the development branch is intentionally integrated into `main`.

No additional acceptance receipt or reconstructed governance record is required.
