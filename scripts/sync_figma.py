#!/usr/bin/env python3
"""
scripts/sync_figma.py - Figma Variables to Design Tokens Sync Bridge

Fetches Figma Variables (Design Tokens) via the official Figma REST API
(GET /v1/files/{file_key}/variables/local) in accordance with the Figma Developer Platform terms,
and synchronizes them directly into reference/tokens/*.json.
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error

def rgba_to_hex(r, g, b, a=1.0):
    ri = int(round(r * 255))
    gi = int(round(g * 255))
    bi = int(round(b * 255))
    if a < 0.999:
        ai = int(round(a * 255))
        return f"#{ri:02x}{gi:02x}{bi:02x}{ai:02x}"
    return f"#{ri:02x}{gi:02x}{bi:02x}"

def fetch_figma_variables(file_key, token):
    url = f"https://api.figma.com/v1/files/{file_key}/variables/local"
    req = urllib.request.Request(url, headers={"X-Figma-Token": token})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            if resp.status == 200:
                return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"Figma API Error ({e.code}): {e.read().decode('utf-8')}", file=sys.stderr)
    except Exception as e:
        print(f"Network error connecting to Figma: {e}", file=sys.stderr)
    return None

def parse_and_sync(variables_payload, target_tokens_dir="reference/tokens"):
    os.makedirs(target_tokens_dir, exist_ok=True)
    meta = variables_payload.get("meta", {})
    variables = meta.get("variables", {})

    colors = {}
    spacing = {}
    radii = {}

    for var_id, var_data in variables.items():
        name = var_data.get("name", "").lower().replace("/", ".")
        var_type = var_data.get("resolvedType")
        values_by_mode = var_data.get("valuesByMode", {})
        if not values_by_mode:
            continue
        first_val = list(values_by_mode.values())[0]

        if var_type == "COLOR" and isinstance(first_val, dict):
            r = first_val.get("r", 0)
            g = first_val.get("g", 0)
            b = first_val.get("b", 0)
            a = first_val.get("a", 1.0)
            colors[name] = rgba_to_hex(r, g, b, a)

        elif var_type == "FLOAT" and isinstance(first_val, (int, float)):
            if "radius" in name or "radii" in name or "corner" in name:
                radii[name] = f"{int(first_val)}px"
            else:
                spacing[name] = f"{int(first_val)}px"

    # Merge into reference/tokens
    if colors:
        c_path = os.path.join(target_tokens_dir, "colors.json")
        with open(c_path, "w", encoding="utf-8") as f:
            json.dump(colors, f, indent=2)
        print(f"Synced {len(colors)} color tokens -> {c_path}")

    if spacing:
        s_path = os.path.join(target_tokens_dir, "spacing.json")
        with open(s_path, "w", encoding="utf-8") as f:
            json.dump(spacing, f, indent=2)
        print(f"Synced {len(spacing)} spacing tokens -> {s_path}")

    if radii:
        r_path = os.path.join(target_tokens_dir, "radii.json")
        with open(r_path, "w", encoding="utf-8") as f:
            json.dump(radii, f, indent=2)
        print(f"Synced {len(radii)} radii tokens -> {r_path}")

    return True

def main():
    parser = argparse.ArgumentParser(description="Sync Figma Variables to reference/tokens/*.json")
    parser.add_argument("--file-key", help="Figma File Key (from URL: figma.com/file/<key>/...)")
    parser.add_argument("--token", help="Figma Personal Access Token (or FIGMA_ACCESS_TOKEN env)")
    parser.add_argument("--target-dir", default="reference/tokens", help="Target tokens directory")
    args = parser.parse_args()

    token = args.token or os.environ.get("FIGMA_ACCESS_TOKEN")
    file_key = args.file_key or os.environ.get("FIGMA_FILE_KEY")

    if not token or not file_key:
        print("Usage error: Missing Figma credentials.", file=sys.stderr)
        print("Provide --file-key and --token, or set FIGMA_ACCESS_TOKEN & FIGMA_FILE_KEY.", file=sys.stderr)
        print("\nTip: To integrate live Figma nodes directly inside your AI agent, configure the companion MCP:", file=sys.stderr)
        print("  github.com/GLips/Figma-Context-MCP or figma-mcp-server", file=sys.stderr)
        return 1

    print(f"Fetching local variables for Figma file: {file_key}...")
    payload = fetch_figma_variables(file_key, token)
    if not payload:
        return 1

    parse_and_sync(payload, args.target_dir)
    print("Figma token synchronization complete.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
