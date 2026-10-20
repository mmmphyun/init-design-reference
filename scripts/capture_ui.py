#!/usr/bin/env python3
"""
scripts/capture_ui.py - Headless Browser UI Capture & Deterministic UX/A11y Auditor

Integrates with Microsoft Playwright (Apache License 2.0, Microsoft Corp),
plugin87/ux-ui-agent-skills (MIT License, plugin87), and
pbakaus/impeccable (Apache-2.0, Paul Bakaus) to capture viewports,
measure real computed contrast, target sizes (WCAG 2.2), horizontal overflow,
and issue a cryptographic audit receipt (`ux_audit_receipt.json`).
"""

import os
import sys
import json
import socket
import hashlib
import argparse
from datetime import datetime

DOM_UX_AUDIT_JS = r"""
() => {
    const findings = [];
    let passedCount = 0;

    // Helper: Parse rgba string to [r, g, b, a]
    function parseRgba(str) {
        if (!str || str === 'transparent') return [0, 0, 0, 0];
        const m = str.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)/);
        if (m) {
            return [parseInt(m[1]), parseInt(m[2]), parseInt(m[3]), m[4] !== undefined ? parseFloat(m[4]) : 1.0];
        }
        return [0, 0, 0, 1];
    }

    // Helper: Composite fg over bg
    function blend(fg, bg) {
        const a = fg[3] + bg[3] * (1 - fg[3]);
        if (a === 0) return [255, 255, 255, 1];
        const r = Math.round((fg[0] * fg[3] + bg[0] * bg[3] * (1 - fg[3])) / a);
        const g = Math.round((fg[1] * fg[3] + bg[1] * bg[3] * (1 - fg[3])) / a);
        const b = Math.round((fg[2] * fg[3] + bg[2] * bg[3] * (1 - fg[3])) / a);
        return [r, g, b, a];
    }

    // Helper: Relative luminance
    function luminance(r, g, b) {
        const a = [r, g, b].map(v => {
            v /= 255;
            return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
        });
        return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722;
    }

    // Helper: Contrast ratio
    function contrastRatio(rgb1, rgb2) {
        const lum1 = luminance(rgb1[0], rgb1[1], rgb1[2]);
        const lum2 = luminance(rgb2[0], rgb2[1], rgb2[2]);
        const brightest = Math.max(lum1, lum2);
        const darkest = Math.min(lum1, lum2);
        return (brightest + 0.05) / (darkest + 0.05);
    }

    // 1. Horizontal Overflow Reflow Gate (plugin87 verify_overflow / impeccable audit)
    const docEl = document.documentElement;
    const body = document.body;
    const scrollWidth = Math.max(docEl.scrollWidth, body ? body.scrollWidth : 0);
    const clientWidth = docEl.clientWidth;
    if (scrollWidth > clientWidth + 2) {
        findings.push({
            rule_id: "ux-horizontal-overflow",
            severity: "ERROR",
            selector: "html",
            message: `Horizontal overflow detected: content width (${scrollWidth}px) exceeds viewport width (${clientWidth}px). Fix unconstrained widths or margin overflows.`,
            value: `${scrollWidth}px > ${clientWidth}px`
        });
    } else {
        passedCount++;
    }

    // 2. Interactive Target Size Gate (WCAG 2.2 SC 2.5.8 - plugin87 verify_target_size)
    const interactives = document.querySelectorAll('button, a, input, select, textarea, [role="button"], [role="tab"], [role="checkbox"], [role="switch"]');
    interactives.forEach(el => {
        // Skip hidden, disabled, or display:none elements
        if (el.disabled || el.getAttribute('aria-disabled') === 'true') return;
        const rect = el.getBoundingClientRect();
        if (rect.width === 0 && rect.height === 0) return;
        const style = window.getComputedStyle(el);
        if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') return;

        // Skip inline text links inside paragraphs/spans (WCAG Inline Exception)
        if (el.tagName.toLowerCase() === 'a' && style.display === 'inline') {
            const parentDisplay = el.parentElement ? window.getComputedStyle(el.parentElement).display : '';
            if (parentDisplay === 'block' || parentDisplay === 'inline' || parentDisplay === 'inline-block') {
                return;
            }
        }

        const tag = el.tagName.toLowerCase();
        const label = (el.innerText || el.getAttribute('aria-label') || el.getAttribute('title') || el.id || tag).trim().slice(0, 30);
        const w = Math.round(rect.width * 10) / 10;
        const h = Math.round(rect.height * 10) / 10;

        // Level AA Minimum: 24x24px
        if (w < 23.5 || h < 23.5) {
            findings.push({
                rule_id: "a11y-target-size-minimum",
                severity: "ERROR",
                selector: `${tag}${el.id ? '#' + el.id : ''}${el.className ? '.' + el.className.split(' ')[0] : ''}`,
                message: `Interactive target "${label}" size (${w}x${h}px) is below WCAG 2.2 minimum 24x24px. Increase padding or hit target size.`,
                value: `${w}x${h}px`
            });
        } else if (window.innerWidth <= 450 && (w < 43.5 || h < 43.5)) {
            // Mobile Recommendation: 44x44px (WARN)
            findings.push({
                rule_id: "ux-mobile-target-size-recommended",
                severity: "WARN",
                selector: `${tag}${el.id ? '#' + el.id : ''}`,
                message: `Mobile touch target "${label}" size (${w}x${h}px) is below recommended 44x44px thumb target.`,
                value: `${w}x${h}px`
            });
        } else {
            passedCount++;
        }

        // Check empty icon buttons lacking accessible name
        if (tag === 'button' || el.getAttribute('role') === 'button') {
            const hasText = el.innerText && el.innerText.trim().length > 0;
            const hasAria = el.getAttribute('aria-label') || el.getAttribute('aria-labelledby') || el.getAttribute('title');
            const hasImg = el.querySelector('img[alt], svg[aria-label]');
            if (!hasText && !hasAria && !hasImg) {
                findings.push({
                    rule_id: "a11y-empty-button-unlabeled",
                    severity: "ERROR",
                    selector: `${tag}${el.id ? '#' + el.id : ''}`,
                    message: `Button has no accessible name or visible text. Screen readers cannot announce its action.`,
                    value: "unlabeled"
                });
            }
        }
    });

    // 3. Rendered Contrast Gate (WCAG 1.4.3 - plugin87 measure_render)
    // Walk visible elements with direct text content
    const walker = document.createTreeWalker(document.body || docEl, NodeFilter.SHOW_ELEMENT);
    let currNode = walker.nextNode();
    let checkedTexts = 0;

    while (currNode && checkedTexts < 150) {
        const textNodes = Array.from(currNode.childNodes).filter(n => n.nodeType === Node.TEXT_NODE && n.nodeValue.trim().length > 0);
        if (textNodes.length > 0) {
            const style = window.getComputedStyle(currNode);
            const rect = currNode.getBoundingClientRect();
            if (rect.width > 0 && rect.height > 0 && style.visibility !== 'hidden' && style.display !== 'none' && style.opacity !== '0') {
                checkedTexts++;
                const fgColor = parseRgba(style.color);

                // Ascend DOM to blend background colors
                let bgColor = [255, 255, 255, 1]; // Fallback canvas white
                let p = currNode;
                const layers = [];
                while (p && p !== document) {
                    const pStyle = window.getComputedStyle(p);
                    const bg = parseRgba(pStyle.backgroundColor);
                    if (bg[3] > 0) {
                        layers.unshift(bg);
                    }
                    p = p.parentElement;
                }
                for (const l of layers) {
                    bgColor = blend(l, bgColor);
                }

                const ratio = Math.round(contrastRatio(fgColor, bgColor) * 100) / 100;
                const fontSize = parseFloat(style.fontSize);
                const isBold = parseInt(style.fontWeight) >= 700 || style.fontWeight === 'bold';
                const isLargeText = fontSize >= 24 || (fontSize >= 18.66 && isBold);
                const minRatio = isLargeText ? 3.0 : 4.5;

                if (ratio < minRatio && fgColor[3] >= 0.5) {
                    const textSample = currNode.innerText.trim().slice(0, 25);
                    findings.push({
                        rule_id: "a11y-rendered-contrast-failure",
                        severity: "ERROR",
                        selector: `${currNode.tagName.toLowerCase()}${currNode.className ? '.' + currNode.className.split(' ')[0] : ''}`,
                        message: `Rendered contrast ratio for "${textSample}" is ${ratio}:1, failing WCAG AA (minimum ${minRatio}:1).`,
                        value: `${ratio}:1 < ${minRatio}:1`
                    });
                } else {
                    passedCount++;
                }
            }
        }
        currNode = walker.nextNode();
    }

    return {
        passedCount: passedCount,
        findings: findings
    };
}
"""

def compute_sources_hash():
    """Computes a SHA-256 fingerprint of current project markup/components for receipt verification."""
    h = hashlib.sha256()
    target_dirs = ["src", "app", "pages", "components", "templates"]
    scanned_files = 0
    for td in target_dirs:
        if os.path.exists(td):
            for root, _, files in os.walk(td):
                for f in sorted(files):
                    if f.endswith((".tsx", ".jsx", ".vue", ".svelte", ".html", ".css")):
                        fp = os.path.join(root, f)
                        try:
                            with open(fp, "rb") as fh:
                                h.update(fh.read())
                                scanned_files += 1
                        except Exception:
                            continue
    return h.hexdigest()[:16] if scanned_files > 0 else "untracked"

def check_playwright_installed():
    try:
        import playwright
        return True
    except ImportError:
        return False

def detect_active_port(candidate_ports=None) -> int:
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

def resolve_output_dir(output_dir=None):
    if output_dir:
        return output_dir
    if os.path.exists(".design"):
        return ".design/screenshots/audit"
    if os.path.exists("reference"):
        return "reference/screenshots/audit"
    return ".design/screenshots/audit"

def capture_ui(url=None, output_dir=None, allow_missing=False, advisory=False):
    output_dir = resolve_output_dir(output_dir)
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
    viewport_audits = {}

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

            print("Capturing Desktop viewport (1440x900) & executing DOM UX audit...")
            page_desktop.goto(url, wait_until="networkidle", timeout=15000)
            desktop_audit = page_desktop.evaluate(DOM_UX_AUDIT_JS)
            viewport_audits["desktop_1440"] = desktop_audit

            desktop_path = os.path.join(output_dir, "desktop_1440.png")
            page_desktop.screenshot(path=desktop_path, full_page=True)
            print(f"Saved: {desktop_path}")
            context_desktop.close()

            # 2. Mobile Viewport (375x812 - iPhone 13/Mini scale)
            context_mobile = browser.new_context(viewport={"width": 375, "height": 812}, is_mobile=True)
            page_mobile = context_mobile.new_page()

            page_mobile.on("console", lambda msg: console_logs.append({"type": msg.type, "text": f"[Mobile] {msg.text}"}))
            page_mobile.on("pageerror", lambda err: page_errors.append(f"[Mobile] {err}"))

            print("Capturing Mobile viewport (375x812) & executing DOM UX audit...")
            page_mobile.goto(url, wait_until="networkidle", timeout=15000)
            mobile_audit = page_mobile.evaluate(DOM_UX_AUDIT_JS)
            viewport_audits["mobile_375"] = mobile_audit

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

    # Dump console audit log
    log_file = os.path.join(output_dir, "console_audit.json")
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.utcnow().isoformat(),
            "url": url,
            "errors": page_errors,
            "logs": console_logs
        }, f, indent=2)
    print(f"Saved console audit: {log_file}")

    # Compile Cryptographic UX Audit Receipt (plugin87/gate.mjs model)
    source_hash = compute_sources_hash()
    total_errors = 0
    total_warnings = 0
    all_findings = []

    for vp_name, data in viewport_audits.items():
        for f in data.get("findings", []):
            item = dict(f)
            item["viewport"] = vp_name
            all_findings.append(item)
            if item["severity"] == "ERROR":
                total_errors += 1
            else:
                total_warnings += 1

    receipt = {
        "timestamp": datetime.utcnow().isoformat(),
        "url": url,
        "source_hash": source_hash,
        "viewports": viewport_audits,
        "total_errors": total_errors,
        "total_warnings": total_warnings,
        "status": "FAILED" if total_errors > 0 else "PASSED"
    }

    receipt_file = os.path.join(output_dir, "ux_audit_receipt.json")
    with open(receipt_file, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)
    print(f"Saved UX audit receipt: {receipt_file}")

    # Print summary table
    print("\n=== UX & Runtime Audit Summary ===")
    print(f"Source SHA-256 Fingerprint: {source_hash}")
    print(f"Runtime Errors: {len(page_errors)}")
    print(f"Deterministic UX Errors: {total_errors} (Target size, contrast, overflow)")
    print(f"Deterministic UX Warnings: {total_warnings}")

    if all_findings:
        print("\nFindings breakdown:")
        for fd in all_findings:
            sev_bracket = f"[{fd['severity']}]"
            print(f"  {sev_bracket} ({fd['viewport']}) {fd['rule_id']}: {fd['message']}")

    if page_errors:
        print(f"\nWarning: {len(page_errors)} uncaught page errors detected during render!", file=sys.stderr)
        for err in page_errors:
            print(f"  - {err}", file=sys.stderr)
        if not advisory:
            return 1

    if total_errors > 0:
        print(f"\nUX Audit FAILED: {total_errors} deterministic UX/A11y hard constraints violated.", file=sys.stderr)
        print("Self-heal: Adjust tokens (colors.json) or markup (padding, overflow) before proceeding.", file=sys.stderr)
        if not advisory:
            return 1

    print("Headless visual capture & deterministic UX audit complete. Ready for vision inspection.")
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Headless Browser UI Capture & Deterministic UX Auditor")
    parser.add_argument("--url", default=None, help="Target URL (default: auto-detected localhost port)")
    parser.add_argument("--output", default=None, help="Output directory for screenshots (default: .design/screenshots/audit or reference fallback)")
    parser.add_argument("--allow-missing", action="store_true", help="Do not exit with error if Playwright/server is unavailable")
    parser.add_argument("--advisory", action="store_true", help="Report UX findings without exiting with code 1")
    args = parser.parse_args()

    sys.exit(capture_ui(args.url, args.output, args.allow_missing, args.advisory))
