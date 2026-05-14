# Frontend MVP Implementation Plan

## Context

The THA Tennis Points Platform frontend needs to be built from scratch. The `frontend/` directory currently contains only `CLAUDE.md`. The backend is fully implemented and tested (22 tests passing). This plan covers scaffolding two Vue 3 apps (admin panel + public H5) and implementing all MVP pages (P0 + P1 features).

---

## Architecture Overview

Two independent Vue 3 + Vite + TypeScript apps sharing types/utils via pnpm workspace:

- `frontend/admin/` — Desktop admin panel (Element Plus, port 5174)
- `frontend/user/` — Mobile-first public ranking page (no UI library, port 5173)
- `frontend/shared/` — Shared types, HTTP client, utilities

---

## Phase 0: Project Scaffolding

Create workspace structure, both Vite apps, shared package, and all configuration.

**Files:**
- `frontend/pnpm-workspace.yaml`
- `frontend/package.json` (workspace root)
- `frontend/shared/package.json`, `shared/tsconfig.json`
- `frontend/shared/types/` — api.ts, season.ts, player.ts, tournament.ts, pointsRule.ts, upload.ts, ranking.ts, dashboard.ts, enums.ts
- `frontend/shared/utils/` — http.ts (axios factory + interceptors), polling.ts, debounce.ts
- `frontend/admin/` — Vite scaffold (package.json, vite.config.ts, tsconfig.json, index.html, src/)
- `frontend/user/` — Vite scaffold (package.json, vite.config.ts, tsconfig.json, index.html, src/)

## Phase 1: Login + Auth (A-01)

- `admin/src/router/index.ts` — routes + navigation guard
- `admin/src/api/auth.ts` — login(), getMe()
- `admin/src/stores/auth.ts` — Pinia: token, user, login/logout
- `admin/src/views/LoginView.vue`

## Phase 2: Admin Layout Shell

- `admin/src/layouts/AdminLayout.vue` — sidebar + topbar + router-view
- `admin/src/stores/app.ts` — currentSeason (displayed in topbar)

## Phase 3: Season Management (A-02)

- `admin/src/views/SeasonsView.vue`
- `admin/src/components/seasons/SeasonFormDialog.vue`
- `admin/src/api/seasons.ts`

## Phase 4: Player Management (A-03)

- `admin/src/views/PlayersView.vue`
- `admin/src/components/players/PlayerFormDialog.vue`
- `admin/src/api/players.ts`

## Phase 5: Tournament Management (A-04)

- `admin/src/views/TournamentsView.vue`
- `admin/src/components/tournaments/TournamentFormDialog.vue`
- `admin/src/api/tournaments.ts`

## Phase 6: Points Rules (A-05)

- `admin/src/views/PointsRulesView.vue`
- `admin/src/components/pointsRules/RuleFormDialog.vue`
- `admin/src/api/pointsRules.ts`

## Phase 7: Excel Import (A-06)

- `admin/src/views/UploadsView.vue` — step wizard (select tournament → upload → polling → preview → confirm)
- `admin/src/components/uploads/StepBar.vue`
- `admin/src/components/uploads/FileUploader.vue`
- `admin/src/components/uploads/ImportPreviewTable.vue`
- `admin/src/api/uploads.ts`

## Phase 8: Rankings Management (A-07)

- `admin/src/views/RankingsView.vue`
- `admin/src/components/rankings/PlayerPointsDialog.vue`
- `admin/src/api/rankings.ts`

## Phase 9: Public Rankings (U-01)

- `user/src/App.vue`
- `user/src/views/RankingView.vue`
- `user/src/components/RankingHeader.vue`
- `user/src/components/RankingFilter.vue`
- `user/src/components/RankingTable.vue` (desktop ≥768px)
- `user/src/components/RankingCardList.vue` (mobile <768px)
- `user/src/components/PlayerPointsDialog.vue`
- `user/src/api/public.ts`
- `user/src/styles/main.css`

## Phase 10: Dashboard (A-08)

- `admin/src/views/DashboardView.vue`
- `admin/src/components/dashboard/StatCard.vue`
- `admin/src/components/dashboard/RecentUploadsList.vue`
- `admin/src/api/dashboard.ts`

---

## Route Design

### Admin (`/login` outside layout, rest inside AdminLayout)

| Path | Page | Component |
|------|------|-----------|
| /login | 登录 | LoginView |
| / | 重定向 | → /dashboard |
| /dashboard | 仪表盘 | DashboardView |
| /seasons | 赛季管理 | SeasonsView |
| /players | 选手管理 | PlayersView |
| /tournaments | 赛事管理 | TournamentsView |
| /points-rules | 积分规则 | PointsRulesView |
| /uploads | Excel 导入 | UploadsView |
| /rankings | 排行榜管理 | RankingsView |

### User (single route)

| Path | Page | Component |
|------|------|-----------|
| / | 年度积分排行榜 | RankingView |

---

## API Integration Plan

### Admin API Modules

| Module | Endpoints |
|--------|-----------|
| auth.ts | POST /admin/auth/login, GET /admin/auth/me |
| seasons.ts | GET/POST /admin/seasons, PUT /admin/seasons/{id}, POST /{id}/activate, POST /{id}/close |
| players.ts | GET/POST /admin/players, GET/PUT /admin/players/{id} |
| tournaments.ts | GET/POST /admin/tournaments, GET/PUT /{id}, POST /{id}/generate-points, POST /{id}/revoke-publish |
| pointsRules.ts | GET/POST/PUT/DELETE /admin/points-rules |
| uploads.ts | POST /admin/uploads, GET /{id}, GET /{id}/preview, POST /{id}/confirm, POST /{id}/cancel |
| rankings.ts | GET /admin/rankings, POST /admin/rankings/refresh, GET /public/players/{id}/points |
| dashboard.ts | GET /admin/dashboard |

### User API Module

| Module | Endpoints |
|--------|-----------|
| public.ts | GET /public/seasons/current, GET /public/rankings, GET /public/players/{id}/points, GET /public/departments |

### HTTP Client Design

- Shared axios instance factory in `shared/utils/http.ts`
- Admin instance: attaches Bearer token from localStorage, handles 401 → redirect to /login
- User instance: no auth header
- Both: base URL `/api/v1`, Vite proxy to `http://localhost:8000`

---

## "未开发"能力标注方式

| 处理方式 | 适用场景 | 示例 |
|----------|----------|------|
| 按钮置灰 + "即将上线" tooltip | P2 功能入口可见但不可用 | "下载模板"、"导出排行榜" |
| 完全隐藏 | P2 功能无 UI 入口 | 删除赛季、批量导入、上传历史 |

实现方式：`<el-tooltip content="即将上线"><el-button disabled>...</el-button></el-tooltip>`

---

## Testing Strategy

- **Vitest** for unit tests (shared utils, API modules, Pinia stores)
- **Manual testing** against running backend for UI verification
- No E2E framework in MVP
- Test files: `shared/__tests__/`, `admin/src/__tests__/`

---

## Not Implemented in MVP

- WeChat mini-program
- Player personal page
- Multi-season switching
- Data export
- Dark mode / i18n
- Department/team management pages
- Audit log / AI parse log
- System settings
- Ranking trend charts
- Delete season/tournament buttons
- Batch import (players/rules)
- Upload history list
- Points generation log
- Password change

---

## Verification

1. `cd frontend && pnpm install` — install all workspace dependencies
2. `cd frontend/admin && pnpm dev` — start admin on port 5174
3. `cd frontend/user && pnpm dev` — start user on port 5173
4. Verify login flow against backend
5. Verify each admin page loads and displays data
6. Verify public ranking page responsive layout
7. `pnpm --filter admin build && pnpm --filter user build` — verify production builds
8. Write results to `docs/11_integration/frontend_test_report.md`
