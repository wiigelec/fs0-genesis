---
doc_id: DP-001
title: Repository Development Lifecycle
depends_on: []
---

# Repository Development Lifecycle

## Purpose

This repository framework exists to turn conversational human intent into correct working software while keeping the process understandable, bounded, and simple.

The lifecycle has six major concerns:

1. Design
2. Planning
3. Build
4. Validation
5. Semantic Review
6. Acceptance

Each concern exists only to support development of the actual project.

Every lifecycle artifact, process, and mechanism should be kept as simple as practicable while still preserving the user's intent, required behavior, correctness, necessary constraints, and necessary control of the AI agent.

A downstream artifact or process may realize, validate, or review upstream intent, but it does not create new persistent intent merely by existing. Implementation behavior, validation behavior, review findings, generated artifacts, and historical repository behavior do not independently become Design or normative requirements.

## Design

Design is the bridge between human and machine understanding.

Design captures intended system meaning as human-readable Markdown organized for reliable machine ingestion. It is developed as a hierarchical outline whose concepts are decomposed naturally as more detail is required.

Design owns system meaning.

See DP-010.

## Planning

Planning is the technical bridge between Design and Build.

Planning consumes Design and existing repository state, selects a bounded Functional Set, and develops the technical specification, normative requirements, and requirement evaluation mapping needed to implement that work.

Planning owns Functional Set scope, technical specification, and normative distillation while leaving ordinary code-level implementation decisions to Build.

See DP-020.

## Build

Build is the physical manifestation of Design and Planning.

Build transforms the reviewed Planning result into actual repository state while preserving intended meaning, technical constraints, normative obligations, and Functional Set scope.

Build owns implementation correctness and ordinary code-level decisions.

See DP-030.

## Validation

Validation mechanically enforces mechanically decidable normative requirements and helps bound the AI agent.

Mechanical enforcement must be directly traceable to the normative requirement it enforces. Validation does not invent normative intent.

Validation is a gate to acceptance, not a separately documented lifecycle result.

See DP-040.

## Semantic Review

Semantic Review evaluates alignment and semantic sufficiency after each major lifecycle stage and is normally iterative.

Design Review evaluates Design for semantic completeness.

Plan Review evaluates the complete Planning result against Design.

Build Review evaluates Build against both Planning and Design.

Semantic Review also challenges unnecessary complexity and asks whether a materially simpler solution could preserve the same intent, required behavior, correctness, necessary constraints, and necessary agent control.

Review findings are working-process information and do not require durable governance records.

See DP-050.

## Acceptance

Development work occurs on a development branch.

The development branch contains candidate work. `main` contains accepted repository state.

Applicable Validation and Semantic Review must be satisfactory before integration. If they are not satisfactory, the candidate remains on the development branch and is corrected there.

For this single-developer repository, intentionally merging the development branch into `main` is acceptance. No parallel acceptance record, receipt, provider reconstruction, or separate acceptance history is required.

See DP-060.
