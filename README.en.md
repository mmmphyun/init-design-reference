# init-design-reference

[한국어](README.md) | English

Production-grade UI design reference and token architecture scaffolder for agentic AI coding assistants (Google Antigravity, Claude Code, Cursor, Codex).

## Overview

AI coding assistants frequently produce generic, cookie-cutter interfaces (identical rounded cards, meaningless gradient fills, low-contrast text). `init-design-reference` combats this by generating a deterministic `/reference` directory inside your project root, establishing a Single Source of Truth (SSOT) for design tokens, typography fallbacks, accessibility standards, and strict anti-cliché constraints.

## Features

- **Decoupled Architecture**: All templates are pure, readable Markdown and JSON files—no obfuscated string literals inside scripts.
- **Strict Anti-Cliché Rules**: Directly incorporates the latest anti-tell principles from Anthropic's `frontend-design` specification (`notes/do-not-copy.md`).
- **Bilingual Typography Stack**: Built-in support for Korean and English mixed text rendering with robust system fallbacks (`Pretendard` + `Space Grotesk` + `JetBrains Mono`).
- **Safe & Idempotent**: Never overwrites existing user modifications unless `--force` is explicitly provided.
- **Git Bloat Protection**: Automatically configures `.gitignore` to prevent committing raw screenshot binaries and webfont files.
- **Framework Aware**: Inspects `package.json` to detect style engines (Tailwind v3, Tailwind v4, CSS Modules) and suggests zero-drift integration strategies.

## Directory Layout

```
reference/
  screenshots/          # UI target captures (.gitignore applied)
  notes/
    do-not-copy.md      # AI cliché bans (SaaS card kits, ALL-CAPS eyebrows, etc.)
    layout.md           # Breakpoints & spacing rhythm
    interaction.md      # Transitions & modal focus traps
    visual-direction.md # Surface hierarchy & signature element rules
    accessibility.md    # WCAG 2.1 AA mandates
  tokens/
    colors.json         # Hex values for surface, text, accents
    spacing.json        # Rem-based rhythm
    typography.json     # Role-based font metrics
    radii.json          # Border radius tokens
    shadows.json        # Surface depth tokens
    motion.json         # Durations and easing curves
  fonts/
    README.md           # Web font guidelines
    font-license.md     # Font licensing terms
    preview.html        # Interactive multilingual rendering test
  DESIGN.md             # Core design system constitution
  COMPONENTS.md         # Component states (loading, empty, error, populated)
  REVIEW_CHECKLIST.md   # Pre-commit UI verification checklist
```

## Installation

### One-Liner Install (No Clone Required)

#### Windows (PowerShell)
```powershell
# Default: Google Antigravity ($env:USERPROFILE/.gemini/config/skills/init-design-reference)
irm https://raw.githubusercontent.com/mmmphyun/init-design-reference/main/install.ps1 | iex

# Local repository execution
.\install.ps1 -Agent antigravity
.\install.ps1 -Agent claude
.\install.ps1 -Agent cursor
.\install.ps1 -TargetDir "C:/path/to/custom/skills/init-design-reference" -Force
```

#### macOS / Linux (Bash)
```bash
# Default: Google Antigravity (~/.gemini/config/skills/init-design-reference)
curl -fsSL https://raw.githubusercontent.com/mmmphyun/init-design-reference/main/install.sh | bash

# Install for Claude Code or Cursor
curl -fsSL https://raw.githubusercontent.com/mmmphyun/init-design-reference/main/install.sh | bash -s -- --agent claude
curl -fsSL https://raw.githubusercontent.com/mmmphyun/init-design-reference/main/install.sh | bash -s -- --agent cursor

# Local execution
chmod +x ./install.sh
./install.sh --agent antigravity
```

### Agent Paths Reference

| Agent | OS | Installation Path |
| :--- | :--- | :--- |
| **Google Antigravity** | Windows | `$env:USERPROFILE/.gemini/config/skills/init-design-reference` |
| **Google Antigravity** | Linux/macOS | `~/.gemini/config/skills/init-design-reference` |
| **Claude Code** | Windows | `$env:USERPROFILE/.claude/skills/init-design-reference` |
| **Claude Code** | Linux/macOS | `~/.claude/skills/init-design-reference` |
| **Cursor** | All | `~/.cursor/skills/init-design-reference` (or workspace local) |

### Direct CLI Usage
```powershell
python "scripts/adapter.py" "reference"

# Overwrite existing files
python "scripts/adapter.py" "reference" --force
```

## Recommended Workflow

1. **Scaffold**: Run `init-design-reference` to build the `/reference` structure.
2. **Refine**: Invoke your assistant with the `frontend-design` skill to establish domain-specific color palettes and typography roles in `tokens/`.
3. **Build**: Write frontend components, strictly adhering to `/reference` as the SSOT.
4. **Audit**: Verify compliance against `reference/REVIEW_CHECKLIST.md` prior to committing.

## Contributing

For guidelines on reporting bugs, proposing new AI anti-patterns, or adding framework detections, see [CONTRIBUTING.md](CONTRIBUTING.en.md).

## License

[MIT License](LICENSE).
