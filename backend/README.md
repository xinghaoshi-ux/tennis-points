# THA Tennis Points Platform — Backend

## 技术栈

- Python 3.11 + FastAPI + Pydantic v2
- SQLAlchemy 2.0 (async) + Alembic
- PostgreSQL 16 + Redis 7
- ARQ (异步任务)
- JWT 认证 (HS256)

## 快速开始

### 1. 安装依赖

```bash
cd backend
uv sync
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，确认数据库和 Redis 连接信息
```

### 3. 启动基础服务

```bash
# 项目根目录
docker compose up -d
```

### 4. 数据库迁移

```bash
uv run alembic upgrade head
```

### 5. 初始化种子数据

```bash
uv run python -m app.scripts.seed
```

创建管理员账号：`admin` / `admin123`，以及一个初始活跃赛季。

### 6. 启动 API 服务

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API 文档：http://localhost:8000/docs

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| DATABASE_URL | PostgreSQL 连接串 | postgresql+asyncpg://postgres:postgres@localhost:5432/tha_tennis |
| TEST_DATABASE_URL | 测试数据库连接串 | postgresql+asyncpg://postgres:postgres@localhost:5432/tha_tennis_test |
| REDIS_URL | Redis 连接串 | redis://localhost:6379/0 |
| JWT_SECRET_KEY | JWT 签名密钥 | dev-secret-key-change-in-production |
| JWT_ALGORITHM | JWT 算法 | HS256 |
| JWT_EXPIRE_HOURS | Token 过期时间（小时） | 24 |
| UPLOAD_DIR | 文件上传目录 | ./uploads |
| MAX_UPLOAD_SIZE | 最大上传大小（字节） | 10485760 |
| APP_ENV | 运行环境 | development |
| DEBUG | 调试模式 | true |

## 测试

```bash
# 运行全部测试
uv run pytest -v

# 运行单个文件
uv run pytest tests/test_auth.py -v

# 带覆盖率
uv run pytest --cov=app
```

测试默认使用 SQLite（无需 PostgreSQL），配置在 `tests/conftest.py`。

## 代码检查

```bash
uv run ruff check .
uv run ruff format .
```

## 项目结构

```
app/
├── core/           # 配置、安全、依赖注入、异常
├── models/         # SQLAlchemy 模型
├── schemas/        # Pydantic 请求/响应模型
├── repositories/   # 数据访问层
├── services/       # 业务逻辑层
├── processors/     # 复杂业务处理（Excel、积分）
├── routers/        # API 路由
├── workers/        # ARQ 异步任务
├── scripts/        # 脚本（种子数据等）
└── main.py         # 应用入口
```
