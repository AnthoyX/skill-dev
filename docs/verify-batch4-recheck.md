---
date: 2026-08-31
对象: amis-helper v1.2 批次 4 落地改动（第二轮复审）
范围: references/self-check.md（新建 54 行）+ META.md L56 + SKILL.md §3 触发矩阵 +1 行
依据: 首轮评审 docs/review-batch4.md + 迭代计划 §4.4/§5.2/§6.2 + 首轮输入 review-batch4-input.yaml
结论: 放行，0 阻塞，2 处建议修改（不阻塞）
---

# amis-helper v1.2 批次 4 复审意见

## 总评

**放行，0 阻塞，2 处建议修改（不阻塞）。** 首轮 4 项修改全部落实，32 条全覆盖、无 ID 错位、SSOT 合规、入口完备。

---

## 必查项逐项

### 1. 首轮 4 项修改落实 —— ✅ 通过

| 修改项 | 落实 |
|---|---|
| 位置 `references/self-check.md` | ✅ 已放 references/ |
| D-10 补入 | ✅ §3「弹层与动作」L30，D 组 11 条全齐 |
| 条目粒度（问句含判断关键词 + ≤1 行括注 + 不贴 JSON） | ✅ 无 ```json 代码块，问句均含属性名/组件名 |
| META L56 措辞 | ✅ 已改（5 份 + 1 份自检清单 + 示例计数） |

另：首轮优化建议也一并采纳——组名改「弹层与动作」、A-01 移「通用必查」（现 §1 通用含 R-01/A-02/A-01）。

### 2. self-check 内容质量 —— ✅ 通过（2 处建议优化）

- **32 条全覆盖**：R×1 + C×8 + D×11 + F×10 + A×2 = 32，C-02 二次引用（L14 + L54）符合设计说明。
- **无 ID 错位**：§6.2 原文的 C-02/C-03 错位**未重演**——L16 统计条→`C-04`、L14 id+name→`C-02`、L15 syncLocation→`C-03`。
- **无捏造属性名**：逐条扫描 `perPageAvailable`/`filterTogglable`/`loadDataOnce`/`selectedItems|pick`/`columnRatio` 等，全部出自 references 权威文件。
- 语义一致，2 处建议（见文末）。

### 3. SSOT 合规 —— ✅ 通过

self-check 全文均为裸 `` `X-xx` `` 引用，无 `**\`X-xx\`**` 或 `### \`X-xx\`` 权威形态；头部 L3 声明「只引规则 ID，权威写法见指向处」到位。

### 4. 体量与格式 —— ✅ 通过（字节级验证）

| 文件 | 行数 | CRLF | loneLF |
|---|---|---|---|
| self-check.md | 54 | 54 | 0 ✅ |
| META.md | 60（不变） | 60 | 0 ✅ |
| SKILL.md | 60（≤60） | 60 | 0 ✅ |

三文件纯 CRLF，无 lone LF；无 JSON 注释问题（self-check 无 JSON 内容）。

### 5. 入口完备 —— ✅ 通过

SKILL.md L54「任何生成任务完成后 → references/self-check.md」指向存在；self-check 引用的 META/references/pitfalls 均存在，无新悬空引用。

---

## 建议修改（2 处，不阻塞）

**S1 — self-check.md L24**

```
- [ ] 提交按钮 `close: false` + `submitSucc` 内手动 `closeDialog`（reload 在前）？→ `D-01`
```

「（reload 在前）」是权威定义未声明的顺序断言——D-01 定义只写 `close:false + submitSucc 手动 closeDialog`，未规定 reload 与 closeDialog 的先后；它是 §1 示例的惯例顺序，非硬约束。建议删括注：

```
- [ ] 提交按钮 `close: false` + `submitSucc` 内手动 `closeDialog`？→ `D-01`
```

**S2 — self-check.md L48**

```
- [ ] 联想下拉已提示后端直接返回 `label`/`value`（协作约束，前端不可独立完成）？→ `F-09`
```

「已提示后端」是过程动作，自检时无法从配置/代码判断，可判断性弱于「后端是否返回」。建议改为以事实为检查点：

```
- [ ] 联想下拉后端响应是否返回标准 `label`/`value` 字段（协作约束，前端不可独立完成，否则用降级方案）？→ `F-09`
```

---

两处均为建议级，不阻塞落地。
