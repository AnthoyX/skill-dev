# amis-helper v1.2 批次 3 · B3 实测报告

| 项 | 值 |
|---|---|
| 对象 | `amis-helper` v1.2 批次 3 评审中的 B3 决策点（dialog 内 download 按钮的 loadingOn 三件套） |
| 目的 | 用实测裁决「A（补 loadingOn，动示例）vs B（给 D-08 加豁免，动规则）」，并验证 A 的可行性 |
| 环境 | 本地实验室 `_amis-lab/`（amis 6.13.0 SDK + mock `waitSeconds` 延迟） |
| 方法 | playwright-cli 自动化点击 + MutationObserver 变量时间线 + waitForResponse 响应锚定 |
| 日期 | 2026-08-31 |
| 结论 | **选 A，机制可行**；另发现 button loading 视觉疑点在 6.13.0 SDK 下无表现（需复核） |

---

## 0. 一句话结论

**dialog 内 `setValue componentId` 定位外层 Service 完全生效，download 精确等待 3 秒**——之前担心的「dialog 作用域隔离」不存在。**A 方案机制成立，选 A 不变**。

但顺带发现一个更深的坑：**6.13.0 SDK 下 button 的 loading 视觉（loadingOn / loading:true / ajax 内建）均无 DOM 表现**，与 V-1「submit 内建 loading 转圈」、V-3「loading 写法有效」存在张力，需拿官方 demo 站点复核。

---

## 1. 背景（B3 是什么）

批次 3 拆分 `crud-full.json` 时，评审发现 `dialog-import` 片段（Import 弹层）里的「Download Template」按钮：

```json
{ "type": "button", "label": "Download Template", "actionType": "download",
  "args": { "api": { "method": "get", "url": "/XXX/XXXX/downloadTemplate" } } }
```

它用了 `actionType:"download"` 但**没有 `loadingOn` + Service 变量 + `setValue` 配对**，违反 `D-08`（「download 无内建 loading，必须 loadingOn + setValue 配对，否则点击无反馈」）。

两个修法：

| 方案 | 做法 | 代价 |
|---|---|---|
| **A** | 补 loadingOn 三件套（动示例，不动冻结规则） | 宿主依赖从「不依赖 Service」变为「依赖 pageStateService + 变量」 |
| **B** | 给 D-08 加豁免「静态模板下载可无 loadingOn」 | 动冻结规则，语义边界模糊 |

评审与用户均倾向 A，但 A 有一个隐患：**D-08 的 V-3 实测对象是 headerToolbar 的 Export 按钮（dialog 外），而 Download Template 在 dialog 内**——「dialog 内 setValue 能否定位外层 Service」是未实测变体。因此先实测。

---

## 2. 实验设计

在 `_amis-lab/schema.json` 建两组（归档 `schemas/v4-dialog-download-loading.json`）：

```yaml
page
└─ service (id=pageStateService, data={templateDownloading:false, exportDownloading:false})
   ├─ tpl 显示两个变量值          # 用 MutationObserver 监听它的变化
   ├─ G组: dialog(Import) 内「Download Template」按钮
   │     loadingOn="${templateDownloading}"
   │     onEvent.click = setValue(pageStateService, true) → download(waitSeconds=3) → setValue(pageStateService, false)
   └─ 对照组: dialog 外「download」按钮（复现 V-3 场景，变量 exportDownloading）
```

验证两个点：
1. **dialog 内 setValue 是否生效**——看 templateDownloading 是否真的变 true
2. **download 是否等待完成**——看变量从 true 变回 false 的时刻是否 ≈ 3 秒后

---

## 3. 实测数据

### 3.1 变量时间线（MutationObserver，相对点击时刻）

| 组 | 变量变化序列 | download 响应耗时 |
|---|---|---|
| G 组（dialog 内） | `[38ms:true, 3051ms:false]` | respMs = 3042ms |
| 对照组（dialog 外，V-3 场景） | `[41ms:true, 3049ms:false]` | respMs = 3050ms |

**解读**：两组行为完全一致——setValue true 在点击后 ~40ms 生效，download 精确等待 3 秒返回，setValue false 在响应返回后（~3050ms）立即执行。

### 3.2 关键结论 1：dialog 内 setValue 生效

G 组 `templateDownloading` 在 dialog 内被 `setValue componentId=pageStateService` 成功写入外层 Service（38ms 变 true）。**componentId 是全局定位，不受 dialog 作用域隔离影响。**

### 3.3 关键结论 2（意外发现）：button loading 视觉无表现

对按钮 loading 视觉做了三组补充测试，**按钮 DOM 均无任何变化**：

| 触发方式 | 按钮 class / innerHTML / attribute |
|---|---|
| 静态 `loading: true`（primary） | 无 spinner、无 is-disabled、icon 不变 |
| `loadingOn` 表达式为 true | 同上 |
| `actionType: ajax` 执行期间（内建 loading） | MutationObserver 监听 3.5s 得**空数组**，无任何 mutation |

即：即使变量已经是 true（MutationObserver 已证实），按钮也没有「转圈 / 禁用 / 图标替换」等任何 DOM 层面的 loading 反馈。

---

## 4. 结论与建议

### 4.1 对 B3：选 A，机制可行

- ✅ dialog 内 setValue 定位外层 Service 生效（38ms true）
- ✅ download 等待完成（3042ms）
- ✅ 宿主依赖「依赖 pageStateService + templateDownloading」成立

**A 的价值**：① 机制能跑通；② 保持 SSOT 一致（示例遵守自己的 D-08 规则），「动示例不动冻结规则」零涟漪。

### 4.2 待复核项（不影响 B3，但影响 D-08）

「button loading 视觉无表现」可能是：① 本地 `embed` 环境 + cxd 主题的视觉弱化；② amis 6.13.0 真实行为变化。**需拿官方 demo 站点（`aisuda.bce.baidu.com/amis/zh-CN/components/button`）对比定性。**

若确认 6.13.0 button loading 视觉确实失效，则 D-08「配 loadingOn 有视觉反馈」的前提动摇，需在后续批次复核 D-08；但**这不改变 B3 选 A**（A 的机制与 SSOT 一致性仍成立）。

### 4.3 落地建议

给 `dialog-import` 补 loadingOn 三件套时，标注「button loading 视觉待复核」，不要把「配了 loadingOn 就有视觉反馈」当已证事实写死。

---

## 5. 附注：实测方法坑

- `body.innerText` 采样有严重竞态（dialog 遮罩下会读到旧快照，多次误判变量为 false），**必须用 MutationObserver + page.waitForResponse 双重锚定**才可靠。
- mock 用 `waitSeconds=3` 制造延迟，`page.waitForResponse` 锚定响应时刻，是判断「是否等待完成」的唯一干净手段。
