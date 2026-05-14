# 工程规范

> 本文定义 THA 年度赛事积分系统的工程化约定，包括代码组织、命名、提交、分支和协作规范。
>
> 规范服务于 MVP 快速落地，不追求完美，追求一致。

---

## 1. 代码组织规范

### 1.1 后端文件命名

| 类型 | 命名方式 | 示例 |
|---|---|---|
| Python 模块 | snake_case | `points_generation.py` |
| 类名 | PascalCase | `PointsGenerationProcessor` |
| 函数/方法 | snake_case | `generate_points()` |
| 常量 | UPPER_SNAKE_CASE | `MAX_UPLOAD_SIZE` |
| 数据库表名 | snake_case 复数 | `entries_points` |
| 数据库字段 | snake_case | `player_id` |

### 1.2 前端文件命名

| 类型 | 命名方式 | 示例 |
|---|---|---|
| Vue 组件文件 | PascalCase | `RankingTable.vue` |
| TypeScript 模块 | camelCase | `pointsRules.ts` |
| 类型定义文件 | camelCase | `index.ts`（在 types/ 下） |
| CSS 文件 | kebab-case | `main.css` |
| 目录名 | kebab-case 或 camelCase | `services/`、`stores/` |

### 1.3 API 路径命名

| 规则 | 示例 |
|---|---|
| 资源用复数名词 | `/players`、`/tournaments` |
| 路径用 kebab-case | `/points-rules`、`/generate-points` |
| 版本前缀 | `/api/v1/` |
| 公共接口前缀 | `/api/v1/public/` |
| 管理接口前缀 | `/api/v1/admin/` |

---

## 2. Git 规范

### 2.1 分支策略

MVP 阶段采用简单分支模型：

| 分支 | 用途 |
|---|---|
| main | 稳定版本，可部署 |
| dev | 开发主线，功能合入点 |
| feature/xxx | 功能分支，完成后合入 dev |
| fix/xxx | 修复分支 |

### 2.2 提交信息格式

```text
<type>: <简短描述>

可选正文
```

type 取值：

| type | 说明 |
|---|---|
| feat | 新功能 |
| fix | 修复 |
| docs | 文档 |
| refactor | 重构 |
| test | 测试 |
| chore | 工程配置 |

示例：

```text
feat: 实现排行榜查询接口
fix: 修复团体赛积分分摊四舍五入问题
docs: 补充 API 契约文档
```

### 2.3 .gitignore 要点

```text
# 环境变量
.env
.env.local

# Python
__pycache__/
*.pyc
.venv/

# Node
node_modules/
dist/

# IDE
.idea/
.vscode/
*.swp

# 上传文件
uploads/

# 系统文件
.DS_Store
```

---

## 3. 代码质量工具

### 3.1 后端

| 工具 | 用途 | 运行时机 |
|---|---|---|
| ruff | 格式化 + lint | 保存时 / 提交前 |
| mypy | 类型检查（可选） | CI 或手动 |
| pytest | 测试 | 提交前 / CI |

ruff 配置（pyproject.toml）：

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I"]
```

### 3.2 前端

| 工具 | 用途 | 运行时机 |
|---|---|---|
| ESLint | 代码检查 | 保存时 |
| Prettier | 格式化 | 保存时 |
| TypeScript | 类型检查 | 构建时 |

---

## 4. API 设计规范

### 4.1 请求格式

- Content-Type: `application/json`（常规请求）
- Content-Type: `multipart/form-data`（文件上传）
- 认证: `Authorization: Bearer <token>`

### 4.2 响应格式

成功响应：

```json
{
  "data": { ... },
  "message": "ok"
}
```

列表响应：

```json
{
  "data": [ ... ],
  "total": 100,
  "page": 1,
  "page_size": 20
}
```

错误响应：

```json
{
  "detail": "错误描述",
  "code": "ERROR_CODE"
}
```

### 4.3 HTTP 状态码使用

| 状态码 | 场景 |
|---|---|
| 200 | 查询成功、更新成功 |
| 201 | 创建成功 |
| 202 | 异步任务已接受 |
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 409 | 业务冲突（状态不允许） |
| 422 | 数据校验失败 |
| 500 | 服务器内部错误 |

---

## 5. 数据库规范

### 5.1 表设计约定

- 每张表必须有 `id` 主键（UUID 或自增整数，MVP 用自增整数）。
- 每张表必须有 `created_at` 字段。
- 需要追踪修改的表加 `updated_at` 字段。
- 外键字段命名为 `{关联表单数}_id`，如 `season_id`、`player_id`。
- 状态字段统一命名为 `status`，类型为 VARCHAR。

### 5.2 迁移规范

- 每次数据库结构变更必须通过 Alembic 迁移。
- 迁移文件必须有描述性消息。
- 不允许手动修改生产数据库结构。
- 迁移必须可回滚（提供 downgrade）。

---

## 6. 错误处理规范

### 6.1 后端异常层级

```text
AppException（基类）
├─ AuthenticationError      → 401
├─ PermissionError          → 403
├─ NotFoundError            → 404
├─ BusinessConflictError    → 409
├─ ValidationError          → 422
└─ InternalError            → 500
```

### 6.2 异常处理原则

- Service 层抛出业务异常。
- API 层通过全局异常处理器捕获并转换为 HTTP 响应。
- Repository 层的数据库异常由 Service 层捕获并转换为业务异常。
- Worker 中的异常捕获后更新对象状态，不向上抛出。

---

## 7. 日志规范

### 7.1 日志级别

| 级别 | 使用场景 |
|---|---|
| ERROR | 需要关注的错误（任务失败、数据库异常） |
| WARNING | 异常但可恢复的情况（重试、降级） |
| INFO | 关键业务事件（导入完成、积分生成完成） |
| DEBUG | 开发调试信息（仅开发环境启用） |

### 7.2 日志内容

- 包含时间戳、级别、模块名。
- 业务日志包含关键 ID（upload_id、tournament_id）。
- 不记录敏感信息（密码、Token 全文）。

---

## 8. 安全规范

### 8.1 认证

- 管理端使用 JWT Bearer Token。
- Token 有效期 24 小时。
- 用户端公共接口无需认证。

### 8.2 密码

- 使用 bcrypt 哈希存储。
- 不记录明文密码。
- 登录失败不透露具体原因（统一提示"用户名或密码错误"）。

### 8.3 输入校验

- 所有输入通过 Pydantic 校验。
- SQL 通过 SQLAlchemy 参数化查询，防止注入。
- 文件上传校验类型和大小。

---

## 9. 协作约定

### 9.1 代码审查

MVP 阶段如为单人开发，自行 review 后合入。多人开发时：

- feature 分支合入 dev 需要 review。
- dev 合入 main 需要确认测试通过。

### 9.2 文档同步

- API 变更必须同步更新 `docs/08_api_spec/`。
- 数据模型变更必须同步更新 `docs/07_data_model/`。
- 架构变更必须同步更新 `docs/06_architecture/`。
