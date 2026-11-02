"""Replace untranslated English UI strings with Traditional Chinese, in place.
Re-scans the tree (robust to source changes), only touches the string argument
of known UI calls, and replaces the exact literal span. usage: localize_en.py <tree>
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
M = {}
M.update(json.load(open(os.path.join(HERE, 'tm.json'), encoding='utf-8')))
for mod in ('en_zh_core', 'en_zh_ext', 'en_zh_ext2'):
    m = __import__(mod)
    M.update(m.T)
CALLS = r'(submenu_add_item(?:_ex)?|submenu_set_header|variable_item_list_add|variable_item_set_current_value_text|dialog_ex_set_header|dialog_ex_set_text|dialog_ex_set_left_button_text|dialog_ex_set_right_button_text|dialog_ex_set_center_button_text|dialog_message_set_header|dialog_message_set_text|popup_set_header|popup_set_text|widget_add_string_element|widget_add_string_multiline_element|widget_add_text_scroll_element|widget_add_text_box_element|widget_add_button_element|text_input_set_header_text|byte_input_set_header_text|number_input_set_header_text|text_box_set_text|loading|canvas_draw_str|canvas_draw_str_aligned|elements_button_left|elements_button_right|elements_button_center|elements_multiline_text|elements_multiline_text_aligned|menu_add_item|furi_string_set_str|furi_string_set)'
callre = re.compile(CALLS + r'\s*\(')
litre = re.compile(r'"((?:[^"\\]|\\.)*)"')
nfiles = nrepl = 0
for dp, dn, fn in os.walk(sys.argv[1]):
    if '.git' in dp.split(os.sep): continue
    for f in fn:
        if not f.endswith(('.c', '.cpp', '.cxx')): continue
        p = os.path.join(dp, f)
        try: s = open(p, encoding='utf-8', errors='ignore').read()
        except OSError: continue
        edits = []
        for m in callre.finditer(s):
            semi = s.find(';', m.end())
            end = min(m.end() + 400, semi if semi != -1 else len(s))
            lm = litre.search(s, m.end(), end)
            if not lm: continue
            lit = lm.group(1)
            zh = M.get(lit)
            if zh and zh != lit:
                edits.append((lm.start(), lm.end(), '"' + zh + '"'))
        if not edits: continue
        edits.sort(reverse=True)
        seen = set()
        for a, b, rep in edits:
            if a in seen: continue
            seen.add(a)
            s = s[:a] + rep + s[b:]
        open(p, 'w', encoding='utf-8', newline='').write(s)
        nfiles += 1; nrepl += len(edits)
print(f'localized {nfiles} files, {nrepl} replacements')
