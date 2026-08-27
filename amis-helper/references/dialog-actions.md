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
        "close": false,
        "loadingOn": "${deleteLoading}"
      }
    ],
    "body": {
      "type": "form",
      "onEvent": {
        "submitSucc": {
          "actions": [
            { "actionType": "setValue", "componentId": "外层service", "args": { "value": { "deleteLoading": false } } },
            { "actionType": "reload", "componentId": "目标crud的id" },
            { "actionType": "closeDialog" }
          ]
        },
        "submitFail": {
          "actions": [
            { "actionType": "setValue", "componentId": "外层service", "args": { "value": { "deleteLoading": false } } }
          ]
        }
      },
      "api": {
        "method": "post",
        "url": "/XXX/XXXX/delete",
        "data": { "id": "${id}" },
        "reload": "目标crud的name"
      },
      "body": [
        { "type": "alert", "body": "确认删除该条记录?", "level": "warning" }
      ]
    }
  }
}
```

关键规则：
- `close: false`：阻止提交后立即自动关弹框（否则 loading 没意义）
- `submitSucc` 中手动 `closeDialog`；`submitFail` **不关**（用户可重试）
- **禁止 form `onEvent.submit`**：会拦截 `actionType: "submit"` 的内置 API 调用，接口不发出
- loading 变量声明在外层 Service 的 `data` 里（crud 的 setValue 不传播到 headerToolbar）→ §4
- 确认弹层用 `actionType: "dialog"` 自定义弹框，不用 `confirmText`（浏览器原生框无法 loading、无法展示复杂提示）
- `close: false` 模式下 form api 的 `reload` 不生效（见 pitfalls P1.4），可省略；刷新统一靠 `submitSucc` 内显式 `{"actionType": "reload", "componentId": "..."}` 触发。examples 中 api.reload 保留仅作"语义标记"，不影响功能

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
| 事件动作（onEvent 内） | `componentId` | 匹配组件的 `id` 属性；用 `target` 不生效 |
| form api 配置 | `reload` | 值为组件 `name` |

所以被刷新的 crud 必须**同时**设 `id` 和 `name`。

## §4 Service 包装层（loading 变量作用域）

问题：crud 内 `setValue` 的变量不传播到 headerToolbar 子组件，按钮 `loadingOn` 读不到。

```json
{
  "type": "service",
  "id": "pageStateService",
  "data": { "exportDownloading": false, "formLoading": false },
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
