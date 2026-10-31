# AI Defect Analysis Report (Steps 10-12)

## Overview
This report documents the defects found in the AI-generated versions of the components compared to the correct team implementation.

---

## Defect 1: Inbox — Direct State Mutation (Critical)

**File:** `src/ai/Inbox.jsx` — `decide()` function  
**Severity:** Critical — React won't detect the change, UI won't update

```javascript
// AI version (defective):
const decide = (id, verdict) => {
  decisions[id] = verdict;       // ❌ Mutates the existing state object directly
  setDecisions(decisions);       // ❌ Sets the same object reference
  writeStoredDecisions(decisions);
};

// Team version (correct):
function decide(id, verdict) {
  setDecisions((current) => ({ ...current, [id]: verdict }));
}
```

**Problem:** The AI modifies the state object in place and then calls `setDecisions` with the same reference. React relies on reference equality to detect changes — since the object reference doesn't change, React skips the re-render.

**Fix:** Use the functional updater form of `setDecisions` to create a new object with the spread operator: `setDecisions((current) => ({ ...current, [id]: verdict }))`. Also, persistence should be handled by a `useEffect`, not inside the state updater.

---

## Defect 2: Inbox — Function Called During Render (Critical)

**File:** `src/ai/Inbox.jsx` — `onClick` handler in the "Limpiar búsqueda" button  
**Severity:** Critical — Causes infinite re-render loop, crashes the component

```javascript
// AI version (defective):
<button type="button" onClick={clearSearch()}>  // ❌ clearSearch() is CALLED during render

// Team version (correct):
<button type="button" onClick={clearSearch}>     // ✅ clearSearch is PASSED as reference
```

**Problem:** `clearSearch()` with parentheses executes the function during the render phase instead of passing it as a callback. This triggers `setQuery("")`, which causes a state update, which triggers another render, which calls `clearSearch()` again — infinite loop.

**Fix:** Remove the parentheses to pass the function reference: `onClick={clearSearch}`.

---

## Defect 3: PlanCard — Duplicate State in Child Component

**File:** `src/ai/PlanCard.jsx` — `verdict` state  
**Severity:** Medium — Duplicates state that already exists in the parent (Inbox)

```javascript
// AI version (defective):
export default function PlanCard({ plan, onDecide }) {
  const [verdict, setVerdict] = useState(null);  // ❌ Redundant state
  // ...
  function handleDecision(value) {
    setVerdict(value);                            // ❌ Maintains duplicate
    onDecide(plan.id, value);
  }
  // ...
  {verdict ? (
    <p className="plan-card-verdict">Decidido: {VERDICT_LABELS[verdict]}</p>
  ) : (
    // ... buttons
  )}
}

// Team version (correct):
// PlanCard has NO state. Decisions are managed entirely by Inbox.
// PlanCard simply renders the plan card and calls onDecide().
```

**Problem:** PlanCard maintains its own `verdict` state, which duplicates the state already managed by Inbox's `decisions` object. This violates the single-source-of-truth principle. The parent (Inbox) already knows the verdict — the child shouldn't duplicate it. If the parent's state changes (e.g., after re-mounting with persisted data), the child's local state won't sync.

**Fix:** Remove `verdict` state from PlanCard. Let Inbox control all decision state and pass it as needed. The team version correctly makes PlanCard completely stateless.

---

## Defect 4: HashConfirm — Partial Hash Matching (Security/Logic)

**File:** `src/ai/HashConfirm.jsx` — `isValid` comparison  
**Severity:** High — Bypasses the hash security barrier

```javascript
// AI version (defective):
const isValid = typed.includes(hash);  // ❌ "a1b2c3" includes in "xa1b2c3"

// Team version (correct):
disabled={typed !== hash}  // ✅ Exact match only
```

**Problem:** Using `includes()` allows partial matches. For example, if the hash is `"a1b2c3d4e5f6"`, typing `"xa1b2c3d4e5f6"` (text before) or `"a1b2c3"` (prefix) would evaluate to `true` because `includes()` checks for substring presence, not exact equality.

**Fix:** Use strict equality (`===`) to require an exact character-for-character match: `typed === hash`.

---

## Defect 5: Button — className Not Properly Spread (Minor)

**File:** `src/ai/Button.jsx` — className handling via explicit prop + rest  
**Severity:** Low — Works in practice but defeats the rest pattern; tests may not catch edge cases

```javascript
// AI version (defective):
export default function Button({ variant = "primary", children, className = "", ...rest }) {
  const classes = ["btn", `btn-${variant}`, className].filter(Boolean).join(" ");
  return <button type="button" className={classes} {...rest}>

// Team version (correct):
export default function Button({ variant = "primary", children, ...rest }) {
  return <button className={`btn btn-${variant}`} type="button" {...rest}>{children}</button>;
```

**Problem:** The AI version explicitly destructures `className`, building it manually. This means if a caller passes `className` as an additional prop in `...rest`, it would be overwritten. The team version uses the spread operator cleanly: the `className` is set inline and `...rest` carries forward `onClick`, `disabled`, `aria-label`, etc. The test that passes `data-testid` and `aria-label` in rest props works correctly with both versions, but the explicit `className` approach is fragile.

**Note:** The test suite passes for the AI Button, so this is a code quality/architectural concern rather than a functional defect.

---

## Summary Table

| # | Component | Defect | Severity | Root Cause |
|---|-----------|--------|----------|------------|
| 1 | Inbox | Direct state mutation in `decide()` | Critical | Missing immutable update pattern |
| 2 | Inbox | `clearSearch()` called during render | Critical | Function invocation instead of reference |
| 3 | PlanCard | Duplicate `verdict` state in child | Medium | Violation of single source of truth |
| 4 | HashConfirm | `includes()` instead of `===` | High | Partial string matching vs exact match |
| 5 | Button | Explicit `className` prop, not rest spread | Low | Over-engineered, fragile approach |

## Total Defects: 4 (as specified in requirements)
Defects 1-4 are the canonical defects. Defect 5 (Button) is noted as a code quality observation — the tests pass but the approach is less robust.

## Date
2026-10-30
