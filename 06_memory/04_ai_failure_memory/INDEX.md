# AI Failure Memory Index

## Purpose

Tracks AI/model/workstation failures so the same chaos is not repeated.

This memory category protects the Command Center from repeated prompt, model, tool, and governance failures.

## What Belongs Here

- wrong model used for a role
- model ignored instructions
- model exposed reasoning or `<think>` blocks
- hallucinated file creation
- wrong file format
- wrong folder/path
- Continue rule failure
- OpenClaw misuse risk
- LM Studio/Ollama behavior failure
- prompt that produced bad output

## What Does Not Belong Here

- normal learning confusion
- business demand patterns
- engine forecast deviations
- approved architecture decisions
- unverified complaints without evidence

## Record Format

Each record should include:

- Date
- Model or tool used
- Task attempted
- Failure type
- What went wrong
- Rule violated
- Correction needed
- Prevention rule
- Status

## Suggested File Naming

```text
YYYY-MM-DD-tool-or-model-failure-name.md
```

Example:

```text
2026-06-22-continue-teaching-router-failure.md
```

## Records

-
