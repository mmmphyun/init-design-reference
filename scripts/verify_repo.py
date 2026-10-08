#!/usr/bin/env python3
"""
Repository Integrity & Architecture Verification Script
Validates core architectural principles, token validity, adapter idempotency, and linter functions.
"""

import os
import sys
import glob
import json
import shutil
import tempfile
import subprocess
import re


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def log(msg, status="INFO"):
    print(f"[{status}] {msg}")

def check_python_syntax():
    log("Validating Python syntax for all scripts...", "TEST")
    scripts = ["adapter.py", "lint_ui.py", "capture_ui.py", "sync_figma.py", "verify_repo.py"]
    for s in scripts:
        script_path = os.path.join(REPO_ROOT, "scripts", s)
        res = subprocess.run([sys.executable, "-m", "py_compile", script_path], capture_output=True, text=True)
        if res.returncode != 0:
            log(f"Syntax error in scripts/{s}:\n{res.stderr}", "FAIL")
            return False
        log(f"scripts/{s} syntax OK.", "PASS")
    return True

def check_json_tokens():
    log("Validating token JSON schemas...", "TEST")
    token_files = glob.glob(os.path.join(REPO_ROOT, "templates", "tokens", "*.json"))
    if not token_files:
        log("No token JSON files found in templates/tokens!", "FAIL")
        return False

    for token_file in token_files:
        rel_path = os.path.relpath(token_file, REPO_ROOT)
        try:
            with open(token_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                log(f"{rel_path}: root must be a JSON object", "FAIL")
                return False
        except Exception as e:
            log(f"{rel_path}: JSON parsing failed: {e}", "FAIL")
            return False
        log(f"{rel_path} valid JSON.", "PASS")
    return True

def check_required_templates():
    log("Checking mandatory templates and metadata...", "TEST")
    required = [
        "SKILL.md",
        "README.md",
        "README.en.md",
        "CONTRIBUTING.md",
        "CONTRIBUTING.en.md",
        "LICENSE",
        "NOTICE.md",
        "templates/notes/do-not-copy.md",
        "templates/notes/layout.md",
        "templates/tokens/colors.json",
        "templates/tokens/typography.json",
        "templates/tokens/spacing.json",
        "templates/tokens/radii.json",
        "templates/tokens/shadows.json",
        "templates/tokens/motion.json",
        "templates/patterns/layout-shells.md",
        "templates/patterns/data-display.md",
        "templates/patterns/forms-inputs.md",
        "templates/patterns/micro-interactions.md",
        "templates/root/DESIGN.md",
        "templates/root/COMPONENTS.md",
        "templates/root/REVIEW_CHECKLIST.md",
        "scripts/lint_ui.py",
        "scripts/capture_ui.py",
        "scripts/sync_figma.py"
    ]

    missing = []
    for item in required:
        full_path = os.path.join(REPO_ROOT, item.replace("/", os.sep))
        if not os.path.exists(full_path):
            missing.append(item)

    if missing:
        log(f"Missing mandatory files: {missing}", "FAIL")
        return False
    log("All mandatory templates present.", "PASS")
    return True

def check_decoupled_architecture():
    log("Verifying decoupled architecture (no hardcoded templates in script)...", "TEST")
    adapter_path = os.path.join(REPO_ROOT, "scripts", "adapter.py")
    with open(adapter_path, "r", encoding="utf-8") as f:
        content = f.read()

    # adapter.py must not hardcode template markdown or component content
    prohibited_snippets = [
        "# Prohibited Patterns",
        "# System Design Principles",
        "# Component Architecture Guidelines",
        "WCAG 2.1 AA",
        "Pretendard",
        "Space Grotesk"
    ]

    violations = [snip for snip in prohibited_snippets if snip in content]
    if violations:
        log(f"Architecture violation: adapter.py contains hardcoded template strings: {violations}", "FAIL")
        log("Templates must remain decoupled in templates/ directory only.", "FAIL")
        return False

    log("Decoupled architecture rule satisfied.", "PASS")
    return True

def check_scaffold_and_idempotency():
    log("Testing scaffolding and idempotency in isolated workspace...", "TEST")
    adapter_path = os.path.join(REPO_ROOT, "scripts", "adapter.py")
    temp_dir = tempfile.mkdtemp(prefix="init_design_test_")

    try:
        target_design = os.path.join(temp_dir, ".design")

        # 1st run with preset: must create all files in .design
        run1 = subprocess.run([sys.executable, adapter_path, target_design, "--preset", "b2b-dense"], capture_output=True, text=True, cwd=temp_dir)
        if run1.returncode != 0:
            log(f"First run failed with code {run1.returncode}:\n{run1.stderr}", "FAIL")
            return False

        if "Created:" not in run1.stdout:
            log("First run did not report created files.", "FAIL")
            return False

        # Verify preset dials applied to freshly scaffolded DESIGN.md
        with open(os.path.join(target_design, "DESIGN.md"), "r", encoding="utf-8") as f:
            d_init = f.read()
        if "`DESIGN_VARIANCE`: 3" not in d_init or "`VISUAL_DENSITY`: 9" not in d_init:
            log("Fresh preset application failed: b2b-dense dials not applied on initial scaffold!", "FAIL")
            return False

        # Verify pattern and token files exist in target
        expected_pattern = os.path.join(target_design, "patterns", "data-display.md")
        if not os.path.exists(expected_pattern):
            log(f"Pattern file not created: {expected_pattern}", "FAIL")
            return False

        # Verify --verify-spec passes on freshly scaffolded target
        run_spec = subprocess.run([sys.executable, adapter_path, target_design, "--verify-spec"], capture_output=True, text=True, cwd=temp_dir)
        if run_spec.returncode != 0:
            log(f"--verify-spec failed on valid scaffold:\n{run_spec.stderr}", "FAIL")
            return False

        # 2nd run: must skip existing files (idempotency)
        run2 = subprocess.run([sys.executable, adapter_path, target_design], capture_output=True, text=True, cwd=temp_dir)
        if run2.returncode != 0:
            log(f"Second run failed with code {run2.returncode}:\n{run2.stderr}", "FAIL")
            return False

        if "Created:" in run2.stdout or "Skipped existing:" not in run2.stdout:
            log("Idempotency violated: second run modified or recreated files.", "FAIL")
            return False

        # Test dial preservation: modify dial manually, run adapter without --force or --dials
        design_md = os.path.join(target_design, "DESIGN.md")
        with open(design_md, "r", encoding="utf-8") as f:
            d_content = f.read()
        d_content_mod = re.sub(r"`DESIGN_VARIANCE`:\s*[0-9]+", "`DESIGN_VARIANCE`: 9", d_content)
        with open(design_md, "w", encoding="utf-8") as f:
            f.write(d_content_mod)

        subprocess.run([sys.executable, adapter_path, target_design], capture_output=True, text=True, cwd=temp_dir)
        with open(design_md, "r", encoding="utf-8") as f:
            d_content_after = f.read()
        if "`DESIGN_VARIANCE`: 9" not in d_content_after:
            log("Dial preservation violated: existing dial was overridden without --force/--dials.", "FAIL")
            return False

        # Test --bridge-only flag
        run_bridge = subprocess.run([sys.executable, adapter_path, target_design, "--bridge-only"], capture_output=True, text=True, cwd=temp_dir)
        if run_bridge.returncode != 0:
            log(f"--bridge-only failed:\n{run_bridge.stderr}", "FAIL")
            return False
        tokens_css_path = os.path.join(target_design, "tokens", "tokens.css")
        # Test dynamic status alpha derivation in CSS bridge (including 4-digit and custom HEX)
        tokens_json_path = os.path.join(target_design, "tokens", "colors.json")
        with open(tokens_json_path, "r", encoding="utf-8") as f:
            c_data = json.load(f)
        c_data.setdefault("status", {})["error"] = "#f00f"  # 4-digit hex (#RGBA)
        with open(tokens_json_path, "w", encoding="utf-8") as f:
            json.dump(c_data, f, indent=2)

        run_bridge2 = subprocess.run([sys.executable, adapter_path, target_design, "--bridge-only"], capture_output=True, text=True, cwd=temp_dir)
        if run_bridge2.returncode != 0:
            log(f"--bridge-only with custom status failed:\n{run_bridge2.stderr}", "FAIL")
            return False

        with open(tokens_css_path, "r", encoding="utf-8") as f:
            t_css_custom = f.read()
        if "--status-error-bg: rgba(255, 0, 0, 0.12);" not in t_css_custom:
            log(f"Dynamic status alpha derivation failed for 4-digit hex #f00f! Got:\n{t_css_custom}", "FAIL")
            return False

        # Test token preservation when DESIGN.md is absent with overlapping preset keys (background.primary)
        isolated_dir = tempfile.mkdtemp(prefix="token_preserv_test_")
        try:
            iso_target = os.path.join(isolated_dir, ".design")
            os.makedirs(os.path.join(iso_target, "tokens"), exist_ok=True)
            custom_colors_path = os.path.join(iso_target, "tokens", "colors.json")
            with open(custom_colors_path, "w", encoding="utf-8") as f:
                json.dump({
                    "background": {"primary": "#112233"},
                    "custom": {"brand": "#123456"}
                }, f)
            # Scaffold without DESIGN.md initially present
            subprocess.run([sys.executable, adapter_path, iso_target, "--preset", "apple-fluid"], capture_output=True, text=True, cwd=isolated_dir)
            with open(custom_colors_path, "r", encoding="utf-8") as f:
                read_colors = json.load(f)
            if read_colors.get("background", {}).get("primary") != "#112233":
                log("Token preservation failed: overlapping key 'background.primary' was overridden by preset!", "FAIL")
                return False
            if read_colors.get("custom", {}).get("brand") != "#123456":
                log("Token preservation failed: custom key was lost!", "FAIL")
                return False
        finally:
            shutil.rmtree(isolated_dir, ignore_errors=True)

        # 3rd run with --force: must overwrite
        run3 = subprocess.run([sys.executable, adapter_path, target_design, "--force"], capture_output=True, text=True, cwd=temp_dir)
        if run3.returncode != 0:
            log(f"Force run failed with code {run3.returncode}:\n{run3.stderr}", "FAIL")
            return False

        if "Created:" not in run3.stdout:
            log("Force flag violated: did not report recreated files.", "FAIL")
            return False

        log("Scaffolding, idempotency, preset, hard-guard, dial/token preservation, and force overwrite verified.", "PASS")
        return True
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def check_linter_behavior():
    log("Verifying lint_ui.py detector behavior...", "TEST")
    linter_path = os.path.join(REPO_ROOT, "scripts", "lint_ui.py")
    temp_dir = tempfile.mkdtemp(prefix="lint_test_")

    try:
        # Create a file with deliberate AI clichés and raw tailwind palette
        bad_file = os.path.join(temp_dir, "bad_component.tsx")
        with open(bad_file, "w", encoding="utf-8") as f:
            f.write(
                '<span className="uppercase tracking-widest text-[#6366f1]">BAD</span>\n'
                '<div className="bg-slate-900">Untokenized color</div>\n'
            )


        # Create a clean file with multiline JSX and commented-out hex (must NOT trigger false positives)
        good_file = os.path.join(temp_dir, "good_component.tsx")
        with open(good_file, "w", encoding="utf-8") as f:
            f.write(
                '// Legacy note mentioning #6366f1 in comment\n'
                '/* Block comment with #123456 */\n'
                '<input\n'
                '  className="outline-none"\n'
                '  focus-visible:ring-2\n'
                '/>\n'
                '<span className="text-sm font-medium text-foreground">GOOD</span>\n'
            )

        # Run linter on bad file (must fail with exit code 1)
        res_bad = subprocess.run([sys.executable, linter_path, bad_file], capture_output=True, text=True)
        if res_bad.returncode == 0 or "hardcoded-hex" not in res_bad.stdout or "untokenized-tailwind-color" not in res_bad.stdout:
            log("Linter failed to catch intentional hardcoded hex / raw color / cliché!", "FAIL")
            return False

        # Create a bad high-density file testing high-density-max-width-constraint, numeric-column-text-left, indicator-too-slender, critical-identifier-truncate
        bad_telemetry = os.path.join(temp_dir, "bad_telemetry.tsx")
        with open(bad_telemetry, "w", encoding="utf-8") as f:
            f.write(
                'export function BadDashboard() {\n'
                '  return (\n'
                '    <div className="max-w-7xl mx-auto">\n'
                '      <div className="truncate text-xs">node-kr-zone-1 (order-tx-8821)</div>\n'
                '      <div className="w-full bg-background rounded-full h-1 overflow-hidden" />\n'
                '      <table>\n'
                '        <thead>\n'
                '          <tr>\n'
                '            <th className="py-2 px-3 text-left">CPU 부하율</th>\n'
                '          </tr>\n'
                '        </thead>\n'
                '        <tbody>\n'
                '          <tr>\n'
                '            <td className="text-left font-mono">84.2%</td>\n'
                '          </tr>\n'
                '        </tbody>\n'
                '      </table>\n'
                '    </div>\n'
                '  );\n'
                '}\n'
            )

        res_bad_telem = subprocess.run([sys.executable, linter_path, bad_telemetry], capture_output=True, text=True)
        # High-density patterns (max-width, numeric alignment, slender bar, truncate) are WARN design suggestions
        if "high-density-max-width-constraint" not in res_bad_telem.stdout:
            log("Linter failed to catch high-density-max-width-constraint in high-density file!", "FAIL")
            return False
        if "numeric-column-text-left" not in res_bad_telem.stdout:
            log("Linter failed to catch numeric-column-text-left in table header/cell!", "FAIL")
            return False
        if "indicator-too-slender" not in res_bad_telem.stdout:
            log("Linter failed to catch indicator-too-slender in high-density file!", "FAIL")
            return False
        if "critical-identifier-truncate" not in res_bad_telem.stdout:
            log("Linter failed to catch critical-identifier-truncate in high-density file!", "FAIL")
            return False

        # Run linter on good file (must pass with exit code 0)
        res_good = subprocess.run([sys.executable, linter_path, good_file], capture_output=True, text=True)
        if res_good.returncode != 0:
            log(f"Linter falsely flagged clean file:\n{res_good.stdout}", "FAIL")
            return False

        log("Linter correctly caught anti-patterns (max-w constraint, numeric text-left, slender indicator, critical identifier truncate, untokenized color) and passed clean code.", "PASS")
        return True
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def check_figma_sync():
    log("Verifying sync_figma.py nested grouping and deep merge...", "TEST")
    sys.path.insert(0, os.path.join(REPO_ROOT, "scripts"))
    temp_dir = tempfile.mkdtemp(prefix="figma_test_")
    try:
        import sync_figma
        target_tokens = os.path.join(temp_dir, "tokens")
        os.makedirs(target_tokens, exist_ok=True)
        with open(os.path.join(target_tokens, "colors.json"), "w", encoding="utf-8") as f:
            json.dump({"brand": {"primary": "#111111"}}, f)

        mock_payload = {
            "meta": {
                "variables": {
                    "v1": {
                        "name": "background/surface",
                        "resolvedType": "COLOR",
                        "valuesByMode": {"m1": {"r": 0.1, "g": 0.1, "b": 0.1, "a": 1.0}}
                    },
                    "v2": {
                        "name": "corner/radius/sm",
                        "resolvedType": "FLOAT",
                        "valuesByMode": {"m1": 4.0}
                    }
                }
            }
        }
        sync_figma.parse_and_sync(mock_payload, target_tokens)
        with open(os.path.join(target_tokens, "colors.json"), "r", encoding="utf-8") as f:
            colors = json.load(f)
        if colors.get("background", {}).get("surface") != "#1a1a1a":
            log("sync_figma failed to parse nested color structure!", "FAIL")
            return False
        if colors.get("brand", {}).get("primary") != "#111111":
            log("sync_figma failed to preserve pre-existing tokens during merge!", "FAIL")
            return False
        log("sync_figma.py nested token structuring and deep merge verified.", "PASS")
        return True
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def main():
    print("=" * 60)
    print("init-design-reference: Repository Integrity Test")
    print("=" * 60)

    checks = [
        check_python_syntax,
        check_json_tokens,
        check_required_templates,
        check_decoupled_architecture,
        check_scaffold_and_idempotency,
        check_linter_behavior,
        check_figma_sync
    ]


    all_passed = True
    for check in checks:
        if not check():
            all_passed = False
            break

    print("=" * 60)
    if all_passed:
        print("[SUMMARY] ALL INTEGRITY CHECKS PASSED.")
        sys.exit(0)
    else:
        print("[SUMMARY] INTEGRITY CHECKS FAILED.")
        sys.exit(1)

if __name__ == "__main__":
    main()
