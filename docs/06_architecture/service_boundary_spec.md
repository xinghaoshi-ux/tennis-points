# Service 边界规范

> 本文定义 THA 年度赛事积分系统后端各 Service 模块的职责边界、输入输出和协作关系。
>
> 本文档是后端开发实施的直接依据。

---

## 1. Service 设计原则

- 每个 Service 对应一个业务领域，职责单一。
- Service 之间不互相调用，避免循环依赖。
- 如果一个操作涉及多个领域，由 API 层按顺序调用多个 Service，或由 Processor 协调。
- Service 控制事务边界，Repository 不自行提交。
- Service 负责业务校验，Repository 只负责数据读写。

---

## 2. AuthService

### 2.1 职责

管理员身份认证和会话管理。

### 2.2 能力清单

| 方法 | 输入 | 输出 | 说明 |
|---|---|---|---|
| login | 用户名、密码 | Token + 用户信息 | 验证凭证，签发 JWT |
| logout | Token | 无 | 使 Token 失效（可选） |
| get_current_user | Token | 用户信息 | 解析并校验 Token |

### 2.3 边界

- 不负责用户 CRUD（MVP 阶段管理员通过种子数据创建）。
- 不负责权限细分（MVP 阶段只有管理员一种角色）。

---

## 3. SeasonService

### 3.1 职责

赛季生命周期管理。

### 3.2 能力清单

| 方法 | 输入 | 输出 | 说明 |
|---|---|---|---|
| list | 分页参数 | 赛季列表 | 查询所有赛季 |
| create | 赛季信息 | 赛季记录 | 创建 draft 赛季 |
| update | 赛季 ID、更新字段 | 赛季记录 | 编辑赛季信息 |
| activate | 赛季 ID | 赛季记录 | 激活赛季（关闭原 active） |
| close | 赛季 ID | 赛季记录 | 关闭赛季 |
| get_current | 无 | 赛季记录或 null | 获取当前 active 赛季 |

### 3.3 业务规则

- 同一时间最多一个 active 赛季。
- 激活新赛季时，原 active 赛季在同一事务内变为 closed。
- closed 赛季不可编辑。
- draft 赛季可删除，active 和 closed 不可删除。

### 3.4 状态迁移

| 当前状态 | 允许操作 | 目标状态 |
|---|---|---|
| draft | activate | active |
| draft | delete | 删除 |
| active | close | closed |
| closed | 无 | 终态 |

---

## 4. PlayerService

### 4.1 职责

选手信息管理。

### 4.2 能力清单

| 方法 | 输入 | 输出 | 说明 |
|---|---|---|---|
| list | 分页、搜索、筛选参数 | 选手列表 | 支持姓名模糊搜索和院系筛选 |
| create | 选手信息 | 选手记录 | 新增选手 |
| update | 选手 ID、更新字段 | 选手记录 | 编辑选手 |
| get | 选手 ID | 选手记录 | 获取单个选手 |
| match_by_name | 姓名 | 选手记录或 null | Excel 导入时匹配选手 |

### 4.3 业务规则

- 姓名不要求唯一（同名选手通过院系和出生日期区分）。
- 不存储积分和排名（衍生数据）。
- 年龄通过 birth_date 动态计算，不存储。

---

## 5. TournamentService

### 5.1 职责

赛事生命周期管理。

### 5.2 能力清单

| 方法 | 输入 | 输出 | 说明 |
|---|---|---|---|
| list | 分页、状态筛选 | 赛事列表 | 查询赛事 |
| create | 赛事信息 | 赛事记录 | 创建 draft 赛事 |
| update | 赛事 ID、更新字段 | 赛事记录 | 编辑赛事 |
| get | 赛事 ID | 赛事记录 | 获取单个赛事 |
| mark_completed | 赛事 ID | 赛事记录 | 标记为已完赛 |
| mark_published | 赛事 ID | 赛事记录 | 标记为已发布 |
| revoke_publish | 赛事 ID | 赛事记录 | 撤回发布 |

### 5.3 业务规则

- 赛事必须关联 active 赛季。
- draft 状态可编辑和删除。
- completed 和 published 状态不可删除。
- 撤回发布时需同时删除关联的 entries_points 记录。

### 5.4 状态迁移

| 当前状态 | 允许操作 | 目标状态 |
|---|---|---|
| draft | mark_completed | completed |
| draft | delete | 删除 |
| completed | mark_published | published |
| published | revoke_publish | completed |

---

## 6. PointsRuleService

### 6.1 职责

积分规则配置管理。

### 6.2 能力清单

| 方法 | 输入 | 输出 | 说明 |
|---|---|---|---|
| list | 赛季 ID、规则类型 | 规则列表 | 按类型分组查询 |
| create | 规则信息 | 规则记录 | 新增规则 |
| update | 规则 ID、更新字段 | 规则记录 | 编辑规则 |
| delete | 规则 ID | 无 | 删除规则 |
| match_rule | 赛季、级别、组别、成绩 | 规则记录或 null | 积分生成时匹配规则 |

### 6.3 业务规则

- 规则关联赛季，不同赛季可有不同规则。
- 同一赛季内，赛事级别 + 组别 + 成绩的组合应唯一。
- 已被 entries_points 引用的规则不可删除（可禁用）。

---

## 7. UploadService

### 7.1 职责

Excel 上传记录管理和导入流程控制。

### 7.2 能力清单

| 方法 | 输入 | 输出 | 说明 |
|---|---|---|---|
| create_upload | 文件、赛事 ID | upload 记录 | 保存文件，创建记录，派发解析任务 |
| get | upload ID | upload 记录 + 预览数据 | 查询上传状态和解析结果 |
| get_preview | upload ID | 预览行列表 | 获取导入预览数据 |
| confirm_import | upload ID、确认行列表 | 导入结果 | 确认导入，写入 event_results |
| cancel | upload ID | upload 记录 | 取消上传 |

### 7.3 业务规则

- 上传时自动派发异步解析任务。
- 确认导入时只导入状态为"正常"的行，忽略被管理员标记忽略的行。
- 确认导入在单一事务内完成（Upload 状态更新 + event_results 写入）。
- 同一赛事不允许同时有多个 parsing 状态的上传。

### 7.4 状态迁移

| 当前状态 | 允许操作 | 目标状态 |
|---|---|---|
| pending | 系统开始解析 | parsing |
| pending | cancel | cancelled |
| parsing | 解析成功 | parsed |
| parsing | 解析失败 | parse_failed |
| parsed | confirm_import | imported |
| parsed | cancel | cancelled |

---

## 8. PointsService

### 8.1 职责

积分生成和积分查询。

### 8.2 能力清单

| 方法 | 输入 | 输出 | 说明 |
|---|---|---|---|
| generate | 赛事 ID | 任务状态 | 触发积分生成异步任务 |
| get_player_points | 选手 ID、赛季 ID | 积分明细列表 | 查询选手积分构成 |
| delete_by_tournament | 赛事 ID | 删除数量 | 撤回发布时删除积分记录 |

### 8.3 业务规则

- 积分生成前校验赛事状态为 completed。
- 积分生成前校验对应积分规则存在。
- 团体赛分摊：round(团队总积分 / 有效队员人数)。
- 单项双打：每名搭档获得完整名次积分。
- 生成完成后自动更新赛事状态为 published。

---

## 9. RankingService

### 9.1 职责

排行榜查询和刷新。

### 9.2 能力清单

| 方法 | 输入 | 输出 | 说明 |
|---|---|---|---|
| get_rankings | 赛季 ID、分页、搜索、筛选 | 排行榜列表 | 查询排行榜 |
| refresh | 赛季 ID | 任务状态 | 触发排行榜刷新异步任务 |
| get_status | 赛季 ID | 排行榜状态 | 查询是否最新 |

### 9.3 业务规则

- 排行榜基于 entries_points 动态计算。
- 排名使用 RANK() 窗口函数，同积分并列。
- 同积分展示顺序：姓名首字母 ASC → 姓名 ASC → player_id ASC。
- MVP 阶段每次查询实时计算（数据量小），不使用物化视图。

---

## 10. Service 间协作关系

Service 之间不直接调用。跨领域操作通过以下方式协调：

### 10.1 API 层顺序调用

简单的跨领域操作由 API 层按顺序调用多个 Service：

```text
撤回发布：
  API 层调用 PointsService.delete_by_tournament(tournament_id)
  API 层调用 TournamentService.revoke_publish(tournament_id)
```

### 10.2 异步任务内协调

复杂流程在异步任务内按步骤调用多个 Service/Processor：

```text
积分生成任务：
  PointsGenerationProcessor.generate()  → 计算并写入积分
  TournamentService.mark_published()    → 更新赛事状态
  RankingService（标记 stale）           → 标记排行榜待刷新
```

### 10.3 依赖关系图

```text
UploadService ──→ ExcelParseProcessor ──→ PlayerRepository
                                      ──→ TournamentRepository

PointsService ──→ PointsGenerationProcessor ──→ PointsRuleRepository
                                             ──→ EventResultRepository
                                             ──→ EntriesPointsRepository

RankingService ──→ RankingCalculationProcessor ──→ EntriesPointsRepository
                                               ──→ PlayerRepository
```
