# Glossary

The glossary defines shared language for AI agents and human reviewers. Terms
here must be used consistently across standards, Project Brain entries, ADRs,
and review comments.

## 2026-06-27 - Initial AI-OS Terms

- Context: Phase 1 established the operating vocabulary for the AI Engineering
  Operating System.
- Decision: These terms are authoritative until revised.
- Rationale: Consistent language prevents agents from treating governance,
  implementation, and review concepts as interchangeable.
- Impact: Future standards must reuse these meanings or explicitly introduce a
  narrower term.
- Owner: Technical Writer.
- Review trigger: Revisit when Phase 2 expands anti-patterns and smells.

## Terms

### AI Engineering Operating System

The documentation, governance, role model, loops, standards, prompts, and
persistent knowledge that direct AI-assisted software modernization.

### Agent

An AI actor performing a defined role such as Product Manager, Software
Architect, Backend Engineer, Security Engineer, QA Engineer, Reviewer, or
Release Manager.

### Goal Engineering

The discipline of converting intent into measurable, constrained, reviewable
work with acceptance criteria, exit criteria, risks, and success metrics.

### Engineering Loop

A repeatable workflow with entry criteria, activities, outputs, exit criteria,
and checklist.

### Project Brain

The persistent knowledge base that stores durable rules, decisions, risks,
dependencies, lessons, debt, patterns, anti-patterns, and roadmap context.

### Architecture Constitution

The mandatory architecture rule set that governs system boundaries, dependency
direction, side effects, persistence, API contracts, security, testing, and
exceptions.

### Phase

A bounded unit of AI-OS work that produces complete reviewable deliverables,
updates state files, commits, pushes, and stops for review.

### Quality Gate

A role-owned check that must pass before work can move to the next loop or
phase.
