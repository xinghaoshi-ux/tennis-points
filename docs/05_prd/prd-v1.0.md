# 产品需求文档（PRD）v1.0

> THA 年度赛事积分系统 MVP 阶段产品需求文档。
>
> 本文档基于已完成的业务研究、交互设计、架构设计、数据模型和 API 规范收口，作为 UI 设计、前端实现和后端实现的共同输入。

---

## 1. 产品背景

THA（清华校友网球协会）每年组织多场网球赛事，涉及单项双打赛、团体赛、代表队赛事等多种形式。当前积分统计依赖人工 Excel 汇总，存在以下问题：

- 积分计算规则复杂（6 种积分来源），人工计算易出错
- 排行榜更新滞后，校友无法实时查看排名
- 赛事结果分散在多个文件中，缺乏统一管理
- 团体赛积分分摊、远程参赛奖补等规则执行不一致

系统化平台旨在解决上述问题，建立标准化的积分管理和展示流程。

---

## 2. 产品目标

| 目标 | 衡量标准 |
|---|---|
| 积分计算自动化 | 管理员上传 Excel 后系统自动匹配规则生成积分 |
| 排行榜实时可查 | 校友通过 H5 页面随时查看最新排名 |
| 数据准确可追溯 | 每条积分记录可追溯到具体赛事和成绩 |
| 管理流程标准化 | 赛季→赛事→上传→生成→发布的固定流程 |

---

## 3. 目标用户和用户角色

| 角色 | 描述 | 使用场景 | 访问方式 |
|---|---|---|---|
| 校友（公共用户） | THA 会员，参赛选手或关注者 | 查看排行榜、查看个人积分明细 | H5 页面，无需登录 |
| 管理员 | THA 赛事运营人员（1-3 人） | 管理赛季、选手、赛事、规则，导入结果，生成积分 | 管理端 Web，需登录 |

MVP 阶段不设普通用户账号体系，公共页面无需认证。

---

## 4. 核心业务场景

### 4.1 校友查看排行榜

校友打开 H5 页面 → 看到当前赛季排行榜 → 可按姓名搜索或按院系筛选 → 点击某位选手查看积分明细（分类汇总 + 逐条记录）。

### 4.2 管理员完整操作链路

```
创建赛季 → 激活赛季
    → 配置积分规则
    → 录入选手
    → 创建赛事
        → 上传 Excel 赛事结果
        → 审核预览数据
        → 确认导入
        → 生成积分
    → 刷新排行榜
```

### 4.3 积分生成核心流程

上传 Excel → 系统解析并匹配选手 → 管理员审核预览（确认/忽略行）→ 确认导入写入赛事结果 → 触发积分生成（匹配规则计算积分）→ 赛事状态变为 published → 排行榜数据更新。

---

## 5. MVP 功能模块

### 5.1 模块 F-01：排行榜展示（公共）

| 维度 | 说明 |
|---|---|
| 业务目标 | 校友可实时查看当前赛季积分排名 |
| 用户操作 | 浏览排行榜、搜索姓名、筛选院系、查看选手积分明细 |
| 前端依赖 | 用户端 H5 页面（U-01） |
| 后端依赖 | GET /public/rankings、GET /public/players/{id}/points、GET /public/departments、GET /public/seasons/current |
| 数据对象 | EntriesPoints（聚合）、Player、Season |

### 5.2 模块 F-02：管理员认证

| 维度 | 说明 |
|---|---|
| 业务目标 | 保护管理端操作，仅授权人员可访问 |
| 用户操作 | 输入用户名密码登录、页面刷新保持登录态、退出登录 |
| 前端依赖 | 管理端登录页（A-01） |
| 后端依赖 | POST /admin/auth/login、GET /admin/auth/me |
| 数据对象 | User |

### 5.3 模块 F-03：赛季管理

| 维度 | 说明 |
|---|---|
| 业务目标 | 管理积分统计周期，确保同一时间只有一个激活赛季 |
| 用户操作 | 创建赛季、编辑赛季、激活赛季、关闭赛季 |
| 前端依赖 | 管理端赛季管理页（A-02） |
| 后端依赖 | GET/POST /admin/seasons、PUT /admin/seasons/{id}、POST /admin/seasons/{id}/activate、POST /admin/seasons/{id}/close |
| 数据对象 | Season |
| 业务规则 | 同一时间最多一个 active 赛季；激活新赛季时原 active 自动变 closed |

### 5.4 模块 F-04：选手管理

| 维度 | 说明 |
|---|---|
| 业务目标 | 维护参赛校友基础信息，支撑 Excel 导入时的选手匹配 |
| 用户操作 | 创建选手、编辑选手、搜索选手、按院系筛选 |
| 前端依赖 | 管理端选手管理页（A-03） |
| 后端依赖 | GET/POST /admin/players、GET/PUT /admin/players/{id} |
| 数据对象 | Player |

### 5.5 模块 F-05：赛事管理

| 维度 | 说明 |
|---|---|
| 业务目标 | 记录每场赛事的基本信息，作为积分来源的载体 |
| 用户操作 | 创建赛事、编辑赛事、查看赛事列表和详情 |
| 前端依赖 | 管理端赛事管理页（A-04） |
| 后端依赖 | GET/POST /admin/tournaments、GET/PUT /admin/tournaments/{id} |
| 数据对象 | Tournament、Season |
| 业务规则 | 赛事自动归属当前 active 赛季；仅 draft 状态可编辑 |

### 5.6 模块 F-06：积分规则管理

| 维度 | 说明 |
|---|---|
| 业务目标 | 配置不同赛事级别、组别、成绩对应的积分值 |
| 用户操作 | 创建规则、编辑规则、删除规则、按类型筛选 |
| 前端依赖 | 管理端积分规则页（A-05） |
| 后端依赖 | GET/POST/PUT/DELETE /admin/points-rules |
| 数据对象 | PointsRule、Season |
| 业务规则 | 同赛季内 (rule_type, event_level, group_name, result_type) 组合唯一；已被引用的规则不可删除 |

### 5.7 模块 F-07：Excel 导入

| 维度 | 说明 |
|---|---|
| 业务目标 | 将赛事结果从 Excel 导入系统，支持预览审核 |
| 用户操作 | 选择赛事 → 上传文件 → 等待解析 → 审核预览 → 确认/忽略行 → 确认导入 |
| 前端依赖 | 管理端 Excel 导入页（A-06） |
| 后端依赖 | POST /admin/uploads、GET /admin/uploads/{id}、GET /admin/uploads/{id}/preview、POST /admin/uploads/{id}/confirm、POST /admin/uploads/{id}/cancel |
| 数据对象 | Upload、EventResult、EventResultPlayer、Player |
| 业务规则 | 仅支持 .xlsx；解析时自动匹配选手姓名；未匹配选手标记为 warning；管理员可选择忽略异常行 |

### 5.8 模块 F-08：积分生成

| 维度 | 说明 |
|---|---|
| 业务目标 | 根据赛事结果和积分规则自动计算并生成积分记录 |
| 用户操作 | 在赛事详情页点击"生成积分" → 等待完成 → 确认赛事状态变为 published |
| 前端依赖 | 管理端赛事详情页（A-04 内） |
| 后端依赖 | POST /admin/tournaments/{id}/generate-points、GET /admin/tournaments/{id} |
| 数据对象 | EntriesPoints、EventResult、PointsRule、Team、TeamMember |
| 业务规则 | 仅 completed 状态赛事可生成积分；单项双打每人获完整积分；团体赛按有效队员数分摊；跨省奖补 200 分、跨境奖补 500 分 |

### 5.9 模块 F-09：排行榜管理

| 维度 | 说明 |
|---|---|
| 业务目标 | 管理员可查看和刷新排行榜 |
| 用户操作 | 查看管理端排行榜、点击刷新 |
| 前端依赖 | 管理端排行榜页（A-07） |
| 后端依赖 | GET /admin/rankings、POST /admin/rankings/refresh |
| 数据对象 | EntriesPoints（聚合）、Player |

### 5.10 模块 F-10：仪表盘

| 维度 | 说明 |
|---|---|
| 业务目标 | 管理员登录后快速了解系统概况 |
| 用户操作 | 查看当前赛季、选手数、赛事数、积分记录数、最近上传 |
| 前端依赖 | 管理端仪表盘页（A-08） |
| 后端依赖 | GET /admin/dashboard |
| 数据对象 | Season、Player、Tournament、EntriesPoints、Upload |

---

## 6. 页面与交互要求

### 6.1 用户端（H5）

| 页面 | 编号 | 核心交互 |
|---|---|---|
| 排行榜页 | U-01 | 表格展示排名；顶部搜索框实时筛选；院系下拉筛选；点击姓名弹出积分明细弹窗 |

交互要求：
- 移动端优先，响应式适配
- 首屏加载排行榜前 20 条
- 搜索输入 300ms 防抖
- 积分明细弹窗展示分类汇总饼图/条形 + 逐条记录列表
- 无数据时展示空状态提示

### 6.2 管理端（Web）

| 页面 | 编号 | 核心交互 |
|---|---|---|
| 登录页 | A-01 | 用户名+密码表单，登录后跳转仪表盘 |
| 赛季管理 | A-02 | 列表+操作按钮（激活/关闭），创建/编辑弹窗 |
| 选手管理 | A-03 | 列表+搜索+筛选，创建/编辑弹窗 |
| 赛事管理 | A-04 | 列表+状态筛选，创建/编辑弹窗，详情页含"生成积分"按钮 |
| 积分规则 | A-05 | 按类型分组展示，创建/编辑/删除操作 |
| Excel 导入 | A-06 | 选择赛事→上传文件→解析进度→预览表格→勾选确认 |
| 排行榜 | A-07 | 同公共排行榜+刷新按钮 |
| 仪表盘 | A-08 | 统计卡片+最近上传列表 |

交互要求：
- 桌面端优先，最小宽度 1280px
- 使用 Element Plus 组件库
- 左侧导航栏固定
- 表格支持分页（默认 20 条/页）
- 操作按钮根据状态动态启用/禁用
- 异步操作（上传解析、积分生成）显示 loading 状态
- 所有破坏性操作（删除、撤回）需二次确认

---

## 7. 状态流转摘要

### 7.1 赛季（Season）

```
draft → active → closed
```

- draft：可编辑、可删除、可激活
- active：可编辑、可关闭；同一时间最多一个
- closed：仅可查看

### 7.2 赛事（Tournament）

```
draft → completed → published
                 ↑←←←←←←←←←↓（撤回发布）
```

- draft：可编辑、可上传结果
- completed：结果已导入，可生成积分
- published：积分已生成，可撤回

### 7.3 上传（Upload）

```
pending → parsing → parsed → imported
                  ↘ parse_failed
          parsed → cancelled
```

- pending：文件已上传，等待解析
- parsing：解析中
- parsed：解析完成，等待确认
- imported：已确认导入
- parse_failed：解析失败
- cancelled：已取消

---

## 8. 数据对象摘要

| 实体 | 业务含义 | 核心字段 | 关键关系 |
|---|---|---|---|
| Season | 赛季 | name, start_date, end_date, status | 1:N → Tournament, PointsRule, EntriesPoints |
| Player | 选手 | full_name, gender, birth_date, department | 1:N → EntriesPoints, TeamMember |
| Tournament | 赛事 | name, event_category, level, group_name, location, status | 属于 Season；1:N → EventResult, Upload |
| EventResult | 赛事结果 | result_type, is_cross_province, is_cross_border | 属于 Tournament；M:N → Player（通过 EventResultPlayer） |
| EntriesPoints | 积分记录 | source_type, points_earned, result_type, description | 属于 Player + Tournament + Season |
| PointsRule | 积分规则 | rule_type, event_level, group_name, result_type, points | 属于 Season |
| Team | 团体 | name, department | 1:N → TeamMember, EventResult |
| TeamMember | 团体队员 | is_active | 属于 Team + Player + Tournament |
| Upload | 上传记录 | filename, status, total_rows, valid_rows, error_rows | 属于 Tournament |
| User | 管理员 | username, password_hash, display_name | 1:N → Upload |

---

## 9. API 依赖摘要

### 9.1 公共接口（无认证）

| 接口 | 用途 | 调用页面 |
|---|---|---|
| GET /public/seasons/current | 获取当前赛季 | U-01 |
| GET /public/rankings | 排行榜查询 | U-01 |
| GET /public/players/{id}/points | 选手积分明细 | U-01（弹窗） |
| GET /public/departments | 院系列表 | U-01（筛选器） |

### 9.2 管理接口（Bearer Token）

| 接口 | 用途 | 调用页面 |
|---|---|---|
| POST /admin/auth/login | 登录 | A-01 |
| GET /admin/auth/me | Token 验证 | 全局 |
| GET/POST /admin/seasons | 赛季列表/创建 | A-02 |
| PUT /admin/seasons/{id} | 编辑赛季 | A-02 |
| POST /admin/seasons/{id}/activate | 激活赛季 | A-02 |
| POST /admin/seasons/{id}/close | 关闭赛季 | A-02 |
| GET/POST /admin/players | 选手列表/创建 | A-03 |
| GET/PUT /admin/players/{id} | 选手详情/编辑 | A-03 |
| GET/POST /admin/tournaments | 赛事列表/创建 | A-04 |
| GET/PUT /admin/tournaments/{id} | 赛事详情/编辑 | A-04 |
| GET/POST/PUT/DELETE /admin/points-rules | 积分规则 CRUD | A-05 |
| POST /admin/uploads | 上传 Excel | A-06 |
| GET /admin/uploads/{id} | 上传状态查询 | A-06 |
| GET /admin/uploads/{id}/preview | 导入预览 | A-06 |
| POST /admin/uploads/{id}/confirm | 确认导入 | A-06 |
| POST /admin/uploads/{id}/cancel | 取消上传 | A-06 |
| POST /admin/tournaments/{id}/generate-points | 积分生成 | A-04 |
| GET /admin/rankings | 管理端排行榜 | A-07 |
| POST /admin/rankings/refresh | 刷新排行榜 | A-07 |
| POST /admin/tournaments/{id}/revoke-publish | 撤回发布 | A-04 |
| GET /admin/dashboard | 仪表盘数据 | A-08 |

---

## 10. MVP 范围

### 10.1 MVP 包含（本期实现）

| 类别 | 内容 |
|---|---|
| 用户端 | 排行榜页（搜索、筛选、积分明细弹窗） |
| 管理端 | 登录、赛季管理、选手管理、赛事管理、积分规则管理、Excel 导入、积分生成、排行榜管理、仪表盘 |
| 后端 | 全部 P0 接口（25 个）、JWT 认证、异步任务（Excel 解析、积分生成） |
| 基础设施 | PostgreSQL、Redis、ARQ Worker、本地文件存储 |

### 10.2 MVP 简化处理

| 功能 | 简化方式 |
|---|---|
| 仪表盘 | 返回基础统计数据，不做图表 |
| 排行榜 | 动态查询计算，不使用物化视图 |
| 文件存储 | 本地磁盘，不接入 OSS |
| 管理员 | 单角色，不做权限分级 |
| 选手匹配 | 精确姓名匹配，不做模糊/智能匹配 |

---

## 11. 非 MVP 范围

以下功能明确不在本期实现范围内：

| 功能 | 原因 |
|---|---|
| 微信小程序 | MVP 仅 H5，后续根据用户反馈决定 |
| 用户账号体系 | 公共端无需登录，MVP 不做用户注册/绑定 |
| AI 智能匹配 | 选手匹配先用精确匹配，AI 模块延后 |
| 数据导出 | 管理端暂不支持导出 Excel/PDF |
| 操作日志 | 不记录管理员操作审计日志 |
| 多赛季对比 | 排行榜仅展示当前赛季 |
| 通知推送 | 不做积分变动通知 |
| 批量导入选手 | 选手逐个录入，不支持批量 Excel 导入 |
| CI/CD | 本期手动部署 |
| 国际化 | 仅中文 |
| 深色模式 | 不做 |

---

## 12. 验收标准

### 12.1 功能验收

| 场景 | 验收标准 |
|---|---|
| 排行榜展示 | 校友打开页面 3 秒内看到排行榜；搜索和筛选响应 < 1 秒 |
| 积分明细 | 点击选手姓名后弹窗展示分类汇总和逐条记录，数据与后端一致 |
| 管理员登录 | 正确凭证登录成功；错误凭证提示明确错误；Token 过期自动跳转登录 |
| 赛季管理 | 创建/激活/关闭流程正常；同一时间只有一个 active 赛季 |
| 选手管理 | CRUD 正常；搜索和筛选正常；分页正常 |
| 赛事管理 | CRUD 正常；状态约束生效（draft 可编辑，非 draft 不可编辑） |
| 积分规则 | CRUD 正常；重复规则创建时报错；已引用规则不可删除 |
| Excel 导入 | 上传→解析→预览→确认全流程正常；异常行标识清晰；可选择忽略行 |
| 积分生成 | 生成后积分记录正确；单项双打每人完整积分；团体赛按人数分摊 |
| 排行榜刷新 | 刷新后排行榜数据与积分记录一致；同积分并列排名 |

### 12.2 数据验收

| 验证项 | 标准 |
|---|---|
| 积分计算正确性 | 与人工计算结果一致（抽样 10 条验证） |
| 排名正确性 | 同积分并列，下一名跳号（RANK 语义） |
| 团体赛分摊 | round(团队总积分 / 有效队员数) |
| 远程参赛奖补 | 跨省 200 分、跨境 500 分 |

### 12.3 非功能验收

| 维度 | 标准 |
|---|---|
| 页面加载 | 首屏 < 3 秒（本地网络） |
| API 响应 | 同步接口 < 500ms |
| 并发 | 支持 10 个管理员同时操作 |
| 数据量 | 支持 500 选手、50 赛事、5000 积分记录 |

---

## 13. 风险和限制

| 风险 | 影响 | 缓解措施 |
|---|---|---|
| Excel 格式不统一 | 解析失败率高 | 提供模板下载；解析时容错处理；预览环节人工审核 |
| 选手姓名重复 | 匹配错误 | 精确匹配 + 预览时标记未匹配行；管理员人工确认 |
| 积分规则变更 | 已生成积分需重算 | 提供撤回发布功能；撤回后可重新生成 |
| 单管理员操作 | 无并发冲突控制 | MVP 阶段管理员人数少（1-3 人），暂不做乐观锁 |
| 数据量增长 | 排行榜查询变慢 | MVP 数据量小（<5000 条），动态查询可满足；后续可加物化视图 |
| H5 兼容性 | 部分老旧浏览器不支持 | 目标浏览器：iOS Safari 14+、Android Chrome 80+、微信内置浏览器 |
| 无备份机制 | 数据丢失风险 | MVP 阶段手动定期备份 PostgreSQL；后续接入自动备份 |

---

## 14. 术语表

| 术语 | 含义 |
|---|---|
| THA | 清华校友网球协会（Tsinghua Alumni Tennis Association） |
| 赛季 | 年度积分统计周期（如 2026-04 至 2027-04） |
| 单项双打赛 | 两人一组的双打比赛 |
| 团体赛 | 以团队为单位参赛，积分按队员分摊 |
| 代表队赛事 | 代表学校/协会参加的外部赛事 |
| 积分来源 | individual_event / team_share / travel_bonus / representative_team / organizer_bonus / donation_bonus |
| 赛事级别 | THA1000 / THA800 / THA500 / THA200 / THA_S / THA_A / THA_B |
