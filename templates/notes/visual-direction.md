# Visual Direction & Aesthetic Framework
<!-- Derived from jakubkrehel/skills (MIT License) & frontend-design -->

Synthesizes Jakub Krehel's design brief extraction protocol with deterministic token execution and curated palette libraries.

---

## 1. Gate 0: Smart Alignment Intake (2-Turn Progressive Interview)

Before touching layout or code, the agent MUST run this non-expert-friendly 2-turn alignment interview to establish design anchors without cognitive overload:

### Turn 1: 3 Casual Anchor Questions
Ask the user these 3 intuitive, non-jargon questions:
1. **Target User**: [A] Internal team / power operators (speed & scanning priority) vs [B] General public / consumers (clean & welcoming)
2. **Atmosphere / Persona**:
   - [A] **Toss / Apple style**: Spacious, clean, tactile spring micro-interactions (`apple-fluid`)
   - [B] **AWS / Bloomberg cockpit**: High-density telemetry, dark carbon surfaces, tabular data (`b2b-dense`)
   - [C] **Notion / Editorial minimal**: Monotone calm, airy typography, reading rhythm (`editorial-minimal`)
   - [D] **Terminal / Developer HUD**: Low-reflection dark surfaces, mono fonts, dense status signals (`technical-mono`)
3. **Brand / Accent Color**: Desired logo/accent hex or general hue (or default to recommended palette).

### Turn 2: Persona-to-Preset Deterministic Translation Table
The agent deterministically translates the user's choice into baseline dials and fonts:

| Selected Persona | Preset | Variance | Density | Motion | Font Pair |
|---|---|---|---|---|---|
| **[A] Toss / Apple** | `apple-fluid` | 6 | 5 | 9 | Display: Pretendard / Body: Pretendard |
| **[B] AWS / Bloomberg Cockpit** | `b2b-dense` | 3 | 9 | 2 | Display: Space Grotesk / Body: Pretendard (tabular-nums) |
| **[C] Notion / Editorial** | `editorial-minimal` | 8 | 3 | 5 | Display: Space Grotesk / Body: Pretendard |
| **[D] Terminal / Dev HUD** | `technical-mono` | 4 | 8 | 1 | Display: JetBrains Mono / Body: JetBrains Mono |

- **Anchor & Tune Rule**: The preset sets the baseline anchor. If the user asks for minor tweaks ("Apple vibe but slightly more dense data"), tune dials relatively (`Density +2`) without abandoning the persona.
- **Approval Gate**: Present the concrete proposal (Preset, Palette, Fonts, Density). **Wait for explicit user confirmation ("진행해", "확정") before initiating Gate 1~4 autonomous execution.**

---

## 2. Curated Aesthetic Palettes (Aesthetic Taste Over Pure Formulas)

Mathematical color spaces (like OKLCH) guarantee contrast ratios, but cannot compute aesthetic discernment or domain taste. When no external design reference or Figma token set exists, adopt one of these curated domain palettes:

### A. Fintech / High-Trust Dashboard
- **Surface**: `#0A0F1D` (Deep Abyssal Blue) / `#111827` (Card Elevated)
- **Foreground**: `#F9FAFB` (High-contrast Primary Text) / `#9CA3AF` (Secondary Muted)
- **Accent**: `#00D084` (Crisp Signal Green) / `#3B82F6` (Operational Blue)
- **Border**: `#1F2937` (Subtle 1px Structure)

### B. Healthcare / Clinical Portal
- **Surface**: `#F8FAFC` (Sterile Slate 50) / `#FFFFFF` (Elevated White)
- **Foreground**: `#0F172A` (Obsidian Ink) / `#64748B` (Neutral Cool Grey)
- **Accent**: `#0284C7` (Clinical Sky Blue) / `#EF4444` (Critical Alert)
- **Border**: `#E2E8F0` (Crisp Architectural Rule)

### C. Developer Tools / Telemetry HUD
- **Surface**: `#121316` (Low-reflection Carbon) / `#1A1B20` (Surface Plate)
- **Foreground**: `#EDEDED` (Terminal Off-white) / `#888888` (Muted Syntax)
- **Accent**: `#FF6B00` (Amber Telemetry Signal) / `#22C55E` (Daemon Healthy)
- **Border**: `#27282D` (Hairline Border)

### D. Creative Editorial / Showcase
- **Surface**: `#F7F5F0` (Warm Unbleached Paper) / `#FFFFFF` (Surface Island)
- **Foreground**: `#1A1A1A` (Editorial Black) / `#5A5A5A` (Bookwork Grey)
- **Accent**: `#C93B2B` (Vermilion Red Seal) / `#1D2A44` (Deep Indigo Navy)
- **Border**: `#E5E0D8` (Warm Deckle Edge)

---

## 3. External MCP & Tool Integration Guidelines

When external Color or Palette MCPs (e.g., Coolors MCP, Color Hunt MCP) are available in the agent harness:
1. Extract the primary 4-6 hex codes.
2. Verify contrast against WCAG 2.1 AA (4.5:1 for body text) using `reference/REVIEW_CHECKLIST.md`.
3. Directly populate `reference/tokens/colors.json` under `surface`, `foreground`, `primary`, and `muted`.
