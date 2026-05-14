# THA 年度赛事积分系统 Phase 开发计划

## 一、Phase 总览

| Phase | 阶段名称 | 目标 | 产出 |
| --- | --- | --- | --- |
| Phase 1 | 前后端基础框架搭建与运行测试 | 让项目跑起来 | 后端、用户端、管理后台基础框架 |
| Phase 2 | 前端 UI 研发 | 用 Mock 数据完成页面 | 公共排行榜 UI、弹窗、后台页面 |
| Phase 3 | 后端接口研发 | 完成真实业务接口 | 数据库、API、Excel 导入、积分计算 |
| Phase 4 | 前后端联调 | 打通完整业务闭环 | 可用 MVP 系统 |

---

## 二、Phase 1：前后端基础框架搭建与运行测试

### 2.1 Phase 1 目标

Phase 1 不做复杂业务，重点是把项目基础工程跑通。

需要完成：

- 后端服务能启动
- 数据库能连接
- Redis 能连接
- 用户端能启动
- 管理后台能启动
- 前端能调用后端健康检查接口
- 基础测试能运行

### 2.2 推荐项目目录结构

建议采用三端分离结构：

```
Tennis points platform/
  backend/
  frontend-user/
  frontend-admin/
  docker-compose.yml
  docs/
```

其中：

- `backend/`         后端 FastAPI 服务
- `frontend-user/`   公共积分榜用户端，微信小程序 / H5
- `frontend-admin/`  Web 管理后台
- `docs/`            产品文档、架构文档、接口文档

### 2.3 后端基础框架任务

后端技术栈：

- FastAPI
- Python
- SQLAlchemy 2.0
- Pydantic
- Alembic
- PostgreSQL
- Redis
- ARQ
- pytest

#### 任务清单

| 编号 | 任务 | 说明 |
| --- | --- | --- |
| BE-001 | 初始化 FastAPI 项目 | 创建 backend 目录 |
| BE-002 | 配置项目入口 | 创建 app/main.py |
| BE-003 | 配置环境变量 | 创建 .env.example |
| BE-004 | 配置数据库连接 | PostgreSQL 连接 |
| BE-005 | 配置 Redis 连接 | 后续任务队列使用 |
| BE-006 | 配置 CORS | 允许用户端和管理后台访问 |
| BE-007 | 配置 API 路由 | /api/v1 路由前缀 |
| BE-008 | 实现健康检查接口 | /api/v1/health |
| BE-009 | 初始化 Alembic | 数据库迁移 |
| BE-010 | 初始化 pytest | 后端测试 |
| BE-011 | 配置基础日志 | 方便调试 |

### 2.4 后端目录结构建议

```
backend/
  app/
    main.py
    api/
      v1/
        router.py
        health.py
    core/
      config.py
      database.py
      redis.py
      security.py
      logging.py
    models/
    schemas/
    services/
    repositories/
    workers/
    integrations/
    utils/
  tests/
    test_health.py
  alembic/
  alembic.ini
  pyproject.toml
  .env.example
```

### 2.5 Phase 1 后端接口

Phase 1 只需要一个基础接口：

```
GET /api/v1/health
```

返回示例：

```json
{
  "status": "ok",
  "service": "tha-tennis-points-api",
  "database": "connected",
  "redis": "connected"
}
```

### 2.6 用户端基础框架任务

用户端技术栈：

- Uni-app
- Vue 3
- TypeScript
- Pinia
- Wot Design Uni

用户端定位：

- 公共积分榜查看平台
- 无需登录
- 进入后直接查看排行榜

#### 任务清单

| 编号 | 任务 | 说明 |
| --- | --- | --- |
| FU-001 | 初始化 Uni-app 项目 | 支持 H5 和微信小程序 |
| FU-002 | 配置 TypeScript | 统一类型规范 |
| FU-003 | 配置 Pinia | 状态管理 |
| FU-004 | 配置 Wot Design Uni | UI 组件库 |
| FU-005 | 创建公共排行榜首页 | 暂时只显示标题 |
| FU-006 | 配置 API 请求封装 | 调用后端 health |
| FU-007 | 配置主题色 | 清华紫 |
| FU-008 | 移除登录 / 我的页面 | 用户端不需要登录 |

### 2.7 用户端目录结构建议

```
frontend-user/
  src/
    pages/
      ranking/
        index.vue
    components/
      RankingList.vue
      PlayerPointsDialog.vue
    services/
      request.ts
      ranking.ts
    stores/
      app.ts
    styles/
      theme.scss
    utils/
```

### 2.8 管理后台基础框架任务

管理后台技术栈：

- Vue 3
- TypeScript
- Element Plus
- Pinia
- Vue Router

#### 任务清单

| 编号 | 任务 | 说明 |
| --- | --- | --- |
| FA-001 | 初始化 Vue 3 项目 | 管理后台 |
| FA-002 | 配置 TypeScript | 类型规范 |
| FA-003 | 配置 Element Plus | 后台 UI |
| FA-004 | 配置 Vue Router | 路由管理 |
| FA-005 | 配置 Pinia | 状态管理 |
| FA-006 | 创建后台 Layout | 顶部栏 + 左侧菜单 |
| FA-007 | 创建登录页占位 | Phase 3 接真实接口 |
| FA-008 | 创建仪表盘占位 | Mock 数据 |
| FA-009 | 配置 API 请求封装 | 调用后端 health |

### 2.9 管理后台目录结构建议

```
frontend-admin/
  src/
    layouts/
      AdminLayout.vue
    views/
      Login.vue
      Dashboard.vue
      Seasons.vue
      Players.vue
      Tournaments.vue
      Uploads.vue
      PointsRules.vue
      Rankings.vue
      Logs.vue
    components/
    router/
      index.ts
    stores/
      auth.ts
      app.ts
    services/
      request.ts
      health.ts
    styles/
      theme.scss
```

### 2.10 Docker 基础服务

Phase 1 建议先用 Docker 跑：

- PostgreSQL
- Redis

本地开发时：

- 后端本地启动
- 用户端本地启动
- 管理后台本地启动
- PostgreSQL 和 Redis 用 Docker

### 2.11 Phase 1 验收标准

| 模块 | 验收标准 |
| --- | --- |
| 后端 | FastAPI 启动成功 |
| 后端 | /api/v1/health 返回正常 |
| 数据库 | PostgreSQL 可连接 |
| Redis | Redis 可连接 |
| 用户端 | 页面能启动，显示 THA 年度积分榜 |
| 用户端 | 不出现登录 / 我的页面 |
| 管理后台 | 后台 Layout 显示正常 |
| 管理后台 | 左侧菜单显示正常 |
| 测试 | 后端 pytest 能运行 |

---

## 三、Phase 2：前端 UI 研发

### 3.1 Phase 2 目标

用 Mock 数据完成所有核心页面 UI。

此阶段不依赖真实后端业务接口。

目标是：

- 先让产品看得见
- 先确定页面布局
- 先确定交互方式
- 后端接口完成后直接替换 Mock 数据

### 3.2 用户端 UI 规划

#### 用户端核心原则

用户端是公共积分榜：

- 无需登录
- 无我的页面
- 无用户中心
- 首页就是排行榜
- 点击选手名称打开积分明细弹窗

### 3.3 用户端页面结构

用户端建议采用单页布局：

**THA 年度积分榜页面**

页面结构：

```
顶部标题区
    ↓
赛季信息区
    ↓
筛选搜索区
    ↓
排行榜列表
    ↓
选手积分明细弹窗
```

### 3.4 用户端排行榜页面 UI

#### 桌面 H5 布局

适合宽屏，用表格展示：

```
排名    积分    姓名    年龄    参赛数量    院系
```

#### 移动端 / 小程序布局

适合卡片展示：

```
#1    张三                   2680 分
计算机系 ｜ 年龄 38 ｜ 参赛 6 次

#2    李四                   2400 分
经管学院 ｜ 年龄 42 ｜ 参赛 5 次

#2    王五                   2400 分
自动化系 ｜ 年龄 36 ｜ 参赛 7 次
```

### 3.5 用户端筛选区 UI

建议包含：

- 姓名搜索
- 院系筛选
- 组别筛选，可选
- 赛季选择，可选

第一版可以先做：

- 姓名搜索 + 院系筛选

### 3.6 选手积分明细弹窗 UI

点击排行榜中的选手姓名后弹出。

不要跳转页面。

#### 弹窗结构

```
弹窗标题：张三积分明细

基础信息：
- 院系
- 年龄
- 当前排名
- 年度总积分
- 参赛数量

积分统计：
- 单项赛积分
- 团体赛积分
- 奖补积分
- 办赛 / 捐赠积分

积分明细列表：
- 日期
- 积分来源
- 赛事名称
- 成绩 / 说明
- 获得积分
```

### 3.7 用户端组件拆分

- RankingPage
- RankingHeader
- SeasonInfoCard
- RankingFilter
- RankingTable
- RankingCardList
- PlayerPointsDialog
- PointsSourceTag

### 3.8 管理后台 UI 规划

#### 管理后台整体布局

- 顶部栏
- 左侧菜单
- 右侧内容区

#### 顶部栏

- THA 年度赛事积分管理系统
- 当前赛季：2026-2027
- 管理员名称
- 退出登录

#### 左侧菜单

- 仪表盘
- 赛季管理
- 选手管理
- 院系管理
- 赛事管理
- 团体管理
- Excel 导入
- 积分规则
- 积分明细
- 年度排行榜
- DeepSeek 解析日志
- 系统日志
- 系统设置

### 3.9 管理后台页面拆分

#### 1）仪表盘

展示：

- 当前赛季
- 选手总数
- 赛事总数
- 积分记录数
- 当前榜首
- 最近上传记录
- 最近刷新时间
- 异常数据数量

#### 2）赛季管理

功能：

- 赛季列表
- 新增赛季
- 编辑赛季
- 设置当前赛季
- 关闭赛季

#### 3）选手管理

功能：

- 选手列表
- 姓名搜索
- 院系筛选
- 新增选手
- 编辑选手
- 导入选手
- 合并重复选手

#### 4）赛事管理

功能：

- 赛事列表
- 新增赛事
- 编辑赛事
- 赛事等级
- 赛事组别
- 赛事地点
- 赛事日期
- 赛事状态

#### 5）团体管理

功能：

- 团体列表
- 团体成员维护
- 有效队员设置
- 团体赛积分分摊预览

#### 6）Excel 导入

这是最重要页面。

采用步骤条：

```
1 上传 Excel
2 解析 Excel
3 DeepSeek 辅助识别
4 导入预览
5 管理员确认
6 导入完成
```

#### 7）积分规则

Tabs：

- 单项赛事
- 团体赛事
- 远程参赛
- 代表队赛事
- 办赛奖励
- 捐赠赞助

#### 8）年度排行榜

功能：

- 查看排行榜
- 刷新排行榜
- 导出排行榜
- 查看选手积分明细
- 生成排名快照

### 3.10 Phase 2 验收标准

| 模块 | 验收标准 |
| --- | --- |
| 用户端 | 打开后直接看到排行榜 |
| 用户端 | 无登录入口 |
| 用户端 | 无我的页面 |
| 用户端 | 点击选手名称弹出积分明细 |
| 用户端 | 移动端卡片布局正常 |
| 用户端 | H5 表格布局正常 |
| 管理后台 | Layout 完成 |
| 管理后台 | Excel 导入步骤条完成 |
| 管理后台 | 积分规则页面完成 |
| 管理后台 | 排行榜管理页面完成 |
| 数据 | 所有页面可用 Mock 数据展示 |

---

## 四、Phase 3：后端接口研发

### 4.1 Phase 3 目标

完成真实后端业务能力。

包括：

- 数据库模型
- 管理后台接口
- 公共排行榜接口
- Excel 上传
- DeepSeek 接入
- 积分生成
- 排行榜计算
- 审计日志

### 4.2 数据库表开发顺序

建议按以下顺序建表：

1. users
2. seasons
3. departments
4. players
5. tournaments
6. points_rules
7. uploads
8. event_results
9. teams
10. team_members
11. entries_points
12. audit_logs
13. ai_parse_logs
14. ranking_snapshots

### 4.3 公共接口优先开发

用户端无需登录，所以公共接口优先级很高。

#### 公共接口

```
GET /api/v1/public/seasons/current
GET /api/v1/public/rankings
GET /api/v1/public/players/{player_id}/points
GET /api/v1/public/rules/summary
```

### 4.4 管理后台接口

#### 登录接口

```
POST /api/v1/admin/auth/login
POST /api/v1/admin/auth/logout
GET  /api/v1/admin/auth/me
```

#### 赛季接口

```
GET  /api/v1/admin/seasons
POST /api/v1/admin/seasons
PUT  /api/v1/admin/seasons/{id}
POST /api/v1/admin/seasons/{id}/activate
```

#### 选手接口

```
GET    /api/v1/admin/players
POST   /api/v1/admin/players
PUT    /api/v1/admin/players/{id}
DELETE /api/v1/admin/players/{id}
```

#### 赛事接口

```
GET    /api/v1/admin/tournaments
POST   /api/v1/admin/tournaments
PUT    /api/v1/admin/tournaments/{id}
DELETE /api/v1/admin/tournaments/{id}
```

#### 积分规则接口

```
GET    /api/v1/admin/points-rules
POST   /api/v1/admin/points-rules
PUT    /api/v1/admin/points-rules/{id}
DELETE /api/v1/admin/points-rules/{id}
```

#### Excel 上传接口

```
POST /api/v1/admin/uploads
GET  /api/v1/admin/uploads
GET  /api/v1/admin/uploads/{id}
POST /api/v1/admin/uploads/{id}/parse
POST /api/v1/admin/uploads/{id}/confirm
```

#### DeepSeek 接口

```
POST /api/v1/admin/ai/deepseek/parse-upload/{upload_id}
GET  /api/v1/admin/ai/deepseek/logs
GET  /api/v1/admin/ai/deepseek/logs/{id}
```

#### 排行榜接口

```
GET  /api/v1/admin/rankings
POST /api/v1/admin/rankings/refresh
GET  /api/v1/admin/rankings/export
POST /api/v1/admin/rankings/snapshot
```

### 4.5 后端服务开发顺序

建议顺序：

1. SeasonService
2. PlayerService
3. TournamentService
4. PointsRuleService
5. UploadService
6. EventResultService
7. PointsGenerationService
8. RankingService
9. DeepSeekService
10. AuditService

### 4.6 DeepSeek 接入细化

#### DeepSeekService 职责

- 读取 Excel 解析文本
- 组装 Prompt
- 调用 DeepSeek API
- 获取 JSON 输出
- Pydantic 校验 JSON
- 保存 ai_parse_logs
- 生成导入预览

#### DeepSeek 使用边界

- 只辅助解析
- 不直接入库
- 不计算最终积分
- 不刷新排行榜
- 必须经过管理员确认

### 4.7 积分生成逻辑

#### 单项双打

- 选手 A / 选手 B 获得冠军
- 赛事等级 THA500
- 冠军积分 500
- 选手 A entries_points +500
- 选手 B entries_points +500

#### 团体赛

- 团队总积分 1800
- 有效队员 8 人
- 每人积分 round(1800 / 8) = 225

#### 远程参赛

- 跨省 +200
- 跨境 +500

#### 代表队参赛

- 胜场 40
- 负场 20
- 基础参赛 20

#### 办赛奖励

- 承办 THA500 = 500
- 承办 THA800 = 800

#### 捐赠赞助

- 等值 10000 元 = 200 分

### 4.8 Phase 3 验收标准

| 模块 | 验收标准 |
| --- | --- |
| 数据库 | 所有核心表完成 |
| 公共接口 | 排行榜接口返回真实数据 |
| 公共接口 | 选手积分明细接口返回真实数据 |
| 后台接口 | 登录可用 |
| 后台接口 | 赛季、选手、赛事 CRUD 可用 |
| Excel | 上传、解析、预览、确认流程可用 |
| 积分 | 单项双打积分生成正确 |
| 积分 | 团体赛分摊正确 |
| 排行榜 | 并列排名正确 |
| DeepSeek | 基础解析接口完成 |
| 测试 | 关键服务单元测试通过 |

---

## 五、Phase 4：前后端联调

### 5.1 Phase 4 目标

打通完整业务闭环。

### 5.2 用户端联调

联调内容：

- 打开用户端
- 自动请求当前赛季
- 自动请求排行榜
- 展示排行榜
- 姓名搜索
- 院系筛选
- 点击选手名称
- 请求积分明细接口
- 弹出积分明细

对应接口：

```
GET /api/v1/public/seasons/current
GET /api/v1/public/rankings
GET /api/v1/public/players/{player_id}/points
```

### 5.3 管理后台联调

联调内容：

- 管理员登录
- 创建赛季
- 创建积分规则
- 导入选手
- 创建赛事
- 上传 Excel
- 生成导入预览
- 确认导入
- 生成积分明细
- 刷新排行榜
- 用户端查看最新排行榜

### 5.4 业务闭环测试

必须完整跑通：

```
创建 2026-2027 赛季
    ↓
配置 THA500 规则
    ↓
创建 THA500 成都站
    ↓
导入冠军 / 亚军 / 前四名 Excel
    ↓
系统生成导入预览
    ↓
管理员确认导入
    ↓
生成 entries_points
    ↓
刷新排行榜
    ↓
公共用户端看到排名
    ↓
点击张三
    ↓
弹出张三积分明细
```

### 5.5 Phase 4 验收标准

| 模块 | 验收标准 |
| --- | --- |
| 用户端 | 无需登录即可访问 |
| 用户端 | 排行榜展示真实数据 |
| 用户端 | 点击姓名弹出积分明细 |
| 管理后台 | 登录可用 |
| 管理后台 | Excel 导入闭环可用 |
| 管理后台 | 积分规则配置可用 |
| 管理后台 | 排行榜刷新可用 |
| DeepSeek | 可调用或已预留 |
| 全链路 | 标准赛事结果导入到排行榜展示闭环跑通 |

---

## 六、推荐开发排期

如果是 1-2 人开发，建议：

| 阶段 | 时间 | 重点 |
| --- | --- | --- |
| Phase 1 | 3-5 天 | 框架搭建和运行测试 |
| Phase 2 | 5-8 天 | 前端 UI 和 Mock 数据 |
| Phase 3 | 10-15 天 | 后端接口和积分逻辑 |
| Phase 4 | 5-7 天 | 联调和修复问题 |

总计：

- 约 3-5 周完成 MVP

如果人手更多，可以并行：

- 前端 Phase 2 与后端 Phase 3 部分并行

---

## 七、任务优先级建议

### 最高优先级 P0

- 用户端公共排行榜
- 选手积分明细弹窗
- 管理后台 Excel 上传
- 积分规则配置
- 积分生成
- 年度排行榜计算

### 高优先级 P1

- 赛季管理
- 选手管理
- 赛事管理
- 团体管理
- 导入预览
- 审计日志

### 中优先级 P2

- DeepSeek 智能解析
- 院系榜
- 历史排名
- 导出 Excel
- 排名快照

### 低优先级 P3

- 复杂图表
- Elo/Glicko
- 自动签表
- 逐场比分录入
- 社交功能

---

## 八、最终建议执行路径

建议你现在就按这个顺序推进：

1. 第一步：搭 backend / frontend-user / frontend-admin 三个项目骨架
2. 第二步：后端先出 health 接口
3. 第三步：两个前端都调通 health 接口
4. 第四步：用户端先完成公共排行榜 UI
5. 第五步：管理后台完成 Excel 导入 UI
6. 第六步：后端开始建表和接口
7. 第七步：后端实现积分生成和排行榜
8. 第八步：前后端联调完整导入流程

这样项目推进会比较稳，且每个阶段都有明确可验收产物。

