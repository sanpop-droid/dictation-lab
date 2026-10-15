"""Add the 'เข้าใจง่ายใน 1 นาที' boxes (tools/easy.py) to the lesson files in exam/data.
Run after building or rebuilding any of those files:  python3 tools/add_easy.py
"""
import json, os
from examdata import D
from easy import EASY

def main():
    for key, table in EASY.items():
        path = os.path.join(D, key + '.js'); s = open(path, encoding='utf-8').read()
        pre = '(window.__X=window.__X||{})["%s"]=' % key
        assert s.startswith(pre), key
        data = json.loads(s[len(pre):].rstrip().rstrip(';'))
        ids = [L['id'] for L in data['lessons']]
        missing = [i for i in ids if i not in table]; extra = [i for i in table if i not in ids]
        assert not missing and not extra, (key, missing, extra)
        for L in data['lessons']:
            say, eg, rule = table[L['id']]
            L['easy'] = {'say': say, 'eg': list(eg), 'rule': rule}
        out = pre + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n'
        open(path, 'w', encoding='utf-8').write(out)
        print(key, len(ids), 'lessons', len(out.encode()), 'bytes')

if __name__ == '__main__':
    main()
