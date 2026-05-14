#!/usr/bin/env python3
"""Build v4.0 HTML - minimal DATA for fast parse"""
import json, os

print("Loading prescriptions_v40.json...")
with open('prescriptions_v40.json') as f:
    data = json.load(f)
print(f"Loaded {len(data)} prescriptions")

# Keep ONLY fields needed for search/diagnosis
minimal = []
for p in data:
    minimal.append({
        "id": p["id"],
        "name": p["name"],
        "alias": p.get("alias", []),
        "category": p.get("category", ""),
        "desc": p.get("desc", ""),
        "cure": p.get("cure", ""),
        "herbs": p.get("herbs", []),
        "effect": p.get("effect", ""),
        "syndromes": p.get("syndromes", []),
        "suitable": p.get("suitable", []),
        "classical": p.get("classical", ""),
        "period": p.get("period", ""),
    })

compact = json.dumps(minimal, separators=(',', ':'), ensure_ascii=False)
print(f"Minimal DATA: {len(compact)/1024/1024:.1f}MB")

print("Reading template...")
with open('zhangshang_baicao_v39.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = 'const DATA = ['
start_idx = content.find(start_marker)
if start_idx == -1:
    print("ERROR: Could not find 'const DATA = ['")
    exit(1)

search_from = start_idx + len(start_marker)
bracket_count = 1
pos = search_from
while bracket_count > 0 and pos < len(content):
    ch = content[pos]
    if ch == '[': bracket_count += 1
    elif ch == ']': bracket_count -= 1
    pos += 1

old_end = pos - 1
old_len = old_end - start_idx
print(f"Replacing: {old_len/1024/1024:.1f}MB -> {len(compact)/1024/1024:.1f}MB")

new_content = content[:start_idx] + 'const DATA = ' + compact + '; window.DATA = DATA; // END DATA' + content[old_end:]

output = 'zhangshang_baicao_v40.html'
with open(output, 'w', encoding='utf-8') as f:
    f.write(new_content)

size_mb = os.path.getsize(output) / 1024 / 1024
print(f"Written: {output} ({size_mb:.1f} MB)")
