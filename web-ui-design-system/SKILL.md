---
name: web-ui-design-system
description: 中文企业级 Web 产品界面设计系统（源自企业级管理后台原型）。当用户要求生成后台管理、数据看板、表单页、列表页等 Web 端 HTML 原型或页面时，应使用本技能，以确保视觉风格一致：主色蓝 #4B74F0、浅灰页面底、白色卡片、6px 圆角、灰底表头表格、状态标签色系、固定顶栏 + 左侧菜单 + 标签栏布局。This skill should be used when the user asks to build or prototype any web page (admin dashboard, management console, data table, form page, HTML mockup) and wants it to follow this established Chinese enterprise UI style.
agent_created: true
---

# 中文企业级 Web 界面设计系统

## 用途

本技能封装了一套完整的中文企业后台 / 管理系统视觉规范，提取自企业级管理后台单文件 HTML 原型。
用于在生成任何 Web 端页面时，复用同一套设计令牌（颜色、间距、圆角、字体）与组件类名（顶栏、侧边菜单、卡片、查询区、表格、分页、标签、弹窗、表单网格），保证多页面、多项目之间风格统一。

## 何时使用

- 用户要求「生成一个网页 / 管理后台 / 数据看板 / 列表页 / 表单页 / 原型 / HTML」。
- 用户要求「按某系统风格做页面」「用统一风格」「改造成企业后台风格」。
- 任何需要输出单文件 HTML（含内联 CSS）的 Web UI 任务，且未指定其它设计系统。

**注意**：若用户明确指定了其它设计语言（如 Ant Design、Element Plus、特定品牌色），则遵循用户指定，本技能仅作风格参考。

## 如何使用

1. **读取设计令牌**：先读 `references/design-tokens.md`，获取完整的 `:root` 变量与所有组件 CSS 类。生成页面时把 `:root` 变量与所需类直接复制进 `<style>`，不要重新发明样式。

2. **基于模板起步**：生成新页面时，复制 `assets/template.html` 作为骨架。它已包含：
   - 顶栏（`.header`，蓝底白字，含 logo / 使用手册 / 通知 / 用户区）
   - 标签栏（`.tab-bar`）+ 侧边菜单（`.sidebar`）+ 主内容区（`.main`）
   - 示例组件：查询区（`.filter-card`）、表格（`.dt`）、分页（`.pager`）、状态标签（`.tag`）
   只需替换菜单项、页面标题、表格列与数据，无需重写布局 CSS。

3. **遵循风格约定**：
   - 主色统一用 `--primary (#4B74F0)`；主按钮 `btn btn-primary`，次级 `btn btn-plain`，行内操作 `btn-link`。
   - 页面底色 `--bg-page (#F4F8FF)`，内容容器用白底 `.card` / 表格。
   - 表格：灰底表头、斑马纹、hover 高亮；状态用 `.tag-*` 色系（成功绿 / 警告橙 / 错误红 / 信息蓝 / 默认灰）。
   - 查询区用 `.filter-card`（条件横排 + 右侧查询/重置）；分页右对齐在表格下方。
   - 弹窗用 `.modal-mask > .modal(.modal-form/.modal-confirm/.modal-audit)`，含 `.modal-h/.modal-b/.modal-f` 三段。
   - 表单用 `.form-grid`（两列，整行加 `.full`），必填标 `*`（`req` 红字），时间区间用 `.tf-row` 两列。
   - 同一页内区分"我发起/我参与"等视图，用分段标签 `.seg-tabs`（选中项 `.seg.active` 蓝底白字）。
   - 审批记录类弹窗用 `.modal-audit`（宽 720），`modal-b` 内放 `.audit-table`（流程节点/处理人/处理时间/审批操作/审批意见），审批操作列用实心胶囊 `.tag-pill`（`tag-pill-success` 绿 / `tag-pill-error` 红 / `tag-pill-warning` 橙 / `tag-pill-info` 蓝 / `tag-pill-default` 灰），底部"关闭"居中。
   - 确认型弹窗（撤回/删除等）用 `.confirm-body`（图标 + 标题 + 描述），底部"再想想"(`btn-plain`) + "确认操作"(`btn-danger`)。
   - 周期性（按星期）不可用时间编辑器用 `.unavail-list` + `.unavail-add`(`.week-chk` 星期多选胶囊 + `.tf-row` 时间区间)。
   - 分段标签带数量徽章：`.seg-tabs` 内分段可嵌 `.seg-badge`（待办类加 `.warn` 橙高亮），如审批中心「待审批 N / 已同意 N / 已拒绝 N / 全部 N」。
   - 工作台首页顶部总览条用 `.wb-banner`（有任务加 `.has-task` 橙底，含大数字 `.wb-banner-num` + 文案 + 右侧跳转按钮）；下方用 `.stat-grid` 统计卡 + 柱状/饼图卡片。
   - 审批中心列表：`.seg-tabs`（带 `.seg-badge` 计数）+ `.card > table.dt`；行内操作——待审批显示「通过(`btn-success` 绿) / 详情(`btn-primary` 蓝) / 拒绝(`btn-danger` 红)」，已处理显示「详情 / 审批记录」。
   - 审批详情页：`.card.ad-detail` 四列信息网格（整行项加 `.full`）+ 24h 时间占用条(`.ad-timeline`，空闲绿/已占用灰/当前会议蓝)+ `.card.ad-actions-card` 操作卡片（同意 `btn-success` / 批注·退回·评论 `btn-primary` / 拒绝 `btn-danger` / 返回 `btn-plain`）+ `.seg-tabs.ad-tabs`（审批记录 / 评论 切换）。
   - 24 小时时间占用条（会议室占用页 / 预订选时段）用 `.room-timeline`：`.timeline-bars` 内 24 格 `.timeline-cell`（空闲绿 / 已占用灰 `.occupied` / 已选黄 `.selected`），hover 浮层显示时段，底部 `.timeline-legend` 图例。
   - 中文文案、13px 基准字号、`PingFang SC / Microsoft YaHei` 字体栈。
   - **文案约定**：审批通过的状态标签统一写"**同意**"（内部值 `approved` 不变）；拒绝写"已拒绝"；待审批写"待审批"；撤回写"撤回"。

4. **布局骨架固定**：顶栏高 56px 固定顶部；左侧菜单宽 240px 固定；标签栏高 36px 位于顶栏下、菜单右侧；主内容 `margin-left:240px; margin-top:calc(56px+36px)`。单文件 HTML 即开即用，无需构建。

## 资源文件

- `references/design-tokens.md` — 完整设计令牌与组件 CSS（生成页面时复制）。
- `assets/template.html` — 可复制的单文件 HTML 模板骨架（含布局 + 示例组件）。

## 输出建议

- 优先输出**单个自包含 HTML 文件**（内联 CSS/JS，无外部依赖），便于直接预览。
- 保持视觉细节一致：圆角 6px、边框 `#ebeef5`、阴影用主色低透明度、过渡 `.15s`。
- 配色与状态语义遵循令牌，勿硬编码散落的 hex 色（除令牌已定义的色值外）。
