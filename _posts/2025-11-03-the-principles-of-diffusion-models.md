---
title: "diffusion model 大概在做什么事情？"
date: 2025-11-03 17:46:00 +0800
categories: ["The Principles of Diffusion Models: From Origins to Advances"]
tags: [diffusion-models, reading-notes, generative-models]
---

### 我不喜欢从原理讲起的书，但

我本来想直奔讲解推理加速的章节的，但看了一眼全是公式，我还是老实地从头看起吧。

虽然我一向不喜欢从xxx原理开始介绍的书籍

关于diffusion model，同事曾推荐我以下的资料：

- [Diffusion Models &#124; Paper Explanation &#124; Math Explained](http s://www.youtube.com/watch?v=HoKDTa5jHvg&t=444s)
- [Flow Matching &#124; Explanation + PyTorch Implementation](https://www.youtube.com/watch?v=7cMzfkWFWhI)

同事说可以直接看第二个，但都是公式推导，我连那些基本的棍子符号都忘记是什么意思了，这个视频我打开过三次，看到公示就开始涣散了，我决定放过我自己，等我足够厉害了再回来看这个广受好评的视频。

为了给我自己梳理一下diffusion model，我决定应该先大概建立一个感性的概念。

**3Blue1Brown** 一向是这方面的专家，**强烈**建议观看：[But how do AI images and videos actually work? &#124; Guest video by Welch Labs](https://youtu.be/iv-5mZ_9CPY?si=n8vbkBPiJDRM_YHl)

如果上面这个视频对你来说还是有点困难，可以先从最小幅度开始建立这种感性的概念：[【闪客】为啥AI画的“表”总是10:10？]( https://www.bilibili.com/video/BV11RWizREYM/?share_source=copy_web&vd_source=4bfa9204702e7e835ea454eb5c71a71a)


### diffusion model 大概在做什么事情？

我的情况比较特殊，我基本是对着diffusion model 的推理代码开始入门的，没有看过原理，所以决心开始写博客补课。

在diffusion model的推理过程中，除了模型权重以外，会需要输入一些参数：prompt、num_inference_steps、guidance_scale、noise_seed等等。可以先玩玩文生图的工作流：[在线ComfyUI 体验Qwen Image文生图](https://bizyair.cn/community/models/publicity/37000)

在`3Blue1Brown`的视频中，对diffusion model的推理过程有一个很好的概括：**时变的矢量场**

### 参考文献

[1] The Principles of Diffusion Models: From Origins to Advances. arXiv preprint arXiv:2510.21890, 2025. https://arxiv.org/pdf/2510.21890