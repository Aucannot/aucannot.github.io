---
name: ai-auto-note-publisher
description: 自动把学习对话沉淀成博客笔记并提交到当前仓库。当用户提到“学习总结/自动归档/上传笔记/ai auto note/论文共读/论文总结”时使用。统一写入 categories: ["ai-auto-note", "<auto-subcategory>"]，并按子目录自动归类。
---

# AI Auto Note Publisher

将学习对话整理为可发布的 Jekyll 博客文章，并存入本仓库。

## 何时使用

当用户希望把与 AI 学习（尤其是论文共读）的结论自动沉淀成文档，并上传到仓库时。

## 输出规范

- 路径：`_posts/ai-auto-note/<subcategory>/YYYY-MM-DD-title.md`
- Front matter 固定：
  - `categories: ["ai-auto-note", "<subcategory>"]`
  - `tags`: 至少包含 `"ai-auto-note"` 与 `<subcategory>`
- 正文结构至少包含：
  - `## 背景`
  - `## 结论速记`
  - `## 后续行动`
- 若子分类是 `paper-reading`，额外包含：
  - `## 论文信息`
  - `## 方法与实验要点`

## 快速流程

1. 先和用户完成论文/主题讨论，确认有稳定结论。
2. 准备学习记录文本（例如 `tmp/notes.txt`）。
3. 运行脚本生成文章：

```bash
python3 skills/ai-auto-note-publisher/scripts/create_ai_auto_note.py \
  --title "你的标题" \
  --input tmp/notes.txt \
  --repo-root .

# 如需手动指定二级分类（覆盖自动分类）
python3 skills/ai-auto-note-publisher/scripts/create_ai_auto_note.py \
  --title "你的标题" \
  --input tmp/notes.txt \
  --subcategory paper-reading \
  --repo-root .
```

4. 检查生成内容是否符合语义；若是论文笔记，补全“核心任务/主要贡献”等占位字段。
5. 提交到仓库。
6. 推送分支并自动创建 PR（需 gh CLI 已登录）。

## 子分类策略

脚本会按关键词自动分类（如 `llm`、`prompting`、`rag`、`agents`、`paper-reading` 等），并优先做英文关键词边界匹配（避免 `evaluation` 误命中等情况）。

如未命中关键词，默认分类为 `general`。

详细映射见：`references/subcategory-rules.md`。

脚本会自动从原文提取论文标题（如 `Title:` / `论文标题:` / `《...》`）与 arXiv 链接；未识别时保留“待补充”。

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
