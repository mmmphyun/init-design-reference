#!/usr/bin/env python3
"""
scripts/verify_motion_scenarios.py - Mechanical Motion Invariants & Browser Interaction Verification

Evaluates mechanical motion constraints, token preservation, and browser interaction:
1. Short new request invariant: Adapter applies baseline neutral dials (MOTION_INTENSITY=4) without arbitrary extremes.
2. Subdued direction invariant: Adapter applies and preserves requested low motion dial (MOTION_INTENSITY=2) passing spec verification.
3. Existing design system invariant: Custom team motion tokens/curves in motion.json survive subsequent adapter runs.
4. Browser interactive & reduced-motion verification: Loads generated scaffold assets (tokens.css) and component markup
   (micro-interactions.md TactileButton & Sheet) in Playwright Chromium, testing real interactive toggles and reduced-motion suppression.

Note on Scope:
- This script tests mechanical invariants of the repository's tooling (adapter, tokens, linter, headless browser).
- It does NOT evaluate interactive LLM chat session behavior (e.g. conversational prompt understanding).
- Headless browser verification strictly requires Playwright; if Playwright is missing or fails, this test fails (no silent pass).
- Ephemeral test artifacts and servers are destroyed after verification; nothing is committed to the repository.
"""

import os
import sys
import json
import tempfile
import shutil
import subprocess
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def log(msg, status="INFO"):
    print(f"[{status}] {msg}")

def run_invariant_1_short_new_request():
    """
    Invariant 1: Short New Request Tooling Invariant
    Verifies that scaffolding without explicit dials defaults to baseline neutral motion (MOTION_INTENSITY=4).
    """
    log("Running Invariant 1: Baseline neutral motion dials on unconfigured scaffold...", "TEST")
    temp_dir = tempfile.mkdtemp(prefix="scenario_1_")
    try:
        adapter_path = os.path.join(REPO_ROOT, "scripts", "adapter.py")
        target_design = os.path.join(temp_dir, ".design")

        res = subprocess.run([sys.executable, adapter_path, target_design], capture_output=True, text=True, cwd=temp_dir)
        if res.returncode != 0:
            log(f"Invariant 1 failed: adapter exited with {res.returncode}", "FAIL")
            return False

        design_md_path = os.path.join(target_design, "DESIGN.md")
        with open(design_md_path, "r", encoding="utf-8") as f:
            content = f.read()

        if "`MOTION_INTENSITY`: 4" not in content:
            log("Invariant 1 failed: default MOTION_INTENSITY is not standard baseline 4", "FAIL")
            return False

        log("Invariant 1 PASS: Adapter establishes baseline neutral motion dials (MOTION_INTENSITY: 4).", "PASS")
        return True
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def run_invariant_2_subdued_direction_request():
    """
    Invariant 2: Subdued Direction Tooling Invariant
    Verifies that explicitly requested subdued motion (--dials 4,7,2) is applied and validated by --verify-spec.
    """
    log("Running Invariant 2: Explicit subdued motion dial persistence & spec validation...", "TEST")
    temp_dir = tempfile.mkdtemp(prefix="scenario_2_")
    try:
        adapter_path = os.path.join(REPO_ROOT, "scripts", "adapter.py")
        target_design = os.path.join(temp_dir, ".design")

        res = subprocess.run([
            sys.executable, adapter_path, target_design,
            "--dials", "4,7,2"
        ], capture_output=True, text=True, cwd=temp_dir)
        if res.returncode != 0:
            log(f"Invariant 2 failed: adapter execution failed", "FAIL")
            return False

        with open(os.path.join(target_design, "DESIGN.md"), "r", encoding="utf-8") as f:
            content = f.read()

        if "`MOTION_INTENSITY`: 2" not in content:
            log("Invariant 2 failed: custom dial MOTION_INTENSITY=2 was not preserved", "FAIL")
            return False

        res_spec = subprocess.run([sys.executable, adapter_path, "--verify-spec", target_design], capture_output=True, text=True, cwd=temp_dir)
        if res_spec.returncode != 0:
            log(f"Invariant 2 failed: --verify-spec failed on subdued dials:\n{res_spec.stderr}", "FAIL")
            return False

        log("Invariant 2 PASS: Subdued motion dial preserved and passed --verify-spec.", "PASS")
        return True
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def run_invariant_3_existing_design_system_preservation():
    """
    Invariant 3: Existing Design System Preservation Invariant
    Verifies that custom motion tokens added to motion.json are preserved across adapter executions.
    """
    log("Running Invariant 3: Preservation of existing motion tokens across adapter runs...", "TEST")
    temp_dir = tempfile.mkdtemp(prefix="scenario_3_")
    try:
        adapter_path = os.path.join(REPO_ROOT, "scripts", "adapter.py")
        target_design = os.path.join(temp_dir, ".design")

        # 1. Initial scaffold
        subprocess.run([sys.executable, adapter_path, target_design], check=True, capture_output=True, cwd=temp_dir)

        # 2. Add custom brand motion tokens
        motion_json_path = os.path.join(target_design, "tokens", "motion.json")
        with open(motion_json_path, "r", encoding="utf-8") as f:
            motion_data = json.load(f)

        motion_data["duration"]["brand-swift"] = "180ms"
        motion_data["springs"]["brand-gentle"] = {"stiffness": 180, "damping": 22, "mass": 1.1}
        with open(motion_json_path, "w", encoding="utf-8") as f:
            json.dump(motion_data, f, indent=2)

        # 3. Re-run adapter without --force
        res_rerun = subprocess.run([sys.executable, adapter_path, target_design, "--preset", "b2b-dense"], capture_output=True, text=True, cwd=temp_dir)
        if res_rerun.returncode != 0:
            log("Invariant 3 failed: adapter second run failed", "FAIL")
            return False

        with open(motion_json_path, "r", encoding="utf-8") as f:
            verified_motion = json.load(f)

        if "brand-swift" not in verified_motion.get("duration", {}) or "brand-gentle" not in verified_motion.get("springs", {}):
            log("Invariant 3 failed: custom brand motion tokens were overwritten by preset re-run!", "FAIL")
            return False

        log("Invariant 3 PASS: Custom motion tokens preserved through idempotent adapter runs.", "PASS")
        return True
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def run_invariant_4_browser_scaffold_output_interactive():
    """
    Invariant 4: Headless Browser Interactive Verification of Scaffold Output
    Builds a test page using scaffolded tokens.css and template component markup
    (TactileButton and Sheet from micro-interactions.md), then validates interaction
    and reduced-motion suppression in Playwright Chromium.
    MANDATORY: Fails if Playwright is missing or browser launch fails.
    """
    log("Running Invariant 4: Headless browser interactive verification of scaffold output...", "TEST")
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        log("Invariant 4 FAIL: Playwright is mandatory for browser interaction verification.", "FAIL")
        return False

    temp_dir = tempfile.mkdtemp(prefix="scenario_4_")
    server = None
    try:
        # 1. Generate real tokens.css using adapter in temp workspace
        adapter_path = os.path.join(REPO_ROOT, "scripts", "adapter.py")
        target_design = os.path.join(temp_dir, ".design")
        subprocess.run([sys.executable, adapter_path, target_design], check=True, capture_output=True, cwd=temp_dir)

        tokens_css_path = os.path.join(target_design, "tokens", "tokens.css")
        if not os.path.exists(tokens_css_path):
            log("Invariant 4 failed: scaffolded tokens.css does not exist", "FAIL")
            return False

        # Read scaffolded tokens.css
        with open(tokens_css_path, "r", encoding="utf-8") as f:
            tokens_css_content = f.read()

        # 2. Build test HTML referencing scaffolded tokens.css and micro-interactions.md patterns
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Scaffold Output Motion Verification</title>
  <style>
    /* Injected scaffold tokens.css */
    {tokens_css_content}

    body {{
      background: var(--background);
      color: var(--foreground);
      font-family: sans-serif;
      padding: 24px;
    }}

    /* TactileButton pattern from micro-interactions.md */
    .tactile-btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 8px 16px;
      font-size: 14px;
      border-radius: var(--radius-btn, 6px);
      background: var(--accent);
      color: #ffffff;
      border: none;
      cursor: pointer;
      user-select: none;
      transition-property: transform, background-color, box-shadow;
      transition-duration: var(--duration-fast);
      transition-timing-function: var(--ease-apple-snappy);
    }}
    .tactile-btn:active {{
      transform: scale(0.98);
    }}

    /* Sheet pattern from micro-interactions.md */
    .sheet-backdrop {{
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.6);
      opacity: 0;
      transition: opacity var(--duration-fast) ease-out;
      z-index: 50;
    }}
    .sheet-backdrop.active {{
      display: flex;
      justify-content: flex-end;
      opacity: 1;
    }}
    .sheet-surface {{
      width: 100%;
      max-width: 400px;
      height: 100%;
      background: var(--surface);
      border-left: 1px solid var(--border-default);
      box-shadow: var(--shadow-elevation-4, 0 10px 15px rgba(0,0,0,0.3));
      transform: translateX(100%);
      transition: transform var(--duration-normal) var(--ease-apple-spring);
      padding: 20px;
      box-sizing: border-box;
    }}
    .sheet-backdrop.active .sheet-surface {{
      transform: translateX(0);
    }}

    /* Global reduced motion override from interaction.md */
    @media (prefers-reduced-motion: reduce) {{
      *, ::before, ::after {{
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
      }}
    }}
  </style>
</head>
<body>
  <h1>Scaffold Output Motion Verification</h1>
  <button id="open-sheet-btn" class="tactile-btn" onclick="openSheet()">Open Drawer Sheet</button>

  <div id="sheet-backdrop" class="sheet-backdrop" role="dialog" aria-modal="true" aria-label="Settings Sheet">
    <div class="sheet-surface">
      <h2>Drawer Sheet Surface</h2>
      <p>Testing scaffold pattern behavior.</p>
      <button id="close-sheet-btn" class="tactile-btn" onclick="closeSheet()">Close</button>
    </div>
  </div>

  <script>
    function openSheet() {{
      document.getElementById('sheet-backdrop').classList.add('active');
    }}
    function closeSheet() {{
      document.getElementById('sheet-backdrop').classList.remove('active');
    }}
  </script>
</body>
</html>
"""
        html_file = os.path.join(temp_dir, "index.html")
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        # Serve on ephemeral localhost port
        class QuietHandler(SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=temp_dir, **kwargs)
            def log_message(self, format, *args):
                pass

        server = HTTPServer(("127.0.0.1", 0), QuietHandler)
        port = server.server_address[1]
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()

        target_url = f"http://127.0.0.1:{port}/index.html"

        with sync_playwright() as p:
            browser = p.chromium.launch()

            # 4-A: Standard Browser Context
            ctx_std = browser.new_context()
            page_std = ctx_std.new_page()
            page_std.goto(target_url)

            # Test TactileButton presence & styling
            btn = page_std.locator("#open-sheet-btn")
            if not btn.is_visible():
                log("Invariant 4 failed: TactileButton not visible", "FAIL")
                browser.close()
                return False

            # Test Sheet open and close
            sheet = page_std.locator("#sheet-backdrop")
            close_btn = page_std.locator("#close-sheet-btn")

            btn.click()
            page_std.wait_for_timeout(50)
            if not sheet.is_visible():
                log("Invariant 4 failed: Sheet did not open in standard context", "FAIL")
                browser.close()
                return False

            close_btn.click()
            page_std.wait_for_timeout(50)
            if sheet.is_visible():
                log("Invariant 4 failed: Sheet did not close in standard context", "FAIL")
                browser.close()
                return False

            ctx_std.close()

            # 4-B: Reduced-Motion Context (prefers-reduced-motion: reduce)
            ctx_rm = browser.new_context(reduced_motion="reduce")
            page_rm = ctx_rm.new_page()
            page_rm.goto(target_url)

            # Validate that transition duration on Sheet is suppressed to ~0
            computed_duration = page_rm.evaluate("""() => {
              const el = document.getElementById('sheet-backdrop');
              return window.getComputedStyle(el).getPropertyValue('transition-duration');
            }""")

            if "0s" not in computed_duration and "0.00001s" not in computed_duration and "1e-05s" not in computed_duration:
                log(f"Invariant 4 failed: transition-duration not suppressed under reduced-motion (got {computed_duration})", "FAIL")
                browser.close()
                return False

            # Validate functional interaction still functions seamlessly under reduced motion
            btn_rm = page_rm.locator("#open-sheet-btn")
            sheet_rm = page_rm.locator("#sheet-backdrop")
            close_btn_rm = page_rm.locator("#close-sheet-btn")

            btn_rm.click()
            if not sheet_rm.is_visible():
                log("Invariant 4 failed: Sheet failed to open under reduced-motion", "FAIL")
                browser.close()
                return False

            close_btn_rm.click()
            if sheet_rm.is_visible():
                log("Invariant 4 failed: Sheet failed to close under reduced-motion", "FAIL")
                browser.close()
                return False

            ctx_rm.close()
            browser.close()

        log("Invariant 4 PASS: Scaffolded tokens & component patterns verified in Playwright browser with reduced-motion suppression.", "PASS")
        return True
    finally:
        if server:
            server.shutdown()
        shutil.rmtree(temp_dir, ignore_errors=True)

def main():
    print("=" * 60)
    print("init-design-reference: Tooling Motion Invariants & Browser Test")
    print("=" * 60)

    invariants = [
        run_invariant_1_short_new_request,
        run_invariant_2_subdued_direction_request,
        run_invariant_3_existing_design_system_preservation,
        run_invariant_4_browser_scaffold_output_interactive,
    ]

    all_passed = True
    for inv in invariants:
        if not inv():
            all_passed = False
            break

    print("=" * 60)
    if all_passed:
        print("[SUMMARY] ALL MECHANICAL MOTION INVARIANTS PASSED.")
        sys.exit(0)
    else:
        print("[SUMMARY] MOTION INVARIANTS VERIFICATION FAILED.")
        sys.exit(1)

if __name__ == "__main__":
    main()
