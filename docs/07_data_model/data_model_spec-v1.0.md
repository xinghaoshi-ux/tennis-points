# 数据模型规范 v1.0

> 本文定义 THA 年度赛事积分系统 MVP 阶段的核心数据模型，包括实体识别、字段设计、状态定义和 API 支撑说明。
>
> 本文档是数据库表设计、API 规范设计和前端数据展示的共同依据。

---

## 1. 核心实体清单

| 编号 | 实体 | 英文名 | 业务含义 |
|---|---|---|---|
| E-01 | 赛季 | Season | 年度积分统计周期，所有积分归属于某个赛季 |
| E-02 | 选手 | Player | 参赛校友，积分和排名的主体 |
| E-03 | 赛事 | Tournament | 一次具体的比赛活动，积分来源的载体 |
| E-04 | 赛事结果 | EventResult | 某次赛事中某个成绩的事实记录 |
| E-05 | 积分记录 | EntriesPoints | 某位选手在某次赛事中获得的具体积分 |
| E-06 | 积分规则 | PointsRule | 不同赛事级别、组别、成绩对应的积分配置 |
| E-07 | 团体 | Team | 团体赛中的参赛队伍 |
| E-08 | 团体队员 | TeamMember | 某个团体在某次赛事中的队员名单 |
| E-09 | 上传记录 | Upload | 一次 Excel 文件上传及其处理状态 |
| E-10 | 管理员 | User | 系统管理员账号 |

---

## 2. 实体详细设计

### 2.1 Season（赛季）

业务含义：年度积分统计的时间周期。系统内同一时间只有一个激活赛季，所有积分计算和排行榜展示基于当前激活赛季。

| 字段名 | 含义 | 类型 | 必填 | 示例值 | 前端展示 | 后端持久化 | 内部字段 |
|---|---|---|---|---|---|---|---|
| id | 赛季唯一标识 | INTEGER (PK) | 是 | 1 | 否 | 是 | 否 |
| name | 赛季名称 | VARCHAR(100) | 是 | 2026-2027 THA 赛季 | 是 | 是 | 否 |
| start_date | 赛季开始日期 | DATE | 是 | 2026-04-20 | 是 | 是 | 否 |
| end_date | 赛季结束日期 | DATE | 是 | 2027-04-20 | 是 | 是 | 否 |
| status | 赛季状态 | VARCHAR(20) | 是 | active | 是 | 是 | 否 |
| created_at | 创建时间 | TIMESTAMP | 是 | 2026-03-01 10:00:00 | 否 | 是 | 是 |
| updated_at | 更新时间 | TIMESTAMP | 否 | 2026-03-15 14:00:00 | 否 | 是 | 是 |

状态定义：

| 状态值 | 含义 | 进入条件 | 可执行操作 |
|---|---|---|---|
| draft | 草稿，未生效 | 创建赛季 | 编辑、删除、激活 |
| active | 当前有效赛季 | 管理员激活 | 编辑、关闭 |
| closed | 已关闭，数据冻结 | 管理员关闭或新赛季激活 | 仅查看 |

---

### 2.2 Player（选手）

业务含义：参赛校友的基础信息。选手是积分和排名的主体。不存储积分和排名（衍生数据动态计算）。

| 字段名 | 含义 | 类型 | 必填 | 示例值 | 前端展示 | 后端持久化 | 内部字段 |
|---|---|---|---|---|---|---|---|
| id | 选手唯一标识 | INTEGER (PK) | 是 | 42 | 否 | 是 | 否 |
| full_name | 姓名 | VARCHAR(50) | 是 | 张三 | 是 | 是 | 否 |
| gender | 性别 | VARCHAR(10) | 否 | male | 否 | 是 | 否 |
| birth_date | 出生日期 | DATE | 否 | 1988-05-12 | 否（展示年龄） | 是 | 否 |
| department | 院系/部门 | VARCHAR(100) | 否 | 计算机系 | 是 | 是 | 否 |
| phone | 联系电话 | VARCHAR(20) | 否 | 138xxxx1234 | 否 | 是 | 是 |
| status | 选手状态 | VARCHAR(20) | 是 | active | 否 | 是 | 是 |
| created_at | 创建时间 | TIMESTAMP | 是 | 2026-04-01 09:00:00 | 否 | 是 | 是 |
| updated_at | 更新时间 | TIMESTAMP | 否 | — | 否 | 是 | 是 |

说明：
- 年龄通过 birth_date 动态计算，不存储。
- 排行榜中展示的"年龄"由后端在查询时计算后返回。
- phone 为内部管理字段，不在公共接口暴露。

---

### 2.3 Tournament（赛事）

业务含义：一次具体的比赛活动。赛事是积分来源的载体，管理员创建赛事后上传结果。

| 字段名 | 含义 | 类型 | 必填 | 示例值 | 前端展示 | 后端持久化 | 内部字段 |
|---|---|---|---|---|---|---|---|
| id | 赛事唯一标识 | INTEGER (PK) | 是 | 5 | 否 | 是 | 否 |
| season_id | 所属赛季 | INTEGER (FK) | 是 | 1 | 否 | 是 | 否 |
| name | 赛事名称 | VARCHAR(200) | 是 | THA500 成都站 | 是 | 是 | 否 |
| event_category | 赛事分类 | VARCHAR(50) | 是 | individual_doubles | 是 | 是 | 否 |
| level | 赛事级别 | VARCHAR(20) | 是 | THA500 | 是 | 是 | 否 |
| group_name | 组别 | VARCHAR(50) | 否 | 甲组 | 是 | 是 | 否 |
| start_date | 开始日期 | DATE | 否 | 2026-08-15 | 是 | 是 | 否 |
| end_date | 结束日期 | DATE | 否 | 2026-08-17 | 是 | 是 | 否 |
| location | 办赛地点 | VARCHAR(200) | 否 | 成都 | 是 | 是 | 否 |
| alumni_player_count | 校友参赛人数 | INTEGER | 否 | 35 | 否 | 是 | 否 |
| status | 赛事状态 | VARCHAR(20) | 是 | draft | 是 | 是 | 否 |
| created_at | 创建时间 | TIMESTAMP | 是 | — | 否 | 是 | 是 |
| updated_at | 更新时间 | TIMESTAMP | 否 | — | 否 | 是 | 是 |

event_category 取值：

| 值 | 含义 |
|---|---|
| individual_doubles | 单项双打赛 |
| team | 团体赛 |
| representative | 代表队赛事 |
| bonus | 奖励积分（办赛/捐赠） |

level 取值：

| 值 | 含义 |
|---|---|
| THA1000 | 校庆总决赛 |
| THA800 | 高级别分站赛 |
| THA500 | 标准分站赛 |
| THA200 | 卫星赛 |
| THA_S | S 级团体赛 |
| THA_A | A 级团体赛 |
| THA_B | B 级团体赛 |
| representative | 代表队赛事 |
| bonus | 奖励积分 |

状态定义：

| 状态值 | 含义 | 进入条件 | 可执行操作 |
|---|---|---|---|
| draft | 草稿，可编辑 | 创建赛事 | 编辑、删除、上传结果 |
| completed | 已完赛，结果已导入 | 确认导入赛事结果 | 生成积分、修正数据 |
| published | 已发布，积分已生成 | 积分生成完成 | 查看、撤回发布 |

---

### 2.4 EventResult（赛事结果）

业务含义：某次赛事中某个成绩的事实记录。系统第一版只记录最终成绩（冠军/亚军/前四名等），不记录逐场比分。

| 字段名 | 含义 | 类型 | 必填 | 示例值 | 前端展示 | 后端持久化 | 内部字段 |
|---|---|---|---|---|---|---|---|
| id | 结果记录唯一标识 | INTEGER (PK) | 是 | 101 | 否 | 是 | 否 |
| tournament_id | 所属赛事 | INTEGER (FK) | 是 | 5 | 否 | 是 | 否 |
| result_type | 成绩类型（枚举） | VARCHAR(30) | 是 | champion | 是 | 是 | 否 |
| team_id | 团体赛团队 ID | INTEGER (FK) | 否 | 3 | 否 | 是 | 否 |
| team_total_points | 团体赛团队总积分 | INTEGER | 否 | 1800 | 是 | 是 | 否 |
| team_member_count | 团体赛有效队员人数 | INTEGER | 否 | 8 | 否 | 是 | 否 |
| is_cross_province | 是否跨省参赛 | BOOLEAN | 否 | true | 是 | 是 | 否 |
| is_cross_border | 是否跨境参赛 | BOOLEAN | 否 | false | 是 | 是 | 否 |
| upload_id | 来源上传记录 | INTEGER (FK) | 否 | 10 | 否 | 是 | 是 |
| created_at | 创建时间 | TIMESTAMP | 是 | — | 否 | 是 | 是 |

result_type 取值：

| 值 | 含义 |
|---|---|
| champion | 冠军 |
| runner_up | 亚军 |
| semifinal | 前四名 |
| quarterfinal | 前八名 |
| participant | 参赛 |

说明：
- 单项双打赛的选手通过关联表 event_result_players 记录。
- 团体赛的队员通过 team_members 表记录。
- 一条 EventResult 可能对应多名选手（双打组合）。

---

### 2.5 EventResultPlayer（赛事结果-选手关联）

业务含义：记录某条赛事结果对应的选手。单项双打赛一条结果对应 2 名选手，代表队赛事对应 1 名选手。

| 字段名 | 含义 | 类型 | 必填 | 示例值 | 前端展示 | 后端持久化 | 内部字段 |
|---|---|---|---|---|---|---|---|
| id | 唯一标识 | INTEGER (PK) | 是 | 201 | 否 | 是 | 是 |
| event_result_id | 赛事结果 ID | INTEGER (FK) | 是 | 101 | 否 | 是 | 否 |
| player_id | 选手 ID | INTEGER (FK) | 是 | 42 | 否 | 是 | 否 |

---

### 2.6 EntriesPoints（积分记录）

业务含义：某位选手在某次赛事中获得的具体积分。排行榜基于此表动态聚合计算。这是系统最核心的事实数据表。

| 字段名 | 含义 | 类型 | 必填 | 示例值 | 前端展示 | 后端持久化 | 内部字段 |
|---|---|---|---|---|---|---|---|
| id | 积分记录唯一标识 | INTEGER (PK) | 是 | 301 | 否 | 是 | 否 |
| player_id | 选手 ID | INTEGER (FK) | 是 | 42 | 是 | 是 | 否 |
| tournament_id | 赛事 ID | INTEGER (FK) | 是 | 5 | 是 | 是 | 否 |
| season_id | 赛季 ID | INTEGER (FK) | 是 | 1 | 否 | 是 | 否 |
| source_type | 积分来源类型 | VARCHAR(30) | 是 | individual_event | 是 | 是 | 否 |
| points_earned | 获得积分 | INTEGER | 是 | 500 | 是 | 是 | 否 |
| result_type | 成绩类型 | VARCHAR(30) | 否 | champion | 是 | 是 | 否 |
| description | 积分来源说明 | VARCHAR(500) | 否 | THA500 成都站 甲组 冠军 | 是 | 是 | 否 |
| team_id | 团体赛团队 ID | INTEGER (FK) | 否 | 3 | 是 | 是 | 否 |
| team_total_points | 团体赛团队总积分 | INTEGER | 否 | 1800 | 是 | 是 | 否 |
| team_member_count | 团体赛分摊人数 | INTEGER | 否 | 8 | 是 | 是 | 否 |
| event_result_id | 来源赛事结果 ID | INTEGER (FK) | 否 | 101 | 否 | 是 | 是 |
| created_at | 创建时间 | TIMESTAMP | 是 | — | 否 | 是 | 是 |

source_type 取值：

| 值 | 含义 | 说明 |
|---|---|---|
| individual_event | 单项赛事积分 | 双打每人获得完整积分 |
| team_share | 团体赛分摊积分 | round(团队总积分/有效队员数) |
| travel_bonus | 远程参赛奖补 | 跨省 200 / 跨境 500 |
| representative_team | 代表队参赛积分 | 胜场 40 + 负场 20 + 基础 20 |
| organizer_bonus | 办赛奖励积分 | 按承办赛事级别 |
| donation_bonus | 捐赠赞助积分 | 等值 10000 元 = 200 分 |

---

### 2.7 PointsRule（积分规则）

业务含义：配置不同赛事级别、组别、成绩对应的积分值。积分生成时根据此表匹配规则。

| 字段名 | 含义 | 类型 | 必填 | 示例值 | 前端展示 | 后端持久化 | 内部字段 |
|---|---|---|---|---|---|---|---|
| id | 规则唯一标识 | INTEGER (PK) | 是 | 1 | 否 | 是 | 否 |
| season_id | 所属赛季 | INTEGER (FK) | 是 | 1 | 否 | 是 | 否 |
| rule_type | 规则类型 | VARCHAR(30) | 是 | individual_event | 是 | 是 | 否 |
| event_level | 赛事级别 | VARCHAR(20) | 否 | THA500 | 是 | 是 | 否 |
| group_name | 组别 | VARCHAR(50) | 否 | 甲组 | 是 | 是 | 否 |
| result_type | 成绩类型 | VARCHAR(30) | 否 | champion | 是 | 是 | 否 |
| points | 积分值 | INTEGER | 是 | 500 | 是 | 是 | 否 |
| enabled | 是否启用 | BOOLEAN | 是 | true | 是 | 是 | 否 |
| created_at | 创建时间 | TIMESTAMP | 是 | — | 否 | 是 | 是 |

rule_type 取值与 source_type 一致：individual_event / team_event / travel_bonus / representative_team / organizer_bonus / donation_bonus。

---

### 2.8 Team（团体）

业务含义：团体赛中的参赛队伍。团体可代表院系、班级、俱乐部等。

| 字段名 | 含义 | 类型 | 必填 | 示例值 | 前端展示 | 后端持久化 | 内部字段 |
|---|---|---|---|---|---|---|---|
| id | 团体唯一标识 | INTEGER (PK) | 是 | 3 | 否 | 是 | 否 |
| name | 团体名称 | VARCHAR(100) | 是 | 计算机学院队 | 是 | 是 | 否 |
| department | 所属院系/部门 | VARCHAR(100) | 否 | 计算机系 | 是 | 是 | 否 |
| created_at | 创建时间 | TIMESTAMP | 是 | — | 否 | 是 | 是 |

---

### 2.9 TeamMember（团体队员）

业务含义：某个团体在某次赛事中的队员名单，用于团体赛积分分摊计算。

| 字段名 | 含义 | 类型 | 必填 | 示例值 | 前端展示 | 后端持久化 | 内部字段 |
|---|---|---|---|---|---|---|---|
| id | 唯一标识 | INTEGER (PK) | 是 | 401 | 否 | 是 | 是 |
| team_id | 团体 ID | INTEGER (FK) | 是 | 3 | 否 | 是 | 否 |
| player_id | 队员 ID | INTEGER (FK) | 是 | 42 | 是 | 是 | 否 |
| tournament_id | 所属赛事 ID | INTEGER (FK) | 是 | 5 | 否 | 是 | 否 |
| is_active | 是否为有效分摊队员 | BOOLEAN | 是 | true | 否 | 是 | 否 |
| created_at | 创建时间 | TIMESTAMP | 是 | — | 否 | 是 | 是 |

---

### 2.10 Upload（上传记录）

业务含义：一次 Excel 文件上传及其处理全过程的状态追踪。

| 字段名 | 含义 | 类型 | 必填 | 示例值 | 前端展示 | 后端持久化 | 内部字段 |
|---|---|---|---|---|---|---|---|
| id | 上传唯一标识 | INTEGER (PK) | 是 | 10 | 否 | 是 | 否 |
| tournament_id | 关联赛事 | INTEGER (FK) | 是 | 5 | 是 | 是 | 否 |
| filename | 原始文件名 | VARCHAR(255) | 是 | THA500成都站结果.xlsx | 是 | 是 | 否 |
| file_path | 服务器存储路径 | VARCHAR(500) | 是 | /uploads/2026/08/xxx.xlsx | 否 | 是 | 是 |
| status | 上传处理状态 | VARCHAR(20) | 是 | parsed | 是 | 是 | 否 |
| total_rows | 总数据行数 | INTEGER | 否 | 12 | 是 | 是 | 否 |
| valid_rows | 正常行数 | INTEGER | 否 | 10 | 是 | 是 | 否 |
| error_rows | 异常行数 | INTEGER | 否 | 2 | 是 | 是 | 否 |
| error_log | 错误信息 | TEXT | 否 | 第3行：选手未匹配 | 是 | 是 | 否 |
| preview_data | 解析预览数据（JSON） | JSONB | 否 | [...] | 是 | 是 | 是 |
| uploaded_by | 上传人 ID | INTEGER (FK) | 是 | 1 | 否 | 是 | 是 |
| created_at | 上传时间 | TIMESTAMP | 是 | — | 是 | 是 | 否 |

状态定义：

| 状态值 | 含义 | 进入条件 |
|---|---|---|
| pending | 待处理，文件已上传 | 文件上传成功 |
| parsing | 解析中 | 异步任务开始执行 |
| parsed | 已解析，等待确认 | 解析任务成功完成 |
| parse_failed | 解析失败 | 解析任务出错 |
| imported | 已导入 | 管理员确认导入 |
| cancelled | 已取消 | 管理员取消 |

---

### 2.11 User（管理员）

业务含义：系统管理员账号。MVP 阶段只有管理员角色，无普通用户账号。

| 字段名 | 含义 | 类型 | 必填 | 示例值 | 前端展示 | 后端持久化 | 内部字段 |
|---|---|---|---|---|---|---|---|
| id | 管理员唯一标识 | INTEGER (PK) | 是 | 1 | 否 | 是 | 否 |
| username | 用户名 | VARCHAR(50) | 是 | admin | 是 | 是 | 否 |
| password_hash | 密码哈希 | VARCHAR(255) | 是 | $2b$12$... | 否 | 是 | 是 |
| display_name | 显示名称 | VARCHAR(50) | 否 | 管理员 | 是 | 是 | 否 |
| is_active | 是否启用 | BOOLEAN | 是 | true | 否 | 是 | 是 |
| created_at | 创建时间 | TIMESTAMP | 是 | — | 否 | 是 | 是 |

---

## 3. 状态字段汇总

| 实体 | 字段 | 可选值 | 状态流转 |
|---|---|---|---|
| Season | status | draft → active → closed | draft→active→closed |
| Tournament | status | draft → completed → published | draft→completed→published（可撤回到 completed） |
| Upload | status | pending → parsing → parsed → imported | pending→parsing→parsed→imported（或 parse_failed / cancelled） |

---

## 4. 数据模型对 API 的支撑

### 4.1 公共接口数据来源

| 接口 | 数据来源 |
|---|---|
| GET /public/seasons/current | Season（status=active） |
| GET /public/rankings | EntriesPoints 聚合 + Player 关联 |
| GET /public/players/{id}/points | EntriesPoints + Tournament + Team |
| GET /public/departments | Player.department 去重 |

### 4.2 管理接口数据来源

| 接口 | 数据来源 |
|---|---|
| CRUD /admin/seasons | Season |
| CRUD /admin/players | Player |
| CRUD /admin/tournaments | Tournament |
| CRUD /admin/points-rules | PointsRule |
| POST /admin/uploads | Upload + 文件系统 |
| GET /admin/uploads/{id}/preview | Upload.preview_data |
| POST /admin/uploads/{id}/confirm | Upload → EventResult + EventResultPlayer |
| POST /admin/tournaments/{id}/generate-points | EventResult + PointsRule → EntriesPoints |
| POST /admin/rankings/refresh | EntriesPoints 聚合计算 |

### 4.3 排行榜查询模型

排行榜不是独立实体，而是基于 EntriesPoints 的动态聚合：

```text
SELECT
  player_id,
  SUM(points_earned) AS total_points,
  COUNT(DISTINCT tournament_id) AS tournament_count,
  RANK() OVER (ORDER BY SUM(points_earned) DESC) AS ranking
FROM entries_points
WHERE season_id = :current_season_id
GROUP BY player_id
```

关联 Player 表获取姓名、院系、出生日期（计算年龄）。
