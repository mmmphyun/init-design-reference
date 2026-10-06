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
        target_ref = os.path.join(temp_dir, "reference")

        # 1st run with preset: must create all files
        run1 = subprocess.run([sys.executable, adapter_path, target_ref, "--preset", "b2b-dense"], capture_output=True, text=True, cwd=temp_dir)
        if run1.returncode != 0:
            log(f"First run failed with code {run1.returncode}:\n{run1.stderr}", "FAIL")
            return False

        if "Created:" not in run1.stdout:
            log("First run did not report created files.", "FAIL")
            return False

        # Verify pattern files exist in target
        expected_pattern = os.path.join(target_ref, "patterns", "data-display.md")
        if not os.path.exists(expected_pattern):
            log(f"Pattern file not created: {expected_pattern}", "FAIL")
            return False

        # 2nd run: must skip existing files (idempotency)
        run2 = subprocess.run([sys.executable, adapter_path, target_ref], capture_output=True, text=True, cwd=temp_dir)
        if run2.returncode != 0:
            log(f"Second run failed with code {run2.returncode}:\n{run2.stderr}", "FAIL")
            return False

        if "Created:" in run2.stdout or "Skipped existing:" not in run2.stdout:
            log("Idempotency violated: second run modified or recreated files.", "FAIL")
            return False

        # 3rd run with --force: must overwrite
        run3 = subprocess.run([sys.executable, adapter_path, target_ref, "--force"], capture_output=True, text=True, cwd=temp_dir)
        if run3.returncode != 0:
            log(f"Force run failed with code {run3.returncode}:\n{run3.stderr}", "FAIL")
            return False

        if "Created:" not in run3.stdout:
            log("Force flag violated: did not report recreated files.", "FAIL")
            return False

        log("Scaffolding, idempotency, preset, and force overwrite verified.", "PASS")
        return True
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def check_linter_behavior():
    log("Verifying lint_ui.py detector behavior...", "TEST")
    linter_path = os.path.join(REPO_ROOT, "scripts", "lint_ui.py")
    temp_dir = tempfile.mkdtemp(prefix="lint_test_")

    try:
        # Create a file with a deliberate AI cliché (uppercase tracking-widest)
        bad_file = os.path.join(temp_dir, "bad_component.tsx")
        with open(bad_file, "w", encoding="utf-8") as f:
            f.write('<span className="uppercase tracking-widest text-[#6366f1]">BAD</span>\n')

        # Create a clean file
        good_file = os.path.join(temp_dir, "good_component.tsx")
        with open(good_file, "w", encoding="utf-8") as f:
            f.write('<span className="text-sm font-medium text-foreground">GOOD</span>\n')

        # Run linter on bad file (must fail with exit code 1)
        res_bad = subprocess.run([sys.executable, linter_path, bad_file], capture_output=True, text=True)
        if res_bad.returncode == 0 or "hardcoded-hex" not in res_bad.stdout:
            log("Linter failed to catch intentional hardcoded hex / cliché!", "FAIL")
            return False

        # Run linter on good file (must pass with exit code 0)
        res_good = subprocess.run([sys.executable, linter_path, good_file], capture_output=True, text=True)
        if res_good.returncode != 0:
            log(f"Linter falsely flagged clean file:\n{res_good.stdout}", "FAIL")
            return False

        log("Linter correctly caught anti-patterns and passed clean code.", "PASS")
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
        check_linter_behavior
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
