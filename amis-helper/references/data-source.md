# API 与数据源

## §1 api 配置三种写法

```json
// 1. 字符串简写（GET）
"api": "/XXX/XXXX/list"

// 2. 方法前缀简写
"api": "put:/XXX/XXXX/reset/${id}"

// 3. 对象（推荐，可控制 data/headers）
"api": {
  "method": "post",
  "url": "/XXX/XXXX/page",
  "data": { "current": "${page}", "size": "${perPage}" }
}
```

支持的 method：get/post/put/delete。

## §2 响应结构转换（adapter/adaptor）

amis 标准响应：`{ status: 0, data: { items: [...], total: n } }`。

非标准响应必须转换，两种位置：

```json
// crud/form 的 api：转响应结构（adapter 或 adaptor 均有效，官方标准名是 adaptor）
{
  "api": {
    "method": "post",
    "url": "/XXX/XXXX/page",
    "adapter": "return { ...payload, data: { items: payload.data.rows, total: payload.data.total } };"
  }
}

// select 等的 source：转字典数据
{
  "source": {
    "url": "/XXX/XXXX/dict/list?type=Country",
    "adaptor": "return { status: payload.code === 200 ? 0 : payload.code, data: payload.data };"
  }
}
```

常见转换场景：
- 后端分页字段是 `rows/total` → 转成 `items/total`
- 后端业务码 `code: 200` → 转成 `status: 0`
- adaptor 是 JS 片段，可用 `return { ...payload, ... }` 展开原 payload

## §3 变量取值

| 变量 | 来源 |
|------|------|
| `${page}` / `${perPage}` / `${total}` | crud 数据域 |
| `${行字段名}` | 行上下文（operation 列按钮、弹层 title） |
| `${term}` | autoComplete 搜索词 |
| `${selectedItems}` / `${selectedItems.length}` / `${selectedItems\|pick:字段}` | crud 选中行 |
| `${file}` | input-file |
| `${ENV.xxx}` / `${LC_LOCALE}` | 环境变量 |

## §4 表达式条件显隐

- `visibleOn: "${xxx == 'a'}"` 控制显隐（visible 直接布尔）
- `disabledOn: "!${selectedItems.length}"` 控制禁用
- sendOn 控制联想请求触发条件

## §5 CRUD 与 Service 数据域

外层 Service 的 `data` 声明的变量（如 loading 标记）会进入作用域链，内层所有组件可读。crud 自己 setValue 的变量不会向上/向外传播 → 弹层 loading 必须走 Service 包层（dialog-actions.md §4）。
