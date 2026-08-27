# 踩坑手册

格式：症状 → 错误写法 → 正确写法。生成配置后对照本表自检。

## P1 弹层与动作

### P1.1 form onEvent.submit 拦截 API
- 症状：点击提交按钮接口不调用，submitSucc 也不触发，loading 卡死
- 错误：form 配了 `onEvent.submit`
- 正确：删掉 submit 事件，只用 `submitSucc` / `submitFail`

### P1.2 提交后弹框立即关闭，loading 无效
- 症状：API 未返回弹框已关，看不到 loading
- 错误：`actionType: "submit"` 默认 `close: true`
- 正确：提交按钮加 `close: false`，`submitSucc` 中 `closeDialog`，`submitFail` 不关

### P1.3 事件动作 reload 用 target 不生效
- 症状：submitSucc 里 reload 了但表格不刷新
- 错误：`{ "actionType": "reload", "target": "crudName" }`
- 正确：`{ "actionType": "reload", "componentId": "crud的id" }`，crud 必须设 `id`

### P1.4 close:false 模式下 api.reload 不生效
- 症状：form api 里写了 reload 但表格不刷
- 原因：`close: false` 阻止了 api.reload 触发
- 正确：在 `submitSucc` 中显式 `{"actionType": "reload", "componentId": "..."}`

### P1.5 CRUD setValue 变量不传播
- 症状：headerToolbar 按钮 `loadingOn: "${exportDownloading}"` 读不到变量
- 原因：crud 内 setValue 的变量不传播到 headerToolbar 子组件
- 正确：Service 包裹 crud，`data` 显式声明变量，setValue 的 componentId 指向 service

### P1.6 blob 导出 loading 卡死
- 症状：`ajax` action + `responseType: "blob"` + `then`，then 不触发
- 正确：改用 `actionType: "download"`

### P1.7 fetch() 请求 401
- 症状：custom action 里 fetch() 报 401
- 原因：fetch 不携带 AMIS auth token
- 正确：用 AMIS 内置 `download` action

## P2 Select / 联想

### P2.1 autoComplete 不触发联想
- 错误：`"autoComplete": true` + 外部 `source: {...}`
- 正确：`autoComplete` 直接是对象（method/url/sendOn 都在里面）

### P2.2 联想下拉显示 invalid label
- 错误：adapter 字符串转换返回字段名（此 AMIS 版本不执行）
- 正确：后端直接返回标准 `label`/`value` 字段（推荐），或前端 labelField/valueField

### P2.3 联想响应格式错
- 错误：`data: { options: [...] }` 嵌套
- 正确：autoComplete 模式下 data 直接是数组

### P2.4 sendOn 位置错
- 错误：sendOn 放在 source 对象内
- 正确：放在 autoComplete 对象内

## P3 分页与工具栏

### P3.1 每页条数切换器不出现
- 错误：`{ "type": "switch-per-page", "perPageOptions": [...] }` 写在 footerToolbar 里（属性名错+位置错）
- 正确：crud 顶层 `"perPageAvailable": [20, 50, 100, 150]` + footerToolbar 里字符串简写 `"switch-per-page"` + `defaultParams.perPage`
- 依据：amis-ui BasicPaginationProps 接口定义，官方 issue #6685

### P3.2 单页时底部统计条不显示
- 症状：total <= perPage 时 statistics 不渲染，textContent 属性无效
- 正确：用 `{ "type": "tpl", "tpl": "Total ${total} records" }`

## P4 布局

### P4.1 表单项宽度控制无效
- 错误：`size: "xl"`（只控样式）/ `inputClassName: "w-xl"`（无此类）/ `style.width`（不传到 input）
- 正确：`"columnRatio": 2`

## P5 格式

### P5.1 JSON 内注释导致校验失败
- 症状：amis Schema 严格校验报错 "JSON 中不允许有注释"
- 正确：配置内禁止注释，说明写在配置外的文档里
