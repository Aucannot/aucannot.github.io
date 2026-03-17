# Subcategory Rules

用于 `ai-auto-note-publisher` 的自动归类规则。

## 当前分类

- `llm`: llm, 大模型, transformer, attention, token
- `prompting`: prompt, 提示词, system prompt, cot, chain-of-thought
- `rag`: rag, 检索, 向量数据库, embedding, 召回, retrieval, rerank, chunk
- `agents`: agent, tool call, function calling, 多智能体, 工作流
- `training`: finetune, sft, rlhf, 训练, 蒸馏
- `evaluation`: benchmark, eval, 评测, 幻觉, hallucination
- `deployment`: 部署, serving, latency, 吞吐, inference
- `paper-reading`: paper, 论文, arxiv, method, 实验, ablation, baseline, sota
- `productivity`: 复盘, 学习计划, todo, 行动项, 习惯, 时间管理
- 默认: `general`

## 调整建议

- 如果某个主题常出现误分类，优先新增关键词而不是新增大量新类。
- 英文关键词建议使用“完整词”匹配（如 `eval` 只匹配独立单词），减少误命中。
- 保持二级分类数量可控（建议 < 12）。


## 元信息提取补充

- arXiv 链接支持两种来源：完整 URL（`https://arxiv.org/abs/...`）和编号格式（`arXiv:2501.12345`）。
- 若识别到编号格式，生成文章时会规范化为 `https://arxiv.org/abs/<id>`。
