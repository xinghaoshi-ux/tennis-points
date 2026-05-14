# 工作流架构设计

> 本文定义 THA 年度赛事积分系统中涉及多步骤处理的工作流架构，包括 Excel 导入流程、积分生成流程和排行榜刷新流程。
>
> 工作流是系统中最复杂的部分，本文档明确每个流程的步骤、状态变化、异常处理和恢复策略。

---

## 1. 工作流设计原则

- 每个工作流有明确的起点和终点。
- 每个步骤执行后都有确定的状态记录。
- 任何步骤失败都不会产生"半完成"的脏数据。
- 异步工作流通过状态字段追踪进度，前端通过轮询获取状态。
- 人工确认节点将工作流分为"系统自动"和"人工决策"两段。

---

## 2. Excel 导入工作流

### 2.1 流程总览

```text
上传文件 → 解析 Excel → 数据校验 → 生成预览 → [人工确认] → 写入数据库
```

### 2.2 详细步骤

| 步骤 | 执行方式 | 执行者 | 输入 | 输出 | 状态变化 |
|---|---|---|---|---|---|
| 1. 接收文件 | 同步 | API 层 | multipart 文件 | 文件路径 | Upload: → pending |
| 2. 创建记录 | 同步 | UploadService | 文件路径、赛事 ID | upload 记录 | 无 |
| 3. 派发任务 | 同步 | UploadService | upload ID | 任务 ID | 无 |
| 4. 读取 Excel | 异步 | ExcelParseProcessor | 文件路径 | 原始行数据 | Upload: pending → parsing |
| 5. 识别表头 | 异步 | ExcelParseProcessor | 原始行数据 | 字段映射 | 无 |
| 6. 提取数据行 | 异步 | ExcelParseProcessor | 字段映射 + 原始数据 | 结构化行列表 | 无 |
| 7. 校验数据 | 异步 | DataValidationProcessor | 结构化行列表 | 校验结果（正常/异常标记） | 无 |
| 8. 生成预览 | 异步 | Worker | 校验结果 | 预览数据（含行级状态） | Upload: parsing → parsed |
| 9. 人工审核 | 等待 | 管理员 | 预览数据 | 确认/修改/忽略/取消 | 无 |
| 10. 写入数据 | 同步 | UploadService | 确认的行列表 | event_results 记录 | Upload: parsed → imported |

### 2.3 步骤 4-8 详细处理（异步任务内）

```text
excel_parse_task(upload_id):
    1. 更新 Upload status = parsing
    2. 读取文件
       ├─ 成功 → 继续
       └─ 失败 → status = parse_failed, 记录错误, 结束
    3. 识别表头，匹配标准模板列
       ├─ 匹配成功 → 继续
       └─ 匹配失败 → status = parse_failed, 记录错误, 结束
    4. 逐行提取数据
    5. 逐行校验
       ├─ 选手匹配：查询 players 表
       ├─ 成绩校验：检查是否在允许值内
       ├─ 重复检测：检查 event_results 是否已存在
       └─ 组别校验：检查是否在系统配置中
    6. 生成预览数据（每行标记 status: normal / warning / error）
    7. 保存预览数据
    8. 更新 Upload status = parsed
```

### 2.4 步骤 10 详细处理（确认导入）

```text
confirm_import(upload_id, confirmed_rows):
    BEGIN TRANSACTION
    1. 校验 Upload status == parsed
    2. 过滤出 confirmed_rows 中状态为 normal 的行
    3. 批量写入 event_results
    4. 更新 Upload status = imported
    5. 更新 Tournament status = completed（如果是该赛事首次导入结果）
    COMMIT
    
    失败时：ROLLBACK，Upload 保持 parsed
```

### 2.5 异常恢复

| 异常 | 恢复策略 |
|---|---|
| 文件读取失败 | status = parse_failed，管理员重新上传 |
| 表头不匹配 | status = parse_failed，提示使用标准模板 |
| 部分行校验失败 | status = parsed，异常行标记在预览中，管理员决定 |
| 确认导入时数据库错误 | 事务回滚，保持 parsed，管理员重试 |

---

## 3. 积分生成工作流

### 3.1 流程总览

```text
触发生成 → 查询赛事结果 → 匹配规则 → 计算积分 → 写入记录 → 更新状态
```

### 3.2 详细步骤

| 步骤 | 执行方式 | 执行者 | 输入 | 输出 |
|---|---|---|---|---|
| 1. 触发 | 同步 | PointsService | 赛事 ID | 任务 ID |
| 2. 前置校验 | 异步 | Worker | 赛事 ID | 校验结果 |
| 3. 查询赛事结果 | 异步 | PointsGenerationProcessor | 赛事 ID | event_results 列表 |
| 4. 匹配积分规则 | 异步 | PointsGenerationProcessor | 赛事级别、组别、成绩 | 规则记录 |
| 5. 计算积分 | 异步 | PointsGenerationProcessor | 结果 + 规则 | 积分记录列表 |
| 6. 写入积分 | 异步 | Worker | 积分记录列表 | entries_points 记录 |
| 7. 更新赛事状态 | 异步 | Worker | 赛事 ID | Tournament: published |
| 8. 标记排行榜 | 异步 | Worker | 赛季 ID | Ranking: stale |

### 3.3 步骤 5 积分计算逻辑

```text
对每条 event_result：
    判断赛事分类：
    
    [单项双打赛]
        查找规则：赛事级别 + 组别 + 成绩 → 积分值
        为每名搭档生成一条 entries_points（source_type: individual_event）
        如有远程参赛标记：额外生成一条 entries_points（source_type: travel_bonus）
    
    [团体赛]
        查找规则：团体赛级别 + 成绩 → 团队总积分
        获取有效队员列表
        计算分摊：round(团队总积分 / 有效队员人数)
        为每名有效队员生成一条 entries_points（source_type: team_share）
    
    [代表队赛事]
        根据胜场/负场/基础参赛计算积分
        生成 entries_points（source_type: representative_team）
    
    [办赛奖励]
        查找规则：承办赛事级别 → 奖励积分
        生成 entries_points（source_type: organizer_bonus）
    
    [捐赠赞助]
        根据金额换算积分
        生成 entries_points（source_type: donation_bonus）
```

### 3.4 事务设计

```text
points_generation_task(tournament_id):
    BEGIN TRANSACTION
    1. 校验 Tournament status == completed
    2. 校验无已有积分记录（防止重复生成）
    3. 执行积分计算
    4. 批量写入 entries_points
    5. 更新 Tournament status = published
    COMMIT
    
    成功后（事务外）：
    6. 标记排行榜为 stale
    
    失败时：ROLLBACK，Tournament 保持 completed
```

### 3.5 异常恢复

| 异常 | 恢复策略 |
|---|---|
| 规则未找到 | 任务失败，提示管理员配置规则后重试 |
| 团体队员人数为零 | 任务失败，提示管理员修正队员数据 |
| 数据库写入失败 | 事务回滚，管理员重试 |
| 重复生成检测 | 拒绝执行，提示已有积分记录 |

---

## 4. 排行榜刷新工作流

### 4.1 流程总览

```text
触发刷新 → 聚合积分 → 计算排名 → 更新状态
```

### 4.2 详细步骤

| 步骤 | 执行方式 | 执行者 | 说明 |
|---|---|---|---|
| 1. 触发 | 同步 | RankingService | 派发异步任务 |
| 2. 聚合积分 | 异步 | RankingCalculationProcessor | SUM(entries_points) GROUP BY player |
| 3. 计算排名 | 异步 | RankingCalculationProcessor | RANK() OVER (ORDER BY total DESC) |
| 4. 更新状态 | 异步 | Worker | Ranking: stale → up_to_date |

### 4.3 计算逻辑

```text
ranking_refresh_task(season_id):
    1. 标记 Ranking status = refreshing
    2. 执行聚合查询：
       SELECT player_id, SUM(points_earned) as total_points
       FROM entries_points
       WHERE season_id = :season_id
       GROUP BY player_id
    3. 计算排名：
       RANK() OVER (ORDER BY total_points DESC)
    4. 排序规则（同积分）：
       total_points DESC,
       player_name_pinyin ASC,
       player_name ASC,
       player_id ASC
    5. 标记 Ranking status = up_to_date
```

### 4.4 MVP 实现策略

MVP 阶段排行榜不使用物化视图或缓存表，每次查询实时计算：

- 数据量预估：选手 < 500 人，赛事 < 50 场，积分记录 < 5000 条。
- 实时聚合查询在此数据量下性能足够（< 100ms）。
- "刷新"操作在 MVP 阶段等同于"清除可能的缓存"，实际查询始终实时。

后续版本（V2）在数据量增长后引入物化视图：

```text
V2 策略：
  积分写入后 → 刷新物化视图 → 查询走物化视图
```

### 4.5 异常恢复

| 异常 | 恢复策略 |
|---|---|
| 聚合查询超时 | 标记失败，管理员重试 |
| 数据不一致 | 记录日志，管理员排查后重试 |

---

## 5. 工作流状态追踪

### 5.1 状态存储方式

| 工作流 | 状态存储位置 | 字段 |
|---|---|---|
| Excel 导入 | uploads 表 | status |
| 积分生成 | tournaments 表 | status（completed → published） |
| 排行榜刷新 | Redis 或内存 | ranking_status（MVP 可简化） |

### 5.2 前端轮询策略

```text
前端发起操作
    ↓
后端返回 202 Accepted + 资源 ID
    ↓
前端每 3 秒请求 GET /resource/{id}
    ↓
检查 status 字段
    ├─ 中间态（parsing / processing / refreshing）→ 继续轮询
    └─ 终态（parsed / imported / published / failed）→ 停止轮询，展示结果
```

---

## 6. 工作流与模块的映射

```text
Excel 导入工作流
├─ API 层：POST /uploads, GET /uploads/{id}, POST /uploads/{id}/confirm
├─ Service 层：UploadService
├─ Processor 层：ExcelParseProcessor, DataValidationProcessor
├─ Repository 层：UploadRepository, EventResultRepository, PlayerRepository
└─ Worker：excel_parse_task

积分生成工作流
├─ API 层：POST /tournaments/{id}/generate-points
├─ Service 层：PointsService, TournamentService
├─ Processor 层：PointsGenerationProcessor
├─ Repository 层：EventResultRepository, PointsRuleRepository, EntriesPointsRepository
└─ Worker：points_generation_task

排行榜刷新工作流
├─ API 层：POST /rankings/refresh, GET /rankings
├─ Service 层：RankingService
├─ Processor 层：RankingCalculationProcessor
├─ Repository 层：EntriesPointsRepository, PlayerRepository
└─ Worker：ranking_refresh_task
```

---

## 7. 工作流间的触发关系

```text
Excel 导入完成（imported）
    ↓
管理员触发积分生成
    ↓
积分生成完成（published）
    ↓
系统自动标记排行榜为 stale
    ↓
管理员触发排行榜刷新（或系统自动刷新）
    ↓
排行榜更新为 up_to_date
    ↓
用户端查询到最新排名
```

MVP 阶段各工作流之间通过管理员手动触发串联。后续版本可实现自动串联：

```text
[V2] 积分生成完成后自动触发排行榜刷新
[V2] Excel 确认导入后自动触发积分生成
```

---

## 8. 并发控制

### 8.1 需要并发控制的场景

| 场景 | 控制方式 |
|---|---|
| 同一赛事同时上传多个 Excel | 检查是否有 parsing 状态的上传，有则拒绝 |
| 同一赛事重复生成积分 | 检查是否已有 entries_points 记录，有则拒绝 |
| 排行榜并发刷新 | 检查是否正在刷新，是则拒绝 |
| 赛季并发激活 | 事务内加锁，确保只有一个 active |

### 8.2 实现方式

MVP 阶段使用数据库状态检查 + 事务隔离实现并发控制，不引入分布式锁：

```text
操作前检查状态 → 状态允许则执行 → 事务内更新状态
```

---

## 9. MVP 工作流能力边界

### 9.1 MVP 实现

| 工作流 | 实现程度 |
|---|---|
| Excel 导入 | 完整实现（标准模板解析） |
| 积分生成 | 完整实现（所有积分类型） |
| 排行榜刷新 | 简化实现（实时查询，刷新 = 清缓存） |

### 9.2 后置能力

| 能力 | 归属版本 |
|---|---|
| AI 辅助 Excel 解析 | V3 |
| 物化视图排行榜 | V2 |
| 自动串联工作流 | V2 |
| 工作流重试队列 | V2 |
| 工作流执行日志 | V2 |
