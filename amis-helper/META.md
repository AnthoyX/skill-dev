# amis-helper 元信息（META）

## 版本锚定

| 项 | 值 |
|---|---|
| 实测 amis 版本 | **6.13.0**（本 skill 全部规则的实测基准） |
| 适用版本范围 | amis 6.x |
| 不适用 | amis 2.x / 3.x 早期版本（行为可能不同，规则未验证）；amis-editor 可视化拖拽场景 |
| 验证环境 | 本地 amis 6.13.0 SDK（`_amis-lab/`），2026-08-31 |

## 适用边界

- **适用**：通过 JSON Schema 手写/生成 amis 页面配置（后台管理系统 CRUD 类页面）
- **不适用**：
  - amis-editor 可视化编辑器产出的配置（其 schema 带编辑器元数据，结构不同）
  - 移动端 H5（`amis-mobile` 渲染规则不同，未验证）
  - 服务端渲染 / SSR 场景

## 规则 ID 体系（v1.2 起）

| 前缀 | 域 | 权威定义位置 |
|---|---|---|
| `R-xx` | 跨域硬规则 | `META.md` |
| `C-xx` | CRUD / 列表 | `references/crud.md` |
| `D-xx` | 弹层 / 动作链 | `references/dialog-actions.md` |
| `F-xx` | 表单控件 | `references/form-controls.md` |
| `A-xx` | 接口 / 数据源 | `references/data-source.md` |
| `P-xx` | 排障条目（症状索引，不含正确写法） | `references/pitfalls.md` |

**SSOT 原则**：一条规则全文仅一处权威定义，其余位置只做 ID 引用。
每条权威规则带元数据四要素：`来源|状态|版本|违反后果`。

## 跨域硬规则

### `R-01` 生成的 JSON 配置内禁止注释

`来源:实战观察|状态:已实测|版本:全版本|后果:amis Schema 严格校验报错"JSON 中不允许有注释"`

说明写在配置外的文档里；配置内一律不放 `//` 或 `/* */`（含文档中的可复制示例）。

## 规则可信度分级

| 级别 | 含义 | 当前数量 |
|---|---|---|
| 已实测 | 在 amis 6.13.0 真实环境验证过行为 | D-01/D-02/D-04/D-05/D-08（V-1/V-1-D/V-2/V-3 系列）+ R-01 |
| 据官方文档 | 有官方文档或 issue 佐证，未单独实测 | C-01/C-06 等 |
| 实战观察 | 项目中踩坑总结，症状真实但机制未复现验证 | 其余多数条目 |

**未经实测的规则不得标注为「已实测」。** 新增规则默认「实战观察」，实测后升级。

## 规则数量（v1.2 重构后）

- 权威规则：30 条（R-01 + C×8 + D×10 + F×10 + A×2 …… 见各域文件）
- 排障条目：16 条（`references/pitfalls.md`，P-01～P-16）
- 参考文档：6 份（含 self-check.md）；示例：见 `examples/INDEX.md`

## 变更记录

见仓库 `CHANGELOG.md`（v1.2 起建立；v1.1 变更见 `docs/amis-helper-iteration-plan.md`）。
