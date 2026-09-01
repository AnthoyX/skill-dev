# amis-helper v1.2 批次 1 评审报告

| 项 | 值 |
|---|---|
| 评审对象 | `amis-helper` v1.2 批次 1（commit `5d3d67c`） |
| 改造前基线 | v1.1.0（commit `7d1dea8`） |
| 审查文件 | `references/crud.md` / `dialog-actions.md` / `form-controls.md` / `data-source.md` / `META.md` |
| 评审基准 | `docs/plan-iteration.md`（§4.3 / §5.1 / §5.2 / §6.1） |
| 评审日期 | 2026-08-31 |
| 结论 | **需返工**（阻塞级 6 项） |

---

## 0. 结论摘要

批次 1 的 ID 体系大方向正确：前缀归属全部对应、C/D/A 域无重号跳号、绝大多数规则四要素齐全、行数全部达标、V 系列实测表述与 §5.1 一致。但存在 **1 处编号断裂、1 处 SSOT 状态矛盾、3 处悬空引用、2 处信息丢失**，不能放行。

---

## 1. 审查清单

```yaml
检查1_ID体系: fail
  issues:
    - {文件: form-controls.md, 行号: "§4 之前", 问题: "F-07 漏号，编号从 F-06 直接跳到 F-08，F 域实际只有 9 条", 建议: "补 F-07（如原『必填双写』可拆出邮箱/远程/长度校验），或确认 F 域为 9 条并修正 META 统计"}
    - {文件: META.md, 行号: 54, 问题: "『权威规则 30 条（R-01 + C×8 + D×10 + F×10 + A×2）』：F 实际 9 条，括号内明细相加=31 与『30 条』自相矛盾", 建议: "F×10 改 F×9，明细相加与总数对齐"}
    - {文件: META.md, 行号: 55, 问题: "声称排障条目『P-01～P-16』，但 pitfalls.md 仍是 P1.1~P5.1 旧编号，编号体系未落地", 建议: "pitfalls.md 重编号后再写 P-xx，或标注『待落地』"}
  归属核对: "C→crud / D→dialog-actions / F→form-controls / A→data-source / R→META 全部正确；仅 F-07 漏号"

检查2_元数据: fail
  issues:
    - {文件: META.md vs dialog-actions.md, 行号: "46 vs 65-66", 问题: "META 分级表把 D-02 列入『已实测』，但 D-02 权威定义标『状态:实战观察』；且 D-02（只用 download/禁 ajax+blob/禁 fetch）未被 V-3 直接验证，V-3 只验证 download 等待完成（属 D-08），META 属虚标", 建议: "以权威定义为准，META 分级表『已实测』去掉 D-02"}
    - {文件: META.md, 行号: 38, 问题: "R-01 状态标『已实测』但来源写『实战观察』，V 系列四项实测均未覆盖『JSON 注释报错』，依据不足", 建议: "改『据官方文档』或补实测记录"}
  核对: "『已实测』实际出现在 D-01/D-04/D-05/D-08/R-01 共 5 处，其中 R-01 依据不足，D-02 该标未标"

检查3_SSOT: warn
  issues:
    - {文件: data-source.md §5 vs dialog-actions.md §4, 行号: "61 vs 84", 问题: "A-01 与 D-09 共享同一机制（crud setValue 变量不传播）和同一后果（loadingOn 读不到变量恒 false），两者都完整写了一遍，边界模糊", 建议: "机制归 A-01，D-09 只留 loading 应用并 ID 引用 A-01，删重复的机制/后果"}
    - {文件: crud.md §9 / dialog-actions.md §1末尾 / §3第3行, 行号: "107 / 45 / 76", 问题: "『默认关闭模式下 form api reload 有效』未分配 ID，散落三处（均标据官方文档未实测）", 建议: "分配独立 ID 或并入 D-05 的未实测分支，其余改 ID 引用"}
  正面: "reload 核心已收敛：crud.md §9 降级为索引表并明示权威在弹层域，D-03/D-05 各一处权威定义"

检查4_信息丢失: fail
  issues:
    - {文件: form-controls.md §3, 行号: 47-52, 问题: "旧版『下拉项数据格式：直接是数组（非 {options:[...]} 嵌套）』整条丢失（仅 pitfalls P2.3 残留）", 建议: "补回或并入 F-03 后果说明"}
    - {文件: form-controls.md §3 排查链, 行号: 52, 问题: "『invalid label 根因=返回字段与 labelField 不匹配』被统一改指 F-10，但 F-10 只讲『adapter 字符串转换不可用』，两类根因混为一谈", 建议: "排查链保留两类根因：① adapter 转换不可用（F-10）② 字段与 labelField 不匹配"}
    - {文件: crud.md §7, 行号: 94, 问题: "filter 完整 JSON 示例被删，改为指向不存在的 examples/crud-base.json", 建议: "改指 crud-full.json 或补回 filter 精简 JSON"}
    - {文件: dialog-actions.md §5, 行号: 93-99, 问题: "bulkActions 完整 JSON 删除，D-10 文字未覆盖 actionType:ajax / close:true / reload:父crud 等细节", 建议: "可选，在 D-10 补一句『提交用 ajax + reload 父 crud 的 name』"}
    - {文件: crud.md §2 / form-controls.md §9, 行号: "34 / 103", 问题: "『tpl 一定渲染』正向说明、控件清单括号注释丢失", 建议: "轻微，可回补"}
  data-source.md: "无信息丢失（§1 去 // 注释符合 R-01，§2 两段 adaptor 代码块完整保留）"

检查5_实测一致性: warn
  issues:
    - {文件: dialog-actions.md §1末尾 / crud.md §9, 行号: "45 / 107", 问题: "迭代计划 §5.1 改动项 1.1.10 要求补『可用 reload:none 关闭』，两处均只写『默认自动刷新…未实测』，reload:none 缺失", 建议: "补『可用 reload:\"none\" 关闭默认刷新』"}
  V-1/V-2/V-3 核对: "一致：D-04（loadingOn 冗余）、D-05（close:false 下 api.reload 不生效+默认不刷新+submitSucc 唯一写法）、D-08（download 等待完成）与 §5.1 吻合；『语义标记』等旧说法已清除，无残留过期表述"

检查6_行数: pass
  结果: "crud.md 107 / dialog-actions.md 99 / form-controls.md 103 / data-source.md 62 / META.md 60，全部 ≤120"

检查7_可执行性: fail
  issues:
    - {文件: META.md, 行号: 55-56, 问题: "悬空引用『参考文档 6 份（含 self-check.md）』『示例见 examples/INDEX.md』——两个文件均不存在（references 仅 5 份、examples 仅 3 个 JSON）", 建议: "移除或标注『待建』"}
    - {文件: crud.md §7, 行号: 94, 问题: "悬空引用 examples/crud-base.json", 建议: 同上}
    - {文件: crud.md §1, 行号: 26-27, 问题: "C-02 后果『reload 定位不到目标』未区分：不设 name→target/api.reload 失效，不设 id→componentId 失效", 建议: "后果拆两句或精简指向正文说明"}

阻塞级问题数: 6
结论: 需返工
必须修:
  1. form-controls.md 补 F-07 或修正 F 域为 9 条
  2. META.md 规则数量修正（F×10→F×9，明细与总数对齐）
  3. META.md 分级表去掉 D-02（已实测）或对齐 D-02 状态（建议 META 去 D-02）
  4. META.md 移除/标注悬空引用（self-check.md、examples/INDEX.md、P-01~P-16）
  5. crud.md §7 悬空引用 crud-base.json 改指现有文件
  6. form-controls.md §3 补回「下拉数据格式=直接数组」+ 拆分 invalid label 两类根因
可选修复: reload:none 补回；C-02 后果精确化；§9 未实测条目分配 ID；A-01/D-09 去重；R-01 状态依据修正
```

---

## 2. 补充建议

### 2.1 批次边界治理（最优先）

本次批次只动了 4 个 reference + META，但 META 已经用新 ID 体系引用尚未改动的 `pitfalls.md`（仍是 P1.x）与 `SKILL.md`（硬规则表仍是数字 1~10），造成「文档声明 vs 现实」割裂。

建议：**META.md 只描述当前已落地状态**，超前内容一律标「待建」或删除。批次 1 的冻结边界应为「4 reference + META 的 ID 与元数据」，`pitfalls.md` / `SKILL.md` 归入批次 2。

### 2.2 修复优先级

| 级别 | 条目 | 理由 |
|---|---|---|
| P0 阻塞 | F-07 漏号、META 统计、D-02 状态矛盾、3 处悬空引用、2 处信息丢失 | 会让 AI 读到不存在的文件 / 自相矛盾的状态 |
| P1 建议 | reload:none 补回、C-02 后果精确化、§9 未实测条目分配 ID、A-01/D-09 去重 | 影响可执行性与 SSOT 纯净度 |
| P2 润色 | R-01 状态依据、控件清单注释、D 域编号顺序重排 | 不影响正确性 |

### 2.3 元数据「状态」迁移规则固化

D-04/D-05/D-08 已示范正确做法：升级为「已实测」时，来源必须带实测编号 + 日期（如 `V-2实测(2026-08-31)`）。建议在 META 固化为强制规范：

```
状态迁移：实战观察 →（实测通过）→ 已实测
升级条件：来源字段必须含 V-x 编号 + 日期，否则不得标已实测
```

R-01 正是违反此规范的反例（来源写实战观察却标已实测）。固化后可杜绝此类无依据升级。

### 2.4 SSOT 自动化校验

建议在批次完成后加一条验收动作：grep 每条规则的**加粗权威形态** `**\`X-xx\`**` 在全文出现次数必须为 1（权威定义），其余出现一律为 `\`X-xx\`` 纯引用形态。可用一条命令批量验证：

```
grep -rn '**[`]C-..[`]**' references/   # 每条应只命中 1 处
```

这能自动化拦截「同一条规则两处完整定义」这类漂移（本次 D-02 状态矛盾、A-01/D-09 重复正是此类）。

### 2.5 编号连续性验收

F-07 漏号这类问题靠人工读容易漏。建议给每个域文件加一条自检约定：**文件内最大编号 == META 声称的该域数量**，且编号无跳号。可作为 CHANGELOG 提交前的固定检查项。

### 2.6 后续批次顺序重排

原计划批次顺序依赖「ID 体系稳定」，建议调整为：

1. **本批次返工**（修 6 项阻塞）→ 冻结 ID 体系
2. 1.2.3 pitfalls 改写（依赖 ID 稳定，P-xx 重编号）
3. 1.2.2 SKILL 硬规则表降级为 ID 索引（依赖 pitfalls 与 reference 的 ID）
4. 1.2.5 self-check + 1.2.8 INDEX（正向清单与宿主依赖，依赖规则 ID 稳定）
5. 1.2.9 crud-full 瘦身（独立，可并行）
6. 1.2.11 CHANGELOG 收尾

理由：self-check / INDEX / SKILL 索引都以规则 ID 为锚点，ID 体系不冻结就做会重复返工（本次 META 提前引用 self-check/INDEX 就是教训）。

### 2.7 crud.md §9「默认关闭模式」条目的处理

该条「form api reload 在默认关闭模式下有效」从未实测（据官方文档），却散落三处且无 ID。建议二选一：

- **A**：分配 ID（如并入 D-05 的「未实测」分支），状态标「待验证」，其余两处改 ID 引用；
- **B**：明确降级为「参考信息」，不占规则 ID，三处合并为一处集中说明。

倾向 A——它是一条有边界条件的可执行规则（close 缺省 vs close:false 行为不同），值得正式编号，同时用「待验证」状态诚实标注可信度。
