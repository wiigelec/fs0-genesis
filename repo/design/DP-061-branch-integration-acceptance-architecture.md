---
doc_id: DP-061
title: Branch Integration Acceptance Architecture
depends_on:
  - DP-060
  - DP-042
  - DP-052
---

# Branch Integration Acceptance Architecture

## Purpose

Branch integration acceptance defines the conditions under which candidate work becomes accepted repository state.

For this repository, acceptance is the intentional integration of the development branch into `main`.

## Candidate and Accepted State

The development branch contains candidate repository state.

`main` contains accepted repository state.

Work may change repeatedly on the development branch without becoming accepted.

Acceptance occurs only when the candidate state is intentionally integrated into `main`.

## Preconditions

Before integration, all lifecycle work required for the candidate must be satisfactory.

This includes:

- required mechanical Validation passing; and
- required Semantic Review converging.

If either condition is not satisfied, the candidate remains on the development branch.

A passing individual check, review pass, commit, push, or other repository event does not independently create acceptance.

## Acceptance Action

Intentional integration of the development branch into `main` is the acceptance action.

The accepted state is the repository state represented by that integration.

No separate acceptance token, receipt, database entry, provider comment, issue transition, or reconstructed acceptance event is required.

## History

Git history is sufficient to show accepted repository progression because it records changes integrated into `main`.

The framework does not maintain a parallel acceptance history.

The current `main` state is the current accepted state.

## Boundaries

Acceptance does not decide whether Design, Planning, Build, Validation, or Semantic Review are correct.

Those lifecycle activities determine whether the candidate is ready.

Acceptance only changes the repository state from candidate to accepted through integration.

## Single-Developer Scope

This architecture assumes the current single-developer workflow.

It does not require a separate actor-authorization or approval subsystem.

If the repository later becomes multi-developer or requires independent approval authority, that new need should be designed explicitly rather than anticipated through unused machinery now.

## Simplicity

Acceptance should remain a direct state transition:

    satisfactory candidate on development branch
        ↓
    intentional integration into `main`
        ↓
    accepted repository state

Additional acceptance machinery is justified only if Git integration later proves insufficient for a concrete repository need.
