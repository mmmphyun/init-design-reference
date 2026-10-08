# Component Architecture Guidelines
<!-- Derived from wshobson/agents (MIT License) & pbakaus/impeccable (Apache 2.0) -->

## 1. Asynchronous Data 4-State Completeness Contract
For asynchronous data-fetching components, network collection views, or views subject to remote state changes, provide explicit UI representations for all 4 lifecycle states. Purely static, presenter, or layout components are exempt.

```
       ┌───────────────┐
       │ 1. Loading    │ ──(data fetched)──► ┌──────────────────┐
       │ aria-busy     │                     │ 2. Populated     │
       └───────┬───────┘                     │ Default view     │
               │                             └─────────┬────────┘
       (empty) │ (failed)                              │ (deleted/cleared)
               ▼                                       ▼
       ┌───────────────┐                     ┌──────────────────┐
       │ 4. Error      │                     │ 3. Empty         │
       │ role="alert"  │                     │ Actionable CTA   │
       └───────────────┘                     └──────────────────┘
```

1. **Loading State**:
   - Semantic skeleton with `aria-busy="true"` and `aria-live="polite"`.
   - Dimension-matched skeletons preventing Layout Shift (CLS score = 0).
2. **Populated State**:
   - Default view utilizing semantic tokens (`bg-surface`, `text-foreground`).
3. **Empty State**:
   - Actionable zero-data layout with informative title, description, and primary CTA. No dead-ends.
4. **Error State**:
   - Accessible error container with `role="alert"`, descriptive cause, and non-blocking retry button.

---

## 2. Interactive Micro-State Specification (Hobson / Kowalski)

For pressable, navigable, or input components:

| Micro-State | Visual Requirement | ARIA / Accessibility | CSS / Tailwind Pattern |
| :--- | :--- | :--- | :--- |
| **Idle** | Token-defined surface & border | `aria-disabled="false"` | `bg-surface border-border text-foreground` |
| **Hover** | 5% surface brightness or tint, no layout shift | N/A | `hover:brightness-105 transition-all` |
| **Focus-Visible** | High-contrast 2px ring with 2px offset | Native focus tracking | `focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2` |
| **Active / Press** | Physical compression `scale(0.98)`, 100ms spring | N/A | `active:scale-[0.98] duration-press will-change-transform` |
| **Disabled** | 50% opacity, no pointer events | `aria-disabled="true" disabled` | `disabled:opacity-50 disabled:pointer-events-none` |

---

## 3. Unstyled Radix Composition (shadcn/ui Paradigm)
- Separate structural accessibility logic from visual styling tokens.
- Favor compositional primitives (`Slot`, `asChild`) over monolithic nested components.
- Zero hardcoded arbitrary Tailwind classes (`p-[13px]`, `bg-[#1e293b]`). All styles bind directly to `reference/tokens/*.json`.
