import os
import sys
import shutil
import json

def detect_project_context():
    context = {
        "framework": "unknown",
        "style_engine": "css",
        "has_package_json": False
    }

    if os.path.exists("package.json"):
        context["has_package_json"] = True
        try:
            with open("package.json", "r", encoding="utf-8") as f:
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
        except Exception as e:
            print(f"Notice: Failed to parse package.json ({e})")

    return context

def update_gitignore(base_dir):
    gitignore_path = ".gitignore"
    clean_dir = base_dir.replace("\\", "/").strip("./")
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

def scaffold_reference(target_dir="reference", force=False):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(os.path.dirname(script_dir), "templates")

    if not os.path.exists(templates_dir):
        print(f"Error: Templates directory not found at {templates_dir}", file=sys.stderr)
        sys.exit(1)

    # Required target directories
    for sub in ["screenshots", "notes", "tokens", "fonts"]:
        os.makedirs(os.path.join(target_dir, sub), exist_ok=True)

    # Ensure screenshots .gitkeep
    gitkeep_path = os.path.join(target_dir, "screenshots", ".gitkeep")
    if not os.path.exists(gitkeep_path) or force:
        with open(gitkeep_path, "w", encoding="utf-8") as f:
            pass

    # Copy template folders
    for category in ["notes", "tokens", "fonts"]:
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

    # Update .gitignore
    update_gitignore(target_dir)

    # Inspect context
    ctx = detect_project_context()
    print(f"\nScaffolding complete in: {os.path.abspath(target_dir)}")
    print(f"Detected Environment: Framework={ctx['framework']}, StyleEngine={ctx['style_engine']}")

    if ctx["style_engine"] == "tailwind-v4":
        print("Integration Tip: Reference tokens can be mapped directly into @theme within your CSS entrypoint.")
    elif ctx["style_engine"] == "tailwind-v3":
        print("Integration Tip: Reference tokens can be imported into tailwind.config.js theme.extend.")

if __name__ == "__main__":
    force_flag = "--force" in sys.argv or "-f" in sys.argv
    args = [arg for arg in sys.argv[1:] if arg not in ("--force", "-f")]
    target = args[0] if args else "reference"
    scaffold_reference(target, force=force_flag)
