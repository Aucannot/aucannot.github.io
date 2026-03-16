#!/usr/bin/env python3
"""Generate a Jekyll post under _posts/ai-auto-note/<subcategory>/ from learning notes."""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path

CATEGORY = "ai-auto-note"

SUBCATEGORY_KEYWORDS = {
    "llm": ["llm", "大模型", "transformer", "attention", "token"],
    "prompting": ["prompt", "提示词", "system prompt", "cot", "chain-of-thought"],
    "rag": ["rag", "检索", "向量数据库", "embedding", "召回", "retrieval", "rerank", "chunk"],
    "agents": ["agent", "tool call", "function calling", "多智能体", "工作流"],
    "training": ["finetune", "sft", "rlhf", "训练", "蒸馏"],
    "evaluation": ["benchmark", "eval", "评测", "幻觉", "hallucination"],
    "deployment": ["部署", "serving", "latency", "吞吐", "inference"],
    "paper-reading": [
        "paper",
        "论文",
        "arxiv",
        "method",
        "实验",
        "ablation",
        "baseline",
        "sota",
    ],
    "productivity": ["复盘", "学习计划", "todo", "行动项", "习惯", "时间管理"],
}

VALID_SUBCATEGORIES = set(SUBCATEGORY_KEYWORDS) | {"general"}

WORD_LIKE_KEYWORDS = {
    "llm",
    "transformer",
    "attention",
    "token",
    "prompt",
    "cot",
    "rag",
    "embedding",
    "agent",
    "benchmark",
    "eval",
    "hallucination",
    "inference",
    "latency",
    "serving",
    "paper",
    "arxiv",
    "method",
    "ablation",
    "baseline",
    "sota",
    "todo",
}

METADATA_PREFIXES = (
    "title:",
    "title：",
    "paper title:",
    "paper title：",
    "论文标题:",
    "论文标题：",
    "链接:",
    "链接：",
    "link:",
    "link：",
    "arxiv:",
    "arxiv：",
)


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff\s-]", "", text).strip().lower()
    slug = re.sub(r"\s+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug[:80] or "ai-note"


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


def _keyword_hit(normalized_text: str, keyword: str) -> bool:
    """Match English keywords with word boundary, CJK keywords by substring."""
    keyword_lower = keyword.lower().strip()
    if not keyword_lower:
        return False

    if keyword_lower in WORD_LIKE_KEYWORDS:
        return re.search(rf"\b{re.escape(keyword_lower)}\b", normalized_text) is not None

    return keyword_lower in normalized_text


def classify_subcategory(text: str) -> str:
    text_lower = _normalize_text(text)
    scores: dict[str, int] = {}
    for name, keywords in SUBCATEGORY_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if _keyword_hit(text_lower, kw):
                score += 2 if kw.lower() == name else 1
        scores[name] = score

    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "general"


def _is_metadata_line(line: str) -> bool:
    lower = line.strip().lower()
    if lower.startswith(METADATA_PREFIXES):
        return True

    # Skip pure arXiv URL lines, but keep explanatory sentences that merely contain a URL.
    pure_arxiv_url = re.fullmatch(
        r"https?://arxiv\.org/(?:abs|pdf)/\d{4}\.\d{4,5}(?:v\d+)?/?",
        lower,
    )
    return pure_arxiv_url is not None


def summarize_points(content: str, max_points: int = 6) -> list[str]:
    lines = [ln.strip(" -\t") for ln in content.splitlines() if ln.strip()]
    points = []
    for line in lines:
        if len(line) < 8 or _is_metadata_line(line):
            continue
        points.append(line)
        if len(points) >= max_points:
            break

    return points if points else ["本次学习暂无可提炼要点，请补充上下文后重新生成。"]


def _yaml_escaped(value: str) -> str:
    return value.replace('"', '\\"')


def _normalize_subcategory(value: str) -> str:
    return re.sub(r"[^a-z0-9-]", "", value.lower()) or "general"


def _validate_forced_subcategory(value: str | None, parser: argparse.ArgumentParser) -> str | None:
    if value is None:
        return None

    normalized = _normalize_subcategory(value)
    if normalized not in VALID_SUBCATEGORIES:
        allowed = ", ".join(sorted(VALID_SUBCATEGORIES))
        parser.error(f"Invalid --subcategory '{value}'. Allowed values: {allowed}")
    return normalized


def _collect_tags(subcategory: str, source_text: str) -> list[str]:
    tags: list[str] = [CATEGORY, subcategory]
    normalized_text = _normalize_text(source_text)
    topic_tags = {
        "llm": ["transformer", "token", "attention", "大模型"],
        "rag": ["retrieval", "检索", "embedding", "向量"],
        "agents": ["agent", "tool", "workflow", "多智能体"],
        "prompting": ["prompt", "提示词", "cot"],
        "evaluation": ["eval", "benchmark", "评测", "hallucination"],
        "training": ["sft", "rlhf", "finetune", "训练", "蒸馏"],
        "deployment": ["inference", "serving", "部署", "latency"],
        "paper-reading": ["paper", "arxiv", "method", "实验", "ablation"],
        "productivity": ["复盘", "行动项", "计划", "时间管理", "学习方法"],
    }

    for tag, markers in topic_tags.items():
        if tag == subcategory:
            continue
        if any(_keyword_hit(normalized_text, marker) for marker in markers):
            tags.append(tag)

    return tags[:5]


def _extract_field_value(line: str, field: str) -> str | None:
    pattern = rf"^\s*{re.escape(field)}\s*[:：]\s*(.+?)\s*$"
    match = re.match(pattern, line, flags=re.IGNORECASE)
    if match:
        value = match.group(1).strip()
        return value or "待补充"
    return None


def _extract_paper_title(source_text: str) -> str:
    lines = [ln.strip() for ln in source_text.splitlines() if ln.strip()]
    title_fields = ("title", "paper title", "论文标题")
    for line in lines:
        for field in title_fields:
            value = _extract_field_value(line, field)
            if value is not None:
                return value

    quoted = re.search(r"[《\"]([^》\"]{8,160})[》\"]", source_text)
    if quoted:
        return quoted.group(1).strip()

    return "待补充"


def _extract_arxiv_link(source_text: str) -> str:
    match = re.search(r"https?://arxiv\.org/(?:abs|pdf)/\d{4}\.\d{4,5}(?:v\d+)?", source_text, re.IGNORECASE)
    if match:
        return match.group(0)
    return "待补充"


def build_post(
    title: str,
    source_text: str,
    date: dt.date,
    forced_subcategory: str | None = None,
) -> tuple[str, str]:
    subcategory = forced_subcategory or classify_subcategory(f"{title}\n{source_text}")
    bullets = summarize_points(source_text)
    tags = _collect_tags(subcategory, source_text)

    body = [
        "## 背景",
        "",
        "本篇为学习对话自动沉淀的笔记，保留结论和可复用要点。",
        "",
    ]

    if subcategory == "paper-reading":
        paper_title = _extract_paper_title(source_text)
        arxiv_link = _extract_arxiv_link(source_text)
        body.extend(
            [
                "## 论文信息",
                "",
                f"- 论文标题：{paper_title}",
                "- 核心任务：待补充",
                "- 主要贡献：待补充",
                f"- 链接：{arxiv_link}",
                "",
                "## 方法与实验要点",
                "",
            ]
        )

    body.extend([
        "## 结论速记",
        "",
    ])
    body.extend([f"- {point}" for point in bullets])
    body.extend(
        [
            "",
            "## 后续行动",
            "",
            "- [ ] 把结论应用到一个最小实验中",
            "- [ ] 补充失败案例与边界条件",
        ]
    )

    front_matter = "\n".join(
        [
            "---",
            f'title: "{_yaml_escaped(title)}"',
            f"date: {date.isoformat()} 09:00:00 +0800",
            f'categories: ["{CATEGORY}", "{subcategory}"]',
            "tags: [" + ", ".join(f'\"{tag}\"' for tag in tags) + "]",
            "---",
            "",
        ]
    )

    return subcategory, front_matter + "\n".join(body) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", required=True, help="Post title")
    parser.add_argument(
        "--input",
        required=True,
        help="Path to raw conversation/learning notes text",
    )
    parser.add_argument(
        "--date",
        default=dt.date.today().isoformat(),
        help="Post date in YYYY-MM-DD (default: today)",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root containing _posts",
    )
    parser.add_argument(
        "--subcategory",
        default=None,
        help="Force specific subcategory (e.g. rag/agents/paper-reading/productivity/general)",
    )

    args = parser.parse_args()

    source_path = Path(args.input)
    if not source_path.is_file():
        parser.error(f"Input file not found: {source_path}")

    try:
        source_text = source_path.read_text(encoding="utf-8")
    except OSError as exc:
        parser.error(f"Failed to read input file '{source_path}': {exc}")

    try:
        date = dt.date.fromisoformat(args.date)
    except ValueError as exc:
        parser.error(f"Invalid --date '{args.date}': {exc}")

    forced_subcategory = _validate_forced_subcategory(args.subcategory, parser)

    subcategory, post = build_post(
        title=args.title,
        source_text=source_text,
        date=date,
        forced_subcategory=forced_subcategory,
    )

    output_dir = Path(args.repo_root) / "_posts" / CATEGORY / subcategory
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{date.isoformat()}-{slugify(args.title)}.md"
    output_path = output_dir / filename
    output_path.write_text(post, encoding="utf-8")

    print(output_path)


if __name__ == "__main__":
    main()
