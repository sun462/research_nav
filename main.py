# v1.1.0 搜索阶段.搜索源与搜索词.初步框架
import os
import re
import json
import math
import time
import requests
import xml.etree.ElementTree as ET
from urllib.parse import quote
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    timeout=60.0,
)

OPENALEX_URL = "https://api.openalex.org/works"
ARXIV_URL = "http://export.arxiv.org/api/query"


# -----------------------------
# Utils
# -----------------------------

def call_qwen_json(prompt, temperature=0.2):
    resp = client.chat.completions.create(
        model="qwen-plus",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )

    text = resp.choices[0].message.content.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)


def recover_abstract(inv):
    if not inv:
        return ""

    words = []
    for word, positions in inv.items():
        for pos in positions:
            words.append((pos, word))

    return " ".join(word for _, word in sorted(words))


def normalize_title(title):
    title = title.lower().strip()
    title = re.sub(r"[^a-z0-9\u4e00-\u9fff ]+", "", title)
    title = re.sub(r"\s+", " ", title)
    return title


def safe_get(d, key, default=None):
    value = d.get(key)
    return value if value is not None else default


# -----------------------------
# 1. Term Discovery
# -----------------------------

def discover_terms(user_query):
    prompt = f"""
用户想研究：{user_query}

请生成：
1. 相关术语
2. 全局检索词
3. 同义词/近义词

要求：
- terms 适合给新手理解领域
- global_queries 适合用于跨数据库检索
- global_queries 尽量使用英文
- 只返回 JSON，不要 Markdown，不要解释

JSON格式：
{{
  "terms": ["term1", "term2"],
  "global_queries": ["query1", "query2"]
}}
"""

    return call_qwen_json(prompt)


# -----------------------------
# 2. Retrieval Planning
# -----------------------------

def plan_retrieval_sources(user_query, terms, global_queries):
    prompt = f"""
用户研究主题：{user_query}

术语：
{terms}

初始全局检索词：
{global_queries}

请你为这个研究主题生成一个多源学术检索计划。

重要要求：
1. 不要使用固定单一领域判断。
2. 要把主题拆成多个可能子领域。
3. 每个子领域要有自己的专属 search queries。
4. 每个子领域要有可能相关的顶会/顶刊/重要venue。
5. 给出 source_weights。
6. arXiv 可以用于前沿补充，但不要给太高权重。
7. 权重总和尽量接近 1。
8. 只返回 JSON，不要 Markdown，不要解释。

JSON格式：
{{
  "global_queries": ["..."],
  "source_weights": {{
    "openalex": 0.65,
    "arxiv": 0.20,
    "venue_boost": 0.15
  }},
  "subdomains": [
    {{
      "name": "subdomain name",
      "weight": 0.4,
      "description": "why this subdomain matters",
      "queries": ["query1", "query2"],
      "preferred_venues": ["ICRA", "IROS", "RSS"]
    }}
  ]
}}
"""

    plan = call_qwen_json(prompt)

    # 防御式修正
    if "global_queries" not in plan:
        plan["global_queries"] = global_queries

    if "source_weights" not in plan:
        plan["source_weights"] = {
            "openalex": 0.65,
            "arxiv": 0.20,
            "venue_boost": 0.15,
        }

    if "subdomains" not in plan:
        plan["subdomains"] = []

    return plan


# -----------------------------
# 3. Multi-source Search
# -----------------------------

def get_venue_score(paper, preferred_venues):
    venue_text = " ".join([
        str(paper.get("venue", "")),
        str(paper.get("source_display_name", "")),
        str(paper.get("host_venue", "")),
    ]).lower()

    for venue in preferred_venues:
        if venue.lower() in venue_text:
            return 1.0

    return 0.0


def search_openalex_for_query(query, subdomain_name, preferred_venues, per_query=25):
    papers = []

    params = {
        "search": query,
        "per-page": per_query,
        "sort": "relevance_score:desc",
        "filter": "has_abstract:true,type:article",
    }

    try:
        response = requests.get(OPENALEX_URL, params=params, timeout=30)
        response.raise_for_status()
    except Exception as e:
        print(f"[OpenAlex Error] query={query}, error={e}")
        return papers

    results = response.json().get("results", [])

    for item in results:
        paper_id = item.get("id")
        if not paper_id:
            continue

        primary_location = item.get("primary_location") or {}
        source = primary_location.get("source") or {}
        venue_name = source.get("display_name", "")

        paper = {
            "id": paper_id,
            "title": item.get("display_name", ""),
            "year": item.get("publication_year"),
            "citations": item.get("cited_by_count", 0),
            "abstract": recover_abstract(item.get("abstract_inverted_index")),
            "url": item.get("doi") or item.get("id"),
            "source": "openalex",
            "matched_query": query,
            "matched_subdomain": subdomain_name,
            "relevance_score": item.get("relevance_score", 0),
            "venue": venue_name,
            "source_display_name": venue_name,
        }

        paper["venue_score"] = get_venue_score(paper, preferred_venues)
        papers.append(paper)

    return papers


def search_arxiv_for_query(query, subdomain_name, preferred_venues, per_query=15):
    papers = []

    encoded_query = quote(f'all:"{query}"')
    url = (
        f"{ARXIV_URL}"
        f"?search_query={encoded_query}"
        f"&start=0"
        f"&max_results={per_query}"
        f"&sortBy=submittedDate"
        f"&sortOrder=descending"
    )

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except Exception as e:
        print(f"[arXiv Error] query={query}, error={e}")
        return papers

    try:
        root = ET.fromstring(response.text)
    except Exception as e:
        print(f"[arXiv Parse Error] query={query}, error={e}")
        return papers

    ns = {"atom": "http://www.w3.org/2005/Atom"}

    for entry in root.findall("atom:entry", ns):
        title = entry.findtext("atom:title", default="", namespaces=ns)
        abstract = entry.findtext("atom:summary", default="", namespaces=ns)
        link = entry.findtext("atom:id", default="", namespaces=ns)
        published = entry.findtext("atom:published", default="", namespaces=ns)

        year = None
        if published:
            try:
                year = int(published[:4])
            except Exception:
                year = None

        paper = {
            "id": link,
            "title": re.sub(r"\s+", " ", title).strip(),
            "year": year,
            "citations": 0,
            "abstract": re.sub(r"\s+", " ", abstract).strip(),
            "url": link,
            "source": "arxiv",
            "matched_query": query,
            "matched_subdomain": subdomain_name,
            "relevance_score": 0,
            "venue": "arXiv",
            "source_display_name": "arXiv",
            "venue_score": 0.0,
        }

        papers.append(paper)

    return papers


def multi_source_search(plan, per_query_openalex=25, per_query_arxiv=15):
    all_papers = []

    # 1. 全局 query：作为兜底召回
    for query in plan.get("global_queries", []):
        preferred_venues = []
        subdomain_name = "global"

        all_papers.extend(
            search_openalex_for_query(
                query,
                subdomain_name,
                preferred_venues,
                per_query=per_query_openalex,
            )
        )

        all_papers.extend(
            search_arxiv_for_query(
                query,
                subdomain_name,
                preferred_venues,
                per_query=per_query_arxiv,
            )
        )

        time.sleep(0.3)

    # 2. 子领域 query：对应子领域专属检索
    for subdomain in plan.get("subdomains", []):
        subdomain_name = subdomain.get("name", "unknown")
        preferred_venues = subdomain.get("preferred_venues", [])

        for query in subdomain.get("queries", []):
            all_papers.extend(
                search_openalex_for_query(
                    query,
                    subdomain_name,
                    preferred_venues,
                    per_query=per_query_openalex,
                )
            )

            all_papers.extend(
                search_arxiv_for_query(
                    query,
                    subdomain_name,
                    preferred_venues,
                    per_query=per_query_arxiv,
                )
            )

            time.sleep(0.3)

    return deduplicate_papers(all_papers)


def deduplicate_papers(papers):
    deduped = {}

    for paper in papers:
        title_key = normalize_title(paper.get("title", ""))
        if not title_key:
            continue

        if title_key not in deduped:
            deduped[title_key] = paper
        else:
            old = deduped[title_key]

            # 如果重复，优先保留 OpenAlex，因为 citation/venue 信息更完整
            if old.get("source") == "arxiv" and paper.get("source") == "openalex":
                deduped[title_key] = paper

            # 或者保留引用更高的版本
            elif paper.get("citations", 0) > old.get("citations", 0):
                deduped[title_key] = paper

    return list(deduped.values())


# -----------------------------
# 4. Reranking and Feedback
# -----------------------------

def normalize_log_citation(citations):
    return min(1.0, math.log1p(citations) / math.log1p(1000))


def normalize_recency(year):
    if not year:
        return 0.0

    if year >= 2024:
        return 1.0
    if year >= 2022:
        return 0.85
    if year >= 2020:
        return 0.7
    if year >= 2015:
        return 0.45
    return 0.25


def normalize_relevance(raw_score):
    if not raw_score:
        return 0.3

    # OpenAlex relevance_score 可能范围不稳定，这里做粗略压缩
    return min(1.0, raw_score / 100.0)


def get_source_score(source):
    if source == "openalex":
        return 0.8
    if source == "arxiv":
        return 0.45
    return 0.5


def rerank_papers(papers, user_query, plan):
    source_weights = plan.get("source_weights", {})

    w_openalex = source_weights.get("openalex", 0.65)
    w_arxiv = source_weights.get("arxiv", 0.20)
    w_venue_boost = source_weights.get("venue_boost", 0.15)

    for paper in papers:
        source = paper.get("source")

        relevance_score = normalize_relevance(paper.get("relevance_score", 0))
        citation_score = normalize_log_citation(paper.get("citations", 0))
        recency_score = normalize_recency(paper.get("year"))
        venue_score = paper.get("venue_score", 0.0)
        source_score = get_source_score(source)

        source_weight = w_openalex if source == "openalex" else w_arxiv

        final_score = (
            0.30 * relevance_score
            + 0.22 * citation_score
            + 0.18 * recency_score
            + 0.20 * venue_score * w_venue_boost
            + 0.10 * source_score * source_weight
        )

        # arXiv 降权：除非很新，否则不要太靠前
        if source == "arxiv" and (paper.get("year") or 0) < 2023:
            final_score *= 0.75

        paper["score_detail"] = {
            "relevance_score": round(relevance_score, 4),
            "citation_score": round(citation_score, 4),
            "recency_score": round(recency_score, 4),
            "venue_score": round(venue_score, 4),
            "source_score": round(source_score, 4),
            "source_weight": round(source_weight, 4),
        }

        paper["final_score"] = round(final_score, 4)

    return sorted(papers, key=lambda p: p.get("final_score", 0), reverse=True)


def analyze_feedback(papers, plan, top_k=30):
    top_papers = papers[:top_k]

    source_stats = {}
    subdomain_stats = {}

    for paper in papers:
        source = paper.get("source", "unknown")
        subdomain = paper.get("matched_subdomain", "unknown")

        source_stats.setdefault(source, {
            "retrieved": 0,
            "top_selected": 0,
            "avg_score": 0.0,
            "scores": [],
        })

        subdomain_stats.setdefault(subdomain, {
            "retrieved": 0,
            "top_selected": 0,
            "avg_score": 0.0,
            "scores": [],
            "venue_hits": 0,
        })

        source_stats[source]["retrieved"] += 1
        source_stats[source]["scores"].append(paper.get("final_score", 0))

        subdomain_stats[subdomain]["retrieved"] += 1
        subdomain_stats[subdomain]["scores"].append(paper.get("final_score", 0))
        if paper.get("venue_score", 0) > 0:
            subdomain_stats[subdomain]["venue_hits"] += 1

    for paper in top_papers:
        source = paper.get("source", "unknown")
        subdomain = paper.get("matched_subdomain", "unknown")

        if source in source_stats:
            source_stats[source]["top_selected"] += 1

        if subdomain in subdomain_stats:
            subdomain_stats[subdomain]["top_selected"] += 1

    for stats in source_stats.values():
        scores = stats.pop("scores")
        stats["avg_score"] = round(sum(scores) / len(scores), 4) if scores else 0.0

    for stats in subdomain_stats.values():
        scores = stats.pop("scores")
        stats["avg_score"] = round(sum(scores) / len(scores), 4) if scores else 0.0
        retrieved = stats["retrieved"] or 1
        stats["venue_hit_rate"] = round(stats["venue_hits"] / retrieved, 4)

    suggestions = []

    for source, stats in source_stats.items():
        if stats["retrieved"] > 0 and stats["top_selected"] == 0:
            suggestions.append(
                f"{source} 返回了 {stats['retrieved']} 篇，但 Top{top_k} 中没有入选，建议降低该 source 权重。"
            )

        if stats["avg_score"] >= 0.55:
            suggestions.append(
                f"{source} 平均质量分较高，建议保留或略微提高权重。"
            )

    for subdomain, stats in subdomain_stats.items():
        if subdomain == "global":
            continue

        if stats["retrieved"] < 10:
            suggestions.append(
                f"{subdomain} 召回数量偏少，可能需要扩展或重写该子领域 query。"
            )

        if stats["retrieved"] >= 10 and stats["avg_score"] < 0.35:
            suggestions.append(
                f"{subdomain} 召回数量足够但平均分偏低，说明 query 可能偏离主题，建议重写。"
            )

        if stats["venue_hit_rate"] < 0.05:
            suggestions.append(
                f"{subdomain} 的 preferred venue 命中率较低，建议检查 venue 列表或调整 source。"
            )

    return {
        "source_stats": source_stats,
        "subdomain_stats": subdomain_stats,
        "suggestions": suggestions,
    }


def refine_queries(user_query, plan, feedback):
    prompt = f"""
用户研究主题：{user_query}

当前检索计划：
{json.dumps(plan, ensure_ascii=False, indent=2)}

检索反馈：
{json.dumps(feedback, ensure_ascii=False, indent=2)}

请根据反馈，只修正表现差的子领域 query。
不要大幅改变原计划。
不要删除高质量子领域。
如果某个子领域召回不足，请扩展 query。
如果某个子领域召回多但质量低，请重写 query。
只返回更新后的 JSON，格式与原 plan 一致。
"""

    return call_qwen_json(prompt, temperature=0.2)


# -----------------------------
# 5. Topic Clustering and Learning Path
# -----------------------------

def cluster_topics(papers):
    paper_text = "\n\n".join([
        f"Title: {p['title']}\n"
        f"Year: {p['year']}\n"
        f"Citations: {p['citations']}\n"
        f"Source: {p['source']}\n"
        f"Subdomain: {p['matched_subdomain']}\n"
        f"Abstract: {p['abstract'][:800]}"
        for p in papers[:25]
    ])

    prompt = f"""
下面是一个研究主题下经过多源检索和rerank后的论文列表。

请根据论文标题和摘要，把它们聚类成 4-6 个研究方向。

要求：
- 每个方向包含 direction_name
- 每个方向包含 description
- 每个方向包含 related_papers，必须使用给定论文标题，不要编造
- 只返回 JSON，不要 Markdown

论文列表：
{paper_text}

JSON格式：
{{
  "clusters": [
    {{
      "direction_name": "",
      "description": "",
      "related_papers": []
    }}
  ]
}}
"""

    return call_qwen_json(prompt)["clusters"]


def generate_learning_path(user_query, terms, clusters):
    prompt = f"""
用户想研究：{user_query}

术语列表：
{terms}

研究方向聚类：
{clusters}

请为新手生成一个学习路径。

要求：
- 分成 4-6 个阶段
- 每个阶段包含目标、要学的概念、推荐阅读方向
- 不要编造具体论文
- 只返回 JSON

JSON格式：
{{
  "learning_path": [
    {{
      "stage": "",
      "goal": "",
      "concepts": [],
      "reading_suggestion": ""
    }}
  ]
}}
"""

    return call_qwen_json(prompt)["learning_path"]


# -----------------------------
# 6. Report
# -----------------------------

def generate_report(user_query, terms, papers, clusters, learning_path, plan, feedback):
    os.makedirs("outputs", exist_ok=True)

    must_read = sorted(
        [p for p in papers if p.get("source") != "arxiv"],
        key=lambda p: (p.get("citations") or 0, p.get("final_score") or 0),
        reverse=True,
    )[:8]

    frontier = sorted(
        papers,
        key=lambda p: (p.get("year") or 0, p.get("final_score") or 0),
        reverse=True,
    )[:8]

    report = "# Research Navigator Report\n\n"
    report += f"研究主题：{user_query}\n\n"

    report += "## 0. 检索策略与反馈\n\n"

    report += "### 0.1 Source Weights\n\n"
    report += "| Source | Weight |\n"
    report += "|---|---:|\n"
    for source, weight in plan.get("source_weights", {}).items():
        report += f"| {source} | {weight} |\n"

    report += "\n### 0.2 Subdomain Routing\n\n"
    report += "| Subdomain | Weight | Preferred Venues |\n"
    report += "|---|---:|---|\n"
    for sub in plan.get("subdomains", []):
        venues = ", ".join(sub.get("preferred_venues", []))
        report += f"| {sub.get('name')} | {sub.get('weight')} | {venues} |\n"

    report += "\n### 0.3 Global Queries\n\n"
    for q in plan.get("global_queries", []):
        report += f"- {q}\n"

    report += "\n### 0.4 Source Feedback\n\n"
    report += "| Source | Retrieved | Top Selected | Avg Score |\n"
    report += "|---|---:|---:|---:|\n"
    for source, stats in feedback.get("source_stats", {}).items():
        report += (
            f"| {source} | {stats['retrieved']} | "
            f"{stats['top_selected']} | {stats['avg_score']} |\n"
        )

    report += "\n### 0.5 Subdomain Feedback\n\n"
    report += "| Subdomain | Retrieved | Top Selected | Avg Score | Venue Hit Rate |\n"
    report += "|---|---:|---:|---:|---:|\n"
    for subdomain, stats in feedback.get("subdomain_stats", {}).items():
        report += (
            f"| {subdomain} | {stats['retrieved']} | "
            f"{stats['top_selected']} | {stats['avg_score']} | "
            f"{stats['venue_hit_rate']} |\n"
        )

    report += "\n### 0.6 Feedback Suggestions\n\n"
    for s in feedback.get("suggestions", []):
        report += f"- {s}\n"

    report += "\n## 1. 术语发现\n\n"
    for term in terms:
        report += f"- {term}\n"

    report += "\n## 2. 领域结构 / 研究方向聚类\n\n"
    for cluster in clusters:
        report += f"### {cluster['direction_name']}\n\n"
        report += f"{cluster['description']}\n\n"
        report += "相关论文：\n"
        for title in cluster.get("related_papers", []):
            report += f"- {title}\n"
        report += "\n"

    report += "\n## 3. 必读论文\n\n"
    for p in must_read:
        report += f"### {p['title']}\n\n"
        report += f"- Year: {p['year']}\n"
        report += f"- Citations: {p['citations']}\n"
        report += f"- Source: {p['source']}\n"
        report += f"- Venue: {p.get('venue', '')}\n"
        report += f"- Subdomain: {p.get('matched_subdomain', '')}\n"
        report += f"- Query: {p.get('matched_query', '')}\n"
        report += f"- Final Score: {p.get('final_score')}\n"
        report += f"- URL: {p['url']}\n"
        report += f"- Abstract: {p['abstract'][:600]}...\n\n"

    report += "\n## 4. 前沿论文\n\n"
    for p in frontier:
        report += f"### {p['title']}\n\n"
        report += f"- Year: {p['year']}\n"
        report += f"- Citations: {p['citations']}\n"
        report += f"- Source: {p['source']}\n"
        report += f"- Venue: {p.get('venue', '')}\n"
        report += f"- Subdomain: {p.get('matched_subdomain', '')}\n"
        report += f"- Query: {p.get('matched_query', '')}\n"
        report += f"- Final Score: {p.get('final_score')}\n"
        report += f"- URL: {p['url']}\n"
        report += f"- Abstract: {p['abstract'][:600]}...\n\n"

    report += "\n## 5. 新手学习路径\n\n"
    for i, stage in enumerate(learning_path, 1):
        report += f"### 阶段 {i}: {stage['stage']}\n\n"
        report += f"- 目标：{stage['goal']}\n"
        report += f"- 概念：{', '.join(stage.get('concepts', []))}\n"
        report += f"- 阅读建议：{stage['reading_suggestion']}\n\n"

    report += "\n## 6. 推荐 Github 检索词\n\n"
    github_keywords = []

    for term in terms:
        github_keywords.append(term)

    for cluster in clusters:
        github_keywords.append(cluster["direction_name"])

    for kw in github_keywords[:15]:
        report += f"- {kw}\n"

    report += "\n## 7. Top Papers with Source Trace\n\n"
    report += "| Rank | Title | Year | Source | Subdomain | Score |\n"
    report += "|---:|---|---:|---|---|---:|\n"

    for i, p in enumerate(papers[:20], 1):
        title = p["title"].replace("|", " ")
        report += (
            f"| {i} | {title} | {p.get('year')} | "
            f"{p.get('source')} | {p.get('matched_subdomain')} | "
            f"{p.get('final_score')} |\n"
        )

    path = "outputs/report.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(report)

    return path


# -----------------------------
# 7. Main
# -----------------------------

def main():
    user_query = input("Research topic: ").strip()

    if not user_query:
        print("请输入研究主题")
        return

    print("\n[1/8] 正在生成术语和全局检索词...")
    discovered = discover_terms(user_query)

    terms = discovered.get("terms", [])
    global_queries = discovered.get("global_queries", [])

    print("\n## Terms")
    for term in terms:
        print("-", term)

    print("\n## Global Queries")
    for query in global_queries:
        print("-", query)

    print("\n[2/8] 正在生成多源检索计划...")
    plan = plan_retrieval_sources(user_query, terms, global_queries)

    print("\n## Retrieval Plan")
    print(json.dumps(plan, ensure_ascii=False, indent=2))

    print("\n[3/8] 第一轮多源检索：OpenAlex + arXiv...")
    papers = multi_source_search(plan)

    print(f"第一轮检索后去重论文数：{len(papers)}")

    print("\n[4/8] Reranking 与质量评分...")
    ranked = rerank_papers(papers, user_query, plan)

    print("\n[5/8] 分析检索反馈...")
    feedback = analyze_feedback(ranked, plan)

    print("\n## Feedback")
    print(json.dumps(feedback, ensure_ascii=False, indent=2))

    # 简单触发二次检索：如果 Top30 平均分过低，或建议中出现“query”
    need_second_round = False
    if ranked:
        avg_top_score = sum(p.get("final_score", 0) for p in ranked[:30]) / min(30, len(ranked))
        if avg_top_score < 0.35:
            need_second_round = True

    if any("query" in s.lower() or "重写" in s for s in feedback.get("suggestions", [])):
        need_second_round = True

    if need_second_round:
        print("\n[6/8] 检索质量不足，正在基于反馈优化 query 并进行第二轮检索...")
        refined_plan = refine_queries(user_query, plan, feedback)

        second_papers = multi_source_search(refined_plan)
        merged = deduplicate_papers(ranked + second_papers)

        ranked = rerank_papers(merged, user_query, refined_plan)
        feedback = analyze_feedback(ranked, refined_plan)
        plan = refined_plan

        print(f"第二轮检索后总论文数：{len(ranked)}")
    else:
        print("\n[6/8] 第一轮检索质量可接受，不进行第二轮检索。")

    top_papers = ranked[:30]

    print("\n[7/8] 正在生成研究方向聚类和学习路径...")
    clusters = cluster_topics(top_papers)
    learning_path = generate_learning_path(user_query, terms, clusters)

    print("\n[8/8] 正在生成 Markdown 报告...")
    report_path = generate_report(
        user_query=user_query,
        terms=terms,
        papers=top_papers,
        clusters=clusters,
        learning_path=learning_path,
        plan=plan,
        feedback=feedback,
    )

    print(f"\n报告已生成：{report_path}")

    print("\n## Top Papers")
    for i, paper in enumerate(top_papers[:20], 1):
        print(f"\n### {i}. {paper['title']}")
        print("Year:", paper["year"])
        print("Citations:", paper["citations"])
        print("Source:", paper["source"])
        print("Subdomain:", paper["matched_subdomain"])
        print("Query:", paper["matched_query"])
        print("Final Score:", paper["final_score"])
        print("URL:", paper["url"])


if __name__ == "__main__":
    main()