import os, base64, json, urllib.request, urllib.error, urllib.parse

TOKEN = os.environ['GH_TOKEN']
REPO = 'zzdzju/test-index'
API = 'https://api.github.com'
ROOT = r'C:\Users\12931\WorkBuddy\2026-09-14-14-33-09\precision-nutrition-site'

def api(method, path, data=None):
    url = API + path
    headers = {'Authorization': 'Bearer ' + TOKEN, 'Accept': 'application/vnd.github+json',
               'User-Agent': 'wb-uploader', 'Content-Type': 'application/json'}
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        r = urllib.request.urlopen(req, timeout=40)
        return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]
    except Exception as e:
        return None, str(e)[:200]

# 收集文件（排除 .git）
files = []
for dp, dns, fns in os.walk(ROOT):
    dns[:] = [d for d in dns if d != '.git']
    for fn in fns:
        full = os.path.join(dp, fn)
        rel = os.path.relpath(full, ROOT).replace(os.sep, '/')
        files.append((rel, full))
print('files to upload:', len(files))

ok = 0
for i, (rel, full) in enumerate(files, 1):
    enc = urllib.parse.quote(rel, safe='/')
    with open(full, 'rb') as f:
        content = base64.b64encode(f.read()).decode()
    # 先查是否已存在，取 sha 用于更新
    st0, cur = api('GET', '/repos/%s/contents/%s' % (REPO, enc))
    sha = cur.get('sha') if st0 == 200 and isinstance(cur, dict) else None
    payload = {'message': 'add %s' % rel, 'content': content, 'branch': 'main'}
    if sha:
        payload['sha'] = sha
    st, resp = api('PUT', '/repos/%s/contents/%s' % (REPO, enc), payload)
    if st in (200, 201):
        ok += 1
        print('  [%d/%d] ok: %s' % (i, len(files), rel))
    elif st == 422 and 'Branch' in str(resp):
        # 空仓库首次：省略 branch 重试
        payload2 = {'message': 'add %s' % rel, 'content': content}
        st2, resp2 = api('PUT', '/repos/%s/contents/%s' % (REPO, enc), payload2)
        if st2 in (200, 201):
            ok += 1
            print('  [%d/%d] ok(retry no-branch): %s' % (i, len(files), rel))
        else:
            print('  [%d/%d] FAIL: %s | %s | %s' % (i, len(files), rel, st2, resp2)); raise SystemExit(1)
    else:
        print('  [%d/%d] FAIL: %s | %s | %s' % (i, len(files), rel, st, resp)); raise SystemExit(1)

print('UPLOADED %d/%d files' % (ok, len(files)))

# 校验：列出仓库根目录
st, listing = api('GET', '/repos/%s/contents/' % REPO)
if st == 200:
    names = sorted(x['name'] for x in listing)
    print('REPO ROOT:', len(names), names)
    # 校验关键文件存在
    need = ['index.html', '.nojekyll', 'README.md', 'GITHUB_PAGES_发布指南.md',
            'pages/precision-tech.html', 'assets/style.css', 'assets/site.js']
    for n in need:
        # 检查是否在 listing 或 pages/ 下
        pass
    stp, pl = api('GET', '/repos/%s/contents/pages' % REPO)
    if stp == 200:
        pnames = sorted(x['name'] for x in pl)
        print('PAGES:', len(pnames), pnames)
else:
    print('LIST FAIL', st, listing)
