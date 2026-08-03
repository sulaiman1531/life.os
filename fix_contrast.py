import os
import re

TARGET_DIR = r"c:\projects\demo1\gen\project 2\frontend\src"

REPLACEMENTS = {
    # Remaining Backgrounds
    r"bg-\[\#050505\]": "bg-background",
    r"bg-\[\#030014\]": "bg-background",
    
    # Remaining Text Opacities
    r"text-white/10": "text-slate-300 dark:text-white/10",
    r"text-white/20": "text-slate-400 dark:text-white/20",
    r"text-white/90": "text-slate-800 dark:text-white/90",
    
    # Placeholders
    r"placeholder-white/30": "placeholder-slate-400 dark:placeholder-white/30",
    
    # Onboarding Overlay text gradient (from-white to-white/20)
    r"from-white": "from-slate-800 dark:from-white",
    r"via-white(?!/)": "via-slate-600 dark:via-white",
    r"to-white/20": "to-slate-400 dark:to-white/20",
}

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    for pattern, replacement in REPLACEMENTS.items():
        content = re.sub(pattern, replacement, content)

    if original != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed: {filepath}")

for root, _, files in os.walk(TARGET_DIR):
    for file in files:
        if file.endswith(".tsx") or file.endswith(".ts"):
            process_file(os.path.join(root, file))

print("Contrast fix complete.")
