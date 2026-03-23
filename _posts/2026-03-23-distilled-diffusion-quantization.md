---
title: "为什么蒸馏后的扩散模型反而更好量化？"
date: 2026-03-23 16:15:00 +0800
categories: ["ai-auto-note", "quantization"]
tags: [diffusion-models, quantization, distillation, generative-models]
math: true
---

> **TL;DR**: 少步数蒸馏优化的是"离散轨迹上的误差"，不一定会让网络内部表征更极端；很多时候反而会让它更规整、更可预测、更适合低比特近似。

---

## 引言：一个反直觉的发现

最近在量化文生图模型时，我遇到了一个有趣的现象：**蒸馏模型的量化效果居然比 base 模型更好**。

这有点反直觉。按照常理，蒸馏模型在更少的步数内完成生成，似乎应该意味着内部激活和参数更加"sharp"（尖锐/极端），量化时应该更困难才对。但实验结果恰恰相反。

经过深入分析，我发现这个现象背后有一系列有趣机制。这篇文章将系统性地拆解这个问题。

---

## 直觉误区："少步数 = 更 Sharp"?

很多人的第一反应是：

> "蒸馏模型用更少步数推理出最终效果，按道理它的激活和参数应该更 sharp，而不是更平滑。"

这里的"sharp"被模糊地理解为：
- 参数分布更分散
- 激活值范围更大
- 对量化噪声更敏感

但问题在于：**"输出空间中收敛更快"不等于"参数空间中更极端"**。这两个概念被混为一谈了。

---

## 核心机制：为什么蒸馏模型更好量化？

### 1. 蒸馏学到的是"平均后的 Teacher 行为"

蒸馏的本质不是直接拟合真实数据分布，而是拟合 teacher 的输出映射。这带来一个关键效果：

**Student 更像一个 smoothed function approximator**。

因为它学的是 teacher 在很多输入上的"稳定响应"，而不是自己去探索所有细碎的自由度。结果是：

- 参数分布更集中
- 某些通道的重要性差异变小
- 激活 outlier 减少
- 对小扰动更不敏感

这些都会让量化更友好。

> **关键区分**：你直觉里的"更 sharp"更像是**输出空间里对一步误差更敏感**，但量化看的是**权重/激活空间里能不能被低精度近似**，这俩不是一回事。

---

### 2. 蒸馏把"多步迭代求解"变成了"直接回归"

Base 模型在很多步里逐渐修正噪声，内部会经历很多"过渡态"。这些过渡态可能带来：

- 时序上更大的 activation range
- 某些 step 特别依赖少量高幅值通道
- 不同步之间统计量漂移更大

而蒸馏模型为了在少步数里直接到位，经常会学出一种**更短、更受约束的轨迹**。它未必更尖，反而可能是把原来长链路里的不稳定中间过程"折叠"掉了。

从量化角度看：

- 不同 timestep 的分布更接近
- Calibration 更容易
- Per-tensor / per-channel scale 更容易覆盖主要质量区域

---

### 3. "输出更快收敛" ≠ "内部 Lipschitz 更大"

一个粗糙的比喻：

- **Base 模型**：像用 20 次小修正走到目标
- **蒸馏模型**：像学会了一条更直的路

"路更短"不代表"每一步更猛"；也可能只是**冗余弯路更少**。

蒸馏模型学到的是**更直接的坐标变换**，不是更剧烈的非线性。

---

### 4. 蒸馏训练带来"隐式正则化"

图像生成里的蒸馏，student 通常在 teacher supervision 下训练，损失会偏向：

- 匹配 teacher 预测
- 匹配某种 velocity / noise / x0 target
- 在固定少数 sampling nodes 上表现稳定

这类目标往往比原始生成训练更"受约束"，自由度更小。自由度变小后，模型常见会出现：

- Hessian 更没那么病态
- 权重冗余更高
- 对低精度噪声更鲁棒

**结论**：蒸馏把模型带到了一个**更平坦、容错更高**的 basin。

---

### 5. Base 模型更依赖"细小残差累积"

Base 模型多步采样时，每一步误差都不需要特别小，但**误差会累积**。量化噪声如果每一步都加一点，最终可能滚大。

蒸馏模型虽然步数少，但**总误差注入次数也少**。于是即便单步更复杂，整体反而更稳。

在扩散模型里特别常见：

| 模型类型 | 步数 | 量化误差累计 |
|---------|------|-------------|
| Base | 20~50 步 | 每步很小的 bias，累计多次 |
| Distilled | 1~4 步 | 只累计少数几次 |

所以最终图像质量上，蒸馏模型可能明显更抗量化。

---

### 6. "Sharp"可能只体现在输出语义，不体现在数值统计

蒸馏模型"出图更果断、更一步到位"，**视觉上看像更 sharp**，但数值上不一定表现为：

- 更大的 kurtosis（峰度）
- 更高的 outlier ratio
- 更大的 max-abs

建议把"sharp"拆成几个可测指标：

| 指标 | 含义 |
|-----|------|
| 权重的 max / p99 / p99.9 | 极端值占比 |
| Activation 的 per-layer kurtosis | 分布尖锐程度 |
| Outlier channel ratio | 异常通道比例 |
| Timestep 间 activation distribution drift | 时序稳定性 |
| Hessian trace 或近似曲率 | 局部平滑度 |
| SQNR / cosine similarity under fake quant | 量化敏感度 |

**常见发现**：蒸馏模型视觉行为更激进，但内部统计更规整。

---

### 7. 蒸馏模型常在"更窄的操作域"优化

如果你的蒸馏目标只覆盖：
- 有限步数
- 有限 CFG 区间
- 有限分辨率

那 student 其实是在一个**更窄的操作域**里被优化的。Base 模型则要对更广的噪声区间、更多步数都 work。

更窄的操作域意味着：

- 激活支持集更小
- 极端 case 更少
- Calibration 数据更容易覆盖实际部署分布

---

## 验证实验：如何证明这些机制？

为了把这个现象讲清楚，建议做以下几组 ablation：

### 实验 A：分离"误差累计"因素

- 对 base 和 distilled 都做 fake quant
- 记录每一步 latent 与 fp 模型的 distance
- 看 error 是线性累积、指数放大，还是前几步最关键

**预期**：base 的误差随 step 明显滚大。

---

### 实验 B：对比 Activation 统计

每层统计：

- Max abs
- P99.9
- Kurtosis
- Channel-wise variance CV
- Outlier channel ratio

**预期**：distilled 的 tail 更短。

---

### 实验 C：Timestep-Conditioned Sensitivity

对每个 timestep 单独量化某一层，测最终图像退化。

**预期**：
- Base 在某些早期/中期 step 极敏感
- Distilled 的敏感点更少、更集中

---

### 实验 D：比较权重几何

- Layerwise weight norm
- Spectral norm
- Hessian trace 近似
- Sharpness-aware perturbation test

**预期**：直方图看不出差异，但局部曲率差很多。

---

## 总结：更准确的表述

这个观察可以总结为：

> **蒸馏减少的是采样轨迹长度，不一定增加网络内部表示的尖锐性；相反，由于 teacher supervision、操作域收缩和误差累计减少，蒸馏模型常常表现出更高的量化鲁棒性。**

### 最可能的解释排序

1. **少步数减少误差累计** —— 最直接、最常见
2. **蒸馏让 timestep 分布更集中、更稳定**
3. **Teacher-student 训练带来隐式平滑**
4. **Base 模型为了覆盖长轨迹，内部保留了更多难量化的极端通道**

### 关键洞察

不要把两种 "sharpness" 混在一起：

- **生成轨迹上的高效率**（蒸馏模型更强）
- **数值表示上的高尖锐度/难量化性**（蒸馏模型不一定更强）

前者变强，并不推出后者也变强。

---

## 参考与延伸

- 扩散模型蒸馏技术：Progressive Distillation, Consistency Models, Guided Distillation
- 量化敏感性分析：SQNR, Perturbation Analysis, Hessian-based metrics
- 部署优化：Static vs Dynamic Quantization, Calibration strategies

---

*本文基于与 AI 助手的对话整理而成，记录了量化扩散模型蒸馏版本时的观察与思考。*
