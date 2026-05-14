# 字段字典

> 本文汇总 THA 年度赛事积分系统所有实体的字段定义，作为后端数据库设计、API 响应设计和前端数据展示的统一参考。
>
> 每个字段标注其用途分类：前端展示 / 后端持久化 / 内部处理。

---

## 1. 字段用途分类说明

| 分类 | 含义 | 示例 |
|---|---|---|
| 前端展示 | 需要在用户端或管理端页面上展示 | 选手姓名、赛事名称、积分值 |
| 后端持久化 | 需要存储到数据库 | 所有字段都需要持久化 |
| 内部处理 | 仅后端内部使用，不在 API 响应中暴露 | 密码哈希、文件存储路径 |

---

## 2. Season（赛季）

| # | 字段名 | 中文含义 | 类型 | 必填 | 默认值 | 示例 | 展示 | 持久化 | 内部 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | id | 赛季 ID | INTEGER | 是 | 自增 | 1 | — | 是 | — |
| 2 | name | 赛季名称 | VARCHAR(100) | 是 | — | 2026-2027 THA 赛季 | 是 | 是 | — |
| 3 | start_date | 开始日期 | DATE | 是 | — | 2026-04-20 | 是 | 是 | — |
| 4 | end_date | 结束日期 | DATE | 是 | — | 2027-04-20 | 是 | 是 | — |
| 5 | status | 状态 | VARCHAR(20) | 是 | draft | active | 是 | 是 | — |
| 6 | created_at | 创建时间 | TIMESTAMP | 是 | now() | — | — | 是 | 是 |
| 7 | updated_at | 更新时间 | TIMESTAMP | 否 | — | — | — | 是 | 是 |

---

## 3. Player（选手）

| # | 字段名 | 中文含义 | 类型 | 必填 | 默认值 | 示例 | 展示 | 持久化 | 内部 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | id | 选手 ID | INTEGER | 是 | 自增 | 42 | — | 是 | — |
| 2 | full_name | 姓名 | VARCHAR(50) | 是 | — | 张三 | 是 | 是 | — |
| 3 | gender | 性别 | VARCHAR(10) | 否 | — | male | — | 是 | — |
| 4 | birth_date | 出生日期 | DATE | 否 | — | 1988-05-12 | — | 是 | — |
| 5 | department | 院系 | VARCHAR(100) | 否 | — | 计算机系 | 是 | 是 | — |
| 6 | phone | 联系电话 | VARCHAR(20) | 否 | — | 138xxxx1234 | — | 是 | 是 |
| 7 | status | 状态 | VARCHAR(20) | 是 | active | active | — | 是 | 是 |
| 8 | created_at | 创建时间 | TIMESTAMP | 是 | now() | — | — | 是 | 是 |
| 9 | updated_at | 更新时间 | TIMESTAMP | 否 | — | — | — | 是 | 是 |

衍生字段（API 响应中计算返回，不存储）：

| 字段名 | 中文含义 | 计算方式 | 展示 |
|---|---|---|---|
| age | 年龄 | 当前日期 - birth_date | 是 |
| total_points | 年度总积分 | SUM(entries_points.points_earned) | 是 |
| ranking | 当前排名 | RANK() 窗口函数 | 是 |
| tournament_count | 参赛数量 | COUNT(DISTINCT tournament_id) | 是 |

---

## 4. Tournament（赛事）

| # | 字段名 | 中文含义 | 类型 | 必填 | 默认值 | 示例 | 展示 | 持久化 | 内部 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | id | 赛事 ID | INTEGER | 是 | 自增 | 5 | — | 是 | — |
| 2 | season_id | 所属赛季 | INTEGER | 是 | — | 1 | — | 是 | — |
| 3 | name | 赛事名称 | VARCHAR(200) | 是 | — | THA500 成都站 | 是 | 是 | — |
| 4 | event_category | 赛事分类 | VARCHAR(50) | 是 | — | individual_doubles | 是 | 是 | — |
| 5 | level | 赛事级别 | VARCHAR(20) | 是 | — | THA500 | 是 | 是 | — |
| 6 | group_name | 组别 | VARCHAR(50) | 否 | — | 甲组 | 是 | 是 | — |
| 7 | start_date | 开始日期 | DATE | 否 | — | 2026-08-15 | 是 | 是 | — |
| 8 | end_date | 结束日期 | DATE | 否 | — | 2026-08-17 | 是 | 是 | — |
| 9 | location | 办赛地点 | VARCHAR(200) | 否 | — | 成都 | 是 | 是 | — |
| 10 | alumni_player_count | 校友参赛人数 | INTEGER | 否 | — | 35 | — | 是 | — |
| 11 | status | 状态 | VARCHAR(20) | 是 | draft | draft | 是 | 是 | — |
| 12 | created_at | 创建时间 | TIMESTAMP | 是 | now() | — | — | 是 | 是 |
| 13 | updated_at | 更新时间 | TIMESTAMP | 否 | — | — | — | 是 | 是 |

---

## 5. EventResult（赛事结果）

| # | 字段名 | 中文含义 | 类型 | 必填 | 默认值 | 示例 | 展示 | 持久化 | 内部 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | id | 结果 ID | INTEGER | 是 | 自增 | 101 | — | 是 | — |
| 2 | tournament_id | 所属赛事 | INTEGER | 是 | — | 5 | — | 是 | — |
| 3 | result_type | 成绩类型 | VARCHAR(30) | 是 | — | champion | 是 | 是 | — |
| 4 | team_id | 团体 ID | INTEGER | 否 | — | 3 | — | 是 | — |
| 5 | team_total_points | 团队总积分 | INTEGER | 否 | — | 1800 | 是 | 是 | — |
| 6 | team_member_count | 有效队员人数 | INTEGER | 否 | — | 8 | — | 是 | — |
| 7 | is_cross_province | 跨省参赛 | BOOLEAN | 否 | false | true | 是 | 是 | — |
| 8 | is_cross_border | 跨境参赛 | BOOLEAN | 否 | false | false | 是 | 是 | — |
| 9 | upload_id | 来源上传 | INTEGER | 否 | — | 10 | — | 是 | 是 |
| 10 | created_at | 创建时间 | TIMESTAMP | 是 | now() | — | — | 是 | 是 |

---

## 6. EventResultPlayer（赛事结果-选手关联）

| # | 字段名 | 中文含义 | 类型 | 必填 | 默认值 | 示例 | 展示 | 持久化 | 内部 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | id | 关联 ID | INTEGER | 是 | 自增 | 201 | — | 是 | 是 |
| 2 | event_result_id | 赛事结果 ID | INTEGER | 是 | — | 101 | — | 是 | — |
| 3 | player_id | 选手 ID | INTEGER | 是 | — | 42 | — | 是 | — |

---

## 7. EntriesPoints（积分记录）

| # | 字段名 | 中文含义 | 类型 | 必填 | 默认值 | 示例 | 展示 | 持久化 | 内部 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | id | 积分记录 ID | INTEGER | 是 | 自增 | 301 | — | 是 | — |
| 2 | player_id | 选手 ID | INTEGER | 是 | — | 42 | 是 | 是 | — |
| 3 | tournament_id | 赛事 ID | INTEGER | 是 | — | 5 | 是 | 是 | — |
| 4 | season_id | 赛季 ID | INTEGER | 是 | — | 1 | — | 是 | — |
| 5 | source_type | 积分来源类型 | VARCHAR(30) | 是 | — | individual_event | 是 | 是 | — |
| 6 | points_earned | 获得积分 | INTEGER | 是 | — | 500 | 是 | 是 | — |
| 7 | result_type | 成绩类型 | VARCHAR(30) | 否 | — | champion | 是 | 是 | — |
| 8 | description | 来源说明 | VARCHAR(500) | 否 | — | THA500 成都站 甲组 冠军 | 是 | 是 | — |
| 9 | team_id | 团体 ID | INTEGER | 否 | — | 3 | 是 | 是 | — |
| 10 | team_total_points | 团队总积分 | INTEGER | 否 | — | 1800 | 是 | 是 | — |
| 11 | team_member_count | 分摊人数 | INTEGER | 否 | — | 8 | 是 | 是 | — |
| 12 | event_result_id | 来源结果 ID | INTEGER | 否 | — | 101 | — | 是 | 是 |
| 13 | created_at | 创建时间 | TIMESTAMP | 是 | now() | — | — | 是 | 是 |

---

## 8. PointsRule（积分规则）

| # | 字段名 | 中文含义 | 类型 | 必填 | 默认值 | 示例 | 展示 | 持久化 | 内部 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | id | 规则 ID | INTEGER | 是 | 自增 | 1 | — | 是 | — |
| 2 | season_id | 所属赛季 | INTEGER | 是 | — | 1 | — | 是 | — |
| 3 | rule_type | 规则类型 | VARCHAR(30) | 是 | — | individual_event | 是 | 是 | — |
| 4 | event_level | 赛事级别 | VARCHAR(20) | 否 | — | THA500 | 是 | 是 | — |
| 5 | group_name | 组别 | VARCHAR(50) | 否 | — | 甲组 | 是 | 是 | — |
| 6 | result_type | 成绩类型 | VARCHAR(30) | 否 | — | champion | 是 | 是 | — |
| 7 | points | 积分值 | INTEGER | 是 | — | 500 | 是 | 是 | — |
| 8 | enabled | 是否启用 | BOOLEAN | 是 | true | true | 是 | 是 | — |
| 9 | created_at | 创建时间 | TIMESTAMP | 是 | now() | — | — | 是 | 是 |

---

## 9. Team（团体）

| # | 字段名 | 中文含义 | 类型 | 必填 | 默认值 | 示例 | 展示 | 持久化 | 内部 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | id | 团体 ID | INTEGER | 是 | 自增 | 3 | — | 是 | — |
| 2 | name | 团体名称 | VARCHAR(100) | 是 | — | 计算机学院队 | 是 | 是 | — |
| 3 | department | 所属院系 | VARCHAR(100) | 否 | — | 计算机系 | 是 | 是 | — |
| 4 | created_at | 创建时间 | TIMESTAMP | 是 | now() | — | — | 是 | 是 |

---

## 10. TeamMember（团体队员）

| # | 字段名 | 中文含义 | 类型 | 必填 | 默认值 | 示例 | 展示 | 持久化 | 内部 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | id | 记录 ID | INTEGER | 是 | 自增 | 401 | — | 是 | 是 |
| 2 | team_id | 团体 ID | INTEGER | 是 | — | 3 | — | 是 | — |
| 3 | player_id | 队员 ID | INTEGER | 是 | — | 42 | 是 | 是 | — |
| 4 | tournament_id | 所属赛事 | INTEGER | 是 | — | 5 | — | 是 | — |
| 5 | is_active | 是否有效分摊队员 | BOOLEAN | 是 | true | true | — | 是 | — |
| 6 | created_at | 创建时间 | TIMESTAMP | 是 | now() | — | — | 是 | 是 |

---

## 11. Upload（上传记录）

| # | 字段名 | 中文含义 | 类型 | 必填 | 默认值 | 示例 | 展示 | 持久化 | 内部 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | id | 上传 ID | INTEGER | 是 | 自增 | 10 | — | 是 | — |
| 2 | tournament_id | 关联赛事 | INTEGER | 是 | — | 5 | 是 | 是 | — |
| 3 | filename | 原始文件名 | VARCHAR(255) | 是 | — | 结果.xlsx | 是 | 是 | — |
| 4 | file_path | 存储路径 | VARCHAR(500) | 是 | — | /uploads/xxx.xlsx | — | 是 | 是 |
| 5 | status | 处理状态 | VARCHAR(20) | 是 | pending | parsed | 是 | 是 | — |
| 6 | total_rows | 总行数 | INTEGER | 否 | — | 12 | 是 | 是 | — |
| 7 | valid_rows | 正常行数 | INTEGER | 否 | — | 10 | 是 | 是 | — |
| 8 | error_rows | 异常行数 | INTEGER | 否 | — | 2 | 是 | 是 | — |
| 9 | error_log | 错误信息 | TEXT | 否 | — | 第3行选手未匹配 | 是 | 是 | — |
| 10 | preview_data | 预览数据 | JSONB | 否 | — | [...] | 是 | 是 | 是 |
| 11 | uploaded_by | 上传人 | INTEGER | 是 | — | 1 | — | 是 | 是 |
| 12 | created_at | 上传时间 | TIMESTAMP | 是 | now() | — | 是 | 是 | — |

---

## 12. User（管理员）

| # | 字段名 | 中文含义 | 类型 | 必填 | 默认值 | 示例 | 展示 | 持久化 | 内部 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | id | 管理员 ID | INTEGER | 是 | 自增 | 1 | — | 是 | — |
| 2 | username | 用户名 | VARCHAR(50) | 是 | — | admin | 是 | 是 | — |
| 3 | password_hash | 密码哈希 | VARCHAR(255) | 是 | — | $2b$12$... | — | 是 | 是 |
| 4 | display_name | 显示名称 | VARCHAR(50) | 否 | — | 管理员 | 是 | 是 | — |
| 5 | is_active | 是否启用 | BOOLEAN | 是 | true | true | — | 是 | 是 |
| 6 | created_at | 创建时间 | TIMESTAMP | 是 | now() | — | — | 是 | 是 |

---

## 13. 枚举值汇总

### 13.1 status 枚举

| 实体 | 可选值 |
|---|---|
| Season | draft, active, closed |
| Tournament | draft, completed, published |
| Upload | pending, parsing, parsed, parse_failed, imported, cancelled |
| Player | active, inactive |

### 13.2 event_category 枚举

| 值 | 中文 |
|---|---|
| individual_doubles | 单项双打赛 |
| team | 团体赛 |
| representative | 代表队赛事 |
| bonus | 奖励积分 |

### 13.3 level 枚举

| 值 | 中文 |
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

### 13.4 result_type 枚举

| 值 | 中文 |
|---|---|
| champion | 冠军 |
| runner_up | 亚军 |
| semifinal | 前四名 |
| quarterfinal | 前八名 |
| participant | 参赛 |

### 13.5 source_type 枚举

| 值 | 中文 |
|---|---|
| individual_event | 单项赛事积分 |
| team_share | 团体赛分摊积分 |
| travel_bonus | 远程参赛奖补 |
| representative_team | 代表队参赛积分 |
| organizer_bonus | 办赛奖励积分 |
| donation_bonus | 捐赠赞助积分 |

### 13.6 rule_type 枚举

| 值 | 中文 |
|---|---|
| individual_event | 单项赛事规则 |
| team_event | 团体赛事规则 |
| travel_bonus | 远程参赛规则 |
| representative_team | 代表队参赛规则 |
| organizer_bonus | 办赛奖励规则 |
| donation_bonus | 捐赠赞助规则 |

### 13.7 gender 枚举

| 值 | 中文 |
|---|---|
| male | 男 |
| female | 女 |
