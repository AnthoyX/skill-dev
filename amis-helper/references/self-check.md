# 生成配置自检清单

生成 amis 配置后、交付前逐条自检。本清单只引规则 ID，权威写法见 ID 指向处（META.md / references/ 各域文件）。P-xx 为事后排障索引（pitfalls.md），不在此列。

## 1. 通用（每次必查）

- [ ] 生成的 JSON 内无 `//` 或 `/* */` 注释？→ `R-01`
- [ ] 非 amis 标准响应（status 非 0 / rows 与 items 字段不符）已用 `adaptor` 转换，且拼写统一为 `adaptor`？→ `A-02`
- [ ] loading 等状态变量声明在外层 Service 的 `data`，而非依赖 crud 内 `setValue` 向外传播？→ `A-01`

## 2. CRUD / 列表页

- [ ] `perPageAvailable` 放 crud 顶层，不在 footerToolbar 组件内？→ `C-01`
- [ ] 被外部定位 / 刷新的 crud 同时设了 `id` 和 `name`？→ `C-02`
- [ ] `syncLocation: false` 已设？→ `C-03`
- [ ] footerToolbar 统计条用 `tpl`，未用 `statistics`？→ `C-04`
- [ ] 后端分页字段非 page/perPage 时，api.data 已显式映射 `${page}` / `${perPage}`？→ `C-05`
- [ ] 用 `filter-toggler` 时 crud 已设 `filterTogglable: true`？→ `C-06`
- [ ] mapping 写了 `*` 兜底 key？→ `C-07`
- [ ] 操作列 `fixed: "right"` + `width` 固定，行内多按钮收进 `button-group`？→ `C-08`

## 3. 弹层与动作（新增/编辑/删除/导入/确认/选择器）

- [ ] 提交按钮 `close: false` + `submitSucc` 内手动 `closeDialog`？→ `D-01`
- [ ] 弹层提交按钮**未配** `loadingOn`（submit 有内建 loading）？→ `D-04`
- [ ] `close: false` 下 form api 内**未写** `reload`，刷新靠 `submitSucc` 显式 `componentId` reload？→ `D-05`
- [ ] form 未配 `onEvent.submit`？→ `D-06`
- [ ] 确认操作用 `actionType: "dialog"` 自定义弹层，未用 `confirmText`？→ `D-07`
- [ ] 事件动作（onEvent.actions）内 reload 用 `componentId`（此处 target 失效）？→ `D-03`
- [ ] 按钮级 reload：刷新专用按钮（actionType:reload）用 `target`、业务按钮（ajax 等）用顶层 `reload` 属性（值均为 name）？→ `D-12`
- [ ] 弹层内选择数据用 crud `loadDataOnce: true` + `bulkActions`，提交用 `${selectedItems|pick:字段}`，空选已 `disabledOn` 禁用？→ `D-10`

## 4. 下载 / 导出（loading 要求与弹层提交相反）

- [ ] 文件下载/导出用 `actionType: "download"`，未用 ajax+blob、裸 `fetch()`？→ `D-02`
- [ ] download 按钮配了 `loadingOn` + 外层 Service 变量 + `setValue true/false` 配对（download 无内建 loading）？→ `D-08`
- [ ] `setValue` 的 `componentId` 指向外层 Service（loading 变量声明在其 `data`）？→ `D-09`

## 5. 表单控件

- [ ] 多选 select 带齐 `multiple` + `extractValue` + `joinValues` + `delimiter`？→ `F-01`
- [ ] 必填字段配了 `required: true`（无需双写 `validations.isRequired`）？→ `F-02`
- [ ] `autoComplete` 是对象（method/url/sendOn 都在内），非 `true` + 外部 source？→ `F-03`
- [ ] `sendOn` 在 autoComplete 对象内，未放进 source？→ `F-04`
- [ ] `asBlob: true` 与 api 的 `dataType: "form-data"` 成对出现？→ `F-05`
- [ ] 表单项宽度用 `columnRatio`，未用 size / inputClassName / style.width？→ `F-06`
- [ ] 联想响应 data 直接是数组，非 `{options:[...]}` 嵌套？→ `F-07`
- [ ] 编辑弹层只读展示用 `static`、提交主键用 `hidden`？→ `F-08`
- [ ] 联想下拉后端响应是否返回标准 `label`/`value` 字段（协作约束，前端不可独立完成，否则用降级方案）？→ `F-09`
- [ ] 未使用 adapter 字符串转换（6.13.0 不可用，报 invalid label）？→ `F-10`

## 6. 刷新定位

- [ ] 弹层默认关闭模式（close 缺省）下 form api 的 `reload`（值 name）生效？→ `D-11`（close:false 下不生效，见 `D-05`）
- [ ] 被 reload 的目标 crud 同时设了 `id` 和 `name`？→ `C-02`
