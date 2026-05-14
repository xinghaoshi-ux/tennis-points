# 后端测试报告

## 测试环境

- Python: 3.11.15
- pytest: 8.4.2
- pytest-asyncio: 0.26.0
- 数据库: SQLite (aiosqlite) — 用于无 PostgreSQL 环境下的测试
- 运行日期: 2026-05-14

## 测试结果

```
22 passed, 2 warnings in 3.89s
```

**全部通过。**

## 测试覆盖模块

| 测试文件 | 测试数 | 状态 | 覆盖内容 |
|----------|--------|------|----------|
| test_health.py | 1 | PASSED | 健康检查接口 |
| test_auth.py | 4 | PASSED | 登录成功/失败、/me 有/无 token |
| test_seasons.py | 4 | PASSED | 创建、列表、激活、非 draft 激活失败 |
| test_players.py | 3 | PASSED | 创建、搜索/筛选、404 |
| test_tournaments.py | 3 | PASSED | 无活跃赛季创建失败、正常创建、编辑 draft |
| test_points_rules.py | 3 | PASSED | 创建、重复失败、删除 |
| test_uploads.py | 1 | PASSED | 无文件上传返回 422 |
| test_rankings.py | 3 | PASSED | 空排行榜、当前赛季、院系列表 |

## Warnings

1. `passlib` 使用了 Python 3.13 将移除的 `crypt` 模块（不影响功能）
2. `pytest-asyncio` 提示 `event_loop` fixture 重定义已废弃（不影响测试执行）

## 已修复的问题

| 问题 | 原因 | 修复方式 |
|------|------|----------|
| `list[str]` TypeError | `list` 方法名遮蔽内置 `list` 类型 | 添加 `from __future__ import annotations` |
| JSONB 不兼容 SQLite | 测试使用 SQLite 不支持 JSONB | 改用 `sqlalchemy.JSON`（兼容两种数据库） |
| bcrypt 5.x 不兼容 passlib | passlib 未适配 bcrypt 5.0 API 变更 | 锁定 bcrypt 至 4.x |
| 模块导入失败 | 项目未配置为可安装包 | 添加 hatchling build-system 配置 |

## 未测试项（MVP 范围外或需要外部依赖）

- Excel 文件上传解析完整流程（需要实际 .xlsx 文件）
- 积分生成完整流程（需要预置赛事结果数据）
- 排行榜刷新（MVP 中为动态查询，无需刷新）
- ARQ Worker 异步任务执行
- PostgreSQL 特有功能（JSONB 索引、窗口函数排名）

## 生产环境注意事项

- 生产环境使用 PostgreSQL 16，可将 `upload.preview_data` 改回 `JSONB` 以获得更好的查询性能
- 建议在 CI 中使用 PostgreSQL 容器运行完整测试
- bcrypt 版本锁定为 4.x，待 passlib 适配 5.x 后可升级
