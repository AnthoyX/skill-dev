# 弹层与动作链

## §1 弹层提交 + loading 防重复（标准模式）

所有"确认操作"弹层（新增/编辑/删除/导入）统一此结构：

```json
{
  "type": "button",
  "label": "删除",
  "level": "danger",
  "icon": "fa fa-trash",
  "actionType": "dialog",
  "dialog": {
    "title": "确认删除",
    "actions": [
      { "type": "button", "label": "取消", "actionType": "close" },
      {
        "type": "button",
        "label": "确认删除",
        "level": "danger",
        "actionType": "submit",
        "close": false
      }
    ],
    "body": {
      "type": "form",
      "onEvent": {
        "submitSucc": {
          "actions": [
            { "actionType": "reload", "componentId": "目标crud的id" },
            { "actionType": "closeDialog" }
          ]
        }
      },
      "api": {
        "method": "post",
        "url": "/XXX/XXXX/delete",
        "data": { "id": "${id}" }
      },
      "body": [
        { "type": "alert", "body": "确认删除该条记录?", "level": "warning" }
      ]
    }
  }
}
```

关键规则（依据 2026-08-31 实测，amis 6.13.0）：
- `close: false`：**必须**。阻止提交后立即自动关弹框——否则弹层秒关，loading 根本看不见
- **不要给提交按钮配 `loadingOn`**：`actionType: "submit"` 的按钮有 amis **内建 loading**（实测：`loadingOn` 恒为 false 时按钮照样转圈，配了也是死配置）。接口失败时内建 loading 会正常结束、弹层保持打开、可再次提交，**无需任何 `setValue` 配合**
- `submitSucc` 中手动 `closeDialog`；`submitFail` **不用写**（默认就不关弹层，可重试）
- **禁止 form `onEvent.submit`**：会拦截 `actionType: "submit"` 的内置 API 调用，接口不发出
- 确认弹层用 `actionType: "dialog"` 自定义弹框，不用 `confirmText`（浏览器原生框无法 loading、无法展示复杂提示）
- 弹层**默认关闭模式**（close 缺省）下提交后自动刷新 CRUD（官方 crud 文档「增」章节，据官方文档未实测）；`close: false` 模式下**默认不刷新**（V-2 实测：提交后无任何 crud 请求）
- `close: false` 模式下 form api 的 `reload` **不生效**（V-2 实测：带 reload 与不带均无 crud 请求，submitSucc 显式 reload 才触发），**api 里不要写 `reload`**；唯一可靠写法是 `submitSucc` 显式 `{"actionType": "reload", "componentId": "..."}`（V-2 E 组实证有效）

## §2 下载/导出（唯一正确写法）

```json
{
  "type": "button",
  "label": "Export",
  "level": "warning",
  "icon": "fa fa-download",
  "loadingOn": "${exportDownloading}",
  "onEvent": {
    "click": {
      "actions": [
        { "actionType": "setValue", "componentId": "外层service", "args": { "value": { "exportDownloading": true } } },
        {
          "actionType": "download",
          "args": {
            "api": {
              "method": "get",
              "url": "/XXX/XXXX/export",
              "data": { "code": "${code}" }
            }
          }
        },
        { "actionType": "setValue", "componentId": "外层service", "args": { "value": { "exportDownloading": false } } }
      ]
    }
  }
}
```

规则：
- 只用 `actionType: "download"`：自带 auth token + 返回 Promise（顺序 action 会等待完成）
- 禁止 `ajax` action + `responseType: "blob"` + `then`（then 不触发，loading 卡死）
- 禁止裸 `fetch()`（不带 AMIS auth token，401）

## §3 reload 定位方式（易错点）

| 位置 | 属性 | 说明 |
|------|------|------|
| 事件动作（`onEvent.actions` 内） | `componentId` | 匹配组件的 `id` 属性；**此处**用 `target` 不生效 |
| `{"type":"action","actionType":"reload"}` 按钮 | `target` | 值为组件 `name`，**官方支持的合法写法**（官方 crud 文档「刷新按钮」章节），不要误判为错误 |
| form api 配置 | `reload` | 值为组件 `name`；仅默认关闭模式有效（据官方文档），`close: false` 下不生效（V-2 实测） |

所以被刷新的 crud 建议**同时**设 `id` 和 `name`，两种定位方式都能命中。

## §4 Service 包装层（仅导出/下载类按钮需要）

**弹层提交按钮不需要 Service 包层**——submit 有内建 loading（见 §1）。
只有 `onEvent.click` + `download` 这类**无内建 loading 的按钮**才需要 loading 变量：
crud 内 `setValue` 的变量不传播到 headerToolbar 子组件，按钮 `loadingOn` 读不到，
所以变量必须声明在外层 Service 的 `data` 里。

```json
{
  "type": "service",
  "id": "pageStateService",
  "data": { "exportDownloading": false },
  "body": [ { "type": "crud", "id": "xxxCrud", "name": "xxxCrud", "...": "..." } ]
}
```

作用域链：按钮 → CRUD → **service** → page。setValue 的 componentId 指向 service。

## §5 弹层内嵌选择器（dialog/drawer + crud + bulkActions）

选择一批数据回填时（如给分组批量绑定数据），drawer + crud(loadDataOnce) + bulkActions：

```json
{
  "type": "crud",
  "loadDataOnce": true,
  "bulkActions": [
    {
      "type": "button",
      "label": "Add Selected (${selectedItems.length})",
      "level": "primary",
      "actionType": "ajax",
      "disabledOn": "!${selectedItems.length}",
      "api": {
        "method": "put",
        "url": "/XXX/XXXX/bind",
        "data": {
          "idList": "${selectedItems|pick:id}",
          "groupCode": "${groupCode}"
        }
      },
      "close": true,
      "reload": "父crud的name"
    }
  ]
}
```

- `${selectedItems|pick:字段名}` 从选中行提取单字段数组
- `${selectedItems.length}` 显示选中数，`disabledOn: "!${selectedItems.length}"` 未选中禁用
- 长内容侧滑用 `drawer`，普通用 `dialog`
