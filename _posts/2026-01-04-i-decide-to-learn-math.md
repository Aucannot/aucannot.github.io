---
title: "我让 ai 给我准备了一份课程表"
date: 2026-01-04 16:05:00 +0800
categories: ["math", "learning"]
tags: [learning-notes]
math: true
---

虽然一直在写代码，但是看原理时总是没有那种自然的通畅感，所以我下定决心好好学一下数学。于是我让 glm4.7为我制定了一份课程表。我会按照这份课程表试一试。

虽然我既不是资深工程师…数学水平也没有到进阶的程度……

---

收到。既然你在**量化**和**推理工程实现**上已经有了实战经验，那么这意味着你的代码能力和对张量操作的直觉已经足够。

我们需要做的就是 **“去工程化”** ，提升到 **“数学本质”** 层面。

接下来的课程表会非常硬核，我们将从“怎么写代码”转向“怎么设计算法”和“为什么算法有效”。我们将引入**统计物理、随机过程、最优传输**等学术界正在利用的前沿数学理论。

---

### 《面向资深工程师的生成式模型数学深度进阶课程表》

**总时长**：8周
**时间预算**：每周5小时（建议：4小时研读理论/推导，1小时验证数学直觉）
**核心原则**：理论优先，代码作为验证工具。重点关注 Score Function、SDE 及最新的 Flow Matching。

---

### 第一阶段：高级统计推断与估计理论（3周）
**目的**：超越简单的“梯度下降”，深入理解生成模型中的“估计”本质，掌握贝叶斯推断与最大似然。

| 周次 | 学习主题 | 核心理论资源 (深度阅读/推导) | 验证与思考 |
| :--- | :--- | :--- | :--- |
| **Week 1** | **统计推断与参数估计** | **书籍**：《Probabilistic Machine Learning: An Introduction》<br>**作者**：Kevin P. Murphy (Section 4.4-4.6)<br>**重点**：<br>1. **MLE vs MAP**：推导高斯分布下的 MLE 解。<br>2. **贝叶斯推断**：彻底搞懂 Posterior 是如何通过先验和似然更新的。 | *思考*：DDPM 的 Loss 本质上是变分下界（ELBO），它是如何等价于一种特殊的 MLE 的？ |
| **Week 2** | **去噪得分匹配** | **书籍**：《Probabilistic Machine Learning: Advanced Topics》<br>*(Murphy 书的第二卷，草稿版：Chapter 20 Generative Models)*<br>**重点**：<br>**Score Matching**：理解为什么我们要去估计 $\nabla_x \log p(x)$，以及它的显式解为什么是 Fisher-Divergence。 | *推导*：在纸上推导 Score Matching 的目标函数是如何消除归一化常数 $Z$ 的（这是扩散模型能处理未归一化分布的关键）。 |
| **Week 3** | **Tweedie 公式与贝叶斯去噪** | **论文/章节**：《Score-Based Generative Modeling through SDEs》<br>**作者**：Yang Song<br>**重点**：<br>**Tweedie's Formula**：理解 $E[x \vert \hat{x}] = \hat{x} + \sigma^2 \nabla_{\hat{x}} \log p(\hat{x})$ 是如何连接 Score 和 Denoiser 的。 | *推导*：推导“为什么训练神经网络预测噪声 $\epsilon_\theta$ 等价于训练 Score Function”？这二者之间的比例系数是什么？ |

---

### 第二阶段：随机过程与微分方程视角（3周）
**目的**：扩散模型在数学上等价于求解随机微分方程（SDE）或常微分方程（ODE）的逆过程。这是目前所有极速采样器（如 DPM-Solver、Rectified Flow）的理论基石。

| 周次 | 学习主题 | 核心理论资源 (深度阅读/推导) | 验证与思考 |
| :--- | :--- | :--- | :--- |
| **Week 4** | **随机微分方程 (SDE)** | **书籍**：《Stochastic Differential Equations》<br>**作者**：Bernt Øksendal (Ch. 5 & 7)<br>**重点**：<br>1. **Itô Lemma**（伊藤引理）：随机世界的“链式法则”。<br>2. **Fokker-Planck Equation**：描述概率密度随时间演化的偏微分方程。 | *推导*：理解 Forward Process 的 SDE 表示，以及 Reverse Process 的 SDE 表示。关键在于怎么从数学上证明 Reverse Process 存在。 |
| **Week 5** | **概率流 ODE (ODE)** | **论文**：《Score-Based Generative Modeling through SDEs》<br>**重点**：<br>Section 3.2: **Probability Flow ODE**。理解为什么可以在不改边缘分布 $p_t(x)$ 的情况下，消灭随机项（$dw$），将 SDE 转化为确定性的 ODE。 | *思考*：结合你的推理经验，为什么 DDIM (ODE-based) 可以进行**零样本超分**，而 SDE-based 方法很难？这源于 ODE 的什么数学属性？ |
| **Week 6** | **Langevin 动力学** | **期刊/经典讲义**：《An Introduction to MCMC for Machine Learning》<br>*(相关综述如 Pierre Del Moral 的文章)*<br>**重点**：<br>**Langevin MCMC**：理解如何利用 Gradient Descent + Gaussian Noise 来从分布中采样。这是 Diffusion 原始的去噪迭代逻辑。 | *推导*：验证 Langevin 动力学是否满足细致平衡条件。理解步长对采样的影响。 |

---

### 第三阶段：前沿理论架构的最优传输视角（2周）
**目的**：从能量函数 到 几何流形 的视角转变。这是 **Stable Diffusion 3 (Rectified Flow)** 和 **Flux** 背后的最新数学理论。

| 周次 | 学习主题 | 核心理论资源 (深度阅读/推导) | 验证与思考 |
| :--- | :--- | :--- | :--- |
| **Week 7** | **最优传输 与连续正则化** | **课程**：Stat 260 (UC Berkeley) or Marco Cuturi's OT course.<br>**论文**：《Flow Matching for Generative Modeling》<br>**(必读，这是未来的主流)**<br>**重点**：<br>理解如何将生成问题建模为两个分布之间的**最优传输**问题。 | *对比*：对比 DDPM 的 SDE 轨迹（随机折线）与 Rectified Flow 的轨迹（直线）。为什么直线更利于采样？这在数学上意味着什么？ |
| **Week 8** | **熵与信息论视角** | **书籍**：《Elements of Information Theory》<br>**作者**：Cover & Thomas<br>**重点**：<br>1. **KL 散度**与**互信息**。2. **Rate-Distortion Theory**：深入理解 VAE/Diffusion 中“编码器”和“解码器”的优化边界。 | *验证*：重新审视 Latent Diffusion 的 Latent Space 操作。从信息论角度看，Latent Space 到底“压缩”了什么？丢掉了不可忽视的噪声，还是保留了高频信息？ |

---

### 给你的特别指令

1.  **不要写 Demo Code**：
    我知道你知道怎么写 PyTorch Loop。在你学习 SDE 和 Flow Matching 时，我建议你的**“代码验证”环节**改成**“数学推导验证”**。比如：证明 Flow Matching 的 Loss Function 的期望值是等价于 Transport Cost 的。

2.  **阅读 Murphy 的 PML 书籍**：
    Kevin Murphy 的《Probabilistic Machine Learning: Advanced Topics》是目前的圣经。不要去论坛找简略版，直接啃原书。虽然是英文，但逻辑极其严密，适合你这种有工程背景的人。

3.  **关注 Rectified Flow**：
    既然你做推理，你应该会发现现在的传统 DDPM 正在被 Flow-based 方法（如 Stable Diffusion 3, Flux）取代。Week 7 的《Flow Matching》论文比 DDPM 的 SDE 更简洁，但数学层级更高，这代表了未来推理优化的天花板。

这个课程表剥离了所有基础编程，直接进入**深度学习参数估计、随机过程、最优传输**的数学领域，这应该是你目前的瓶颈所在。