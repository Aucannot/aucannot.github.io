---
name: ai-auto-note
description: "Summarize completed AI learning conversations into publishable Jekyll blog posts for this repository. Use when the user asks to整理学习结论、沉淀对话成果、自动生成笔记、或把学习记录上传到仓库，并希望统一主分类为 ai-auto-note 且自动分配子分类。"
---

# AI Auto Note

## Overview

Convert finalized learning conversations into structured, publication-ready notes under `_posts/`, with consistent metadata and stable categorization.

## Workflow

1. Confirm the source material is conclusion-ready.
2. Extract key conclusions, evidence, and next actions.
3. Map the note to one subcategory using `references/subcategory-taxonomy.md`.
4. Generate a new post file from `assets/post-template.md`.
5. Save the file to `_posts/YYYY-MM-DD-ai-auto-note-<slug>.md`.
6. Keep `categories` in this exact order:
   - `ai-auto-note`
   - `<subcategory>`

## Output Rules

- Write in Chinese by default unless the user requests another language.
- Keep the title specific and outcome-oriented.
- Use short paragraphs and bullet lists for scanability.
- Include only high-signal content; remove chat noise.
- Ensure the post is self-contained and understandable without the original chat.

## Frontmatter Rules

Always generate frontmatter with these keys:

```yaml
---
title: "<note title>"
date: <YYYY-MM-DD HH:MM:SS +0800>
categories: [ai-auto-note, <subcategory>]
tags: [<tag1>, <tag2>, <tag3>]
---
```

Constraints:

- Keep `ai-auto-note` as the first category every time.
- Select exactly one subcategory from the taxonomy reference.
- Use 3-6 tags.

## Content Structure

Follow this section order:

1. `## TL;DR`
2. `## 背景与问题`
3. `## 核心结论`
4. `## 可复用方法`
5. `## 后续行动`

If the source includes references, append:

- `## 参考资料`

## Quality Checklist

Before finishing:

- Verify the filename date matches frontmatter date.
- Verify the post has both primary and secondary categories.
- Verify conclusions are actionable, not only descriptive.
- Verify no confidential content is copied by accident.
