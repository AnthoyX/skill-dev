# API 与数据源

规则 ID 前缀 `A-xx`，元数据四要素：`来源|状态|版本|违反后果`。

## §1 api 配置三种写法

1. 字符串简写（GET）：`"api": "/XXX/XXXX/list"`
2. 方法前缀简写：`"api": "put:/XXX/XXXX/reset/${id}"`
3. 对象（推荐，可控制 data/headers）：

```json
{
  "api": {
    "method": "post",
    "url": "/XXX/XXXX/page",
    "data": { "current": "${page}", "size": "${perPage}" }
  }
}
```

支持的 method：get/post/put/delete。

## §2 响应结构转换（`A-02`）

- **`A-02`** 非 amis 标准响应必须用 `adaptor` 转换，**统一用官方标准名 `adaptor`**（`adapter` 也能识别但禁止混用）
  `来源:实战观察|状态:实战观察|版本:6.x|后果:数据不渲染（status 非 0 / 字段名不匹配）`

amis 标准响应：`{ "status": 0, "data": { "items": [...], "total": n } }`。两个转换位置：

```json
{ "api": { "method": "post", "url": "/XXX/XXXX/page",
  "adaptor": "return { ...payload, data: { items: payload.data.rows, total: payload.data.total } };" } }
```

```json
{ "source": { "url": "/XXX/XXXX/dict/list?type=Country",
  "adaptor": "return { status: payload.code === 200 ? 0 : payload.code, data: payload.data };" } }
```

常见转换：后端分页字段 `rows/total` → `items/total`；业务码 `code:200` → `status:0`；adaptor 是 JS 片段，可用 `return { ...payload, ... }` 展开原 payload。

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

- `visibleOn: "${xxx == 'a'}"` 控制显隐（`visible` 直接布尔）
- `disabledOn: "!${selectedItems.length}"` 控制禁用
- `sendOn` 控制联想请求触发条件（位置规则 → references/form-controls.md §3 `F-04`）

## §5 CRUD 与 Service 数据域（`A-01`）

- **`A-01`** 外层 Service `data` 声明的变量进入作用域链，内层所有组件可读；**crud 自己 setValue 的变量不向上/向外传播** → loading 等状态变量必须走 Service 包层（写法 → references/dialog-actions.md §4 `D-09`）
  `来源:实战观察|状态:实战观察|版本:6.x|后果:headerToolbar 按钮 loadingOn 读不到变量恒 false`
