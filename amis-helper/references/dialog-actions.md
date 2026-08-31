# 弹层与动作链

规则 ID 前缀 `D-xx`，元数据四要素：`来源|状态|版本|违反后果`。

## §1 弹层提交标准模式

所有「确认操作」弹层（新增/编辑/删除/导入）统一此结构：

```json
{
  "type": "button", "label": "删除", "level": "danger", "icon": "fa fa-trash",
  "actionType": "dialog",
  "dialog": {
    "title": "确认删除",
    "actions": [
      { "type": "button", "label": "取消", "actionType": "close" },
      { "type": "button", "label": "确认删除", "level": "danger", "actionType": "submit", "close": false }
    ],
    "body": {
      "type": "form",
      "onEvent": {
        "submitSucc": { "actions": [
          { "actionType": "reload", "componentId": "目标crud的id" },
          { "actionType": "closeDialog" }
        ] }
      },
      "api": { "method": "post", "url": "/XXX/XXXX/delete", "data": { "id": "${id}" } },
      "body": [ { "type": "alert", "body": "确认删除该条记录?", "level": "warning" } ]
    }
  }
}
```

- **`D-01`** 提交按钮 `close: false` + `submitSucc` 内手动 `closeDialog`；`submitFail` 不用写（默认保持弹层打开可重试，实测失败分支无需处理）
  `来源:实战观察+V-1-D实测(2026-08-31)|状态:已实测|版本:6.13.0|后果:弹层秒关看不到 loading，接口失败无法重试`
- **`D-04`** 弹层提交按钮**不配 `loadingOn`**、不需要 Service 变量与 `setValue`——submit 按钮有内建 loading（实测 loadingOn 恒 false 照样转圈）
  `来源:V-1/V-1-D实测(2026-08-31)|状态:已实测|版本:6.13.0|后果:死配置，误导读者`
  例外：download 导出按钮**必须**配对 → §2（`D-08`）
- **`D-05`** `close: false` 下 form api 的 `reload` **不生效**、提交也**不默认刷新** CRUD（实测带不带 reload 均无 crud 请求），api 里**不要写 reload**；唯一写法是 `submitSucc` 显式 `{"actionType":"reload","componentId":"..."}`（E 组实证）
  `来源:V-2实测(2026-08-31)|状态:已实测|版本:6.13.0|后果:表格不刷新`
- **`D-06`** 禁止 form `onEvent.submit`——会拦截 `actionType:"submit"` 的内置调用，接口不发出
  `来源:实战观察|状态:实战观察|版本:6.x|后果:接口不调用、submitSucc 不触发、loading 卡死`
- **`D-07`** 确认弹层用 `actionType:"dialog"` 自定义弹框，不用 `confirmText`
  `来源:实战观察|状态:实战观察|版本:6.x|后果:原生框无法 loading、无法展示复杂提示`
- **`D-11`** 弹层默认关闭模式（close 缺省）下 form api 的 `reload`（值为 crud 的 `name`）生效，提交后自动刷新 CRUD；可用 `"reload": "none"` 显式关闭
  `来源:官方文档(crud「增」章节)|状态:据官方文档,未实测|版本:6.x|后果:行为未经本地实测，注意与 D-05（close:false 下相反）的边界`

## §2 下载/导出（唯一正确写法）

```json
{
  "type": "button", "label": "Export", "level": "warning", "icon": "fa fa-download",
  "loadingOn": "${exportDownloading}",
  "onEvent": {
    "click": {
      "actions": [
        { "actionType": "setValue", "componentId": "外层service", "args": { "value": { "exportDownloading": true } } },
        { "actionType": "download", "args": { "api": { "method": "get", "url": "/XXX/XXXX/export", "data": { "code": "${code}" } } } },
        { "actionType": "setValue", "componentId": "外层service", "args": { "value": { "exportDownloading": false } } }
      ]
    }
  }
}
```

- **`D-02`** 文件下载/导出只用 `actionType:"download"`（自带 auth token）；禁止 `ajax`+`responseType:"blob"`+`then`、禁止裸 `fetch()`
  `来源:实战观察|状态:实战观察|版本:6.x|后果:then 不触发 loading 卡死 / fetch 无 token 401`
- **`D-08`** download 按钮**必须** `loadingOn` + 外层 Service 变量 + `setValue true/false` 配对（download 无内建 loading）；实测顺序 action 会**等待下载完成**（waitSeconds=3 → loading 持续 3 秒）
  `来源:V-3实测(2026-08-31)|状态:已实测|版本:6.13.0|后果:点击无反馈，用户重复点击`

## §3 reload 定位方式（`D-03` 详情）

| 位置 | 属性 | 说明 |
|------|------|------|
| 事件动作（`onEvent.actions` 内） | `componentId` | 匹配组件 `id`；**此处** `target` 不生效 |
| `{"type":"action","actionType":"reload"}` 按钮 | `target` | 值为组件 `name`，**官方支持的合法写法**，勿误判为错误 |
| form api 配置 | `reload` | 值为组件 `name`；仅默认关闭模式有效（`D-11`，未实测）；`close:false` 下不生效（`D-05`） |

- **`D-03`** 事件动作内 reload 必须用 `componentId`（`target` 失效），目标组件必须设 `id`
  `来源:实战观察|状态:实战观察|版本:6.x|后果:reload 不生效`
- 被刷新 crud 同时设 `id` 和 `name` → references/crud.md §1（`C-02`）

## §4 Service 包装层（仅无内建 loading 的按钮需要）

- **`D-09`** loading 变量声明在**外层 Service 的 `data`**，`setValue` 的 componentId 指向 service（机制：crud 内 setValue 不向外传播 → references/data-source.md §5 `A-01`）；弹层提交按钮不需要 Service → `D-04`
  `来源:实战观察|状态:实战观察|版本:6.x|后果:loadingOn 读不到变量恒 false`

```json
{ "type": "service", "id": "pageStateService", "data": { "exportDownloading": false }, "body": [ { "type": "crud", "id": "xxxCrud", "name": "xxxCrud" } ] }
```

作用域链：按钮 → CRUD → **service** → page。

## §5 弹层内嵌选择器

完整可落地配置 → examples/bulk-actions-picker.json。要点：

- **`D-10`** 选择一批数据回填用 dialog/drawer + crud(`loadDataOnce:true`) + `bulkActions`；`${selectedItems|pick:字段}` 提取字段数组、`${selectedItems.length}` 显示选中数、`disabledOn: "!${selectedItems.length}"` 未选中禁用
  `来源:实战观察|状态:实战观察|版本:6.x|后果:提交格式错 / 空选可提交`
- 长内容侧滑用 `drawer`，普通用 `dialog`
