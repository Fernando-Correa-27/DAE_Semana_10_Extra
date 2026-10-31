# Evidence Index — La bandeja de aprobaciones

This index lists all evidence artifacts for the "La bandeja de aprobaciones" lab.

## Files

| File | Steps | Description |
|------|-------|-------------|
| [`step-1-observation.md`](./step-1-observation.md) | 1 | Baseline: dev server observation, UI behavior, findings |
| [`ai-defect-analysis.md`](./ai-defect-analysis.md) | 10–12 | AI-generated defects analysis across 4 files |
| [`summary-report.md`](./summary-report.md) | 13–16 | Full summary of all work, fixes, and key learnings |
| [`index.md`](./index.md) | — | This file |

## Branches

| Branch | SHA | Purpose |
|--------|-----|---------|
| `main` | `744a976` | Team components (Button, HashConfirm, Inbox) + documentation |
| `experiment-fixes` | `7edc7e8` | AI defect corrections — **separate branch, not merged** |

## Test Results

| Milestone | Tests | Passed | Status |
|-----------|-------|--------|--------|
| After Step 3 (Button) | 12 | 12 | ✅ |
| After Step 5 (HashConfirm) | 24 | 24 | ✅ |
| After Step 9 (Inbox) | 61 | 61 | ✅ |
| After Step 13 (experiment fixes) | 61 | 61 | ✅ |

## Commit History (main)

```
744a976 docs: add observation and AI defect analysis documentation
9b3f1b4 feat: implement Button, HashConfirm, and Inbox components
587ad06 Initial commit
```

## Commit History (experiment-fixes)

```
7edc7e8 fix: correct 4 canonical AI defects in Button, HashConfirm, Inbox, and PlanCard
```
