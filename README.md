# README

此文件为最小技术栈

```
用户输入
↓
LLM生成术语和检索词
↓
OpenAlex搜索论文
↓
按年份+引用量+相关性排序
↓
输出Top论文
```

先让系统能找到论文。

今天的完成标准：

```
输入一个模糊问题
能返回20篇左右相关论文
每篇包含 title / year / citations / abstract / url
```