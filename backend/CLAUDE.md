# Backend CLAUDE.md

## 职责边界

本目录承载 THA 年度赛事积分系统的全部后端实现，包括：

- API 层：接收请求、参数校验、响应序列化
- Service 层：业务逻辑、状态流转、规则执行
- Processor 层：复杂业务处理（Excel 解析、积分生成）
- Repository 层：数据访问、查询构建

后端职责：
- 实现 API 契约定义的所有接口
- 业务逻辑计算（积分计算、排名计算、选手匹配）
- 数据持久化和查询
- 状态流转控制
- 认证和鉴权
- 异步任务处理（Excel 解析、积分生成、排行榜刷新）
- 数据校验（业务规则校验）

后端不负责：
- 页面渲染和前端交互
- 业务文档编写
- 前端构建和部署

---

## 必须遵守的文档列表

实现前必须阅读并遵守以下文档，按优先级排列：

| 优先级 | 文档 | 用途 |
|---|---|---|
| 1 | `docs/08_api_spec/api_spec-v1.0.md` | API 契约，接口实现的唯一标准 |
| 2 | `docs/08_api_spec/error_code_spec.md` | 错误码定义和 HTTP 状态码映射 |
| 3 | `docs/07_data_model/data_model_spec-v1.0.md` | 数据模型和字段定义 |
| 4 | `docs/07_data_model/entity_relationships.md` | 实体关系和索引设计 |
| 5 | `docs/07_data_model/field_dictionary.md` | 字段字典和枚举值 |
| 6 | `docs/06_architecture/backend_architecture_spec-v1.0.md` | 四层架构设计 |
| 7 | `docs/06_architecture/service_boundary_spec.md` | 服务边界和业务规则 |
| 8 | `docs/06_architecture/workflow_architecture.md` | 异步工作流设计 |
| 9 | `docs/06_architecture/engineering_conventions.md` | 工程规范 |
| 10 | `docs/04_interaction_design/flow_state_spec-v1.0.md` | 状态流转定义 |

---

## API 契约来源

**所有接口实现必须严格遵循 `docs/08_api_spec/api_spec-v1.0.md`。**

具体约束：
- 路径、方法、参数名必须与文档一致
- 响应结构必须与文档一致（字段名、嵌套层级、类型）
- 错误响应必须使用 `docs/08_api_spec/error_code_spec.md` 定义的错误码
- 如需变更契约，必须先更新文档，再修改实现

通用响应结构：

```python
# 成功（单对象）
{"data": {...}, "message": "ok"}

# 成功（列表）
{"data": [...], "total": 100, "page": 1, "page_size": 20}

# 错误
{"detail": "错误描述", "code": "ERROR_CODE"}
```

---

## 数据模型约束

### 技术栈

- ORM：SQLAlchemy 2.0（声明式映射）
- 迁移：Alembic
- 数据库：PostgreSQL 16

### 模型实现规则

- 表名使用复数蛇形命名（如 `seasons`、`entries_points`、`event_result_players`）
- 主键统一使用 `id: Integer, primary_key, autoincrement`
- 时间字段使用 `TIMESTAMP WITH TIME ZONE`
- 外键必须声明且命名（如 `fk_tournament_season_id`）
- 枚举值使用 VARCHAR 存储，不使用数据库 ENUM 类型
- 索引按 `docs/07_data_model/entity_relationships.md` 第 4 节建议创建

### 枚举值约束

所有枚举值必须与 `docs/07_data_model/field_dictionary.md` 第 13 节一致：

- Season.status: draft, active, closed
- Tournament.status: draft, completed, published
- Upload.status: pending, parsing, parsed, parse_failed, imported, cancelled
- Player.status: active, inactive
- event_category: individual_doubles, team, representative, bonus
- level: THA1000, THA800, THA500, THA200, THA_S, THA_A, THA_B, representative, bonus
- result_type: champion, runner_up, semifinal, quarterfinal, participant
- source_type: individual_event, team_share, travel_bonus, representative_team, organizer_bonus, donation_bonus
- rule_type: individual_event, team_event, travel_bonus, representative_team, organizer_bonus, donation_bonus
- gender: male, female

---

## 状态流转约束

状态变更必须由 Service 层控制，遵循以下规则：

### Season

```
draft → active（激活）
active → closed（关闭，或被新赛季激活时自动关闭）
```

- 同一时间最多一个 active 赛季
- closed 赛季不可回退

### Tournament

```
draft → completed（确认导入赛事结果）
completed → published（积分生成完成）
published → completed（撤回发布）
```

- 仅 draft 状态可编辑
- 仅 completed 状态可生成积分
- 撤回发布时删除关联积分记录

### Upload

```
pending → parsing（开始解析）
parsing → parsed（解析成功）
parsing → parse_failed（解析失败）
parsed → imported（确认导入）
parsed → cancelled（取消）
pending → cancelled（取消）
```

---

## 服务分层要求

### 四层架构

```
API Layer (Routers)
    ↓
Service Layer
    ↓
Processor Layer（复杂业务）
    ↓
Repository Layer
```

### 各层职责

| 层 | 职责 | 禁止事项 |
|---|---|---|
| API (Router) | 参数校验（Pydantic）、调用 Service、序列化响应 | 不含业务逻辑 |
| Service | 业务规则、状态流转、事务协调 | 不直接操作数据库 |
| Processor | 复杂计算（积分生成、Excel 解析） | 不处理 HTTP 请求/响应 |
| Repository | SQL 查询、数据读写 | 不含业务判断 |

### 模块划分

```
app/
├── routers/          # API 层
│   ├── auth.py
│   ├── seasons.py
│   ├── players.py
│   ├── tournaments.py
│   ├── points_rules.py
│   ├── uploads.py
│   ├── rankings.py
│   └── public.py
├── services/         # Service 层
├── processors/       # Processor 层
├── repositories/     # Repository 层
├── models/           # SQLAlchemy 模型
├── schemas/          # Pydantic 模型
├── workers/          # ARQ 异步任务
├── core/             # 配置、安全、依赖注入
└── main.py           # FastAPI 应用入口
```

---

## 环境变量管理规则

### .env 文件

- `.env.example` 提交到版本控制，包含所有变量名和示例值
- `.env` 不提交到版本控制（已在 .gitignore）
- 本地开发使用 `.env`，生产环境使用系统环境变量

### 必需环境变量

```bash
# 数据库
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/tha_tennis

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=24

# 文件上传
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=10485760  # 10MB

# 应用
APP_ENV=development
DEBUG=true
```

### 配置读取

- 使用 Pydantic Settings 管理配置
- 所有配置通过依赖注入获取，不直接读取 os.environ
- 敏感信息（密码、密钥）不得出现在日志中

---

## 本地启动和测试命令

### 安装依赖

```bash
cd backend
uv sync
```

### 配置环境

```bash
cp .env.example .env
# 编辑 .env 确认数据库和 Redis 连接信息
```

### 数据库迁移

```bash
uv run alembic upgrade head
```

### 启动 API 服务

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 启动异步 Worker

```bash
uv run arq app.workers.settings.WorkerSettings
```

### 运行测试

```bash
uv run pytest                          # 全部测试
uv run pytest tests/test_xxx.py        # 指定文件
uv run pytest -v                       # 详细输出
uv run pytest --cov=app                # 覆盖率
```

### 代码检查

```bash
uv run ruff check .
uv run ruff format .
```

### 创建迁移

```bash
uv run alembic revision --autogenerate -m "描述"
```

### 种子数据

```bash
uv run python -m app.scripts.seed
```

---

## 禁止事项

1. **禁止偏离 API 契约**：不得在未更新 `docs/08_api_spec/api_spec-v1.0.md` 的情况下增删字段、修改语义、变更错误码或改变响应结构。
2. **禁止跳过状态校验**：所有状态变更必须校验当前状态是否允许目标转换。
3. **禁止在 Router 层写业务逻辑**：Router 只做参数校验和调用 Service。
4. **禁止在 Repository 层做业务判断**：Repository 只负责数据读写。
5. **禁止硬编码配置**：数据库连接、密钥等必须通过环境变量配置。
6. **禁止返回内部字段**：`phone`、`password_hash`、`file_path` 等标记为"内部"的字段不得出现在 API 响应中。
7. **禁止忽略外键约束**：所有外键关系必须在模型中声明。
8. **禁止跳过数据完整性校验**：唯一性约束（规则组合唯一、赛季唯一激活等）必须在 Service 层校验。

---

## 当前优先主链路

按联调顺序，后端开发优先级：

1. **健康检查 + 认证**：GET /health、POST /admin/auth/login、GET /admin/auth/me
2. **赛季 CRUD + 激活**：GET/POST /admin/seasons、PUT /admin/seasons/{id}、POST /admin/seasons/{id}/activate
3. **选手 CRUD**：GET/POST /admin/players、GET/PUT /admin/players/{id}
4. **赛事 CRUD**：GET/POST /admin/tournaments、GET/PUT /admin/tournaments/{id}
5. **积分规则 CRUD**：GET/POST/PUT/DELETE /admin/points-rules
6. **Excel 上传 + 解析 + 预览 + 确认**：POST /admin/uploads、GET /admin/uploads/{id}、GET /admin/uploads/{id}/preview、POST /admin/uploads/{id}/confirm
7. **积分生成**：POST /admin/tournaments/{id}/generate-points
8. **排行榜**：GET /public/rankings、GET /public/players/{id}/points、POST /admin/rankings/refresh
9. **补全**：GET /admin/dashboard、POST /admin/seasons/{id}/close、POST /admin/uploads/{id}/cancel、POST /admin/tournaments/{id}/revoke-publish

每个接口实现后必须通过 curl 或 pytest 验证，再通知前端联调。
