# repo-spec Genesis

This repository is the portable seed of the repo-spec repository framework established through `FS0-GENESIS`.

`FS0-GENESIS` is the unique root functional set of the repository framework. It establishes the minimum complete self-hosting framework substrate required for ordinary successor framework functional sets. `FS0-CORE` is different: it is a product-root concept used for the first ordinary functional set of a product developed under an established repository framework.

## Repository framework surfaces

The framework separates responsibilities rather than treating repository files, tools, CI, or review activity as interchangeable authority:

- **Authority** — accepted repository-framework normative requirements under `repo/`.
- **Design** — maintained Design Proposals that own semantic meaning.
- **Planning** — functional-set scope, normative distillation, and exact implementation intent.
- **Build** — implementation of one accepted Plan within its authorized mutation scope.
- **Conformance** — mechanical enforcement of accepted normative authority.
- **Assurance** — bounded semantic review and evidence for governed decisions.
- **Accepted state** — the exact repository revision established through Governance acceptance.

These orientation descriptions are non-authoritative. Accepted repository authority controls if this README ever differs from governed framework state.

## Validation

Once the Genesis Conformance runtime is realized, the canonical public repository validation entry point is:

```bash
repo/scripts/validate
```

Use that entry point for canonical mechanical Conformance. CI and other wrappers may invoke it, but they do not define independent normative predicates or create acceptance by themselves.

## Successor framework work

Genesis is intentionally minimal. Later framework capabilities are added through ordinary successor functional sets using the governed Design → Planning → Build lifecycle. They are not added by silently expanding or rewriting Genesis semantics.

## License

This repository is licensed under the GNU General Public License, version 3. See `LICENSE`.
