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

### P-06 blob 导出 loading 卡死
- 错误：`ajax` + `responseType: "blob"` + `then`（then 不触发）→ 见 references/dialog-actions.md §2（`D-02`）

### P-07 custom action 里 fetch() 报 401
- 错误：裸 `fetch()` 不携带 auth token → 见 references/dialog-actions.md §2（`D-02`）

### P-08 弹层提交按钮配 loadingOn 是死配置
- 实测（V-1/V-1-D，2026-08-31）：submit 按钮有内建 loading，`loadingOn` 恒 false 也照常转圈；接口失败时 loading 正常结束、弹层保持打开、可重试 → 见 references/dialog-actions.md §1（`D-04`）

## 表单控件

### P-09 autoComplete 不触发联想
- 错误：`autoComplete: true` + 外部 `source` → 见 references/form-controls.md §3（`F-03`）

### P-10 联想下拉显示 invalid label
- 错误：① adapter 字符串转换（amis 6.13.0 不可用）② 返回字段与 labelField 不匹配 → 见 references/form-controls.md §8（`F-10`）、§7（`F-09`）

### P-11 联想下拉为空
- 错误：响应 data 嵌套为 `{options:[...]}` → 见 references/form-controls.md §3（`F-07`）

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
