import os
import re

TARGET_DIR = r"c:\projects\demo1\gen\project 2\frontend\src"

def check_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find occurrences of text-white or bg-white without dark: prefix, 
    # except when it's bg-white/x where x is in our light mode (e.g. glass-card uses bg-white/80)
    for i, line in enumerate(content.split('\n')):
        if 'text-white' in line and 'dark:text-white' not in line:
            print(f"{filepath}:{i+1}: {line.strip()}")
        # Check if text-transparent is used (often with white gradients)
        if 'text-transparent' in line:
            print(f"{filepath}:{i+1}: {line.strip()}")
        # Check for hardcoded bg-[# something
        if 'bg-[#' in line:
            print(f"{filepath}:{i+1}: {line.strip()}")

for root, _, files in os.walk(TARGET_DIR):
    for file in files:
        if file.endswith(".tsx") or file.endswith(".ts"):
            check_file(os.path.join(root, file))
