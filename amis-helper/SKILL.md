---
name: amis-helper
description: 百度amis低代码框架JSON Schema生成。包含高频坑点的避坑规则与可复用骨架，生成可直接落地的crud/弹层/表单/导入导出配置。
version: 1.2.0
amis-version: "6.x（规则实测基于 6.13.0）"
allowed-tools: Read, Grep, Glob
disable: false
---
# amis-helper Skill

规则全文以 ID 权威定义为准（META.md + references/），本文件只做索引。适用边界：仅 JSON Schema 手写生成，不适用于 amis-editor 可视化 / amis 2.x / 移动端 H5，详见 META.md。
## 1. 硬规则索引（高频 TOP14，非全集；完整 32 条见 META.md / references/ 各域文件，交付前必跑 self-check 全量核对）

| ID | 一句话 | 权威定义 |
|---|---|---|
| R-01 | JSON 配置内禁止注释 | META.md |
| C-01 | perPageAvailable 放 crud 顶层 | references/crud.md §1 |
| C-04 | 统计条用 tpl 不用 statistics | references/crud.md §2 |
| D-01/D-04/D-06 | 弹层提交：close:false+submitSucc 关窗，禁 loadingOn/onEvent.submit | references/dialog-actions.md §1 |
| D-05 | close:false 下 form api 内禁写 reload，刷新靠 submitSucc 显式 componentId reload | references/dialog-actions.md §1 |
| D-02/D-08 | 下载导出只用 download，loadingOn+setValue 配对 | references/dialog-actions.md §2 |
| D-03 | 事件动作 reload 用 componentId | references/dialog-actions.md §3 |
| F-03 | autoComplete 必须是对象 | references/form-controls.md §3 |
| F-05 | 上传 asBlob 与 form-data 成对 | references/form-controls.md §5 |
| F-06 | 宽度只认 columnRatio | references/form-controls.md §6 |
| A-02 | 非标准响应用 adaptor 转换 | references/data-source.md §2 |

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
| 表格loading/按钮防重复 | 弹层提交靠内建 loading；导出/下载按钮用 Service 包层 + data 变量 + loadingOn | 弹层提交按钮配 loadingOn（死配置） |
| 刷新其他组件 | 事件动作用 componentId reload；close:false 弹层默认不刷新 crud，须在 submitSucc 里显式 componentId reload | 弹层 form api 里写 reload（close:false 下不生效，实测） |

## 3. 触发矩阵（按需读取）

| 触发信号 | 必读 |
|---|---|
| crud / 列表 / 表格 / 分页 / 工具栏 | references/crud.md |
| dialog / drawer / 弹层 / 提交按钮 / 动作 / 刷新 | references/dialog-actions.md |
| form / 表单 / select / 校验 / 上传 / 字典 | references/form-controls.md |
| api / 接口 / 后端字段 / 响应结构 / 变量取值 | references/data-source.md |
| 不生效 / 没反应 / 报错 / 排查 / 为什么 | references/pitfalls.md |
| 需要整页骨架 | 本文 §4 examples 索引 |
| 任何生成任务完成后 | references/self-check.md |

命中即读，不得凭记忆作答。本 skill 规则多为反直觉坑点，凭常识推理必然出错。

## 4. examples 索引

6 个片段（原整页示例 1:1 拆分）+ 宿主依赖 + 组合说明见 examples/INDEX.md。清单：crud-base.json（列表页骨架，自包含）、dialog-import.json（导入弹层）、dialog-form-add.json（新增弹层）、dialog-form-edit.json（编辑弹层）、dialog-confirm-loading.json（删除确认）、bulk-actions-picker.json（弹层内选择器）。
