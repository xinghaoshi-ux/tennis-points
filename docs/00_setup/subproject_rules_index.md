# 子项目规则索引

> 本文说明 THA 年度赛事积分系统中 Claude Code 上下文规则文件的层级关系、适用范围和更新时机。

---

## 1. 规则文件清单

| 文件路径 | 适用范围 | 角色 |
|---|---|---|
| `/CLAUDE.md` | 项目根目录 | 全局规则，约束所有子目录行为 |
| `/frontend/CLAUDE.md` | frontend/ 目录 | 前端实现规则 |
| `/backend/CLAUDE.md` | backend/ 目录 | 后端实现规则 |

---

## 2. 层级关系

```text
/CLAUDE.md（全局）
├── /frontend/CLAUDE.md（前端子项目）
└── /backend/CLAUDE.md（后端子项目）
```

### 继承规则

- 子项目规则继承根目录规则，不得与根目录规则冲突
- 根目录规则定义全局原则（先文档后代码、API 契约优先、禁止伪造等）
- 子项目规则在全局原则基础上，补充该子项目的具体约束

### 优先级

当规则存在歧义时：
1. 根目录 `/CLAUDE.md` 的禁止事项优先级最高
2. 子项目 `CLAUDE.md` 的具体实现规则次之
3. `docs/` 中的规范文档作为实现依据

---

## 3. 各目录规则适用说明

### 在根目录工作时

Claude Code 遵守：
- `/CLAUDE.md` 全局规则
- 项目目录职责边界
- 执行原则（先计划再执行、先文档后代码、API 契约优先）
- 阶段输出要求
- 所有禁止事项

典型场景：编写文档、跨模块协调、项目级配置（docker-compose.yml 等）

### 在 frontend/ 目录工作时

Claude Code 遵守：
- `/CLAUDE.md` 全局规则（继承）
- `/frontend/CLAUDE.md` 前端规则（补充）

具体约束：
- 页面实现范围限定在 MVP 功能矩阵
- API 调用严格按照 api_spec-v1.0.md
- 不得伪造后端能力
- 不得本地计算替代后端
- 未实现功能按规则标注
- 使用指定技术栈（Vue 3 + Vite + TypeScript + pnpm）
- 管理端使用 Element Plus
- 用户端不使用组件库

### 在 backend/ 目录工作时

Claude Code 遵守：
- `/CLAUDE.md` 全局规则（继承）
- `/backend/CLAUDE.md` 后端规则（补充）

具体约束：
- 接口实现严格遵循 api_spec-v1.0.md
- 数据模型遵循 data_model_spec-v1.0.md
- 状态流转遵循 flow_state_spec-v1.0.md
- 四层架构分层（Router → Service → Processor → Repository）
- 错误码使用 error_code_spec.md 定义
- 环境变量通过 .env 管理
- 使用指定技术栈（Python 3.11 + FastAPI + SQLAlchemy 2.0 + uv）

---

## 4. 规则更新时机

### 必须更新的场景

| 触发事件 | 需要更新的文件 | 原因 |
|---|---|---|
| API 契约变更 | backend/CLAUDE.md、frontend/CLAUDE.md | 接口依赖变化 |
| 新增功能模块 | 对应子项目 CLAUDE.md | 实现范围扩展 |
| 技术栈变更 | 对应子项目 CLAUDE.md | 工具和依赖变化 |
| 架构调整 | backend/CLAUDE.md | 分层或模块结构变化 |
| 项目阶段推进 | /CLAUDE.md | 当前阶段和目标变化 |
| 新增子项目 | /CLAUDE.md + 新子项目 CLAUDE.md | 职责边界变化 |

### 更新流程

1. 先更新 `docs/` 中的上游文档（如 API 规范、架构文档）
2. 再更新对应的 `CLAUDE.md` 规则文件
3. 确保子项目规则与根目录规则不冲突

### 不需要更新的场景

- 日常 bug 修复（不改变架构和契约）
- 代码重构（不改变外部行为）
- 测试补充
- 文档内容修正（不改变规则）

---

## 5. 规则冲突处理

如果发现子项目规则与根目录规则或上游文档存在冲突：

1. 以根目录 `/CLAUDE.md` 的禁止事项为最高优先级
2. 以 `docs/08_api_spec/api_spec-v1.0.md` 为接口实现标准
3. 以 `docs/07_data_model/data_model_spec-v1.0.md` 为数据模型标准
4. 发现冲突时，先暂停实现，标记冲突点，等待确认后再继续

---

## 6. 检查清单

进入实现阶段前，确认以下事项：

- [ ] 根目录 `/CLAUDE.md` 已更新"当前阶段"为实现阶段
- [ ] `frontend/CLAUDE.md` 页面实现范围与 MVP 功能矩阵一致
- [ ] `backend/CLAUDE.md` API 契约来源指向最新版本
- [ ] 所有禁止事项在三个文件中保持一致
- [ ] 技术栈选择与 `docs/06_architecture/tech_stack_decision.md` 一致
