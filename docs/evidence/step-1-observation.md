# Evidence: Baseline Observation (Step 1)

## Dev Server
- Running on `http://localhost:5176/` (ports 5173-5175 in use)
- Vite v7.3.7

## UI Behavior at Baseline

### Components as Stubs
- **Button**: Renders a `<button>` but ignores the `variant` prop and doesn't set `type="button"` by default
- **HashConfirm**: Shows an input field and an "Aprobar" button, but the input doesn't capture any state and the button is always enabled (no hash barrier)
- **Inbox**: The state values are initialized as arrays `[{}, () => {}]` and `["", () => {}]` instead of proper `useState` calls. The `decide`, `clearSearch` functions are empty. Derived values (`pending`, `decided`, `visible`) all point directly to `plans` without filtering

### Test Results (Before Implementation)
- **61 total tests** across 6 test files
- **34 failed, 27 passed** — components are stubs as expected
- The 27 passing tests are from `App.test.jsx` and `untrusted.test.jsx` which don't depend on the component implementations

## Key Architectural Decisions Observed
- `@impl` alias resolves: `team` → `src/components`, `ai` → `src/ai`
- `PlanCard.jsx` is read-only (protected file) — it shows plans and delegates decisions to parent
- Risk classification: R1 = "crea datos", R2 = "destructivo" (requires hash confirmation)
- Decisions persist via localStorage with key `dae-s10-decisions`
- Inbox manages all state; PlanCard and HashConfirm are stateless/contained

## File Structure
```
src/
├── components/      # Team implementation (Button, HashConfirm, Inbox, PlanCard)
├── ai/              # AI-generated versions with known defects
├── test/            # Test files (never edit)
├── lib/             # storage.js, plans.js helpers
└── data/            # plans.js data (never edit)
```

## Date
2026-10-30
