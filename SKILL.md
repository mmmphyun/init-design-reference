---
name: init-design-reference
description: Scaffolds a production-grade UI design reference and token architecture (/reference) with strict anti-cliché constraints and framework awareness.
---

# Design Reference Scaffolding & Framework Adapter

Scaffolds a `/reference` directory structure within the project root to enforce deterministic design constraints, anti-cliché standards, and token-driven development.

## Collaboration with `frontend-design`

This skill works as the **structural scaffold** paired with the **`frontend-design`** skill:
1. **Scaffold First**: Run `init-design-reference` to build the deterministic file structure and inject baseline anti-cliché constraints (`notes/do-not-copy.md`).
2. **Refine with `frontend-design`**: Use `frontend-design` to engage in domain-specific visual decisions, customize tokens (`tokens/*.json`), and establish the signature aesthetic.
3. **Implement UI**: All frontend coding must strictly read from and conform to the `/reference` directory as the Single Source of Truth (SSOT).

## Execution Protocol

To initialize or scaffold design references in the active project:

1. Target directory is `<workspace_root>/reference`.
2. Run the adapter script using `python`:
   ```powershell
   # Windows (Google Antigravity)
   python "$env:USERPROFILE/.gemini/config/skills/init-design-reference/scripts/adapter.py" "reference"

   # macOS / Linux (Google Antigravity)
   python "$HOME/.gemini/config/skills/init-design-reference/scripts/adapter.py" "reference"

   # Claude Code / Other
   python "<skill_dir>/scripts/adapter.py" "reference"
   ```
   - **Default Behavior (Safe)**: Skips files that already exist to protect existing user tokens and notes.
   - **Force Overwrite**: Append `--force` or `-f` to overwrite existing files.
3. The adapter automatically inspects `package.json` to detect the framework (Next.js, Vite, etc.) and style engine (Tailwind v3/v4, CSS), outputting integration tips.
4. Git binary exclusions are automatically appended to the project root `.gitignore`.

## Structure Overview

```
reference/
  screenshots/          # UI target captures (.gitignore applied)
  notes/
    do-not-copy.md      # Strict AI cliché bans (derived from frontend-design)
    layout.md           # Breakpoints & spacing rhythm
    interaction.md      # Transition timing & modal focus rules
    visual-direction.md # Surface hierarchy & signature elements
    accessibility.md    # WCAG 2.1 AA & contrast mandates
  tokens/
    colors.json         # Hex values for surface, text, accents
    spacing.json        # Rem-based vertical & horizontal rhythm
    typography.json     # Role-based typography & bilingual fallbacks
    radii.json          # Border radius tokens
    shadows.json        # Depth tokens
    motion.json         # Durations and easing functions
  fonts/
    README.md           # Local font handling guidelines
    font-license.md     # Licensing documentation
    preview.html        # Bilingual font stack rendering test
  DESIGN.md             # Core design system constitution
  COMPONENTS.md         # Component state completeness rules
  REVIEW_CHECKLIST.md   # Pre-commit UI verification checklist
```
