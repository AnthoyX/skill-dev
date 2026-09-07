# 外部评审核验记录（2026-09-01）

核验对象：`docs/review-external-in-260901.yml`（第三方对 amis-helper v1.2.0 的评审反馈，13 条）
核验方式：逐条对照 `amis-helper/` 源码文件确认，不采信评审措辞本身
配套文档：`docs/review-external-out-260901.yaml`（发给外部 AI 的定夺提示词 + 回执结论）

## 1. 核验总览

| 结论 | 数量 | 明细 |
|---|---|---|
| 属实 | 10 | B2 B3 B4 B5 B6 / Q2 Q3 / S1 S2 S3 |
| 待核 | 2 | B1 B7（依赖仓库外的 `skill-card.md`） |
| 需实测定案 | 1 | Q1（F-02 必填双写） |

说明：

- **B1 / B7 无法本地核验**——`skill-card.md` 不在本仓库，是 ClawHub 平台在发布时生成的卡片。全仓库搜索无此文件。
- **Q1 是唯一能改变规则内容的一条**，其余均为文档格式/口径问题。已通过外部评审定夺（见 out 文档 Q1），待 V-11 实测确认最后一环。

## 2. 逐条判定

| 项 | 判定 | 关键证据 |
|---|---|---|
| B1 版本号打架 | 待核 | 内部一致（`SKILL.md` frontmatter 1.2.0 = CHANGELOG 1.2.0）；ClawHub 发布版 0.1.1 在仓库外 |
| B2 self-check 计数 | 属实 | 33 个 checkbox 覆盖 32 个唯一 ID；`C-02` 在第 14 行与第 54 行各出现一次。META「32 条」正确，**错的是 CHANGELOG「6 组 32 条」措辞** |
| B3 P-13 属性名混淆 | 属实 | `pitfalls.md` 提 `perPageOptions`，`crud.md` C-01 定义的是 `perPageAvailable` |
| B4 static 写法不一致 | 属实 | `dialog-form-edit.json` 的 `code` 带 `value:"${code}"`，`name` 不带；F-08 要求必带 |
| B5 示例含盲区配置 | 属实 | `bulk-actions-picker.json` 的 `"reload":"mainCrud"` + INDEX 自注「属规则盲区，勿套用」 |
| B6 adaptor 缺 total | 属实（低危） | 与 `crud-base.json` 的 adaptor 带 total 不一致；`loadDataOnce` 下无碍，切非全量模式会出错 |
| B7 artifact/ 死链 | 待核 | 同上，文件不在仓库 |
| Q1 F-02 必填双写 | 需实测 | 高度疑似误导性规则，影响 3 处（评审只报了 1 处） |
| Q2 D-11 未实测 | 属实 | `dialog-actions.md` 标「据官方文档,未实测」，却被 `self-check.md` 与 `crud.md §9` 依赖 |
| Q3 联想隐含前提 | 属实 | `crud-base.json` 的 autoComplete select 未配 labelField/valueField，隐含后端返回标准 label/value；INDEX 标「自包含」也不准 |
| S1 索引名不副实 | 属实 | `SKILL.md §1` 共 12 行 **13 个 ID** / 32 条，缺 19 条（含已实测的 D-05） |
| S2 元数据格式 | 属实 | D-01 来源写「实战观察+V-1-D实测」，其余已实测规则均为纯「V-x实测」 |
| S3 缺版本漂移策略 | 属实 | META 只写适用/不适用，无「非 6.13.0 环境如何降级」说明 |

## 3. Q1 影响面补正（评审漏报 2 处）

评审只提到 `examples/dialog-form-add.json:40`，实际共 3 处：

| 文件:行 | 内容 |
|---|---|
| `references/form-controls.md:28` | F-02 权威定义（根因） |
| `references/self-check.md:41` | 自检项「必填双写」 |
| `examples/dialog-form-add.json:39-40` | 示例照做双写 |

## 4. 评审遗漏（本轮新发现 N1-N5）

| ID | 问题 | 位置 | 处置 |
|---|---|---|---|
| **N1** | `D-03` 一个 ID 承载两种相反语义：`crud.md §9` 第 2 行把「action 按钮 reload 用 target」标 D-03，而 D-03 权威定义说「target 失效」。同一 ID 同时断言合法与失效，AI 读到自相矛盾 | `crud.md` §9 | 外部评审采纳，拆出 D-12（按钮级 reload） |
| N2 | C-02 无条件要求所有 crud 设 id+name，但 `bulk-actions-picker.json` 内层选择器 crud 两者皆无 | `crud.md:26` | 已限定为「被外部定位/刷新的 crud」 |
| N3 | 同 B6 的另一面：内层 crud 有 `switch-per-page` + `pagination` 但 total 缺失 | `bulk-actions-picker.json` | 并入 B6 处理 |
| N4 | `dialog-confirm-loading.json` 文件名残留——v1.1 删除 loadingOn 后已无 loading 语义 | 文件名 | 待 `git mv` 为 `dialog-confirm-danger.json` |
| N5 | 编辑弹层回填依赖 form 继承父级行数据（无 initApi），该前提未写入任何规则 | `dialog-form-edit.json` | 低优先，建议 F-08 补前提说明 |

## 5. 复核外部评审结论（核出 5 个问题）

定夺结论见 `review-external-out-260901.yaml` 第 285-430 行。5 条全部采纳，其中 Q3 纠正了我的方案（我主张拆 D-12/D-13，对方合并为单一 D-12，理由成立）。复核发现的问题：

| ID | 问题 | 处置 |
|---|---|---|
| N1' | **预算漏算**：结论写「规则层 607→~760，D-12 约 +8」，只算了 D-12，未算 META 新增（准入标准 / reload 载体总表 / 复检说明）与 pitfalls 新增 | 实算 v2.0 后 ~766；reload 总表顺延到 D-12 落地时一起加，避免悬空引用 |
| N2' | **D-12 合并后正文有歧义风险**：两种按钮写法时机不同（顶层 reload = 操作完成后刷新；`actionType:"reload"` + target = 点击立即刷新），一句话表述会让 AI 写错属性名 | 已写入 `plan-lab-handoff-260901.yaml`：正文必须两列表格，由 V-10 定夺是否可合并 |
| N3' | **V-10 未覆盖时序**：`bulk-actions-picker` 的按钮同时有 `close:true` 与 `reload`，先刷新还是先关窗未验证 | 已补进 V-10 追加对照 |
| N4' | **源码结论没转成排障条目**：Q1 挖出的两个真实坑（hidden 必填字段误拦截、combo 行级 required 不校验）只留在结论里 | 已列入 handoff：新增 P-17 / P-18 |
| N5' | **状态标注不合规**：F-02 落地动作写「来源升『官方文档+源码(V-x实测)』」，但 META 规定缺实测编号不得标「已实测」 | 改为两步：先标「据官方文档」，V-11 跑通后再补编号 |

## 6. 交叉收益

Q1 的源码结论 `formItem.validate()` 无 disabled 跳过逻辑——**disabled 字段仍参与校验**，直接回答了 v2.0 批次 A 中 V-6 的一半，影响 PM-03「字段只读」推荐写法。已回填进 `plan-v2.0.yaml` 的 V-6 条目。
