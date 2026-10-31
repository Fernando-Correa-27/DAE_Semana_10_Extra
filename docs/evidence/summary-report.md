# Summary Report — La bandeja de aprobaciones

## Objective

Complete Steps 13–16 of the "La bandeja de aprobaciones" lab: identify and fix AI-generated defects, create an experiment branch as evidence, and finalize documentation.

## Baseline

- **Baseline SHA**: `587ad064b1d162a1f72a86c2589ead76021fbfb0`
- **Total tests**: 61 (across 6 test files)
- **Tests passing after Step 9**: 61/61 ✅
- **Tests passing after experiment fixes**: 61/61 ✅

## Work Completed

### Steps 1–9: Team Component Implementation

All team components implemented on `main` branch:

| Step | Component | Tests | Status |
|------|-----------|-------|--------|
| 3    | Button    | 12    | ✅ |
| 5    | HashConfirm | 12  | ✅ |
| 6–9  | Inbox     | 22    | ✅ |
| —    | PlanCard  | 10    | ✅ (provided) |
| —    | App       | 2     | ✅ (provided) |
| —    | Untrusted | 3     | ✅ (provided) |

**Commit**: `9b3f1b4` — `feat: implement Button, HashConfirm, and Inbox components`

### Steps 10–12: AI Defect Analysis

Analyzed the AI-generated versions in `src/ai/` and identified 4 canonical defects:

| # | File | Defect | Severity |
|---|------|--------|----------|
| 1 | `Button.jsx` | Uses explicit `className` prop + manual string join instead of rest spread; prevents custom class passing | Medium |
| 2 | `HashConfirm.jsx` | Uses `includes()` instead of `===` for hash matching; allows partial matches | High |
| 3 | `Inbox.jsx` | State mutation in `decide()` — modifies `decisions` object directly and calls `writeStoredDecisions` during render | Critical |
| 3b| `Inbox.jsx` | Calls `clearSearch()` during render (`onClick={clearSearch()}`) instead of passing reference | Critical |
| 4 | `PlanCard.jsx` | Maintains duplicate `verdict` state; violates parent-owned-state pattern | Medium |

**Documentation**: `docs/evidence/ai-defect-analysis.md`

### Step 13: Experiment Branch — Fixes Applied

Created `experiment-fixes` branch with corrected AI versions:

| Fix | Change |
|-----|--------|
| Button | Removed explicit `className` prop; uses rest spread pattern (`{...rest}`) like team version |
| HashConfirm | Changed `typed.includes(hash)` → `typed === hash` for exact match |
| Inbox | Replaced state mutation with functional updater: `setDecisions((current) => ({ ...current, [id]: verdict }))`; removed inline `writeStoredDecisions` call |
| Inbox | Changed `onClick={clearSearch()}` → `onClick={clearSearch}` |
| PlanCard | Removed local `verdict` state; delegates all decisions to parent via `onDecide` |

**Commit**: `7edc7e8` — `fix: correct 4 canonical AI defects in Button, HashConfirm, Inbox, and PlanCard`
**Branch**: `experiment-fixes` (pushed, NOT merged to `main`)

## Key Learnings

1. **State mutation is the most critical AI defect**: Directly modifying state objects bypasses React's change detection and causes stale renders.
2. **Function calls during render**: AI often confuses `onClick={handler}` with `onClick={handler()}` — the former passes a reference, the latter executes during render.
3. **State ownership**: Child components should never maintain their own copy of parent-owned data (verdict state belongs to Inbox).
4. **Exact matching vs. partial matching**: For security-sensitive comparisons (hash verification), `includes()` is insufficient; exact equality (`===`) is required.

## Git Branches

| Branch | Purpose | Commit |
|--------|---------|--------|
| `main` | Team components + documentation | `744a976` |
| `experiment-fixes` | AI defect corrections (separate evidence) | `7edc7e8` |

## Evidence Location

All evidence is stored in `docs/evidence/` and committed to Git:

- `docs/evidence/step-1-observation.md` — Baseline observation
- `docs/evidence/ai-defect-analysis.md` — Defect analysis report
- `docs/evidence/summary-report.md` — This file
- `docs/evidence/index.md` — Evidence index
