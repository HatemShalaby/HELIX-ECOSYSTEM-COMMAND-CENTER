# Engine Performance Memory Index

## Purpose

Tracks forecast performance, staffing recommendations, actual outcomes, deviations, confidence, and improvement recommendations.

This memory category supports the future demand-to-capacity intelligence engine.

## What Belongs Here

- predictions
- actual outcomes
- forecast errors
- staffing recommendation results
- confidence levels
- deviation patterns
- model/rule improvement suggestions
- human override reasons related to engine outputs

## What Does Not Belong Here

- general learning notes
- generic business rules without performance evidence
- AI prompt failures
- product architecture decisions
- raw operational dumps without interpretation

## Record Format

Each record should include:

- Date
- Business context
- Prediction
- Actual result
- Deviation
- Confidence level
- Cause hypothesis
- Recommendation
- Human approval status

## Suggested File Naming

```text
YYYY-MM-DD-context-deviation.md
```

Example:

```text
2026-06-22-restaurant-evening-demand-deviation.md
```

## Records

-
