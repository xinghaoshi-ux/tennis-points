# 本地开发命令

> 本文列出 THA 年度赛事积分系统本地开发所需的全部命令。
>
> 按照以下顺序执行即可完成本地环境搭建。

---

## 1. 前置条件

确认以下工具已安装：

| 工具 | 版本要求 | 验证命令 |
|---|---|---|
| Node.js | 20.x LTS | `node --version` |
| pnpm | 9.x | `pnpm --version` |
| Python | 3.11.x | `python3 --version` |
| uv | 最新 | `uv --version` |
| Docker | 最新 | `docker --version` |
| Docker Compose | v2 | `docker compose version` |
| Git | 最新 | `git --version` |

---

## 2. 启动基础服务

### 2.1 启动 PostgreSQL 和 Redis

```bash
# 在项目根目录
docker compose up -d
```

docker-compose.yml 提供 PostgreSQL 和 Redis 容器。

### 2.2 验证服务连接

```bash
# 验证 PostgreSQL
docker compose exec postgres pg_isready

# 验证 Redis
docker compose exec redis redis-cli ping
```

---

## 3. 后端

### 3.1 安装依赖

```bash
cd backend

# 创建虚拟环境并安装依赖
uv sync
```

### 3.2 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env，确认数据库和 Redis 连接信息
```

### 3.3 数据库迁移

```bash
# 执行迁移
uv run alembic upgrade head
```

### 3.4 启动后端服务

```bash
# 开发模式启动（自动重载）
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3.5 启动异步 Worker

```bash
# 另开终端
uv run arq app.workers.settings.WorkerSettings
```

### 3.6 运行测试

```bash
# 运行全部测试
uv run pytest

# 运行指定测试文件
uv run pytest tests/test_rankings.py

# 显示详细输出
uv run pytest -v
```

### 3.7 代码检查

```bash
# 格式化 + lint
uv run ruff check .
uv run ruff format .
```

### 3.8 创建数据库迁移

```bash
# 生成迁移文件
uv run alembic revision --autogenerate -m "描述"
```

---

## 4. 前端（用户端）

### 4.1 安装依赖

```bash
cd frontend/user
pnpm install
```

### 4.2 启动开发服务

```bash
pnpm dev
```

默认地址：http://localhost:5173

### 4.3 构建

```bash
pnpm build
```

### 4.4 代码检查

```bash
pnpm lint
```

---

## 5. 前端（管理端）

### 5.1 安装依赖

```bash
cd frontend/admin
pnpm install
```

### 5.2 启动开发服务

```bash
pnpm dev
```

默认地址：http://localhost:5174

### 5.3 构建

```bash
pnpm build
```

### 5.4 代码检查

```bash
pnpm lint
```

---

## 6. 全部服务一键启动（开发模式）

建议使用多终端或 tmux：

| 终端 | 命令 | 说明 |
|---|---|---|
| 终端 1 | `docker compose up -d` | 基础服务 |
| 终端 2 | `cd backend && uv run uvicorn app.main:app --reload --port 8000` | 后端 API |
| 终端 3 | `cd backend && uv run arq app.workers.settings.WorkerSettings` | 异步 Worker |
| 终端 4 | `cd frontend/user && pnpm dev` | 用户端 |
| 终端 5 | `cd frontend/admin && pnpm dev` | 管理端 |

---

## 7. 常用端口

| 服务 | 端口 |
|---|---|
| 后端 API | 8000 |
| 用户端 | 5173 |
| 管理端 | 5174 |
| PostgreSQL | 5432 |
| Redis | 6379 |

---

## 8. 数据库管理

### 8.1 创建种子数据

```bash
# 创建管理员账号和初始赛季（脚本待实现）
uv run python -m app.scripts.seed
```

### 8.2 重置数据库

```bash
# 删除并重建数据库
docker compose exec postgres dropdb -U postgres tha_tennis
docker compose exec postgres createdb -U postgres tha_tennis
uv run alembic upgrade head
```

---

## 9. 验证清单

环境搭建完成后，逐项验证：

```bash
# 1. 后端健康检查
curl http://localhost:8000/api/v1/health

# 2. 用户端可访问
# 浏览器打开 http://localhost:5173

# 3. 管理端可访问
# 浏览器打开 http://localhost:5174

# 4. 后端测试通过
cd backend && uv run pytest
```

---

## 10. 常见问题

### 10.1 端口被占用

```bash
# 查找占用端口的进程
lsof -i :8000
# 终止进程
kill -9 <PID>
```

### 10.2 数据库连接失败

- 确认 Docker 容器正在运行：`docker compose ps`
- 确认 .env 中的 DATABASE_URL 正确
- 确认 PostgreSQL 容器健康：`docker compose logs postgres`

### 10.3 pnpm install 失败

- 确认 Node.js 版本为 20.x：`node --version`
- 清除缓存重试：`pnpm store prune && pnpm install`

### 10.4 uv sync 失败

- 确认 Python 版本为 3.11.x：`python3 --version`
- 确认 uv 已安装：`uv --version`
