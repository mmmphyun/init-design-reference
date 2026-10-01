# System Design Principles

## 1. Single Source of Truth
- All visual values (colors, spacing, typography, radii) MUST be derived from `reference/tokens/`.
- Do NOT inject arbitrary hex codes or ad-hoc pixel values into component source code.

## 2. Aesthetic Constraints
- Read `reference/notes/do-not-copy.md` before initiating any frontend work.
- Strict avoidance of generic AI aesthetics (overly rounded cards, ambient neon glows, unsemantic step markers).
- Focus boldness in a single signature feature per page.
