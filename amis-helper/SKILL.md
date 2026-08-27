---
name: amis-helper
description: 百度amis低代码框架JSON Schema生成。包含高频坑点的避坑规则与可复用骨架，生成可直接落地的crud/弹层/表单/导入导出配置。
version: 1.0.0
allowed-tools:
disable: false
---

# amis-helper Skill

生成 amis 配置时必须遵守本文件规则，深水区场景按需读取 references/。

## 1. 生成前必查硬规则（违反任意一条=返工）

| # | 规则 | 详情 |
|---|------|------|
| 1 | JSON 内禁止注释 | amis Schema 校验报错，注释只能写在配置外的文档里 |
| 2 | crud 分页切换器：`perPageAvailable` 必须放 crud 顶层，不能放 footerToolbar 内组件里 | references/crud.md §1 |
| 3 | 事件动作中 reload 用 `componentId`（非 `target`），目标组件必须设置 `id` 属性 | references/dialog-actions.md §3 |
| 4 | 弹层提交按钮要 loading 防重复：`close: false` + `submitSucc` 中 `closeDialog`，禁止用 `onEvent.submit` | references/dialog-actions.md §1 |
| 5 | 文件下载/导出用 `actionType: "download"`，禁止 `ajax` + `responseType: "blob"` 或裸 `fetch()` | references/dialog-actions.md §2 |
| 6 | select 远程联想：`autoComplete` 必须是对象（含 method/url/sendOn），不能是 `true` + 外部 source | references/form-controls.md §3 |
| 7 | 文件上传提交：`input-file` 加 `asBlob: true`，api 加 `dataType: "form-data"` | references/form-controls.md §5 |
| 8 | 控制表单项宽度用 `columnRatio`，`size`/`style.width`/`inputClassName` 均无效 | references/form-controls.md §6 |
| 9 | footerToolbar 统计条用 `tpl`（`${total}`），不用 `statistics`（单页时不渲染） | references/crud.md §2 |
| 10 | 非 amis 标准后端响应结构必须用 `adapter`/`adaptor` 转换，不能假设后端适配 | references/data-source.md §2 |

## 2. 场景 → 组件决策表

| 业务场景 | 用什么 | 别用 |
|---------|--------|------|
| 数据列表+搜索 | crud + filter | 独立搜索表单+target |
| 新增/编辑/详情 | `actionType: "dialog"` + 内嵌 form | drawer（仅侧边长内容用） |
| 危险操作确认 | 自定义 dialog 弹层（alert提示 + confirm按钮） | confirmText 浏览器原生框 |
| 状态列展示 | `type: "mapping"` + label 样式 | tpl 拼接 |
| 行内多按钮 | operation 列 + `button-group` | 平铺多个按钮撑爆列宽 |
| 导入 Excel | dialog + input-file(asBlob) + form-data | |
| 导出/模板下载 | `actionType: "download"` | window.open / blob ajax |
| 字典/枚举下拉 | select + source(带 adaptor) | 前端硬编码 options |
| 远程联想输入 | select + autoComplete 对象 | input-text 手输 |
| 弹层内选择数据 | dialog + crud(loadDataOnce) + bulkActions | |
| 表格loading/按钮防重复 | Service 包层 + data 变量 + loadingOn | crud setValue（不传播） |
| 刷新其他组件 | api.reload（默认关弹层模式）/ componentId reload（close:false 模式） | |

## 3. references 索引（按需读取）

| 文件 | 内容 | 何时读 |
|------|------|--------|
| references/crud.md | CRUD 骨架/分页/工具栏/刷新机制/loadDataOnce | 生成任何 crud 时 |
| references/dialog-actions.md | 弹层提交/loading/下载/动作链/刷新 | 生成弹层、按钮动作时 |
| references/form-controls.md | select字典/autoComplete/校验/文件上传/宽度 | 生成表单时 |
| references/data-source.md | api配置/adapter数据转换/source数据源 | 对接任何接口时 |
| references/pitfalls.md | 踩坑手册（症状→错误→正确） | 自检或排查问题时 |
| examples/ | 3个完整骨架片段 | 需要整体参考时 |

## 4. examples 索引

| 文件 | 场景 | 覆盖点 |
|------|------|--------|
| examples/crud-full.json | 列表页全套骨架 | Service包层(loading变量) + crud + filter(autoComplete联想/字典多选) + 导入弹层(input-file) + 新增弹层 + 导出下载 + mapping状态列 + operation列 + 分页 |
| examples/dialog-confirm-loading.json | 危险操作确认弹层（放 operation 列或 headerToolbar 均可） | close:false防自动关 + loadingOn防重复 + submitSucc动作链(关loading/reload/关弹窗) + submitFail保持打开 |
| examples/bulk-actions-picker.json | 弹层/抽屉内数据选择器 | dialog + crud(loadDataOnce前端分页) + bulkActions批量提交 + selectedItems\|pick过滤器 + disabledOn未选中禁用 |
