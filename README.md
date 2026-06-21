# README
LLM 生成初始检索计划
↓
多源检索
↓
Reranker 给每篇论文打分
↓
聚合质量信号
↓
判断问题来源
   ├─ 召回不足：改 query
   └─ 排序/质量不足：调 source / venue 权重
↓
二次检索
↓
最终排序和报告

主要初步通过反馈机制解决搜索源和搜索词的质量问题

1. search_papers() 拆成 search_openalex() + search_arxiv()
2. 每篇 paper 增加 source / matched_query / venue_score
3. 加 plan_retrieval_sources()
4. 改 rank_papers() 为 rerank_papers()
5. 加 analyze_feedback()
6. generate_report() 显示 source_weights、source_stats、feedback