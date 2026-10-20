# Visual Direction & Aesthetic Framework
<!-- Derived from jakubkrehel/skills (MIT License) & frontend-design -->

Synthesizes Jakub Krehel's design brief extraction protocol with deterministic token execution and curated palette libraries.

---

## 1. Gate 0: Alignment Protocol & Decision Matrix Tracking

Before touching layout or code, the agent extracts requirements using a structured **7-Decision Matrix**:

### 7-Decision Matrix Tracking
1. **Target User & Context**: Internal operators vs consumers / casual users.
2. **Hero Action & Screen**: The single most critical operation or viewport.
3. **Visual Direction & References**: Tonal mood, surface brightness (dark vs light vs warm neutral), typographic character (sans vs serif vs mono), benchmark aesthetics.
4. **Interaction & Motion Vibe**: Immediate/understated reaction vs organic/spring feedback.
5. **Visual Density**: Information-dense multi-metric cockpit vs airy typographical rhythm.
6. **Device Scope**: Desktop workspace vs mobile-first responsive.
7. **Brand Constraints & Accessibility**: Specific brand colors, contrast targets, compliance.

### Turn-Budgeted Deep Probe
- **Budget**: Recommended 2~3 dialog turns total (max 1 follow-up probe per specific topic). Continue inquiry only when high-impact architecture items remain undefined.
- **Probe Only High-Impact Gaps**: Questions are limited to undefined ([미정]) items that alter design architecture.
- **Neutral Phrasing**: Avoid biased brand names. Inquire about concrete tactile feedback and information hierarchy.
- **Dynamic Theme Synthesis**: Predefined presets serve as baselines. Tune the 3 dials (`DESIGN_VARIANCE`, `VISUAL_DENSITY`, `MOTION_INTENSITY`) freely (1~10) to match the agreed brief.
- **Approval Gate**: Present the synthesized proposal, explicit dials, and default assumptions. **Wait for explicit user confirmation before initiating Phase 1~4 autonomous execution.**

---

## 2. Curated Aesthetic Palettes (Reference Baselines)

Mathematical color spaces (like OKLCH) guarantee contrast ratios, but cannot compute aesthetic discernment or domain taste. When no project design reference, Figma token set, or explicit user color brief exists, the following domain palettes may serve as starting baselines:

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

When external Color or Palette MCPs (e.g., `color-palette-mcp`, Coolors MCP, Color Hunt MCP) are available in the agent harness:

### A. Recommended Tooling: `color-palette-mcp` (ppower-dev)
When the user specifies an explicit brand color (e.g. `#0A84FF`), domain-specific aesthetic (e.g. `ecommerce`, `dashboard`, `webrtc`), or natural language visual intent, invoke `color-palette-mcp` to generate dynamic 50~900 scales rather than falling back to static preset defaults:
- `generate_palette`: Generates base 50~900 scales and semantic colors from a single hex input.
- `extend_palette_for_project`: Tailors complementary palettes for domain types (`ecommerce`, `dashboard`, `webrtc`, `blog`).
- `generate_dynamic_colors`: Synthesizes project-tailored color tokens from natural language descriptions.
- `validate_accessibility`: Verifies WCAG AA/AAA contrast ratios between text and surface pairs.

### B. Deterministic Semantic Token Mapping
Map the 50~900 numeric palette output into `.design/tokens/colors.json` semantic slots:
- **Dark Mode Standard** (Default for SaaS cockpits & technical portals):
  - Canvas & Surfaces: `background.primary` = 950 (Canvas), `background.surface` = 900 (Surface Plate), `background.secondary` = 850 (Card Elevated).
  - Typography: `text.primary` = 50 (High contrast), `text.secondary` = 400 (Readable metadata), `text.muted` = 500 (Subtle hints).
  - Accent Affordance: `accent.primary` = 500 (Brand focal), `accent.hover` = 600 (Interactive active).
  - Structural Borders: `border.subtle` = 850, `border.default` = 800, `border.strong` = 700.
  - Status Indicators: Preserve standard semantic signals (`status.success`, `warning`, `error`, `info`).
- **Light Mode Standard** (Inverted luminance):
  - Canvas & Surfaces: `background.primary` = 50, `background.surface` = 100, `background.secondary` = 200.
  - Typography: `text.primary` = 900, `text.secondary` = 700, `text.muted` = 500.

### C. Validation & Hard-Guard Check
1. Verify body text contrast meets WCAG 2.1 AA (>= 4.5:1 against adjacent surface).
2. Directly populate `.design/tokens/colors.json`.
3. Run `python scripts/adapter.py --verify-spec` to ensure all required core token slots and hex formats pass validation.

