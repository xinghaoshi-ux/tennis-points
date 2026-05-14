# Frontend CLAUDE.md

## 职责边界

本目录承载 THA 年度赛事积分系统的全部前端实现，包括：

- 用户端（H5）：`frontend/user/` — 面向校友的排行榜展示
- 管理端（Web）：`frontend/admin/` — 面向管理员的后台管理系统

前端职责：
- 页面渲染、交互、状态管理
- API 调用和响应处理
- 表单校验（格式校验，非业务校验）
- 路由和导航
- 错误提示展示

前端不负责：
- 业务逻辑计算（积分计算、排名计算、选手匹配）
- 数据聚合（积分汇总、参赛次数统计）
- 状态流转控制（赛季/赛事/上传状态变更由后端决定）
- 业务文档编写

---

## 必须遵守的文档列表

实现前必须阅读并遵守以下文档，按优先级排列：

| 优先级 | 文档 | 用途 |
|---|---|---|
| 1 | `docs/08_api_spec/api_spec-v1.0.md` | API 契约，接口地址/参数/响应结构 |
| 2 | `docs/08_api_spec/error_code_spec.md` | 错误码处理和前端展示策略 |
| 3 | `docs/05_prd/prd-v1.0.md` | 功能范围和验收标准 |
| 4 | `docs/05_prd/mvp_feature_matrix.md` | 功能实现范围和优先级 |
| 5 | `docs/06_architecture/frontend_design_spec-v1.0.md` | 页面结构和组件设计 |
| 6 | `docs/04_interaction_design/flow_state_spec-v1.0.md` | 状态展示和流转 |
| 7 | `docs/04_interaction_design/exception_paths.md` | 异常路径处理 |
| 8 | `docs/06_architecture/frontend_backend_boundary_spec-v1.0.md` | 前后端职责边界 |
| 9 | `docs/08_api_spec/integration_sequence.md` | 联调顺序 |

---

## 页面实现范围

### 本期实现（MVP）

用户端：
- U-01：排行榜页（搜索、筛选、积分明细弹窗）

管理端：
- A-01：登录页
- A-02：赛季管理页
- A-03：选手管理页
- A-04：赛事管理页（含积分生成操作）
- A-05：积分规则管理页
- A-06：Excel 导入页
- A-07：排行榜管理页
- A-08：仪表盘页

### 本期不实现

- 微信小程序
- 选手个人主页
- 多赛季切换
- 数据导出页面
- 深色模式
- 国际化

---

## 路由和组件实现规则

### 用户端（frontend/user）

- 技术栈：Vue 3 + Vite + TypeScript + pnpm
- 不使用组件库，自行实现轻量组件
- 移动端优先，响应式适配
- 单页面应用，路由简单（仅排行榜页 + 积分明细弹窗）

### 管理端（frontend/admin）

- 技术栈：Vue 3 + Vite + TypeScript + pnpm + Element Plus
- 使用 Element Plus 组件库
- 桌面端优先，最小宽度 1280px
- 左侧导航栏 + 右侧内容区布局
- 路由结构：

```
/login                    → A-01 登录页
/dashboard                → A-08 仪表盘
/seasons                  → A-02 赛季管理
/players                  → A-03 选手管理
/tournaments              → A-04 赛事管理
/tournaments/:id          → A-04 赛事详情
/points-rules             → A-05 积分规则
/uploads                  → A-06 Excel 导入
/rankings                 → A-07 排行榜管理
```

### 组件规则

- 页面级组件放在 `views/` 或 `pages/` 目录
- 可复用组件放在 `components/` 目录
- API 调用封装在 `api/` 目录
- 类型定义放在 `types/` 目录
- 状态管理使用 Pinia（如需要）
- HTTP 客户端使用 axios，统一封装拦截器

---

## API 使用规则

### 基础约定

- Base URL：`/api/v1`
- 公共接口前缀：`/api/v1/public`
- 管理接口前缀：`/api/v1/admin`
- 开发环境通过 Vite proxy 代理到 `http://localhost:8000`

### 请求规则

- 管理端所有请求携带 `Authorization: Bearer {token}` 头
- 分页参数：`page`（默认 1）、`page_size`（默认 20）
- 搜索参数：`search`
- 筛选参数：按字段名传递（如 `department`、`status`）

### 响应处理

- 成功响应取 `data` 字段
- 列表响应额外取 `total`、`page`、`page_size`
- 错误响应读取 `detail` 和 `code` 字段

### 全局错误拦截

以下错误码由 HTTP 拦截器统一处理：
- `AUTH_TOKEN_MISSING` / `AUTH_TOKEN_EXPIRED` / `AUTH_TOKEN_INVALID` → 清除 Token，跳转登录页
- `SYSTEM_INTERNAL_ERROR` → 全局 Toast "系统异常"
- `RATE_LIMITED` → 全局 Toast "操作过于频繁"

### 业务错误处理

- `VALIDATION_ERROR` → 标红对应表单字段
- `*_STATUS_INVALID` → 刷新页面数据
- `*_DUPLICATE` / `CONFLICT` → 提示冲突原因

---

## 后端未实现能力标注规则

对于 MVP 功能矩阵中标注为"本期不实现"的功能：

| 处理方式 | 适用场景 | 实现方式 |
|---|---|---|
| 不展示入口 | 功能完全不可见 | 不写对应路由和组件 |
| 按钮置灰 + "即将上线" | 入口可见但不可操作 | 按钮 disabled + tooltip |
| 按钮不展示 | 操作入口不可见 | 不渲染对应按钮 |

具体标注项：
- "下载 Excel 模板"按钮：置灰，标注"即将上线"
- "导出排行榜"按钮：置灰，标注"即将上线"
- 其他未实现功能：不展示入口

---

## 禁止事项

1. **禁止伪造后端能力**：不得用本地 mock 数据冒充正式后端响应。开发阶段如需 mock，必须明确标注为开发临时方案，且不得合入主分支。
2. **禁止本地计算替代后端**：积分计算、排名计算、选手匹配等必须调用后端接口，不得前端自行实现。
3. **禁止自行假定接口结构**：所有接口调用必须严格按照 `api_spec-v1.0.md` 定义的请求参数和响应结构。
4. **禁止越权实现**：不得实现 MVP 功能矩阵中标注为"本期不实现"的功能。
5. **禁止硬编码业务数据**：院系列表、赛事级别等枚举值从后端获取或从文档定义的枚举中引用，不得硬编码。

---

## 本地启动命令

### 用户端

```bash
cd frontend/user
pnpm install
pnpm dev          # http://localhost:5173
```

### 管理端

```bash
cd frontend/admin
pnpm install
pnpm dev          # http://localhost:5174
```

### 代码检查

```bash
pnpm lint
pnpm build        # 构建验证
```

---

## 当前优先主链路

按联调顺序，前端开发优先级：

1. **管理端登录**（A-01）→ 验证认证机制
2. **赛季管理**（A-02）→ 基础 CRUD 模式建立
3. **选手管理**（A-03）→ 搜索筛选模式建立
4. **赛事管理**（A-04）→ 状态约束 UI 模式
5. **积分规则**（A-05）→ CRUD + 删除约束
6. **Excel 导入**（A-06）→ 异步流程 UI 模式
7. **排行榜**（A-07 + U-01）→ 数据展示
8. **仪表盘**（A-08）→ 补全

每完成一个页面，必须与后端联调验证后再进入下一个。
