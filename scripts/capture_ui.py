#!/usr/bin/env python3
"""
scripts/capture_ui.py - Headless Browser UI Capture & Runtime Console Auditor

Integrates with Microsoft Playwright (Apache License 2.0, Copyright (c) Microsoft Corporation)
to capture deterministic desktop & mobile screenshots and collect
console errors from local development servers (e.g. http://localhost:3000).
Enforces the visual feedback loop required to prevent generic AI style drift.
"""

import os
import sys
import json
import socket
import argparse
from datetime import datetime

def check_playwright_installed():
    try:
        import playwright
        return True
    except ImportError:
        return False

def detect_active_port(candidate_ports=None) -> int:
    """
    Probes candidate ports via TCP connection to detect active dev server.
    Defaults to 3000 if none detected.
    """
    if candidate_ports is None:
        candidate_ports = [3000, 5173, 8080, 4321, 8000]

    for port in candidate_ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.15)
                if s.connect_ex(("127.0.0.1", port)) == 0:
                    return port
        except Exception:
            continue
    return 3000

def capture_ui(url=None, output_dir="reference/screenshots/audit", allow_missing=False):
    if not url:
        port = detect_active_port()
        url = f"http://localhost:{port}"
        print(f"Auto-detected active dev server on port {port}: {url}")
    if not check_playwright_installed():
        print("\n==================================================================", file=sys.stderr)
        print("[ACTION REQUIRED] Playwright is not installed in the current environment.", file=sys.stderr)
        print("To close the visual feedback loop and enable vision verification, install Playwright:", file=sys.stderr)
        print("  pip install playwright", file=sys.stderr)
        print("  npx playwright install chromium", file=sys.stderr)
        print("==================================================================\n", file=sys.stderr)
        if allow_missing:
            print("Notice: --allow-missing specified. Skipping headless capture.")
            return 0
        return 1

    from playwright.sync_api import sync_playwright

    os.makedirs(output_dir, exist_ok=True)
    console_logs = []
    page_errors = []

    print(f"Connecting to development server at: {url}")
    try:
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)
            except Exception as e:
                print("\n==================================================================", file=sys.stderr)
                print(f"[ACTION REQUIRED] Chromium binary missing: {e}", file=sys.stderr)
                print("Run: npx playwright install chromium", file=sys.stderr)
                print("==================================================================\n", file=sys.stderr)
                if allow_missing:
                    return 0
                return 1

            # 1. Desktop Viewport (1440x900)
            context_desktop = browser.new_context(viewport={"width": 1440, "height": 900})
            page_desktop = context_desktop.new_page()

            page_desktop.on("console", lambda msg: console_logs.append({"type": msg.type, "text": msg.text}))
            page_desktop.on("pageerror", lambda err: page_errors.append(str(err)))

            print("Capturing Desktop viewport (1440x900)...")
            page_desktop.goto(url, wait_until="networkidle", timeout=15000)
            desktop_path = os.path.join(output_dir, "desktop_1440.png")
            page_desktop.screenshot(path=desktop_path, full_page=True)
            print(f"Saved: {desktop_path}")
            context_desktop.close()

            # 2. Mobile Viewport (375x812 - iPhone 13/Mini scale)
            context_mobile = browser.new_context(viewport={"width": 375, "height": 812}, is_mobile=True)
            page_mobile = context_mobile.new_page()

            print("Capturing Mobile viewport (375x812)...")
            page_mobile.goto(url, wait_until="networkidle", timeout=15000)
            mobile_path = os.path.join(output_dir, "mobile_375.png")
            page_mobile.screenshot(path=mobile_path, full_page=True)
            print(f"Saved: {mobile_path}")
            context_mobile.close()

            browser.close()

    except Exception as e:
        print(f"Error during UI capture: {e}", file=sys.stderr)
        print("Ensure local development server is running and accessible.", file=sys.stderr)
        if allow_missing:
            return 0
        return 1

    # Dump logs
    log_file = os.path.join(output_dir, "console_audit.json")
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.utcnow().isoformat(),
            "url": url,
            "errors": page_errors,
            "logs": console_logs
        }, f, indent=2)
    print(f"Saved console audit: {log_file}")

    if page_errors:
        print(f"Warning: {len(page_errors)} uncaught page errors detected during render!", file=sys.stderr)
        for err in page_errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("Headless visual capture complete. Ready for vision inspection.")
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Headless Browser UI Capture & Auditor")
    parser.add_argument("--url", default=None, help="Target URL (default: auto-detected localhost port)")
    parser.add_argument("--output", default="reference/screenshots/audit", help="Output directory for screenshots")
    parser.add_argument("--allow-missing", action="store_true", help="Do not exit with error if Playwright/server is unavailable")
    args = parser.parse_args()

    sys.exit(capture_ui(args.url, args.output, args.allow_missing))
