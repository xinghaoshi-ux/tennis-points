# THA Tennis Points Platform — Frontend

## 项目结构

```
frontend/
├── pnpm-workspace.yaml     # 工作区配置
├── package.json            # 根 package（脚本入口）
├── shared/                 # 共享类型和工具
│   ├── types/              # TypeScript 类型定义
│   └── utils/              # HTTP 客户端、轮询、防抖
├── admin/                  # 管理端应用
│   ├── src/
│   │   ├── api/            # API 调用模块
│   │   ├── layouts/        # 布局组件
│   │   ├── router/         # 路由配置
│   │   ├── stores/         # Pinia 状态管理
│   │   ├── views/          # 页面组件
│   │   └── utils/          # 工具函数
│   └── vite.config.ts
└── user/                   # 用户端应用（H5）
    ├── src/
    │   ├── api/            # API 调用模块
    │   ├── views/          # 页面组件
    │   ├── router/         # 路由配置
    │   └── styles/         # 样式
    └── vite.config.ts
```

## 技术栈

- Vue 3 + TypeScript + Vite 6
- 管理端：Element Plus
- 用户端：无组件库（自定义轻量 CSS）
- 状态管理：Pinia
- HTTP：axios
- 包管理：pnpm workspace

## 快速开始

### 安装依赖

```bash
cd frontend
pnpm install
```

### 启动管理端

```bash
pnpm dev:admin
# 或
cd admin && pnpm dev
```

访问 http://localhost:5174

### 启动用户端

```bash
pnpm dev:user
# 或
cd user && pnpm dev
```

访问 http://localhost:5173

### 构建

```bash
pnpm build:admin
pnpm build:user
```

## 环境变量

前端通过 Vite proxy 代理 API 请求，无需额外环境变量。

开发环境代理配置（已内置于 vite.config.ts）：

```
/api → http://localhost:8000
```

确保后端在 8000 端口运行。

## 页面列表

### 管理端 (port 5174)

| 路径 | 页面 |
|------|------|
| /login | 登录 |
| /dashboard | 仪表盘 |
| /seasons | 赛季管理 |
| /players | 选手管理 |
| /tournaments | 赛事管理 |
| /points-rules | 积分规则 |
| /uploads | Excel 导入 |
| /rankings | 排行榜管理 |

### 用户端 (port 5173)

| 路径 | 页面 |
|------|------|
| / | 年度积分排行榜 |

## 开发说明

- 管理端默认账号：`admin` / `admin123`（需先运行后端 seed 脚本）
- API 调用严格遵循 `docs/08_api_spec/api_spec-v1.0.md`
- 未实现的 P2 功能按钮已置灰并标注"即将上线"
