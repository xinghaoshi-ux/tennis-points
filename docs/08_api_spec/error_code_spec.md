# 错误码规范

> 本文定义 THA 年度赛事积分系统所有 API 错误码的编码规则、含义、前端展示建议和重试策略。
>
> 前后端必须以本文档为准处理错误响应。

---

## 1. 错误响应结构

```json
{
  "detail": "人类可读的错误描述",
  "code": "ERROR_CODE"
}
```

| 字段 | 说明 |
|---|---|
| detail | 面向开发者的错误描述，可直接用于前端 toast 展示 |
| code | 机器可读的错误码，前端据此判断处理逻辑 |

---

## 2. 错误码编码规则

格式：`{模块}_{错误类型}`

模块前缀：

| 前缀 | 模块 |
|---|---|
| AUTH | 认证 |
| SEASON | 赛季 |
| PLAYER | 选手 |
| TOURNAMENT | 赛事 |
| RULE | 积分规则 |
| UPLOAD | Excel 上传 |
| POINTS | 积分生成 |
| RANKING | 排行榜 |
| SYSTEM | 系统级 |

---

## 3. 通用错误码

| HTTP 状态码 | 错误码 | 含义 | 前端展示建议 | 可重试 |
|---|---|---|---|---|
| 400 | VALIDATION_ERROR | 请求参数校验失败 | 显示 detail 中的具体字段错误 | 否（需修正输入） |
| 401 | AUTH_TOKEN_MISSING | 未提供认证 Token | 跳转登录页 | 否 |
| 401 | AUTH_TOKEN_EXPIRED | Token 已过期 | 跳转登录页，提示"登录已过期" | 否 |
| 401 | AUTH_TOKEN_INVALID | Token 无效 | 跳转登录页 | 否 |
| 403 | AUTH_FORBIDDEN | 无权限执行此操作 | Toast 提示"无权限" | 否 |
| 404 | RESOURCE_NOT_FOUND | 请求的资源不存在 | Toast 提示"数据不存在" | 否 |
| 409 | CONFLICT | 数据冲突 | 显示 detail 中的冲突说明 | 否（需人工处理） |
| 422 | UNPROCESSABLE_ENTITY | 请求语义错误 | 显示 detail | 否 |
| 429 | RATE_LIMITED | 请求频率超限 | Toast 提示"操作过于频繁" | 是（延迟后重试） |
| 500 | SYSTEM_INTERNAL_ERROR | 服务器内部错误 | Toast 提示"系统异常，请稍后重试" | 是 |
| 503 | SYSTEM_UNAVAILABLE | 服务暂不可用 | Toast 提示"服务维护中" | 是（延迟后重试） |

---

## 4. 认证模块错误码

| HTTP 状态码 | 错误码 | 含义 | 前端展示建议 | 可重试 |
|---|---|---|---|---|
| 401 | AUTH_CREDENTIALS_INVALID | 用户名或密码错误 | 表单提示"用户名或密码错误" | 否（需修正输入） |
| 401 | AUTH_ACCOUNT_DISABLED | 账号已禁用 | 提示"账号已被禁用，请联系管理员" | 否 |

---

## 5. 赛季模块错误码

| HTTP 状态码 | 错误码 | 含义 | 前端展示建议 | 可重试 |
|---|---|---|---|---|
| 404 | SEASON_NOT_FOUND | 赛季不存在 | Toast 提示 | 否 |
| 409 | SEASON_ALREADY_ACTIVE | 已有激活赛季 | 提示"已有激活赛季，请先关闭当前赛季" | 否 |
| 409 | SEASON_STATUS_INVALID | 赛季状态不允许此操作 | 显示 detail（如"仅 draft 赛季可激活"） | 否 |
| 400 | SEASON_DATE_INVALID | 日期范围无效 | 表单提示"结束日期必须晚于开始日期" | 否 |

---

## 6. 选手模块错误码

| HTTP 状态码 | 错误码 | 含义 | 前端展示建议 | 可重试 |
|---|---|---|---|---|
| 404 | PLAYER_NOT_FOUND | 选手不存在 | Toast 提示 | 否 |
| 409 | PLAYER_NAME_DUPLICATE | 选手姓名重复 | 表单提示"该姓名已存在，请确认" | 否（需确认） |

---

## 7. 赛事模块错误码

| HTTP 状态码 | 错误码 | 含义 | 前端展示建议 | 可重试 |
|---|---|---|---|---|
| 404 | TOURNAMENT_NOT_FOUND | 赛事不存在 | Toast 提示 | 否 |
| 409 | TOURNAMENT_STATUS_INVALID | 赛事状态不允许此操作 | 显示 detail（如"仅 draft 赛事可编辑"） | 否 |
| 409 | TOURNAMENT_NO_ACTIVE_SEASON | 无激活赛季，无法创建赛事 | 提示"请先激活一个赛季" | 否 |

---

## 8. 积分规则模块错误码

| HTTP 状态码 | 错误码 | 含义 | 前端展示建议 | 可重试 |
|---|---|---|---|---|
| 404 | RULE_NOT_FOUND | 规则不存在 | Toast 提示 | 否 |
| 409 | RULE_DUPLICATE | 规则组合重复 | 提示"该规则组合已存在" | 否 |
| 409 | RULE_IN_USE | 规则已被引用，不可删除 | 提示"该规则已被使用，无法删除" | 否 |

---

## 9. Excel 上传模块错误码

| HTTP 状态码 | 错误码 | 含义 | 前端展示建议 | 可重试 |
|---|---|---|---|---|
| 400 | UPLOAD_FILE_EMPTY | 文件为空 | 表单提示"请选择文件" | 否 |
| 400 | UPLOAD_FILE_TYPE_INVALID | 文件类型不支持 | 提示"仅支持 .xlsx 格式" | 否 |
| 400 | UPLOAD_FILE_TOO_LARGE | 文件超过大小限制 | 提示"文件不能超过 10MB" | 否 |
| 404 | UPLOAD_NOT_FOUND | 上传记录不存在 | Toast 提示 | 否 |
| 409 | UPLOAD_STATUS_INVALID | 上传状态不允许此操作 | 显示 detail（如"仅 parsed 状态可确认导入"） | 否 |
| 409 | UPLOAD_TOURNAMENT_HAS_RESULTS | 该赛事已有导入结果 | 提示"该赛事已有结果数据，请先撤回" | 否 |
| 500 | UPLOAD_PARSE_FAILED | 文件解析失败 | 提示"文件解析失败，请检查格式后重新上传" | 是（修正文件后） |

---

## 10. 积分生成模块错误码

| HTTP 状态码 | 错误码 | 含义 | 前端展示建议 | 可重试 |
|---|---|---|---|---|
| 409 | POINTS_TOURNAMENT_NOT_COMPLETED | 赛事未完赛 | 提示"请先完成赛事结果导入" | 否 |
| 409 | POINTS_ALREADY_GENERATED | 积分已生成 | 提示"该赛事积分已生成" | 否 |
| 409 | POINTS_RULE_MISSING | 缺少匹配的积分规则 | 显示 detail（列出缺失规则） | 否（需配置规则） |
| 500 | POINTS_GENERATION_FAILED | 积分生成过程异常 | 提示"积分生成失败，请联系管理员" | 是 |

---

## 11. 排行榜模块错误码

| HTTP 状态码 | 错误码 | 含义 | 前端展示建议 | 可重试 |
|---|---|---|---|---|
| 409 | RANKING_NO_ACTIVE_SEASON | 无激活赛季 | 提示"当前无激活赛季" | 否 |
| 500 | RANKING_REFRESH_FAILED | 排行榜刷新失败 | 提示"刷新失败，请稍后重试" | 是 |

---

## 12. 前端错误处理策略

### 12.1 全局拦截器处理

以下错误码由 HTTP 拦截器统一处理，业务代码无需关注：

| 错误码 | 处理方式 |
|---|---|
| AUTH_TOKEN_MISSING | 清除本地 Token，跳转登录页 |
| AUTH_TOKEN_EXPIRED | 清除本地 Token，跳转登录页，Toast 提示"登录已过期" |
| AUTH_TOKEN_INVALID | 清除本地 Token，跳转登录页 |
| SYSTEM_INTERNAL_ERROR | 全局 Toast 提示"系统异常" |
| SYSTEM_UNAVAILABLE | 全局 Toast 提示"服务维护中" |
| RATE_LIMITED | 全局 Toast 提示"操作过于频繁" |

### 12.2 业务层处理

以下错误码需要业务代码针对性处理：

| 场景 | 错误码 | 处理方式 |
|---|---|---|
| 表单提交 | VALIDATION_ERROR | 解析 detail，标红对应字段 |
| 状态操作 | *_STATUS_INVALID | 刷新页面数据，提示状态已变更 |
| 创建操作 | *_DUPLICATE / CONFLICT | 提示冲突原因 |
| 文件上传 | UPLOAD_FILE_* | 在上传区域显示错误提示 |

### 12.3 重试策略

| 条件 | 策略 |
|---|---|
| 可重试 = 是 | 最多重试 2 次，间隔 1s、3s |
| HTTP 429 | 按 Retry-After 头等待，无头则等待 5s |
| 网络断开 | 不自动重试，提示用户检查网络 |
| 轮询超时 | 停止轮询，提示用户手动刷新 |

---

## 13. 错误码与 HTTP 状态码对应关系

| HTTP 状态码 | 语义 | 使用场景 |
|---|---|---|
| 400 | Bad Request | 参数格式错误、文件类型错误 |
| 401 | Unauthorized | 未认证、Token 过期/无效、凭证错误 |
| 403 | Forbidden | 已认证但无权限 |
| 404 | Not Found | 资源不存在 |
| 409 | Conflict | 状态冲突、数据重复、业务规则不满足 |
| 422 | Unprocessable Entity | 参数格式正确但语义错误 |
| 429 | Too Many Requests | 频率限制 |
| 500 | Internal Server Error | 服务器未预期异常 |
| 503 | Service Unavailable | 服务不可用 |
