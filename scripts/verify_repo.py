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
        # Test dynamic status alpha derivation in CSS bridge (including 4-digit, 8-digit, background & border HEX)
        tokens_json_path = os.path.join(target_design, "tokens", "colors.json")
        with open(tokens_json_path, "r", encoding="utf-8") as f:
            c_data = json.load(f)
        c_data.setdefault("status", {})["error"] = "#f00f"  # 4-digit hex (#RGBA)
        c_data.setdefault("status", {})["warning"] = "#00ff00aa"  # 8-digit hex (#RRGGBBAA)
        with open(tokens_json_path, "w", encoding="utf-8") as f:
            json.dump(c_data, f, indent=2)

        run_bridge2 = subprocess.run([sys.executable, adapter_path, target_design, "--bridge-only"], capture_output=True, text=True, cwd=temp_dir)
        if run_bridge2.returncode != 0:
            log(f"--bridge-only with custom status failed:\n{run_bridge2.stderr}", "FAIL")
            return False

        with open(tokens_css_path, "r", encoding="utf-8") as f:
            t_css_custom = f.read()
        if "--status-error-bg: rgba(255, 0, 0, 0.12);" not in t_css_custom:
            log(f"Dynamic status alpha derivation failed for 4-digit hex #f00f (bg)! Got:\n{t_css_custom}", "FAIL")
            return False
        if "--status-error-border: rgba(255, 0, 0, 0.25);" not in t_css_custom:
            log(f"Dynamic status alpha derivation failed for 4-digit hex #f00f (border)! Got:\n{t_css_custom}", "FAIL")
            return False
        if "--status-warning-bg: rgba(0, 255, 0, 0.12);" not in t_css_custom:
            log(f"Dynamic status alpha derivation failed for 8-digit hex #00ff00aa (bg)! Got:\n{t_css_custom}", "FAIL")
            return False
        if "--status-warning-border: rgba(0, 255, 0, 0.25);" not in t_css_custom:
            log(f"Dynamic status alpha derivation failed for 8-digit hex #00ff00aa (border)! Got:\n{t_css_custom}", "FAIL")
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

def check_css_bridge_completeness():
    log("Verifying complete token export to CSS/Tailwind bridges (spacing & typography roles)...", "TEST")
    temp_dir = tempfile.mkdtemp(prefix="bridge_test_")
    try:
        sys.path.insert(0, os.path.join(REPO_ROOT, "scripts"))
        import adapter
        target_design = os.path.join(temp_dir, ".design")
        adapter.scaffold_reference(target_design, preset="default")

        # 1. tokens.css validation
        tokens_css_path = os.path.join(target_design, "tokens", "tokens.css")
        with open(tokens_css_path, "r", encoding="utf-8") as f:
            tokens_css = f.read()
        for token in ["--space-md:", "--gutter-desktop:", "--text-page-title-size:", "--text-body-line-height:"]:
            if token not in tokens_css:
                log(f"tokens.css missing expected token '{token}'!", "FAIL")
                return False

        # 2. Tailwind v4 theme.css validation
        adapter.generate_css_bridges(target_design, "tailwind-v4", force=True)
        theme_css_path = os.path.join(target_design, "tokens", "theme.css")
        with open(theme_css_path, "r", encoding="utf-8") as f:
            theme_css = f.read()
        for token in ["--spacing-md:", "--font-size-page-title:", "--letter-spacing-page-title:"]:
            if token not in theme_css:
                log(f"theme.css missing expected Tailwind v4 token '{token}'!", "FAIL")
                return False

        # 3. Tailwind v3 tailwind.preset.js validation
        adapter.generate_css_bridges(target_design, "tailwind-v3", force=True)
        preset_js_path = os.path.join(target_design, "tokens", "tailwind.preset.js")
        with open(preset_js_path, "r", encoding="utf-8") as f:
            preset_js = f.read()
        for token in ['spacing: {', 'fontSize: {', '"page-title":']:
            if token not in preset_js:
                log(f"tailwind.preset.js missing expected Tailwind v3 section '{token}'!", "FAIL")
                return False

        log("CSS/Tailwind bridge completeness (colors, spacing, typography roles, radii, shadows, motion) verified.", "PASS")
        return True
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def check_css_path_resolution():
    log("Verifying deterministic CSS integration path resolution...", "TEST")
    temp_dir = tempfile.mkdtemp(prefix="path_test_")
    try:
        sys.path.insert(0, os.path.join(REPO_ROOT, "scripts"))
        import adapter

        # Scenario 1: Standard src/index.css in root
        os.makedirs(os.path.join(temp_dir, "src"), exist_ok=True)
        css_file = os.path.join(temp_dir, "src", "index.css")
        with open(css_file, "w") as f: f.write("/* root */")
        p1 = adapter.resolve_css_integration_paths(temp_dir, os.path.join(temp_dir, ".design"))
        if p1["import_theme"] != "../.design/tokens/theme.css" or p1["is_inferred"]:
            log(f"Path resolution failed for root src/index.css: {p1}", "FAIL")
            return False

        # Scenario 2: Monorepo subproject apps/web/src/index.css
        sub_src = os.path.join(temp_dir, "apps", "web", "src")
        os.makedirs(sub_src, exist_ok=True)
        with open(os.path.join(sub_src, "index.css"), "w") as f: f.write("/* mono */")
        p2 = adapter.resolve_css_integration_paths(temp_dir, os.path.join(temp_dir, ".design"), subproject_dir="apps/web")
        if p2["import_theme"] != "../../../.design/tokens/theme.css" or p2["is_inferred"]:
            log(f"Path resolution failed for monorepo subproject: {p2}", "FAIL")
            return False

        # Scenario 3: Non-standard CSS name via shallow scan
        custom_dir = os.path.join(temp_dir, "custom_app", "styles")
        os.makedirs(custom_dir, exist_ok=True)
        with open(os.path.join(custom_dir, "custom.css"), "w") as f: f.write("/* custom */")
        p3 = adapter.resolve_css_integration_paths(temp_dir, os.path.join(temp_dir, ".design"), subproject_dir="custom_app")
        if p3["is_inferred"] or not p3["import_theme"].endswith(".design/tokens/theme.css"):
            log(f"Path resolution failed for custom CSS scan: {p3}", "FAIL")
            return False

        log("Deterministic CSS integration path resolution verified across standard, monorepo, and custom structures.", "PASS")
        return True
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def check_workspace_framework_and_css_resolution():
    log("Verifying workspace monorepo, framework detection, and ambiguous CSS resolution...", "TEST")
    sys.path.insert(0, os.path.join(REPO_ROOT, "scripts"))
    import adapter

    temp_dir = tempfile.mkdtemp(prefix="ws_fw_test_")
    try:
        # 1. Framework detection checks (React, Next.js, Vue, Nuxt, Svelte, SvelteKit, Vite separation, Vanilla)
        test_cases = [
            ({"next": "^14.0.0"}, "nextjs", None),
            ({"react": "^18.0.0"}, "react", None),
            ({"nuxt": "^3.0.0"}, "nuxt", None),
            ({"vue": "^3.3.0"}, "vue", None),
            ({"@sveltejs/kit": "^2.0.0"}, "sveltekit", None),
            ({"svelte": "^4.0.0"}, "svelte", None),
            ({"react": "^18.0.0", "vite": "^5.0.0"}, "react", "vite"),
            ({"vite": "^5.0.0"}, "unknown", "vite"),
            ({}, "unknown", None),
        ]

        for deps, expected_fw, expected_bt in test_cases:
            case_dir = os.path.join(temp_dir, f"case_{expected_fw}_{expected_bt}")
            os.makedirs(case_dir, exist_ok=True)
            with open(os.path.join(case_dir, "package.json"), "w", encoding="utf-8") as f:
                json.dump({"dependencies": deps}, f)
            ctx = adapter.detect_project_context(base_dir=case_dir)
            if ctx["framework"] != expected_fw:
                log(f"Framework detection mismatch for deps {deps}: expected {expected_fw}, got {ctx['framework']}", "FAIL")
                return False
            if ctx["build_tool"] != expected_bt:
                log(f"Build tool detection mismatch for deps {deps}: expected {expected_bt}, got {ctx['build_tool']}", "FAIL")
                return False

        # 2. Workspace Monorepo: Root package.json with multiple sub-apps (apps/web, apps/docs)
        mono_dir = os.path.join(temp_dir, "monorepo")
        os.makedirs(mono_dir, exist_ok=True)
        with open(os.path.join(mono_dir, "package.json"), "w", encoding="utf-8") as f:
            json.dump({"name": "mono-root", "workspaces": ["apps/*"]}, f)

        web_dir = os.path.join(mono_dir, "apps", "web")
        docs_dir = os.path.join(mono_dir, "apps", "docs")
        os.makedirs(os.path.join(web_dir, "src"), exist_ok=True)
        os.makedirs(os.path.join(docs_dir, "assets"), exist_ok=True)

        with open(os.path.join(web_dir, "package.json"), "w", encoding="utf-8") as f:
            json.dump({"name": "web", "dependencies": {"next": "^14.0.0", "tailwindcss": "^3.4.0"}}, f)
        with open(os.path.join(docs_dir, "package.json"), "w", encoding="utf-8") as f:
            json.dump({"name": "docs", "dependencies": {"nuxt": "^3.0.0"}}, f)

        # Multiple apps without explicit --app: must detect ambiguity without arbitrary selection
        mono_ctx = adapter.detect_project_context(base_dir=mono_dir)
        if len(mono_ctx["ambiguous_apps"]) < 2:
            log(f"Monorepo failed to report ambiguous apps: {mono_ctx}", "FAIL")
            return False

        # Targeting specific app via app_dir
        web_ctx = adapter.detect_project_context(base_dir=mono_dir, app_dir="apps/web")
        if web_ctx["framework"] != "nextjs" or web_ctx["subproject_dir"] != "apps/web":
            log(f"Targeting apps/web failed: {web_ctx}", "FAIL")
            return False

        # 2-b. Hoisted Tailwind in root + Next.js only in subproject + tailwind.config.js in subproject
        hoist_mono = os.path.join(temp_dir, "hoist_monorepo")
        os.makedirs(os.path.join(hoist_mono, "apps", "web"), exist_ok=True)
        with open(os.path.join(hoist_mono, "package.json"), "w", encoding="utf-8") as f:
            json.dump({"name": "hoist-root", "devDependencies": {"tailwindcss": "^3.4.1"}}, f)
        with open(os.path.join(hoist_mono, "apps", "web", "package.json"), "w", encoding="utf-8") as f:
            json.dump({"name": "web-app", "dependencies": {"next": "^14.0.0"}}, f)
        with open(os.path.join(hoist_mono, "apps", "web", "tailwind.config.js"), "w", encoding="utf-8") as f:
            f.write("module.exports = {};")

        hoist_ctx = adapter.detect_project_context(base_dir=hoist_mono, app_dir="apps/web")
        if hoist_ctx["framework"] != "nextjs":
            log(f"Hoisted mono framework detection failed: expected 'nextjs', got '{hoist_ctx['framework']}'", "FAIL")
            return False
        if hoist_ctx["style_engine"] != "tailwind-v3":
            log(f"Hoisted mono style_engine detection failed: expected 'tailwind-v3', got '{hoist_ctx['style_engine']}'", "FAIL")
            return False

        # 3. Multiple CSS candidates: detecting ambiguity vs explicit override
        with open(os.path.join(web_dir, "src", "index.css"), "w") as f: f.write("/* 1 */")
        with open(os.path.join(web_dir, "src", "main.css"), "w") as f: f.write("/* 2 */")

        target_design = os.path.join(mono_dir, ".design")
        paths_ambig = adapter.resolve_css_integration_paths(mono_dir, target_design, subproject_dir="apps/web")
        if not paths_ambig["ambiguous"] or len(paths_ambig["candidates"]) != 2:
            log(f"Multiple CSS candidates not flagged as ambiguous: {paths_ambig}", "FAIL")
            return False

        # Explicit CSS path override: must resolve deterministically without ambiguity
        paths_explicit = adapter.resolve_css_integration_paths(
            mono_dir, target_design, subproject_dir="apps/web", custom_css="apps/web/src/main.css"
        )
        if paths_explicit["ambiguous"] or paths_explicit["display_entry"] != "apps/web/src/main.css":
            log(f"Explicit CSS override failed: {paths_explicit}", "FAIL")
            return False

        # 4. Non-standard CSS location & Tailwind config dir separation
        deep_css_dir = os.path.join(web_dir, "src", "styles", "deep")
        os.makedirs(deep_css_dir, exist_ok=True)
        deep_css_file = os.path.join(deep_css_dir, "app.css")
        with open(deep_css_file, "w") as f: f.write("/* deep */")
        with open(os.path.join(web_dir, "tailwind.config.js"), "w") as f: f.write("module.exports = {};")

        paths_separated = adapter.resolve_css_integration_paths(
            mono_dir, target_design, subproject_dir="apps/web", custom_css=deep_css_file
        )
        # tailwind config is at apps/web -> relative preset path should be "../../.design/tokens/tailwind.preset.js"
        # css is at apps/web/src/styles/deep -> relative theme path should be "../../../../../.design/tokens/theme.css"
        if paths_separated["import_preset"] != "../../.design/tokens/tailwind.preset.js":
            log(f"Relative preset path calculation incorrect: {paths_separated['import_preset']}", "FAIL")
            return False
        if paths_separated["import_theme"] != "../../../../../.design/tokens/theme.css":
            log(f"Relative theme path calculation incorrect: {paths_separated['import_theme']}", "FAIL")
            return False

        # 5. CLI end-to-end execution with --app and --css options
        adapter_path = os.path.join(REPO_ROOT, "scripts", "adapter.py")
        run_res = subprocess.run([
            sys.executable, adapter_path, target_design,
            "--app", "apps/web",
            "--css", "apps/web/src/styles/deep/app.css"
        ], capture_output=True, text=True, cwd=mono_dir)
        if run_res.returncode != 0:
            log(f"CLI adapter run with --app and --css failed:\n{run_res.stderr}", "FAIL")
            return False
        if "Framework=nextjs" not in run_res.stdout or "apps/web/src/styles/deep/app.css" not in run_res.stdout:
            log(f"CLI output missing framework or custom css entrypoint:\n{run_res.stdout}", "FAIL")
            return False

        log("Workspace monorepo, framework detection, and ambiguous CSS resolution verified.", "PASS")
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
        check_figma_sync,
        check_css_bridge_completeness,
        check_css_path_resolution,
        check_workspace_framework_and_css_resolution
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
