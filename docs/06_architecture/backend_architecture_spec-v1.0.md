# 后端架构规范 v1.0

> 本文定义 THA 年度赛事积分系统 MVP 阶段的后端架构设计，包括模块划分、分层边界、请求处理链路和异步策略。
>
> 本文档是数据模型设计和 API 规范设计的上游依据，不包含代码实现。

---

## 1. 技术选型

| 层次 | 技术 | 说明 |
|---|---|---|
| Web 框架 | FastAPI | 异步支持、自动文档、Pydantic 集成 |
| 数据校验 | Pydantic v2 | 请求/响应模型、业务数据校验 |
| ORM | SQLAlchemy 2.0 | 异步模式、声明式模型 |
| 数据库 | PostgreSQL | 关系查询、窗口函数、事务一致性 |
| 数据库迁移 | Alembic | 版本化迁移管理 |
| 任务队列 | Redis + ARQ | 轻量异步任务 |
| 缓存 | Redis | 排行榜缓存、会话管理 |
| 测试 | pytest + httpx | 单元测试、集成测试 |

---

## 2. 核心模块划分

```text
backend/
├─ app/
│  ├─ api/                  # API 层：路由、请求响应定义
│  │  ├─ v1/
│  │  │  ├─ public/         # 公共接口（无需认证）
│  │  │  └─ admin/          # 管理接口（需认证）
│  │  └─ deps.py            # 依赖注入（数据库会话、当前用户等）
│  ├─ schemas/              # Pydantic 模型：请求体、响应体、内部 DTO
│  ├─ services/             # Service 层：业务逻辑编排
│  ├─ processors/           # Processor 层：复杂业务流程处理
│  ├─ repositories/         # Data Access 层：数据库操作
│  ├─ models/               # SQLAlchemy 模型：数据库表定义
│  ├─ core/                 # 基础设施：配置、数据库连接、安全、日志
│  ├─ workers/              # 异步任务定义
│  └─ main.py              # 应用入口
├─ alembic/                 # 数据库迁移
├─ tests/                   # 测试
└─ pyproject.toml           # 项目配置
```

### 2.1 模块职责总览

| 模块 | 职责 | 不负责 |
|---|---|---|
| api | 路由注册、请求解析、响应序列化、权限校验 | 业务逻辑、数据库操作 |
| schemas | 定义请求/响应数据结构、字段校验规则 | 业务逻辑 |
| services | 业务逻辑编排、调用 repository、状态管理 | HTTP 细节、SQL 细节 |
| processors | 复杂多步骤业务流程（Excel 解析、积分生成） | 简单 CRUD |
| repositories | 数据库查询和写入、SQL 构建 | 业务逻辑、事务决策 |
| models | 数据库表结构定义、字段约束 | 查询逻辑 |
| core | 配置管理、数据库连接池、Redis 连接、认证工具 | 业务逻辑 |
| workers | 异步任务执行（Excel 解析、排行榜刷新） | HTTP 请求处理 |

---

## 3. 分层架构

### 3.1 四层结构

```text
┌─────────────────────────────────────────────┐
│              API 层 (api/)                    │
│  路由、请求校验、响应序列化、权限检查          │
├─────────────────────────────────────────────┤
│           Service 层 (services/)             │
│  业务逻辑编排、状态管理、事务控制             │
├─────────────────────────────────────────────┤
│        Processor 层 (processors/)            │
│  复杂流程处理：Excel 解析、积分计算           │
├─────────────────────────────────────────────┤
│       Data Access 层 (repositories/)         │
│  数据库读写、查询构建、分页                   │
└─────────────────────────────────────────────┘
```

### 3.2 层间调用规则

- API 层只调用 Service 层，不直接调用 Repository 或 Processor。
- Service 层可调用 Repository 层和 Processor 层。
- Processor 层可调用 Repository 层。
- Repository 层不调用上层任何模块。
- 同层模块之间不互相调用（避免循环依赖）。

### 3.3 各层详细边界

#### API 层

| 负责 | 不负责 |
|---|---|
| 定义路由和 HTTP 方法 | 业务判断和计算 |
| 解析请求参数和请求体 | 数据库操作 |
| 调用 Service 获取结果 | 状态迁移逻辑 |
| 序列化响应 | 异步任务编排 |
| 权限检查（通过依赖注入） | 文件读写 |
| HTTP 错误码映射 | 业务错误判断 |

#### Service 层

| 负责 | 不负责 |
|---|---|
| 业务逻辑编排 | HTTP 请求/响应细节 |
| 事务边界控制 | SQL 构建 |
| 状态迁移决策 | 文件解析细节 |
| 调用 Processor 处理复杂流程 | 路由注册 |
| 业务规则校验 | 数据库连接管理 |
| 异步任务派发 | 任务执行 |

#### Processor 层

| 负责 | 不负责 |
|---|---|
| Excel 文件解析和数据提取 | 事务控制 |
| 积分计算逻辑 | 状态迁移 |
| 排行榜计算逻辑 | HTTP 细节 |
| 数据校验和转换 | 路由定义 |
| 调用 Repository 读写数据 | 权限检查 |

#### Data Access 层

| 负责 | 不负责 |
|---|---|
| SQL 查询构建 | 业务逻辑 |
| 数据库读写操作 | 事务提交/回滚决策 |
| 分页和排序 | 状态迁移 |
| 关联查询 | 文件操作 |
| 窗口函数（排名计算） | 业务校验 |

---

## 4. 核心模块详细设计

### 4.1 Service 模块清单

| Service | 职责 |
|---|---|
| AuthService | 管理员登录、Token 签发、Token 校验 |
| SeasonService | 赛季 CRUD、赛季激活、赛季关闭 |
| PlayerService | 选手 CRUD、选手搜索、选手匹配 |
| TournamentService | 赛事 CRUD、赛事状态管理 |
| PointsRuleService | 积分规则 CRUD、规则查询 |
| UploadService | 上传记录管理、触发解析、确认导入 |
| PointsService | 积分生成触发、积分记录查询 |
| RankingService | 排行榜查询、排行榜刷新触发 |

### 4.2 Processor 模块清单

| Processor | 职责 |
|---|---|
| ExcelParseProcessor | 读取 Excel、识别表头、提取数据行、校验格式 |
| DataValidationProcessor | 校验选手匹配、成绩合法性、重复检测 |
| PointsGenerationProcessor | 根据规则计算积分（单项、团体分摊、奖补） |
| RankingCalculationProcessor | 聚合积分、计算排名、处理并列 |

### 4.3 Repository 模块清单

| Repository | 职责 |
|---|---|
| SeasonRepository | seasons 表读写 |
| PlayerRepository | players 表读写、模糊搜索 |
| TournamentRepository | tournaments 表读写 |
| PointsRuleRepository | points_rules 表读写、规则匹配查询 |
| UploadRepository | uploads 表读写 |
| EventResultRepository | event_results 表读写 |
| EntriesPointsRepository | entries_points 表读写、积分聚合查询 |
| RankingRepository | 排行榜查询（基于 entries_points 聚合） |

---

## 5. 请求处理链路

### 5.1 简单查询链路（排行榜查询）

```text
HTTP GET /api/v1/public/rankings
    ↓
API 层：解析查询参数（分页、搜索、筛选）
    ↓
Service 层：RankingService.get_rankings()
    ↓
Repository 层：RankingRepository.query_rankings()
    ↓
数据库：执行聚合查询 + 窗口函数排名
    ↓
返回：排行榜数据列表
```

### 5.2 简单写入链路（创建赛事）

```text
HTTP POST /api/v1/admin/tournaments
    ↓
API 层：权限校验、解析请求体
    ↓
Service 层：TournamentService.create()
    ├─ 校验赛季是否 active
    ├─ 校验赛事字段合法性
    └─ 调用 Repository 写入
    ↓
Repository 层：TournamentRepository.create()
    ↓
数据库：INSERT
    ↓
返回：赛事记录
```

### 5.3 复杂异步链路（Excel 导入）

```text
HTTP POST /api/v1/admin/uploads
    ↓
API 层：接收文件、权限校验
    ↓
Service 层：UploadService.create_upload()
    ├─ 保存文件到磁盘
    ├─ 创建 upload 记录（status: pending）
    └─ 派发异步任务
    ↓
返回：upload_id + status: pending
    ↓
[异步] Worker：excel_parse_task
    ├─ 更新 status: parsing
    ├─ ExcelParseProcessor.parse()
    ├─ DataValidationProcessor.validate()
    ├─ 生成预览数据
    └─ 更新 status: parsed 或 parse_failed
    ↓
[前端轮询] GET /api/v1/admin/uploads/{id}
    ↓
返回：当前状态 + 预览数据（如已解析）
```

### 5.4 积分生成链路

```text
HTTP POST /api/v1/admin/tournaments/{id}/generate-points
    ↓
API 层：权限校验
    ↓
Service 层：PointsService.generate()
    ├─ 校验赛事状态为 completed
    ├─ 校验积分规则存在
    └─ 派发异步任务
    ↓
返回：accepted（202）
    ↓
[异步] Worker：points_generation_task
    ├─ PointsGenerationProcessor.generate()
    │  ├─ 查询赛事结果
    │  ├─ 匹配积分规则
    │  ├─ 计算单项积分
    │  ├─ 计算团体分摊积分
    │  ├─ 计算远程奖补积分
    │  └─ 写入 entries_points
    ├─ 更新赛事状态：completed → published
    └─ 标记排行榜为 stale
```

---

## 6. 同步与异步划分

### 6.1 同步处理

| 操作 | 原因 |
|---|---|
| 排行榜查询 | 用户端核心体验，需即时响应 |
| 选手积分明细查询 | 弹窗展示，需即时响应 |
| 赛季/选手/赛事/规则 CRUD | 数据量小，操作简单 |
| 登录认证 | 需即时返回 Token |
| 文件上传（接收文件） | 文件保存后立即返回 |
| 确认导入（写入 event_results） | 数据量可控，事务内完成 |

### 6.2 异步处理

| 操作 | 原因 | 实现方式 |
|---|---|---|
| Excel 解析 | 文件可能较大，解析耗时 | ARQ 异步任务 |
| 积分生成 | 涉及多表写入和复杂计算 | ARQ 异步任务 |
| 排行榜刷新 | 聚合计算可能耗时 | ARQ 异步任务 |

### 6.3 异步任务状态查询

前端通过轮询获取异步任务状态：

```text
前端发起操作 → 后端返回任务 ID / 资源 ID → 前端每 3 秒轮询状态接口 → 直到终态
```

MVP 阶段不使用 WebSocket，轮询足够满足需求。

---

## 7. 状态管理职责

### 7.1 状态更新归属

| 业务对象 | 状态更新负责模块 | 说明 |
|---|---|---|
| Season | SeasonService | 激活/关闭由 Service 层控制 |
| Tournament | TournamentService + Worker | CRUD 由 Service 控制，published 由异步任务更新 |
| Upload | UploadService + Worker | 创建由 Service 控制，解析状态由异步任务更新 |
| Ranking | Worker | 刷新状态由异步任务控制 |

### 7.2 状态更新原则

- 状态迁移必须在事务内完成。
- 异步任务更新状态时，必须先检查当前状态是否允许迁移。
- 状态更新失败时，事务回滚，保持原状态。
- 不允许跳过中间状态直接到达终态。

---

## 8. 异常处理设计

### 8.1 异常分层

| 层次 | 异常类型 | 处理方式 |
|---|---|---|
| API 层 | 请求参数错误 | 返回 422 + 字段级错误信息 |
| Service 层 | 业务规则违反 | 抛出业务异常，API 层捕获后返回 409/400 |
| Processor 层 | 处理失败 | 抛出处理异常，Service/Worker 捕获后更新状态 |
| Repository 层 | 数据库错误 | 抛出数据异常，上层捕获后返回 500 |
| Worker | 任务执行失败 | 捕获异常，更新对象状态为失败态，记录错误日志 |

### 8.2 业务异常定义

| 异常 | 触发场景 | HTTP 状态码 |
|---|---|---|
| SeasonNotActiveError | 操作需要 active 赛季但当前无 | 409 |
| TournamentStateError | 赛事状态不允许当前操作 | 409 |
| UploadStateError | 上传状态不允许当前操作 | 409 |
| RuleNotFoundError | 积分生成时找不到匹配规则 | 422 |
| PlayerNotFoundError | 选手匹配失败 | 422 |
| DuplicateDataError | 重复导入检测 | 409 |
| AuthenticationError | 登录失败或 Token 无效 | 401 |

### 8.3 异步任务异常处理

```text
任务执行
    ├─ 成功 → 更新状态为成功态
    └─ 失败
        ├─ 可重试错误（网络超时等）→ ARQ 自动重试（最多 3 次）
        └─ 不可重试错误（数据错误等）→ 更新状态为失败态 + 记录错误日志
```

---

## 9. 事务设计

### 9.1 事务边界

事务由 Service 层控制，Repository 层不自行提交事务。

| 操作 | 事务范围 |
|---|---|
| 单表 CRUD | 单次数据库操作 |
| 确认导入 | Upload 状态更新 + event_results 批量写入 |
| 积分生成 | entries_points 批量写入 + Tournament 状态更新 |
| 赛季激活 | 原赛季关闭 + 新赛季激活 |
| 撤回发布 | entries_points 删除 + Tournament 状态回退 |

### 9.2 事务失败处理

- 事务内任何步骤失败，整体回滚。
- 回滚后业务对象保持操作前状态。
- 前端收到错误响应后可重试。

---

## 10. AI / LLM 模块边界（后置，MVP 不实现）

MVP 阶段不接入 AI 能力，但架构预留接入点。

### 10.1 三层边界

```text
┌─────────────────────────────────────────┐
│         人工确认层（管理员操作）           │
│  管理员审核 AI 解析结果，确认或修正        │
├─────────────────────────────────────────┤
│         业务编排层（Service/Processor）   │
│  组装 Prompt、调用模型、校验输出           │
├─────────────────────────────────────────┤
│         模型调用层（Integration）          │
│  HTTP 调用 LLM API、处理响应              │
└─────────────────────────────────────────┘
```

### 10.2 各层职责

| 层次 | 职责 | MVP 状态 |
|---|---|---|
| 模型调用层 | 封装 LLM API 调用（DeepSeek/OpenAI） | 不实现 |
| 业务编排层 | 组装 Prompt、解析 JSON 输出、Pydantic 校验 | 不实现 |
| 人工确认层 | 展示 AI 解析结果、管理员确认/修正 | 不实现 |

### 10.3 MVP 替代方案

MVP 阶段使用标准 Excel 模板 + openpyxl 解析 + Pydantic 校验，不依赖 AI。

AI 接入点预留在 ExcelParseProcessor 中：

```text
ExcelParseProcessor
├─ [MVP] 标准模板解析：openpyxl 读取 → Pydantic 校验
└─ [V3]  AI 辅助解析：LLM 识别字段 → Pydantic 校验 → 人工确认
```

---

## 11. MVP 架构能力清单

### 11.1 MVP 必须实现

| 能力 | 说明 |
|---|---|
| RESTful API | 公共接口 + 管理接口 |
| JWT 认证 | 管理端登录和接口保护 |
| 标准 CRUD | 赛季、选手、赛事、积分规则 |
| Excel 解析 | 标准模板解析（openpyxl） |
| 数据校验 | Pydantic 请求校验 + 业务规则校验 |
| 积分计算 | 单项、团体分摊、远程奖补、代表队、办赛、捐赠 |
| 排行榜计算 | 聚合积分、并列排名、姓名排序 |
| 异步任务 | Excel 解析、积分生成、排行榜刷新 |
| 事务管理 | 关键操作的原子性保障 |
| 错误处理 | 结构化错误响应 |
| 数据库迁移 | Alembic 版本管理 |

### 11.2 MVP 后置（V2+）

| 能力 | 归属版本 | 说明 |
|---|---|---|
| AI Excel 解析 | V3 | DeepSeek / LLM 辅助识别 |
| 物化视图 | V2 | 排行榜性能优化 |
| 排名快照 | V2 | 历史排名记录 |
| 审计日志 | V2 | 操作记录追踪 |
| 文件云存储 | V2 | OSS / COS 集成 |
| WebSocket | V2 | 实时状态推送替代轮询 |
| 批量导入优化 | V2 | 大文件分片处理 |
| 多租户 | 不规划 | 当前为单组织系统 |

---

## 12. 部署架构（MVP）

```text
┌──────────────┐     ┌──────────────┐
│  用户端 H5    │     │  管理端 Web   │
│  (Nginx)     │     │  (Nginx)     │
└──────┬───────┘     └──────┬───────┘
       │                     │
       └──────────┬──────────┘
                  ↓
       ┌──────────────────┐
       │   FastAPI 服务     │
       │   (Uvicorn)       │
       └────────┬─────────┘
                │
       ┌────────┼────────┐
       ↓        ↓        ↓
┌──────────┐ ┌──────┐ ┌──────────┐
│PostgreSQL│ │Redis │ │文件存储   │
│          │ │      │ │(本地磁盘) │
└──────────┘ └──────┘ └──────────┘
```

MVP 阶段单机部署，PostgreSQL 和 Redis 使用 Docker 容器。
