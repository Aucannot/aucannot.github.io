---
title: "Diffusion Cache 综述"
date: 2026-04-22 14:47:27 +0800
categories: ["inference-acceleration"]
tags: [diffusion-models, inference-acceleration, cache, generative-models]
math: true
---

Diffusion model 的推理加速主要包括 cache、量化、剪枝、蒸馏等，另外的还有分布式推理、采样器优化等。

最近在思考如何设计一个好的 cache 方案，于是先从阅读理解论文开始。

# why DiT cache ?

首先来讲讲 `cache` 这个概念。如果有过编程经验的话，对这个词应该并不陌生。我觉得这个单词的核心就是空间换时间。它可以是省略 io 操作的 cache，也可以是跳过计算的 cache。这里的 Dit cache 属于后者。

## 为什么 diffusion model 可以 cache 呢？

在 diffusion model 的推理过程中， U-Net 和 DiT 在 forward 中实际上扮演着“去噪预测器“的作用。它们输入 noisy sample $x_t$，timestep $t$，以及 condition $c$，推理预测出噪声 $\epsilon$，clean sample $x_0$ 或者 velocity $v$ 等用于更新采样状态的量。真正的状态更新 $x_t\rightarrow x_{t-1}$ 由 sampler/scheduler 根据这些推理结果完成。

在训练过程中，DDPM 的 forward noising process 定义了一个从干净图像样本 $x_0$ 到高噪声样本 $x_T$ 的逐步加入高斯噪声的马尔科夫链；timestep t 越大，$x_t$ 的噪声比例就越高，越接近高斯噪声图。

对应的单步前向加噪分布可以写成：

$$
q(x_t \mid x_{t-1}) = \mathcal{N}(\sqrt{1-\beta_t}x_{t-1}, \beta_t I)
$$

我原本以为 diffusion model的 denoising process 其实就是 ddpm noising process 的逆过程，因此在逐步推理时，去噪的幅度会逐步减小，因此可以做 cache 跳过某些 denoising process steps，让变化小的几步合并成变化大的一步。 但实际并非如此，因为去噪过程并不是加噪过程的简单确定性逆过程，并且单步更新的幅度也不必然随着 timestep 单调减小，而是取决于 scheduler、noise schedule、模型参数和当前 sample。

DiT cache 真正利用的是 denoising trajectory 在时间维度上的局部冗余：相邻 timestep 的输入、模型输出或中间 feature 往往具有较高相似性。因此可以在某些 timestep 中复用/cache 之前计算过的中间结果，近似计算替代一些 module 的  forward。

## DiT cache 具体 cache 什么？