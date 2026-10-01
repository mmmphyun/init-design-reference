# Prohibited Patterns (Do Not Copy)

Source: Derived from Anthropic frontend-design guidelines & Production Standards.

## 1. AI Cliché Aesthetics
- **No SaaS Card Kit**: Do NOT chop content into identical rounded cards with uniform border-radius and soft grey drop-shadows (`rgba(0, 0, 0, 0.1)`).
- **No Warm-Clay Defaults**: Do NOT use warm cream (`#F4F1EA`) paired with high-contrast serif display and terracotta/warm-clay accents (`#D97757`) unless explicitly requested.
- **No Neon Monotones**: Do NOT use near-black backgrounds accented solely by a single bright acid-green or vermilion element.
- **No Broadsheet Mimicry**: Do NOT use dense hairline newspaper layouts with zero border-radius unless fitting the editorial brief.
- **No Tinted Near-Black**: Do NOT substitute pure black with tinted near-black (`#0B0B0B`, `#111`) as a generic default.
- **No Decorative Gradient Washes**: Gradients must encode state or depth, never purely arbitrary background fills.
- **No Hero Stats Default**: Do NOT default to a big number + small label + supporting stats + gradient accent layout unless justified by the brief.

## 2. Template Chrome & Typography Tells
- **No Tracked-Out Eyebrows**: Do NOT place small uppercase labels with wide letter-spacing (`ALL-CAPS`) directly above every single heading.
- **No Redundant Typographic Labels**: Do NOT prepend decorative category labels above content when context is already self-evident.
- **No Monospace Data Labels**: Do NOT reach for monospace fonts for small UI labels, badges, or meta tags unless displaying actual code or tabular numbers.
- **No Middle-Dot Meta Strings**: Avoid repetitive `Item A · Item B · Item C` meta strings across cards.
- **No Spaced Em Dash Labels**: Avoid labels structured as `CATEGORY — description`.
- **No Suffix Arrows**: Do NOT append `→` or `->` to every link and button.
- **No Single-Word Color Highlights**: Do NOT accent just a single word in a headline with italic, bold, or accent color.
- **Line Length Constraints**: Keep body text lines strictly under 80 characters for optimal readability.

## 3. Structural & Motion Tells
- **No Decorative Step Numbers**: Do NOT place numbered markers (`01`, `02`, `03`) next to content unless it is a genuinely ordered process or timeline.
- **No Universal Scroll Entrances**: Avoid cascading fade-and-slide-up animations across every section; use motion only for direct user interactions.
- **Respect Reduced Motion**: Always provide `@media (prefers-reduced-motion: reduce)` fallbacks.

## 4. UI Copywriting & State Rules
- **Active Voice CTAs**: Name buttons by immediate outcome ("Save changes", "Create project"), not vague system commands ("Submit").
- **Directional Errors**: Explain precisely what went wrong and provide an actionable fix without emotional apologies.
- **Actionable Empty States**: An empty screen must guide the user to their first action, never remain dead space.
