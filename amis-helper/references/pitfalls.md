# 踩坑手册（排障索引）

格式：症状 → 错误写法 → 见权威规则 ID。本文不含正确写法，命中即读指向文件。

## 弹层与动作

### P-01 点提交接口不调用，submitSucc 不触发，loading 卡死
- 错误：form 配了 `onEvent.submit`（拦截内置提交）→ 见 references/dialog-actions.md §1（`D-06`）

### P-02 提交后弹框立即关闭，看不到 loading
- 错误：提交按钮缺 `close: false`，未在 `submitSucc` 中 `closeDialog` → 见 references/dialog-actions.md §1（`D-01`）

### P-03 submitSucc 里 reload 了但表格不刷新
- 错误：事件动作内用 `target` 定位（此处失效），或目标 crud 未设 `id` → 见 references/dialog-actions.md §3（`D-03`）

### P-04 close:false 弹层提交后表格不刷新
- 实测（V-2，2026-08-31）：`close: false` 下 form api 的 `reload` 不生效，提交也不默认刷新 CRUD，唯一写法见 references/dialog-actions.md §1（`D-05`）

### P-05 headerToolbar 按钮 loadingOn 读不到变量
- 错误：loading 变量依赖 crud 内 `setValue`（变量不向外传播）→ 见 references/dialog-actions.md §4（`D-09`）、references/data-source.md §5（`A-01`）

### P-06 blob 导出拿不到文件 / 后续动作不执行
- 实测（V-16，2026-09-07）：`ajax` + `responseType: "blob"` + `then` → `then` 不触发；且 `then` 恒不触发、与 blob 无关，后续动作须写进 `onEvent.click.actions` 数组 → 见 references/dialog-actions.md §2（`D-02`）

### P-07 custom action 里 fetch() 报 401
- 实测（V-16，2026-09-07）：裸 `fetch()` 绕过 amis fetcher，不携带 auth token → 401 → 见 references/dialog-actions.md §2（`D-02`）

### P-08 弹层提交按钮配 loadingOn 是死配置
- 实测（V-1/V-1-D，2026-08-31）：submit 按钮有内建 loading，`loadingOn` 恒 false 也照常转圈；接口失败时 loading 正常结束、弹层保持打开、可重试 → 见 references/dialog-actions.md §1（`D-04`）

## 表单控件

### P-09 autoComplete 不触发联想
- 错误：`autoComplete: true` + 外部 `source` → 见 references/form-controls.md §3（`F-03`）

### P-10 联想下拉显示 invalid label
- 错误：① adapter 字符串转换（amis 6.13.0 不可用）② 返回字段与 labelField 不匹配 → 见 references/form-controls.md §8（`F-10`）、§7（`F-09`）

### P-11 联想下拉显示 invalid label / 选项错乱
- 错误：autoComplete 的 source 响应 `data` 是 CRUD 式对象（如 `{rows,items}`、`{count,total}`）→ amis 把对象的**值**当选项遍历，显示 `invalid label` 或数字 → 见 references/form-controls.md §3（`F-07`）

### P-12 sendOn 配了但联想请求不发出
- 错误：`sendOn` 放在 source 对象内 → 见 references/form-controls.md §3（`F-04`）

## CRUD/列表

### P-13 每页条数切换器不出现
- 错误：`switch-per-page` 组件写在 footerToolbar 里（属性名 `perPageOptions` 不存在、位置错）→ 见 references/crud.md §1（`C-01`）

### P-14 单页时底部统计条不显示
- 错误：footerToolbar 用 `statistics`（total ≤ perPage 时不渲染，`textContent` 无效）→ 见 references/crud.md §2（`C-04`）

## 通用

### P-15 表单项宽度控制无效
- 错误：`size: "xl"` / `inputClassName: "w-xl"` / `style.width` → 见 references/form-controls.md §6（`F-06`）

### P-16 amis Schema 校验报「JSON 中不允许有注释」
- 错误：配置内含 `//` 或 `/* */` → 见 META.md（`R-01`）

### P-17 隐藏/不可见的必填字段导致提交被拦截
- 实测（V-11 轮次4，2026-09-01）：hidden/visible:false 的 required 字段值空时仍参与校验，提交被拦截图弹「依赖的部分字段没有通过验证」 → 见 references/form-controls.md §2（`F-02`）

### P-18 combo / input-table 行内必填不校验
- 据 amis 官方 issue#9537（未实测）：combo/input-table 行内字段的 required 在整体提交时不触发校验 → 见 references/form-controls.md §2（`F-02`）

## 补充症状

### P-19 地址栏被分页参数污染，分享链接带 page/perPage
- 错误：crud 未设 `syncLocation: false`（crud defaultProps 默认是 `syncLocation:!0`）→ 见 references/crud.md §1（`C-03`）

### P-20 翻页数据不变 / 后端收不到分页参数
- 错误：后端分页字段非 page/perPage，api.data 未显式映射 `${page}` / `${perPage}` → 见 references/crud.md §3（`C-05`）

### P-21 状态列部分行显示空白
- 错误：mapping 缺 `*` 兜底 key，未命中值不渲染 → 见 references/crud.md §5（`C-07`）

### P-22 多选下拉提交到后端是数组，后端解析失败
- 实测（V-14，2026-09-03）：多选提交值**恒为数组**，配 `joinValues` 也变不成字符串；`joinValues:false` 更糟（元素变 `{label,value}` 对象）。要字符串用 `${field|join:','}` → 见 references/form-controls.md §1（`F-01`）

### P-23 上传 Excel 后端收不到文件
- 错误：`asBlob: true` 与 api 的 `dataType: "form-data"` 未成对出现 → 见 references/form-controls.md §5（`F-05`）

### P-24 编辑提交后端报缺主键 / 只读字段被误改
- 错误：主键未用 `hidden` 承载、只读字段未用 `static` 展示 → 见 references/form-controls.md §4（`F-08`）

### P-25 ajax 按钮提交时必填校验不拦截，空值照样发请求
- 实测（V-11 轮次，2026-09-01）：ajax 按钮跳过提交前校验阻断；表单项的实时红字是 onChange 副作用，非提交阻断 → 见 references/form-controls.md §2（`F-02`）

### P-26 行内（columns）读不到外层 Service 的状态变量
- 实测（V-13-B，2026-09-03）：`setValue` 到 Service 后 crud **headerToolbar 可实时读到，columns 行内只能拿到初始快照**；`setValue` 不带 `componentId` 则落在按钮自身域，三处全读不到 → 见 references/data-source.md §5（`A-01`）

### P-27 动作里配了 `then` 但后续动作不执行
- 实测（V-16，2026-09-07）：`then` 作为动作的兄弟字段在 amis 6.13.0 **恒不触发**，与 `responseType` 无关（普通 JSON 的 ajax 对照组同样不触发）；后续动作必须写进 `onEvent.click.actions` 数组顺序执行 → 见 references/dialog-actions.md §2（`D-02`）
