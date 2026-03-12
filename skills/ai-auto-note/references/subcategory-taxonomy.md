# AI Auto Note Subcategory Taxonomy

Use exactly one subcategory per post.

## Candidate subcategories

- `llm-basics`：模型机制、提示工程基础、上下文管理。
- `reasoning`：推理链、思维框架、问题拆解。
- `coding`：代码生成、重构、调试、工程实践。
- `tooling`：Agent、函数调用、自动化工作流、MCP。
- `math`：线代、概率、优化、算法推导。
- `paper-reading`：论文精读、方法对比、实验解读。
- `deployment`：推理部署、性能优化、服务化。
- `evaluation`：评测基准、A/B、幻觉与可靠性。
- `productivity`：学习方法、知识管理、复盘策略。
- `career`：成长路线、能力模型、项目规划。

## Selection rules

1. Prefer the subcategory that matches the main output, not side discussion.
2. If two are close, choose the one that produces clearer future retrieval.
3. Keep naming stable over time; avoid creating ad-hoc categories unless user asks.

## Quick mapping examples

- “如何让模型输出更稳定” -> `reasoning` 或 `evaluation`（以核心目标判断）。
- “把一段脚本改成可维护结构” -> `coding`。
- “总结一篇新论文并提炼方法” -> `paper-reading`。
- “多轮对话后形成学习计划” -> `productivity`。
