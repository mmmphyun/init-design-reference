import os
import sys
import shutil
import json
import re
import argparse

def load_presets(templates_dir):
    presets = {}
    presets_dir = os.path.join(templates_dir, "presets")
    if os.path.exists(presets_dir):
        for f in sorted(os.listdir(presets_dir)):
            if f.endswith(".json"):
                name = os.path.splitext(f)[0]
                try:
                    with open(os.path.join(presets_dir, f), "r", encoding="utf-8") as fp:
                        presets[name] = json.load(fp)
                except Exception:
                    pass
    return presets

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_TEMPLATES_DIR = os.path.join(os.path.dirname(_SCRIPT_DIR), "templates")
PRESETS = load_presets(_TEMPLATES_DIR)

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

def apply_preset(target_dir, preset_name, dials_override=None, force=False, is_new=False, design_existed=None, colors_existed=None, typography_existed=None):
    if preset_name not in PRESETS:
        print(f"Notice: Preset '{preset_name}' not in predefined templates. Falling back to baseline 'default' with custom tuning.")
        preset_name = "default"

    config = PRESETS[preset_name]
    variance = config.get("variance", 5)
    density = config.get("density", 5)
    motion = config.get("motion", 5)

    if dials_override:
        try:
            parts = [int(p.strip()) for p in dials_override.split(",")]
            if len(parts) == 3:
                variance, density, motion = parts[0], parts[1], parts[2]
                print(f"Overriding dials with custom values: Variance={variance}, Density={density}, Motion={motion}")
        except Exception as e:
            print(f"Notice: Failed to parse --dials '{dials_override}', using preset values ({e})")

    design_md_path = os.path.join(target_dir, "DESIGN.md")
    colors_json_path = os.path.join(target_dir, "tokens", "colors.json")
    typography_json_path = os.path.join(target_dir, "tokens", "typography.json")

    has_design = design_existed if design_existed is not None else (not is_new if os.path.exists(design_md_path) else False)
    has_colors = colors_existed if colors_existed is not None else (not is_new if os.path.exists(colors_json_path) else False)
    has_typo = typography_existed if typography_existed is not None else (not is_new if os.path.exists(typography_json_path) else False)

    # 1. Update DESIGN.md Dials
    if os.path.exists(design_md_path):
        if not force and not dials_override and has_design:
            print(f"Preserved existing dials in {design_md_path} (use --dials or -f/--force to override).")
        else:
            try:
                with open(design_md_path, "r", encoding="utf-8") as f:
                    content = f.read()

                content = re.sub(r"`DESIGN_VARIANCE`:\s*[0-9]+", f"`DESIGN_VARIANCE`: {variance}", content)
                content = re.sub(r"`VISUAL_DENSITY`:\s*[0-9]+", f"`VISUAL_DENSITY`: {density}", content)
                content = re.sub(r"`MOTION_INTENSITY`:\s*[0-9]+", f"`MOTION_INTENSITY`: {motion}", content)

                with open(design_md_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Applied dials (Variance={variance}, Density={density}, Motion={motion}) to DESIGN.md")
            except Exception as e:
                print(f"Notice: Failed to update DESIGN.md with preset ({e})")


    # 2. Inject Curated Domain Palette into colors.json (Skip if already exists unless force=True)
    if "colors" in config:
        if has_colors and not force:
            print(f"Preserved existing colors in {colors_json_path} (use -f/--force to overwrite with preset palette).")
        else:
            try:
                existing_colors = {}
                if os.path.exists(colors_json_path):
                    with open(colors_json_path, "r", encoding="utf-8") as f:
                        existing_colors = json.load(f)

                for group, vals in config["colors"].items():
                    if group not in existing_colors:
                        existing_colors[group] = {}
                    existing_colors[group].update(vals)

                with open(colors_json_path, "w", encoding="utf-8") as f:
                    json.dump(existing_colors, f, indent=2, ensure_ascii=False)
                print(f"Injected curated domain colors for '{preset_name}' into {colors_json_path}")
            except Exception as e:
                print(f"Notice: Failed to update colors.json with preset ({e})")

    # 3. Inject Curated Typography into typography.json (Skip if already exists unless force=True)
    if "typography" in config and os.path.exists(typography_json_path):
        if has_typo and not force:
            print(f"Preserved existing typography in {typography_json_path} (use -f/--force to overwrite with preset fonts).")
        else:

            try:
                with open(typography_json_path, "r", encoding="utf-8") as f:
                    existing_typo = json.load(f)
                if "imports" in config["typography"]:
                    existing_typo["imports"] = config["typography"]["imports"]
                if "families" in config["typography"]:
                    existing_typo["families"].update(config["typography"]["families"])
                with open(typography_json_path, "w", encoding="utf-8") as f:
                    json.dump(existing_typo, f, indent=2, ensure_ascii=False)
                print(f"Injected curated typography for '{preset_name}' into {typography_json_path}")
            except Exception as e:
                print(f"Notice: Failed to update typography.json with preset ({e})")

def hex_to_rgba(hex_code, alpha):
    h = str(hex_code).lstrip("#")
    if len(h) == 3:
        h = "".join([c * 2 for c in h])
    elif len(h) == 4:
        # 4-digit hex (#RGBA) -> expand RGB, keep original alpha scaled if needed or extract RGB
        h = "".join([c * 2 for c in h[:3]])
    elif len(h) == 8:
        # 8-digit hex (#RRGGBBAA) -> extract RGB part
        h = h[:6]
    try:
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return f"rgba({r}, {g}, {b}, {alpha})"
    except Exception:
        return str(hex_code)

def generate_css_bridges(target_dir, style_engine, force=False):
    tokens_dir = os.path.join(target_dir, "tokens")
    colors_file = os.path.join(tokens_dir, "colors.json")
    shadows_file = os.path.join(tokens_dir, "shadows.json")
    typography_file = os.path.join(tokens_dir, "typography.json")
    radii_file = os.path.join(tokens_dir, "radii.json")
    motion_file = os.path.join(tokens_dir, "motion.json")

    def load_json(path):
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    colors = load_json(colors_file)
    shadows = load_json(shadows_file)
    typography = load_json(typography_file)
    radii = load_json(radii_file)
    motion = load_json(motion_file)

    bg_primary = colors.get("background", {}).get("primary", "#09090b")
    bg_surface = colors.get("background", {}).get("surface", "#18181b")
    bg_surface_secondary = colors.get("background", {}).get("secondary", "#121215")
    text_primary = colors.get("text", {}).get("primary", "#fafafa")
    text_muted = colors.get("text", {}).get("muted", "#71717a")
    accent_primary = colors.get("accent", {}).get("primary", "#2563eb")
    border_default = colors.get("border", {}).get("default", "#27272a")
    border_subtle = colors.get("border", {}).get("subtle", "#18181b")
    border_strong = colors.get("border", {}).get("strong", "#3f3f46")

    status_error = colors.get("status", {}).get("error", "#ef4444")
    status_success = colors.get("status", {}).get("success", "#22c55e")
    status_warning = colors.get("status", {}).get("warning", "#eab308")
    status_info = colors.get("status", {}).get("info", "#3b82f6")

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
        f"  --surface-secondary: {bg_surface_secondary};",
        f"  --foreground: {text_primary};",
        f"  --muted: {text_muted};",
        f"  --accent: {accent_primary};",
        f"  --border: {border_default};",
        f"  --border-default: {border_default};",
        f"  --border-subtle: {border_subtle};",
        f"  --border-strong: {border_strong};",
        f"  --primary: {accent_primary};",
        f"  --primary-foreground: #ffffff;",
        f"  --danger: {status_error};",
        f"  --danger-foreground: #ffffff;",
        f"  --status-error: {status_error};",
        f"  --status-error-bg: {hex_to_rgba(status_error, 0.12)};",
        f"  --status-error-border: {hex_to_rgba(status_error, 0.25)};",
        f"  --status-success: {status_success};",
        f"  --status-success-bg: {hex_to_rgba(status_success, 0.12)};",
        f"  --status-success-border: {hex_to_rgba(status_success, 0.25)};",
        f"  --status-warning: {status_warning};",
        f"  --status-warning-bg: {hex_to_rgba(status_warning, 0.12)};",
        f"  --status-warning-border: {hex_to_rgba(status_warning, 0.25)};",
        f"  --status-info: {status_info};",
        f"  --skeleton: {bg_surface};",
        f"  --skeleton-subtle: {bg_primary};",
    ])
    for fam_key, fam_list in font_families.items():
        formatted_fam = ", ".join([f'"{f}"' if " " in f else f for f in fam_list])
        tokens_css_lines.append(f"  --font-{fam_key}: {formatted_fam};")
    for key, val in shadows.items():
        if key.startswith("elevation-"):
            tokens_css_lines.append(f"  --shadow-{key}: {val};")
    for r_k, r_v in radii.items():
        tokens_css_lines.append(f"  --radius-{r_k}: {r_v};")
    for d_k, d_v in motion.get("duration", {}).items():
        tokens_css_lines.append(f"  --duration-{d_k}: {d_v};")
    for e_k, e_v in motion.get("easing", {}).items():
        tokens_css_lines.append(f"  --ease-{e_k}: {e_v};")
    tokens_css_lines.append("}\n")
    safe_write(os.path.join(tokens_dir, "tokens.css"), "\n".join(tokens_css_lines), force=force)

    # 2. Tailwind v4 @theme bridge
    if style_engine == "tailwind-v4":
        theme_css_lines = ["/* Tailwind v4 @theme bridge */"]
        for url in font_imports:
            theme_css_lines.append(f'@import url("{url}");')
        theme_css_lines.extend([
            '@import "./tokens.css";',
            "",
            "@theme {",
            "  --color-background: var(--background);",
            "  --color-surface: var(--surface);",
            "  --color-surface-secondary: var(--surface-secondary);",
            "  --color-foreground: var(--foreground);",
            "  --color-muted: var(--muted);",
            "  --color-accent: var(--accent);",
            "  --color-border: var(--border);",
            "  --color-border-default: var(--border-default);",
            "  --color-border-subtle: var(--border-subtle);",
            "  --color-border-strong: var(--border-strong);",
            "  --color-primary: var(--primary);",
            "  --color-primary-foreground: var(--primary-foreground);",
            "  --color-danger: var(--danger);",
            "  --color-danger-foreground: var(--danger-foreground);",
            "  --color-status-error: var(--status-error);",
            "  --color-status-error-bg: var(--status-error-bg);",
            "  --color-status-error-border: var(--status-error-border);",
            "  --color-status-success: var(--status-success);",
            "  --color-status-success-bg: var(--status-success-bg);",
            "  --color-status-success-border: var(--status-success-border);",
            "  --color-status-warning: var(--status-warning);",
            "  --color-status-warning-bg: var(--status-warning-bg);",
            "  --color-status-warning-border: var(--status-warning-border);",
            "  --color-status-info: var(--status-info);",
            "  --color-skeleton: var(--skeleton);",
            "  --color-skeleton-subtle: var(--skeleton-subtle);",
        ])
        for fam_key, fam_list in font_families.items():
            formatted_fam = ", ".join([f'"{f}"' if " " in f else f for f in fam_list])
            theme_css_lines.append(f"  --font-{fam_key}: {formatted_fam};")
        for key in shadows:
            if key.startswith("elevation-"):
                theme_css_lines.append(f"  --shadow-{key}: var(--shadow-{key});")
        for r_k in radii:
            theme_css_lines.append(f"  --radius-{r_k}: var(--radius-{r_k});")
        for d_k in motion.get("duration", {}):
            theme_css_lines.append(f"  --duration-{d_k}: var(--duration-{d_k});")
        for e_k in motion.get("easing", {}):
            theme_css_lines.append(f"  --ease-{e_k}: var(--ease-{e_k});")
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
        radii_entries = ",\n".join(
            [f'        "{k}": "var(--radius-{k})"' for k in radii]
        )
        duration_entries = ",\n".join(
            [f'        "{k}": "var(--duration-{k})"' for k in motion.get("duration", {})]
        )
        easing_entries = ",\n".join(
            [f'        "{k}": "var(--ease-{k})"' for k in motion.get("easing", {})]
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
        "surface-secondary": "var(--surface-secondary)",
        foreground: "var(--foreground)",
        muted: "var(--muted)",
        accent: "var(--accent)",
        border: "var(--border)",
        "border-default": "var(--border-default)",
        "border-subtle": "var(--border-subtle)",
        "border-strong": "var(--border-strong)",
        primary: "var(--primary)",
        "primary-foreground": "var(--primary-foreground)",
        danger: "var(--danger)",
        "danger-foreground": "var(--danger-foreground)",
        "status-error": "var(--status-error)",
        "status-error-bg": "var(--status-error-bg)",
        "status-error-border": "var(--status-error-border)",
        "status-success": "var(--status-success)",
        "status-success-bg": "var(--status-success-bg)",
        "status-success-border": "var(--status-success-border)",
        "status-warning": "var(--status-warning)",
        "status-warning-bg": "var(--status-warning-bg)",
        "status-warning-border": "var(--status-warning-border)",
        "status-info": "var(--status-info)",
        skeleton: "var(--skeleton)",
        "skeleton-subtle": "var(--skeleton-subtle)",
      }},
      borderRadius: {{
{radii_entries}
      }},
      transitionDuration: {{
{duration_entries}
      }},
      transitionTimingFunction: {{
{easing_entries}
      }},
      boxShadow: {{
{shadow_entries}
      }},
    }},
  }},
}};
"""
        safe_write(os.path.join(tokens_dir, "tailwind.preset.js"), preset_content, force=force)



def resolve_design_target(custom_target=None):
    if custom_target:
        return custom_target
    if os.path.exists(".design"):
        return ".design"
    if os.path.exists("reference"):
        return "reference"
    return ".design"

def verify_design_spec(target_dir=None):
    resolved = resolve_design_target(target_dir)
    design_md = os.path.join(resolved, "DESIGN.md")
    colors_json = os.path.join(resolved, "tokens", "colors.json")

    if not os.path.exists(design_md):
        print(f"[HARD-GUARD FAIL] {design_md} does not exist.", file=sys.stderr)
        return False

    with open(design_md, "r", encoding="utf-8") as f:
        content = f.read()

    variance = re.search(r"`DESIGN_VARIANCE`:\s*([0-9]+)", content)
    density = re.search(r"`VISUAL_DENSITY`:\s*([0-9]+)", content)
    motion = re.search(r"`MOTION_INTENSITY`:\s*([0-9]+)", content)

    if not (variance and density and motion):
        print(f"[HARD-GUARD FAIL] {design_md} is missing one of DESIGN_VARIANCE, VISUAL_DENSITY, MOTION_INTENSITY.", file=sys.stderr)
        return False

    v_val, d_val, m_val = int(variance.group(1)), int(density.group(1)), int(motion.group(1))
    for name, val in [("DESIGN_VARIANCE", v_val), ("VISUAL_DENSITY", d_val), ("MOTION_INTENSITY", m_val)]:
        if not (1 <= val <= 10):
            print(f"[HARD-GUARD FAIL] {name} value {val} out of bounds. Must be an integer between 1 and 10.", file=sys.stderr)
            return False

    if not os.path.exists(colors_json):
        print(f"[HARD-GUARD FAIL] {colors_json} does not exist.", file=sys.stderr)
        return False

    try:
        with open(colors_json, "r", encoding="utf-8") as f:
            colors = json.load(f)
        required = [("background", "surface"), ("background", "primary"), ("accent", "primary"), ("border", "default")]
        hex_pattern = re.compile(r"^#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")
        for sec, key in required:
            val = colors.get(sec, {}).get(key)
            if not val:
                print(f"[HARD-GUARD FAIL] {colors_json} missing required token '{sec}.{key}'.", file=sys.stderr)
                return False
            if not hex_pattern.match(str(val)):
                print(f"[HARD-GUARD FAIL] Token '{sec}.{key}' has invalid hex value '{val}'.", file=sys.stderr)
                return False
    except Exception as e:
        print(f"[HARD-GUARD FAIL] Failed to parse {colors_json}: {e}", file=sys.stderr)
        return False

    print(f"[HARD-GUARD PASS] Design specification and tokens in '{resolved}' are valid (Variance={v_val}, Density={d_val}, Motion={m_val}).")
    return True

def scaffold_reference(target_dir=None, force=False, preset="default", dials_override=None):
    target_dir = resolve_design_target(target_dir)
    design_existed = os.path.exists(os.path.join(target_dir, "DESIGN.md"))
    colors_existed = os.path.exists(os.path.join(target_dir, "tokens", "colors.json"))
    typography_existed = os.path.exists(os.path.join(target_dir, "tokens", "typography.json"))
    is_new = not design_existed and not colors_existed and not typography_existed
    script_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(os.path.dirname(script_dir), "templates")

    if not os.path.exists(templates_dir):
        print(f"Error: Templates directory not found at {templates_dir}", file=sys.stderr)
        sys.exit(1)

    # Required target directories: tokens, screenshots, patterns
    for sub in ["screenshots", "tokens", "patterns"]:
        os.makedirs(os.path.join(target_dir, sub), exist_ok=True)

    # Ensure screenshots .gitkeep
    gitkeep_path = os.path.join(target_dir, "screenshots", ".gitkeep")
    if not os.path.exists(gitkeep_path) or force:
        with open(gitkeep_path, "w", encoding="utf-8") as f:
            pass

    # Copy template folders: tokens, patterns (exclude notes and fonts from repo pollution)
    for category in ["tokens", "patterns"]:
        cat_src = os.path.join(templates_dir, category)
        if os.path.exists(cat_src):
            for filename in os.listdir(cat_src):
                src_file = os.path.join(cat_src, filename)
                dst_file = os.path.join(target_dir, category, filename)
                safe_copy(src_file, dst_file, force=force)

    # Copy single constitutional spec (DESIGN.md) to target root
    design_src = os.path.join(templates_dir, "root", "DESIGN.md")
    if os.path.exists(design_src):
        safe_copy(design_src, os.path.join(target_dir, "DESIGN.md"), force=force)

    # Apply selected Taste preset
    apply_preset(
        target_dir,
        preset,
        dials_override=dials_override,
        force=force,
        is_new=is_new,
        design_existed=design_existed,
        colors_existed=colors_existed,
        typography_existed=typography_existed,
    )


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

    clean_target = target_dir.replace("\\", "/").strip("./")
    css_entry = f"{ctx['subproject_dir']}/src/index.css" if ctx.get("subproject_dir") else "your CSS entrypoint"
    if ctx["style_engine"] == "tailwind-v4":
        print(f"Integration: Generated {clean_target}/tokens/theme.css. Add '@import \"./{clean_target}/tokens/theme.css\";' (or relative path) at Line 1 of {css_entry} (before '@import \"tailwindcss\";') to prevent W3C font drop.")
    elif ctx["style_engine"] == "tailwind-v3":
        print(f"Integration: Generated {clean_target}/tokens/tailwind.preset.js. Add 'presets: [require(\"./{clean_target}/tokens/tailwind.preset.js\")]' to tailwind.config.js, and import {clean_target}/tokens/tokens.css in {css_entry}.")
    else:
        print(f"Integration: Generated {clean_target}/tokens/tokens.css. Add '@import \"./{clean_target}/tokens/tokens.css\";' to {css_entry}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scaffold production-grade UI design reference and pattern architecture")
    parser.add_argument("target", nargs="?", default=None, help="Target directory (default: .design or reference fallback)")
    parser.add_argument("-f", "--force", action="store_true", help="Force overwrite existing template files")
    parser.add_argument("-p", "--preset", default="default", help="Design taste preset (apple-fluid, b2b-dense, editorial-minimal, technical-mono, etc.)")
    parser.add_argument("--dials", default=None, help="Custom dial override in format: 'variance,density,motion' (e.g. '7,4,8')")
    parser.add_argument("--verify-spec", action="store_true", help="Verify integrity of design specification and tokens (Hard-Guard)")
    parser.add_argument("--bridge-only", action="store_true", help="Regenerate CSS and Tailwind bridges only from tokens")
    args = parser.parse_args()

    if args.verify_spec:
        sys.exit(0 if verify_design_spec(args.target) else 1)

    if args.bridge_only:
        target = resolve_design_target(args.target)
        project_base = os.path.dirname(os.path.abspath(target))
        ctx = detect_project_context(base_dir=project_base)
        generate_css_bridges(target, ctx["style_engine"], force=True)
        print(f"Regenerated CSS bridges for '{target}'.")
        sys.exit(0)

    scaffold_reference(args.target, force=args.force, preset=args.preset, dials_override=args.dials)

