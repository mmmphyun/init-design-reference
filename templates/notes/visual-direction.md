# Visual Direction & Aesthetic Framework
<!-- Derived from jakubkrehel/skills (MIT License) & frontend-design -->

Synthesizes Jakub Krehel's design brief extraction protocol with deterministic token execution and curated palette libraries.

---

## 1. Gate 0: Natural Language Brief Intake (Interview Protocol)

Before touching layout or code, the agent MUST establish these four anchor points through brief confirmation with the user:

1. **Concrete Subject & Audience**:
   - *Example*: "A clinical laboratory portal for senior pathologists" vs "A playful mobile gamification tool for students aged 10-14".
   - The vernacular, materials, and vocabulary of the subject dictate the visual tone.
2. **The Interface's Primary Job**:
   - High-throughput scanning and editing vs single-action focus and conversion vs exploratory browsing.
3. **The Single Signature Element (Spend Boldness in One Place)**:
   - Identify the ONE memorable visual anchor (e.g., an oversized typographic ticker, an interactive timeline canvas, a dense data HUD). Keep all surrounding surfaces disciplined, quiet, and minimalist.
4. **Taste Dial Mapping**:
   - Select and write target dials to `reference/DESIGN.md`:
     - **B2B High-Density Data Cockpit**: `DESIGN_VARIANCE=3`, `VISUAL_DENSITY=9`, `MOTION_INTENSITY=2`
     - **Apple Fluid Tactile Experience**: `DESIGN_VARIANCE=6`, `VISUAL_DENSITY=5`, `MOTION_INTENSITY=9`
     - **Editorial Minimalist Showcase**: `DESIGN_VARIANCE=8`, `VISUAL_DENSITY=3`, `MOTION_INTENSITY=5`
     - **Technical Terminal / Developer HUD**: `DESIGN_VARIANCE=4`, `VISUAL_DENSITY=8`, `MOTION_INTENSITY=1`
     - **Default Balanced SaaS**: `DESIGN_VARIANCE=5`, `VISUAL_DENSITY=7`, `MOTION_INTENSITY=4`

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
