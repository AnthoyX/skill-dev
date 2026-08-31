# amis-helper 迭代进化路线图

| 项 | 值 |
|---|---|
| 文档版本 | v1.1（补充实测结论，修正 P0-1 定性） |
| 评审日期 | 2026-08-31 |
| 评审对象 | `amis-helper` v1.0.0（SKILL.md + 5 references + 3 examples，共 957 行） |
| 路线图覆盖 | v1.1（止血）→ v1.2（提质/提命中）→ v2.0（扩能力/建机制） |
| 状态 | 待评审 |
| 实测环境 | amis 6.13.0，本地实验室 `_amis-lab/` |
| 实测进展 | V-1 ✅ / V-1-D ✅ / V-3 ✅ / V-2 ⏳ 待补（见 §5.1） |

---

## 0. 结论摘要

这个 skill 的**选题和结构是对的**：渐进式加载、硬规则前置、examples 兜底，方向没问题。但通读完 957 行后发现三类硬伤：

**A. 「loading 防重复」三件套是死配置**（原判 P0，**实测后降为 P1**）

整个 skill 主打的「弹层提交 loading 防重复」（硬规则 R4、`dialog-actions.md §1`），在其标准模式和 `crud-full.json` 全套示例里，**loading 变量从未被置为 `true`**——只有 `submitSucc` 里的 `setValue false`。

> **【2026-08-31 实测修正，amis 6.13.0】** 原判断「点提交后无任何反馈 → 只能反复点击 → 实际制造了重复提交」**不成立**。
> 四组对照实验（A `loadingOn` 置 true / B `loadingOn` 恒 false / C 不带 `loadingOn` / D 接口失败）显示：
> **A、B、C 三组提交均正常转圈**——amis 的 submit 按钮有**内建 loading**，`loadingOn` 为 false 也压不住它。
> D 组（接口返回 `status=1`）：loading 正常结束、弹层保持打开、可再次提交，**失败分支完全正常**。

所以真实问题不是「会产生运行时故障」，而是：`loadingOn` + Service 变量 + `setValue` 这**三件套从未起过作用**，是纯冗余配置，且让规则描述与运行时行为不符、示例误导读者。**v1.1 的处理是删掉它，而不是补全它。**

**例外**：导出按钮（`onEvent.click` + `download`）不适用此结论——`download` 没有内建 loading，其 `loadingOn` + `setValue` 是必要的，实测有效（见 V-3）。

**B. 规则冗余到 100%，且已经产生自相矛盾**
SKILL.md 的 10 条硬规则，**每一条**都在 `pitfalls.md` 或 references 里有重述（多数三处）。因为有多份副本，它们已经开始打架——最典型的是 `api.reload` 到底该不该写、写了生不生效，三份文件给出三种说法。

**C. 缺版本锚定，规则不可迁移也无法验证**
`pitfalls.md` 写了「此 AMIS 版本不执行」、`form-controls.md` 写了「该 AMIS 版本无此内置 CSS 类」，但整个 skill 没有任何地方声明它对应 amis 哪个版本。版本不明，规则的可信度无从判断，换项目也不敢复用。

**建议节奏**：v1.1 修 A 与 B 的矛盾项（止血，改动小、收益大），v1.2 做结构化的单一事实源重构，v2.0 再谈扩能力域和自进化机制。**在 V-2 结论出来前不建议扩能力域**——在尚未验证的核心规则上叠加更多场景，只会把不确定性放大。

> **实测的价值已得到验证**：本文档 v1.0 基于静态阅读给出的 P0-1 判断（「必然诱发重复提交」）
> 被实测推翻。这恰恰说明「先实测后动笔」必须排在第一步——**静态阅读能发现结构问题，
> 但判断不了运行时行为**。

---

## 1. 现状盘点

### 1.1 体量与结构

| 层 | 文件 | 行数 | 占比 | 加载时机 |
|---|---|---:|---:|---|
| 入口 | `SKILL.md` | 52 | 5.4% | 每次命中必读 |
| 规范 | `references/dialog-actions.md` | 138 | 14.4% | 生成弹层/动作时 |
| 规范 | `references/form-controls.md` | 109 | 11.4% | 生成表单时 |
| 规范 | `references/crud.md` | 103 | 10.8% | 生成 crud 时 |
| 规范 | `references/pitfalls.md` | 59 | 6.2% | 自检/排查时 |
| 规范 | `references/data-source.md` | 54 | 5.6% | 对接接口时 |
| 示例 | `examples/crud-full.json` | 334 | 34.9% | 需整页骨架时 |
| 示例 | `examples/bulk-actions-picker.json` | 59 | 6.2% | 需选择器时 |
| 示例 | `examples/dialog-confirm-loading.json` | 49 | 5.1% | 需确认弹层时 |
| **合计** | | **957** | 100% | |

结构上是清晰的四层（入口 / 规范 / 排障 / 示例），但**示例层占了 46.2%**，其中单个 `crud-full.json` 就占 34.9%。这是一次性加载的最大成本项。

### 1.2 规则资产盘点

| 来源 | 条目数 | 说明 |
|---|---:|---|
| `SKILL.md` 硬规则 | 10 | R1–R10，标注为「违反任意一条=返工」 |
| `SKILL.md` 决策表 | 12 | 场景→组件→反模式 |
| `pitfalls.md` 排障条目 | 13 | P1.1–P1.7、P2.1–P2.4、P3.1–P3.2、P4.1、P5.1 |
| references 内嵌规则 | ~30 | 分散在各 `§` 小节的「规则：」段落 |
| **规则总条目（去重前）** | **~65** | |

### 1.3 冗余度实测：10 条硬规则全部有副本

| 硬规则 | 副本位置 | 副本数 |
|---|---|---:|
| R1 禁止 JSON 注释 | `pitfalls.md P5.1` | 2 |
| R2 `perPageAvailable` 放顶层 | `pitfalls P3.1`、`crud.md §1` | 3 |
| R3 reload 用 `componentId` | `pitfalls P1.3`、`dialog-actions.md §3`、`crud.md §9` | 4 |
| R4 `close:false` + `submitSucc` 关弹层 | `pitfalls P1.1`、`pitfalls P1.2`、`dialog-actions §1` | 4 |
| R5 下载用 `actionType: download` | `pitfalls P1.6`、`pitfalls P1.7`、`dialog-actions §2` | 4 |
| R6 `autoComplete` 必须是对象 | `pitfalls P2.1`、`pitfalls P2.4`、`form-controls §3` | 4 |
| R7 `asBlob` + `form-data` 成对 | `form-controls §5` | 2 |
| R8 宽度只认 `columnRatio` | `pitfalls P4.1`、`form-controls §6` | 3 |
| R9 统计条用 `tpl` 不用 `statistics` | `pitfalls P3.2`、`crud.md §2` | 3 |
| R10 非标准响应用 adapter | `data-source.md §2`、`crud.md §3` | 3 |

**硬规则重复率 = 10/10 = 100%**。平均每条规则存在 3.2 份副本。

---

## 2. 问题诊断

按严重度排序。P0 = 会导致生成错误配置，P1 = 会导致规则冲突或维护失控，P2 = 规范性与可维护性瑕疵。

### P0-1（经实测降级为 P1，编号保留以免全文引用失效）「loading 防重复」三件套是死配置

**位置**：`SKILL.md` R4、`dialog-actions.md §1`、`examples/crud-full.json`（Import/Add/Edit 三个弹层）、`examples/dialog-confirm-loading.json`

**事实**：`crud-full.json` 中所有 `setValue` 调用的完整清单——

| 行号 | 设置 | 值 |
|---|---|---|
| 105 | `formLoading` | `false` |
| 112 | `formLoading` | `false` |
| 181 | `formLoading` | `false` |
| 188 | `formLoading` | `false` |
| 231 | `exportDownloading` | `true` |
| 245 | `exportDownloading` | `false` |
| 297 | `formLoading` | `false` |
| 304 | `formLoading` | `false` |

三个弹层的 `formLoading` **只有 `false`，从未有 `true`**。`dialog-actions.md §1` 的标准模式同样只示范了 `submitSucc` 里的 `setValue false`，没有交代在哪里置 `true`。

**原推断的后果链（已被实测推翻）**：

1. ~~`loadingOn` 变量恒为 `false` → 按钮永远不进入 loading 态~~
2. ~~`close: false` 阻止弹框自动关闭~~
3. ~~用户点击后无任何视觉反馈 → 再点一次 → 重复提交~~

**实测结论**（amis 6.13.0，2026-08-31）：

| 组 | 提交按钮配置 | 结果 |
|---|---|---|
| A | `loadingOn` + `onEvent.click` 置 `true` | 转圈 |
| B | `loadingOn` 恒 `false`（skill 现状） | **也转圈** |
| C | 不带 `loadingOn` | 也转圈 |
| D | 接口失败（`status=1`） | loading 正常结束 / 弹层保持打开 / 可再次提交 |

**submit 按钮有 amis 内建 loading，`loadingOn` 无法禁用它。** 因此「点了没反应」不会发生，原判断的「必然诱发重复提交」不成立。

**修正后的定性**（P0 → P1）：

- 不产生运行时故障，但**配置冗余无效**——三件套写了等于没写
- **规则描述与运行时行为不符**——`dialog-actions.md §1` 把 `loadingOn` 写成必需要素，实际它不是
- **示例误导**——照抄的开发者会以为自己在控制 loading，实际是内建行为兜底

**v1.1 处理**：弹层提交按钮**删掉** `loadingOn` + Service 变量 + `setValue`，**保留** `close: false`（否则弹层秒关，loading 看不见）。导出按钮的 `loadingOn` 保留。详见 §5.1 改动项 1.1.1。

### P0-2 examples 之间存在组合性断裂

**位置**：`examples/dialog-confirm-loading.json` vs `examples/crud-full.json`

`dialog-confirm-loading.json` 使用 `loadingOn: "${deleteLoading}"` 并向 `pageStateService` 写 `deleteLoading`；但 `crud-full.json` 的 Service `data` 只声明了：

```json
"data": { "exportDownloading": false, "formLoading": false }
```

**`deleteLoading` 未被声明**。把该确认弹层挂到 `crud-full.json` 的 operation 列（这正是文件索引暗示的用法），`deleteLoading` 取值为 `undefined` → 恒 falsy → loading 失效，且同样叠加 P0-1 的「从未置 true」问题。

三个 example 之间的宿主依赖（Service id、crud name、变量声明）**没有任何地方声明**，目前靠读者自己拼。

### P0-3 `api.reload` 规则三处自相矛盾

同一件事，三份文件三种说法：

| 出处 | 说法 |
|---|---|
| `crud.md §9` | 「弹层默认模式（提交后自动关）→ form api 里加 `"reload": "目标crud的name"`」——列为主推写法 |
| `dialog-actions.md §1` | 「`close: false` 模式下 form api 的 `reload` 不生效，**可省略**；examples 中 api.reload 保留仅作"语义标记"，不影响功能」 |
| `crud.md §9` 第二行 | 「`close: false` 模式 → api.reload 不生效，**必须**在 `submitSucc` 里显式 reload」 |
| `examples/crud-full.json` | 三处弹层 form api **都写了** `"reload": "mainCrud"`，但这些弹层**都是** `close: false` 模式 |

矛盾点：如果 `close:false` 下 `api.reload` 确实无效，那么 `crud-full.json` 里三处 `"reload": "mainCrud"` 就是死代码——而它恰恰是模型最容易抄的示例。规则说「可省略」，示例却全写上，模型必然学到不一致的行为。

附带问题：「仅作语义标记」这个说法本身是个坏味道——在无副作用的死配置上加语义注释，会误导读者以为它有用。

### P1-1 规则 100% 冗余，且已开始漂移

见 §1.3 实测。当前处于「多份副本内容恰好还一致」的脆弱平衡，P0-3 就是漂移的第一个实例。任何一次局部修改都可能制造新的矛盾，且**没有机制能发现**。

### P1-2 `adapter` / `adaptor` 双轨命名

- `data-source.md §2`：写「adapter 或 adaptor 均有效，官方标准名是 adaptor」
- `SKILL.md` R10：写「`adapter`/`adaptor`」
- `crud-full.json`：用的是 `adapter`
- `form-controls.md §1`：用的是 `adaptor`

规则没给出取舍标准，示例两种都用 → 模型随机选。既然认定官方标准名是 `adaptor`，就应在规则里明确「优先 `adaptor`」并统一示例。

### P1-3 缺 amis 版本锚定

以下条目强依赖版本，但全 skill 无版本声明：

- `pitfalls P2.2`：「adapter 字符串转换在**此版本**不可用（报 invalid label）」
- `form-controls §6`：「`inputClassName: "w-xl"` → **该 AMIS 版本**无此内置 CSS 类」
- `form-controls §3`：「**adapter 字符串转换在此版本不可用**，勿选」

后果：
1. 换项目/升级 amis 后，无法判断哪些规则已失效
2. 读者无法评估规则可信度——这是官方行为还是某个版本的偶发行为？
3. 无法向他人推荐这个 skill（不知道适用谁）

### P1-4 文档示例自带注释，与 R1 直接冲突

`data-source.md §1`、`§2` 的代码块里用了 `//` 行注释：

```json
// 1. 字符串简写（GET）
"api": "/XXX/XXXX/list"
```

而 R1（`SKILL.md` 第 17 行）要求「JSON 内禁止注释」，P5.1 进一步说明「配置内禁止注释，说明写在配置外的文档里」。

虽然是 `.md` 里的示例代码块，不是可加载的 schema，但这正是规则污染的典型路径——模型在模仿示例时不会区分「这是文档示意」和「这是生成物格式」。建议文档示例改用表格或编号标题，避免出现 `//`。

### P2-1 frontmatter `allowed-tools` 为空值

`SKILL.md` 第 5 行 `allowed-tools:` 后面没有任何内容。要么显式列出（如 `Read, Grep, Glob`），要么删除该字段。

### P2-2 交叉引用风格不统一

三种写法混用：

- `SKILL.md`：`references/crud.md §1`（全路径 + 章节号）
- `dialog-actions.md`：`pitfalls P1.4`、`§4`（无路径）
- `crud.md`：`data-source.md §2`（有路径）

跨文件引用没有路径，读者（和模型）需要猜。

### P2-3 examples 宿主依赖未标注

- `dialog-confirm-loading.json` 依赖：Service `id=pageStateService`、crud `id=mainCrud`、变量 `deleteLoading`
- `bulk-actions-picker.json` 的 `"reload": "mainCrud"` 指向一个**不在本文件内**的父 crud，作为独立片段加载时该引用悬空

`SKILL.md` 的 examples 索引表只有「场景」和「覆盖点」两列，没有「宿主依赖」。

### P2-4 若干待验证表述

- `crud.md §4`：「`columns-toggler`、`drag-toggler` 需要 crud 设 `"columnsToggled": true` **类配置**时使用」——`columnsToggled` 是否为真实属性名存疑，「类配置」表述含糊
- `dialog-actions.md §2`：「`download` action 返回 Promise（顺序 action 会等待完成）」——若 download 触发浏览器下载后立即返回，则 `setValue false` 会瞬间执行，Export 的 loading 毫无意义。这与 P0-1 同属「loading 时序」问题，需一并实测
- `form-controls §3`：「推荐后端适配……此方案需后端改造，前端无法独立完成」——这条其实是**协作约束**，混在前端规则里，容易被当成可选建议忽略

### P2-5 无变更记录、无验证状态

- `version: 1.0.0` 但没有 CHANGELOG，无法知道某条规则是何时、因何加入
- 没有任何规则标注验证状态（已实测 / 据官方文档 / 实战观察 / 待验证）
- 目前**只有 P3.1 一条**有明确依据来源（「amis-ui BasicPaginationProps 接口定义，官方 issue #6685」），其余 9 条硬规则无出处

---

## 3. 进化目标与原则

五条原则，贯穿三个版本：

**原则 1：单一事实源（SSOT）**
每条规则在 skill 内**只有一个权威定义位置**，其余位置只做 ID 引用。SKILL.md 的硬规则表降级为「ID + 一句话 + 指向」，不再复述细节。

**原则 2：每条规则可溯源**
每条规则强制带三段元数据：来源（官方 issue / 接口定义 / 实战观察 / 推断）、验证状态（已实测 / 待验证）、适用版本。无来源的规则不允许进入硬规则层。

**原则 3：版本锚定**
frontmatter 显式声明 amis 版本范围，所有版本敏感规则标注版本约束。版本外的使用场景需显式提示风险。

**原则 4：生成物可自检**
提供一份正向自检清单，模型生成完配置后逐条过，而不是等出问题再查 `pitfalls.md`。

**原则 5：能力域可扩展**
规则按能力域组织（crud / dialog / form / api / 未来新增 chart、permission、mobile），新增域 = 新增一个 reference + 决策表若干行，不动既有结构。

---

## 4. 目标架构（v2.0 完成时）

### 4.1 目录结构

```
amis-helper/
├── SKILL.md                    # 入口：硬规则索引 + 决策表 + 触发矩阵 + 自检清单
├── CHANGELOG.md                # 版本变更记录
├── META.md                     # 版本锚定、适用范围、规则统计、编写规范
├── references/
│   ├── crud.md                 # 域：列表页
│   ├── dialog-actions.md       # 域：弹层与动作
│   ├── form-controls.md        # 域：表单控件
│   ├── data-source.md          # 域：接口与数据源
│   ├── <新域>.md               # v2.0 扩展：chart / permission / mobile ...
│   ├── pitfalls.md             # 排障：只写症状与诊断，不重复正确写法
│   └── self-check.md           # 自检清单（正向，生成后逐条过）
├── examples/
│   ├── crud-full.json
│   ├── dialog-confirm-loading.json
│   ├── bulk-actions-picker.json
│   └── INDEX.md                # 依赖声明、覆盖点、行数
└── tests/
    ├── README.md               # 回归用例规范
    └── cases/                  # 需求 → 断言点 → 反模式
        ├── 001-crud-list.md
        ├── 002-dialog-submit-loading.md
        └── ...
```

### 4.2 分层职责

| 层 | 职责 | 是否含正确写法 |
|---|---|---|
| 硬规则层（SKILL.md） | ID + 一句话 + 指向 | ❌ 只索引 |
| 域规范层（references/*.md） | **唯一**的权威写法 + 元数据 | ✅ 唯一来源 |
| 排障层（pitfalls.md） | 症状 + 错误写法 + **规则 ID 引用** | ❌ 只引用 |
| 示例层（examples/） | 可直接落地的完整配置 | ✅ 且与规则一致 |
| 验证层（tests/） | 需求 → 断言点 → 反模式 | ❌ 只断言 |

### 4.3 规则 ID 体系

| 前缀 | 域 | 所在文件 |
|---|---|---|
| `R-xx` | 跨领域硬规则（必查） | `SKILL.md` 索引，定义在对应域文件 |
| `C-xx` | CRUD / 列表 | `references/crud.md` |
| `D-xx` | 弹层 / 动作链 | `references/dialog-actions.md` |
| `F-xx` | 表单控件 | `references/form-controls.md` |
| `A-xx` | 接口 / 数据源 | `references/data-source.md` |
| `P-xx` | 排障条目 | `references/pitfalls.md` |

映射示例（重构后）：

| 现硬规则 | 新 ID | 权威定义位置 |
|---|---|---|
| R2 分页切换器 | `C-01` | `crud.md §1` |
| R3 reload 用 componentId | `D-03` | `dialog-actions.md §3` |
| R4 弹层提交 loading | `D-01` | `dialog-actions.md §1` |
| R5 下载用 download | `D-02` | `dialog-actions.md §2` |
| R6 autoComplete 对象 | `F-03` | `form-controls.md §3` |
| R8 宽度只认 columnRatio | `F-06` | `form-controls.md §6` |
| R9 统计条用 tpl | `C-02` | `crud.md §2` |
| R10 adapter 转换 | `A-02` | `data-source.md §2` |
| R1 禁注释 / R7 上传 | `R-01` / `F-05` | `META.md` / `form-controls.md §5` |

`pitfalls.md` 的 13 条全部改写为「症状 → 错误写法 → 见 `X-xx`」，不再重复正确写法。

### 4.4 体量预算

| 文件 | 上限 | 理由 |
|---|---:|---|
| `SKILL.md` | 60 行 | 每次命中必读 |
| 单个 reference | 120 行 | 单次加载成本可控 |
| 单个 example | 150 行 | 示例层是最大成本项 |
| 全 skill 总量 | 800 行 | 为 v2.0 新增能力域预留空间 |

当前 `crud-full.json`（334 行）超出预算 2.2 倍，v1.2 需处理。

---

## 5. 分版本路线图

### 5.1 v1.1 — 止血（修正确）

**目标**：消除会产生错误配置的缺陷，统一矛盾说法。**不重构结构**，改动量最小。

**实测结论**（amis 6.13.0，本地实验室 `_amis-lab/`，2026-08-31）：

| # | 验证项 | 结论 | 影响 |
|---|---|---|---|
| V-1 | submit 按钮声明 `loadingOn` 后，内建 loading 是否失效？ | ✅ **内建 loading 始终有效**，`loadingOn` 恒 false 也照常转圈 | `D-01` 应**删掉** `loadingOn` 三件套，而非补全 |
| V-1-D | 接口失败时 loading 是否正常结束、能否重试？ | ✅ 2 秒后 loading 消失 / 弹层保持打开 / 可再次提交 | 失败分支无需额外处理 |
| V-3 | `download` 是否等待下载完成才执行后续 action？ | ✅ **等待**（`waitSeconds=3` 实测 loading 持续 3 秒） | Export 的 `loadingOn` 写法**有效，保留** |
| V-2 | `close: false` 下 form api 的 `reload` 是否生效？ | ⏳ **待补** | 决定 `crud-full.json` 三处 `"reload"` 删还是留 |

> **V-2 判定方法**：终端日志中，每提交一次后是否**新增一条 `GET /api/mock2/sample`**。
> `POST` 是表单提交本身，不算；只看 `GET`（crud 刷新）。
> 若 A 组（带 `reload`）有而 B 组（不带）无 → `api.reload` 有效；
> 若两组都有 → 刷新是弹层提交的默认行为（官方 crud 文档「增」章节），`api.reload` 冗余。

**改动项**

| # | 改动 | 对应问题 |
|---|---|---|
| 1.1.1 | **删除**弹层提交的 `loadingOn` 死配置：`dialog-actions.md §1` 写明「submit 按钮有内建 loading，无需 `loadingOn`」；`crud-full.json` 三个弹层与 `dialog-confirm-loading.json` 删除 `loadingOn`、Service `data` 中的 `formLoading`/`deleteLoading` 声明、`submitSucc`/`submitFail` 里的 `setValue`。**保留 `close: false`**；**导出按钮的 `loadingOn` 保留**（V-3 证实有效） | P0-1 |
| 1.1.2 | 修复 examples 组合断裂：统一变量命名与 Service `data` 声明；在 `SKILL.md` examples 索引增加「宿主依赖」列 | P0-2 |
| 1.1.3 | 统一 `api.reload` 说法：三处文件给出同一结论；`crud-full.json` 中无效的三处 `"reload"` 按 V-2 实测结果删除或加注 | P0-3 |
| 1.1.4 | `adapter`/`adaptor` 统一为 `adaptor`（官方标准名），同步 `crud-full.json` | P1-2 |
| 1.1.5 | 新增 `META.md`：声明 amis 版本范围、适用项目类型、不适用边界；`SKILL.md` frontmatter 增加 `amis-version` 字段 | P1-3 |
| 1.1.6 | `data-source.md` 示例代码块去掉 `//` 注释，改用编号标题 + 表格 | P1-4 |
| 1.1.7 | frontmatter `allowed-tools` 补全或删除 | P2-1 |
| 1.1.8 | 修正 `reload` 的 `target` 作用域：R3 与 `dialog-actions.md §3` 需说明 `target` 仅在**事件动作**（`onEvent.actions`）内失效；`{"type":"action","actionType":"reload","target":"crudName"}` 是官方支持的合法写法，不应一律判错 | 官方冲突 1 |
| 1.1.9 | 删除 `crud.md §4` 中不存在的 `columnsToggled` 属性；`columns-toggler` 可直接使用，需要额外开关的是 `filter-toggler`（对应 `filterTogglable`） | 官方冲突 2 |
| 1.1.10 | `dialog-actions.md §1` 补充说明：弹层 form 提交后**默认自动刷新 CRUD**（官方 crud 文档「增」章节），可用 `reload: "none"` 关闭 | 官方冲突 3 |

**验收标准**

- [ ] 删掉 `loadingOn` 后，把 `crud-full.json` 导入 amis 编辑器，点 Import/Add/Edit 提交按钮**仍出现 loading**（依赖内建），提交完成后弹框关闭
- [ ] 接口失败时：loading 正常结束、弹层保持打开、可再次提交，且**无需任何 `setValue` 配合**
- [ ] `crud-full.json` 中不再有 `formLoading` / `deleteLoading` 等只为 loading 存在、从未生效的变量声明
- [ ] 导出按钮的 `loadingOn` + `setValue` **保留**，实测仍有 loading
- [ ] 把 `dialog-confirm-loading.json` 挂到 `crud-full.json` 的 operation 列，无需任何修改即可正常工作
- [ ] 全文检索 `api.reload`、`adaptor`、`loadingOn`、`target`，各文件说法一致，无相互矛盾
- [ ] `META.md` 中存在明确的 amis 版本号或版本范围
- [ ] 所有 `.md` 文档的代码块中不含 `//` 注释
- [ ] V-2 实测结论已回填本文档

**预估**：5 个文件改动，其中 `crud-full.json` 改动约 8 处。

---

### 5.2 v1.2 — 提质 + 提命中（结构化）

**目标**：消灭冗余，建立可维护的规则体系，让模型可靠地读到正确内容。

**改动项**

| # | 改动 | 对应问题 |
|---|---|---|
| 1.2.1 | 为全部 ~65 条规则分配唯一 ID（`R-/C-/D-/F-/A-/P-`），建立映射表 | P1-1 |
| 1.2.2 | `SKILL.md` 硬规则表降级为索引表（ID + 一句话 + 指向），删除所有细节复述 | P1-1 |
| 1.2.3 | `pitfalls.md` 13 条改写：只保留「症状 + 错误写法 + 见 `X-xx`」，删除全部正确写法复述 | P1-1 |
| 1.2.4 | 每条规则补三段元数据：来源（官方 issue# / 接口定义 / 实战观察 / 推断）、验证状态（已实测 / 待验证）、适用版本 | P2-5 |
| 1.2.5 | 新增 `references/self-check.md`：生成后正向自检清单，按域分组，每条指向规则 ID | 原则 4 |
| 1.2.6 | `SKILL.md` 增加**触发矩阵**：命中关键词 → 必读文件，规定「命中即读，不得凭记忆作答」 | 原则 D |
| 1.2.7 | 交叉引用统一为 `references/<file>.md §N` 全路径格式 | P2-2 |
| 1.2.8 | 新建 `examples/INDEX.md`：声明每个 example 的宿主依赖、覆盖规则 ID、行数 | P2-3 |
| 1.2.9 | `crud-full.json` 处理到 150 行预算内（方案见 §6.6 开放问题 Q3） | §4.4 |
| 1.2.10 | 清理待验证表述：`columnsToggled` 实测或删除；后端协作项单独归类为「协作约束」 | P2-4 |
| 1.2.11 | 新增 `CHANGELOG.md`，记录 v1.1/v1.2 变更 | P2-5 |

**验收标准**

- [ ] 硬规则重复率从 100% 降至 0%（每条规则在全文只有一处正确写法）
- [ ] 100% 的规则带来源标注；`待验证` 状态的规则不超过 20%
- [ ] `pitfalls.md` 中不含任何完整正确写法代码块（只有 ID 引用）
- [ ] 触发矩阵覆盖全部 5 个 reference，关键词无歧义
- [ ] 全部 example 行数 ≤ 150
- [ ] 交叉引用 100% 使用全路径格式，且无失效引用

---

### 5.3 v2.0 — 扩能力 + 建机制（能力化）

**目标**：从「一份写好的清单」进化为「可持续生长的能力体」。

**改动项**

| # | 改动 | 对应主轴 |
|---|---|---|
| 2.0.1 | 新增 `references/chart.md`（chart / sparkline / 数据可视化） | B 扩能力 |
| 2.0.2 | 新增 `references/permission.md`（按钮级权限、字段级权限、`disabledOn`/`visibleOn` 权限模式） | B 扩能力 |
| 2.0.3 | 新增 `references/advanced-interaction.md`（复杂联动、combo 嵌套、条件字段、跨组件通信） | B 扩能力 |
| 2.0.4 | 新增 `references/mobile.md`（移动端适配、H5 布局差异） | B 扩能力 |
| 2.0.5 | 决策表按能力域重排，每个新域补 3–6 行「场景 / 用什么 / 别用」 | B 扩能力 |
| 2.0.6 | 建立 `tests/` 回归用例集，含规范文档与 ≥10 个种子用例 | C 建机制 |
| 2.0.7 | 制定**新坑回流协议**：踩到新坑时的写入流程、条目格式、验证要求 | C 建机制 |
| 2.0.8 | 规则分级：硬规则（违反=返工）/ 强建议 / 风格偏好，避免所有规则一个权重 | A 提质 |
| 2.0.9 | 版本兼容矩阵：不同 amis 版本的规则差异表 | A 提质 / P1-3 |

**验收标准**

- [ ] 新增 4 个能力域 reference，每个 ≤ 120 行，且都有对应决策表条目
- [ ] `tests/` 不少于 10 个用例，覆盖全部硬规则，每个用例含「必须出现的特征」和「必须不出现的反模式」两类断言
- [ ] 回流协议文档化：包含条目模板、必填字段、审核标准
- [ ] 全 skill 总量 ≤ 800 行

---

## 6. 关键设计详述

### 6.1 规则元数据格式

每条规则在权威定义处带一个元信息块，建议格式：

```markdown
#### `D-01` 弹层提交必须 loading 防重复

> 来源：实战观察 + V-1 实测（amis 3.x，2026-08）
> 状态：已实测
> 适用版本：>=3.0
> 违反后果：点击提交无任何反馈，用户重复点击导致重复提交

**规则**：提交按钮 `close: false` + `loadingOn` 变量 + `submitSucc` 内 `closeDialog`。

**完整写法**：
（代码块）
```

元数据四要素：**来源 / 状态 / 版本 / 违反后果**。其中「违反后果」最容易被忽略，但它决定了模型是否在边缘场景仍遵守规则。

### 6.2 自检清单设计（`references/self-check.md`）

生成完配置后逐条过，按域分组，每条指向规则 ID：

```markdown
## 弹层类配置
- [ ] 提交按钮有 `close: false`？→ `D-01`
- [ ] 弹层提交按钮**不带** `loadingOn`？（submit 有内建 loading，配了也是死配置）→ `D-01`
- [ ] 用了 `onEvent.submit` 吗？有则删 → `D-01`
- [ ] 事件动作内刷新用 `componentId` 而非 `target`？→ `D-03`（注意：`action` 类型按钮的 `target` 是官方支持的合法写法）
- [ ] 导出用了 `ajax` + blob？改为 `actionType: download` → `D-02`
- [ ] 导出/下载按钮配了 `loadingOn` + `setValue` 配对？（`download` 无内建 loading，必须配）→ `D-02`

## 列表类配置
- [ ] `perPageAvailable` 在 crud 顶层？→ `C-01`
- [ ] 底部统计用的 `tpl` 还是 `statistics`？必须是 `tpl` → `C-02`
- [ ] crud 同时设了 `id` 和 `name`？→ `C-03`

## 通用
- [ ] 生成的 JSON 里有注释吗？有则全部移除 → `R-01`
```

清单的价值在于**正向**——它不需要用户先遇到问题，而是生成时就能拦截。

### 6.3 触发矩阵（`SKILL.md` 内）

| 触发信号 | 必读文件 | 说明 |
|---|---|---|
| crud / 列表 / 表格 / 分页 / 工具栏 | `references/crud.md` | 出现 crud 组件即读 |
| dialog / drawer / 弹层 / 提交按钮 / 动作 / 刷新 | `references/dialog-actions.md` | 出现任何弹层即读 |
| form / 表单 / select / 校验 / 上传 / 字典 | `references/form-controls.md` | 出现表单控件即读 |
| api / 接口 / 后端字段 / 响应结构 / 变量取值 | `references/data-source.md` | 对接任何接口即读 |
| 「不生效」「没反应」「报错」「排查」「为什么」 | `references/pitfalls.md` | 排查类问题即读 |
| 需要整页骨架 | `examples/INDEX.md` → 选文件 | 先读索引再读文件 |
| **任何生成任务完成后** | `references/self-check.md` | 强制自检 |

并明确写入：「命中即读，**不得凭记忆作答**。本 skill 的规则多数是反直觉的坑点，凭常识推理必然出错。」

### 6.4 回归用例集设计（`tests/`）

单个用例格式：

```markdown
# 002 弹层提交 loading 防重复

## 需求
一个删除确认弹层，点击确认后调接口，成功后刷新表格并关闭弹层。

## 必须出现的配置特征（断言点）
1. 提交按钮含 `"close": false`
2. `submitSucc` 中含 `reload` → `closeDialog`（顺序不能反）
3. 事件动作内的 `reload` 使用 `componentId`
4. 表单**不含** `onEvent.submit`
5. `submitFail` 中**不含** `closeDialog`（失败要保持弹层可重试）

## 必须不出现的反模式（依据 2026-08-31 实测）
1. 出现 `onEvent.submit`
2. 事件动作内出现 `{"actionType": "reload", "target": ...}`
3. **弹层提交按钮出现 `loadingOn`**——submit 有内建 loading，配了是死配置
4. Service `data` 中出现 `formLoading` / `deleteLoading` 等只为 loading 服务的变量
5. `submitSucc` / `submitFail` 中出现为 loading 变量收尾的 `setValue`

> **注意区分**：导出/下载按钮**必须**有 `loadingOn` + `setValue` 配对
> （`download` 无内建 loading，V-3 实测有效）。弹层与导出，两者要求相反。

## 覆盖规则
`D-01` `D-03` `R-01`
```

种子用例建议（10 个）：
1. 基础列表页（crud + 分页 + 工具栏）
2. 弹层提交 loading 防重复（**当前含死配置，改造前不通过**）
3. 危险操作确认弹层
4. 导出/下载按钮
5. Excel 导入弹层
6. 字典下拉 + 远程联想
7. 多选表单项提交
8. 弹层内数据选择器（bulkActions）
9. 非标准响应的接口对接（adapter）
10. 刷新其他组件（componentId reload）

**用例 2 是 v1.1 的验收标尺**：改造前因 `loadingOn` 死配置而不通过；
改造后（删掉三件套、保留 `close: false`、保留内建 loading）应通过。

### 6.5 新坑回流协议

踩到新坑时，写入流程：

```
发现新坑
  ↓
1. 记录：症状（可复现的现象）/ 错误写法 / 正确写法
  ↓
2. 实测确认：在真实环境验证「错误写法确实错、正确写法确实对」
  ↓
3. 归类：属于哪个域？→ 写入对应 reference，分配 ID
  ↓
4. 若该坑有诊断价值（症状不明显）→ 在 pitfalls.md 加一条，只写症状 + 指向 ID
  ↓
5. 更新自检清单（如果该坑可在生成时拦截）
  ↓
6. 更新测试用例集
  ↓
7. 记录 CHANGELOG（版本号 + 日期 + 触发场景）
```

**条目必填字段**：ID / 来源 / 状态 / 版本 / 违反后果 / 正确写法。
**准入标准**：未经实测的坑点只能标 `待验证`，**不得**进入硬规则层。

这条协议是整个 skill 能否持续进化的关键——没有它，skill 会随 amis 版本推进而逐渐腐化。

### 6.6 待决策的开放问题

| # | 问题 | 备选方案 | 建议 |
|---|---|---|---|
| Q1 | ~~loading 变量在哪里置 `true`？~~ | A：提交按钮 `onEvent.click` 里 `setValue true`；B：去掉 `loadingOn`，依赖 submit 内建 loading | ✅ **已由 V-1 实测消解，选 B**。实测 A/B/C 三组均转圈，内建 loading 已够用，A 方案纯属多余 |
| Q2 | `close:false` 下 `api.reload` 是否真的无效、示例里还留吗？ | A：全部删除；B：保留并加注「无效，仅为语义标记」 | 建议 A。死配置留在示例里是持续的误导源。**待 V-2 实测确认** |
| Q3 | `crud-full.json` 334 行如何处理？ | A：瘦身到 150 行内（抽掉 Edit 弹层等重复结构）；B：拆成 `crud-base.json` + 若干弹层片段，用 INDEX 组合；C：维持现状，接受超预算 | 建议 B。弹层结构高度重复，拆开后既能控行数又便于复用 |
| Q4 | 新能力域的优先级？ | chart / permission / advanced-interaction / mobile | 建议 permission 优先——后台系统刚需，且坑点多（权限与 `disabledOn` 的交互） |
| Q5 | 是否需要声明不适用的边界？ | 如「不适用于 amis-editor 可视化配置」「不适用于 amis 2.x」 | 建议声明。误触发的成本高于漏触发 |

---

## 7. 度量指标

用于判断进化是否真的发生，而非「文档变多了」：

| 指标 | 当前值 | v1.1 目标 | v1.2 目标 | v2.0 目标 |
|---|---:|---:|---:|---:|
| 硬规则重复率 | 100% | — | 0% | 0% |
| 规则带来源标注率 | ~8%（1/13） | 30% | 100% | 100% |
| 规则标注「待验证」比例 | 未标注 | ≤ 40% | ≤ 20% | ≤ 10% |
| 回归用例数 | 0 | 3（P0 相关） | 10 | ≥ 15 |
| 回归用例通过率 | — | 100%（含用例 2） | 100% | 100% |
| 单次典型生成加载行数 | ~957 | ~957 | ≤ 400 | ≤ 400 |
| 单文件最大行数 | 334 | 334 | ≤ 150 | ≤ 150 |
| examples 组合可运行性 | ❌ 断裂 | ✅ | ✅ | ✅ |
| 交叉引用失效率 | 未统计 | 0% | 0% | 0% |

**最关键的一条**：回归用例通过率。它把「规则是否有效」从主观感受变成可验证的事实。

---

## 8. 风险与回退

| 风险 | 影响 | 应对 |
|---|---|---|
| 实测结论与文档现有说法相反 | v1.1 需推翻重写多条规则 | **已发生**：V-1 推翻了 P0-1 的定性（P0→P1），并把修复方向从「补全」反转为「删除」。这正是把实测排在第一位的原因；剩余风险集中在尚未完成的 V-2 |
| v1.2 的 SSOT 重构破坏现有交叉引用 | 引用失效，模型读到空内容 | 重构后逐个检查引用可达性，纳入验收标准 |
| 拆分 `crud-full.json` 后失去「整页参考」价值 | 模型无法一次看到完整页面 | 在 `examples/INDEX.md` 提供组合说明，并保留一个组合后的完整示例供对照 |
| 过度工程化：规则元数据维护成本高 | skill 变成文档负担，反而不更新 | 元数据只要求四要素，不强制长篇说明；`待验证` 是合法状态 |
| 新增能力域引入未经验证的规则 | 稀释整体可信度 | 新域规则默认 `待验证`，且 v2.0 验收要求每个新域都有对应测试用例 |

**回退策略**：v1.1 / v1.2 / v2.0 各自独立可发布。任一版本出问题，回退到上一版本的 tag 即可，不产生跨版本耦合。

---

## 9. 下一步

| 优先级 | 动作 | 状态 |
|---|---|---|
| 1 | 完成 V-1 实测（submit 内建 loading 是否失效） | ✅ 已完成——内建 loading 有效，`loadingOn` 冗余 |
| 2 | 完成 V-3 实测（`download` 是否等待完成） | ✅ 已完成——等待，Export 写法有效 |
| 3 | 补齐 V-2 实测（`close:false` 下 `api.reload` 是否生效） | ⏳ **待做，当前唯一阻塞项** |
| 4 | 确认 Q2–Q5 开放问题（Q1 已被实测消解） | ⏳ 待定 |
| 5 | 启动 v1.1 的 10 项改动（原 7 项 + 官方冲突 3 项） | ⏳ 待 3 完成 |
| 6 | 建立 `tests/cases/002-dialog-submit-loading.md` 作为 v1.1 验收标尺 | ⏳ 待做 |

**Q1（loading 变量在哪置 `true`）已由 V-1 实测消解**——不需要置 `true`，直接删掉 `loadingOn` 三件套。

**在 V-2 结论出来前，不建议开始扩能力域（v2.0）。**
