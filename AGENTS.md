# Agent and Contributor Guidance

This file is operational guidance. It is not repository-framework normative authority and cannot override accepted authority under `repo/`.

## Authority

Treat accepted repository-framework authority under `repo/` as controlling over implementation behavior, generated output, historical convention, workflow status, reviewer preference, or this guidance.

Do not infer normative authority from CI success, a merge, issue closure, generated files, comments, agent output, or existing implementation behavior unless accepted Governance explicitly establishes that authority.

## Responsibility boundaries

- **Design owns semantic meaning.**
- **Planning owns functional-set scope, normative distillation, planned mutation paths, validation intent, sequencing, invariants, and implementation intent.**
- **Build owns implementation correctness within one accepted Plan.**

Route defects to the phase that owns the defective decision:

- missing or incorrect semantics → Design;
- incorrect scope, normative intent, planned files, sequencing, invariants, validation, or implementation intent → Planning;
- incorrect realization of an accepted Plan → Build.

Do not repair an upstream defect by inventing authority or intent downstream.

## Build discipline

Build must consume one accepted Plan and remain within that Plan's authorized mutation set. Do not add unplanned repository paths or broaden behavior merely because an implementation appears useful.

When the canonical Conformance runtime exists, use:

```bash
repo/scripts/validate
```

for repository mechanical Conformance. Do not replace it with a second validator or move normative predicates into CI/workflow glue.

## Genesis and successors

`FS0-GENESIS` is the unique framework root. Ordinary successor framework functional sets extend accepted Genesis-based framework state through the normal governed lifecycle. Genesis-specific bootstrap mechanisms must not become undocumented shortcuts for successor work.
