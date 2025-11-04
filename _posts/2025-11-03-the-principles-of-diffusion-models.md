---
title: "What actually is diffusion model?"
date: 2025-11-03 17:46:00 +0800
categories: ["The Principles of Diffusion Models: From Origins to Advances"]
tags: [diffusion-models, reading-notes, generative-models]
---

### 我不喜欢从原理讲起的书，但

我本来想直奔讲解推理加速的章节的，但看了一眼全是公式，我还是老实地从头看起吧。

虽然我一向不喜欢从xxx原理开始介绍的书籍

关于diffusion model，同事曾推荐我以下的资料：

- [Diffusion Models &#124; Paper Explanation &#124; Math Explained](https://www.youtube.com/watch?v=HoKDTa5jHvg&t=444s)
- [Flow Matching &#124; Explanation + PyTorch Implementation](https://www.youtube.com/watch?v=7cMzfkWFWhI)

如果没有兴趣看完两个长视频，可以直接看第二个。

我曾经看过一些科普文章和科普视频，基本都会说扩散模型（这里应当特指我熟悉的生图模型）的forward就是去噪。虽然我没办法从专业的角度上反驳，但我也能直觉上感觉这种说法单纯止步于“科普”程度。

> Diffusion modeling begins by specifying a forward corruption process that gradually turns data into noise. 
> This forward process links the data distribution to a simple noise distribution by defining a continuous family of intermediate distributions. 
> The core objective of a diffusion model is to construct another process that runs in the opposite direction, transforming noise into data while recovering the same intermediate distributions defined by the forward corruption process.

这里是论文中严谨地介绍，将去噪过程讲解为数据的分布的转换。

之所以专门提到这一点，是因为我最开始以为生图过程就是把一个噪声图逐渐去噪成一幅可读的图片，然而这种想法只是被“去噪”这一说法误导的结果，这让我忽略掉了“vae”。


### 参考文献

[1] The Principles of Diffusion Models: From Origins to Advances. arXiv preprint arXiv:2510.21890, 2025. https://arxiv.org/pdf/2510.21890