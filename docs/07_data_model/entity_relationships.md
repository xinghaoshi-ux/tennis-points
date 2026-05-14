# 实体关系设计

> 本文定义 THA 年度赛事积分系统核心实体之间的关系，包括关系类型、外键方向和业务约束。

---

## 1. 实体关系总览

```text
Season ──1:N──→ Tournament
Season ──1:N──→ PointsRule
Season ──1:N──→ EntriesPoints

Player ──1:N──→ EntriesPoints
Player ──1:N──→ TeamMember
Player ──M:N──→ EventResult（通过 EventResultPlayer）

Tournament ──1:N──→ EventResult
Tournament ──1:N──→ EntriesPoints
Tournament ──1:N──→ Upload
Tournament ──1:N──→ TeamMember

EventResult ──1:N──→ EventResultPlayer
EventResult ──1:N──→ EntriesPoints
EventResult ──N:1──→ Team（团体赛时）

Team ──1:N──→ TeamMember
Team ──1:N──→ EventResult（团体赛时）
Team ──1:N──→ EntriesPoints（团体赛时）

User ──1:N──→ Upload（上传人）
```

---

## 2. 关系详细说明

### 2.1 Season → Tournament（一对多）

| 维度 | 说明 |
|---|---|
| 关系 | 一个赛季包含多个赛事 |
| 外键 | Tournament.season_id → Season.id |
| 约束 | 赛事必须归属于一个赛季 |
| 业务规则 | 只有 active 赛季下才能创建赛事 |
| 级联行为 | 赛季关闭后，其下赛事不可新增 |

### 2.2 Season → PointsRule（一对多）

| 维度 | 说明 |
|---|---|
| 关系 | 一个赛季有一套积分规则 |
| 外键 | PointsRule.season_id → Season.id |
| 约束 | 规则必须归属于一个赛季 |
| 业务规则 | 不同赛季可有不同规则配置 |

### 2.3 Season → EntriesPoints（一对多）

| 维度 | 说明 |
|---|---|
| 关系 | 一个赛季包含所有该赛季的积分记录 |
| 外键 | EntriesPoints.season_id → Season.id |
| 约束 | 积分记录必须归属于一个赛季 |
| 业务规则 | 排行榜按赛季聚合 |

### 2.4 Tournament → EventResult（一对多）

| 维度 | 说明 |
|---|---|
| 关系 | 一个赛事有多条赛事结果 |
| 外键 | EventResult.tournament_id → Tournament.id |
| 约束 | 赛事结果必须归属于一个赛事 |
| 业务规则 | 一个赛事可能有冠军、亚军、前四名等多条结果 |

### 2.5 Tournament → Upload（一对多）

| 维度 | 说明 |
|---|---|
| 关系 | 一个赛事可能有多次上传记录 |
| 外键 | Upload.tournament_id → Tournament.id |
| 约束 | 上传必须关联一个赛事 |
| 业务规则 | 失败后可重新上传，产生新记录 |

### 2.6 EventResult → EventResultPlayer（一对多）

| 维度 | 说明 |
|---|---|
| 关系 | 一条赛事结果对应多名选手（双打 2 人） |
| 外键 | EventResultPlayer.event_result_id → EventResult.id |
| 约束 | 单项双打赛每条结果应有 2 名选手 |
| 业务规则 | 代表队赛事每条结果对应 1 名选手 |

### 2.7 Player ↔ EventResult（多对多，通过 EventResultPlayer）

| 维度 | 说明 |
|---|---|
| 关系 | 一名选手可参加多个赛事结果，一条结果可包含多名选手 |
| 中间表 | EventResultPlayer |
| 业务规则 | 通过中间表实现双打组合和代表队参赛的选手关联 |

### 2.8 Player → EntriesPoints（一对多）

| 维度 | 说明 |
|---|---|
| 关系 | 一名选手有多条积分记录 |
| 外键 | EntriesPoints.player_id → Player.id |
| 约束 | 积分记录必须归属于一名选手 |
| 业务规则 | 排行榜按选手聚合积分 |

### 2.9 Tournament → EntriesPoints（一对多）

| 维度 | 说明 |
|---|---|
| 关系 | 一个赛事产生多条积分记录 |
| 外键 | EntriesPoints.tournament_id → Tournament.id |
| 约束 | 积分记录必须关联来源赛事 |
| 业务规则 | 撤回发布时按 tournament_id 删除积分记录 |

### 2.10 Team → TeamMember（一对多）

| 维度 | 说明 |
|---|---|
| 关系 | 一个团体有多名队员 |
| 外键 | TeamMember.team_id → Team.id |
| 约束 | 队员必须归属于一个团体 |
| 业务规则 | is_active=true 的队员参与积分分摊 |

### 2.11 Team → EventResult（一对多，团体赛）

| 维度 | 说明 |
|---|---|
| 关系 | 一个团体在团体赛中有一条赛事结果 |
| 外键 | EventResult.team_id → Team.id |
| 约束 | 仅团体赛时使用 |
| 业务规则 | 团体赛结果关联团队，积分按队员分摊 |

---

## 3. 关系图

```text
┌──────────┐       ┌──────────────┐       ┌──────────────────┐
│  Season  │──1:N─→│  Tournament  │──1:N─→│   EventResult    │
│          │       │              │       │                  │
│          │──1:N─→│  PointsRule  │       │  team_id (FK)────┼──→ Team
│          │       └──────────────┘       └────────┬─────────┘
│          │              │                        │
│          │              │ 1:N                    │ 1:N
│          │              ↓                        ↓
│          │       ┌──────────────┐       ┌──────────────────┐
│          │       │    Upload    │       │EventResultPlayer │
│          │       └──────────────┘       │                  │
│          │                              │  player_id (FK)──┼──→ Player
│          │                              └──────────────────┘
│          │
│          │──1:N─→┌──────────────────┐
└──────────┘       │  EntriesPoints   │
                   │                  │
                   │  player_id (FK)──┼──→ Player
                   │  tournament_id───┼──→ Tournament
                   │  team_id (FK)────┼──→ Team (可选)
                   └──────────────────┘

┌──────────┐       ┌──────────────┐
│   Team   │──1:N─→│  TeamMember  │
│          │       │              │
│          │       │  player_id───┼──→ Player
│          │       │  tournament──┼──→ Tournament
└──────────┘       └──────────────┘

┌──────────┐
│   User   │──1:N─→ Upload.uploaded_by
└──────────┘
```

---

## 4. 索引建议

| 表 | 索引字段 | 类型 | 用途 |
|---|---|---|---|
| entries_points | (season_id, player_id) | 复合索引 | 排行榜聚合查询 |
| entries_points | (tournament_id) | 单字段索引 | 按赛事查询积分 |
| entries_points | (player_id, season_id) | 复合索引 | 选手积分明细查询 |
| event_results | (tournament_id) | 单字段索引 | 按赛事查询结果 |
| event_result_players | (event_result_id) | 单字段索引 | 关联查询 |
| event_result_players | (player_id) | 单字段索引 | 按选手查询参赛记录 |
| tournaments | (season_id, status) | 复合索引 | 按赛季和状态筛选 |
| players | (full_name) | 单字段索引 | 姓名搜索 |
| players | (department) | 单字段索引 | 院系筛选 |
| team_members | (team_id, tournament_id) | 复合索引 | 查询某赛事某团队队员 |
| uploads | (tournament_id) | 单字段索引 | 按赛事查询上传记录 |

---

## 5. 数据完整性约束

| 约束 | 说明 |
|---|---|
| 赛季唯一激活 | 同一时间 status=active 的 Season 最多一条 |
| 积分规则唯一 | 同一赛季内 (rule_type, event_level, group_name, result_type) 组合唯一 |
| 团体队员唯一 | 同一赛事同一团体内 (team_id, player_id, tournament_id) 唯一 |
| 赛事结果选手唯一 | 同一赛事结果内 (event_result_id, player_id) 唯一 |
| 外键完整性 | 所有外键字段引用的记录必须存在 |
