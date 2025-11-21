---
title: "CoTyle 论文阅读记录"
date: 2025-11-21 14:18:00 +0800
categories: ["reading"]
tags: [diffusion-models, reading-notes, generative-models]
---

同事让我有空看看这个，我就看看了

### 项目地址
- [Github CoTyle](https://github.com/Kwai-Kolors/CoTyle)
- [GithubIO CoTyle](https://kwai-kolors.github.io/CoTyle/)

### 概况
这个模型做到了使用 code（编码而非代码）控制图像风格，也就是说在 code 相同的情况下，改变 prompt 和种子可以生成一组风格相似的图片。

<img src="assets/img/CoTyle-image-1.png" alt="CoTyle卖家秀" style="width: 400px;" />

粗略地看了一下 github 首页，不过它对不同风格之间似乎并没有一种可以查表的方式让人自己选择需要什么风格，code的数值在也非常大，看起来也是和seed 一样需要抽卡的。所以我怀疑它的侧重点并不在于引导单张图片风格化生成，而是维持一组图片保持同样的风格（同样的 code）

### 好奇的问题
1. 这看起来似乎就是一个类似于 clip 的东西
2. 同事好奇的问题：Figure 4 中用红框圈出了“suboptimal style consistency.”，这个一致性是怎么判断的
3. 有没有办法优雅地上线

### 论文的场合