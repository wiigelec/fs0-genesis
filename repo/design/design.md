# Repository Development Lifecycle

## Purpose

This repository framework exists to turn conversational human intent into correct working software while keeping the process understandable, bounded, and simple.

The lifecycle has six major concerns:

1. Design
2. Plan
3. Build
4. Validation
5. Semantic Review
6. Acceptance

Each concern exists only to support development of the actual project. Framework structure and process should remain no more complicated than necessary to preserve understanding, alignment, correctness, and control of the AI agent.

## Design

Design is the bridge between human and machine understanding.

Design is maintained as human-readable Markdown that is also structured for efficient machine ingestion. It is organized as a hierarchical outline: high-level concepts are decomposed into logical partitions, and those partitions are progressively expanded into smaller and more detailed descriptions.

The hierarchy should follow the natural structure of the system rather than a mandatory universal document template. Only the top levels required for current understanding need to be developed; deeper decomposition is added as the design evolves.

## Plan

Plan is the technical bridge between prose Design and code implementation.

A Plan translates selected Design into a technical specification describing what is to be built. It makes the Design concrete enough for implementation by defining the relevant technical structure, interfaces, behavior, constraints, affected implementation areas, and validation expectations.

Planning should specify consequential technical decisions while leaving ordinary code-level implementation decisions to Build.

## Build

Build is the physical manifestation of Design and Plan.

Build transforms the technical specification into actual repository state: source code, configuration, tests, generated artifacts, and other implementation material required by the Plan.

Build owns implementation correctness and ordinary code-level decisions. It does not own changes to intended Design meaning or unresolved consequential technical decisions belonging to Planning.

## Validation

Validation mechanically enforces normative requirements and helps bound the AI agent.

Every validation task that performs normative enforcement must be traceable to the requirement it enforces, and a reader of a normative requirement must be able to determine how that requirement is enforced.

A simple manifest should provide the canonical mapping:

    normative requirement <-> validation task(s)

Validation should remain understandable and proportional to the project. Supporting test infrastructure does not require independent normative traceability unless it itself performs enforcement.

Validation is a gate to acceptance, not a separately documented lifecycle result.

## Semantic Review

Semantic Review checks alignment after each major lifecycle stage and is normally iterative.

### Design Review

Design Review checks the Design for semantic completeness, internal consistency, unresolved consequential decisions, unnecessary complexity, and faithful representation of human intent.

### Plan Review

Plan Review evaluates the Plan against Design to ensure the technical specification completely and faithfully realizes the applicable Design requirements without inventing or omitting consequential semantics.

### Build Review

Build Review evaluates the Build against both Plan and Design to ensure the implementation faithfully realizes the technical specification and underlying intended meaning.

A review may require several correction and re-review passes before convergence. Review findings are working-process information and do not require durable governance records.

## Acceptance

Development work occurs on a development branch.

The development branch contains candidate work. `main` contains accepted repository state.

Validation and the applicable Semantic Reviews must be satisfactory before integration. If they are not satisfactory, the candidate remains on the development branch and is corrected there.

For this single-developer repository, merging the development branch into `main` is acceptance. No parallel acceptance record, receipt, provider reconstruction, or separate acceptance history is required.
