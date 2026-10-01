# Component Architecture Guidelines

## 1. Component Primitives
- **Button**:
  - Variants: `primary`, `secondary`, `ghost`, `destructive`.
  - States: `default`, `hover`, `active`, `disabled`, `loading`.
  - Naming: Active voice verbs ("Save changes", "Delete record").
- **Input / Form**:
  - Explicit `<label>` binding.
  - Distinct border state on `:focus-visible`.
  - Unambiguous error message placement directly below the control.
- **Card**:
  - Border-defined surface hierarchy.
  - Prohibit arbitrary soft drop-shadows on container cards.

## 2. State Completeness
- Every dynamic UI component must implement 4 explicit states:
  1. `Loading` (skeleton or spinner with aria-busy)
  2. `Empty` (actionable guidance)
  3. `Error` (actionable recovery instructions)
  4. `Populated` (default data-rich presentation)
