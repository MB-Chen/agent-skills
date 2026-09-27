---
name: codewave-brain
description: CodeWave 大脑。Use this skill whenever the user asks about CodeWave, 网易 CodeWave, the CodeWave low-code platform, CodeWave official docs, entities, pages, logic, workflows, permissions, components, integrations, OpenAPI, deployment, best practices, or asks how to implement a business requirement with low-code. Also use it for low-code theory questions when the answer should be grounded in CodeWave's official documentation, even if the user does not explicitly say "CodeWave".
---

# CodeWave 大脑

这个 Skill 包含 CodeWave 文档中心 v4.5 Markdown 版官方文档的完整本地副本，用于回答 CodeWave 平台知识、低代码理论、业务实现方案、组件配置、流程/权限/集成等问题。

## 可用资料

- 完整官方文档：`references/docs/`
- 文档地图：`references/doc_map.md`
- 文档索引：`references/catalog.jsonl`
- 远程截图 URL 清单：`references/image_links.jsonl`
- 本地检索脚本：`scripts/search_codewave_docs.py`

Markdown 原文中的远程截图 URL 已保留。需要截图证据时，先读取相关 Markdown；如果需要集中查图，再查 `references/image_links.jsonl`。

## 基本原则

先查文档，再回答。不要只凭通用低代码经验回答 CodeWave 问题。

回答时把“文档事实”和“基于文档的实现推断”分开：

- 文档明确说明的内容，直接给结论，并标注来源文件。
- 文档没有直接覆盖但可以由 CodeWave 架构推导的内容，说明这是实现建议或推断。
- 文档找不到依据时，明确说“当前文档中未检索到直接说明”，再给保守建议。

## 检索流程

在回答前运行本地检索脚本，用用户原问题作为 query：

```bash
python scripts/search_codewave_docs.py "<用户问题>" --top 8
```

如果问题类型明确，可以加模式提高命中率：

```bash
python scripts/search_codewave_docs.py "<业务需求>" --mode business --top 10
python scripts/search_codewave_docs.py "<概念/理论问题>" --mode concept --top 8
python scripts/search_codewave_docs.py "<组件/页面/属性问题>" --mode component --top 8
python scripts/search_codewave_docs.py "<接口/扩展/OpenAPI问题>" --mode integration --top 8
python scripts/search_codewave_docs.py "<发布/权限/运维问题>" --mode ops --top 8
```

读取某个命中文档：

```bash
python scripts/search_codewave_docs.py --path "20.应用开发/05.数据建模/20.实体/010.实体介绍.md" --max-chars 12000
```

如需完整读取，将 `--max-chars` 调大或分段读取原始 Markdown 文件。

## 问题路由

### 业务用低代码怎么实现

优先检索并读取：

- `80.常见场景案例/`
- `85.最佳实践/`
- `10.新手入门/090.实现第一个业务功能.md`
- `20.应用开发/05.数据建模/`
- `20.应用开发/10.页面设计/`
- `20.应用开发/15.逻辑功能实现/`
- `20.应用开发/20.流程设计/`
- 权限、集成、生命周期相关目录，按业务需要补充

回答结构建议：

1. 先把业务拆成 CodeWave 构件：实体/枚举/数据结构、页面、逻辑、流程、权限、外部集成。
2. 给出推荐实现路径：先建模，再页面，再逻辑，再流程/权限，再测试发布。
3. 列出关键配置点和需要补充确认的信息。
4. 标注来源文档；如引用截图，给出截图 URL。

### 低代码理论或平台概念

优先检索并读取：

- `05.平台介绍.md`
- `10.新手入门/040.平台基础概念介绍.md`
- `85.最佳实践/105.一文了解应用开发规范.md`
- 与问题关键词对应的专题文档

回答时先给定义，再说明它在 CodeWave 中和数据、页面、逻辑、流程、权限的关系。避免泛泛而谈。

### 具体功能、组件或配置

先查精确关键词，再读取具体文件。常见入口：

- 页面与组件：`20.应用开发/10.页面设计/`
- 数据建模：`20.应用开发/05.数据建模/`
- 逻辑：`20.应用开发/15.逻辑功能实现/`
- 流程：`20.应用开发/20.流程设计/`
- 权限：`20.应用开发/10.页面设计/35.权限模块/`、`45.平台运维管理/20.权限管理.md`
- 扩展集成：`40.扩展与集成/`
- OpenAPI：`97.平台OpenAPI接口文档/`

回答要尽量给可执行步骤，而不是只解释概念。

## 引用来源

回答末尾用简短“参考文档”列出读取过的文件，例如：

- `references/docs/20.应用开发/05.数据建模/20.实体/010.实体介绍.md`
- `references/docs/20.应用开发/15.逻辑功能实现/10.逻辑IDE/10.逻辑IDE介绍.md`

如果答案包含截图依据，也列出相关图片 URL。不要一次贴大量 URL，只列和答案直接相关的 1-3 个。
