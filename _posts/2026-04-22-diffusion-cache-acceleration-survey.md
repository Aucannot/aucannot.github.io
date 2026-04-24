---
title: "Diffusion Cache 综述"
date: 2026-04-22 14:47:27 +0800
categories: ["inference-acceleration"]
tags: [diffusion-models, inference-acceleration, cache, generative-models]
---

Diffusion model 的推理加速主要包括 cache、量化、剪枝、蒸馏等，另外的还有分布式推理、采样器优化等。

最近在思考如何设计一个好的 cache 方案，于是先从阅读理解论文开始。

# why DiT cache ?

首先来讲讲 `cache` 这个概念。如果有过编程经验的话，对这个词应该并不陌生。我觉得这个单词的核心就是空间换时间。它可以是省略 io 操作的 cache，也可以是跳过计算的 cache。这里的 Dit cache 属于后者。

`DiT cache` 的核心思想是