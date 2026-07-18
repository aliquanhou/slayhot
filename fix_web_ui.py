#!/usr/bin/env python3
"""Restore and fix Web GUI static files (index.html, app.js) from git."""
import subprocess, os

cwd = os.getcwd()
files = [
    'agent/web_gui/static/index.html',
    'agent/web_gui/static/app.js',
]

for f in files:
    # Get original from parent commit
    result = subprocess.run(
        ['git', 'show', f'HEAD~1:{f}'],
        capture_output=True, cwd=cwd
    )
    if result.returncode != 0:
        print(f'ERROR: cannot get {f}')
        continue

    # decode with BOM handling
    content = result.stdout.decode('utf-8-sig')
    original_size = len(content)

    # Apply renames
    content = content.replace('SlayHot', 'SlayHot')
    content = content.replace('slayhot', 'slayhot')
    content = content.replace('SLAYHOT', 'SLAYHOT')

    path = os.path.join(cwd, f)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(content)
    print(f'Fixed: {f} ({original_size} -> {len(content)} bytes)')

print('Done')
