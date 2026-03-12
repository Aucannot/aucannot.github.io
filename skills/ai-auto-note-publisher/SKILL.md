---
name: ai-auto-note-publisher
description: 自动把学习对话沉淀成博客笔记并提交到当前仓库。当用户提到“学习总结/自动归档/上传笔记/ai auto note”时使用。统一写入 categories: ["ai-auto-note", "<auto-subcategory>"]，并按子目录自动归类。
---

# AI Auto Note Publisher

将学习对话整理为可发布的 Jekyll 博客文章，并存入本仓库。

## 何时使用

当用户希望把与 AI 学习的结论自动沉淀成文档，并上传到仓库时。

## 输出规范

- 路径：`_posts/ai-auto-note/<subcategory>/YYYY-MM-DD-title.md`
- Front matter 固定：
  - `categories: ["ai-auto-note", "<subcategory>"]`
  - `tags: ["ai-auto-note", "<subcategory>"]`
- 正文结构至少包含：
  - `## 背景`
  - `## 结论速记`
  - `## 后续行动`

## 快速流程

1. 准备学习记录文本（例如 `tmp/notes.txt`）。
2. 运行脚本生成文章：

```bash
python3 skills/ai-auto-note-publisher/scripts/create_ai_auto_note.py \
  --title "你的标题" \
  --input tmp/notes.txt \
  --repo-root .

# 如需手动指定二级分类（覆盖自动分类）
python3 skills/ai-auto-note-publisher/scripts/create_ai_auto_note.py \
  --title "你的标题" \
  --input tmp/notes.txt \
  --subcategory rag \
  --repo-root .
```

3. 检查生成内容是否符合语义；必要时微调标题与要点。
4. 提交到仓库。
5. 推送分支并自动创建 PR（需 gh CLI 已登录）。

## 子分类策略

脚本会按关键词自动分类（如 `llm`、`prompting`、`rag`、`agents` 等），并优先做英文关键词边界匹配（避免 `evaluation` 误命中等情况）。

如未命中关键词，默认分类为 `general`。

详细映射见：`references/subcategory-rules.md`。

## 自动推送 PR 到本仓库

准备 PR 描述文件（例如 `tmp/pr-body.md`）后执行：

```bash
bash skills/ai-auto-note-publisher/scripts/push_note_pr.sh \
  --branch feat/ai-auto-note-2026-03-12 \
  --title "feat: add ai auto notes" \
  --body-file tmp/pr-body.md
```

脚本会：
- `git push -u origin <branch>`
- `gh pr create` 自动向仓库默认分支发起 PR。
