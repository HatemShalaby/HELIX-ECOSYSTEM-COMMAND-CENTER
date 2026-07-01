# Helix Mini — Project Charter

## Purpose
Build a clean generic staffing engine that calculates required staffing, monitors risk, and explains operational decisions.

## First Version Scope
- Input demand forecast
- Input average handling/service time
- Input shrinkage
- Calculate required staffing
- Show coverage risk
- Produce simple dashboard output
- Keep architecture clean and explainable

## Not In Scope Yet
- Full Helix ecosystem
- Multi-tenant SaaS
- Complex ML
- Enterprise auth
- Advanced integrations
- MCP automation

## Target Users
- Contact centers
- Restaurants
- Any business with demand-based staffing needs

## Core Principle
Same math, different business wrapper.

## Success Criteria
- A non-technical person can understand the staffing result.
- A technical reviewer can understand the architecture.
- The system is testable.
- The system is small enough to rebuild cleanly.