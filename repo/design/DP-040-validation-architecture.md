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

Validation mechanically enforces normative requirements and helps bound the AI agent.

Validation provides executable evidence that the Build satisfies requirements that can be determined mechanically.

## Normative Basis

Normative requirements are developed during Planning.

Validation does not invent normative intent. Every validation task that performs normative enforcement exists because of one or more normative requirements.

Supporting validation implementation such as helpers, fixtures, parsers, loaders, or shared utilities does not require independent normative ownership unless it itself performs enforcement.

## Validation Manifest

A simple manifest provides the canonical mapping between normative requirements and their mechanical enforcement.

The core relationship is:

    normative requirement <-> validation task(s)

The manifest should allow a reader of a requirement to determine how it is enforced and a reader of an enforcement task to determine which requirement justifies its existence.

The manifest should remain a direct mapping rather than becoming a second validation ontology or provenance graph.

## Scope of Validation

Validation should enforce requirements that are meaningfully and reliably mechanically decidable.

Validation should remain proportional to the behavior and risk it protects. It should not become more complicated than the project merely to prove that its own framework is internally complete.

Validation infrastructure should be introduced only when it materially improves enforcement, understandability, reuse, or reliability.

## Organization

Validation should remain understandable when inspected locally.

An enforcement task should have a clear purpose, descriptive behavior, and obvious relationship to the requirement it enforces.

Validation code should be organized around the behavior being protected rather than around framework metadata categories.

## Execution

Validation is run against the Build before acceptance.

A failing required validation task prevents merge to `main` until the Build, Planning, or Design defect responsible for the failure is corrected.

Passing validation is a gate condition, not a separately accepted or documented lifecycle result.

## Limits

Mechanical validation cannot determine every semantic property of a system.

Questions of completeness, faithful interpretation, unnecessary complexity, scope meaning, and semantic alignment belong to Semantic Review rather than being forced into mechanical validation.
