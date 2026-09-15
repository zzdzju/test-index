# 精准营养技术网 · GitHub Pages 发布指南

> 站点已通过 GitHub Pages 兼容性审计：纯静态（HTML/CSS/JS，无后端/无数据库/无构建）、
> 整站约 984K、全部链接为相对路径（挂在 `/repo名/` 子路径也不会断）、已加 `.nojekyll`。
> 结论：**完全适合 GitHub Pages 直接发布。**

---

## 一、本机已就绪（无需再装）

- ✅ **Git** 已装好并加入用户 PATH：`C:\Users\12931\.workbuddy\binaries\PortableGit\versions\1.2.0\cmd`
- ✅ **GitHub CLI (gh) v2.100.0** 已装好并加入用户 PATH：`C:\Users\12931\.workbuddy\binaries\gh\bin`
- ✅ **仓库已初始化并提交**：`precision-nutrition-site/` 已 `git init -b main` + 首次提交（35 个文件）
- ⚠️ **唯一需要你做的**：用你的 GitHub 账号授权一次（`gh auth login`），并把代码推上去。
  > 注：本机 WorkBuddy 沙箱代理挡掉了 `github.com` 的 git 推送（仅放行 `api.github.com`），
  > 所以**推送必须在你自己的终端跑**（你的真网络不被挡）。下面两行命令即在你终端执行。

---

## 一·五、排障：提示"gh 不是可运行的程序 / 找不到命令"

**现象**：`gh auth login` 报"不是可运行的程序"或 "'gh' 不是内部或外部命令"。

**原因**：`git`/`gh` 已正确写入**用户 PATH**（已验证 `C:\Users\12931\.workbuddy\binaries\gh\bin` 在 PATH 中，
`gh.exe` 也存在且可运行），但**你跑命令的那个终端窗口是在改 PATH 之前打开的，没刷新环境变量**。
Windows 改了用户 PATH 后，已打开的窗口不会自动继承，必须重开。

**两种解法（任选其一）**：

1. **重开终端（推荐）**：关掉当前窗口，新开一个 **PowerShell** 或 **cmd**，直接打 `gh auth login`。
   新窗口会从注册表读到刚加的 PATH，`gh` 和 `git` 都能直接用。

2. **不重开，当前窗口临时加 PATH**（会话级，关窗失效）：
   ```powershell
   # PowerShell
   $env:Path += ";C:\Users\12931\.workbuddy\binaries\PortableGit\versions\1.2.0\cmd;C:\Users\12931\.workbuddy\binaries\gh\bin"
   gh auth login
   ```
   ```bat
   :: cmd
   set PATH=%PATH%;C:\Users\12931\.workbuddy\binaries\PortableGit\versions\1.2.0\cmd;C:\Users\12931\.workbuddy\binaries\gh\bin
   gh auth login
   ```

3. **极稳妥兜底（完全不依赖 PATH）**：用 `gh.exe` 绝对路径直接跑：
   ```powershell
   & "C:\Users\12931\.workbuddy\binaries\gh\bin\gh.exe" auth login
   ```
> 注意：`gh repo create ... --push` 内部会再调用 `git`，若用绝对路径跑 gh，请务必确保当前窗口
> 的 PATH 里也有 git（用解法 1 重开终端最省心），否则建库推送那步会因找不到 git 失败。

---

## 一·六、授权时连接 github.com 超时（国内网络最常见）

**现象**：`gh auth login` 报
`failed to authenticate via web browser: Post "https://github.com/login/device/code": ... wsarecv: A connection attempt failed ...`

**原因**：`gh` 的「浏览器登录」流程要直连 `github.com`；而国内网络直连 `github.com` 经常超时。
浏览器能打开 GitHub，是因为浏览器走了**代理/梯子**那条出口；但命令行（cmd/PowerShell）没配代理，
`gh` 只能直连，于是超时。这是网络出口不一致，不是安装或 PATH 问题。

**解法 1（根因，推荐）— 给命令行配代理，让 gh 走浏览器同款出口**：

1. 看你本地代理软件（Clash / v2rayN / 小飞机 等）的 **HTTP 代理端口**（常见 `7890`、`10808`、`10809`）。
2. 在终端里设好再登录（cmd 与 PowerShell 写法不同）：

   ```bat
   :: cmd
   set HTTPS_PROXY=http://127.0.0.1:7890
   set HTTP_PROXY=http://127.0.0.1:7890
   gh auth login
   ```

   ```powershell
   # PowerShell
   $env:HTTPS_PROXY = "http://127.0.0.1:7890"
   $env:HTTP_PROXY  = "http://127.0.0.1:7890"
   gh auth login
   ```

3. **后续 `git push` 也吃这个代理**：`git` 同样直连 `github.com`，配了上面的环境变量后 push 就通；
   若仍超时，再给 git 单独指定代理：
   ```bat
   git config --global http.proxy http://127.0.0.1:7890
   git config --global https.proxy http://127.0.0.1:7890
   ```

**解法 2（绕过浏览器）— 用 Personal Access Token (PAT) 登录**：

1. 在**浏览器**打开 https://github.com → Settings → Developer settings →
   Personal access tokens → Tokens (classic) → **Generate new token**（勾选 `repo`，可选 `workflow`）。
2. 复制生成的 `ghp_xxx` token。
3. 终端执行 `gh auth login` → 选 **GitHub.com** → 选 **Paste an authentication token** → 粘贴。
   - 此模式仅向 `api.github.com` 验证，不走 `github.com` 浏览器流程；**但若 `api.github.com` 也直连超时，
     仍会失败，届时回到解法 1 配代理即可**。

> 经验：国内环境最稳的是**解法 1 配代理**——一次设好，授权和后续 push 全通；PAT 只是绕过浏览器的临时方案。

---

## 一·七、gh 认证成功，但 `gh repo create --push` 报 unable to find git executable

**现象**：`gh auth login`（PAT）已成功，执行 `gh repo create ... --push` 却报
`unable to find git executable in PATH; please install Git for Windows before retrying`。

**原因**：你是用 `gh.exe` **绝对路径**登录的（如 `& "C:\Users\12931\.workbuddy\binaries\gh\bin\gh.exe" auth login`），
该窗口 PATH 里只有系统原有项、**没有 git**，所以 `gh` 内部再调 `git` 时找不到。
（git 本体已装好：`C:\Users\12931\.workbuddy\binaries\PortableGit\versions\1.2.0\cmd\git.exe`）

**解法（在当前窗口直接补 git 到 PATH 再重试）**：

```powershell
# PowerShell（gh 认证状态在凭据管理器里，重开/加 PATH 都不丢，无需重新 login）
$env:Path += ";C:\Users\12931\.workbuddy\binaries\PortableGit\versions\1.2.0\cmd;C:\Users\12931\.workbuddy\binaries\gh\bin"
cd C:\Users\12931\WorkBuddy\2026-09-14-14-33-09\precision-nutrition-site
gh repo create precision-nutrition-site --public --source=. --remote=origin --push
```

```bat
:: cmd
set PATH=%PATH%;C:\Users\12931\.workbuddy\binaries\PortableGit\versions\1.2.0\cmd;C:\Users\12931\.workbuddy\binaries\gh\bin
cd /d C:\Users\12931\WorkBuddy\2026-09-14-14-33-09\precision-nutrition-site
gh repo create precision-nutrition-site --public --source=. --remote=origin --push
```

**更彻底**：重开一个系统自带的 PowerShell / cmd（已重新写入注册表 PATH 并广播刷新，git+gh 都在），
直接 `cd` 进目录跑 `gh repo create ... --push` 即可。

> 若 push 时又报连接 github.com 超时（国内网络），记得同一窗口先设代理（见一·六 解法 1）：
> `set HTTPS_PROXY=http://127.0.0.1:7890`（端口换成你本地代理软件显示的）。

---

## 一·八、gh repo create 报 "Resource not accessible by personal access token (createRepository)"

**成因**：你登录用的 PAT 权限不够，GitHub 创建仓库要求 token 具备建库权限：
- **classic token** 必须勾选 `repo`（含其下全部子项，不只是 `public_repo`）；
- **fine-grained token** 需在 Account permissions 里把 **Repository creation** 设为 **Read and write**。

gh 建库走 GraphQL `createRepository`，权限不足会直接拒绝，且仓库**不会被创建**（远程无脏数据，网页建库不会冲突）。

**推荐绕开（不重发 token）：网页建库 + 本地 git push**，网页建库不消耗 gh 的建库权限：

1. 浏览器打开 github.com → 右上角 **New repository**：
   - Repository name：`precision-nutrition-site`
   - 选 **Public**
   - **不要**勾 Add a README / .gitignore / license（保持空仓库）
   - 点 Create repository
2. 回到终端（新开窗口，PATH 含 git+gh）：

```bat
cd /d C:\Users\12931\WorkBuddy\2026-09-14-14-33-09\precision-nutrition-site
gh auth setup-git                      :: 让 git 复用 gh 的登录态，push 不弹凭据框
gh api user --jq .login                :: 查你的用户名，下面 URL 用
git remote add origin https://github.com/<你的用户名>/precision-nutrition-site.git
git branch -M main
git push -u origin main
```

> 若 push 报连接 github.com 超时（国内直连），同窗口先设代理：`set HTTPS_PROXY=http://127.0.0.1:7890`（端口换成你本地代理软件显示值）。

**路径 B（仍想用 gh 建库）**：去 GitHub 重新生成带 `repo` 全权限（或 fine-grained 开 Repository creation: write）的 PAT，再 `gh auth login` 重新粘贴，然后执行 `gh repo create precision-nutrition-site --public --source=. --remote=origin --push`。

---

## 一·九、git push 报 `remote: Permission to zzdzju/test-index.git denied` / 403

**成因**：仓库已存在（你在网页建的 `test-index`，私有），认证身份也是 `zzdzju` 本人，但**当前 gh 里存的 PAT 只有读/建库等部分权限，没有这个私有库的"内容写入"权**——GitHub 对私有库 push 要求 token 带 `repo`（即 contents read/write）。所以 `gh auth setup-git` 让 git 复用该 token 时，GitHub 直接返回 **403 Permission denied**。

**注意**：这是**权限**问题，不是网络、不是仓库名错（已实测 `origin` 正确指向 `.../zzdzju/test-index.git`）。

**修法（重新发一个带 `repo` 全权的 PAT，再重登录）**：

1. 浏览器打开 GitHub → **Settings → Developer settings → Personal access tokens**：
   - **classic token**（推荐，最省事）：Generate new token (classic)，**务必勾选 `repo`（整组，含其下全部子项，不要只勾 `public_repo`）**，过期按需设。
   - **fine-grained token**：在 **Repository permissions** 里把 **Contents** 设为 **Read and write**，并确认 **Metadata** 为 Read-only（默认即可）。
   - 复制生成的 `ghp_xxx`。
2. 终端重新登录（会覆盖旧 token）：
   ```bat
   gh auth login
   ```
   选 GitHub.com → 选 **Paste an authentication token** → 粘贴新 `ghp_xxx`。
3. 清掉可能缓存的旧凭据，再推：
   ```bat
   printf "protocol=https\nhost=github.com\n" | git credential reject
   cd /d C:\Users\12931\WorkBuddy\2026-09-14-14-33-09\precision-nutrition-site
   git push -u origin main
   ```
   > `origin` 已存在且指向正确，无需再 `git remote add`。若之前没跑过 `gh auth setup-git`，先跑一次再 push。

**成功标志**：终端出现 `main -> main` / `Writing objects: 100%` 且显示 `https://github.com/zzdzju/test-index.git`。

**预判**：push 直连 `github.com`，国内可能再超时。若报 `connection failed / timeout`，同窗口先设代理再重跑 `git push`：
`set HTTPS_PROXY=http://127.0.0.1:7890`（端口换成你本地代理软件显示值）。

---

## 一·十、git push 报 `Recv failure: Connection was reset` / `Connection timed out`

**成因**：403 已解决（说明 PAT 权限够了），现在卡在**网络**——本机直连 `github.com` 的 git 智能 HTTP 传输被中间网络重置（RST）。浏览器能开 GitHub ≠ git 能直连：浏览器走了你的代理/通道，而 git 默认**不走**系统代理，于是直连被拦。

**核心思路**：让 git 走你已经可用的那条代理通道（你浏览器能上 GitHub，说明通道是通的）。

**首选：给 git 配代理（最稳，一次性设置）**

先确认你本地代理软件的端口与类型（看软件界面 "Port / 端口"）：
- Clash / Clash Verge：默认 **7890**（HTTP 混合同端口）或 SOCKS 7891
- v2rayN：默认 **10808**（SOCKS5）/ HTTP 10809
- Shadowsocks：默认 **1080**（SOCKS5）

```bat
:: 情况 A：HTTP 代理（Clash 7890、v2rayN HTTP 10809 等）
git config --global http.proxy  http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890

:: 情况 B：SOCKS5 代理（v2rayN 10808、SS 1080 等）
git config --global http.proxy  socks5://127.0.0.1:10808
git config --global https.proxy socks5://127.0.0.1:10808

cd /d C:\Users\12931\WorkBuddy\2026-09-14-14-33-09\precision-nutrition-site
git push -u origin main
```
（上面端口按你软件实际值改；`--global` 是全局生效，之后所有 git 仓库都走代理。只想本仓库走代理就去掉 `--global` 在该仓库目录执行。）

**备选：SSH 走 443 端口（绕过被拦的 22 / 直连 HTTPS）**

若代理法仍不稳，改用 SSH over 443（GitHub 的 `ssh.github.com:443` 通常不被重置）：
1. 生成密钥（一路回车）：`ssh-keygen -t ed25519 -C "you@example.com"`
2. 复制公钥：`type %USERPROFILE%\.ssh\id_ed25519.pub`，到 GitHub → Settings → SSH and GPG keys → New SSH key 粘贴。
3. 改远程为 SSH + 强制 443：
   ```bat
   git remote set-url origin git@github.com:zzdzju/test-index.git
   ```
4. 新建/编辑 `C:\Users\12931\.ssh\config`，写入：
   ```
   Host github.com
     Hostname ssh.github.com
     Port 443
   ```
5. `git push -u origin main`（首次会问 yes，输入 `yes`）。

**再备选：API 直传（无需你本机网络通 github.com）**

若你本机无论代理/SSH 都不通，可把仓库改成**仅能写这一个仓库**的 fine-grained token 交给我，我从能通 `api.github.com` 的通道用 Contents API 把 35 个文件逐个 PUT 上去。**代价**：需把 token 交给我（凭据安全由你定），且该 token 务必限定最小权限。

---

## 二、发布步骤（在你自己的终端里执行，2 行搞定）

> 请**新开一个终端窗口**（让上面加好的 git/gh 生效），`cd` 到站点目录：
> `cd C:\Users\12931\WorkBuddy\2026-09-14-14-33-09\precision-nutrition-site`

```bash
# 1) 用你的 GitHub 账号授权（弹出浏览器，选 GitHub.com / HTTPS / 网页登录授权）
gh auth login

# 2) 建仓库 + 推送一步到位（仓库名 precision-nutrition-site，公开）
gh repo create precision-nutrition-site --public --source=. --remote=origin --push
```

> 若不用 gh（改用网页建库）：在 github.com 右上角 New repository，仓库名填
> `precision-nutrition-site`、**不要**勾 README；然后执行
> `git remote add origin https://github.com/<你的用户名>/precision-nutrition-site.git`
> 与 `git push -u origin main` 即可。

推送完成后仓库即建好、代码已就位、等待部署。

---

## 三、开启 GitHub Pages

推送成功后：

- **最快**：上述 `gh repo create` 已建好仓库。再执行一次 Pages 设置（或直接在网页点）：
  ```bash
  gh api repos/<你的用户名>/precision-nutrition-site/pages \
    --method POST -f source='{"branch":"main","path":"/"}' \
    -f build_type=legacy 2>/dev/null \
    || echo "请到网页 Settings → Pages 手动选 main / root"
  ```
- **稳妥（推荐新手）**：打开 `https://github.com/<你的用户名>/precision-nutrition-site`
  → **Settings** → **Pages** → Source 选 **Deploy from a branch** → Branch 选 **main**、
  folder 选 **/ (root)** → **Save**。

等待约 1–2 分钟（首次部署稍慢），访问：

```
https://<你的用户名>.github.io/precision-nutrition-site/
```

---

## 四、两种站点形态（相对路径都兼容，无需改代码）

| 形态 | 仓库名 | 访问地址 | 说明 |
|---|---|---|---|
| 项目站（推荐） | `precision-nutrition-site` | `https://<用户>.github.io/precision-nutrition-site/` | 最简单，本指南默认 |
| 用户/组织站 | `<用户>.github.io` | `https://<用户>.github.io/` | 仓库必须叫这个，站点直接挂根域名 |

---

## 五、上线前必改的占位（公开前请补齐）

| 位置 | 当前占位 |
|---|---|
| 页脚 地址 / 电话 / 邮箱 | 北京市××区××路××号、010-XXXX XXXX、service@example.com |
| 页脚 二维码 | 程序生成的**假码图形**，需替换为真实微信二维码 |
| 页脚 备案号 | 京ICP备XXXXXXXX号-1、京公网安备 110105XXXXXXXX号 |
| 证书页 / 图书页 | 【占位】证书名称、书名 |
| 文章页正文 | 仅主题框架，待填 |

> 文案集中在 `build.py` 顶部的 `CONTENT` 字典，改完运行 `python build.py` 整站重建，
> 然后再 `git add -A && git commit -m "更新内容" && git push`。

---

## 六、已知限制（发布后依然存在的）

1. **顾客咨询表单不会真正收到留言**：`site.js` 里表单提交只做本地"提交成功"提示，
   无后端。上线后需用以下任一方案接真接收件：
   - Formspree / 腾讯问卷（前端表单直连，免后端）；
   - 或挂到你那台腾讯轻量云（111.231.5.254）的接口。
2. 本站为健康科普展示，**不构成医疗建议**（页脚已标注）。

---

## 七、更新内容后重新发布

```bash
git add -A
git commit -m "更新：xxx"
git push
```

GitHub Pages 会在推送后自动重新部署（通常几十秒内生效）。
