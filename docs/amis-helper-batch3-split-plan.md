# amis-helper v1.2 批次 3 拆分方案（待评审）

> 状态：方案已产出，未执行。本文档供外部 AI 评审 + 确认点裁决使用。
> 评审基准：`docs/amis-helper-iteration-plan.md`（§5.2 改动项 1.2.8/1.2.9、§4.4 体量预算、§6.6 Q3 决策=选 B 拆分）。

## 1. 背景与已完成进度

```yaml
skill: amis-helper/（百度 amis 低代码 JSON Schema 生成）
阶段: v1.2 SSOT 重构
已完成:
  批次1: commit 5d3d67c + ee1a027 — ID 体系冻结，权威规则 32 条
        (R-01 + C-01~C-08 + D-01~D-11 + F-01~F-10 + A-02 等)，每条带 来源|状态|版本|违反后果
  批次2: commit ded35a5 — pitfalls.md 重编号 P-01~P-16 纯引用化；
        SKILL.md 硬规则降级为 ID 索引 + 触发矩阵
本批次(3): 拆分 examples/crud-full.json(310行, 超150行预算2.2倍) + 新建 examples/INDEX.md + META.md 计数同步
保留不动: dialog-confirm-loading.json(42行) / bulk-actions-picker.json(59行)，仅登记进 INDEX.md
```

## 2. 硬性约束

- 拆分行为等价：不回潮 v1.1 已清理死配置（弹层提交禁 `loadingOn`/`setValue` 三件套、close:false 下 api 内禁 `reload`、统一 `adaptor` 拼写）
- 每个片段 JSON 可独立 `json.load` 校验；弹层片段为「挂在父页 headerToolbar / operation 列的按钮配置」形态
- 单 example ≤150 行；INDEX.md ≤60 行；CRLF 行尾；JSON 内禁止注释（R-01）
- 规则 ID 只引已冻结 32 条 + P-01~P-16；INDEX.md 不引用不存在文件（self-check.md 批次 4 才建）

## 3. 拆分切面（按原 crud-full.json 行号，1:1 平移不改属性值）

| 新文件 | 取自原行号 | 内容 | 预估行数 |
|---|---|---|---|
| `crud-base.json` | 1-79, 205-232, 234-255, 297-309 + footerToolbar(300-304) | page + Service 包层(pageStateService/exportDownloading) + alert + crud(api+adaptor/filter/headerToolbar前2项/导出按钮/columns+mapping/operation列骨架/footerToolbar统计条) | ~143 |
| `dialog-import.json` | 80-147 | 完整 Import 按钮（dialog + input-file asBlob + form-data + 模板下载） | ~68 |
| `dialog-form-add.json` | 148-204 | 完整 Add 按钮（dialog + 新增表单） | ~57 |
| `dialog-form-edit.json` | 256-296 | 完整 Edit 按钮（dialog + static/hidden 编辑表单） | ~41 |

- 原 `crud-full.json` 删除
- 弹层内容 1:1 平移 → 行为天然等价（已核对无死配置回潮）

## 4. 片段间宿主依赖约定

```yaml
固定标识:
  crud: {id: mainCrud, name: mainCrud}   # 3 个新弹层 submitSucc reload 的 componentId 指向它
  service: {id: pageStateService, data: {exportDownloading: false}}  # 仅 crud-base 导出按钮需要
宿主依赖明细:
  crud-base:              自包含（含 Service 与 crud）
  dialog-import:          挂 headerToolbar；需 mainCrud.id；不依赖 Service/行上下文
  dialog-form-add:        挂 headerToolbar；需 mainCrud.id；不依赖 Service/行上下文
  dialog-form-edit:       挂 operation.buttons；需 mainCrud.id + 行上下文 ${code}/${name}/${id}
  dialog-confirm-loading: 挂 operation.buttons；需 mainCrud.id + ${code}/${id}（既有，保留）
  bulk-actions-picker:    挂 operation.buttons；需 mainCrud.name(reload target, D-11 默认关闭模式) + ${groupCode}/${groupId}（既有，保留）
```

## 5. INDEX.md 结构（≤60 行）

- 片段清单表：文件｜场景｜宿主依赖｜覆盖规则 ID｜行数
- 覆盖规则映射：

| 片段 | 覆盖规则 ID |
|---|---|
| crud-base | C-01~C-05, C-07, C-08, D-02, D-08, D-09, A-01, A-02, F-01, F-03, F-04, F-06 |
| dialog-import | D-01, D-04, D-05, D-02(模板下载), F-05 |
| dialog-form-add | D-01, D-04, D-05, F-02, F-03, F-04 |
| dialog-form-edit | D-01, D-04, D-05, F-08 |
| dialog-confirm-loading | D-01, D-04, D-05, D-07 |
| bulk-actions-picker | D-10, D-11(reload 合法写法), A-02 |

- 组合说明段：crud-base 为骨架 → Import/Add 粘进 headerToolbar → Edit/Delete/Picker 粘进 operation.buttons（即原 crud-full 的组合方式）

## 6. META.md 改动（仅 1 处）

规则数量段：`示例：3 个` → `示例：6 个（4 个新拆片段 + 2 个保留，索引见 examples/INDEX.md）`

## 7. 确认点（请评审 AI 逐条给意见）

```yaml
Q1_operation_buttons_empty:
  问题: crud-base.json 的 operation 列 buttons 留空数组做骨架，
        还是保留一个不含 dialog 的按钮壳/示例？
  倾向: buttons: []，靠 INDEX.md 说明粘贴位置（最干净，无死配置）
  顾虑: 空数组是否会被模型误解为「operation 列可以没有按钮」

Q2_行数切面:
  问题: crud-base ~143 行贴近 150 上限，是否需要再瘦身
        （如 filter 的 autoComplete select 挪到独立片段）？
  倾向: 不挪。filter 是 crud 教学价值最高的部分，拆走反而破坏「整页骨架」定位

Q3_两处过期引用归属:
  问题: 拆分后以下引用将指向已删除的 crud-full.json，本批次是否顺手改？
    - SKILL.md §4 第 59 行「examples/crud-full.json：列表页全套骨架…」
    - references/crud.md §7 末尾「完整写法见 examples/crud-full.json」
  约束: 本批次声明「只动 examples/ 与 META.md」；但留着就是断链
  倾向: 顺手改为指向 examples/INDEX.md（各 1 行小改，风险极低）

Q4_组合完整性:
  问题: 拆分后失去「整页一次看全」能力，评审基准 §6.6 风险表建议
        「保留一个组合后的完整示例供对照」，是否需要？
  倾向: 不保留。 crud-full 内容 = 4 片段 1:1 拼接，无信息损失；
        INDEX.md 组合说明已足够，保留完整版违背 150 行预算初衷
```

## 8. 评审裁决与执行修正（2026-08-31，batch3-review + b3-verify）

```yaml
评审: docs/amis-helper-v1.2-batch3-review.md（需返工，2 阻塞 + 1 强建议）
裁决落地:
  B1: bulk-actions-picker 映射删 D-11 → INDEX.md 注明「ajax 按钮 reload 指向 name，
      属规则盲区勿套 D-11/D-03，v2.0 待补」
  B2: 选① crud-base 补 filterTogglable:true，映射标 C-06（crud-base 映射改 C-01~C-08）
  B3: 选 A（b3-verify 实测确认：dialog 内 setValue componentId 定位外层 Service 生效 38ms，
      download 精确等待 waitSeconds=3）→ dialog-import 模板下载按钮补 loadingOn 三件套
      （${templateDownloading}），crud-base Service data 增 templateDownloading 声明；
      按 b3-verify §4.3，INDEX.md 注明「button loading 视觉在 6.13.0 SDK 下待复核」，
      未写死「配 loadingOn 即有视觉反馈」
确认点终裁: Q1 buttons:[] + INDEX 醒目声明（已做）；Q2 filter 不挪；Q3 必改
  （SKILL.md §4 段重写 + crud.md §7 改指 INDEX.md，本批次一并完成）；Q4 不保留完整版，
  INDEX 补组合结构树（已做）
S1~S5: 全采纳（Q3 工作量如实；切面表 233 行归骨架胶水、dialog-import/form-add 平移已去尾逗号；
  META 措辞改「6 个 .json + 1 个 INDEX.md 索引」）
实际行数: crud-base 144 / dialog-import 71 / dialog-form-add 57 / dialog-form-edit 41
  （较预估 +1/+4/-0/0，来自 B2/B3 补属性；全部 ≤150）
```

