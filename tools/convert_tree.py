"""Convert all Simplified Chinese text in a source tree to Traditional Chinese (Taiwan).
usage: convert_tree.py <tree>
Only CJK runs are rewritten, so code, escapes and format specifiers stay untouched.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import s2twp

EXTS = {'.c', '.h', '.cpp', '.hpp', '.cxx', '.fam', '.txt', '.ir', '.json'}
SKIP_DIRS = {'.git', 'toolchain', 'build', 'dist', 'u8g2_cn_tools'}

files = runs = 0
for dp, dn, fn in os.walk(sys.argv[1]):
    dn[:] = [d for d in dn if d not in SKIP_DIRS]
    for f in fn:
        if os.path.splitext(f)[1] not in EXTS:
            continue
        p = os.path.join(dp, f)
        try:
            s = open(p, encoding='utf-8', newline='').read()
        except (UnicodeDecodeError, OSError):
            continue
        if not s2twp.CJK_RUN.search(s):
            continue
        n = s2twp.convert_mixed(s)
        if n != s:
            open(p, 'w', encoding='utf-8', newline='').write(n)
            files += 1
            runs += len(s2twp.CJK_RUN.findall(s))
print(f'converted {files} files ({runs} Chinese text runs)')
