# 技术栈决策

> 本文锁定 THA 年度赛事积分系统 MVP 阶段的技术选型，解决上游文档中的待确认项。
>
> 选型原则：服务 MVP 快速落地，与业务复杂度匹配，不为"先进"而过度复杂。

---

## 1. 前端技术栈

### 1.1 用户端

| 技术 | 版本 | 选型原因 |
|---|---|---|
| Vue 3 | 3.4+ | 生态成熟，团队熟悉 |
| TypeScript | 5.x | 类型安全，减少运行时错误 |
| Vite | 5.x | 构建快，开发体验好 |
| Pinia | 2.x | Vue 3 官方推荐状态管理 |
| Axios | 1.x | HTTP 请求，拦截器机制成熟 |

**MVP 阶段用户端只做 H5 Web 版本，不做微信小程序。**

原因：
- MVP 目标是验证核心闭环，H5 可通过微信内置浏览器分享。
- Uni-app 引入额外构建复杂度，与 MVP 快速落地目标冲突。
- 小程序版本作为 V2 规划，届时可基于 H5 版本迁移或用 Uni-app 重写用户端。

用户端不使用 UI 组件库，排行榜页面结构简单，自行实现即可。

### 1.2 管理端

| 技术 | 版本 | 选型原因 |
|---|---|---|
| Vue 3 | 3.4+ | 与用户端统一框架 |
| TypeScript | 5.x | 类型安全 |
| Vite | 5.x | 构建快 |
| Element Plus | 2.x | 后台 UI 组件齐全，表格/表单/弹窗开箱即用 |
| Vue Router | 4.x | SPA 路由管理 |
| Pinia | 2.x | 状态管理 |
| Axios | 1.x | HTTP 请求 |

### 1.3 前端工具链

| 工具 | 选型 | 说明 |
|---|---|---|
| 包管理器 | pnpm | 磁盘效率高，monorepo 友好，锁文件确定性好 |
| 代码格式化 | Prettier | 统一代码风格 |
| 代码检查 | ESLint | 静态质量检查 |
| Node.js | 20 LTS | 当前长期支持版本 |

### 1.4 前端不引入的技术

| 技术 | 原因 |
|---|---|
| Uni-app | MVP 不做小程序，避免构建复杂度 |
| Wot Design Uni | 不使用 Uni-app 则不需要 |
| Tailwind CSS | 管理端用 Element Plus 足够，用户端页面少不需要 |
| Nuxt / SSR | 排行榜不需要 SEO，纯 SPA 足够 |
| 前端单测框架 | MVP 阶段不做前端单测，优先保证后端测试覆盖 |

---

## 2. 后端技术栈

### 2.1 核心框架

| 技术 | 版本 | 选型原因 |
|---|---|---|
| Python | 3.11 | 稳定，FastAPI/SQLAlchemy/Pydantic 兼容性好 |
| FastAPI | 0.110+ | 异步支持、自动文档、Pydantic 原生集成 |
| Pydantic | 2.x | 高性能数据校验，V2 性能大幅提升 |
| SQLAlchemy | 2.0 | 异步 ORM，声明式模型，成熟稳定 |
| Alembic | 1.13+ | 数据库迁移标准工具 |
| Uvicorn | 0.27+ | ASGI 服务器，FastAPI 标配 |

### 2.2 数据与基础服务

| 技术 | 版本 | 选型原因 |
|---|---|---|
| PostgreSQL | 16 | 窗口函数、事务、JSON 支持，适合积分排名计算 |
| Redis | 7.x | 异步任务队列、简单缓存 |
| asyncpg | 0.29+ | PostgreSQL 异步驱动，配合 SQLAlchemy async |
| ARQ | 0.26+ | 轻量异步任务队列，基于 Redis，适合 FastAPI 生态 |

### 2.3 业务处理

| 技术 | 用途 | 选型原因 |
|---|---|---|
| openpyxl | Excel 解析 | 纯 Python，无系统依赖，支持 .xlsx |
| python-jose | JWT 签发/校验 | 轻量，FastAPI 文档推荐 |
| passlib + bcrypt | 密码哈希 | 安全标准实践 |
| python-multipart | 文件上传 | FastAPI 文件上传依赖 |

### 2.4 开发与测试

| 技术 | 用途 |
|---|---|
| pytest | 测试框架 |
| httpx | 异步测试客户端（测试 FastAPI） |
| pytest-asyncio | 异步测试支持 |
| ruff | 代码格式化 + lint（替代 black + flake8，更快） |

### 2.5 依赖管理

| 选型 | 说明 |
|---|---|
| uv | Python 包管理器，速度极快，兼容 pip 生态，支持 lockfile |

选择 uv 而非 Poetry 的原因：
- 安装速度快 10-100 倍。
- 兼容 pyproject.toml 标准。
- 支持 lockfile（uv.lock）确保可复现。
- 社区活跃，已成为主流趋势。

### 2.6 后端不引入的技术

| 技术 | 原因 |
|---|---|
| Celery | ARQ 更轻量，MVP 任务量小，不需要 Celery 的复杂度 |
| pandas | Excel 解析用 openpyxl 足够，pandas 太重 |
| AI/LLM SDK | MVP 不接入 AI |
| SQLModel | 与 SQLAlchemy 2.0 功能重叠，增加学习成本 |
| Dramatiq | ARQ 已满足需求 |

---

## 3. 数据库与存储方案

### 3.1 数据库

| 选型 | 说明 |
|---|---|
| PostgreSQL 16 | 核心业务数据库 |
| 本地开发 | Docker 容器运行 |
| 生产部署 | 云数据库或自建 Docker |

适合 MVP 的原因：
- 积分排名依赖窗口函数（RANK、SUM、GROUP BY），PostgreSQL 原生支持。
- 事务一致性保障关键操作原子性。
- 数据量预估 < 10000 条记录，单机 PostgreSQL 绑绑有余。

### 3.2 缓存

| 选型 | 说明 |
|---|---|
| Redis 7 | 任务队列（ARQ）+ 简单缓存 |
| 本地开发 | Docker 容器运行 |

MVP 阶段 Redis 主要用于 ARQ 任务队列，缓存为可选。

### 3.3 文件存储

| 选型 | 说明 |
|---|---|
| 本地磁盘 | MVP 阶段 Excel 文件存本地目录 |
| 路径配置 | 通过环境变量 UPLOAD_DIR 指定 |

MVP 不接入云存储（OSS/COS），本地磁盘足够。V2 再迁移到云存储。

---

## 4. 前端工程目录组织

### 4.1 整体结构

```text
frontend/
├─ user/                    # 用户端（公共积分榜）
│  ├─ src/
│  │  ├─ App.vue
│  │  ├─ main.ts
│  │  ├─ pages/
│  │  │  └─ ranking/
│  │  │     └─ index.vue
│  │  ├─ components/
│  │  │  ├─ RankingHeader.vue
│  │  │  ├─ RankingFilter.vue
│  │  │  ├─ RankingTable.vue
│  │  │  ├─ RankingCardList.vue
│  │  │  ├─ PlayerPointsDialog.vue
│  │  │  └─ EmptyState.vue
│  │  ├─ services/
│  │  │  ├─ request.ts
│  │  │  └─ ranking.ts
│  │  ├─ stores/
│  │  │  └─ app.ts
│  │  ├─ types/
│  │  │  └─ index.ts
│  │  └─ styles/
│  │     └─ main.css
│  ├─ index.html
│  ├─ vite.config.ts
│  ├─ tsconfig.json
│  ├─ package.json
│  └─ .env.example
├─ admin/                   # 管理端（Web 后台）
│  ├─ src/
│  │  ├─ App.vue
│  │  ├─ main.ts
│  │  ├─ layouts/
│  │  │  └─ AdminLayout.vue
│  │  ├─ views/
│  │  │  ├─ Login.vue
│  │  │  ├─ Dashboard.vue
│  │  │  ├─ Seasons.vue
│  │  │  ├─ Players.vue
│  │  │  ├─ Tournaments.vue
│  │  │  ├─ PointsRules.vue
│  │  │  ├─ Uploads.vue
│  │  │  └─ Rankings.vue
│  │  ├─ components/
│  │  │  ├─ DataTable.vue
│  │  │  ├─ FormDialog.vue
│  │  │  ├─ StatusTag.vue
│  │  │  ├─ StepBar.vue
│  │  │  ├─ ImportPreviewTable.vue
│  │  │  ├─ PlayerPointsDialog.vue
│  │  │  ├─ StatCard.vue
│  │  │  └─ ConfirmAction.vue
│  │  ├─ router/
│  │  │  └─ index.ts
│  │  ├─ services/
│  │  │  ├─ request.ts
│  │  │  ├─ auth.ts
│  │  │  ├─ seasons.ts
│  │  │  ├─ players.ts
│  │  │  ├─ tournaments.ts
│  │  │  ├─ pointsRules.ts
│  │  │  ├─ uploads.ts
│  │  │  └─ rankings.ts
│  │  ├─ stores/
│  │  │  ├─ auth.ts
│  │  │  └─ app.ts
│  │  ├─ types/
│  │  │  └─ index.ts
│  │  └─ styles/
│  │     └─ main.css
│  ├─ index.html
│  ├─ vite.config.ts
│  ├─ tsconfig.json
│  ├─ package.json
│  └─ .env.example
└─ pnpm-workspace.yaml      # pnpm workspace 配置（可选）
```

### 4.2 说明

- 用户端和管理端是两个独立 Vite 项目，各自有 package.json。
- 可选使用 pnpm workspace 管理，共享 TypeScript 类型定义。
- 每个前端项目独立构建、独立部署。
- services/ 目录封装所有 API 调用，一个文件对应一个后端资源。
- components/ 目录放可复用组件，views/ 放页面级组件。

---

## 5. 后端工程目录组织

```text
backend/
├─ app/
│  ├─ __init__.py
│  ├─ main.py                   # FastAPI 应用入口
│  ├─ api/
│  │  ├─ __init__.py
│  │  ├─ deps.py                # 依赖注入（DB session、当前用户）
│  │  └─ v1/
│  │     ├─ __init__.py
│  │     ├─ router.py           # 路由汇总
│  │     ├─ public/
│  │     │  ├─ __init__.py
│  │     │  ├─ rankings.py
│  │     │  └─ seasons.py
│  │     └─ admin/
│  │        ├─ __init__.py
│  │        ├─ auth.py
│  │        ├─ seasons.py
│  │        ├─ players.py
│  │        ├─ tournaments.py
│  │        ├─ points_rules.py
│  │        ├─ uploads.py
│  │        └─ rankings.py
│  ├─ core/
│  │  ├─ __init__.py
│  │  ├─ config.py              # 环境变量读取（Pydantic Settings）
│  │  ├─ database.py            # 数据库连接池
│  │  ├─ redis.py               # Redis 连接
│  │  ├─ security.py            # JWT、密码哈希
│  │  └─ exceptions.py          # 业务异常定义
│  ├─ models/
│  │  ├─ __init__.py
│  │  ├─ season.py
│  │  ├─ player.py
│  │  ├─ tournament.py
│  │  ├─ event_result.py
│  │  ├─ entries_points.py
│  │  ├─ points_rule.py
│  │  ├─ upload.py
│  │  ├─ team.py
│  │  └─ user.py
│  ├─ schemas/
│  │  ├─ __init__.py
│  │  ├─ season.py
│  │  ├─ player.py
│  │  ├─ tournament.py
│  │  ├─ points_rule.py
│  │  ├─ upload.py
│  │  ├─ ranking.py
│  │  └─ auth.py
│  ├─ services/
│  │  ├─ __init__.py
│  │  ├─ auth.py
│  │  ├─ season.py
│  │  ├─ player.py
│  │  ├─ tournament.py
│  │  ├─ points_rule.py
│  │  ├─ upload.py
│  │  ├─ points.py
│  │  └─ ranking.py
│  ├─ processors/
│  │  ├─ __init__.py
│  │  ├─ excel_parse.py
│  │  ├─ data_validation.py
│  │  ├─ points_generation.py
│  │  └─ ranking_calculation.py
│  ├─ repositories/
│  │  ├─ __init__.py
│  │  ├─ season.py
│  │  ├─ player.py
│  │  ├─ tournament.py
│  │  ├─ event_result.py
│  │  ├─ entries_points.py
│  │  ├─ points_rule.py
│  │  ├─ upload.py
│  │  └─ ranking.py
│  └─ workers/
│     ├─ __init__.py
│     ├─ settings.py            # ARQ worker 配置
│     ├─ excel_parse.py
│     ├─ points_generation.py
│     └─ ranking_refresh.py
├─ alembic/
│  ├─ env.py
│  └─ versions/
├─ tests/
│  ├─ conftest.py
│  ├─ test_health.py
│  ├─ test_seasons.py
│  ├─ test_players.py
│  ├─ test_uploads.py
│  ├─ test_points_generation.py
│  └─ test_rankings.py
├─ alembic.ini
├─ pyproject.toml
├─ .env.example
└─ .python-version              # 锁定 Python 版本
```

---

## 6. 配置管理

### 6.1 环境变量读取方式

后端使用 Pydantic Settings 读取环境变量：

- 从 `.env` 文件自动加载（开发环境）。
- 从系统环境变量加载（生产环境）。
- 缺少必需变量时启动即失败，给出明确提示。

### 6.2 环境文件约定

| 文件 | 用途 | 是否提交仓库 |
|---|---|---|
| .env.example | 模板，列出所有变量名和占位值 | 是 |
| .env | 本地开发实际配置 | 否（.gitignore） |

### 6.3 .env.example 内容

```text
# 应用
APP_ENV=development
DEBUG=true

# 数据库
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/tha_tennis

# Redis
REDIS_URL=redis://localhost:6379/0

# 安全
SECRET_KEY=change-me-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440

# 文件上传
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE_MB=10

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:5174
```

### 6.4 前端环境变量

前端通过 Vite 的 `.env` 机制管理：

```text
# frontend/user/.env.example
VITE_API_BASE_URL=http://localhost:8000/api/v1

# frontend/admin/.env.example
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

---

## 7. 依赖管理原则

### 7.1 允许新增依赖的条件

新增依赖必须满足以下全部条件：

1. 当前阶段确实需要该能力（不是"未来可能用到"）。
2. 标准库或已有依赖无法合理实现。
3. 该包活跃维护，最近 6 个月有更新。
4. 该包无已知严重安全漏洞。
5. 引入后不显著增加构建时间或包体积。

### 7.2 禁止新增依赖的场景

- 为了一个工具函数引入整个库（自己写）。
- "以防万一"提前安装。
- 功能与已有依赖重叠。
- 包已停止维护超过 1 年。

### 7.3 依赖升级规则

- patch 版本：可直接升级。
- minor 版本：在分支验证后升级。
- major 版本：需评估 breaking changes，团队确认后升级。

---

## 8. 最小测试策略

### 8.1 后端测试（必须）

| 测试类型 | 覆盖范围 | 工具 |
|---|---|---|
| API 集成测试 | 每个接口的正常路径和主要错误路径 | pytest + httpx |
| 核心流程测试 | 积分生成、排行榜计算 | pytest |
| 数据校验测试 | Pydantic schema 边界值 | pytest |

测试数据库使用独立的测试库，每次测试前清空。

### 8.2 前端测试（MVP 不做）

MVP 阶段不写前端单测。通过以下方式保证质量：

- TypeScript 类型检查。
- ESLint 静态检查。
- 手动 smoke test（启动后主流程可走通）。

### 8.3 最小测试清单

MVP 上线前必须通过的测试：

- [ ] 健康检查接口返回正常
- [ ] 管理员登录成功/失败
- [ ] 赛季 CRUD 正常
- [ ] 选手 CRUD 正常
- [ ] 赛事 CRUD 正常
- [ ] 积分规则 CRUD 正常
- [ ] Excel 上传和解析正常
- [ ] 确认导入写入 event_results 正常
- [ ] 积分生成计算正确（单项、团体分摊）
- [ ] 排行榜查询返回正确排名
- [ ] 选手积分明细查询正常

---

## 9. 当前不做的工程化能力

| 能力 | 原因 |
|---|---|
| CI/CD 流水线 | MVP 手动部署，V2 再配置 |
| Docker 生产镜像 | MVP 先跑通本地，部署时再构建 |
| 前端单测 | 页面少，手动验证足够 |
| E2E 测试 | MVP 规模不需要 |
| 代码覆盖率报告 | 不追求覆盖率数字，追求核心路径覆盖 |
| 性能监控 | 数据量小，无性能瓶颈 |
| 日志聚合 | 单机部署，直接看文件日志 |
| API 版本管理（v2） | 只有 v1 |
| 微服务拆分 | 单体足够 |
| GraphQL | RESTful 满足需求 |
| 国际化 | 只有中文 |
