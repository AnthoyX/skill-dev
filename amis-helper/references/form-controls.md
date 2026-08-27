# 表单控件

## §1 字典/枚举下拉（source + adaptor）

```json
{
  "type": "select",
  "name": "country",
  "label": "Country",
  "clearable": true,
  "multiple": true,
  "searchable": true,
  "extractValue": true,
  "joinValues": true,
  "delimiter": ",",
  "labelField": "name",
  "valueField": "name",
  "source": {
    "method": "get",
    "url": "/XXX/XXXX/dict/list?type=Country",
    "adaptor": "return { status: payload.code === 200 ? 0 : payload.code, data: payload.data };"
  }
}
```

- 后端返回 `{code: 200, data: [...]}` 非 amis 标准（要求 status 0）时，adaptor 转换 status
- 多选必带四件套：`multiple` + `extractValue` + `joinValues` + `delimiter`（提交逗号分隔字符串）
- 简写也行：`"source": "/XXX/XXXX/dict/list?type=Country"`（后端已标准时）

## §2 必填与校验

```json
{
  "type": "select",
  "name": "code",
  "required": true,
  "validations": { "isRequired": true }
}
```

- `required: true` 显示红星，`validations.isRequired` 强制拦截提交，两个都写
- 邮箱类：`"validations": { "isEmail": true }` + `"validateOnChange": true`
- 远程唯一性校验：`"validateApi": "/XXX/XXXX/validate?mail=${email}"`
- 长度限制：`"maxLength": 200`（textarea）

## §3 远程联想 select（autoComplete，正确写法）

```json
{
  "type": "select",
  "name": "code",
  "label": "Item",
  "placeholder": "Search by code or name",
  "clearable": true,
  "overlayStyle": { "width": "450px" },
  "autoComplete": {
    "method": "get",
    "url": "/XXX/XXXX/search?keyword=${term}",
    "sendOn": "${term != null && term.length >= 3}"
  }
}
```

规则：
- `autoComplete` **必须是对象**；写 `true` + 外部 `source` 不触发联想
- `sendOn` 写在 autoComplete 对象**内**（放 source 内失效）
- `${term}` 是 AMIS 默认搜索词变量（GET 为 query 参数）
- 下拉项数据格式：**直接是数组**（不是 `{options: [...]}` 嵌套）
- 【后端配合项】推荐后端适配（最稳）：后端 DTO 直接返回 amis 标准 `label`/`value` 字段（如 `label = "code | name"`、`value = code`），前端零映射配置，下拉与选中框都显示 label。此方案需后端改造，前端无法独立完成
- 降级方案（后端不配合时）：前端用 `labelField`/`valueField` + `menuTpl` 定制下拉展示，能用但选中后输入框只显示 labelField 指向的单字段
- **adapter 字符串转换在此版本不可用**（报 invalid label），勿选
- 后端 SQL 加 `LIMIT 10` 兜底
- `overlayStyle.width` 控制下拉面板宽度

排查：输入不触发联想时按序检查——① Network 请求没发出（sendOn/autoComplete 配置错）→ ② 404（路由未部署）→ ③ 401（需登录）→ ④ 200 但显示 invalid label（返回字段与 labelField 不匹配）→ ⑤ 选中值不对（valueField 错）

## §4 编辑弹层的展示字段

```json
{
  "type": "static",
  "name": "code",
  "label": "Code",
  "value": "${code}"
}
```

行上下文字段用 `static` 只读展示 + `hidden` 传 id。

## §5 文件上传（Excel 导入）

```json
{
  "type": "input-file",
  "name": "file",
  "label": "Excel File",
  "accept": ".xlsx,.xls",
  "asBlob": true,
  "required": true,
  "hint": "Template: code / type / remark",
  "btnText": "Select File",
  "reUploadBtnText": "Re-upload"
}
```

提交的 form api 必须加：

```json
{
  "api": {
    "method": "post",
    "url": "/XXX/XXXX/import",
    "dataType": "form-data"
  }
}
```

规则：`asBlob: true`（文件以二进制随表单提交）+ `dataType: "form-data"` 成对出现。

## §6 宽度控制（只认 columnRatio）

| 尝试 | 结果 |
|------|------|
| `columnRatio: 2` | ✅ 表单项在 grid 布局占 2 列宽 |
| `size: "xl"` | ❌ select 的 size 只控制样式不控宽度 |
| `inputClassName: "w-xl"` | ❌ 该 AMIS 版本无此内置 CSS 类 |
| `style: { width: "350px" }` | ❌ 作用在外层 div，不传到内部 input |

## §7 常用控件清单

input-text / textarea / select / input-number / input-date / input-date-range / input-quarter（季度选择）/ input-year / input-email / input-password / radios / checkboxes / input-file / hidden / static / uuid（隐藏生成唯一值）/ combo（动态增删行）
