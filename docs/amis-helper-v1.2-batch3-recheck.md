# amis-helper v1.2 批次 3 复审报告

| 项 | 值 |
|---|---|
| 评审对象 | `amis-helper` v1.2 批次 3 **执行结果**（4 片段拆分 + examples/INDEX.md + 联动改动） |
| 审查文件 | `examples/crud-base.json` / `dialog-import.json` / `dialog-form-add.json` / `dialog-form-edit.json` / `INDEX.md`；联动 `META.md` / `SKILL.md §4` / `references/crud.md §7` |
| 评审基准 | `docs/amis-helper-batch3-split-plan.md`（§3 切面 / §8 裁决）、`docs/amis-helper-v1.2-batch3-review.md`（前置评审 B1/B2/B3）、`docs/amis-helper-v1.2-batch3-b3-verify.md`（B3 实测）、32 条权威规则 + P-01~P-16 |
| 审查方式 | 全文通读 4 新片段 + INDEX + 5 权威规则文件逐条核对；`git show HEAD:examples/crud-full.json` 取回原文做 1:1 等价性比对；CRLF 字节级校验 |
| 评审日期 | 2026-08-31 |
| 结论 | **放行**（0 阻塞，3 建议） |

---

## 0. 结论摘要

B1/B2/B3 三处返工点全部正确落地，等价性与规则自洽性通过，断链清零，体量与 CRLF 达标。无阻塞项，可进入批次 4。

## 1. 逐项核对表

### 1.1 等价性（对照原 crud-full.json 310 行）

| 片段 | 取自原行号 | 结论 |
|---|---|---|
| crud-base (144) | 1-79 + 205-232 + 234-255(骨架) + 300-304 | ✅ 1:1；`templateDownloading:false`(B3)、`filterTogglable:true`(B2) 为有意新增，方案 §8 已记录 |
| dialog-import (71) | 80-147 | ✅ 1:1 + B3 loadingOn 三件套；尾逗号已去 |
| dialog-form-add (57) | 148-204 | ✅ 1:1 无属性变动 |
| dialog-form-edit (41) | 256-296 | ✅ 1:1（static name 无 value 与原一致） |

行数守恒：144+71+57+41=313 ≠ 309，+4 全部来自 B2/B3 补属性（filterTogglable 1 行 + loadingOn 1 行 + setValue 2 行），方案 §8 已如实标注「+1/+4/-0/0」。

### 1.2 规则自洽（重点项逐条核对）

| 关注点 | 规则 | 结果 |
|---|---|---|
| close:false 弹层 api 内无 reload | D-05 | ✅ import/add/edit 三处 form api 均无 reload，靠 submitSucc `componentId` reload |
| 提交按钮无 loadingOn | D-04 | ✅ Confirm Import/Submit/Save 三按钮均无 loadingOn |
| adaptor 拼写 | A-02 | ✅ crud api + country source 均 `adaptor` |
| asBlob + form-data 成对 | F-05 | ✅ import 弹层 `asBlob:true` + `dataType:"form-data"` |
| mapping `*` 兜底 | C-07 | ✅ crud-base 有 `"*"` |
| autoComplete 对象 + sendOn 位置 | F-03/F-04 | ✅ filter 与 add 弹层两处均对象内、sendOn 在 autoComplete 内 |
| 下载/导出 loadingOn 三件套 | D-08 | ✅ Export 与模板下载均 setValue(pageStateService, true/false) 配对 |
| 多选四件套 | F-01 | ✅ country select 齐全 |
| filter-toggler 需 filterTogglable | C-06 | ✅ B2 已补 |

### 1.3 INDEX.md（32 行 ≤60）

| 项 | 结果 |
|---|---|
| 宿主依赖与片段实际引用一致 | ✅ crud-base 自包含；import 依赖 `pageStateService.templateDownloading + mainCrud.id`；add/edit 依赖 `mainCrud.id`（edit 另含行上下文）均与片段内 componentId 引用吻合 |
| 规则 ID 映射真实 | ✅ 6 片段映射 ID 全部能在片段内找到对应实现，均在 32 条冻结集内；B1 已删 bulk-actions-picker 的 D-11，改文字注「规则盲区」 |
| buttons:[] 骨架占位声明 | ✅ §2 醒目声明 + 组合结构树完整 |
| 无悬空文件引用 | ✅ 未引用 self-check.md 等未建文件 |

### 1.4 断链检查

| 检查 | 结果 |
|---|---|
| `crud-full` 全包引用 | ✅ 仅 META(历史说明) + INDEX(自身说明) 出现，均描述性文字，非失效链接 |
| `examples/*.json` 引用 | ✅ 仅 dialog-actions.md / crud.md → `bulk-actions-picker.json`（存在） |
| META 计数 vs 实际 | ✅ 6 个 .json + 1 个 INDEX.md，与实际目录一致 |

### 1.5 约束符合

| 项 | 结果 |
|---|---|
| 单片段 ≤150 行 | ✅ 144/71/57/41 |
| INDEX ≤60 行 | ✅ 32 行 |
| JSON 无注释（R-01） | ✅ |
| CRLF | ✅ 字节级校验：7 文件 CRLF 全覆盖，0 个 lone LF |
| B3「视觉待复核」表述 | ✅ INDEX 注明「机制已实测生效…视觉在 6.13.0 SDK 下待复核」，未写死「配了即有视觉反馈」 |

## 2. 阻塞项

无。

## 3. 建议项（可选，不阻塞）

| # | 位置 | 问题 | 建议 |
|---|---|---|---|
| S1 | `META.md` 第 56 行 | `self-check.md 批次 4 新增` 写在「示例」括号内，归属（示例 vs 参考文档）语义模糊 | 批次 4 落地时明确归属，避免 6/5 计数口径混淆 |
| S2 | `SKILL.md` frontmatter `version: 1.1.0` | v1.2 三批次已落地但版本号未 bump | v1.2 全部批次完成后统一改 1.2.0 |
| S3 | `META.md` §可信度分级 | D-08 仍标「已实测」，但 b3-verify 指出 button loading 视觉在 6.13.0 下待复核 | 后续批次复核 D-08「视觉反馈」前提（INDEX 已正确标注，本批次不动规则符合 B3 选 A 决策） |

## 4. 附注

- `dialog-import` 模板下载按钮的 `setValue` 只传 `{templateDownloading}` 单字段，与原 Export 按钮 `{exportDownloading}` 模式一致，依赖 amis setValue 对对象 value 的 merge 语义；原 crud-full 已实测有效，无风险。
