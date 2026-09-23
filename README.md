# Agent Skills

个人开发的 Claude Code / ZCode Agent Skills 合集。每个 skill 一个目录，遵循 [Agent Skills 规范](https://docs.anthropic.com/en/docs/claude-code/skills)（`SKILL.md` + frontmatter 触发描述 + 可选 `scripts/` `references/` `assets/`）。

## 目录

| Skill | 一句话说明 |
|-------|-----------|
| [`q-before-a`](./q-before-a/SKILL.md) | "先澄清，后执行"工作模式：检测到触发词后强制进入只读+提问态，完整读取全部上下文、逐条拆解需求、一次性输出编号澄清清单，用户确认前禁止任何写操作 |

## q-before-a 的设计要点

- **状态机式工作流**：决策树定义 澄清模式 → 读上下文 → 拆需求 → 找疑点 → 输出问题 → 等待确认 六个阶段，两个 🔴 CHECKPOINT 强制暂停，防"为了显得在干活"提前执行；
- **需求拆解三要素模板**（目标 / 范围 / 验收标准），缺失项自动标记为疑点，把"问什么"从凭感觉变成可执行规则；
- **失败模式兜底表**：用户不回复 / 敷衍回复 / 部分回复 / 拒绝回答四种场景各有预定义处理分支（含"默认值标注格式"），解决 agent 遇到模糊输入时行为发散的问题；
- **红灯清单**：把挤牙膏式提问、不读文件就执行、替用户决策等反模式写成绝对禁止项并配对照示例——用负例约束比只写正例稳定得多；
- **可验证迭代**：`test-prompts.json` 保存回归测试用例；`q-before-a-result.png` 是用 skill 优化器（Darwin.skill，SkillLens 九维评分）跑出的 5 轮进化报告（81.0 → 87.2），D9 反例黑名单维度 5→8 是最大突破——迭代过程可复现、指标可追溯。

## 如何使用

把 skill 目录复制到 Claude Code 的 `~/.claude/skills/`（或 ZCode 对应目录）即可被自动发现；触发方式见各 `SKILL.md` frontmatter 的 `description` 字段。
