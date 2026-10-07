import os
import sys
import shutil
import json
import argparse

PRESETS = {
    "default": {"variance": 5, "density": 7, "motion": 4, "desc": "Balanced modern SaaS baseline"},
    "b2b-dense": {"variance": 3, "density": 9, "motion": 2, "desc": "High-density data cockpit & telemetry"},
    "editorial-minimal": {"variance": 8, "density": 3, "motion": 5, "desc": "Airy asymmetric showcase & landing"},
    "technical-mono": {"variance": 4, "density": 8, "motion": 1, "desc": "Terminal/developer tool aesthetic"},
    "apple-fluid": {"variance": 6, "density": 5, "motion": 9, "desc": "Fluid spring physics & tactile feedback"},
}

def detect_project_context(base_dir="."):
    context = {
        "framework": "unknown",
        "style_engine": "css",
        "has_package_json": False,
        "subproject_dir": None
    }

    candidate_pkg_paths = [os.path.join(base_dir, "package.json")]
    if not os.path.exists(candidate_pkg_paths[0]):
        try:
            for entry in sorted(os.listdir(base_dir)):
                entry_path = os.path.join(base_dir, entry)
                if os.path.isdir(entry_path) and not entry.startswith(".") and entry not in {"node_modules", "reference", "dist", "build", "templates", "scripts"}:
                    sub_pkg = os.path.join(entry_path, "package.json")
                    if os.path.exists(sub_pkg):
                        candidate_pkg_paths.append(sub_pkg)
        except Exception:
            pass

    for pkg_path in candidate_pkg_paths:
        if os.path.exists(pkg_path):
            context["has_package_json"] = True
            rel_dir = os.path.relpath(os.path.dirname(pkg_path), base_dir)
            if rel_dir and rel_dir != ".":
                context["subproject_dir"] = rel_dir.replace("\\", "/")
            try:
                with open(pkg_path, "r", encoding="utf-8") as f:
                    pkg = json.load(f)
                deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}

                # Detect Framework
                if "next" in deps:
                    context["framework"] = "nextjs"
                elif "vite" in deps:
                    context["framework"] = "vite"
                elif "nuxt" in deps:
                    context["framework"] = "nuxt"
                elif "svelte" in deps or "@sveltejs/kit" in deps:
                    context["framework"] = "svelte"

                # Detect Style Engine
                if "@tailwindcss/postcss" in deps or "@tailwindcss/vite" in deps:
                    context["style_engine"] = "tailwind-v4"
                elif "tailwindcss" in deps:
                    context["style_engine"] = "tailwind-v3"
                elif "@pandacss/dev" in deps:
                    context["style_engine"] = "pandacss"

                break
            except Exception as e:
                print(f"Notice: Failed to parse {pkg_path} ({e})")

    return context

def update_gitignore(target_dir):
    project_base = os.path.dirname(os.path.abspath(target_dir))
    gitignore_path = os.path.join(project_base, ".gitignore")
    clean_dir = os.path.relpath(os.path.abspath(target_dir), project_base).replace("\\", "/").strip("./")
    rules = (
        "\n# Design Reference\n"
        f"{clean_dir}/screenshots/*\n"
        f"!{clean_dir}/screenshots/.gitkeep\n"
        f"{clean_dir}/fonts/*.woff2\n"
        f"{clean_dir}/fonts/*.woff\n"
        f"{clean_dir}/fonts/*.ttf\n"
    )

    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r", encoding="utf-8") as f:
            content = f.read()
        if f"{clean_dir}/screenshots/*" not in content:
            with open(gitignore_path, "a", encoding="utf-8") as f:
                f.write(rules)
            print("Updated .gitignore with reference exclusion rules.")
    else:
        with open(gitignore_path, "w", encoding="utf-8") as f:
            f.write(rules.lstrip())
        print(f"Created {gitignore_path} with reference exclusion rules.")

def safe_copy(src_file, dst_file, force=False):
    if os.path.exists(dst_file) and not force:
        print(f"Skipped existing: {dst_file}")
        return False
    os.makedirs(os.path.dirname(dst_file), exist_ok=True)
    shutil.copy2(src_file, dst_file)
    print(f"Created: {dst_file}")
    return True

def safe_write(dst_file, content, force=False):
    if os.path.exists(dst_file) and not force:
        print(f"Skipped existing: {dst_file}")
        return False
    os.makedirs(os.path.dirname(dst_file), exist_ok=True)
    with open(dst_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {dst_file}")
    return True

def apply_preset(target_dir, preset_name):
    if preset_name not in PRESETS:
        print(f"Warning: Unknown preset '{preset_name}'. Defaulting to 'default'.")
        preset_name = "default"

    config = PRESETS[preset_name]
    design_md_path = os.path.join(target_dir, "DESIGN.md")

    if os.path.exists(design_md_path):
        try:
            with open(design_md_path, "r", encoding="utf-8") as f:
                content = f.read()

            content = content.replace("`DESIGN_VARIANCE`: 5", f"`DESIGN_VARIANCE`: {config['variance']}")
            content = content.replace("`VISUAL_DENSITY`: 7", f"`VISUAL_DENSITY`: {config['density']}")
            content = content.replace("`MOTION_INTENSITY`: 4", f"`MOTION_INTENSITY`: {config['motion']}")

            with open(design_md_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Applied preset '{preset_name}' (Variance={config['variance']}, Density={config['density']}, Motion={config['motion']}) to DESIGN.md")
        except Exception as e:
            print(f"Notice: Failed to update DESIGN.md with preset ({e})")

def generate_css_bridges(target_dir, style_engine, force=False):
    tokens_dir = os.path.join(target_dir, "tokens")
    colors_file = os.path.join(tokens_dir, "colors.json")
    shadows_file = os.path.join(tokens_dir, "shadows.json")
    typography_file = os.path.join(tokens_dir, "typography.json")

    colors = {}
    if os.path.exists(colors_file):
        try:
            with open(colors_file, "r", encoding="utf-8") as f:
                colors = json.load(f)
        except Exception:
            pass

    shadows = {}
    if os.path.exists(shadows_file):
        try:
            with open(shadows_file, "r", encoding="utf-8") as f:
                shadows = json.load(f)
        except Exception:
            pass

    typography = {}
    if os.path.exists(typography_file):
        try:
            with open(typography_file, "r", encoding="utf-8") as f:
                typography = json.load(f)
        except Exception:
            pass

    bg_primary = colors.get("background", {}).get("primary", "#0f172a")
    bg_surface = colors.get("background", {}).get("surface", "#334155")
    text_primary = colors.get("text", {}).get("primary", "#f8fafc")
    text_muted = colors.get("text", {}).get("muted", "#64748b")
    accent_primary = colors.get("accent", {}).get("primary", "#38bdf8")
    border_default = colors.get("border", {}).get("default", "#334155")

    font_imports = typography.get("imports", [])
    font_families = typography.get("families", {})

    # 1. Standard CSS Custom Properties
    tokens_css_lines = ["/* Generated by init-design-reference adapter */"]
    for url in font_imports:
        tokens_css_lines.append(f'@import url("{url}");')

    tokens_css_lines.extend([
        "",
        ":root {",
        f"  --background: {bg_primary};",
        f"  --surface: {bg_surface};",
        f"  --foreground: {text_primary};",
        f"  --muted: {text_muted};",
        f"  --accent: {accent_primary};",
        f"  --border: {border_default};",
    ])
    for fam_key, fam_list in font_families.items():
        formatted_fam = ", ".join([f'"{f}"' if " " in f else f for f in fam_list])
        tokens_css_lines.append(f"  --font-{fam_key}: {formatted_fam};")
    for key, val in shadows.items():
        if key.startswith("elevation-"):
            tokens_css_lines.append(f"  --shadow-{key}: {val};")
    tokens_css_lines.append("}\n")
    safe_write(os.path.join(tokens_dir, "tokens.css"), "\n".join(tokens_css_lines), force=force)

    # 2. Tailwind v4 @theme bridge
    if style_engine == "tailwind-v4":
        theme_css_lines = [
            "/* Tailwind v4 @theme bridge */",
            '@import "./tokens.css";',
            "",
            "@theme {",
            "  --color-background: var(--background);",
            "  --color-surface: var(--surface);",
            "  --color-foreground: var(--foreground);",
            "  --color-muted: var(--muted);",
            "  --color-accent: var(--accent);",
            "  --color-border: var(--border);",
        ]
        for fam_key in font_families:
            theme_css_lines.append(f"  --font-{fam_key}: var(--font-{fam_key});")
        for key in shadows:
            if key.startswith("elevation-"):
                theme_css_lines.append(f"  --shadow-{key}: var(--shadow-{key});")
        theme_css_lines.append("}\n")
        safe_write(os.path.join(tokens_dir, "theme.css"), "\n".join(theme_css_lines), force=force)

    # 3. Tailwind v3 preset bridge
    elif style_engine == "tailwind-v3":
        shadow_entries = ",\n".join(
            [f'        "{k}": "var(--shadow-{k})"' for k in shadows if k.startswith("elevation-")]
        )
        font_entries = ",\n".join(
            [f'        "{k}": ["var(--font-{k})"]' for k in font_families]
        )
        preset_content = f"""/** Tailwind v3 preset bridge */
module.exports = {{
  theme: {{
    extend: {{
      fontFamily: {{
{font_entries}
      }},
      colors: {{
        background: "var(--background)",
        surface: "var(--surface)",
        foreground: "var(--foreground)",
        muted: "var(--muted)",
        accent: "var(--accent)",
        border: "var(--border)",
      }},
      boxShadow: {{
{shadow_entries}
      }},
    }},
  }},
}};
"""
        safe_write(os.path.join(tokens_dir, "tailwind.preset.js"), preset_content, force=force)

def scaffold_reference(target_dir="reference", force=False, preset="default"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(os.path.dirname(script_dir), "templates")

    if not os.path.exists(templates_dir):
        print(f"Error: Templates directory not found at {templates_dir}", file=sys.stderr)
        sys.exit(1)

    # Required target directories
    for sub in ["screenshots", "notes", "tokens", "fonts", "patterns"]:
        os.makedirs(os.path.join(target_dir, sub), exist_ok=True)

    # Ensure screenshots .gitkeep
    gitkeep_path = os.path.join(target_dir, "screenshots", ".gitkeep")
    if not os.path.exists(gitkeep_path) or force:
        with open(gitkeep_path, "w", encoding="utf-8") as f:
            pass

    # Copy template folders (notes, tokens, fonts, patterns)
    for category in ["notes", "tokens", "fonts", "patterns"]:
        cat_src = os.path.join(templates_dir, category)
        if os.path.exists(cat_src):
            for filename in os.listdir(cat_src):
                src_file = os.path.join(cat_src, filename)
                dst_file = os.path.join(target_dir, category, filename)
                safe_copy(src_file, dst_file, force=force)

    # Copy root documents directly to reference root
    root_src = os.path.join(templates_dir, "root")
    if os.path.exists(root_src):
        for filename in os.listdir(root_src):
            src_file = os.path.join(root_src, filename)
            dst_file = os.path.join(target_dir, filename)
            safe_copy(src_file, dst_file, force=force)

    # Apply selected Taste preset
    apply_preset(target_dir, preset)

    # Update .gitignore
    update_gitignore(target_dir)

    # Inspect context & generate CSS bridges
    project_base = os.path.dirname(os.path.abspath(target_dir))
    ctx = detect_project_context(base_dir=project_base)
    generate_css_bridges(target_dir, ctx["style_engine"], force=force)

    sub_info = f" (detected in ./{ctx['subproject_dir']})" if ctx.get("subproject_dir") else ""
    print(f"\nScaffolding complete in: {os.path.abspath(target_dir)}")
    print(f"Preset Applied: {preset} ({PRESETS.get(preset, {}).get('desc', '')})")
    print(f"Detected Environment: Framework={ctx['framework']}, StyleEngine={ctx['style_engine']}{sub_info}")

    css_entry = f"{ctx['subproject_dir']}/src/index.css" if ctx.get("subproject_dir") else "your CSS entrypoint"
    if ctx["style_engine"] == "tailwind-v4":
        print(f"Integration: Generated reference/tokens/theme.css. Add '@import \"./reference/tokens/theme.css\";' (or relative path) to {css_entry}.")
    elif ctx["style_engine"] == "tailwind-v3":
        print(f"Integration: Generated reference/tokens/tailwind.preset.js. Add 'presets: [require(\"./reference/tokens/tailwind.preset.js\")]' to tailwind.config.js, and import reference/tokens/tokens.css in {css_entry}.")
    else:
        print(f"Integration: Generated reference/tokens/tokens.css. Add '@import \"./reference/tokens/tokens.css\";' to {css_entry}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scaffold production-grade UI design reference and pattern architecture")
    parser.add_argument("target", nargs="?", default="reference", help="Target directory (default: reference)")
    parser.add_argument("-f", "--force", action="store_true", help="Force overwrite existing template files")
    parser.add_argument("-p", "--preset", choices=list(PRESETS.keys()), default="default", help="Design taste preset")
    args = parser.parse_args()

    scaffold_reference(args.target, force=args.force, preset=args.preset)
