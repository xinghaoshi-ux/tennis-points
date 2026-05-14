# THA 年度赛事积分系统

本项目用于建设网球赛事积分、排行榜、赛事管理与相关运营流程的平台化系统。

当前阶段仅进行项目初始化和规范搭建，不包含任何前端或后端业务实现。

## 项目目标

- 建立清晰的项目目录结构
- 建立统一的项目级规则
- 建立文档驱动的协作方式
- 为后续研究、设计、开发、联调与发布提供稳定基础

## 目录结构

```text
project-root/
├─ frontend/
├─ backend/
├─ docs/
│  ├─ 00_setup/
│  ├─ 01_business_research/
│  ├─ 02_competitive_analysis/
│  ├─ 03_problem_modeling/
│  ├─ 04_interaction_design/
│  ├─ 05_prd/
│  ├─ 06_architecture/
│  ├─ 07_data_model/
│  ├─ 08_api_spec/
│  ├─ 09_frontend_plan/
│  ├─ 10_ui_design/
│  ├─ 11_integration/
│  └─ 12_release_deployment/
├─ CLAUDE.md
└─ README.md
```

## 职责边界

### `frontend/`

承载所有前端实现，包括用户端、管理端、页面交互、状态管理、API 调用和构建配置。

### `backend/`

承载所有后端实现，包括 API、业务逻辑、数据访问、鉴权、集成与测试。

### `docs/`

承载项目的研究、设计、规范、计划和交付文档，是实现的上游依据。

## 文档阅读顺序

建议按以下顺序阅读：

1. `docs/00_setup/environment_setup.md`
2. `docs/00_setup/tooling_checklist.md`
3. `docs/00_setup/dependency_strategy.md`
4. `docs/00_setup/project_structure.md`
5. `docs/00_setup/project_rules.md`
6. `docs/01_business_research/`
7. `docs/02_competitive_analysis/`
8. `docs/03_problem_modeling/`
9. `docs/04_interaction_design/`
10. `docs/05_prd/`
11. `docs/06_architecture/`
12. `docs/07_data_model/`
13. `docs/08_api_spec/`
14. `docs/09_frontend_plan/`
15. `docs/10_ui_design/`
16. `docs/11_integration/`
17. `docs/12_release_deployment/`

## 当前阶段

当前阶段为：项目初始化与规范搭建。

本阶段已完成：

- 基础环境配置文档
- 工具检查清单
- 依赖策略
- 项目结构说明
- 项目级规则
- 根目录行为约束文件
- 项目说明入口文档

## 开始开发前的原则

- 复杂任务先输出计划，待确认后再执行
- 先文档后代码
- 每个阶段必须有明确输出物
- 收口文档禁止擅自发散
- 前端不得伪造后端真实能力
- 后端不得擅自改变 API 契约
- 主链路优先，MVP 优先

## 说明

如需推进下一阶段，请先在对应 `docs/` 子目录中补齐上游文档，再开始代码实现。