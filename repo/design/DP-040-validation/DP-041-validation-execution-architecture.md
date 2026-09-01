---
doc_id: DP-041
title: Validation Execution Architecture
depends_on:
  - DP-040
  - DP-032
---

# Validation Execution Architecture

## Purpose

Validation execution runs the mechanical enforcement tasks constructed during Build against candidate repository state.

It determines whether mechanically decidable normative obligations pass or fail without inventing new normative intent.

## Inputs

Validation execution consumes:

- candidate Build state;
- mechanical enforcement tasks; and
- the durable Requirement Evaluation Manifest containing the direct mechanical requirement-to-task bindings produced during Build.

The mechanical enforcement tasks are the executable implementation of obligations Planning classified for mechanical evaluation.

## Execution

Validation runs each required mechanical enforcement task applicable to the candidate.

A task should report a mechanically meaningful pass or fail result for the obligation it enforces.

Validation may use ordinary test runners, scripts, linters, build commands, repository checks, or other executable mechanisms appropriate to the project.

The framework does not require a universal validation runner when existing project-native tooling can execute the required checks reliably.

## Failure Routing

A failing validation task means the candidate does not currently satisfy at least one mechanically enforced obligation.

The failure is corrected in the stage that owns the defect:

- semantic meaning defect → Design;
- technical specification or normative distillation defect → Planning; or
- implementation or enforcement-task defect → Build.

Validation does not silently modify Design, Planning, Build, or normative requirements in response to a failure.

## Result Meaning

A passing mechanical task establishes only that the task's mechanically decidable condition passed for the candidate state that was checked.

Mechanical success does not prove semantic completeness, faithful interpretation, or acceptance.

Semantic questions remain with Semantic Review, and acceptance remains governed by DP-060.

## Simplicity

Validation execution should use the simplest reliable mechanism available.

Existing project-native commands and test infrastructure should be reused when practical rather than wrapped in framework-specific machinery without a concrete need.
