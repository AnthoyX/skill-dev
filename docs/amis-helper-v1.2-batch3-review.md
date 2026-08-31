# amis-helper v1.2 批次 3 评审报告

| 项 | 值 |
|---|---|
| 评审对象 | `amis-helper` v1.2 批次 3（拆分 crud-full.json + 新建 examples/INDEX.md + META 计数同步） |
| 审查文件 | `docs/amis-helper-batch3-split-plan.md`（方案）/ `examples/crud-full.json`（待拆原文） |
| 评审基准 | `docs/amis-helper-iteration-plan.md`（§5.2 的 1.2.8 / 1.2.9、§4.4、§6.6 Q3） |
| 审查方式 | 全文通读方案 + 310 行原文 + 5 权威规则文件 + 2 保留片段，逐行核对切面守恒与规则 ID 映射 |
| 评审日期 | 2026-08-31 |
| 结论 | **需返工**（方案级轻量修正：2 阻塞 + 1 强建议，不改架构） |

---

## 0. 结论摘要

切面行号守恒（309 行 1:1 无遗漏）、片段形态（按钮配置）合理、宿主依赖约定完备、4 个确认点倾向均可执行。**但 INDEX.md 规则 ID 映射存在 2 处不自洽**（B1/B2），会导致交付即错，须先改方案再执行；另有 1 处示例违反已实测规则（B3）需裁决。

## 1. 审查清单

```yaml
检查1_切面守恒: pass    # 143+68+57+41=309，与原 309 有效行 1:1 无遗漏；233 行 ] 属骨架胶水未显式列（见 §5 附注）
检查2_片段形态: pass    # 弹层片段=按钮配置形态，与 dialog-confirm-loading/bulk-actions-picker 一致，可独立 json.load
检查3_宿主依赖: pass    # crud id/name=mainCrud、Service id=pageStateService 仅导出需要，4 新片段 + 2 保留依赖明细准确
检查4_INDEX映射: fail   # B1 bulk-actions-picker 标 D-11 错误；B2 crud-base 漏 C-06
检查5_示例规则一致: fail # B2 crud-base 用 filter-toggler 缺 filterTogglable（违 C-06）；B3 Download Template 违 D-08
检查6_体量: warn        # crud-base 143/150 余 7 行；B2/B3 若补属性将超限
检查7_确认点: 见 §3     # Q1~Q4 裁决表
```

## 2. 问题分级清单

### 阻塞级（必须改，否则 INDEX 与规则实际内容冲突）

| # | 位置 | 问题 | 证据 | 修正建议 |
|---|---|---|---|---|
| B1 | 方案 §5 映射表 bulk-actions-picker | 标 `D-11(reload 合法写法)` 是**映射错误** | D-11 权威定义是「**form api** 的 reload（close 缺省）」；`bulk-actions-picker.json` 的 `reload:"mainCrud"` 是 **`actionType:"ajax"` 按钮**的 reload 属性，且按钮显式 `close:true`。32 条规则**无精确对应**，属覆盖盲区 | 改为文字说明「ajax action 按钮 reload 指向 name（规则盲区，勿套 D-11/D-03）」，或后续单独补规则 |
| B2 | 方案 §5 映射表 crud-base | 用 `filter-toggler` 但映射跳过 `C-06`，且 crud 缺 `filterTogglable:true`（违反 C-06） | 原文 78 行 `"filter-toggler"`，crud 配置（18-35 行）无 `filterTogglable`；`crud.md §4` C-06 明确「用 filter-toggler 需设 filterTogglable」；映射「C-01~C-05, C-07, C-08」恰跳 C-06 | 二选一自洽：① 补 `filterTogglable:true` + 映射标 C-06（推荐）；② 删 `filter-toggler` |

### 强建议级（需裁决，否则示例违反已实测规则）

| # | 位置 | 问题 | 裁决选项 |
|---|---|---|---|
| B3 | dialog-import（原 127-143 行 Download Template） | 用 `actionType:"download"` 但无 `loadingOn` + Service 变量 + setValue 配对，违反 D-08（V-3 实测「download 无内建 loading，必须配对」）；方案映射只标 D-02，回避 D-08 | **A**（推荐）：补 loadingOn 三件套 → dialog-import 宿主依赖改为「依赖 pageStateService + templateDownloading」；**B**：D-08 补豁免「静态模板下载可无 loadingOn」（超出批次 3 范围） |

### 建议级（可选，不阻塞）

| # | 位置 | 问题 | 建议 |
|---|---|---|---|
| S1 | 方案 §7 Q3 | 「各 1 行小改」预估偏乐观 | SKILL.md §4 实为**段重写**（3 文件 → INDEX + 4 新拆 + 2 保留），如实更新工作量 |
| S2 | 方案 §7 Q4 | 拆分后失去「整页一次看全」 | INDEX 补「组合结构树」（缩进文本示意挂载位置，≤10 行），比保留 310 行完整 JSON 划算 |
| S3 | 方案 §3 切面表 | 第 233 行 `],`（headerToolbar 闭合）未显式归属；`footerToolbar(300-304)` 已含在 297-309 内重复列出 | 切面表补注 233 行归 crud-base 骨架胶水；删重复的 footerToolbar 描述 |
| S4 | 方案 §2 vs §3 | 「可独立 json.load」与「1:1 平移」隐含冲突 | dialog-import（80-147）/dialog-form-add（148-204）平移需**去尾逗号**，方案明说 |
| S5 | 方案 §6 META | 「示例：6 个」措辞 | 写明「6 个 .json + 1 个 INDEX.md 索引」，与「参考文档：5 份」区分，避免 INDEX 被误算为示例 |

## 3. 确认点裁决表

| 确认点 | 结论 | 理由 |
|---|---|---|
| Q1 空 buttons 骨架 | **接受，但加约束** | `buttons:[]` 可接受，但空 operation 列（`width:220` 无按钮）易被模型当终态；INDEX 组合说明须**醒目声明「空列是骨架占位，Edit/Delete/Picker 片段粘贴于此」**。若担心误导，可放 1 个极简按钮壳作占位 |
| Q2 filter 是否挪出 | **不挪** | 143 行在预算内，filter 是 F-01/F-03/F-04/F-06 的教学载体，拆走破坏「整页骨架」定位；但 B2/B3 补属性后须重估 150 上限 |
| Q3 两处过期引用 | **改，且是「必须」非「顺手」** | 不改 = 断链交付，直接违反 v1.2 验收「交叉引用失效率 0%」，属拆分动作的必要闭环；SKILL.md §4 是段重写非 1 行 |
| Q4 保留组合完整版 | **不保留** | 150 行硬约束优先；用 INDEX「组合结构树」弥补整页参考损失，性价比高于 310 行完整 JSON |

## 4. 行数守恒校验

| 项 | 值 | 结论 |
|---|---|---|
| 原 crud-full.json | 309 有效行（310 含末尾空行） | — |
| 片段合计 | 143+68+57+41 = **309** | ✅ 守恒 |
| crud-base 贴预算 | 143 / 150 | ⚠️ 余量仅 7 行，B2/B3 走「补属性」路线将超限 |

## 5. 附注（执行细节，不影响方案结论）

- **233 行 `],` 归属**：切面表未列，实为 headerToolbar 闭合，属 crud-base 骨架胶水，拼接时自然补齐，非内容丢失；建议切面表补注避免误判。
- **尾逗号**：`dialog-import`（80-147）、`dialog-form-add`（148-204）取自 headerToolbar 数组元素，末行 `},` 须去尾逗号才能独立 `json.load`；`dialog-form-edit`（256-296）是 buttons 数组末元素，无尾逗号。
- **B1/B2/B3 联动**：若 B2 补 filterTogglable + B3 走方案 A（补 loadingOn），`crud-base` 与 `dialog-import` 行数同步上升，需连带重估 `crud-base` 是否再瘦身（与 Q2 联动）。
- **规则盲区记录**：`actionType:"ajax"` 按钮的 `reload` 属性（指向 name）在 crud.md §9 四种 reload 场景中均未覆盖，属批次 1 冻结规则的盲区，建议在 v2.0 或后续批次补规则，勿临时硬套 D-11/D-03。
