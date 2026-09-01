# amis 本地渲染实验室

在本地渲染 amis JSON 配置，自带可控延迟的 mock 接口。用于验证 amis 运行时行为
（loading 时序、刷新机制、download 是否等待完成等），不依赖 GitHub、不依赖外网、无跨域问题。

## 快速开始

```powershell
cd e:\work_2026\skill-dev\_amis-lab
python server.py
```

浏览器打开 <http://localhost:8080>

停止服务：`Ctrl + C`

改端口（默认 8080 被占用时）：

```powershell
python server.py 9000
```

## 目录结构

```
_amis-lab/
├── index.html      # 渲染壳：加载本地 SDK，读取 schema.json 渲染。一般不用改
├── schema.json     # ★ 验证配置，改这里，刷新浏览器即可
├── server.py       # 静态服务 + mock API（带毫秒级时间戳日志）
├── schemas/        # 归档的验证配置，需要时复制回 schema.json
├── README.md       # 本文件
└── vendor/         # amis 6.13.0 SDK 全量文件，从淘宝镜像下载，已 gitignore
    ├── sdk.js      # ~2.0 MB  核心包 + 加载器
    ├── rest.js     # ~2.8 MB  渲染器主体，sdk.js 运行时自动请求，缺了会 404
    ├── sdk.css     # ~2.5 MB  默认样式
    ├── helper.css  # ~0.9 MB  辅助样式
    └── cxd.css / dark.css / antd.css / ang.css   # 主题样式，按需
```

> **`vendor/` 里的文件一个都不能少。** amis 的 SDK 是分包的：`sdk.js` 只是加载器，
> 运行时会自动去同目录拉 `rest.js`（体积比 `sdk.js` 还大）。只放 `sdk.js` + `sdk.css`
> 会导致控制台报 `vendor/rest.js` 404、组件渲染不全。

## 换一个验证项

只需要替换 `schema.json` 的内容，然后刷新浏览器。`index.html` 请求时带了时间戳参数，
不存在浏览器缓存问题。

已归档的配置放在 `schemas/`，需要复现时复制回来：

```powershell
copy schemas\v3-download-timing.json schema.json
```

| 归档文件 | 验证内容 |
|---|---|
| `v3-download-timing.json` | V-3：download action 是否等待下载完成 |
| `v1v2-loading-and-reload.json` | V-1 弹层 loading 变量能否生效 + V-2 `close:false` 下 `api.reload` 是否生效 |
| `v11-required.json` | V-11：required 校验链（required 与 isRequired 等价、0/全空格边界、ajax 跳过提交阻断、隐藏必填误拦截） |
| `v12-close-reload.json` | V-12：close 缺省 vs close:false 下 form api reload 是否生效（D-11 存废） |
| `v10-button-reload.json` | V-10：按钮级 reload 两形态（刷新专用按钮 target / 业务按钮顶层 reload） |

> `schema.json` 里接口地址写相对路径 `/api/mock2/sample`，和 amis 文档站的写法一致，
> 验证通过后可直接搬到真实项目，不用改。

## mock API

任何以 `/api/` 开头的请求都会被 mock 服务接管，返回 amis 标准响应结构：

```json
{ "status": 0, "msg": "ok", "data": { "count": 171, "total": 171, "rows": [...10 条...], "items": [...同 rows...] } }
```

| 参数 | 说明 | 示例 |
|---|---|---|
| `waitSeconds` | 延迟多少秒后返回，用来放大 loading / 时序行为 | `/api/mock2/sample?waitSeconds=3` |

支持 GET / POST / PUT / DELETE，请求体前 300 字符会打印到终端。

`rows` 和 `items` 都返回，所以 crud 和 form 都能直接用。

## 怎么观察时序

终端日志带毫秒时间戳，请求到达和响应各有一条：

```
[19:43:04.900] GET /api/mock2/sample  waitSeconds=1  请求到达
[19:43:05.902] GET /api/mock2/sample  waitSeconds=1  响应 2547B  <<< 此刻前端 loading 应结束
```

判定「某个 action 是否等待接口完成」，就看**前端 loading 结束的时刻**与
**`响应` 那条日志**是否对齐：

- 对齐 → 该 action 等待完成
- 前端 loading 早就结束了 → 该 action 不等完成，后续 action 会立刻执行

## 常见问题

**改了 schema.json 没变化**
确认服务器是在 `_amis-lab` 目录下启动的（`server.py` 把自身所在目录当根目录）。
另外检查终端有没有报 JSON 解析错误。

**页面空白 / 控制台报 `amisRequire is not defined`**
`vendor/sdk.js` 没加载成功。检查文件大小应约 2.0 MB，下载不完整就重新拉一次（见下）。

**控制台报 `vendor/rest.js` 404，或组件渲染不全**
`sdk.js` 运行时会自动请求同目录的 `rest.js`（约 2.8 MB，比 `sdk.js` 还大，包含渲染器主体）。
只放 `sdk.js` + `sdk.css` 不够，必须把 sdk 目录的文件全部下载，清单见「升级 amis 版本」。

**端口被占用**
`python server.py 9000` 换个端口，浏览器地址同步改。

**终端中文乱码**
`server.py` 已强制把 stdout 切到 UTF-8。若仍乱码，用 Windows Terminal 而非老版控制台。

**想看 amis 版本**
页面控制台执行 `amisRequire('amis').version`，SDK 固定为 6.13.0。

## 升级 amis 版本

重新下载两个 SDK 文件即可（走淘宝镜像，不走 GitHub）：

```powershell
$ProgressPreference='SilentlyContinue'
$dir = 'e:\work_2026\skill-dev\_amis-lab\vendor'
# 把 6.13.0 换成目标版本
# 注意：sdk.js 之外还有 rest.js 等文件，必须全部下载，否则运行时报 404
$files = @('sdk.js', 'rest.js', 'sdk.css', 'helper.css', 'cxd.css', 'dark.css', 'antd.css', 'ang.css')
foreach ($f in $files) {
  Invoke-WebRequest -Uri "https://registry.npmmirror.com/amis/6.13.0/files/sdk/$f" `
    -OutFile "$dir\$f" -UseBasicParsing
}
```

查最新版本号：

```powershell
(Invoke-WebRequest -Uri 'https://registry.npmmirror.com/amis/latest' -UseBasicParsing).Content |
  ConvertFrom-Json | Select-Object -ExpandProperty version
```

## 备注

- `vendor/` 已加入仓库根目录的 `.gitignore`（4.4 MB，不入库）
- 服务器用 `ThreadingHTTPServer` 多线程，延迟请求不会阻塞其它请求
- 本目录是长期资产，除 V-1/V-2/V-3 外，后续验证 amis-helper 的规则也在这里做
