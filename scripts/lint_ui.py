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
import argparse
from typing import List, Dict, Tuple

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
        severity="ERROR",
        message="Generic AI purple/indigo gradient detected. Use purposeful, brand-aligned solid surfaces or subtle contrast.",
        pattern=re.compile(r"\b(?:from-indigo-[0-9]{3}|from-purple-[0-9]{3}|from-violet-[0-9]{3})\s+(?:to-purple-[0-9]{3}|to-indigo-[0-9]{3}|to-pink-[0-9]{3})\b")
    ),

    # 3. All-Caps Over-tracking Label Cliche
    Rule(
        rule_id="cliche-tracking-uppercase",
        severity="ERROR",
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
        severity="ERROR",
        message="Decorative ambient glow (blur-2xl / blur-3xl) background artifact detected. Maintain crisp surface boundaries.",
        pattern=re.compile(r"\bblur-(?:2xl|3xl|\[[0-9]{2,3}px\])\b")
    ),

    # 6. Layout Thrashing Transition
    Rule(
        rule_id="layout-thrashing-animation",
        severity="ERROR",
        message="Layout thrashing animation detected (transition-all or animating width/height/top/left). Animate ONLY transform and opacity.",
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
    )
]

def is_line_ignored(line: str) -> bool:
    return bool(re.search(r"lint-ui-(?:disable|ignore)|@lint-ignore", line))

def scan_file(file_path: str) -> List[Dict]:
    violations = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Warning: Failed to read {file_path}: {e}", file=sys.stderr)
        return []

    for line_num, line in enumerate(lines, start=1):
        if is_line_ignored(line):
            continue

        for rule in RULES:
            match = rule.pattern.search(line)
            if match:
                matched_str = match.group(0)
                if rule.exception_pattern and rule.exception_pattern.search(line):
                    continue

                violations.append({
                    "file": file_path,
                    "line": line_num,
                    "rule_id": rule.rule_id,
                    "severity": rule.severity,
                    "message": rule.message,
                    "snippet": line.strip()
                })

    return violations

def run_linter(targets: List[str], excludes: List[str] = None) -> int:
    active_excludes = DEFAULT_EXCLUDES.union(set(excludes or []))
    files_to_scan = []

    for target in targets:
        if os.path.isfile(target):
            files_to_scan.append(target)
        elif os.path.isdir(target):
            for root, dirs, files in os.walk(target):
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
