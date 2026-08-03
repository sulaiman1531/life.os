import os
import re

TARGET_DIR = r"c:\projects\demo1\gen\project 2\frontend\src"

REPLACEMENTS = {
    # Revert light/dark pairs
    r"bg-slate-100 dark:bg-white/5": "bg-white/5",
    r"bg-slate-200 dark:bg-white/10": "bg-white/10",
    r"bg-slate-300 dark:bg-white/20": "bg-white/20",
    
    r"text-slate-300 dark:text-white/10": "text-white/10",
    r"text-slate-400 dark:text-white/20": "text-white/20",
    r"text-slate-400 dark:text-white/30": "text-white/30",
    r"text-slate-500 dark:text-white/40": "text-white/40",
    r"text-slate-500 dark:text-white/50": "text-white/50",
    r"text-slate-600 dark:text-white/60": "text-white/60",
    r"text-slate-600 dark:text-white/70": "text-white/70",
    r"text-slate-700 dark:text-white/80": "text-white/80",
    r"text-slate-800 dark:text-white/90": "text-white/90",
    
    r"border-slate-200 dark:border-white/5": "border-white/5",
    r"border-slate-300 dark:border-white/20": "border-white/20",
    
    r"hover:bg-slate-100 dark:hover:bg-white/5": "hover:bg-white/5",
    r"hover:bg-slate-200 dark:hover:bg-white/10": "hover:bg-white/10",
    r"hover:bg-slate-300 dark:hover:bg-white/20": "hover:bg-white/20",
    
    r"placeholder-slate-400 dark:placeholder-white/30": "placeholder-white/30",
    
    r"from-slate-800 dark:from-white": "from-white",
    r"via-slate-600 dark:via-white": "via-white",
    r"to-slate-400 dark:to-white/20": "to-white/20",
    
    # Revert global variables (except in globals.css which we will handle manually)
    r"bg-background": "bg-[#0A0A0A]",
    r"bg-card": "bg-[#121212]",
    r"text-foreground": "text-white",
    r"hover:text-foreground": "hover:text-white",
    r"border-border": "border-white/10",
    
    # Leftovers from partial class toggles
    r"dark:text-slate-500": "",
    r"dark:text-white/50": "",
    r"dark:hover:text-foreground": "",
}

def process_file(filepath):
    # Don't revert globals.css variables with this regex script, it will mess them up
    if filepath.endswith("globals.css"):
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    for pattern, replacement in REPLACEMENTS.items():
        content = re.sub(pattern, replacement, content)
        
    # Clean up double spaces left by removed classes
    content = re.sub(r"  +", " ", content)

    if original != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Reverted: {filepath}")

for root, _, files in os.walk(TARGET_DIR):
    for file in files:
        if file.endswith(".tsx") or file.endswith(".ts") or file.endswith(".css"):
            process_file(os.path.join(root, file))

print("Revert complete.")
