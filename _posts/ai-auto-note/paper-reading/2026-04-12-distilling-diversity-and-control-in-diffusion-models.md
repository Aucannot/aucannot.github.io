---
title: "蒸馏模型生成的图都一样？"
date: 2026-04-12 19:00:00 +0800
categories: ["ai-auto-note", "paper-reading"]
tags: [diffusion-models, distillation, diversity, generative-models]
math: true
---

最近被反馈了一个问题：同一个 prompt，随机 seed，出来的图长得都差不多。Base model 就没有这个问题。

我起初以为是量化产生的问题，排查后发现是因为用了蒸馏 lora。于是顺着这个线索查到了这篇论文。

## TL; DR

蒸馏模型把 timestep 压缩了，同一个 prompt 换 seed 出来的图都差不多。但奇怪的是 FID 反而比 base 好——至少说明整体分布指标没有一起坏掉，问题更集中在同一个 prompt 下的 sample diversity。论文问的就是：为什么？

结论：
- 多样性问题不只是在"学没学到"，更在"怎么生成"。论文结果说明，蒸馏模型里仍保留了不少和控制、多样性相关的表示能力
- 蒸馏模型在第一个 timestep 就把图像结构拍板了，而 base model 是慢慢想的，所以多样性主要卡在第一步
- 只要把第一步交给 base model、剩下的交给蒸馏模型，多样性就恢复了，而且总步数不变，推理速度也几乎不变（0.64s vs 9.22s）

## "没学到"还是"没用到"？

论文上来先问了一个很自然的问题：蒸馏过程是不是把 base model 的概念表示给破坏了？如果模型内部就没有多样性的"素材"，那自然出不了多样的图。

这个假设很合理。蒸馏的代价是压缩，压缩的代价是丢信息——"丢掉了多样性相关的表示"听起来再正常不过了。

然后论文做了一组迁移实验来验证：把在 base model 上训练的控制机制直接搬到蒸馏模型上，看能不能用。

| 控制方法 | 类型 | Base→DMD | Base→LCM | Base→Turbo | Base→Lightning |
| --- | --- | --- | --- | --- | --- |
| Concept Slider (Age) | 属性控制 | ✓ | ✓ | ✓ | ✓ |
| Concept Slider (Smile) | 属性控制 | ✓ | ✓ | ✓ | ✓ |
| Custom Diffusion (Lego) | 个性化定制 | ✓ | ✓ | ✓ | ✓ |
| SliderSpace (Direction 1) | 多样性方向 | ✓ | ✓ | ✓ | ✓ |

注：`Base` 指原始的多步扩散 teacher；`Base→DMD / LCM / Turbo / Lightning` 表示将 `Base` 上学到的控制方法直接迁移到对应蒸馏 student 上。这里的 `DMD` 指 `Distribution Matching Distillation`，`LCM` 指 `Latent Consistency Models`，`Turbo` 通常指基于 `Adversarial Diffusion Distillation` 的 `SDXL Turbo` 类模型，`Lightning` 指基于 `Progressive Adversarial Diffusion Distillation` 的 `SDXL Lightning` 类模型。它们都是把多步扩散压缩成少步生成的不同蒸馏路线。

这张表真正想问的不是"这些蒸馏方法谁更强"，而是：**不管 student 是用哪条蒸馏路线训出来的，base model 学到的控制能力能不能直接继承过去？**

全部可以直接迁移，不需要任何重新训练。

特别值得关注的是 SliderSpace——这个东西本身就是从 base model 里分解出多样性的方向，它居然也能在蒸馏模型上用。也就是说，蒸馏模型并不是没有"多样性的方向"，它有，只是默认生成的时候没有往这些方向走。

这把问题的定位从"表示层面"挪到了"生成动力学层面"：**蒸馏模型里还保留着不少和多样性相关的"开关"，只是默认采样轨迹没有把这些开关真正调动起来。**

## 既然没丢，那是什么时候丢的？

既然不是"没学到"，那就得看"怎么生成的"——多样性是不是在生成过程中被磨掉的。

论文用了一个很直觉的可视化方法：在去噪过程中，每一步都把模型对最终图像的预测 $\hat{\mathbf{x}}_{0|t}$ 解码出来看。具体来说，扩散模型在第 $t$ 步预测噪声 $\epsilon_\theta(\mathbf{x}_t, t)$，由此可以估计模型认为最终图像长什么样：

$$
\hat{\mathbf{x}}_{0|t} = \frac{\mathbf{x}_t - \sqrt{1 - \bar\alpha_t}\,\epsilon_\theta(\mathbf{x}_t, t)}{\sqrt{\bar\alpha_t}}
$$

为什么要看这个？因为 $\hat{\mathbf{x}}_{0|t}$ 本质上就是模型在每一步对最终结果的"猜测"。如果某一步之后 $\hat{\mathbf{x}}_{0|t}$ 就不怎么变了，那说明模型在那一步就已经"想好了"；如果 $\hat{\mathbf{x}}_{0|t}$ 一直在变，说明模型还在犹豫。

把每一步的 $\hat{\mathbf{x}}_{0|t}$ 串起来看，结论非常明显：

- **Base model**：前面相当一段 step 都在慢慢塑造图像结构，$\hat{\mathbf{x}}_{0|t}$ 从模糊逐步变清晰，过程中结构一直在变
- **蒸馏模型**：第一步 $\hat{\mathbf{x}}_{0|t}$ 就已经和最终输出非常接近了，后面几步基本只做细节微调

换成人话：**蒸馏模型第一步就拍板了，后面只是润色。** 而 base model 是边走边想的。

第一步就定死了，那随机噪声带来的多样性就全被压在第一步里了——但蒸馏模型的压缩过程又正好把这一步的多样性给磨掉了。

## 把第一步换回来试试

如果第一步真的是瓶颈，那把第一步换回 base model 是不是就行了？

论文就这么做了：

1. 第一步用 base model 跑
2. 后面几步用蒸馏模型跑

结果：

| | Sample Diversity ↑ | FID ↓ | 时间 (s) ↓ |
| --- | --- | --- | --- |
| Base | 0.337 | 12.74 | 9.22 |
| Distilled | 0.264 | 15.52 | 0.64 |
| **Hybrid (替换第一步)** | **0.350** | **10.79** | **0.64** |

只换了第一步，多样性不仅恢复了，还比 base model 稍高一点。FID 也更好。推理速度几乎不变，因为总步数没变，只是把原本蒸馏模型的第一步替换成了 base model。

反向验证也做了：如果保持蒸馏模型的第一步，把后面的 step 换成 base model——多样性完全恢复不了。这进一步证死了"多样性就是被第一步卡死的"这个判断。

## 为什么偏偏是第一步？

论文还给了一个理论视角来解释这个现象。直觉上理解的话：蒸馏训练本质上是用 MSE 去拟合 teacher 的输出，而 MSE 的最小化目标是条件均值 $\mathbb{E}[Y \mid X]$——这会让 student 更容易学到 teacher 输出的"平均情况"，从而压缩掉一部分条件方差。

但为什么偏偏是第一步受影响最大？看 $\hat{\mathbf{x}}_{0|t}$ 对噪声预测误差的放大因子：

$$
A_t = \sqrt{\frac{1 - \bar\alpha_t}{\bar\alpha_t}}
$$

在早期 timestep，$\bar\alpha_t \approx 0$，所以 $A_t$ 非常大。这意味着：**同样的多样性损失，越早的 step 被放大得越狠。**

第一步多样性丢了，就是丢了；后面 step 的多样性本来就被噪声压着，丢也丢不了多少。

## 最后

这篇论文的思路很清晰：先排除"表示层面"的问题，再用可视化定位"什么时候出了问题"，最后用 hybrid 推理验证。

和我[之前写的那篇蒸馏量化的文章]({% post_url ai-auto-note/paper-reading/2026-03-23-distilled-diffusion-quantization %})可以对照着看。那篇讨论了为什么蒸馏模型反而更好量化——核心也是"蒸馏改变了生成动力学"。这篇论文给出了一个更具体的说法：第一步就拍板。

有个部署上的现实问题：这个 hybrid 方案需要同时加载 base 和 distilled 两个模型，显存直接翻倍。对实际部署来说不太友好，更像是一个验证机制，而不是没有代价的免费优化。

另一个角度：这个发现其实暗示了训练蒸馏模型的一个方向——如果在蒸馏训练的时候有意保住第一步的多样性（比如不对第一步做 MSE 压缩，或者对第一步加多样性 loss），是不是就不需要这种 hybrid 方案了？

## 参考资料

- 论文: [Distilling Diversity and Control in Diffusion Models](https://arxiv.org/abs/2503.10637)
- 项目主页: [distillation.baulab.info](https://distillation.baulab.info/)
- 代码: [github.com/rohitgandikota/distillation](https://github.com/rohitgandikota/distillation)
- DMD: [One-step Diffusion with Distribution Matching Distillation](https://arxiv.org/abs/2311.18828)
- LCM: [Latent Consistency Models: Synthesizing High-Resolution Images with Few-Step Inference](https://arxiv.org/abs/2310.04378)
- Turbo / ADD: [Adversarial Diffusion Distillation](https://stability.ai/research/adversarial-diffusion-distillation)
- Lightning: [SDXL-Lightning: Progressive Adversarial Diffusion Distillation](https://arxiv.org/abs/2402.13929)
