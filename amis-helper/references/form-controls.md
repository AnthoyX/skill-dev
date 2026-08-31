# 表单控件

规则 ID 前缀 `F-xx`，元数据四要素：`来源|状态|版本|违反后果`。

## §1 字典/枚举下拉（source + adaptor）

```json
{
  "type": "select", "name": "country", "label": "Country",
  "clearable": true, "multiple": true, "searchable": true,
  "extractValue": true, "joinValues": true, "delimiter": ",",
  "labelField": "name", "valueField": "name",
  "source": {
    "method": "get",
    "url": "/XXX/XXXX/dict/list?type=Country",
    "adaptor": "return { status: payload.code === 200 ? 0 : payload.code, data: payload.data };"
  }
}
```

- **`F-01`** 多选必带四件套：`multiple` + `extractValue` + `joinValues` + `delimiter`
  `来源:实战观察|状态:实战观察|版本:6.x|后果:提交的是数组而非逗号分隔字符串，后端解析失败`
- 后端返回 `{code:200,data:[...]}` 非 amis 标准时用 `adaptor` 转 status → references/data-source.md §2（`A-02`）
- 后端已标准时 source 可字符串简写

## §2 必填与校验

- **`F-02`** 必填双写：`required: true`（显示红星）+ `validations: {"isRequired": true}`（拦截提交）
  `来源:实战观察|状态:实战观察|版本:6.x|后果:只有红星不拦截，或只拦截无提示`
- 邮箱：`"validations": {"isEmail": true}` + `"validateOnChange": true`；远程唯一性：`"validateApi": "/XXX/XXXX/validate?mail=${email}"`；textarea 长度：`"maxLength": 200`

## §3 远程联想 select（autoComplete）

```json
{
  "type": "select", "name": "code", "label": "Item",
  "placeholder": "Search by code or name", "clearable": true,
  "overlayStyle": { "width": "450px" },
  "autoComplete": {
    "method": "get",
    "url": "/XXX/XXXX/search?keyword=${term}",
    "sendOn": "${term != null && term.length >= 3}"
  }
}
```

- **`F-03`** `autoComplete` **必须是对象**（method/url/sendOn 都在内）；写 `true` + 外部 `source` 不触发联想
  `来源:实战观察|状态:实战观察|版本:6.x|后果:联想不触发`
- **`F-04`** `sendOn` 写在 autoComplete 对象**内**（放 source 内失效）
  `来源:实战观察|状态:实战观察|版本:6.x|后果:联想不触发`
- `${term}` 是 amis 默认搜索词变量（GET 为 query 参数）；`overlayStyle.width` 控制下拉面板宽度
- 排查链（联想不生效时按序）：请求未发出（sendOn/autoComplete 配置错）→ 404（路由未部署）→ 401（需登录）→ 显示 invalid label（`F-10`）→ 选中值不对（valueField 错）

## §4 编辑弹层展示字段

- **`F-08`** 行上下文只读展示用 `static`（`"type":"static","name":"code","label":"Code","value":"${code}"`）；提交需要的主键用 `{ "type": "hidden", "name": "id" }`
  `来源:实战观察|状态:实战观察|版本:6.x|后果:提交缺主键 / 可编辑字段被误改`

## §5 文件上传（Excel 导入）

```json
{
  "type": "input-file", "name": "file", "label": "Excel File",
  "accept": ".xlsx,.xls", "asBlob": true, "required": true,
  "hint": "Template: code / type / remark", "btnText": "Select File", "reUploadBtnText": "Re-upload"
}
```

提交的 form api 必须加 `"dataType": "form-data"`：

```json
{ "api": { "method": "post", "url": "/XXX/XXXX/import", "dataType": "form-data" } }
```

- **`F-05`** `asBlob: true`（文件二进制随表单提交）与 api `dataType: "form-data"` 必须成对出现
  `来源:实战观察|状态:实战观察|版本:6.x|后果:后端收不到文件`

## §6 宽度控制（只认 columnRatio）

- **`F-06`** 控制表单项宽度用 `columnRatio`（grid 布局占列数，如 `"columnRatio": 2`）
  `来源:实战观察|状态:实战观察|版本:6.x|后果:宽度设置不生效`

| 尝试 | 结果 |
|------|------|
| `size: "xl"` | ❌ select 的 size 只控制样式不控宽度 |
| `inputClassName: "w-xl"` | ❌ amis 6.13.0 无此内置 CSS 类 |
| `style: { "width": "350px" }` | ❌ 作用在外层 div，不传到内部 input |

## §7 协作约束（需后端配合，前端无法独立完成）

- **`F-09`** 联想下拉显示完整 label 的最稳方案：后端 DTO 直接返回 amis 标准 `label`/`value` 字段（如 `label = "code | name"`、`value = code`），前端零映射
  `来源:实战观察|状态:实战观察|版本:6.x|后果:改用降级方案则选中框只能显示单字段`
- 降级方案（后端不配合）：前端 `labelField`/`valueField` + `menuTpl` 定制下拉展示，选中后输入框只显示 labelField 指向的单字段
- 后端 SQL 加 `LIMIT 10` 兜底

## §8 invalid label 陷阱

- **`F-10`** adapter 字符串转换在 amis 6.13.0 不可用（报 invalid label），勿选
  `来源:实战观察|状态:实战观察|版本:6.13.0|后果:下拉项显示 invalid label`

## §9 常用控件清单

input-text / textarea / select / input-number / input-date / input-date-range / input-quarter / input-year / input-email / input-password / radios / checkboxes / input-file / hidden / static / uuid / combo
