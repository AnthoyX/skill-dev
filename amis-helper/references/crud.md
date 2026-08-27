# CRUD 规范

## §1 分页配置（正确写法）

```json
{
  "type": "crud",
  "id": "xxxCrud",
  "name": "xxxCrud",
  "defaultParams": { "perPage": 50, "page": 1 },
  "perPageAvailable": [20, 50, 100, 150],
  "syncLocation": false,
  "footerToolbar": [
    "switch-per-page",
    { "type": "tpl", "tpl": "Total ${total} records, Page ${page}" },
    "pagination"
  ]
}
```

规则：
- `perPageAvailable` 放 crud **顶层**（amis-ui BasicPaginationProps 接口定义，放 footerToolbar 组件内不生效，官方 issue #6685）
- `defaultParams.perPage` 设默认每页条数
- footerToolbar 里 `switch-per-page` 用字符串简写即可
- crud 同时设 `id` 和 `name`：`id` 供事件动作 componentId 定位，`name` 供 api.reload 定位
- `syncLocation: false` 避免分页参数污染 URL

## §2 统计条用 tpl 不用 statistics

`statistics` 组件在 total <= perPage（单页）时不渲染，`textContent` 属性无效。用 tpl 替代（不受分页状态影响，一定渲染）。

## §3 api 对象写法 + 分页参数映射

后端分页参数不是 amis 默认的 page/perPage 时，用 data 显式映射：

```json
{
  "api": {
    "method": "post",
    "url": "/XXX/XXXX/page",
    "data": {
      "code": "${code}",
      "current": "${page}",
      "size": "${perPage}"
    }
  }
}
```

- crud 数据域自动提供 `${page}`、`${perPage}`、filter 字段
- 响应结构非 amis 标准（要求 `{items, total}`）时必须加 adapter 转换 → data-source.md §2

## §4 headerToolbar 标准布局

```json
"headerToolbar": [
  "reload",
  "filter-toggler",
  { "type": "button", "label": "Import", "level": "primary", "icon": "fa fa-upload", "actionType": "dialog", "dialog": {} },
  { "type": "button", "label": "Add", "level": "success", "icon": "fa fa-plus", "actionType": "dialog", "dialog": {} },
  { "type": "button", "label": "Export", "level": "warning", "icon": "fa fa-download", "onEvent": {} }
]
```

字符串简写（reload/filter-toggler）+ 按钮对象混用。`columns-toggler`、`drag-toggler` 需要 crud 设 `"columnsToggled": true` 类配置时使用。

## §5 状态列用 mapping

```json
{
  "name": "status",
  "label": "Status",
  "type": "mapping",
  "map": {
    "Enabled": "<span class='label label-success'>Enabled</span>",
    "Disabled": "<span class='label label-danger'>Disabled</span>",
    "*": "<span class='label label-default'>(blank)</span>"
  }
}
```

`*` 兜底 key 必须写，否则未命中值显示空白。

## §6 operation 操作列

```json
{
  "type": "operation",
  "label": "Action",
  "fixed": "right",
  "width": 220,
  "buttons": [
    { "type": "button-group", "buttons": [ { "按钮1": "..." }, { "按钮2": "..." } ] }
  ]
}
```

- `fixed: "right"` + `width` 固定操作列
- 按钮多时用 button-group 收拢
- 行数据字段通过数据域直接取（如 dialog title 写 `"Edit - ${code}"`）
- 编辑/详情弹层 form 里传 id 用 `{ "type": "hidden", "name": "id" }`

## §7 filter 顶部搜索表单

```json
"filter": {
  "title": "Filter",
  "actions": [
    { "type": "reset", "label": "Reset" },
    { "type": "submit", "label": "Search", "level": "primary" }
  ],
  "body": [ { "表单项": "..." } ]
}
```

filter 字段自动进入 crud 数据域，api 的 data 里用 `${字段名}` 引用。

## §8 loadDataOnce（前端一次拉取）

数据量小（如全量字典/配置列表）时用 `"loadDataOnce": true`：首次请求拉全量，后续分页/排序在前端完成。弹层内嵌选择器 crud 常用（见 examples/bulk-actions-picker.json）。

## §9 刷新机制（三条路，按场景选）

| 场景 | 写法 |
|------|------|
| 弹层默认模式（提交后自动关） | form api 里加 `"reload": "目标crud的name"` |
| `close: false` 模式 | api.reload 不生效，必须在 `submitSucc` 里 `{"actionType": "reload", "componentId": "crud的id"}` |
| 事件动作（onEvent.click 等） | `{"actionType": "reload", "componentId": "..."}`（用 componentId 非 target） |
