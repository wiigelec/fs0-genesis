# fs0-genesis

This repository develops a small repository lifecycle for turning human intent into correct working software while keeping the process understandable and bounded.

## Lifecycle

Work progresses through:

1. **Design** — owns system meaning and intent.
2. **Planning** — selects a bounded Functional Set, resolves consequential technical intent, and derives normative requirements.
3. **Build** — realizes the reviewed Planning result and constructs required mechanical enforcement.
4. **Validation** — mechanically evaluates requirements that Planning classified as mechanically decidable.
5. **Semantic Review** — checks Design, Planning, and Build for fidelity, completeness, drift, and unnecessary complexity.
6. **Acceptance** — intentionally integrates a satisfactory development candidate into `main`.

The lifecycle describes responsibilities and control flow. It does not require every lifecycle stage to have a matching repository directory.

## Repository surfaces

- `repo/design/` — canonical human-readable Design corpus.
- `repo/planning/` — durable Functional Set scope and technical Planning artifacts.
- `repo/specs/` — canonical human-readable, machine-parseable normative specifications.
- `repo/validation/requirement-evaluation.json` — current mechanical requirement-to-Validation-task bindings.
- `repo/scripts/validate` — canonical mechanical Validation entry point.
- `repo_old/` — historical implementation material; it is not a source of current normative intent.
- `user/` — user-owned operational material outside the repository framework.

Planning artifacts preserve the exact Design revision they consumed. Normative specifications under `repo/specs/` are the normative source for requirement text and evaluation classification. Build, parsers, manifests, and Validation do not create new Design meaning or normative requirements merely through implementation behavior.

## Validation

Run:

```bash
repo/scripts/validate
```

Validation checks mechanically decidable obligations. Passing Validation does not establish semantic completeness or Acceptance.

CI delegates mechanical gating to this same entry point rather than defining an independent set of normative predicates.

## Accepted state

Development branches contain candidate work. `main` represents accepted repository state.

A candidate is eligible for Acceptance only after required mechanical Validation passes and required Semantic Review converges. For this single-developer repository, intentional integration of the satisfactory candidate into `main` is Acceptance; no parallel acceptance record is required.

## Historical material

`repo_old/` is retained for historical comparison and implementation evidence. Existing historical behavior is not normative merely because it exists and should not be ported unless current Design and Planning require the capability.

## License

This repository is licensed under the GNU General Public License, version 3. See `LICENSE`.
