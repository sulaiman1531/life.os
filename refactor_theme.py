import os
import re

TARGET_DIR = r"c:\projects\demo1\gen\project 2\frontend\src"

REPLACEMENTS = {
    # Backgrounds
    r"bg-\[\#0A0A0A\]": "bg-background",
    r"bg-\[\#121212\]": "bg-card",
    r"bg-\[\#0c0c0c\]": "bg-background",
    r"bg-\[\#0c0c0c\]/90": "bg-background/90",
    
    r"bg-white/5(?![0-9])": "bg-slate-100 dark:bg-white/5",
    r"bg-white/10": "bg-slate-200 dark:bg-white/10",
    r"bg-white/20": "bg-slate-300 dark:bg-white/20",
    
    # Text
    r"text-white(?!/[0-9])": "text-foreground",
    r"text-white/30": "text-slate-400 dark:text-white/30",
    r"text-white/40": "text-slate-500 dark:text-white/40",
    r"text-white/50": "text-slate-500 dark:text-white/50",
    r"text-white/60": "text-slate-600 dark:text-white/60",
    r"text-white/70": "text-slate-600 dark:text-white/70",
    r"text-white/80": "text-slate-700 dark:text-white/80",

    # Borders
    r"border-white/5(?![0-9])": "border-slate-200 dark:border-white/5",
    r"border-white/10": "border-border", # since we mapped border to 15% in dark and 90% in light
    r"border-white/20": "border-slate-300 dark:border-white/20",

    # Hover Backgrounds
    r"hover:bg-white/5(?![0-9])": "hover:bg-slate-100 dark:hover:bg-white/5",
    r"hover:bg-white/10": "hover:bg-slate-200 dark:hover:bg-white/10",
    r"hover:bg-white/20": "hover:bg-slate-300 dark:hover:bg-white/20",

    # Hover Text
    r"hover:text-white(?!/[0-9])": "hover:text-foreground",
}

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    for pattern, replacement in REPLACEMENTS.items():
        # Only replace inside className strings or template literals.
        # Simple regex replace first
        # Wait, if we replace text-white inside `text-white/50`, it will mess up.
        # The regex `text-white(?!/[0-9])` handles that negative lookahead.
        content = re.sub(pattern, replacement, content)

    if original != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {filepath}")

for root, _, files in os.walk(TARGET_DIR):
    for file in files:
        if file.endswith(".tsx") or file.endswith(".ts"):
            process_file(os.path.join(root, file))

print("Refactoring complete.")
