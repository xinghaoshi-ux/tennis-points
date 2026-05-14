# 后端实现计划

> 本文定义 THA 年度赛事积分系统后端 MVP 的实现计划。
>
> 基于已确认的架构设计、数据模型和 API 规范，指导后端从零开始的完整实现。

---

## 1. 实现概述

后端当前状态：`backend/` 目录仅有 `CLAUDE.md`，无任何代码。需要从项目脚手架开始，逐步实现全部 P0/P1 接口。

实现策略：按 6 个阶段推进，每阶段产出可运行、可测试的代码。

---

## 2. 模块拆分

```
backend/
├── pyproject.toml              # 项目配置和依赖
├── alembic.ini                 # 数据库迁移配置
├── .env.example                # 环境变量模板
├── .gitignore
├── alembic/
│   ├── env.py                  # 异步迁移环境
│   └── versions/               # 迁移文件
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 应用入口
│   ├── core/                   # 基础设施
│   │   ├── config.py           # Pydantic Settings 配置
│   │   ├── database.py         # 异步 SQLAlchemy 引擎和会话
│   │   ├── redis.py            # Redis 连接
│   │   ├── security.py         # JWT + 密码哈希
│   │   ├── exceptions.py       # 异常层级 + 全局处理器
│   │   └── deps.py             # 依赖注入
│   ├── models/                 # SQLAlchemy ORM 模型
│   │   ├── season.py
│   │   ├── player.py
│   │   ├── tournament.py
│   │   ├── event_result.py
│   │   ├── event_result_player.py
│   │   ├── entries_points.py
│   │   ├── points_rule.py
│   │   ├── team.py
│   │   ├── team_member.py
│   │   ├── upload.py
│   │   └── user.py
│   ├── schemas/                # Pydantic 请求/响应模型
│   │   ├── common.py           # 分页、通用响应
│   │   ├── auth.py
│   │   ├── season.py
│   │   ├── player.py
│   │   ├── tournament.py
│   │   ├── points_rule.py
│   │   ├── upload.py
│   │   ├── ranking.py
│   │   └── dashboard.py
│   ├── repositories/           # 数据访问层
│   │   ├── season_repo.py
│   │   ├── player_repo.py
│   │   ├── tournament_repo.py
│   │   ├── points_rule_repo.py
│   │   ├── upload_repo.py
│   │   ├── event_result_repo.py
│   │   ├── entries_points_repo.py
│   │   └── ranking_repo.py
│   ├── services/               # 业务逻辑层
│   │   ├── auth_service.py
│   │   ├── season_service.py
│   │   ├── player_service.py
│   │   ├── tournament_service.py
│   │   ├── points_rule_service.py
│   │   ├── upload_service.py
│   │   ├── points_service.py
│   │   └── ranking_service.py
│   ├── processors/             # 复杂业务处理
│   │   ├── excel_parser.py     # Excel 解析
│   │   └── points_generator.py # 积分生成计算
│   ├── routers/                # API 路由层
│   │   ├── health.py
│   │   ├── auth.py
│   │   ├── seasons.py
│   │   ├── players.py
│   │   ├── tournaments.py
│   │   ├── points_rules.py
│   │   ├── uploads.py
│   │   ├── rankings.py
│   │   ├── public.py
│   │   └── dashboard.py
│   ├── workers/                # ARQ 异步任务
│   │   ├── __init__.py
│   │   ├── settings.py         # ARQ Worker 配置
│   │   └── tasks.py            # 任务定义
│   └── scripts/
│       └── seed.py             # 种子数据脚本
└── tests/
    ├── conftest.py             # 测试配置和 fixtures
    ├── test_health.py
    ├── test_auth.py
    ├── test_seasons.py
    ├── test_players.py
    ├── test_tournaments.py
    ├── test_points_rules.py
    ├── test_uploads.py
    └── test_rankings.py
```

---

## 3. 文件结构说明

### 3.1 core/ — 基础设施

| 文件 | 职责 |
|---|---|
| config.py | 从 .env 读取配置，Pydantic Settings 类 |
| database.py | create_async_engine, async_sessionmaker, get_db 生成器 |
| redis.py | aioredis 连接池，get_redis 依赖 |
| security.py | create_access_token, verify_token, hash_password, verify_password |
| exceptions.py | AppException 基类 + 子类（NotFoundError, BusinessConflictError 等）+ FastAPI exception_handler |
| deps.py | get_db, get_current_user 依赖注入函数 |

### 3.2 models/ — ORM 模型

每个文件对应一个数据库表，字段严格遵循 `docs/07_data_model/data_model_spec-v1.0.md`。使用 SQLAlchemy 2.0 声明式映射（Mapped, mapped_column）。

### 3.3 schemas/ — Pydantic 模型

每个文件包含对应实体的 Create/Update/Response schema，字段和类型严格遵循 API 规范。

### 3.4 repositories/ — 数据访问

每个 Repository 提供：list（分页+筛选）、get_by_id、create、update、delete 等基础方法。不含业务逻辑。

### 3.5 services/ — 业务逻辑

每个 Service 封装对应领域的业务规则、状态校验、事务控制。Service 之间不互相调用。

### 3.6 processors/ — 复杂处理

- excel_parser.py：读取 .xlsx、提取行数据、匹配选手、生成预览
- points_generator.py：匹配规则、计算各类积分、批量写入

### 3.7 workers/ — 异步任务

ARQ Worker 定义，包含：parse_excel_task、generate_points_task。

---

## 4. API 实现顺序

严格按照 `docs/08_api_spec/integration_sequence.md` 的联调阶段：

### 阶段 1：基础通路

| 序号 | 接口 | 方法 |
|---|---|---|
| 1 | /api/v1/health | GET |
| 2 | /api/v1/admin/auth/login | POST |
| 3 | /api/v1/admin/auth/me | GET |

### 阶段 2：数据管理 CRUD

| 序号 | 接口 | 方法 |
|---|---|---|
| 4 | /api/v1/admin/seasons | GET, POST |
| 5 | /api/v1/admin/seasons/{id} | PUT |
| 6 | /api/v1/admin/seasons/{id}/activate | POST |
| 7 | /api/v1/admin/seasons/{id}/close | POST |
| 8 | /api/v1/admin/players | GET, POST |
| 9 | /api/v1/admin/players/{id} | GET, PUT |
| 10 | /api/v1/admin/tournaments | GET, POST |
| 11 | /api/v1/admin/tournaments/{id} | GET, PUT |
| 12 | /api/v1/admin/points-rules | GET, POST |
| 13 | /api/v1/admin/points-rules/{id} | PUT, DELETE |

### 阶段 3：核心异步流程

| 序号 | 接口 | 方法 |
|---|---|---|
| 14 | /api/v1/admin/uploads | POST |
| 15 | /api/v1/admin/uploads/{id} | GET |
| 16 | /api/v1/admin/uploads/{id}/preview | GET |
| 17 | /api/v1/admin/uploads/{id}/confirm | POST |
| 18 | /api/v1/admin/uploads/{id}/cancel | POST |
| 19 | /api/v1/admin/tournaments/{id}/generate-points | POST |

### 阶段 4：数据展示

| 序号 | 接口 | 方法 |
|---|---|---|
| 20 | /api/v1/public/seasons/current | GET |
| 21 | /api/v1/public/departments | GET |
| 22 | /api/v1/public/rankings | GET |
| 23 | /api/v1/public/players/{id}/points | GET |

### 阶段 5：补全

| 序号 | 接口 | 方法 |
|---|---|---|
| 24 | /api/v1/admin/rankings | GET |
| 25 | /api/v1/admin/rankings/refresh | POST |
| 26 | /api/v1/admin/tournaments/{id}/revoke-publish | POST |
| 27 | /api/v1/admin/dashboard | GET |

---

## 5. 数据模型实现方式

### 5.1 ORM 技术选择

- SQLAlchemy 2.0 声明式映射（`DeclarativeBase`, `Mapped`, `mapped_column`）
- 异步引擎：`create_async_engine` + `asyncpg`
- 会话：`async_sessionmaker` + `AsyncSession`

### 5.2 模型基类

```python
class Base(DeclarativeBase):
    pass

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=func.now())
```

### 5.3 迁移策略

- 使用 Alembic autogenerate 生成初始迁移
- 每次模型变更生成新迁移文件
- 迁移必须包含 upgrade 和 downgrade

### 5.4 索引

按 `docs/07_data_model/entity_relationships.md` 第 4 节创建：
- entries_points: (season_id, player_id), (tournament_id), (player_id, season_id)
- event_results: (tournament_id)
- event_result_players: (event_result_id), (player_id)
- tournaments: (season_id, status)
- players: (full_name), (department)
- team_members: (team_id, tournament_id)
- uploads: (tournament_id)

---

## 6. 服务层设计

### 6.1 AuthService

- login(username, password) → Token
- get_current_user(token) → User
- 密码验证使用 bcrypt
- Token 有效期 24 小时

### 6.2 SeasonService

- list_seasons(page, page_size) → 分页列表
- create_season(data) → Season（status=draft）
- update_season(id, data) → Season
- activate_season(id) → Season（原 active 变 closed）
- close_season(id) → Season
- get_active_season() → Season | None

### 6.3 PlayerService

- list_players(page, page_size, search, department) → 分页列表
- create_player(data) → Player（status=active）
- update_player(id, data) → Player
- get_player(id) → Player

### 6.4 TournamentService

- list_tournaments(page, page_size, status, season_id) → 分页列表
- create_tournament(data) → Tournament（自动取 active season_id）
- update_tournament(id, data) → Tournament（仅 draft 可编辑）
- get_tournament(id) → Tournament
- revoke_publish(id) → Tournament（published → completed，删除积分）

### 6.5 PointsRuleService

- list_rules(season_id, rule_type) → 列表
- create_rule(data) → PointsRule（自动取 active season_id）
- update_rule(id, data) → PointsRule
- delete_rule(id) → void（已引用不可删）

### 6.6 UploadService

- create_upload(file, tournament_id) → Upload（保存文件，派发解析任务）
- get_upload(id) → Upload
- get_preview(id) → preview_data
- confirm_import(id, confirmed_rows, ignored_rows) → 写入 EventResult
- cancel_upload(id) → Upload

### 6.7 PointsService

- generate_points(tournament_id) → 派发生成任务
- 生成逻辑：匹配规则 → 计算积分 → 批量写入 entries_points → 更新赛事状态

### 6.8 RankingService

- get_rankings(page, page_size, search, department) → 排行榜
- get_player_points(player_id) → 积分明细 + 分类汇总
- refresh() → 触发刷新（MVP 为实时查询，refresh 仅标记）

---

## 7. 测试方式

### 7.1 测试框架

- pytest + pytest-asyncio
- httpx.AsyncClient 作为测试客户端
- 独立测试数据库 `tha_tennis_test`

### 7.2 测试范围

| 模块 | 测试内容 |
|---|---|
| health | 健康检查返回 200 |
| auth | 登录成功/失败、Token 验证、过期处理 |
| seasons | CRUD、激活/关闭、状态约束 |
| players | CRUD、搜索、筛选 |
| tournaments | CRUD、状态约束、无 active 赛季时创建失败 |
| points_rules | CRUD、重复检测、引用检测 |
| uploads | 上传、状态查询、预览、确认、取消 |
| rankings | 排行榜查询、积分明细 |

### 7.3 测试策略

- 每个测试文件独立，使用 fixture 管理数据库状态
- 测试前清空数据库，测试后回滚事务
- 覆盖正常路径 + 关键异常路径

---

## 8. 当前不实现的能力

| 能力 | 原因 |
|---|---|
| 物化视图 | MVP 数据量小，动态查询足够 |
| 云文件存储 | 本地磁盘存储 |
| WebSocket 推送 | 前端轮询替代 |
| 审计日志 | 非 MVP 范围 |
| 批量选手导入 | 非 MVP 范围 |
| 数据导出 | 非 MVP 范围 |
| AI 选手匹配 | 精确匹配即可 |
| 多角色权限 | 单管理员角色 |
| 国际化 | 仅中文 |
| CI/CD | 手动部署 |

---

## 9. 依赖清单

```
# 核心
fastapi>=0.110.0,<1.0.0
uvicorn[standard]>=0.27.0,<1.0.0
pydantic>=2.0.0,<3.0.0
pydantic-settings>=2.0.0,<3.0.0

# 数据库
sqlalchemy>=2.0.0,<3.0.0
asyncpg>=0.29.0,<1.0.0
alembic>=1.13.0,<2.0.0

# Redis + 异步任务
redis>=5.0.0,<6.0.0
arq>=0.26.0,<1.0.0

# 安全
python-jose[cryptography]>=3.3.0,<4.0.0
passlib[bcrypt]>=1.7.4,<2.0.0

# 文件处理
python-multipart>=0.0.6,<1.0.0
openpyxl>=3.1.0,<4.0.0

# 测试
pytest>=8.0.0,<9.0.0
pytest-asyncio>=0.23.0,<1.0.0
httpx>=0.27.0,<1.0.0

# 代码质量
ruff>=0.3.0,<1.0.0
```

---

## 10. 环境变量

```bash
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/tha_tennis
TEST_DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/tha_tennis_test
REDIS_URL=redis://localhost:6379/0
JWT_SECRET_KEY=dev-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=24
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=10485760
APP_ENV=development
DEBUG=true
```

---

## 11. 验证步骤

实现完成后执行：

1. `docker compose up -d` — 启动 PostgreSQL + Redis
2. `cd backend && uv sync` — 安装依赖
3. `cp .env.example .env` — 配置环境变量
4. `uv run alembic upgrade head` — 执行迁移
5. `uv run python -m app.scripts.seed` — 创建种子数据
6. `uv run uvicorn app.main:app --reload --port 8000` — 启动服务
7. `curl http://localhost:8000/api/v1/health` — 验证健康检查
8. `uv run pytest -v` — 运行测试
9. 测试结果写入 `docs/11_integration/backend_test_report.md`
