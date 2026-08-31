# CRUD 规范

规则 ID 前缀 `C-xx`，元数据四要素：`来源|状态|版本|违反后果`。
排障条目见 references/pitfalls.md。

## §1 分页与骨架

```json
{
  "type": "crud",
  "id": "xxxCrud",
  "name": "xxxCrud",
  "syncLocation": false,
  "defaultParams": { "perPage": 50, "page": 1 },
  "perPageAvailable": [20, 50, 100, 150],
  "footerToolbar": [
    "switch-per-page",
    { "type": "tpl", "tpl": "Total ${total} records, Page ${page}" },
    "pagination"
  ]
}
```

- **`C-01`** `perPageAvailable` 必须放 crud **顶层**，不能放 footerToolbar 内组件里
  `来源:amis-ui BasicPaginationProps 接口定义+官方issue#6685|状态:据官方文档|版本:6.x|后果:切换器不出现`
- **`C-02`** crud 同时设 `id` 和 `name`：`id` 供事件动作 componentId 定位，`name` 供按钮 target / api.reload 定位
  `来源:实战观察|状态:实战观察|版本:6.x|后果:reload 定位不到目标`
- **`C-03`** `syncLocation: false`，避免分页参数污染 URL
  `来源:实战观察|状态:实战观察|版本:6.x|后果:刷新/分享链接携带分页参数`
- `defaultParams.perPage` 设默认每页条数；footerToolbar 内 `switch-per-page` 用字符串简写

## §2 统计条

- **`C-04`** footerToolbar 统计条用 `tpl`（如 `"Total ${total} records, Page ${page}"`），不用 `statistics`
  `来源:实战观察|状态:实战观察|版本:6.x|后果:total<=perPage 单页时 statistics 不渲染、textContent 属性无效`

## §3 api 分页参数映射

```json
{
  "api": {
    "method": "post",
    "url": "/XXX/XXXX/page",
    "data": { "current": "${page}", "size": "${perPage}" }
  }
}
```

- **`C-05`** 后端分页字段非 page/perPage 时必须在 api.data 显式映射（crud 数据域自动提供 `${page}`/`${perPage}`/filter 字段）
  `来源:实战观察|状态:实战观察|版本:6.x|后果:后端收不到分页参数，分页失效`
- 响应结构非 amis 标准（要求 `{items, total}`）时必须加 adaptor → references/data-source.md §2（`A-02`）

## §4 headerToolbar 标准布局

```json
["reload", "filter-toggler", { "type": "button", "label": "Import", "actionType": "dialog", "dialog": {} }]
```

- **`C-06`** 用 `filter-toggler` 需 crud 设 `"filterTogglable": true`；`columns-toggler`/`drag-toggler` 直接使用无需配置
  `来源:官方文档(amis 6.13.0)|状态:据官方文档|版本:6.13.0|后果:开关按钮不显示`
  注：`columnsToggled` 属性不存在（v1.1 已修正误记）

## §5 状态列 mapping

```json
{
  "name": "status", "label": "Status", "type": "mapping",
  "map": {
    "Enabled": "<span class='label label-success'>Enabled</span>",
    "Disabled": "<span class='label label-danger'>Disabled</span>",
    "*": "<span class='label label-default'>(blank)</span>"
  }
}
```

- **`C-07`** mapping 必须写 `*` 兜底 key
  `来源:实战观察|状态:实战观察|版本:6.x|后果:未命中值显示空白`

## §6 operation 操作列

```json
{
  "type": "operation", "label": "Action", "fixed": "right", "width": 220,
  "buttons": [ { "type": "button-group", "buttons": [ { "按钮1": "..." }, { "按钮2": "..." } ] } ]
}
```

- **`C-08`** 操作列 `fixed: "right"` + `width` 固定；行内多按钮用 button-group 收拢
  `来源:实战观察|状态:实战观察|版本:6.x|后果:平铺按钮撑爆列宽`
- 行数据字段经数据域直接取（如弹层 title 写 `"Edit - ${code}"`）；弹层 form 传 id 用 hidden → references/form-controls.md §4（`F-08`）

## §7 filter 顶部搜索表单

filter 字段自动进入 crud 数据域，api.data 用 `${字段名}` 引用；actions 放 Reset + Submit 按钮。完整写法见 examples/crud-full.json。

## §8 loadDataOnce

小数据量（全量字典/配置类列表）用 `"loadDataOnce": true`：首次请求拉全量，后续分页/排序在前端完成。弹层内嵌选择器常用 → examples/bulk-actions-picker.json（`D-10`）。

## §9 刷新机制（权威定义在弹层域 D-03/D-05/D-11）

| 场景 | 写法 | 规则 |
|------|------|------|
| 事件动作（onEvent.actions 内） | `{"actionType":"reload","componentId":"..."}` | `D-03` |
| action 类型按钮 | `{"type":"action","actionType":"reload","target":"crudName"}`（官方合法写法） | `D-03` |
| close:false 弹层提交 | submitSucc 显式 componentId reload（**唯一**写法） | `D-05` |
| 弹层默认关闭模式（close 缺省） | form api 里加 `"reload": "目标crud的name"`；`"reload":"none"` 可关闭 | `D-11` |
