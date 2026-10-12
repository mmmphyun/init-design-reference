#!/usr/bin/env python3
"""
scripts/lint_ui.py - Deterministic UI Anti-Pattern & Cliché Linter

Ported from pbakaus/impeccable detector rule specifications under the Apache License 2.0.
Original concept: Paul Bakaus (https://github.com/pbakaus/impeccable)

Inspects frontend source files (.tsx, .jsx, .vue, .svelte, .html, .css)
for hardcoded values, AI cliches, layout thrashing, and aesthetic anti-patterns.
"""

import os
import sys
import re
import json
import argparse
from typing import List, Dict, Tuple

_CACHED_AVAILABLE_TOKENS = None

def get_available_color_tokens() -> List[str]:
    global _CACHED_AVAILABLE_TOKENS
    if _CACHED_AVAILABLE_TOKENS is not None:
        return _CACHED_AVAILABLE_TOKENS

    candidates = [
        os.path.join(".design", "tokens", "colors.json"),
        os.path.join("reference", "tokens", "colors.json"),
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates", "tokens", "colors.json")
    ]
    tokens = []
    for c in candidates:
        if os.path.exists(c):
            try:
                with open(c, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for group, items in data.items():
                    if isinstance(items, dict):
                        for subkey in items:
                            tokens.append(f"bg-{subkey}" if group == "background" else f"{group}-{subkey}")
                    else:
                        tokens.append(group)
                break
            except Exception:
                pass

    if not tokens:
        tokens = ["bg-surface", "bg-background", "text-primary", "text-muted", "accent-primary", "border-default"]

    _CACHED_AVAILABLE_TOKENS = tokens
    return _CACHED_AVAILABLE_TOKENS

def get_rule_suggestion(rule_id: str) -> str:
    if rule_id == "a11y-naked-outline-none":
        return "Add 'focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2'"
    if rule_id == "hardcoded-hex":
        tokens = get_available_color_tokens()
        return f"Use semantic tokens from colors.json: {', '.join(tokens[:6])}"
    if rule_id == "cliche-ai-gradient":
        return "Use purposeful solid surface (bg-surface) or subtle single-axis contrast"
    if rule_id == "cliche-tracking-uppercase":
        return "Use standard sentence case or normal tracking (tracking-normal)"
    if rule_id == "high-density-max-width-constraint":
        return "Replace with 'w-full' to prevent lateral whitespace abandonment in high-density views"
    if rule_id == "numeric-column-text-left":
        return "Change 'text-left' to 'text-right' (and justify-end) for numeric data"
    if rule_id == "indicator-too-slender":
        return "Use 'h-1.5' (6px) or larger for functional indicator visibility"
    if rule_id == "critical-identifier-truncate":
        return "Remove 'truncate' and fixed 'max-w-[...]' to ensure full visibility of critical identifiers"
    return ""

# Supported file extensions for frontend source code
DEFAULT_EXTENSIONS = {".tsx", ".jsx", ".vue", ".svelte", ".html", ".css"}
DEFAULT_EXCLUDES = {"node_modules", ".git", "dist", "build", ".next", ".nuxt", "reference"}

class Rule:
    def __init__(self, rule_id: str, severity: str, message: str, pattern: re.Pattern, exception_pattern: re.Pattern = None):
        self.rule_id = rule_id
        self.severity = severity  # "ERROR" or "WARN"
        self.message = message
        self.pattern = pattern
        self.exception_pattern = exception_pattern

# ---------------------------------------------------------------------------
# Deterministic Rule Definitions
# ---------------------------------------------------------------------------
RULES: List[Rule] = [
    # 1. Hardcoded Hex Colors
    Rule(
        rule_id="hardcoded-hex",
        severity="ERROR",
        message="Hardcoded hex color detected. Use semantic tokens (e.g. bg-surface, text-foreground) from reference/tokens/colors.json.",
        pattern=re.compile(r"#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b"),
        exception_pattern=re.compile(r"url\(#|stroke=['\"]#|fill=['\"]#none|currentColor")
    ),

    # 2. AI Cliche Purple / Indigo Gradients
    Rule(
        rule_id="cliche-ai-gradient",
        severity="WARN",
        message="Generic AI purple/indigo gradient detected. Use purposeful, brand-aligned solid surfaces or subtle contrast.",
        pattern=re.compile(r"\b(?:from-indigo-[0-9]{3}|from-purple-[0-9]{3}|from-violet-[0-9]{3})\s+(?:to-purple-[0-9]{3}|to-indigo-[0-9]{3}|to-pink-[0-9]{3})\b")
    ),

    # 3. All-Caps Over-tracking Label Cliche
    Rule(
        rule_id="cliche-tracking-uppercase",
        severity="WARN",
        message="Generic AI 'uppercase tracking-widest' eyebrow label detected. Prefer lowercase or standard sentence case.",
        pattern=re.compile(r"\b(?:tracking-widest|tracking-wider)\s+uppercase\b|\buppercase\s+(?:tracking-widest|tracking-wider)\b")
    ),

    # 4. Overly Rounded Giant Radii
    Rule(
        rule_id="excessive-radius",
        severity="WARN",
        message="Excessive bubble-like card curvature (rounded-3xl/rounded-[32px+]). Enforce reference/tokens/radii.json.",
        pattern=re.compile(r"\brounded-(?:3xl|\[(?:[3-9][0-9]|1[0-9]{2})px\])\b")
    ),

    # 5. Meaningless Ambient Glow Blur
    Rule(
        rule_id="ambient-glow-blur",
        severity="WARN",
        message="Decorative ambient glow (blur-2xl / blur-3xl) background artifact detected. Maintain crisp surface boundaries.",
        pattern=re.compile(r"\bblur-(?:2xl|3xl|\[[0-9]{2,3}px\])\b")
    ),

    # 6. Layout Thrashing Transition
    Rule(
        rule_id="layout-thrashing-animation",
        severity="WARN",
        message="Layout thrashing animation detected (transition-all or animating layout geometry). Avoid animating width/height/top/left/margin/padding; animate spatial properties (transform, opacity) or state feedback properties (color, background-color, border-color, box-shadow).",
        pattern=re.compile(r"\btransition-all\b|\btransition-\[(?:width|height|top|left|margin|padding)\]")
    ),

    # 7. Unsemantic Step Markers (e.g. "01", "02" decorators)
    Rule(
        rule_id="unsemantic-step-marker",
        severity="WARN",
        message="Artificial step number decorator ('01', '02', 'Step 1') detected in UI markup. Remove unless genuinely ordered workflow.",
        pattern=re.compile(r">\s*(?:0[1-9]|Step\s+[0-9])\s*<")
    ),

    # 8. Unnecessary Trailing Arrow Cliche
    Rule(
        rule_id="trailing-arrow-cliche",
        severity="WARN",
        message="Trailing arrow ('->' or '→') appended to CTA label. Let typography and layout communicate affordance.",
        pattern=re.compile(r">\s*.*?(?:&rarr;|→|->)\s*<")
    ),

    # 9. Pseudo-black Abuse
    Rule(
        rule_id="pseudo-black-abuse",
        severity="WARN",
        message="Pure black surface (bg-black) detected. Use dark neutral surface token from reference/tokens/colors.json.",
        pattern=re.compile(r"\bbg-black\b")
    ),

    # 10. Excessive Micro-Interaction Duration (>350ms)
    Rule(
        rule_id="excessive-micro-duration",
        severity="WARN",
        message="Micro-interaction animation duration exceeds 350ms budget (duration-500/700/1000). Use duration-fast or duration-normal.",
        pattern=re.compile(r"\b(?:transition|animate)[^\"'>]*\bduration-(?:500|700|1000)\b")
    ),

    # 11. Untokenized Tailwind Color Palette
    Rule(
        rule_id="untokenized-tailwind-color",
        severity="WARN",
        message="Raw Tailwind color palette detected. Use semantic tokens (e.g. bg-surface, text-foreground, bg-background) from .design/tokens/colors.json.",
        pattern=re.compile(r"\b(?:bg|text|border|ring)-(?:slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-(?:50|[1-9]00|950)\b")
    )
]


def is_line_ignored(line: str) -> bool:
    return bool(re.search(r"lint-ui-(?:disable|ignore)|@lint-ignore", line))

def strip_comments_preserving_lines(text: str) -> str:
    """
    Strips single-line (//), multi-line (/* */, {/* */}), and HTML (<!-- -->) comments.
    Preserves exact newline counts and character offsets by substituting non-newline characters with spaces.
    Prevents false positives on commented-out reference code or documentation.
    """
    def repl_block(m):
        return re.sub(r"[^\r\n]", " ", m.group(0))

    # Strip block comments (/* ... */, <!-- ... -->, {/* ... */})
    text = re.sub(r"/\*[\s\S]*?\*/|<!--[\s\S]*?-->", repl_block, text)
    text = re.sub(r"\{/\*[\s\S]*?\*/\}", repl_block, text)

    # Strip single-line comments (// ...)
    def repl_single(m):
        prefix = m.group(1)
        comment = m.group(2)
        return prefix + (" " * len(comment))

    text = re.sub(r"(^|[^\w:])(//[^\r\n]*)", repl_single, text, flags=re.MULTILINE)
    return text

def extract_tag_blocks(content: str) -> List[Tuple[int, str, str]]:
    """
    Extracts HTML/JSX start-tags and self-closing tags across multiple lines.
    Returns list of (line_number, tag_name, full_tag_content).
    Enables DOM-element scoped attribute analysis (mimicking impeccable's Dom trait).
    """
    tag_blocks = []
    pattern = re.compile(r"<([a-zA-Z][a-zA-Z0-9_\-\.:]*)([^>]*?)>", re.DOTALL)
    for m in pattern.finditer(content):
        start_pos = m.start()
        line_num = content[:start_pos].count("\n") + 1
        tag_name = m.group(1)
        full_tag = m.group(0)
        tag_blocks.append((line_num, tag_name, full_tag))
    return tag_blocks

def check_file_contracts(file_path: str, full_content: str) -> List[Dict]:
    violations = []
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in {".tsx", ".jsx", ".vue", ".svelte"}:
        return violations

    has_collection = bool(re.search(r"\b(?:data|items|records|rows|list)\.map\s*\(", full_content))
    is_component = bool(re.search(r"export\s+(?:default\s+)?(?:function|const)\s+[A-Z]\w+", full_content))

    if has_collection and is_component:
        missing = []
        if not re.search(r"\b(?:loading|isLoading|aria-busy|skeleton|animate-pulse|Spinner)\b", full_content, re.I):
            missing.append("Loading")
        if not re.search(r"\b(?:error|isError|role=[\"']alert[\"']|retry|onRetry)\b", full_content, re.I):
            missing.append("Error")
        if not re.search(r"\b(?:empty|length\s*===?\s*0|no records|zero-data)\b", full_content, re.I):
            missing.append("Empty")

        if missing:
            violations.append({
                "file": file_path,
                "line": 1,
                "rule_id": "component-4state-incomplete",
                "severity": "WARN",
                "message": f"Data collection component missing explicit state guards: {', '.join(missing)}. Enforce 4-state contract (Loading, Empty, Error, Success).",
                "snippet": f"Missing states: {', '.join(missing)}"
            })
    return violations

def scan_file(file_path: str) -> List[Dict]:
    violations = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            raw_content = f.read()
    except Exception as e:
        print(f"Warning: Failed to read {file_path}: {e}", file=sys.stderr)
        return []

    # 1. Whole-file contract validation (Hobson 4-State Completeness)
    violations.extend(check_file_contracts(file_path, raw_content))

    # 2. Preprocess: Strip comments while preserving line numbers (eliminates comment false positives)
    clean_content = strip_comments_preserving_lines(raw_content)
    clean_lines = clean_content.splitlines()

    # 3. DOM-Element Scoped Rules (Tag Blocks across multiple lines)
    tag_blocks = extract_tag_blocks(clean_content)
    for line_num, tag_name, full_tag in tag_blocks:
        if is_line_ignored(full_tag):
            continue

        # Rule 10: a11y-naked-outline-none (WCAG 2.4.7)
        if re.search(r"\b(?:outline-none|focus:outline-none)\b", full_tag):
            if not re.search(r"\b(?:focus-visible:ring|focus:ring|focus-visible:outline)\b", full_tag):
                violations.append({
                    "file": file_path,
                    "line": line_num,
                    "rule_id": "a11y-naked-outline-none",
                    "severity": "ERROR",
                    "message": "outline-none detected on element without focus-visible:ring replacement (WCAG 2.4.7).",
                    "suggestion": get_rule_suggestion("a11y-naked-outline-none"),
                    "snippet": full_tag.strip().splitlines()[0]
                })

        # Rule 11: a11y-missing-alt (WCAG 1.1.1)
        if tag_name.lower() == "img":
            if not re.search(r"\balt=", full_tag, re.I):
                violations.append({
                    "file": file_path,
                    "line": line_num,
                    "rule_id": "a11y-missing-alt",
                    "severity": "ERROR",
                    "message": "<img> tag missing alt attribute (WCAG 1.1.1). Provide informative alt text or alt=\"\" for decorative images.",
                    "suggestion": "Add alt=\"...\" description or alt=\"\" for decorative images",
                    "snippet": full_tag.strip().splitlines()[0]
                })

    # 4. High-Density Views Specialized Checks
    # High-density rules apply when explicit high-density profile is active in DESIGN.md (Density >= 8)
    # or when explicitly marked in file header/name for specialized telemetry views.
    def get_project_density() -> int:
        for p in [".design/DESIGN.md", "reference/DESIGN.md"]:
            if os.path.exists(p):
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        m = re.search(r"`VISUAL_DENSITY`:\s*([0-9]+)", f.read())
                        if m:
                            return int(m.group(1))
                except Exception:
                    pass
        return 5

    project_density = get_project_density()
    is_telemetry_file = bool(re.search(r"telemetry|cockpit|monitor|cluster|node_status", file_path, re.I))
    is_high_density_context = (project_density >= 8) or is_telemetry_file

    if is_high_density_context:
        # Check max-width constraint wrapper (WARN: design advice, not a crash)
        for line_num, line in enumerate(clean_lines, start=1):
            if is_line_ignored(line):
                continue
            if re.search(r"\bmax-w-(?:[5-7]xl|screen-(?:xl|2xl))\b", line):
                violations.append({
                    "file": file_path,
                    "line": line_num,
                    "rule_id": "high-density-max-width-constraint",
                    "severity": "WARN",
                    "message": "Restricted max-width wrapper (max-w-7xl/6xl/etc.) detected in high-density view. Consider w-full if lateral space is needed for operational data.",
                    "suggestion": get_rule_suggestion("high-density-max-width-constraint"),
                    "snippet": line.strip()
                })

        # Check numeric table headers and cells using text-left
        NUMERIC_HEADER_KEYWORDS = re.compile(
            r"(?:CPU|메모리|Memory|부하|점유|로드|Load|스왑|Swap|디스크|Disk|네트워크|Network|IOPS|Throughput|대역폭|가동\s*시간|Uptime|Latency|QPS|RPS|가격|금액|수량|잔액|매출|비율|Percent|Price|Amount|Count|Balance|Revenue|Ratio|Cost|Total|%)",
            re.I
        )
        NUMERIC_CELL_KEYWORDS = re.compile(
            r"(?:usagePercent|loadAvg|iops|Throughput|swapMargin|cores|uptimePercent|amount|price|count|balance|revenue|cost|total|\b\d+(?:\.\d+)?%\b)",
            re.I
        )

        for m in re.finditer(r"<th\b([^>]*)>([\s\S]*?)</th>", clean_content, re.IGNORECASE):
            th_attrs = m.group(1)
            th_content = m.group(2)
            if re.search(r"\btext-left\b", th_attrs) and NUMERIC_HEADER_KEYWORDS.search(th_content):
                start_pos = m.start()
                line_num = clean_content[:start_pos].count("\n") + 1
                full_match = m.group(0).strip().splitlines()[0]
                if not is_line_ignored(full_match):
                    violations.append({
                        "file": file_path,
                        "line": line_num,
                        "rule_id": "numeric-column-text-left",
                        "severity": "WARN",
                        "message": "Numeric metric table header using 'text-left'. Consider 'text-right' alignment for multi-row comparison readability.",
                        "suggestion": get_rule_suggestion("numeric-column-text-left"),
                        "snippet": full_match
                    })

        for m in re.finditer(r"<td\b([^>]*)>([\s\S]*?)</td>", clean_content, re.IGNORECASE):
            td_attrs = m.group(1)
            td_content = m.group(2)
            if re.search(r"\btext-left\b", td_attrs) and NUMERIC_CELL_KEYWORDS.search(td_content):
                start_pos = m.start()
                line_num = clean_content[:start_pos].count("\n") + 1
                full_match = m.group(0).strip().splitlines()[0]
                if not is_line_ignored(full_match):
                    violations.append({
                        "file": file_path,
                        "line": line_num,
                        "rule_id": "numeric-column-text-left",
                        "severity": "WARN",
                        "message": "Numeric telemetry table cell using 'text-left'. Consider 'text-right' alignment for numeric data.",
                        "suggestion": get_rule_suggestion("numeric-column-text-left"),
                        "snippet": full_match
                    })

        # Check anemic slender indicators (h-0.5 or h-1) (w-full progress bar contexts)
        for line_num, line in enumerate(clean_lines, start=1):
            if is_line_ignored(line):
                continue
            if re.search(r"\bw-full\b", line) and re.search(r"\b(?:h-0\.5|h-1)(?![.\d])\b", line) and re.search(r"rounded|bg-|bar|gauge|indicator|progress|overflow-hidden", line):
                violations.append({
                    "file": file_path,
                    "line": line_num,
                    "rule_id": "indicator-too-slender",
                    "severity": "WARN",
                    "message": "Slender indicator bar (h-0.5 or h-1) detected. In operational screens, consider h-1.5 (6px) or larger for peripheral glanceability.",
                    "suggestion": get_rule_suggestion("indicator-too-slender"),
                    "snippet": line.strip()
                })

        # Check illegal truncation on critical domain identifiers (id, code, sku, host, node, zone, account)
        CRITICAL_IDENTIFIER_KEYWORDS = re.compile(r"(?:id|code|sku|uuid|account|tx|order|host|node|region|zone|address|ip|식별자|계좌|주문|호스트)", re.I)
        for line_num, line in enumerate(clean_lines, start=1):
            if is_line_ignored(line):
                continue
            if re.search(r"\b(?:truncate|max-w-\[\d+px\])\b", line) and CRITICAL_IDENTIFIER_KEYWORDS.search(line):
                violations.append({
                    "file": file_path,
                    "line": line_num,
                    "rule_id": "critical-identifier-truncate",
                    "severity": "WARN",
                    "message": "Truncation detected on critical domain identifier. Verify whether full visibility is required to prevent misidentification.",
                    "suggestion": get_rule_suggestion("critical-identifier-truncate"),
                    "snippet": line.strip()
                })

    # 4. Line-by-line regex rule scanning on uncommented code
    for line_num, line in enumerate(clean_lines, start=1):
        if is_line_ignored(line):
            continue

        for rule in RULES:
            match = rule.pattern.search(line)
            if match:
                if rule.exception_pattern and rule.exception_pattern.search(line):
                    continue

                violations.append({
                    "file": file_path,
                    "line": line_num,
                    "rule_id": rule.rule_id,
                    "severity": rule.severity,
                    "message": rule.message,
                    "suggestion": get_rule_suggestion(rule.rule_id),
                    "snippet": line.strip()
                })

    return violations

def run_linter(targets: List[str], excludes: List[str] = None) -> int:
    active_excludes = DEFAULT_EXCLUDES.union(set(excludes or []))
    files_to_scan = []

    for target in targets:
        resolved = target
        if not os.path.exists(resolved):
            clean_target = target.strip("/\\")
            for entry in sorted(os.listdir(".")):
                if os.path.isdir(entry) and not entry.startswith(".") and entry not in active_excludes:
                    candidate = os.path.join(entry, clean_target)
                    if os.path.exists(candidate):
                        resolved = candidate
                        break

        if os.path.isfile(resolved):
            files_to_scan.append(resolved)
        elif os.path.isdir(resolved):
            for root, dirs, files in os.walk(resolved):
                dirs[:] = [d for d in dirs if d not in active_excludes]
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in DEFAULT_EXTENSIONS:
                        files_to_scan.append(os.path.join(root, file))

    if not files_to_scan:
        print(f"No matching frontend source files found in targets: {targets}")
        return 0

    total_violations = []
    for fp in files_to_scan:
        total_violations.extend(scan_file(fp))

    error_count = sum(1 for v in total_violations if v["severity"] == "ERROR")
    warn_count = sum(1 for v in total_violations if v["severity"] == "WARN")

    if total_violations:
        print("\n--- UI Lint Findings ---")
        for v in total_violations:
            prefix = "[ERROR]" if v["severity"] == "ERROR" else "[WARN]"
            print(f"{prefix} {v['file']}:{v['line']} ({v['rule_id']})")
            print(f"       {v['message']}")
            if v.get("suggestion"):
                print(f"       Suggestion: {v['suggestion']}")
            print(f"       Code: {v['snippet']}\n")

    print(f"Scan complete: {len(files_to_scan)} files inspected. Findings: {error_count} errors, {warn_count} warnings.")

    if error_count > 0:
        print("Lint FAILED. Rectify errors or align with reference/ tokens and patterns.", file=sys.stderr)
        return 1

    print("Lint PASSED.")
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deterministic UI Anti-Pattern & Cliché Linter")
    parser.add_argument("targets", nargs="*", default=["."], help="Directories or files to scan")
    parser.add_argument("--exclude", nargs="*", default=[], help="Directories to ignore")
    args = parser.parse_args()

    sys.exit(run_linter(args.targets, args.exclude))
