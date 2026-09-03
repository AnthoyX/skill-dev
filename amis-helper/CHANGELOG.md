# CHANGELOG

## 1.2.4（2026-09-03）

V-14 实测三轮（详见 `docs/verify-lab-260903.yaml` §V-14），三条规则升「已实测」（11→14 条），其中一条**推翻 v1.2.2 的源码推断**：

- **V-14-A `F-01` 重写（重大）**：多选 select 提交值**恒为数组**。实测五种配置（默认 / `joinValues:true` / `+extractValue` / `+delimiter:"|"` / 仅 `extractValue`）提交值**全部是 `["a","b"]`**——v1.2.2 依据 select defaultProps `joinValues:!0` 推断「默认即逗号字符串」**被实测推翻**。真实结论：
  - **禁止 `joinValues: false`**（唯一有实质影响的配置，会让元素变成 `{label,value}` 对象）
  - `joinValues` / `extractValue` / `delimiter` 对提交值形态**无影响**，非必需
  - 要逗号字符串只能靠 `join` 过滤器：`"codes": "${field|join:','}"`（实测得到 `a,b`）
  - 同步修正 P-22（原写「默认 true 会拼成逗号分隔字符串」，与实测相反）
- **V-14-A `F-10` 成立 + 后果修正**：注入式对照（同一非标准响应，`adaptor` / `adapter` / 不写转换三组）——`adaptor` 组正常渲染注入值，`adapter` 组与「不写转换」组一致，均回退显示原始 value。**`adapter` 完全无效**。后果由「显示 invalid label」修正为「下拉为空 / 回退显示原始 value」（invalid label 实为 `labelField` 不匹配的表现）；`F-03` 排查链同步修正因果对应
- **V-14-B `D-03` 成立**：事件动作内 `target` 写法**零请求**（失效），`componentId` 与 `componentName` 均触发刷新（后者验证 v1.2.2 补入的等价写法成立）
- 未验证：`F-07`（需 autoComplete 交互场景，本次用 source 测属场景错配——source 的 `data.options` 是合法结构，不能证伪 F-07）
- lab 增强：mock 新增 `nonstd=1`（非标准业务码 + data 为数组）与 `wrap=options` 两个开关；修复非标准响应下日志 `KeyError: 'status'` 导致请求无响应的 bug

## 1.2.3（2026-09-03）

V-13 实测三轮（详见 `docs/verify-lab-260903.yaml`），四条规则由「实战观察」升「已实测」（7→11 条）：

- **V-13-A `D-06` 成立**：form 配 `onEvent.submit` 后接口**零请求**、`submitSucc` 不触发、弹层不关闭；基线组接口正常发出且弹层关闭。源码推断（事件动作须显式 `preventDefault:true`）被实测推翻——form 的 submit 事件是例外，规则补注「以实测为准」；后果描述由「loading 卡死」改为「弹层不关闭（点了没反应）」
- **V-13-B `A-01` 修正 + `D-09` 成立**：三层观测——`setValue` 不带 `componentId` 落在**按钮自身**数据域（Service / headerToolbar / 行内全读不到，比原描述更严格）；带 `componentId` 指向 Service 时 **Service 与 crud headerToolbar 可读**（`D-08`/`D-09` 方案成立），但 **crud columns 行内读不到**（拿初始快照）。`A-01` 重写为分层三态描述
- **V-13-C `C-04` 成立**：total=5 / perPage=10（单页）时 statistics **整个节点不渲染**，total=171 时正常渲染「1/18 共：171 项」；同期 tpl 替代方案在单页下正常渲染
- 归档验证配置 `_amis-lab/schemas/v13a-d06-submit.json`、`v13b-a01-scope.json`、`v13c-c04-statistics.json`

## 1.2.2（2026-09-02）

v1.2.1 全量审查后修复（审查报告 `docs/review-v121-260902.yaml`，21 项）：

- **事实错误修正（源码实证）**：`A-02` 删除「adapter 也能识别」括注——amis 6.13.0 源码只识别 `adaptor`，`sdk.js` 中 5 处 `adapter` 全是 axios 内部配置（与 `F-10` 的矛盾随之消解）；`F-01` 由「多选必带四件套」改为「保持 `joinValues` 为默认 true，`delimiter`/`extractValue` 按需」——select defaultProps 为 `joinValues:!0 / extractValue:!1 / delimiter:","`，原「不写就提交数组」的后果描述不成立，示例 `crud-base.json` 同步精简
- **元数据同步**：`SKILL.md` 规则总数 32→33；`META.md`「已实测」补 `D-12`/`F-02`（5→7 条），新增「据官方文档或源码」级别承载源码佐证规则；`INDEX.md` 行数声明对齐实际
- **SSOT**：reload 载体表三处（`META.md` / `crud.md §9` / `dialog-actions.md §3`）合一，仅保留 dialog-actions §3 为权威，另两处降级为引用（`D-05` 全文出现数 19→13）
- **来源升级为「据源码」**：`C-03`（crud defaultProps `syncLocation:!0`）、`D-03`（补 `componentName` 等价写法，源码 `componentId ? getComponentById : getComponentByName`）、`F-06`（措辞由「grid 布局」改为「form group 列宽比例」）、`A-02`、`F-01`
- **覆盖补齐**：`pitfalls.md` 新增 P-19～P-25（补 C-03/C-05/C-07/F-01/F-05/F-08 的排障入口 + F-02 的 ajax 跳过校验边界）；`data-source.md` 补 `patch`；`SKILL.md` 触发矩阵补 `META.md` 入口
- **示例层**：`dialog-confirm-loading.json` → `dialog-confirm.json`（`git mv` 保留历史，消除 loading 命名误导）；`INDEX.md` §2 补 `button-group` 包装片段，消除「三个按钮平铺→违反 C-08」的组合隐患；`dialog-form-edit.json` 两个 static 写法统一
- **命中率**：description 补触发场景（crud / 弹层 / 表单校验 / 字典联想 / 导入导出 / 刷新联动）；删除非标准字段 `disable`
- 终检：6 个 JSON 合法 / 16 文件全 CRLF / 33 条 ID 无跳号无悬空 / P-01～P-25 连续 / 规则层 656（≤800）/ 示例层 445（≤460）/ INDEX 声明行数与实际全对
- 未闭环，转入 V-13 实测：`D-06`（onEvent.submit 是否真拦截，源码 preventDefault 机制存疑，后果严重）、`A-01`（crud 内 setValue 不向外传播，D-09 唯一依据）、`C-04`（statistics 单页不渲染）

## 1.2.1（2026-09-01）

v1.2 收尾实测三组（V-10/V-11/V-12，详见 `docs/verify-lab-260901.yaml`）+ 规则落地：

- **V-11 required 校验链**：F-02 改写为「必填只写 `required:true`，勿双写 `validations.isRequired`（幂等无增强）」；实测边界修正源码推断——全空格串被拦截（源码推断不拦截）、ajax 按钮跳过提交前校验阻断（红字是 onChange 副作用）；新增 P-17（隐藏必填误拦截）/ P-18（combo 行内不校验）
- **V-12 close 缺省 form api reload**：D-11 升「已实测」（A 组新增 GET 生效 / B 组 close:false 不生效，V-2 复现）；与 D-05 形成对偶边界
- **V-10 按钮级 reload**：新增 D-12（两形态）——刷新专用按钮 `actionType:reload` 必须用 `target`（顶层 reload 无效）；业务按钮 ajax/submit 用顶层 `reload` 属性（close 不影响）；§3 表格三分、crud.md §9 与 META reload 载体总表同步
- 规则数量 32→33（D×11→D×12）；排障 16→18；META 可信度分级「已实测」行补 D-11
- 终检：权威形态唯一性 / 编号连续 / 悬空引用=0 / 全文 CRLF（见 `docs/verify-lab-260901.yaml` 末）
- 评审回执后补（`docs/review-v121-260901-in.yaml`，有条件通过）：SKILL.md version 同步 1.2.1（必修）；§2 决策表「刷新」行补 D-03/D-12/D-11/D-05；dialog-actions §3 表按钮级行拆两行；form-controls §2 F-02 补 P-18 引用。建议3（三表重叠）跳过（评审自述不强制）

## 1.2.0（2026-08-31）

SSOT 重构，四批次完成（评审文档见 `docs/`，基准 `docs/plan-iteration.md` §5.2）：

- 批次 1（5d3d67c + ee1a027）：规则 ID 体系冻结——32 条权威规则 = R-01 + C-01~C-08 + D-01~D-11 + F-01~F-10 + A-01~A-02，每条带「来源|状态|版本|违反后果」四要素
- 批次 2（ded35a5）：`pitfalls.md` 重编号 P-01~P-16 纯引用化（症状 + 错误写法 + ID 指向）；`SKILL.md` 索引化（59 行）
- 批次 3（135d383）：`crud-full.json` 拆 4 片段 + `examples/INDEX.md`（宿主依赖 / 覆盖规则 ID / 行数）
- 批次 4（a137700）：新增 `references/self-check.md`（6 组 33 项正向自检清单，覆盖 32 条规则，`C-02` 跨组复检，只引规则 ID）；`META.md` 参考文档计数更新；`SKILL.md` 触发矩阵补 self-check 入口
- 终检全部 PASS：权威形态唯一性（32 条各出现 1 次）/ 编号连续无跳号 / 悬空引用 = 0 / 全文 CRLF

## 1.1.0（2026-08-31）

止血修正（commit 7d1dea8；实测 V-1 / V-1-D / V-2 / V-3，详见迭代计划 §5.1）：

- 删除弹层提交 `loadingOn` 死配置（submit 按钮有内建 loading，实测三组对照均转圈）；导出 / download 按钮的 `loadingOn` 保留（实测等待下载完成，有效）
- 统一 `api.reload` 说法：`close: false` 下不生效且提交不默认刷新 CRUD，唯一写法是 `submitSucc` 显式 `componentId` reload（V-2 实测）
- 新增 `META.md`：amis 版本锚定（6.13.0）+ 适用边界 + 规则可信度分级
- `adaptor` 拼写统一为官方标准名；`data-source.md` 示例去 `//` 注释；修正 reload `target` 作用域（仅事件动作内失效）；删除不存在的 `columnsToggled`
- frontmatter 补 `amis-version` / `allowed-tools`

## 1.0.0

首发：SKILL.md + 5 references + 3 examples（957 行）。
