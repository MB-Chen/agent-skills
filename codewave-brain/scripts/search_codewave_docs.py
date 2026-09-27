#!/usr/bin/env python3
"""Search bundled CodeWave Markdown docs.

The script intentionally uses only Python stdlib so the skill works in a
fresh Codex environment.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
DOCS_DIR = SKILL_ROOT / "references" / "docs"

URL_RE = re.compile(r"https?://[^\s\)\"'<>]+")
MD_IMAGE_RE = re.compile(r"!\[[^\]]*\]\((https?://[^\)]+)\)")
HTML_IMAGE_RE = re.compile(r"<img[^>]+src=[\"'](https?://[^\"']+)[\"']", re.I)
HEADING_RE = re.compile(r"^(#{1,4})\s+(.+?)\s*$", re.M)
TAG_RE = re.compile(r"<[^>]+>")
CJK_RE = re.compile(r"[\u4e00-\u9fff]+")
TOKEN_RE = re.compile(r"[a-zA-Z0-9_.-]+|[\u4e00-\u9fff]+")


STOPWORDS = {
    "codewave",
    "CodeWave",
    "怎么",
    "如何",
    "怎样",
    "什么",
    "哪些",
    "哪个",
    "一下",
    "一个",
    "一些",
    "通过",
    "使用",
    "实现",
    "低代码",
    "平台",
    "业务",
    "功能",
    "方案",
    "思路",
    "官方",
    "文档",
    "告诉",
    "回答",
    "请问",
    "需要",
    "可以",
    "进行",
    "创建",
    "配置",
    "用",
    "和",
    "与",
    "是",
    "的",
    "分别",
}


MODE_HINTS = {
    "business": ["常见场景案例", "最佳实践", "实现第一个业务功能", "流程设计", "权限模块", "逻辑功能实现"],
    "concept": ["平台介绍", "新手入门", "平台基础概念介绍", "最佳实践"],
    "component": ["组件清单", "组件说明", "页面设计", "PC端Vue2组件说明", "PC端Vue3组件说明"],
    "integration": ["扩展与集成", "OpenAPI", "服务端扩展开发", "接口"],
    "ops": ["应用生命周期管理", "平台运维管理", "平台配置管理", "权限管理"],
}


@dataclass
class Doc:
    path: Path
    rel: str
    text: str
    clean: str
    title: str
    headings: list[str]
    images: list[str]
    urls: list[str]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def clean_markdown(text: str) -> str:
    text = html.unescape(text)
    text = TAG_RE.sub(" ", text)
    text = re.sub(r"!\[[^\]]*\]\([^\)]*\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^\)]*\)", r"\1", text)
    text = re.sub(r"[`*_>#|~-]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def load_docs() -> list[Doc]:
    docs: list[Doc] = []
    for path in sorted((p for p in DOCS_DIR.rglob("*.md") if p.is_file()), key=lambda p: str(p)):
        text = read_text(path)
        rel = path.relative_to(DOCS_DIR).as_posix()
        headings = [m.group(2).strip() for m in HEADING_RE.finditer(text)]
        title = headings[0] if headings else path.stem
        images = sorted(set(MD_IMAGE_RE.findall(text) + HTML_IMAGE_RE.findall(text)))
        urls = sorted(set(URL_RE.findall(text)))
        docs.append(
            Doc(
                path=path,
                rel=rel,
                text=text,
                clean=clean_markdown(text),
                title=title,
                headings=headings[:30],
                images=images,
                urls=urls,
            )
        )
    return docs


def infer_mode(query: str) -> str:
    q = query.lower()
    if any(k in query for k in ["场景", "案例", "业务", "怎么做", "怎么实现", "实现思路", "审批", "订单", "流程"]):
        return "business"
    if any(k in query for k in ["概念", "理论", "是什么", "区别", "定义", "原理", "为什么"]):
        return "concept"
    if any(k in query for k in ["组件", "表格", "按钮", "页面", "样式", "事件", "属性"]):
        return "component"
    if any(k in query for k in ["接口", "openapi", "集成", "扩展", "依赖库", "api"]) or "openapi" in q:
        return "integration"
    if any(k in query for k in ["发布", "部署", "运维", "权限", "环境", "配置"]):
        return "ops"
    return "general"


def cjk_ngrams(text: str) -> set[str]:
    grams: set[str] = set()
    for chunk in CJK_RE.findall(text):
        chunk = remove_stopwords(chunk)
        if len(chunk) >= 2:
            grams.add(chunk)
        for n in (2, 3, 4):
            for i in range(0, max(0, len(chunk) - n + 1)):
                gram = chunk[i : i + n]
                if gram and gram not in STOPWORDS:
                    grams.add(gram)
    return grams


def remove_stopwords(text: str) -> str:
    result = text
    for word in sorted(STOPWORDS, key=len, reverse=True):
        result = result.replace(word, "")
    return result


def query_terms(query: str) -> list[str]:
    raw_terms: set[str] = set()
    for token in TOKEN_RE.findall(query):
        if token in STOPWORDS or token.lower() in STOPWORDS:
            continue
        if re.fullmatch(r"[a-zA-Z0-9_.-]+", token):
            if len(token) >= 2:
                raw_terms.add(token.lower())
            continue
        cleaned = remove_stopwords(token)
        if len(cleaned) >= 2:
            raw_terms.add(cleaned)
        raw_terms.update(cjk_ngrams(token))

    # 长词更能表达意图，优先用于摘要定位。
    return sorted(raw_terms, key=lambda t: (-len(t), t))


def mode_boost(rel: str, mode: str) -> int:
    if mode == "auto":
        mode = "general"
    hints = MODE_HINTS.get(mode, [])
    score = 0
    for hint in hints:
        if hint.lower() in rel.lower():
            score += 18
    if mode == "business" and rel.startswith(("80.", "85.", "10.", "20.")):
        score += 8
        if "实现第一个业务功能" in rel:
            score += 90
        if rel.startswith("80.常见场景案例"):
            score += 45
        if rel.startswith("85.最佳实践"):
            score += 35
    if mode == "concept" and rel.startswith(("05.", "10.")):
        score += 10
        if "平台基础概念介绍" in rel:
            score += 160
        if rel == "05.平台介绍.md":
            score += 80
    return score


def score_doc(doc: Doc, terms: list[str], query: str, mode: str) -> int:
    hay_title = doc.title.lower()
    hay_path = doc.rel.lower()
    hay_headings = " ".join(doc.headings).lower()
    hay_text = doc.clean.lower()
    score = mode_boost(doc.rel, mode)

    q_norm = query.strip().lower()
    if q_norm and q_norm in hay_text:
        score += 60

    for term in terms:
        t = term.lower()
        if t in hay_title:
            score += 35 + min(len(t), 8)
        if t in hay_path:
            score += 25 + min(len(t), 8)
        if t in hay_headings:
            score += 18 + min(len(t), 8)
        count = hay_text.count(t)
        if count:
            score += min(24, count * 4) + min(len(t), 6)

    return score


def snippet(doc: Doc, terms: list[str], max_chars: int) -> str:
    clean = doc.clean
    lower = clean.lower()
    positions = [lower.find(t.lower()) for t in terms if lower.find(t.lower()) >= 0]
    if positions:
        pos = min(positions)
        start = max(0, pos - max_chars // 3)
        end = min(len(clean), start + max_chars)
    else:
        start, end = 0, min(len(clean), max_chars)
    body = clean[start:end].strip()
    if start > 0:
        body = "..." + body
    if end < len(clean):
        body += "..."
    return body


def print_result(doc: Doc, terms: list[str], score: int, max_chars: int) -> None:
    print(f"## {doc.title}")
    print(f"- score: {score}")
    print(f"- path: references/docs/{doc.rel}")
    if doc.headings[1:8]:
        print(f"- headings: {' / '.join(doc.headings[1:8])}")
    if doc.images:
        print(f"- image_urls: {len(doc.images)} total; first: {doc.images[0]}")
    elif doc.urls:
        print(f"- urls: {len(doc.urls)} total; first: {doc.urls[0]}")
    print()
    print(snippet(doc, terms, max_chars))
    print()


def show_path(rel_path: str, max_chars: int) -> int:
    target = (DOCS_DIR / rel_path).resolve()
    try:
        target.relative_to(DOCS_DIR.resolve())
    except ValueError:
        print(f"Refuse to read outside docs: {target}", file=sys.stderr)
        return 2
    if not target.exists():
        print(f"Not found: references/docs/{rel_path}", file=sys.stderr)
        return 1
    text = read_text(target)
    images = sorted(set(MD_IMAGE_RE.findall(text) + HTML_IMAGE_RE.findall(text)))
    print(f"# references/docs/{target.relative_to(DOCS_DIR).as_posix()}")
    if images:
        print(f"\nImage URLs ({len(images)}):")
        for url in images[:30]:
            print(f"- {url}")
        if len(images) > 30:
            print(f"- ... {len(images) - 30} more")
        print()
    if max_chars and len(text) > max_chars:
        print(text[:max_chars])
        print(f"\n...[truncated, {len(text)} chars total]")
    else:
        print(text)
    return 0


def write_catalog(docs: list[Doc], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as f:
        for doc in docs:
            f.write(
                json.dumps(
                    {
                        "path": f"references/docs/{doc.rel}",
                        "title": doc.title,
                        "headings": doc.headings[:12],
                        "image_url_count": len(doc.images),
                        "url_count": len(doc.urls),
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )


def main() -> int:
    parser = argparse.ArgumentParser(description="Search bundled CodeWave Markdown docs.")
    parser.add_argument("query", nargs="?", help="Question or keywords to search for.")
    parser.add_argument("--top", type=int, default=8, help="Number of results to print.")
    parser.add_argument("--mode", choices=["auto", "general", "business", "concept", "component", "integration", "ops"], default="auto")
    parser.add_argument("--max-chars", type=int, default=900, help="Snippet/full-file character limit.")
    parser.add_argument("--path", help="Print one doc by relative path under references/docs.")
    parser.add_argument("--jsonl", action="store_true", help="Emit JSONL result metadata instead of snippets.")
    parser.add_argument("--write-catalog", help="Write a JSONL catalog and exit.")
    args = parser.parse_args()

    if args.path:
        return show_path(args.path, args.max_chars)

    docs = load_docs()
    if args.write_catalog:
        write_catalog(docs, Path(args.write_catalog))
        return 0

    query = args.query or ""
    mode = infer_mode(query) if args.mode == "auto" else args.mode
    terms = query_terms(query)
    scored = [(score_doc(doc, terms, query, mode), doc) for doc in docs]
    scored = [(score, doc) for score, doc in scored if score > 0]
    scored.sort(key=lambda item: (-item[0], item[1].rel))

    print(f"Query: {query}")
    print(f"Mode: {mode}")
    print(f"Terms: {', '.join(terms[:20]) if terms else '(none)'}")
    print(f"Docs searched: {len(docs)}")
    print()

    for score, doc in scored[: args.top]:
        if args.jsonl:
            print(
                json.dumps(
                    {
                        "score": score,
                        "path": f"references/docs/{doc.rel}",
                        "title": doc.title,
                        "headings": doc.headings[:12],
                        "image_urls": doc.images[:5],
                        "snippet": snippet(doc, terms, args.max_chars),
                    },
                    ensure_ascii=False,
                )
            )
        else:
            print_result(doc, terms, score, args.max_chars)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
