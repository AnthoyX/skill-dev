# CHANGELOG

## 1.2.0（2026-08-31）

SSOT 重构，四批次完成（评审文档见 `docs/`，基准 `docs/plan-iteration.md` §5.2）：

- 批次 1（5d3d67c + ee1a027）：规则 ID 体系冻结——32 条权威规则 = R-01 + C-01~C-08 + D-01~D-11 + F-01~F-10 + A-01~A-02，每条带「来源|状态|版本|违反后果」四要素
- 批次 2（ded35a5）：`pitfalls.md` 重编号 P-01~P-16 纯引用化（症状 + 错误写法 + ID 指向）；`SKILL.md` 索引化（59 行）
- 批次 3（135d383）：`crud-full.json` 拆 4 片段 + `examples/INDEX.md`（宿主依赖 / 覆盖规则 ID / 行数）
- 批次 4（a137700）：新增 `references/self-check.md`（6 组 33 项正向自检清单，覆盖 32 条规则，`C-02` 跨组复检，只引规则 ID）；`META.md` 参考文档计数更新；`SKILL.md` 触发矩阵补 self-check 入口
- 终检全部 PASS：权威形态唯一性（32 条各出现 1 次）/ 编号连续无跳号 / 悬空引用 = 0 / 全文 CRLF

## 1.1.0（2026-08-31）

止血修正（commit 7d1dea8；实测 V-1 / V-1-D / V-2 / V-3，详见迭代计划 §5.1）：

- 删除弹层提交 `loadingOn` 死配置（submit 按钮有内建 loading，实测三组对照均转圈）；导出 / download 按钮的 `loadingOn` 保留（实测等待下载完成，有效）
- 统一 `api.reload` 说法：`close: false` 下不生效且提交不默认刷新 CRUD，唯一写法是 `submitSucc` 显式 `componentId` reload（V-2 实测）
- 新增 `META.md`：amis 版本锚定（6.13.0）+ 适用边界 + 规则可信度分级
- `adaptor` 拼写统一为官方标准名；`data-source.md` 示例去 `//` 注释；修正 reload `target` 作用域（仅事件动作内失效）；删除不存在的 `columnsToggled`
- frontmatter 补 `amis-version` / `allowed-tools`

## 1.0.0

首发：SKILL.md + 5 references + 3 examples（957 行）。
