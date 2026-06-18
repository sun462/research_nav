import os
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

OPENALEX_URL = "https://api.openalex.org/works"


def recover_abstract(inv):
    if not inv:
        return ""

    words = []
    for word, positions in inv.items():
        for pos in positions:
            words.append((pos, word))

    return " ".join(word for _, word in sorted(words))


def discover_terms(user_query):
    prompt = f"""
用户想研究：{user_query}

请生成：
1. 相关术语
2. OpenAlex检索关键词
3. 同义词/近义词

要求：
- terms 适合给新手理解领域
- search_queries 适合直接用于 OpenAlex 检索
- search_queries 尽量使用英文
- 只返回 JSON，不要返回 Markdown，不要返回解释

JSON格式：
{{
  "terms": ["term1", "term2"],
  "search_queries": ["query1", "query2"]
}}
"""

    resp = client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    text = resp.choices[0].message.content.strip()

    # 防止模型返回 ```json ... ```
    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)


def search_papers(search_queries, per_query=10):
    papers = {}

    for q in search_queries:
        params = {
            "search": q,
            "per-page": per_query,
            "sort": "relevance_score:desc",
            "filter": "has_abstract:true",
        }

        response = requests.get(OPENALEX_URL, params=params, timeout=20)
        response.raise_for_status()

        results = response.json().get("results", [])

        for item in results:
            paper_id = item.get("id")

            if not paper_id:
                continue

            papers[paper_id] = {
                "title": item.get("display_name", ""),
                "year": item.get("publication_year"),
                "citations": item.get("cited_by_count", 0),
                "abstract": recover_abstract(item.get("abstract_inverted_index")),
                "url": item.get("doi") or item.get("id"),
                "relevance_score": item.get("relevance_score", 0),
            }

    return list(papers.values())


def rank_papers(papers, user_query):
    return sorted(
        papers,
        key=lambda p: (
            p.get("year") or 0,
            p.get("citations") or 0,
            p.get("relevance_score") or 0,
        ),
        reverse=True,
    )

def cluster_topics(papers):
    paper_text = "\n\n".join([
        f"Title: {p['title']}\nYear: {p['year']}\nCitations: {p['citations']}\nAbstract: {p['abstract'][:1000]}"
        for p in papers[:20]
    ])

    prompt = f"""
下面是一个研究主题下检索到的论文列表。

请根据论文标题和摘要，把它们聚类成 4-6 个研究方向。

要求：
- 每个方向包含 direction_name
- 每个方向包含 description
- 每个方向包含 related_papers，使用论文标题
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

    resp = client.chat.completions.create(
        model="qwen-plus",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    text = resp.choices[0].message.content.strip()
    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)["clusters"]

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

    resp = client.chat.completions.create(
        model="qwen-plus",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    text = resp.choices[0].message.content.strip()
    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)["learning_path"]

def generate_report(user_query, terms, papers, clusters, learning_path):
    os.makedirs("outputs", exist_ok=True)

    must_read = sorted(
        papers,
        key=lambda p: p.get("citations") or 0,
        reverse=True
    )[:8]

    frontier = sorted(
        papers,
        key=lambda p: p.get("year") or 0,
        reverse=True
    )[:8]

    report = f"# Research Navigator Report\n\n"
    report += f"研究主题：{user_query}\n\n"

    report += "## 1. 术语发现\n\n"
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
        report += f"- URL: {p['url']}\n"
        report += f"- Abstract: {p['abstract'][:600]}...\n\n"

    report += "\n## 4. 前沿论文\n\n"
    for p in frontier:
        report += f"### {p['title']}\n\n"
        report += f"- Year: {p['year']}\n"
        report += f"- Citations: {p['citations']}\n"
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

    with open("outputs/report.md", "w", encoding="utf-8") as f:
        f.write(report)

    return "outputs/report.md"

def main():
    user_query = input("Research topic: ").strip()

    if not user_query:
        print("请输入研究主题")
        return

    print("\n正在生成术语和检索词...")
    discovered = discover_terms(user_query)

    terms = discovered.get("terms", [])
    search_queries = discovered.get("search_queries", [])

    print("\n## Terms")
    for term in terms:
        print("-", term)

    print("\n## Search Queries")
    for query in search_queries:
        print("-", query)

    print("\n正在搜索 OpenAlex 论文...")
    papers = search_papers(search_queries)

    ranked = rank_papers(papers, user_query)[:20]

    print("\n## Top Papers")
    for i, paper in enumerate(ranked, 1):
        print(f"\n### {i}. {paper['title']}")
        print("Year:", paper["year"])
        print("Citations:", paper["citations"])
        print("URL:", paper["url"])
        print("Abstract:", paper["abstract"][:800])

    clusters = cluster_topics(ranked)
    learning_path = generate_learning_path(user_query, terms, clusters)
    report_path = generate_report(user_query, terms, ranked, clusters, learning_path)

    print(f"\n报告已生成：{report_path}")


if __name__ == "__main__":
    main()