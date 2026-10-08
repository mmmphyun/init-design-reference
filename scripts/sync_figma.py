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

def load_json_or_empty(path):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def resolve_tokens_target(target=None):
    if target:
        return target
    base = ".design" if os.path.exists(".design") or not os.path.exists("reference") else "reference"
    return os.path.join(base, "tokens")

def parse_and_sync(variables_payload, target_tokens_dir=None):
    target_tokens_dir = resolve_tokens_target(target_tokens_dir)
    os.makedirs(target_tokens_dir, exist_ok=True)
    meta = variables_payload.get("meta", {})
    variables = meta.get("variables", {})

    colors = {}
    spacing = {}
    radii = {}

    for var_id, var_data in variables.items():
        name = var_data.get("name", "").lower()
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
            hex_val = rgba_to_hex(r, g, b, a)
            parts = [p.strip() for p in name.replace("/", ".").split(".") if p.strip()]
            if len(parts) >= 2:
                group, key = parts[0], ".".join(parts[1:])
            else:
                group, key = "custom", parts[0] if parts else "unnamed"
            colors.setdefault(group, {})[key] = hex_val

        elif var_type == "FLOAT" and isinstance(first_val, (int, float)):
            clean_name = name.replace("/", "-").strip("-")
            if "radius" in name or "radii" in name or "corner" in name:
                radii[clean_name] = f"{int(first_val)}px"
            else:
                spacing[clean_name] = f"{int(first_val)}px"

    # Deep merge into target tokens directory
    if colors:
        c_path = os.path.join(target_tokens_dir, "colors.json")
        existing_colors = load_json_or_empty(c_path)
        for g, vals in colors.items():
            if not isinstance(existing_colors.get(g), dict):
                existing_colors[g] = {}
            existing_colors[g].update(vals)
        with open(c_path, "w", encoding="utf-8") as f:
            json.dump(existing_colors, f, indent=2)
        print(f"Synced {len(colors)} color groups -> {c_path}")

    if spacing:
        s_path = os.path.join(target_tokens_dir, "spacing.json")
        existing_spacing = load_json_or_empty(s_path)
        existing_spacing.update(spacing)
        with open(s_path, "w", encoding="utf-8") as f:
            json.dump(existing_spacing, f, indent=2)
        print(f"Synced {len(spacing)} spacing tokens -> {s_path}")

    if radii:
        r_path = os.path.join(target_tokens_dir, "radii.json")
        existing_radii = load_json_or_empty(r_path)
        existing_radii.update(radii)
        with open(r_path, "w", encoding="utf-8") as f:
            json.dump(existing_radii, f, indent=2)
        print(f"Synced {len(radii)} radii tokens -> {r_path}")

    return True

def main():
    parser = argparse.ArgumentParser(description="Sync Figma Variables to design tokens (*.json)")
    parser.add_argument("--file-key", help="Figma File Key (from URL: figma.com/file/<key>/...)")
    parser.add_argument("--token", help="Figma Personal Access Token (or FIGMA_ACCESS_TOKEN env)")
    parser.add_argument("--target-dir", default=None, help="Target tokens directory (default: auto-detected .design/tokens or reference/tokens)")
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
