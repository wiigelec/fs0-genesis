---
doc_id: DP-010
title: Design Architecture
depends_on:
  - DP-001
---

# Design Architecture

## Purpose

Design is the bridge between conversational human intent and machine-actionable technical understanding.

Design exists to capture the meaning of the system in a durable form that humans can read naturally and AI agents can ingest reliably. It describes what the system is intended to be without forcing that meaning into implementation-specific or normative requirement formats.

## Canonical Form

Markdown is the canonical Design format.

Design documents should remain directly readable and editable by humans without specialized authoring tools. Their structure should also make them easy for machines to locate, partition, and ingest.

Each Design document has a stable `DP-NNN` document identity. Document identity exists to support durable reference to the Design corpus without requiring identities on every statement.

Generated metadata or indexes may assist navigation or validation, but they do not replace the Markdown Design documents as the semantic source.

## Hierarchical Decomposition

Design is organized as a hierarchical outline.

A high-level concept is decomposed into logical partitions. Each partition may then be decomposed into smaller and more detailed concepts. This continues until a partition is sufficiently narrow and detailed for its purpose.

Decomposition follows the natural semantic structure of the system rather than a mandatory universal document template.

A parent describes a concept at one level of abstraction. Its children explain the logical parts needed to understand that concept in greater detail.

Design should be decomposed because of semantic complexity, not merely because a document reaches an arbitrary size or token count.

Cross-references may connect concepts that are related but do not have a natural parent-child relationship.

## Design Content

Design describes system meaning.

Depending on the subject, Design may describe behavior, architecture, components, interfaces, data, constraints, invariants, tradeoffs, risks, or other concepts needed to understand the intended system.

These are available forms of description rather than mandatory headings.

Design should remain prose-oriented and understandable to a human reader. Normative requirement language and requirement identities are developed during Planning rather than embedded into Design.

## Design Corpus

The Design corpus is the maintained collection of Design documents that describe the system.

The corpus may be incomplete while still containing Design that is sufficiently developed for useful Planning. New Design documents may be added and existing documents may evolve as understanding grows.

Planning is not required to decompose or implement the entire Design corpus in one pass.

A Design document may depend semantically on other Design documents when those documents are required to interpret its meaning.

Document dependencies describe semantic interpretation, not lifecycle execution order.

## Further Design

Design is decomposed into the following child Design documents:

- DP-011 — Semantic Decomposition Architecture
- DP-012 — Design Corpus Architecture

These documents separate how meaning is hierarchically decomposed from how the resulting Markdown corpus is identified, related, and maintained.

## Planning Boundary

Design does not originate from a Functional Set.

Planning consumes the available Design corpus and distills a bounded portion of that Design into a Functional Set for implementation.

Planning owns the development of normative requirements and technical implementation intent for the selected work.

Design does not ordinarily define exact file mutation scope, exhaustive implementation sequencing, or code-level pseudocode unless a concrete implementation detail is itself part of the intended system meaning.

If Planning discovers that a consequential semantic decision is missing or ambiguous, the work returns to Design.

## Design Review

Design Review evaluates Design for semantic completeness before that Design is relied upon by Planning.

Review looks for missing meaning, ambiguity, contradiction, unresolved consequential decisions, unnecessary complexity, and failure to faithfully represent human intent.

Design Review should also ask whether the Design contains machinery that can be removed or simplified without losing intended meaning, required behavior, correctness, necessary constraints, or necessary agent control.

Design Review is iterative. Findings are corrected in Design and reviewed again until the relevant Design is sufficiently complete and coherent for Planning.

Design Review is a working process and does not require a separate durable review record.
