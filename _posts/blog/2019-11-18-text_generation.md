---
layout: post
title:  文本生成资料汇总
category: 技术
tags:  
    - NLP
keywords: 
description: 
---

# 文本生成资料汇总

## 项目

| 项目 | 语言 | 预训练模型 | 简介 | 相关资料 |
| ---- | ---- | ---- | ---- | ---- |
| [GPT2-Chinese](https://github.com/Morizeyao/GPT2-Chinese) | 中文 | √ | 中文的GPT2训练代码，使用BERT的Tokenizer或Sentencepiece的BPE model（感谢kangzhonghua的贡献，实现BPE模式需要略微修改train.py的代码）。可以写诗，新闻，小说，或是训练通用语言模型。支持字为单位或是分词模式或是BPE模式（需要略微修改train.py的代码）。支持大语料训练。 | |
| [gpt2-ml](https://github.com/imcaspar/gpt2-ml) | 中文 | √ | GPT2 模型， 多语言支持 | |
| [roberta_zh](https://github.com/brightmart/roberta_zh) | 中文 | √ | RoBERTa是BERT的改进版，通过改进训练任务和数据生成方式、训练更久、使用更大批次、使用更多数据等获得了State of The Art的效果；可以用Bert直接加载。| |
| [Chinese-PreTrained-XLNet](https://github.com/ymcui/Chinese-PreTrained-XLNet) | 中文 | √ |  本项目提供了面向中文的XLNet预训练模型，旨在丰富中文自然语言处理资源，提供多元化的中文预训练模型选择。 我们欢迎各位专家学者下载使用，并共同促进和发展中文资源建设。| |
| [fastText](https://github.com/facebookresearch/fastText) | All | √ | fastText is a library for efficient learning of word representations and sentence classification. | |
| [transformers](https://github.com/huggingface/transformers) | All | √ | Transformers: State-of-the-art Natural Language Processing for TensorFlow 2.0 and PyTorch. https://huggingface.co/transformers | |
| [bert-as-service](https://github.com/hanxiao/bert-as-service) | All | √ | Mapping a variable-length sentence to a fixed-length vector using BERT model https://bert-as-service.readthedocs.io | [两行代码玩转Google BERT句向量词向量](https://zhuanlan.zhihu.com/p/50582974), |
| [gpt-2-keyword-generation](https://github.com/minimaxir/gpt-2-keyword-generation) | English | × | Method to encode text for GPT-2 to generate text based on provided keywords | |
| [SC-LSTM](https://github.com/hit-computer/SC-LSTM) | All | × | Implement SC-LSTM model for text generation in control of words, in Python/TensorFlow. 语义控制的文本生成模型 | [github:char-rnn-tf](https://github.com/hit-computer/char-rnn-tf), |
| [ctrl](https://github.com/salesforce/ctrl) | All | √ | Conditional Transformer Language Model for Controllable Generation | [paper: CTRL: A Conditional Transformer Language Model for Controllable Generation](https://arxiv.org/abs/1909.05858), [这年头，AI都懂得编故事了](https://wwww.huxiu.com/article/317781.html) |


## 资料
- [The Illustrated GPT-2 (Visualizing Transformer Language Models)](https://jalammar.github.io/illustrated-gpt2/); [中文翻译版本]()
- [【NLP】BERT中文实战踩坑](https://zhuanlan.zhihu.com/p/51762599)
- [干货 | BERT fine-tune 终极实践教程](https://www.jianshu.com/p/aa2eff7ec5c1)
- [Can BERT be used for sentence generating tasks?](https://ai.stackexchange.com/questions/9141/can-bert-be-used-for-sentence-generating-tasks?newreg=cb71453e03834173ae5c80e0c5504d7c)
- [Can you use BERT to generate text?](http://mayhewsw.github.io/2019/01/16/can-bert-generate-text/)
- [如何把BERT用到文本生成中](https://www.nowcoder.com/discuss/196954)
- [Neural text generation: How to generate text using conditional language models](https://medium.com/phrasee/neural-text-generation-generating-text-using-conditional-language-models-a37b69c7cd4b)
- [史上最强通用NLP模型GPT-2：OpenAI刚又发布7.74亿参数版本](http://blog.itpub.net/29829936/viewspace-2654536/)


## 观点

### Bert能用于文本生成吗?

[观点1 by soloice](https://ai.stackexchange.com/a/10628/31405): 不能

```
For newbies, NO.

Sentence generation requires sampling from a language model, which gives the probability distribution of the next word given previous contexts. But BERT can't do this due to its bidirectional nature.

For advanced researchers, YES.

You can start with a sentence of all [MASK] tokens, and generate words one by one in arbitrary order (instead of the common left-to-right chain decomposition). Though the text generation quality is hard to control.

Here's the technical report BERT has a Mouth, and It Must Speak: BERT as a Markov Random Field Language Model, its errata and the source code.

In summary:

If you would like to do some research in the area of decoding with BERT, there is a huge space to explore
If you would like to generate high quality texts, personally I recommend you to check GPT-2.
```

[观点2 by stuart](https://ai.stackexchange.com/a/11429/31405): 不能; [引用](http://mayhewsw.github.io/2019/01/16/can-bert-generate-text/)

```
this experiment by Stephen Mayhew suggests that BERT is lousy at sequential text generation:

http://mayhewsw.github.io/2019/01/16/can-bert-generate-text/

although he had already eaten a large meal, he was still very hungry
As before, I masked “hungry” to see what BERT would predict. If it could predict it correctly without any right context, we might be in good shape for generation.

This failed. BERT predicted “much” as the last word. Maybe this is because BERT thinks the absence of a period means the sentence should continue. Maybe it’s just so used to complete sentences it gets confused. I’m not sure.

One might argue that we should continue predicting after “much”. Maybe it’s going to produce something meaningful. To that I would say: first, this was meant to be a dead giveaway, and any human would predict “hungry”. Second, I tried it, and it keeps predicting dumb stuff. After “much”, the next token is “,”.

So, at least using these trivial methods, BERT can’t generate text.
```

### 语言模型未来的四大趋势

[来源: 史上最强通用NLP模型GPT-2：OpenAI刚又发布7.74亿参数版本](http://blog.itpub.net/29829936/viewspace-2654536/)

```
趋势1：语言模型转移到设备

考虑到计算能力成本的历史趋势，我们可以期待语言模型在一系列设备上得到更广泛的部署。例如，Hugging Face将1.24亿参数GPT-2移植到Swift CoreML中，以便在iOS设备上进行推理。

趋势2：更可控的文本生成

语言模型的潜在用途将随着提高可靠性和/或可控性的发展而增长，例如新的抽样方法、新的数据集、新的目标函数和新的人机界面。

可控性的例子包括：

•在GROVER模型中，进行界面修改以引入输出可控性，使得可以输入文章元数据（例如，标题，作者）以生成高质量输出。

•清华大学的ERNIE模型与知识库相结合，促进了比通用语言模型更可控的生成。

•Stanford和FAIR展示了通过更直接地针对高级会话属性（例如重复程度）进行优化来改善聊天机器人性能的潜力。

趋势3：更多风险分析

目前还不清楚如何比较具有不同性能配置文件的两个大型语言模型的误用性（misusability），特别是在考虑微调（fine-tuning）时。一些关键的考虑因素包括在模型的帮助下生成一定质量的文本所需的时间和专业知识，以及不使用模型的情况，尽管随着技术工具的发展，这将随着时间的推移而变化。

趋势4：工具可用性提升

今天，模型的训练和部署需要了解ML技术，使用工具的技能以及访问测试平台以进行评估。稳步改进的与语言模型交互的工具，如Talk to Transformer和Write with Transformer，将扩大能够以各种不同方式使用语言模型的参与者的数量。这些对工具可用性的改进将对模型性能和采样方法的改进起到补充作用，并将使语言模型的创造性应用比我们目前看到的更广泛。
```