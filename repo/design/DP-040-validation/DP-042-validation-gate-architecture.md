---
doc_id: DP-042
title: Validation Gate Architecture
depends_on:
  - DP-040
  - DP-041
  - DP-060
---

# Validation Gate Architecture

## Purpose

The Validation gate prevents candidate work with failing required mechanical enforcement from being accepted.

It is a decision boundary, not a separate governance record system.

## Gate Condition

All required mechanical validation applicable to the candidate must pass before the candidate is eligible for acceptance.

If any required mechanical validation fails, the candidate remains on the development branch until the owning defect is corrected and the relevant validation passes.

Validation pass is necessary where mechanical obligations exist, but it is not sufficient by itself for acceptance.

Required Semantic Review must also be satisfactory.

## Result Lifetime

Validation results are working-process information.

The framework does not require a durable validation-pass artifact, evidence manifest, validation receipt, or separately accepted validation state.

Ordinary test output, command output, or CI output may be retained by repository tooling when useful, but that retention is not itself part of the lifecycle model.

## Relationship to Acceptance

Validation does not perform acceptance.

Validation determines whether the mechanical portion of the candidate is eligible to proceed toward acceptance.

Intentional integration into `main` remains the acceptance action.

## Scope

The gate applies only to required mechanical validation.

Optional diagnostic, exploratory, performance, development, or informational checks may exist without becoming acceptance gates unless Planning establishes a normative obligation that makes them required.

## Simplicity

The Validation gate should remain a direct rule:

    required mechanical validation passes
        ↓
    candidate may continue toward acceptance

No additional acceptance token, proof object, or validation-state database is required.
