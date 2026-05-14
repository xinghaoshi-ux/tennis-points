# 前后端联调计划

## 1. 联调目标

验证前端应用（admin + user）与后端 API 的完整通信链路，确保：
- 所有 API 请求/响应结构符合 `docs/08_api_spec/api_spec-v1.0.md` 契约
- 业务主链路（登录 → 数据管理 → Excel 导入 → 积分生成 → 排行榜展示）端到端可用
- 状态流转（赛季/赛事/上传）在前后端一致
- 错误处理和异常路径正确展示

---

## 2. 联调范围

### 已实现后端接口（34 个，全部覆盖）

| 模块 | 接口数 | 状态 |
|------|--------|------|
| 健康检查 | 1 | ✅ 已实现 |
| 认证 | 2 | ✅ 已实现 |
| 赛季管理 | 5 | ✅ 已实现 |
| 选手管理 | 4 | ✅ 已实现 |
| 赛事管理 | 6 | ✅ 已实现 |
| 积分规则 | 4 | ✅ 已实现 |
| Excel 导入 | 5 | ✅ 已实现 |
| 排行榜 | 3 | ✅ 已实现 |
| 仪表盘 | 1 | ✅ 已实现 |
| 公共接口 | 4 | ✅ 已实现 |

### 需要 Mock 的接口

**无。** 后端已完整实现 API 规范定义的全部 34 个接口，前端无需 Mock。

### 联调排除项

- P2 功能（按钮已置灰，无需联调）
- ARQ Worker 异步任务（MVP 中 Excel 解析为同步实现）
- 生产环境部署验证

---

## 3. 主链路联调顺序

```
阶段 1: 基础通路（健康检查 + 认证）
    │
    ├──→ 阶段 2: 数据管理
    │       ├── 2.1 赛季管理
    │       ├── 2.2 选手管理
    │       ├── 2.3 赛事管理（依赖 2.1）
    │       └── 2.4 积分规则（依赖 2.1）
    │
    ├──→ 阶段 3: 核心流程（依赖阶段 2 全部完成）
    │       ├── 3.1 Excel 上传与解析
    │       ├── 3.2 确认导入
    │       └── 3.3 积分生成
    │
    ├──→ 阶段 4: 数据展示（依赖阶段 3）
    │       ├── 4.1 公共排行榜
    │       └── 4.2 管理端排行榜 + 刷新
    │
    └──→ 阶段 5: 补全增强（依赖阶段 4）
            ├── 5.1 仪表盘
            ├── 5.2 赛季关闭
            ├── 5.3 上传取消
            └── 5.4 撤回发布
```

---

## 4. 各阶段详细联调步骤

### 阶段 1：基础通路

| 步骤 | API | 方法 | 前端页面/组件 | 后端路由 | 验收标准 |
|------|-----|------|--------------|----------|----------|
| 1.1 | /api/v1/health | GET | — (curl 验证) | routers/health.py | 返回 `{"status": "ok"}` |
| 1.2 | /api/v1/admin/auth/login | POST | admin/views/LoginView.vue | routers/auth.py | 正确凭证返回 Token；错误返回 401 |
| 1.3 | /api/v1/admin/auth/me | GET | admin/stores/auth.ts (fetchMe) | routers/auth.py | 携带 Token 返回用户信息 |

**前端验证点：**
- 登录页输入 admin/admin123 → 跳转 /dashboard
- localStorage 中存储 tha_admin_token
- 刷新页面后仍保持登录
- 清除 Token 后访问管理页 → 跳转 /login
- 输入错误密码 → 显示"登录失败"提示

---

### 阶段 2：数据管理

#### 2.1 赛季管理

| 步骤 | API | 方法 | 前端组件 | 后端路由 | 验收标准 |
|------|-----|------|----------|----------|----------|
| 2.1.1 | /admin/seasons | POST | SeasonsView.vue (handleSubmit) | routers/seasons.py | 创建赛季，返回 status=draft |
| 2.1.2 | /admin/seasons | GET | SeasonsView.vue (fetchData) | routers/seasons.py | 列表展示所有赛季 |
| 2.1.3 | /admin/seasons/{id} | PUT | SeasonsView.vue (handleSubmit) | routers/seasons.py | 编辑 draft 赛季成功 |
| 2.1.4 | /admin/seasons/{id}/activate | POST | SeasonsView.vue (handleActivate) | routers/seasons.py | 激活后 status=active |

**前端验证点：**
- 表格正确展示赛季列表
- 状态 Tag 颜色正确（draft=warning, active=success, closed=info）
- 激活确认弹窗正常
- 激活后原 active 赛季自动变为 closed

#### 2.2 选手管理

| 步骤 | API | 方法 | 前端组件 | 后端路由 | 验收标准 |
|------|-----|------|----------|----------|----------|
| 2.2.1 | /admin/players | POST | PlayersView.vue (handleSubmit) | routers/players.py | 创建选手成功 |
| 2.2.2 | /admin/players | GET | PlayersView.vue (fetchData) | routers/players.py | 列表分页正常 |
| 2.2.3 | /admin/players?search=X | GET | PlayersView.vue (debouncedSearch) | routers/players.py | 搜索结果正确 |
| 2.2.4 | /admin/players?department=X | GET | PlayersView.vue (fetchData) | routers/players.py | 院系筛选正确 |
| 2.2.5 | /admin/players/{id} | PUT | PlayersView.vue (handleSubmit) | routers/players.py | 编辑选手成功 |

**前端验证点：**
- 搜索输入 300ms 防抖生效
- 院系下拉从 /public/departments 获取
- 分页切换正常
- 创建/编辑弹窗表单校验

#### 2.3 赛事管理

| 步骤 | API | 方法 | 前端组件 | 后端路由 | 验收标准 |
|------|-----|------|----------|----------|----------|
| 2.3.1 | /admin/tournaments | POST | TournamentsView.vue (handleSubmit) | routers/tournaments.py | 创建赛事，自动关联 active 赛季 |
| 2.3.2 | /admin/tournaments | GET | TournamentsView.vue (fetchData) | routers/tournaments.py | 列表展示 |
| 2.3.3 | /admin/tournaments?status=X | GET | TournamentsView.vue (fetchData) | routers/tournaments.py | 状态筛选正确 |
| 2.3.4 | /admin/tournaments/{id} | PUT | TournamentsView.vue (handleSubmit) | routers/tournaments.py | 仅 draft 可编辑 |

**前端验证点：**
- 无 active 赛季时创建赛事 → 显示 409 错误提示
- draft 状态显示编辑按钮，非 draft 禁用
- completed 状态显示"生成积分"按钮
- published 状态显示"撤回发布"按钮

#### 2.4 积分规则

| 步骤 | API | 方法 | 前端组件 | 后端路由 | 验收标准 |
|------|-----|------|----------|----------|----------|
| 2.4.1 | /admin/points-rules | POST | PointsRulesView.vue (handleSubmit) | routers/points_rules.py | 创建规则成功 |
| 2.4.2 | /admin/points-rules?rule_type=X | GET | PointsRulesView.vue (fetchData) | routers/points_rules.py | 按类型筛选 |
| 2.4.3 | /admin/points-rules/{id} | PUT | PointsRulesView.vue (handleSubmit) | routers/points_rules.py | 编辑规则成功 |
| 2.4.4 | /admin/points-rules/{id} | DELETE | PointsRulesView.vue (handleDelete) | routers/points_rules.py | 删除成功 |

**前端验证点：**
- Tab 切换触发按类型筛选
- 重复规则组合创建 → 显示 409 RULE_DUPLICATE 错误
- 删除确认弹窗正常

---

### 阶段 3：核心流程

#### 3.1 Excel 上传与解析

| 步骤 | API | 方法 | 前端组件 | 后端路由 | 验收标准 |
|------|-----|------|----------|----------|----------|
| 3.1.1 | /admin/uploads | POST | UploadsView.vue (handleUpload) | routers/uploads.py | 上传文件，返回 upload_id |
| 3.1.2 | /admin/uploads/{id} | GET | UploadsView.vue (polling) | routers/uploads.py | 状态变化 pending→parsing→parsed |
| 3.1.3 | /admin/uploads/{id}/preview | GET | UploadsView.vue (step=3) | routers/uploads.py | 返回逐行预览数据 |

**前端验证点：**
- 步骤向导正确推进（选赛事→上传→解析中→预览）
- 轮询 3 秒间隔
- 预览表格展示行状态（normal/warning/error）
- 错误行标红并显示 error_message
- 非 .xlsx 文件前端拦截

#### 3.2 确认导入

| 步骤 | API | 方法 | 前端组件 | 后端路由 | 验收标准 |
|------|-----|------|----------|----------|----------|
| 3.2.1 | /admin/uploads/{id}/confirm | POST | UploadsView.vue (handleConfirm) | routers/uploads.py | 状态变为 imported |

**前端验证点：**
- 确认后步骤跳到"完成"
- 关联赛事状态变为 completed

#### 3.3 积分生成

| 步骤 | API | 方法 | 前端组件 | 后端路由 | 验收标准 |
|------|-----|------|----------|----------|----------|
| 3.3.1 | /admin/tournaments/{id}/generate-points | POST | TournamentsView.vue (handleGenerate) | routers/rankings.py | 返回成功，赛事状态变为 published |

**前端验证点：**
- 仅 completed 状态赛事显示"生成积分"按钮
- 点击后刷新列表，状态变为 published
- published 状态显示"撤回发布"按钮

---

### 阶段 4：数据展示

#### 4.1 公共排行榜

| 步骤 | API | 方法 | 前端组件 | 后端路由 | 验收标准 |
|------|-----|------|----------|----------|----------|
| 4.1.1 | /public/seasons/current | GET | user/views/RankingView.vue | routers/public.py | 返回当前 active 赛季 |
| 4.1.2 | /public/departments | GET | user/views/RankingView.vue | routers/public.py | 返回院系列表 |
| 4.1.3 | /public/rankings | GET | user/views/RankingView.vue | routers/public.py | 返回排行榜数据 |
| 4.1.4 | /public/players/{id}/points | GET | user/views/RankingView.vue (showDetail) | routers/public.py | 返回积分明细 |

**前端验证点：**
- 页面加载显示赛季名称
- 排行榜表格/卡片正确渲染
- 搜索 300ms 防抖
- 院系筛选下拉正常
- 点击选手弹出积分明细弹窗
- 积分分类汇总数据正确
- 移动端卡片布局 / 桌面端表格布局切换

#### 4.2 管理端排行榜

| 步骤 | API | 方法 | 前端组件 | 后端路由 | 验收标准 |
|------|-----|------|----------|----------|----------|
| 4.2.1 | /admin/rankings | GET | admin/views/RankingsView.vue | routers/rankings.py | 返回排行榜 |
| 4.2.2 | /admin/rankings/refresh | POST | admin/views/RankingsView.vue (handleRefresh) | routers/rankings.py | 刷新成功 |
| 4.2.3 | /public/players/{id}/points | GET | admin/views/RankingsView.vue (showPlayerDetail) | routers/public.py | 选手积分详情 |

**前端验证点：**
- 管理端排行榜与公共端数据一致
- 刷新按钮点击后数据更新
- "导出排行榜"按钮置灰 + "即将上线" tooltip

---

### 阶段 5：补全增强

| 步骤 | API | 方法 | 前端组件 | 后端路由 | 验收标准 |
|------|-----|------|----------|----------|----------|
| 5.1 | /admin/dashboard | GET | admin/views/DashboardView.vue | routers/dashboard.py | 返回统计数据 |
| 5.2 | /admin/seasons/{id}/close | POST | admin/views/SeasonsView.vue (handleClose) | routers/seasons.py | 赛季关闭成功 |
| 5.3 | /admin/uploads/{id}/cancel | POST | admin/views/UploadsView.vue (handleCancel) | routers/uploads.py | 上传取消成功 |
| 5.4 | /admin/tournaments/{id}/revoke-publish | POST | admin/views/TournamentsView.vue (handleRevoke) | routers/tournaments.py | 撤回后状态回退为 completed |

**前端验证点：**
- 仪表盘统计卡片数据正确
- 最近上传列表展示
- 撤回发布后排行榜数据更新
- 取消上传后步骤重置

---

## 5. 需要替换的 Mock API 清单

**无需替换。** 前端实现中未使用任何 Mock 数据或 Mock API。所有 API 调用直接指向后端真实接口，通过 Vite proxy 代理。

---

## 6. 后端接口未实现时的前端标注方式

当前后端已完整实现全部 34 个 API 接口，无需标注"未开发"。

如果未来出现后端接口未实现的情况，前端应按以下规则处理：

| 场景 | 处理方式 | 实现 |
|------|----------|------|
| 接口完全未实现 | 对应按钮/入口不展示 | 不渲染组件 |
| 接口部分实现（如缺少某个字段） | 正常调用，缺失字段显示"-" | 容错处理 |
| 接口返回 501 Not Implemented | 显示"功能开发中"提示 | catch 中判断 status |
| P2 功能接口未实现 | 按钮置灰 + "即将上线" tooltip | `<el-button disabled>` |

---

## 7. 风险点

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 后端测试使用 SQLite，联调需 PostgreSQL | 部分 SQL 行为差异（如 ILIKE、窗口函数） | 联调前确保 PostgreSQL 启动并完成迁移 |
| Excel 解析为同步实现 | 大文件可能超时 | MVP 限制文件大小 10MB，联调用小文件 |
| bcrypt 版本锁定 4.x | passlib 兼容性 | 已在 pyproject.toml 中锁定 |
| CORS 配置 | 前端跨域请求可能被拒 | 确认 main.py CORS 中间件配置正确 |
| Token 过期处理 | 24h 过期，联调期间可能遇到 | 前端拦截器已处理 401 跳转 |
| 前端 Vite proxy 路径 | 代理配置错误导致 404 | 已配置 `/api` → `http://localhost:8000` |
| 数据库无种子数据 | 联调时无 admin 用户 | 运行 `uv run python -m app.scripts.seed` |
| Docker 不可用 | 无法启动 PostgreSQL/Redis | 需要本地安装或使用远程数据库 |
| 排行榜窗口函数 | SQLite 不支持 RANK() | 联调必须使用 PostgreSQL |
| 前端 Element Plus 图标未注册 | 图标不显示 | 已通过 @element-plus/icons-vue 解决 |

---

## 8. 验收标准

### 阶段 1 验收
- [ ] `curl http://localhost:8000/api/v1/health` 返回 200
- [ ] 管理端登录页输入 admin/admin123 成功跳转 /dashboard
- [ ] 刷新页面保持登录状态
- [ ] 清除 localStorage 后访问管理页跳转 /login
- [ ] 错误密码显示错误提示

### 阶段 2 验收
- [ ] 创建赛季 → 列表中出现新赛季（status=draft）
- [ ] 激活赛季 → 状态变为 active，原 active 变 closed
- [ ] 创建选手 → 列表中出现，搜索可找到
- [ ] 院系筛选 → 结果正确
- [ ] 创建赛事 → 自动关联当前 active 赛季
- [ ] 无 active 赛季时创建赛事 → 显示错误提示
- [ ] 创建积分规则 → 按类型 Tab 展示
- [ ] 重复规则 → 显示 409 冲突错误

### 阶段 3 验收
- [ ] 上传 .xlsx 文件 → 返回 upload_id，进入解析状态
- [ ] 轮询显示"解析中" → 解析完成显示预览表格
- [ ] 预览表格中异常行标红
- [ ] 确认导入 → 赛事状态变为 completed
- [ ] 生成积分 → 赛事状态变为 published
- [ ] 积分记录写入数据库

### 阶段 4 验收
- [ ] 用户端排行榜显示积分数据
- [ ] 排名正确（同积分同排名）
- [ ] 搜索和院系筛选正常
- [ ] 点击选手 → 弹窗显示积分明细
- [ ] 积分分类汇总数据正确
- [ ] 管理端排行榜与用户端一致
- [ ] 刷新排行榜后数据更新

### 阶段 5 验收
- [ ] 仪表盘显示正确统计数据
- [ ] 关闭赛季 → 状态变为 closed
- [ ] 取消上传 → 状态变为 cancelled
- [ ] 撤回发布 → 赛事回退为 completed，积分记录删除
- [ ] 撤回后排行榜数据更新

### 全局验收
- [ ] 所有 API 响应结构符合 api_spec-v1.0.md
- [ ] 错误响应包含 detail 和 code 字段
- [ ] 401 错误自动跳转登录页
- [ ] 500 错误显示"系统异常"提示
- [ ] 分页参数正确传递和响应

---

## 9. 回滚策略

| 场景 | 回滚方式 |
|------|----------|
| 前端代码引入 Bug | git revert 到联调前 commit |
| 后端接口行为变更 | git revert 后端变更，恢复原有行为 |
| 数据库 schema 变更 | alembic downgrade 回退迁移 |
| 种子数据污染 | 重建数据库：drop + create + alembic upgrade head + seed |
| 联调环境不可用 | 前端可独立启动（API 调用会失败但页面可渲染） |
| 某阶段联调失败 | 回退到上一阶段验收通过的状态，修复后重新联调当前阶段 |

**数据库重建命令：**
```bash
# 重建数据库（需要 PostgreSQL 运行）
dropdb tha_tennis && createdb tha_tennis
cd backend && uv run alembic upgrade head
uv run python -m app.scripts.seed
```

**前端回滚：**
```bash
cd frontend && git stash  # 暂存当前修改
# 或
git checkout <last-known-good-commit> -- frontend/
```

---

## 10. 联调环境准备清单

联调开始前，确保以下环境就绪：

| 项目 | 命令 | 预期结果 |
|------|------|----------|
| PostgreSQL 运行 | `pg_isready` | accepting connections |
| Redis 运行 | `redis-cli ping` | PONG |
| 数据库迁移 | `cd backend && uv run alembic upgrade head` | 无错误 |
| 种子数据 | `uv run python -m app.scripts.seed` | admin 用户创建 |
| 后端启动 | `uv run uvicorn app.main:app --port 8000` | 无错误 |
| 健康检查 | `curl http://localhost:8000/api/v1/health` | {"status":"ok"} |
| 管理端启动 | `cd frontend/admin && pnpm dev` | localhost:5174 |
| 用户端启动 | `cd frontend/user && pnpm dev` | localhost:5173 |

---

## 11. 联调时间估算

| 阶段 | 预估工时 | 说明 |
|------|----------|------|
| 环境准备 | 0.5 天 | PostgreSQL + Redis + 迁移 + 种子数据 |
| 阶段 1 | 0.5 天 | 基础通路验证 |
| 阶段 2 | 1.5 天 | 4 个 CRUD 模块 |
| 阶段 3 | 2 天 | 异步流程，需准备测试 Excel 文件 |
| 阶段 4 | 1 天 | 数据展示验证 |
| 阶段 5 | 0.5 天 | 补全功能 |
| **合计** | **6 天** | — |
