---
doc_id: DP-040
title: Validation Architecture
depends_on:
  - DP-001
  - DP-020
  - DP-030
---

# Validation Architecture

## Purpose

Validation mechanically enforces the mechanically decidable portions of normative requirements and helps bound the AI agent.

Validation determines whether observable Build state satisfies obligations that Planning identified as reliably mechanically enforceable.

## Normative Basis

Normative requirements are developed during Planning.

Validation does not invent normative intent. Every validation task that performs normative enforcement exists because of one or more normative requirements.

Supporting validation implementation such as helpers, fixtures, parsers, loaders, or shared utilities does not require independent normative ownership unless it itself performs enforcement.

## Requirement Evaluation Manifest

The Requirement Evaluation Manifest is the canonical record of how normative requirements are evaluated.

Planning establishes whether each requirement requires mechanical evaluation, semantic evaluation, or both.

During Build, each mechanically evaluated requirement is bound to the actual Validation task or tasks that enforce its mechanically decidable obligations.

Semantic evaluation defers the requirement to Semantic Review and does not require an implementation-specific binding.

A requirement may use both paths when its meaning legitimately requires both mechanical enforcement and semantic judgment.

Semantic routing does not create a separate review artifact hierarchy.

## Scope of Validation

Validation should enforce only obligations that are meaningfully and reliably mechanically decidable.

Semantic obligations must not be converted into artificial mechanical predicates merely to make them executable.

Validation should remain proportional to the behavior and risk it protects. It should not become more complicated than the project merely to prove that its own framework is internally complete.

Validation infrastructure should be introduced only when it materially improves enforcement, understandability, reuse, reliability, or necessary agent control.

## Organization

Validation should remain understandable when inspected locally.

An enforcement task should have a clear purpose, descriptive behavior, and direct relationship to the requirement it enforces.

Validation code should be organized around the behavior being protected rather than around framework metadata categories.

The canonical manifest provides requirement traceability. Supporting helpers do not need independent provenance records merely because they participate in Validation.

## Execution

Validation is run against the Build before acceptance.

A failing required validation task prevents merge to `main` until the Build, Planning, or Design defect responsible for the failure is corrected.

Passing validation is a gate condition, not a separately accepted or documented lifecycle result.

## Limits

Mechanical validation cannot determine every semantic property of a system.

Requirements routed to Semantic Review are evaluated semantically rather than being forced into mechanical Validation.

Questions of completeness, faithful interpretation, unnecessary complexity, scope meaning, and semantic alignment belong to Semantic Review.
