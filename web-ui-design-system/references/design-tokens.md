# 设计系统参考（企业级管理后台风格）

本文件提取自企业级管理后台原型的完整设计令牌（Design Tokens）与组件样式。
生成任何 Web 端产品页面（后台管理、企业系统、数据看板、表单页）时，**直接复用**以下 CSS 变量与类名，
保持一致的视觉语言：主色蓝 `#4B74F0`、浅灰页面底 `#F4F8FF`、白色卡片、圆角 6px、表格灰底表头、状态标签色系。

---

## 1. Design Tokens（`:root` 变量，复制到 `<style>` 顶部）

```css
:root{
  --primary:#4B74F0;
  --primary-hover:#3a5cd0;
  --primary-soft:#E8F0FE;
  --bg-page:#F4F8FF;
  --bg-card:#FFFFFF;
  --bg-table-head:#fafbfc;
  --bg-row-stripe:#fbfbfc;
  --border-soft:#ebeef5;
  --border-base:#e5e7eb;
  --text-base:#333333;
  --text-secondary:#4b5563;
  --text-tertiary:#8b94a3;
  --success:#26BD71;
  --warning:#FFB21A;
  --error:#F24957;
  --top-h:56px;
  --side-w:240px;
  --hover-row:#f3f6ff;
  --divider-thin:#f3f4f6;
}
*{margin:0;padding:0;box-sizing:border-box}
html{min-width:1280px}
body{
  font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei","Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  font-size:13px;line-height:20px;color:var(--text-base);background:var(--bg-page);
}
a{color:var(--primary);text-decoration:none}
ul{list-style:none}
```

---

## 2. 布局骨架（顶栏 + 侧边菜单 + 主内容 + 标签栏）

```css
/* Top Bar */
.header{position:fixed;top:0;left:0;right:0;height:var(--top-h);z-index:100;background:var(--primary);
  display:flex;align-items:center;padding:0 20px;color:#fff;box-shadow:0 2px 8px rgba(75,116,240,.25);}
.logo{display:flex;align-items:center;gap:10px;font-size:16px;font-weight:600;color:#fff;flex-shrink:0;margin-right:24px}
.logo-icon{width:32px;height:32px;border-radius:6px;background:#fff;display:flex;align-items:center;justify-content:center;color:var(--primary);font-size:16px;font-weight:600}
.header-right{margin-left:auto;display:flex;align-items:center;gap:12px;flex-shrink:0}
.manual-btn{display:inline-flex;align-items:center;gap:6px;height:30px;padding:0 14px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.3);border-radius:4px;color:#fff;font-size:12px;cursor:pointer;transition:background .15s}
.manual-btn:hover{background:rgba(255,255,255,.22)}
.icon-btn{position:relative;width:32px;height:32px;border:1px solid rgba(255,255,255,.3);background:rgba(255,255,255,.1);border-radius:4px;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:14px;color:#fff}
.icon-btn:hover{background:rgba(255,255,255,.22)}
.badge{position:absolute;top:-4px;right:-4px;background:var(--error);color:#fff;font-size:10px;min-width:16px;height:16px;border-radius:8px;display:flex;align-items:center;justify-content:center;padding:0 4px;border:1.5px solid var(--primary)}
.user-info{display:flex;align-items:center;gap:8px;padding:0 8px;cursor:pointer;height:40px;border-radius:4px}
.user-info:hover{background:rgba(255,255,255,.12)}
.user-avatar{width:32px;height:32px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;color:var(--primary);font-size:16px;flex-shrink:0}
.user-meta{display:flex;flex-direction:column;line-height:16px}
.user-name{font-size:13px;font-weight:500;color:#fff}
.user-role{font-size:11px;color:rgba(255,255,255,.75)}

/* Sidebar */
.sidebar{position:fixed;top:var(--top-h);left:0;bottom:0;width:var(--side-w);z-index:90;
  background:#fff;border-right:1px solid var(--border-soft);padding:8px 0;overflow-y:auto;}
.menu-item{display:flex;align-items:center;gap:10px;padding:0 20px;height:44px;cursor:pointer;
  color:var(--text-secondary);font-size:13px;border-left:3px solid transparent;transition:all .15s;}
.menu-item:hover{background:var(--primary-soft);color:var(--primary)}
.menu-item.active{background:var(--primary-soft);color:var(--primary);border-left-color:var(--primary);font-weight:500}
.menu-item .mi{font-size:16px;width:20px;text-align:center;flex-shrink:0}
.menu-item .arrow{margin-left:auto;font-size:10px;color:var(--text-tertiary);transition:transform .2s}
.menu-item.expanded .arrow{transform:rotate(90deg)}
.submenu{overflow:hidden}
.submenu .menu-item{height:40px;padding-left:48px;font-size:12px}

/* Main + Tab Bar */
.tab-bar{position:fixed;top:var(--top-h);left:var(--side-w);right:0;height:36px;background:#f5f7fa;border-bottom:1px solid var(--border-soft);display:flex;align-items:flex-end;padding:0 12px;z-index:85;overflow-x:auto}
.tab-item{height:32px;padding:0 12px;display:flex;align-items:center;gap:8px;font-size:13px;color:var(--text-secondary);background:#e8ecf3;border:1px solid var(--border-soft);border-bottom:none;border-radius:4px 4px 0 0;margin-right:4px;cursor:pointer;white-space:nowrap}
.tab-item.active{background:#fff;color:var(--primary);border-top:2px solid var(--primary);font-weight:500}
.tab-close{width:16px;height:16px;display:flex;align-items:center;justify-content:center;border-radius:50%;font-size:13px;line-height:1;color:var(--text-tertiary)}
.tab-close:hover{background:var(--error);color:#fff}
.main{margin-left:var(--side-w);margin-top:calc(var(--top-h) + 36px);padding:16px}
```

---

## 3. 卡片 / 统计卡 / 标题

```css
.page-title{font-size:18px;font-weight:600;line-height:28px;margin-bottom:12px;color:var(--text-base)}
.page-toolbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}
.page-toolbar .left{font-size:18px;font-weight:600;color:var(--text-base)}
.page-toolbar .right{display:flex;gap:8px}
.card{background:var(--bg-card);border:1px solid var(--border-soft);border-radius:6px;padding:16px}
.card-title{font-size:15px;font-weight:600;line-height:24px;margin-bottom:12px;display:flex;align-items:center;justify-content:space-between}

.stat-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:16px}
.stat-card{background:var(--bg-card);border:1px solid var(--border-soft);border-radius:6px;padding:16px;display:flex;align-items:center;gap:14px}
.stat-icon{width:44px;height:44px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:20px}
.stat-info .num{font-size:24px;font-weight:700;line-height:30px}
.stat-info .lbl{font-size:12px;color:var(--text-tertiary)}
.stat-card.blue .stat-icon{background:rgba(75,116,240,.1);color:var(--primary)}
.stat-card.green .stat-icon{background:rgba(38,189,113,.1);color:var(--success)}
.stat-card.orange .stat-icon{background:rgba(255,178,26,.1);color:var(--warning)}
.stat-card.purple .stat-icon{background:rgba(114,46,209,.1);color:#722ED1}
```

---

## 4. 查询区（filter-card）

```css
.filter-card{background:var(--bg-card);border:1px solid var(--border-soft);border-radius:6px;padding:12px 16px;margin-bottom:10px;display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.filter-item{display:flex;align-items:center;gap:6px}
.filter-item label{font-size:12px;color:var(--text-tertiary);white-space:nowrap}
.filter-actions{margin-left:auto;display:flex;gap:8px}
.more-filters{display:none;gap:12px;padding-top:8px;border-top:1px dashed var(--border-soft);margin-top:4px;width:100%}
.caret{font-size:10px;margin-left:2px}

/* Segmented Tabs（分段切换，如"我的发起 / 我参与的"） */
.seg-tabs{display:inline-flex;background:var(--bg-card);border:1px solid var(--border-soft);border-radius:4px;padding:3px;margin-bottom:10px;gap:2px}
.seg-tabs .seg{padding:4px 18px;font-size:13px;color:var(--text-secondary);border-radius:3px;cursor:pointer;user-select:none;transition:all .15s;white-space:nowrap}
.seg-tabs .seg:hover{color:var(--primary)}
.seg-tabs .seg.active{background:var(--primary);color:#fff;font-weight:500}
/* 分段内的数量徽章（如待审批数，warn 用橙色高亮） */
.seg-badge{display:inline-flex;align-items:center;justify-content:center;min-width:16px;height:16px;padding:0 5px;margin-left:4px;border-radius:8px;background:var(--text-tertiary);color:#fff;font-size:11px;line-height:16px;font-weight:500}
.seg-badge.warn{background:var(--warning)}
```
用法：用 `<div class="seg-tabs">` 包裹若干 `<span class="seg">`；选中项加 `.active`，点击切换对应视图（如 subTab='initiated' / 'joined'）。常用于同一页内区分"我发起的"与"我参与的"。
分段内可嵌入数量徽章：`<span class="seg-badge warn">3</span>`，数字 >0 时显示；待办类用 `.warn`（橙）高亮，例如审批中心的「待审批 3 / 已同意 12 / 已拒绝 2 / 全部 20」。

---

## 4.1 确认弹窗内容体（confirm-body）

```css
.confirm-body{display:flex;align-items:flex-start}
.confirm-body .text{flex:1}
.confirm-body .text .title{font-size:15px;font-weight:600;margin-bottom:6px}
.confirm-body .text .desc{font-size:13px;color:var(--text-secondary);line-height:20px}
```
用于 `.modal-confirm` 内带图标 + 标题 + 描述的确认提示（如撤回、取消确认）。结构：`<div class="confirm-body"><span class="confirm-icon warning">⚠</span><div class="text"><div class="title">...</div><div class="desc">...</div></div></div>`，底部按钮用「再想想」(`btn-plain`) + 「确认操作」(`btn-danger`)。

---

## 5. 表单控件 & 按钮

```css
.input,.select{height:28px;border:1px solid var(--border-base);border-radius:3px;padding:0 8px;font-size:13px;color:var(--text-base);background:#fff;outline:none;transition:border-color .2s}
.input:focus,.select:focus{border-color:var(--primary)}
.input::placeholder{color:var(--text-tertiary)}
.select{cursor:pointer}
textarea.input{height:auto;padding:6px 8px;resize:vertical;line-height:20px}

.btn{height:28px;padding:0 14px;border-radius:3px;font-size:13px;cursor:pointer;border:1px solid transparent;transition:all .15s;display:inline-flex;align-items:center;gap:4px;white-space:nowrap}
.btn:hover{opacity:.85}
.btn-sm{height:26px;padding:0 10px;font-size:12px}
.btn-primary{background:var(--primary);color:#fff;border-color:var(--primary)}
.btn-primary:hover{background:var(--primary-hover);border-color:var(--primary-hover)}
.btn-success{background:var(--success);color:#fff;border-color:var(--success)}
.btn-success:hover{background:#1ea85f;border-color:#1ea85f}
.btn-secondary{background:#fff;color:var(--primary);border-color:var(--primary)}
.btn-secondary:hover{background:var(--primary-soft)}
.btn-plain{background:#fff;color:var(--text-secondary);border-color:var(--border-base)}
.btn-plain:hover{color:var(--primary);border-color:var(--primary)}
.btn-danger{background:var(--error);color:#fff;border-color:var(--error)}
.btn-danger-secondary{background:#fff;color:var(--error);border-color:var(--error)}
.btn-danger-secondary:hover{background:rgba(242,73,87,.06)}
.btn-link{background:transparent;color:var(--primary);border:none;padding:0 4px;font-size:13px;cursor:pointer}
.btn-link:hover{opacity:.75}
```

常用组合：
- 主操作（查询/提交/新增/详情/批注/退回/评论）→ `btn btn-primary btn-sm`
- 次级（重置/返回）→ `btn btn-plain btn-sm`
- 行内操作（编辑/详情/撤回）→ `btn-link`
- **同意 / 通过（审批正向操作）→ `btn btn-success` 实心绿**；**拒绝（审批负向操作）→ `btn btn-danger` 实心红**（列表与详情页一致）；驳回的弱危险态用 `btn-danger-secondary`
- 危险（删除/确认取消）→ `btn btn-danger`

---

## 6. 表格（dt）

```css
.table-toolbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
.table-toolbar .left{font-size:12px;color:var(--text-tertiary)}
.table-toolbar .left b{color:var(--text-base);font-weight:600}
.table-toolbar .right{display:flex;gap:8px;align-items:center}
.dt{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--border-soft);border-radius:4px;overflow:hidden}
.dt th{background:var(--bg-table-head);color:var(--text-base);font-weight:500;font-size:12.5px;padding:7px 10px;text-align:left;border-bottom:1px solid var(--border-soft);cursor:pointer;white-space:nowrap;user-select:none}
.dt th.center{text-align:center}
.dt th.right{text-align:right}
.dt th .sort{font-size:10px;color:#c8ccd3;margin-left:4px}
.dt th.sorted .sort{color:var(--primary)}
.dt td{padding:6px 10px;font-size:12.5px;border-bottom:1px solid var(--divider-thin);color:var(--text-base)}
.dt td.center{text-align:center}
.dt td.right{text-align:right}
.dt td.amt{text-align:right;font-variant-numeric:tabular-nums}
.dt tbody tr:nth-child(even){background:var(--bg-row-stripe)}
.dt tbody tr:hover{background:var(--hover-row)}
.dt tbody tr:last-child td{border-bottom:none}
.dt td.empty{text-align:center;color:var(--text-tertiary);padding:24px}
```

---

## 7. 分页（pager）

```css
.pager{display:flex;align-items:center;justify-content:flex-end;gap:8px;padding:8px 0;font-size:12px;color:var(--text-tertiary)}
.pager .total{white-space:nowrap}
.pager .page-size{display:flex;align-items:center;gap:4px}
.pager .page-size select{height:26px;border:1px solid var(--border-base);border-radius:3px;font-size:12px;padding:0 4px;cursor:pointer}
.pager .pages{display:flex;gap:2px}
.pager .page{min-width:26px;height:26px;border:1px solid var(--border-base);background:#fff;border-radius:3px;cursor:pointer;font-size:12px;color:var(--text-secondary);display:flex;align-items:center;justify-content:center;padding:0 4px;transition:all .15s}
.pager .page:hover{border-color:var(--primary);color:var(--primary)}
.pager .page.active{background:var(--primary);border-color:var(--primary);color:#fff}
.pager .page.disabled{color:#ccc;cursor:not-allowed;border-color:var(--border-soft)}
.pager .ellipsis{padding:0 4px;color:var(--text-tertiary);line-height:26px}
```
分页结构建议（右对齐）：`共 X 条` + `X 条/页 下拉` + `页码按钮`。原型中「我的预约」页隐藏了「共 X 条」并把「新增预约」放到了分页行最右（用 `style="margin-left:auto"`），按需使用。

---

## 8. 状态标签（tag）

```css
.tag{display:inline-flex;align-items:center;padding:2px 8px;border-radius:3px;font-size:12px;font-weight:500;line-height:18px}
.tag-success{background:rgba(38,189,113,.1);color:var(--success)}
.tag-warning{background:rgba(255,178,26,.1);color:var(--warning)}
.tag-error{background:rgba(242,73,87,.1);color:var(--error)}
.tag-info{background:rgba(75,116,240,.1);color:var(--primary)}
.tag-default{background:rgba(139,148,163,.1);color:var(--text-tertiary)}
```
状态映射约定：`同意(已通过)/可用 → tag-success`，`待审批/维护中 → tag-warning`，`已拒绝/已取消 → tag-error`，`草稿/保存 → tag-default`，`重要信息 → tag-info`。

> 文案约定（与企业后台原型一致）：审批通过的状态标签统一写作 **"同意"**（内部值仍为 `approved`）；拒绝写作"已拒绝"；待审批写作"待审批"；撤回中写作"撤回"。审批操作胶囊（`tag-pill`）同理：通过→`tag-pill-success` 显示"通过"，拒绝→`tag-pill-error` 显示"拒绝"。

---

## 9. 弹窗（modal）

```css
.modal-mask{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.45);z-index:200;display:flex;align-items:center;justify-content:center}
.modal{background:#fff;border-radius:6px;box-shadow:0 8px 32px rgba(0,0,0,.16);overflow:hidden;animation:modalIn .2s ease}
@keyframes modalIn{from{transform:translateY(-20px);opacity:0}to{transform:translateY(0);opacity:1}}
.modal-form{width:520px;max-height:80vh;display:flex;flex-direction:column}
.modal-confirm{width:420px}
.modal-h{height:48px;padding:0 20px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--border-soft);font-size:15px;font-weight:600}
.modal-h .close{cursor:pointer;color:var(--text-tertiary);font-size:18px;width:24px;height:24px;display:flex;align-items:center;justify-content:center;border-radius:3px}
.modal-h .close:hover{background:var(--bg-page);color:var(--text-base)}
.modal-b{padding:20px;overflow-y:auto;flex:1}
.modal-f{height:56px;padding:0 20px;display:flex;align-items:center;justify-content:flex-end;gap:8px;border-top:1px solid var(--border-soft)}
.confirm-icon{width:32px;height:32px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-size:16px;margin-right:8px}
.confirm-icon.warning{background:rgba(255,178,26,.1);color:var(--warning)}
.confirm-icon.error{background:rgba(242,73,87,.1);color:var(--error)}
```

---

## 9.1 审批记录弹窗（modal-audit / audit-table / tag-pill 胶囊标签）

```css
/* 审批记录弹窗：宽 720，body 无内边距直接放表格 */
.modal-audit{width:720px;max-height:80vh;display:flex;flex-direction:column}
.modal-audit .modal-b{padding:0}
.audit-table{width:100%;border-collapse:collapse;font-size:13px}
.audit-table th{background:#f5f7fa;color:var(--text-base);font-weight:500;padding:10px 12px;text-align:left;border-bottom:1px solid var(--border-soft);white-space:nowrap}
.audit-table td{padding:10px 12px;border-bottom:1px solid var(--divider-thin);color:var(--text-base);vertical-align:top}
.audit-table tbody tr:last-child td{border-bottom:none}
.audit-table tbody tr:nth-child(even){background:#fafbfc}
.audit-table .node{color:var(--text-secondary)}
.audit-table .time{white-space:nowrap;color:var(--text-secondary);font-variant-numeric:tabular-nums}
.audit-table .comment{color:var(--text-secondary);max-width:220px;word-break:break-all}
/* 审批操作胶囊标签（实心圆角，区别于 tag 浅底） */
.tag-pill{display:inline-flex;align-items:center;padding:2px 8px;border-radius:10px;font-size:12px;font-weight:500;line-height:18px}
.tag-pill-success{background:var(--success);color:#fff}
.tag-pill-error{background:var(--error);color:#fff}
.tag-pill-warning{background:var(--warning);color:#fff}
.tag-pill-info{background:var(--primary);color:#fff}
.tag-pill-default{background:#e8ebed;color:var(--text-secondary)}
```
审批记录弹窗结构：`modal-mask > modal.modal-audit`，含 `modal-h`（标题"审批记录" + 关闭 ✕）、`modal-b`（`.audit-table` 表格，列：流程节点 / 处理人 / 处理时间 / 审批操作 / 审批意见）、`modal-f`（居中"关闭"按钮，`.modal-audit .modal-f{justify-content:center}`）。审批操作列用 `tag-pill` 实心胶囊，按动作匹配颜色：启动→info(蓝)、通过→success(绿)、拒绝→error(红)、待审批/撤回→warning(橙)、取消/默认→default(灰)。处理时间格式 `YYYY-MM-DD HH:MM:SS`。

---

## 9.2 按星期不可用时间编辑器（unavail-list / week-chk）

```css
/* 会议室"按星期不可用时间"编辑器 */
.unavail-list{display:flex;flex-direction:column;gap:6px;margin-bottom:8px}
.unavail-empty{font-size:12px;color:var(--text-tertiary);padding:4px 0}
.unavail-item{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:6px 10px;border:1px solid var(--border-soft);border-radius:4px;background:var(--bg-page);font-size:13px}
.unavail-add{border:1px dashed var(--border-soft);border-radius:4px;padding:10px;background:#fff}
.week-chk{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:8px}
.week-chk label{display:inline-flex;align-items:center;gap:3px;font-size:12px;padding:2px 8px;border:1px solid var(--border-soft);border-radius:12px;cursor:pointer;background:var(--bg-page)}
.week-chk input{margin:0;cursor:pointer}
.unavail-add .tf-row{margin-bottom:8px}
```
结构：`unavail-list`（已添加条目，每条 `.unavail-item` 显示"周一/三/五 09:00-10:00" + 删除按钮）；`unavail-add`（`.week-chk` 星期多选胶囊 + `.tf-row` 开始/结束时间下拉 + "添加不可用时间"按钮）。提交的 `unavailable` 数组形如 `{days:[1,3,5],start:'09:00',end:'10:00'}`。占用甘特图用橙色斜纹 `.occ-bar.weekly` 展示每周该时段不可用。

---

## 9.3 工作台横幅（wb-banner）

工作台首页顶部的总览提示条，有待办时高亮。

```css
.wb-banner{display:flex;align-items:center;justify-content:space-between;padding:16px 20px;margin-bottom:14px;border-radius:6px;cursor:pointer;
  background:linear-gradient(90deg,#eef2ff,#f7f9ff);border:1px solid #e2e8f7;transition:box-shadow .15s}
.wb-banner.has-task{background:linear-gradient(90deg,#fff7e8,#fffdf7);border-color:#ffe2b8}
.wb-banner:hover{box-shadow:0 2px 10px rgba(75,116,240,.12)}
.wb-banner-l{display:flex;align-items:center;gap:14px}
.wb-banner-num{font-size:30px;font-weight:700;color:var(--warning);line-height:1}
.wb-banner-txt{font-size:13px;color:var(--text-secondary)}
.wb-banner-btn{font-size:13px;color:var(--primary);font-weight:500}
```
结构：`.wb-banner`（有任务加 `.has-task`）内 `.wb-banner-l`（左侧：`.wb-banner-num` 大数字 + `.wb-banner-txt` 文案）+ 右侧 `.wb-banner-btn`（如"前往审批中心 →"）。整条可点击跳转。未有待办时显示中性灰蓝底、数字为 0。

---

## 9.4 审批详情页（ad-* 详情网格 / 操作卡片 / 评论 / 时间占用）

审批中心进入详情后的主体：四列信息网格 + 24h 时间占用条 + 操作按钮卡片 + 审批记录/评论分段。

```css
/* 详情信息网格（4 列，整行项 .full） */
.ad-detail{display:grid;grid-template-columns:repeat(4,1fr);gap:16px 20px;padding:18px 20px}
.ad-item{display:flex;flex-direction:column;gap:4px}
.ad-item.full{grid-column:1 / -1}
.ad-label{font-size:12px;color:var(--text-tertiary)}
.ad-value{font-size:13px;color:var(--text-base);font-weight:500}

/* 操作按钮卡片（同意/批注/退回/评论/拒绝/返回） */
.ad-actions{display:flex;justify-content:center;gap:12px;flex-wrap:wrap}
.ad-actions-card{background:#fff;border:1px solid var(--border-soft);border-radius:6px;padding:14px 16px;margin-top:14px}

/* 详情内分段（审批记录 / 评论） */
.ad-tabs{margin-top:4px}
.ad-section{padding:16px 20px}
.ad-section-title{font-size:14px;font-weight:600;color:var(--text-base);margin-bottom:12px}

/* 评论区 */
.ad-comment-list{display:flex;flex-direction:column;gap:10px;margin-bottom:14px}
.ad-comment{padding:10px 12px;background:var(--bg-page);border-radius:4px;border:1px solid var(--border-soft)}
.ad-comment-h{display:flex;justify-content:space-between;margin-bottom:4px}
.ad-comment-user{font-size:13px;font-weight:600;color:var(--text-base)}
.ad-comment-time{font-size:12px;color:var(--text-tertiary)}
.ad-comment-body{font-size:13px;color:var(--text-secondary);line-height:1.5;word-break:break-all}
.ad-comment-form{display:flex;gap:10px;align-items:flex-start}
.ad-comment-form .input{flex:1;resize:vertical}

/* 详情页 24h 时间占用条（可预约蓝 / 已被预约灰 / 当前会议深蓝） */
.ad-timeline{margin:0 0 16px}
.ad-tl-title{font-size:14px;font-weight:600;color:var(--text-base);margin-bottom:10px}
.ad-tl-wrap{display:flex;flex-direction:column}
.ad-tl-labels{display:flex;height:16px;margin-bottom:2px}
.ad-tl-lbl{flex:1;text-align:center;font-size:9px;color:var(--text-tertiary);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ad-tl-track{display:flex;height:28px;border-radius:3px;overflow:hidden;border:1px solid var(--border-soft)}
.ad-tl-cell{flex:1;border-right:1px solid var(--border-soft);background:#d6e4ff}
.ad-tl-cell:last-child{border-right:none}
.ad-tl-cell.occupied{background:#d7d9dd}
.ad-tl-cell.current{background:#4B74F0}
.ad-tl-legend{display:flex;gap:16px;margin-top:8px;font-size:12px;color:var(--text-tertiary)}
.ad-tl-dot{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:4px;vertical-align:middle}
.ad-tl-dot.free{background:#d6e4ff;border:1px solid var(--border-soft)}
.ad-tl-dot.occupied{background:#d7d9dd}
.ad-tl-dot.current{background:#4B74F0;border:1px solid var(--primary)}
```
审批详情页结构：`card.ad-detail`（`.ad-item` 四列网格，整行项加 `.full`）+ `renderDayTimeline()` 渲染的 `.ad-timeline` + `card.ad-actions-card`（`.ad-actions` 内放按钮：待审批时显示 `同意(btn-success)/批注(btn-primary)/退回(btn-primary)/评论(btn-primary)/拒绝(btn-danger)/返回(btn-plain)`，已处理后仅显示 `评论/返回`）+ `seg-tabs.ad-tabs`（审批记录 / 评论两个分段）+ `card.ad-section`（切换内容：审批记录表用 `.audit-table`、评论用 `.ad-comment-list` + `.ad-comment-form` 文本域）。状态列用 `statusTag()`（同意/待审批/已拒绝/已取消）。

---

## 10. 表单网格（form-grid）

```css
.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px 20px}
.form-item{display:flex;flex-direction:column;gap:4px}
.form-item.full{grid-column:span 2}
.form-item label{font-size:12px;color:var(--text-secondary)}
.form-item label .req{color:var(--error)}
.form-item .input,.form-item .select,.form-item textarea{width:100%}
.tf-row{display:flex;gap:20px}
.tf-col{flex:1;display:flex;flex-direction:column;gap:4px}
.detail-list{display:flex;flex-direction:column;gap:2px}
.dl-row{display:flex;gap:12px;padding:9px 4px;border-bottom:1px solid var(--divider-thin)}
.dl-row:last-child{border-bottom:none}
.dl-k{flex:0 0 92px;color:var(--text-tertiary);font-size:13px}
.dl-v{flex:1;color:var(--text-base);font-size:13px;word-break:break-all}
```
弹窗表单：`.form-grid` 两列布局，整行字段加 `.full`；时间区间用 `.tf-row` + 两个 `.tf-col`（开始/结束各占一半）。必填标记用 `<span class="req">*</span>`。

---

## 11. 时间轴 / 24h 占用甘特图（room-timeline）

```css
/* 24h 时间占用条：每小时一格，hover 显示时段；可预约=蓝 / 已占用=灰 / 已选=黄 */
.room-timeline{display:flex;flex-direction:column;gap:4px}
.timeline-labels{display:flex;height:22px;align-items:center}
.timeline-hour{flex:1;text-align:center;font-size:11px;color:var(--text-tertiary);
  border-right:1px solid var(--border-soft);line-height:20px;min-width:26px}
.timeline-hour:last-child{border-right:none}
.timeline-bars{display:flex;height:34px;border-radius:3px;overflow:hidden;border:1px solid var(--border-soft)}
.timeline-cell{flex:1;min-width:26px;border-right:1px solid #fff;position:relative;
  background:#d6e4ff; /* free: blue (bookable) */
  cursor:pointer;transition:background .12s}
.timeline-cell:last-child{border-right:none}
.timeline-cell.occupied{background:#c9ced6;cursor:not-allowed} /* occupied: gray */
.timeline-cell.selected{background:#ffd54f} /* selected: yellow */
.timeline-cell:hover{background:#ffd54f}
.timeline-cell.occupied:hover{background:#c9ced6}
.timeline-cell:hover::after{content:attr(data-hour);position:absolute;left:50%;top:-22px;transform:translateX(-50%);
  background:rgba(0,0,0,.75);color:#fff;font-size:10px;padding:2px 6px;border-radius:3px;white-space:nowrap;z-index:10}
.timeline-legend{display:flex;gap:16px;align-items:center;font-size:12px;color:var(--text-secondary);margin-top:6px}
.timeline-legend .lg{display:flex;align-items:center;gap:5px}
.timeline-legend .sw{width:14px;height:10px;border-radius:2px;display:inline-block}
.timeline-legend .sw.blue{background:#d6e4ff}
.timeline-legend .sw.gray{background:#c9ced6}
.timeline-legend .sw.yellow{background:#ffd54f}
```
结构：`.room-timeline` > `.timeline-labels`（24 个 `.timeline-hour`，每整点 `00:00`/`01:00`…）+ `.timeline-bars`（24 个 `.timeline-cell`，空闲默认蓝 `free`、占用加 `.occupied` 灰、用户选中加 `.selected` 黄）。单元格 `data-hour` 属性用于 hover 浮层显示时段。底部 `.timeline-legend`（蓝=可预约 / 灰=已占用 / 黄=已选）。
颜色语义：可预约=蓝、已占用=灰、已选=黄（通用"可预约=蓝"语义，与品牌主色一致）。该条用于「会议室占用」页与预订表单选时段；审批详情页的占用条见 §9.4 `.ad-timeline`。

---

## 12. HTML 模板骨架（见 assets/template.html）

生成页面时，复制 `assets/template.html` 作为起点：它已包含上面的 tokens、布局骨架（header + sidebar + tab-bar + main）和示例组件（filter-card、card、dt 表格、pager），只需替换菜单项、标题、表格列与数据。
