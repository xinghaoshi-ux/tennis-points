# API 规范 v1.0

> 本文定义 THA 年度赛事积分系统 MVP 阶段的完整 API 契约。
>
> 前后端实现必须以本文档为准。字段来源于数据模型字段字典，状态值与流程状态规范一致。

---

## 1. 通用约定

### 1.1 基础信息

| 项目 | 值 |
|---|---|
| Base URL | /api/v1 |
| 公共接口前缀 | /api/v1/public |
| 管理接口前缀 | /api/v1/admin |
| 内容类型 | application/json（文件上传为 multipart/form-data） |
| 认证方式 | Bearer Token（管理接口） |
| 分页参数 | page（默认 1）、page_size（默认 20，最大 100） |

### 1.2 通用响应结构

成功（单对象）：

```json
{
  "data": { ... },
  "message": "ok"
}
```

成功（列表）：

```json
{
  "data": [ ... ],
  "total": 100,
  "page": 1,
  "page_size": 20
}
```

错误：

```json
{
  "detail": "错误描述",
  "code": "ERROR_CODE"
}
```

---

## 2. 公共接口

### 2.1 获取当前赛季

| 项目 | 值 |
|---|---|
| 方法 | GET |
| 路径 | /api/v1/public/seasons/current |
| 用途 | 获取当前激活赛季信息 |
| 调用时机 | 用户端页面加载时 |
| 认证 | 无 |

响应示例：

```json
{
  "data": {
    "id": 1,
    "name": "2026-2027 THA 赛季",
    "start_date": "2026-04-20",
    "end_date": "2027-04-20",
    "status": "active"
  }
}
```

---

### 2.2 查询排行榜

| 项目 | 值 |
|---|---|
| 方法 | GET |
| 路径 | /api/v1/public/rankings |
| 用途 | 查询年度积分排行榜 |
| 调用时机 | 用户端排行榜页面加载、搜索、筛选时 |
| 认证 | 无 |

请求参数（Query）：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| page | integer | 否 | 页码，默认 1 |
| page_size | integer | 否 | 每页条数，默认 20 |
| search | string | 否 | 姓名模糊搜索 |
| department | string | 否 | 院系精确筛选 |

响应示例：

```json
{
  "data": [
    {
      "ranking": 1,
      "player_id": 42,
      "full_name": "张三",
      "department": "计算机系",
      "age": 38,
      "total_points": 2680,
      "tournament_count": 6
    },
    {
      "ranking": 2,
      "player_id": 15,
      "full_name": "李四",
      "department": "经管学院",
      "age": 42,
      "total_points": 2400,
      "tournament_count": 5
    }
  ],
  "total": 120,
  "page": 1,
  "page_size": 20
}
```

字段说明：

| 字段 | 来源 | 说明 |
|---|---|---|
| ranking | 动态计算 | RANK() 窗口函数，同积分并列 |
| player_id | Player.id | 选手 ID |
| full_name | Player.full_name | 姓名 |
| department | Player.department | 院系 |
| age | 动态计算 | 当前日期 - Player.birth_date |
| total_points | 动态计算 | SUM(EntriesPoints.points_earned) |
| tournament_count | 动态计算 | COUNT(DISTINCT tournament_id) |

---

### 2.3 查询选手积分明细

| 项目 | 值 |
|---|---|
| 方法 | GET |
| 路径 | /api/v1/public/players/{player_id}/points |
| 用途 | 查询某位选手的积分构成和明细 |
| 调用时机 | 用户点击排行榜中的选手姓名时 |
| 认证 | 无 |

响应示例：

```json
{
  "data": {
    "player": {
      "id": 42,
      "full_name": "张三",
      "department": "计算机系",
      "age": 38,
      "ranking": 1,
      "total_points": 2680,
      "tournament_count": 6
    },
    "summary": {
      "individual_event": 1480,
      "team_share": 450,
      "travel_bonus": 400,
      "representative_team": 120,
      "organizer_bonus": 0,
      "donation_bonus": 230
    },
    "details": [
      {
        "id": 301,
        "tournament_name": "THA500 成都站",
        "source_type": "individual_event",
        "result_type": "champion",
        "points_earned": 500,
        "description": "THA500 成都站 甲组 冠军",
        "tournament_date": "2026-08-17",
        "team_name": null,
        "team_total_points": null,
        "team_member_count": null
      },
      {
        "id": 305,
        "tournament_name": "THA A 级团体赛北京站",
        "source_type": "team_share",
        "result_type": "champion",
        "points_earned": 225,
        "description": "团队冠军 1800 分，8 人分摊",
        "tournament_date": "2026-10-20",
        "team_name": "计算机学院队",
        "team_total_points": 1800,
        "team_member_count": 8
      }
    ]
  }
}
```

---

### 2.4 查询院系列表

| 项目 | 值 |
|---|---|
| 方法 | GET |
| 路径 | /api/v1/public/departments |
| 用途 | 获取院系列表用于筛选器 |
| 调用时机 | 用户端页面加载时 |
| 认证 | 无 |

响应示例：

```json
{
  "data": ["计算机系", "经管学院", "自动化系", "电子系", "物理系"]
}
```

---

## 3. 管理接口 - 认证

### 3.1 管理员登录

| 项目 | 值 |
|---|---|
| 方法 | POST |
| 路径 | /api/v1/admin/auth/login |
| 用途 | 管理员登录获取 Token |
| 调用时机 | 管理端登录页提交 |
| 认证 | 无 |

请求体：

```json
{
  "username": "admin",
  "password": "password123"
}
```

响应示例：

```json
{
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer",
    "expires_in": 86400,
    "user": {
      "id": 1,
      "username": "admin",
      "display_name": "管理员"
    }
  }
}
```

### 3.2 获取当前用户

| 项目 | 值 |
|---|---|
| 方法 | GET |
| 路径 | /api/v1/admin/auth/me |
| 用途 | 验证 Token 有效性并获取用户信息 |
| 调用时机 | 管理端页面刷新时 |
| 认证 | 是 |

---

## 4. 管理接口 - 赛季

### 4.1 查询赛季列表

| 项目 | 值 |
|---|---|
| 方法 | GET |
| 路径 | /api/v1/admin/seasons |
| 用途 | 获取所有赛季 |
| 认证 | 是 |

响应示例：

```json
{
  "data": [
    {
      "id": 1,
      "name": "2026-2027 THA 赛季",
      "start_date": "2026-04-20",
      "end_date": "2027-04-20",
      "status": "active",
      "created_at": "2026-03-01T10:00:00"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 20
}
```

### 4.2 创建赛季

| 项目 | 值 |
|---|---|
| 方法 | POST |
| 路径 | /api/v1/admin/seasons |
| 认证 | 是 |

请求体：

```json
{
  "name": "2026-2027 THA 赛季",
  "start_date": "2026-04-20",
  "end_date": "2027-04-20"
}
```

响应：201 Created，返回赛季记录（status 默认 draft）。

### 4.3 更新赛季

| 项目 | 值 |
|---|---|
| 方法 | PUT |
| 路径 | /api/v1/admin/seasons/{id} |
| 认证 | 是 |

### 4.4 激活赛季

| 项目 | 值 |
|---|---|
| 方法 | POST |
| 路径 | /api/v1/admin/seasons/{id}/activate |
| 用途 | 将 draft 赛季激活为 active |
| 认证 | 是 |

响应：200，返回更新后的赛季记录。原 active 赛季自动变为 closed。

### 4.5 关闭赛季

| 项目 | 值 |
|---|---|
| 方法 | POST |
| 路径 | /api/v1/admin/seasons/{id}/close |
| 用途 | 关闭 active 赛季 |
| 认证 | 是 |

---

## 5. 管理接口 - 选手

### 5.1 查询选手列表

| 项目 | 值 |
|---|---|
| 方法 | GET |
| 路径 | /api/v1/admin/players |
| 认证 | 是 |

请求参数（Query）：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| page | integer | 否 | 页码 |
| page_size | integer | 否 | 每页条数 |
| search | string | 否 | 姓名搜索 |
| department | string | 否 | 院系筛选 |

响应字段：id, full_name, gender, birth_date, department, status, created_at

### 5.2 创建选手

| 项目 | 值 |
|---|---|
| 方法 | POST |
| 路径 | /api/v1/admin/players |
| 认证 | 是 |

请求体：

```json
{
  "full_name": "张三",
  "gender": "male",
  "birth_date": "1988-05-12",
  "department": "计算机系",
  "phone": "13800001234"
}
```

### 5.3 更新选手

| 项目 | 值 |
|---|---|
| 方法 | PUT |
| 路径 | /api/v1/admin/players/{id} |
| 认证 | 是 |

### 5.4 获取单个选手

| 项目 | 值 |
|---|---|
| 方法 | GET |
| 路径 | /api/v1/admin/players/{id} |
| 认证 | 是 |

---

## 6. 管理接口 - 赛事

### 6.1 查询赛事列表

| 项目 | 值 |
|---|---|
| 方法 | GET |
| 路径 | /api/v1/admin/tournaments |
| 认证 | 是 |

请求参数（Query）：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| page | integer | 否 | 页码 |
| page_size | integer | 否 | 每页条数 |
| status | string | 否 | 状态筛选 |
| season_id | integer | 否 | 赛季筛选 |

响应字段：id, season_id, name, event_category, level, group_name, start_date, end_date, location, status, created_at

### 6.2 创建赛事

| 项目 | 值 |
|---|---|
| 方法 | POST |
| 路径 | /api/v1/admin/tournaments |
| 认证 | 是 |

请求体：

```json
{
  "name": "THA500 成都站",
  "event_category": "individual_doubles",
  "level": "THA500",
  "group_name": "甲组",
  "start_date": "2026-08-15",
  "end_date": "2026-08-17",
  "location": "成都",
  "alumni_player_count": 35
}
```

season_id 由后端自动取当前 active 赛季。

### 6.3 更新赛事

| 项目 | 值 |
|---|---|
| 方法 | PUT |
| 路径 | /api/v1/admin/tournaments/{id} |
| 认证 | 是 |
| 约束 | 仅 draft 状态可编辑 |

### 6.4 获取单个赛事

| 项目 | 值 |
|---|---|
| 方法 | GET |
| 路径 | /api/v1/admin/tournaments/{id} |
| 认证 | 是 |

---

## 7. 管理接口 - 积分规则

### 7.1 查询积分规则

| 项目 | 值 |
|---|---|
| 方法 | GET |
| 路径 | /api/v1/admin/points-rules |
| 认证 | 是 |

请求参数（Query）：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| season_id | integer | 否 | 赛季（默认当前赛季） |
| rule_type | string | 否 | 规则类型筛选 |

### 7.2 创建积分规则

| 项目 | 值 |
|---|---|
| 方法 | POST |
| 路径 | /api/v1/admin/points-rules |
| 认证 | 是 |

请求体：

```json
{
  "rule_type": "individual_event",
  "event_level": "THA500",
  "group_name": "甲组",
  "result_type": "champion",
  "points": 500
}
```

season_id 由后端自动取当前 active 赛季。

### 7.3 更新积分规则

| 项目 | 值 |
|---|---|
| 方法 | PUT |
| 路径 | /api/v1/admin/points-rules/{id} |
| 认证 | 是 |

### 7.4 删除积分规则

| 项目 | 值 |
|---|---|
| 方法 | DELETE |
| 路径 | /api/v1/admin/points-rules/{id} |
| 认证 | 是 |
| 约束 | 已被引用的规则不可删除 |

---

## 8. 管理接口 - Excel 导入

### 8.1 上传 Excel

| 项目 | 值 |
|---|---|
| 方法 | POST |
| 路径 | /api/v1/admin/uploads |
| 用途 | 上传赛事结果 Excel 文件 |
| 调用时机 | 管理员在 Excel 导入页选择文件后 |
| 认证 | 是 |
| Content-Type | multipart/form-data |

请求参数：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| file | File | 是 | Excel 文件（.xlsx） |
| tournament_id | integer | 是 | 关联赛事 ID |

响应示例（201）：

```json
{
  "data": {
    "id": 10,
    "tournament_id": 5,
    "filename": "THA500成都站结果.xlsx",
    "status": "pending",
    "created_at": "2026-08-20T14:30:00"
  }
}
```

上传成功后系统自动触发异步解析任务。

### 8.2 查询上传状态

| 项目 | 值 |
|---|---|
| 方法 | GET |
| 路径 | /api/v1/admin/uploads/{id} |
| 用途 | 查询上传处理状态（前端轮询） |
| 调用时机 | 上传后每 3 秒轮询直到终态 |
| 认证 | 是 |

响应示例（解析完成）：

```json
{
  "data": {
    "id": 10,
    "tournament_id": 5,
    "filename": "THA500成都站结果.xlsx",
    "status": "parsed",
    "total_rows": 12,
    "valid_rows": 10,
    "error_rows": 2,
    "error_log": null,
    "created_at": "2026-08-20T14:30:00"
  }
}
```

### 8.3 查询导入预览

| 项目 | 值 |
|---|---|
| 方法 | GET |
| 路径 | /api/v1/admin/uploads/{id}/preview |
| 用途 | 获取解析后的逐行预览数据 |
| 调用时机 | Upload status 变为 parsed 后 |
| 认证 | 是 |

响应示例：

```json
{
  "data": [
    {
      "row_number": 1,
      "tournament_name": "THA500 成都站",
      "level": "THA500",
      "group_name": "甲组",
      "result_type": "champion",
      "player1_name": "张三",
      "player1_id": 42,
      "player1_matched": true,
      "player2_name": "李四",
      "player2_id": 15,
      "player2_matched": true,
      "is_cross_province": true,
      "is_cross_border": false,
      "estimated_points": 500,
      "row_status": "normal",
      "error_message": null
    },
    {
      "row_number": 3,
      "tournament_name": "THA500 成都站",
      "level": "THA500",
      "group_name": "甲组",
      "result_type": "semifinal",
      "player1_name": "小王",
      "player1_id": null,
      "player1_matched": false,
      "player2_name": "赵六",
      "player2_id": 28,
      "player2_matched": true,
      "is_cross_province": false,
      "is_cross_border": false,
      "estimated_points": 180,
      "row_status": "warning",
      "error_message": "选手'小王'未匹配"
    }
  ]
}
```

row_status 取值：normal / warning / error

### 8.4 确认导入

| 项目 | 值 |
|---|---|
| 方法 | POST |
| 路径 | /api/v1/admin/uploads/{id}/confirm |
| 用途 | 管理员确认导入，将数据写入 event_results |
| 调用时机 | 管理员审核预览后点击确认 |
| 认证 | 是 |
| 约束 | Upload status 必须为 parsed |

请求体：

```json
{
  "confirmed_rows": [1, 2, 4, 5, 6, 7, 8, 9, 10, 12],
  "ignored_rows": [3, 11]
}
```

响应示例（200）：

```json
{
  "data": {
    "upload_id": 10,
    "status": "imported",
    "imported_count": 10,
    "ignored_count": 2
  }
}
```

### 8.5 取消上传

| 项目 | 值 |
|---|---|
| 方法 | POST |
| 路径 | /api/v1/admin/uploads/{id}/cancel |
| 用途 | 取消上传 |
| 认证 | 是 |
| 约束 | Upload status 为 pending 或 parsed 时可取消 |

---

## 9. 管理接口 - 积分生成

### 9.1 触发积分生成

| 项目 | 值 |
|---|---|
| 方法 | POST |
| 路径 | /api/v1/admin/tournaments/{id}/generate-points |
| 用途 | 为已完赛的赛事生成积分记录 |
| 调用时机 | Excel 导入完成后 |
| 认证 | 是 |
| 约束 | Tournament status 必须为 completed |

响应示例（202 Accepted）：

```json
{
  "data": {
    "tournament_id": 5,
    "message": "积分生成任务已提交"
  }
}
```

### 9.2 查询赛事积分生成状态

通过查询赛事详情接口（GET /admin/tournaments/{id}）的 status 字段判断：
- completed：积分尚未生成
- published：积分已生成

---

## 10. 管理接口 - 排行榜

### 10.1 查询排行榜（管理端）

| 项目 | 值 |
|---|---|
| 方法 | GET |
| 路径 | /api/v1/admin/rankings |
| 用途 | 管理端查看排行榜 |
| 认证 | 是 |

请求参数同公共排行榜接口。响应结构同公共排行榜接口。

### 10.2 刷新排行榜

| 项目 | 值 |
|---|---|
| 方法 | POST |
| 路径 | /api/v1/admin/rankings/refresh |
| 用途 | 触发排行榜刷新 |
| 认证 | 是 |

响应示例（202 Accepted）：

```json
{
  "data": {
    "message": "排行榜刷新任务已提交"
  }
}
```

### 10.3 撤回赛事发布

| 项目 | 值 |
|---|---|
| 方法 | POST |
| 路径 | /api/v1/admin/tournaments/{id}/revoke-publish |
| 用途 | 撤回已发布赛事，删除关联积分记录 |
| 认证 | 是 |
| 约束 | Tournament status 必须为 published |

响应：200，Tournament 回退为 completed。

---

## 11. 管理接口 - 仪表盘

### 11.1 查询仪表盘数据

| 项目 | 值 |
|---|---|
| 方法 | GET |
| 路径 | /api/v1/admin/dashboard |
| 用途 | 获取系统概览统计 |
| 认证 | 是 |

响应示例：

```json
{
  "data": {
    "current_season": "2026-2027 THA 赛季",
    "player_count": 156,
    "tournament_count": 8,
    "points_record_count": 342,
    "recent_uploads": [
      {
        "id": 10,
        "filename": "THA500成都站结果.xlsx",
        "status": "imported",
        "created_at": "2026-08-20T14:30:00"
      }
    ]
  }
}
```

---

## 12. 健康检查

### 12.1 健康检查接口

| 项目 | 值 |
|---|---|
| 方法 | GET |
| 路径 | /api/v1/health |
| 用途 | 验证服务可用性 |
| 认证 | 无 |

响应示例：

```json
{
  "status": "ok",
  "service": "tha-tennis-points-api",
  "database": "connected",
  "redis": "connected"
}
```

---

## 13. 异步任务接口关系

### 13.1 Excel 解析（异步）

```text
POST /admin/uploads              → 创建上传，返回 upload_id，自动触发解析
GET  /admin/uploads/{id}         → 轮询状态（pending → parsing → parsed / parse_failed）
GET  /admin/uploads/{id}/preview → 状态为 parsed 时获取预览
POST /admin/uploads/{id}/confirm → 确认导入
```

### 13.2 积分生成（异步）

```text
POST /admin/tournaments/{id}/generate-points → 触发生成，返回 202
GET  /admin/tournaments/{id}                 → 轮询状态（completed → published）
```

### 13.3 排行榜刷新（异步）

```text
POST /admin/rankings/refresh → 触发刷新，返回 202
GET  /admin/rankings         → 查询最新排行榜
```

---

## 14. MVP 接口优先级

### 14.1 MVP 必须实现（P0）

| 接口 | 说明 |
|---|---|
| GET /health | 服务验证 |
| POST /admin/auth/login | 登录 |
| GET /admin/auth/me | Token 验证 |
| GET/POST /admin/seasons | 赛季管理 |
| POST /admin/seasons/{id}/activate | 赛季激活 |
| GET/POST/PUT /admin/players | 选手管理 |
| GET/POST/PUT /admin/tournaments | 赛事管理 |
| GET/POST/PUT/DELETE /admin/points-rules | 积分规则 |
| POST /admin/uploads | Excel 上传 |
| GET /admin/uploads/{id} | 上传状态查询 |
| GET /admin/uploads/{id}/preview | 导入预览 |
| POST /admin/uploads/{id}/confirm | 确认导入 |
| POST /admin/tournaments/{id}/generate-points | 积分生成 |
| POST /admin/rankings/refresh | 排行榜刷新 |
| GET /public/seasons/current | 当前赛季 |
| GET /public/rankings | 排行榜查询 |
| GET /public/players/{id}/points | 积分明细 |
| GET /public/departments | 院系列表 |

### 14.2 MVP 可简化（P1）

| 接口 | 说明 |
|---|---|
| GET /admin/dashboard | 仪表盘（可返回简化数据） |
| POST /admin/seasons/{id}/close | 赛季关闭 |
| POST /admin/uploads/{id}/cancel | 取消上传 |
| POST /admin/tournaments/{id}/revoke-publish | 撤回发布 |
| GET /admin/rankings | 管理端排行榜（可复用公共接口） |
