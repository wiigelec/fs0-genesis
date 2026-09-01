---
doc_id: DP-060
title: Acceptance Architecture
depends_on:
  - DP-001
  - DP-020
  - DP-030
  - DP-040
  - DP-050
---

# Acceptance Architecture

## Purpose

Acceptance is the transition from candidate repository state to accepted repository state.

For this repository, acceptance is represented directly by Git integration rather than by a parallel governance record system.

## Repository State

Development occurs on a development branch.

The development branch contains candidate work.

`main` contains accepted repository state.

## Gate Conditions

A candidate remains on the development branch while required work is incomplete.

Applicable Validation and Semantic Review must be satisfactory before the candidate is merged.

If Validation or Semantic Review identifies a defect, the owning stage is corrected and the candidate remains unaccepted.

Passing a review or validation task does not independently create acceptance.

## Acceptance Action

For this single-developer repository, intentionally merging the development branch into `main` is acceptance.

The merge accepts the repository state represented by the integrated candidate.

No separate acceptance receipt, acceptance event database, provider comment, issue state, or acceptance reconstruction mechanism is required.

## History

Git history provides the historical record of accepted repository progression.

The framework does not maintain a parallel acceptance history when Git already records integration into `main`.

The current `main` state is the current accepted state.

## Further Design

Acceptance is decomposed into the following child Design document:

- DP-061 — Branch Integration Acceptance Architecture

This document refines the candidate-to-accepted branch-state transition and its prerequisites without introducing a parallel acceptance record system.

## Boundaries

Repository activity other than intentional integration into `main` does not need to be modeled as a separate acceptance concept.

Acceptance does not replace Design Review, Planning Review, Build Review, or Validation. Those activities determine whether a candidate is ready to be merged; the merge itself is the acceptance action.
