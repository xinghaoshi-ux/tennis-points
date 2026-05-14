# MVP 功能矩阵

> 本文定义 THA 年度赛事积分系统 MVP 阶段的完整功能矩阵。
>
> 每项功能标注优先级、实现状态、页面/接口/数据模型依赖，作为开发排期和验收的参考。

---

## 1. 功能矩阵

### 1.1 公共端功能

| # | 功能名称 | 优先级 | 本期实现 | 对应页面 | 对应接口 | 对应数据模型 | 依赖后端 | 未实现时前端标注 |
|---|---|---|---|---|---|---|---|---|
| P-01 | 查看排行榜 | P0 | 是 | U-01 | GET /public/rankings | EntriesPoints, Player | 是 | — |
| P-02 | 排行榜搜索（姓名） | P0 | 是 | U-01 | GET /public/rankings?search= | Player | 是 | — |
| P-03 | 排行榜筛选（院系） | P0 | 是 | U-01 | GET /public/rankings?department= | Player | 是 | — |
| P-04 | 查看选手积分明细 | P0 | 是 | U-01（弹窗） | GET /public/players/{id}/points | EntriesPoints, Player, Tournament, Team | 是 | — |
| P-05 | 获取院系列表 | P0 | 是 | U-01（筛选器） | GET /public/departments | Player | 是 | — |
| P-06 | 获取当前赛季信息 | P0 | 是 | U-01 | GET /public/seasons/current | Season | 是 | — |
| P-07 | 多赛季切换查看 | P2 | 否 | — | — | — | — | 否（页面不展示入口） |
| P-08 | 选手个人主页 | P2 | 否 | — | — | — | — | 否（页面不展示入口） |

### 1.2 管理端 - 认证

| # | 功能名称 | 优先级 | 本期实现 | 对应页面 | 对应接口 | 对应数据模型 | 依赖后端 | 未实现时前端标注 |
|---|---|---|---|---|---|---|---|---|
| A-01 | 管理员登录 | P0 | 是 | A-01 | POST /admin/auth/login | User | 是 | — |
| A-02 | Token 验证/保持登录 | P0 | 是 | 全局 | GET /admin/auth/me | User | 是 | — |
| A-03 | 退出登录 | P0 | 是 | 全局（导航栏） | 前端清除 Token | — | 否 | — |
| A-04 | 修改密码 | P2 | 否 | — | — | — | — | 否（页面不展示入口） |

### 1.3 管理端 - 赛季管理

| # | 功能名称 | 优先级 | 本期实现 | 对应页面 | 对应接口 | 对应数据模型 | 依赖后端 | 未实现时前端标注 |
|---|---|---|---|---|---|---|---|---|
| S-01 | 查看赛季列表 | P0 | 是 | A-02 | GET /admin/seasons | Season | 是 | — |
| S-02 | 创建赛季 | P0 | 是 | A-02 | POST /admin/seasons | Season | 是 | — |
| S-03 | 编辑赛季 | P0 | 是 | A-02 | PUT /admin/seasons/{id} | Season | 是 | — |
| S-04 | 激活赛季 | P0 | 是 | A-02 | POST /admin/seasons/{id}/activate | Season | 是 | — |
| S-05 | 关闭赛季 | P1 | 是 | A-02 | POST /admin/seasons/{id}/close | Season | 是 | — |
| S-06 | 删除赛季 | P2 | 否 | — | — | — | — | 否（按钮不展示） |

### 1.4 管理端 - 选手管理

| # | 功能名称 | 优先级 | 本期实现 | 对应页面 | 对应接口 | 对应数据模型 | 依赖后端 | 未实现时前端标注 |
|---|---|---|---|---|---|---|---|---|
| PL-01 | 查看选手列表 | P0 | 是 | A-03 | GET /admin/players | Player | 是 | — |
| PL-02 | 创建选手 | P0 | 是 | A-03 | POST /admin/players | Player | 是 | — |
| PL-03 | 编辑选手 | P0 | 是 | A-03 | PUT /admin/players/{id} | Player | 是 | — |
| PL-04 | 查看选手详情 | P0 | 是 | A-03 | GET /admin/players/{id} | Player | 是 | — |
| PL-05 | 搜索选手（姓名） | P0 | 是 | A-03 | GET /admin/players?search= | Player | 是 | — |
| PL-06 | 筛选选手（院系） | P0 | 是 | A-03 | GET /admin/players?department= | Player | 是 | — |
| PL-07 | 批量导入选手 | P2 | 否 | — | — | — | — | 否（页面不展示入口） |
| PL-08 | 停用/启用选手 | P2 | 否 | — | — | — | — | 否（按钮不展示） |

### 1.5 管理端 - 赛事管理

| # | 功能名称 | 优先级 | 本期实现 | 对应页面 | 对应接口 | 对应数据模型 | 依赖后端 | 未实现时前端标注 |
|---|---|---|---|---|---|---|---|---|
| T-01 | 查看赛事列表 | P0 | 是 | A-04 | GET /admin/tournaments | Tournament | 是 | — |
| T-02 | 创建赛事 | P0 | 是 | A-04 | POST /admin/tournaments | Tournament, Season | 是 | — |
| T-03 | 编辑赛事 | P0 | 是 | A-04 | PUT /admin/tournaments/{id} | Tournament | 是 | — |
| T-04 | 查看赛事详情 | P0 | 是 | A-04 | GET /admin/tournaments/{id} | Tournament | 是 | — |
| T-05 | 按状态筛选赛事 | P0 | 是 | A-04 | GET /admin/tournaments?status= | Tournament | 是 | — |
| T-06 | 按赛季筛选赛事 | P0 | 是 | A-04 | GET /admin/tournaments?season_id= | Tournament | 是 | — |
| T-07 | 撤回赛事发布 | P1 | 是 | A-04 | POST /admin/tournaments/{id}/revoke-publish | Tournament, EntriesPoints | 是 | — |
| T-08 | 删除赛事 | P2 | 否 | — | — | — | — | 否（按钮不展示） |

### 1.6 管理端 - 积分规则管理

| # | 功能名称 | 优先级 | 本期实现 | 对应页面 | 对应接口 | 对应数据模型 | 依赖后端 | 未实现时前端标注 |
|---|---|---|---|---|---|---|---|---|
| R-01 | 查看积分规则列表 | P0 | 是 | A-05 | GET /admin/points-rules | PointsRule | 是 | — |
| R-02 | 创建积分规则 | P0 | 是 | A-05 | POST /admin/points-rules | PointsRule | 是 | — |
| R-03 | 编辑积分规则 | P0 | 是 | A-05 | PUT /admin/points-rules/{id} | PointsRule | 是 | — |
| R-04 | 删除积分规则 | P0 | 是 | A-05 | DELETE /admin/points-rules/{id} | PointsRule | 是 | — |
| R-05 | 按类型筛选规则 | P0 | 是 | A-05 | GET /admin/points-rules?rule_type= | PointsRule | 是 | — |
| R-06 | 批量导入规则 | P2 | 否 | — | — | — | — | 否（页面不展示入口） |
| R-07 | 规则模板/预设 | P2 | 否 | — | — | — | — | 否（页面不展示入口） |

### 1.7 管理端 - Excel 导入

| # | 功能名称 | 优先级 | 本期实现 | 对应页面 | 对应接口 | 对应数据模型 | 依赖后端 | 未实现时前端标注 |
|---|---|---|---|---|---|---|---|---|
| U-01 | 上传 Excel 文件 | P0 | 是 | A-06 | POST /admin/uploads | Upload | 是 | — |
| U-02 | 查询上传解析状态 | P0 | 是 | A-06 | GET /admin/uploads/{id} | Upload | 是 | — |
| U-03 | 查看导入预览 | P0 | 是 | A-06 | GET /admin/uploads/{id}/preview | Upload, Player | 是 | — |
| U-04 | 确认导入 | P0 | 是 | A-06 | POST /admin/uploads/{id}/confirm | Upload, EventResult, EventResultPlayer | 是 | — |
| U-05 | 取消上传 | P1 | 是 | A-06 | POST /admin/uploads/{id}/cancel | Upload | 是 | — |
| U-06 | 下载 Excel 模板 | P2 | 否 | — | — | — | — | 是（按钮置灰，标注"即将上线"） |
| U-07 | 上传历史列表 | P2 | 否 | — | — | — | — | 否（页面不展示入口） |

### 1.8 管理端 - 积分生成

| # | 功能名称 | 优先级 | 本期实现 | 对应页面 | 对应接口 | 对应数据模型 | 依赖后端 | 未实现时前端标注 |
|---|---|---|---|---|---|---|---|---|
| PT-01 | 触发积分生成 | P0 | 是 | A-04（详情） | POST /admin/tournaments/{id}/generate-points | EntriesPoints, EventResult, PointsRule | 是 | — |
| PT-02 | 查询积分生成状态 | P0 | 是 | A-04（详情） | GET /admin/tournaments/{id} | Tournament | 是 | — |
| PT-03 | 积分生成日志查看 | P2 | 否 | — | — | — | — | 否（页面不展示入口） |

### 1.9 管理端 - 排行榜管理

| # | 功能名称 | 优先级 | 本期实现 | 对应页面 | 对应接口 | 对应数据模型 | 依赖后端 | 未实现时前端标注 |
|---|---|---|---|---|---|---|---|---|
| RK-01 | 查看管理端排行榜 | P0 | 是 | A-07 | GET /admin/rankings | EntriesPoints, Player | 是 | — |
| RK-02 | 刷新排行榜 | P0 | 是 | A-07 | POST /admin/rankings/refresh | EntriesPoints | 是 | — |
| RK-03 | 导出排行榜 | P2 | 否 | — | — | — | — | 是（按钮置灰，标注"即将上线"） |

### 1.10 管理端 - 仪表盘

| # | 功能名称 | 优先级 | 本期实现 | 对应页面 | 对应接口 | 对应数据模型 | 依赖后端 | 未实现时前端标注 |
|---|---|---|---|---|---|---|---|---|
| D-01 | 查看系统概览 | P1 | 是 | A-08 | GET /admin/dashboard | Season, Player, Tournament, EntriesPoints, Upload | 是 | — |
| D-02 | 查看最近上传记录 | P1 | 是 | A-08 | GET /admin/dashboard | Upload | 是 | — |
| D-03 | 数据趋势图表 | P2 | 否 | — | — | — | — | 否（页面不展示区域） |

---

## 2. 优先级统计

| 优先级 | 功能数 | 本期实现 | 说明 |
|---|---|---|---|
| P0 | 35 | 35 | 核心功能，必须实现 |
| P1 | 6 | 6 | 重要功能，本期实现但可简化 |
| P2 | 13 | 0 | 增强功能，本期不实现 |
| 合计 | 54 | 41 | — |

---

## 3. 前端标注规则

对于本期不实现的功能，前端处理方式：

| 处理方式 | 适用场景 | 示例 |
|---|---|---|
| 不展示入口 | 功能完全不可见 | 批量导入选手、上传历史列表 |
| 按钮置灰 + 标注"即将上线" | 入口可见但不可操作，给用户预期 | 下载 Excel 模板、导出排行榜 |
| 按钮不展示 | 操作入口不可见 | 删除赛季、删除赛事 |

---

## 4. 后端能力依赖说明

所有 P0/P1 功能均依赖后端能力，前端不得用本地逻辑替代：

| 能力 | 说明 |
|---|---|
| 积分计算 | 必须由后端根据规则计算，前端仅展示结果 |
| 排名计算 | 必须由后端 RANK() 窗口函数计算 |
| 选手匹配 | Excel 解析时由后端匹配选手姓名 |
| 状态流转 | 所有状态变更由后端控制，前端根据返回状态渲染 UI |
| 数据聚合 | 积分汇总、参赛次数等由后端聚合返回 |

---

## 5. 开发顺序建议

基于依赖关系，建议按以下顺序开发：

| 批次 | 功能模块 | 原因 |
|---|---|---|
| 第 1 批 | 认证（A-01~A-03） | 所有管理端功能的前置 |
| 第 2 批 | 赛季管理（S-01~S-05） | 赛事和规则的前置 |
| 第 3 批 | 选手管理（PL-01~PL-06） | Excel 导入匹配的前置 |
| 第 4 批 | 赛事管理（T-01~T-06）+ 积分规则（R-01~R-05） | 可并行开发 |
| 第 5 批 | Excel 导入（U-01~U-05） | 依赖赛事和选手 |
| 第 6 批 | 积分生成（PT-01~PT-02） | 依赖导入和规则 |
| 第 7 批 | 排行榜（RK-01~RK-02）+ 公共端（P-01~P-06） | 依赖积分数据 |
| 第 8 批 | 仪表盘（D-01~D-02）+ 撤回发布（T-07） | 补全功能 |
