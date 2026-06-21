#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v1.1.1 搜索阶段.搜索源与搜索词.修改但有问题

Key design changes:
1. global_queries are only used for topic exploration and planning, never direct paper recall.
2. Venue participates in both recall and evaluation.
3. arXiv is treated as frontier/preprint source; OpenAlex/DOI/publisher metadata is canonical when available.
4. Feedback detects recent trends such as LLM, VLM, foundation model, agent, RL, diffusion, world model.
5. OpenAlex calls include cache, global rate limit, exponential backoff, and optional mailto.

Environment variables:
- QWEN_API_KEY: required for DashScope compatible OpenAI API
- OPENALEX_MAILTO: recommended, your email for OpenAlex polite pool

Run:
    python main.py
"""

import os
import re
import json
import math
import time
import random
import hashlib
import requests
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import quote

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# -----------------------------
# Config
# -----------------------------

OPENALEX_URL = "https://api.openalex.org/works"
ARXIV_URL = "http://export.arxiv.org/api/query"
CACHE_DIR = "cache"
OUTPUT_DIR = "outputs"

OPENALEX_MAILTO = os.getenv("OPENALEX_MAILTO", "").strip()
OPENALEX_MIN_INTERVAL_SECONDS = float(os.getenv("OPENALEX_MIN_INTERVAL_SECONDS", "3.0"))
OPENALEX_MAX_RETRIES = int(os.getenv("OPENALEX_MAX_RETRIES", "2"))
OPENALEX_MAX_CALLS_PER_RUN = int(os.getenv("OPENALEX_MAX_CALLS_PER_RUN", "25"))
OPENALEX_DISABLE_AFTER_429 = int(os.getenv("OPENALEX_DISABLE_AFTER_429", "2"))
OPENALEX_COOLDOWN_SECONDS = float(os.getenv("OPENALEX_COOLDOWN_SECONDS", "1200"))
OPENALEX_LONG_RETRY = os.getenv("OPENALEX_LONG_RETRY", "0") == "1"
OPENALEX_LIGHT_MODE = os.getenv("OPENALEX_LIGHT_MODE", "1") == "1"
OPENALEX_ENABLED = os.getenv("OPENALEX_ENABLED", "1") == "1"

DEFAULT_PER_QUERY_OPENALEX = int(os.getenv("PER_QUERY_OPENALEX", "3"))
DEFAULT_PER_QUERY_ARXIV = int(os.getenv("PER_QUERY_ARXIV", "6"))
MAX_SUBDOMAINS = int(os.getenv("MAX_SUBDOMAINS", "4"))
MAX_QUERIES_PER_SUBDOMAIN = int(os.getenv("MAX_QUERIES_PER_SUBDOMAIN", "2"))
MAX_VENUES_PER_QUERY = int(os.getenv("MAX_VENUES_PER_QUERY", "1"))

TREND_TERMS = {
    "llm": ["large language model", "llm", "language model"],
    "vlm": ["vision language model", "vlm", "multimodal large language model", "multimodal foundation model"],
    "foundation_model": ["foundation model", "foundation models", "pretrained model", "pre-trained model"],
    "agent": ["agent", "agents", "autonomous agent", "tool use", "planning agent"],
    "reinforcement_learning": ["reinforcement learning", "rl", "policy learning", "reward model"],
    "diffusion": ["diffusion model", "score-based", "denoising diffusion"],
    "world_model": ["world model", "model-based", "latent dynamics"],
    "transformer": ["transformer", "attention model", "self-attention"],
}


# -----------------------------
# LLM client
# -----------------------------

client = OpenAI(
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    timeout=60.0,
)


def call_qwen_json(prompt: str, temperature: float = 0.2, fallback: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Call Qwen and parse a JSON object robustly."""
    try:
        resp = client.chat.completions.create(
            model="qwen-plus",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        text = (resp.choices[0].message.content or "").strip()
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            text = text[start:end + 1]
        text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
        return json.loads(text)
    except Exception as exc:
        print("\n[Qwen JSON Parse Failed]")
        print("Error:", exc)
        if fallback is not None:
            print("使用 fallback 继续运行。")
            return fallback
        raise


# -----------------------------
# Utilities
# -----------------------------

_LAST_OPENALEX_REQUEST_TIME = 0.0
_OPENALEX_CALL_COUNT = 0
_OPENALEX_429_STREAK = 0
_OPENALEX_COOLDOWN_UNTIL = 0.0


def ensure_dirs() -> None:
    os.makedirs(CACHE_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def clean_search_query(query: str) -> str:
    if not query:
        return ""
    query = str(query)
    query = query.replace("(", " ").replace(")", " ")
    query = re.sub(r"\bAND\b|\bOR\b", " ", query, flags=re.IGNORECASE)
    query = query.replace("*", "")
    query = query.replace("/", " ")
    query = re.sub(r'"([^"]+)"', r"\1", query)
    query = re.sub(r"\s+", " ", query)
    return query.strip()


def normalize_title(title: str) -> str:
    title = (title or "").lower().strip()
    title = re.sub(r"[^a-z0-9\u4e00-\u9fff ]+", "", title)
    title = re.sub(r"\s+", " ", title)
    return title


def normalize_doi(doi: str) -> str:
    doi = (doi or "").strip().lower()
    doi = doi.replace("https://doi.org/", "").replace("http://doi.org/", "")
    return doi


def cache_key(prefix: str, payload: Dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]
    return os.path.join(CACHE_DIR, f"{prefix}_{digest}.json")


def load_cache(path: str) -> Optional[Any]:
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def save_cache(path: str, data: Any) -> None:
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as exc:
        print(f"[Cache Save Failed] {exc}")


def recover_abstract(inv: Optional[Dict[str, List[int]]]) -> str:
    if not inv:
        return ""
    words: List[Tuple[int, str]] = []
    for word, positions in inv.items():
        for pos in positions:
            words.append((pos, word))
    return " ".join(word for _, word in sorted(words))


def year_score(year: Optional[int]) -> float:
    if not year:
        return 0.0
    if year >= 2026:
        return 1.0
    if year >= 2025:
        return 0.98
    if year >= 2024:
        return 0.95
    if year >= 2023:
        return 0.88
    if year >= 2022:
        return 0.78
    if year >= 2020:
        return 0.6
    if year >= 2015:
        return 0.35
    return 0.15


def citation_score(citations: int) -> float:
    return min(1.0, math.log1p(max(0, citations)) / math.log1p(1000))


def relevance_score(raw: Optional[float]) -> float:
    if raw is None:
        return 0.3
    try:
        return min(1.0, float(raw) / 100.0)
    except Exception:
        return 0.3


def source_score(source: str) -> float:
    if source == "openalex":
        return 0.85
    if source == "arxiv":
        return 0.45
    return 0.5


def channel_score(channel: str) -> float:
    return {
        "venue_aware": 1.0,
        "recent": 0.92,
        "citation": 0.9,
        "survey": 0.86,
        "topic": 0.78,
        "frontier": 0.76,
    }.get(channel, 0.6)


def text_contains_any(text: str, terms: List[str]) -> bool:
    t = (text or "").lower()
    return any(term.lower() in t for term in terms)


# -----------------------------
# OpenAlex and arXiv API
# -----------------------------


def openalex_can_try(verbose: bool = False) -> bool:
    """Return whether it is worth making a live OpenAlex request now."""
    if not OPENALEX_ENABLED:
        return False
    now = time.time()
    if now < _OPENALEX_COOLDOWN_UNTIL:
        if verbose:
            remaining = int(_OPENALEX_COOLDOWN_UNTIL - now)
            print(f"[OpenAlex cooldown] 跳过本次请求，剩余约 {remaining}s；继续使用 arXiv/缓存结果。")
        return False
    if _OPENALEX_CALL_COUNT >= OPENALEX_MAX_CALLS_PER_RUN:
        if verbose:
            print(f"[OpenAlex budget] 本轮已达到 {OPENALEX_MAX_CALLS_PER_RUN} 次请求上限；跳过后续 OpenAlex。")
        return False
    return True


def rate_limit_openalex() -> None:
    global _LAST_OPENALEX_REQUEST_TIME
    now = time.time()
    delta = now - _LAST_OPENALEX_REQUEST_TIME
    if delta < OPENALEX_MIN_INTERVAL_SECONDS:
        time.sleep(OPENALEX_MIN_INTERVAL_SECONDS - delta)
    _LAST_OPENALEX_REQUEST_TIME = time.time()


def openalex_get(params: Dict[str, Any], max_retries: int = OPENALEX_MAX_RETRIES) -> Optional[Dict[str, Any]]:
    """OpenAlex GET with cache, mailto, global rate limit and fail-fast 429 protection.

    Important behavior:
    - Cached responses are returned even when the current run is in cooldown.
    - If OpenAlex starts returning 429 repeatedly, this function stops calling OpenAlex
      for the rest of the cooldown window instead of sleeping for many minutes.
    - arXiv recall continues, so the whole pipeline can still finish.
    """
    global _OPENALEX_CALL_COUNT, _OPENALEX_429_STREAK, _OPENALEX_COOLDOWN_UNTIL

    params = {k: v for k, v in params.items() if v is not None and v != ""}
    if OPENALEX_MAILTO:
        params.setdefault("mailto", OPENALEX_MAILTO)

    ck = cache_key("openalex", params)
    cached = load_cache(ck)
    if cached is not None:
        return cached

    if not openalex_can_try(verbose=True):
        return None

    headers = {
        "User-Agent": f"ResearchNavigatorV2/1.0 ({OPENALEX_MAILTO or 'please-set-OPENALEX_MAILTO'})"
    }

    for attempt in range(max_retries):
        try:
            rate_limit_openalex()
            _OPENALEX_CALL_COUNT += 1
            response = requests.get(OPENALEX_URL, params=params, headers=headers, timeout=30)

            if response.status_code == 429:
                _OPENALEX_429_STREAK += 1

                if _OPENALEX_429_STREAK >= OPENALEX_DISABLE_AFTER_429:
                    _OPENALEX_COOLDOWN_UNTIL = time.time() + OPENALEX_COOLDOWN_SECONDS
                    print(
                        f"[OpenAlex 429] 连续 {_OPENALEX_429_STREAK} 次限流；"
                        f"进入 cooldown {int(OPENALEX_COOLDOWN_SECONDS)}s，后续跳过 OpenAlex。"
                    )
                    return None

                retry_after = response.headers.get("Retry-After")
                if OPENALEX_LONG_RETRY and retry_after and retry_after.isdigit():
                    wait = min(90.0, float(retry_after))
                else:
                    wait = min(15.0, 4.0 * (2 ** attempt) + random.uniform(0.5, 2.0))
                print(f"[OpenAlex 429] 短等待 {wait:.1f}s 后重试；如继续 429 将跳过 OpenAlex。")
                time.sleep(wait)
                continue

            response.raise_for_status()
            _OPENALEX_429_STREAK = 0
            data = response.json()
            save_cache(ck, data)
            return data

        except requests.exceptions.HTTPError as exc:
            print(f"[OpenAlex HTTP Error] {exc}")
            return None
        except Exception as exc:
            wait = min(10.0, 2.0 + attempt * 2.0)
            print(f"[OpenAlex Error] {exc}; wait {wait:.1f}s")
            time.sleep(wait)

    return None


def arxiv_tokens(query: str, max_tokens: int = 6) -> List[str]:
    stop = {
        "a", "an", "the", "and", "or", "of", "for", "in", "on", "to", "with", "by", "from",
        "based", "using", "approach", "method", "system", "research", "study", "safe", "real", "time"
    }
    toks = re.findall(r"[A-Za-z][A-Za-z0-9-]{2,}", query.lower())
    out = []
    for t in toks:
        if t in stop:
            continue
        if t not in out:
            out.append(t)
        if len(out) >= max_tokens:
            break
    return out


def build_arxiv_expressions(query: str) -> List[str]:
    """Build progressively broader arXiv search expressions.

    Exact phrase search like all:"visual inertial slam based navigation" often returns 0.
    Try exact phrase -> title/abstract phrase -> keyword AND -> keyword OR.
    """
    query = clean_search_query(query)
    if not query:
        return []
    expressions = [f'all:"{query}"', f'ti:"{query}" OR abs:"{query}"']
    toks = arxiv_tokens(query, max_tokens=6)
    if len(toks) >= 2:
        expressions.append(" AND ".join(f"all:{t}" for t in toks[:4]))
        expressions.append(" OR ".join(f"all:{t}" for t in toks[:6]))
    elif len(toks) == 1:
        expressions.append(f"all:{toks[0]}")

    seen = set()
    uniq = []
    for e in expressions:
        if e not in seen:
            seen.add(e)
            uniq.append(e)
    return uniq


def build_arxiv_url_from_expression(expression: str, per_query: int) -> str:
    encoded = quote(expression)
    return (
        f"{ARXIV_URL}?"
        f"search_query={encoded}"
        f"&start=0&max_results={per_query}"
        f"&sortBy=submittedDate&sortOrder=descending"
    )


def arxiv_xml_has_entries(xml_text: str) -> bool:
    return "<entry>" in xml_text


def arxiv_get(query: str, per_query: int) -> Optional[str]:
    expressions = build_arxiv_expressions(query)
    if not expressions:
        return None
    payload = {"query": query, "expressions": expressions, "per_query": per_query}
    ck = cache_key("arxiv", payload)
    cached = load_cache(ck)
    if cached is not None:
        return cached.get("xml", "")

    last_xml = None
    for idx, expression in enumerate(expressions, 1):
        url = build_arxiv_url_from_expression(expression, per_query)
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            xml_text = response.text
            last_xml = xml_text
            if arxiv_xml_has_entries(xml_text):
                if idx > 1:
                    print(f"[arXiv fallback hit] {query} -> {expression}")
                save_cache(ck, {"xml": xml_text, "expression": expression})
                time.sleep(1.0)
                return xml_text
            time.sleep(1.0)
        except Exception as exc:
            print(f"[arXiv Error] query={query}, expression={expression}, error={exc}")

    if last_xml:
        print(f"[arXiv empty] {query} 的所有 fallback 查询均无结果。")
        save_cache(ck, {"xml": last_xml, "expression": expressions[-1]})
        return last_xml
    return None


# -----------------------------
# Planning
# -----------------------------


def discover_terms(user_query: str) -> Dict[str, Any]:
    fallback = {
        "terms": [user_query],
        "global_queries": [user_query],
        "seed_paper_queries": [f"{user_query} survey", f"{user_query} benchmark"],
    }
    prompt = f"""
用户想研究：{user_query}

请生成用于学术检索规划的概念地图。

要求：
1. terms 是给人看的核心概念。
2. global_queries 只用于理解主题、发现子领域、发现术语，不允许直接作为最终论文召回 query。
3. seed_paper_queries 用于找 survey、benchmark、canonical paper。
4. 尽量使用英文。
5. 不要使用 AND / OR / 括号 / 通配符。
6. 所有字符串内部不要包含换行符。
7. 只返回 JSON，不要 Markdown。

JSON格式：
{{
  "terms": ["term1", "term2"],
  "global_queries": ["broad exploration query"],
  "seed_paper_queries": ["survey query", "benchmark query"]
}}
"""
    return call_qwen_json(prompt, fallback=fallback)


def plan_retrieval_sources(user_query: str, terms: List[str], global_queries: List[str], seed_queries: List[str]) -> Dict[str, Any]:
    fallback = {
        "global_queries": global_queries,
        "seed_paper_queries": seed_queries,
        "source_weights": {"openalex": 0.70, "arxiv": 0.12, "venue_aware": 0.18},
        "recall_channels": {"topic": 0.34, "recent": 0.25, "venue_aware": 0.21, "survey": 0.10, "frontier": 0.10},
        "subdomains": [{
            "name": "Core Research Direction",
            "weight": 1.0,
            "must_cover": True,
            "description": "Core direction inferred from user query.",
            "queries": [user_query],
            "preferred_venues": [],
        }],
    }

    prompt = f"""
用户研究主题：{user_query}

术语：
{json.dumps(terms, ensure_ascii=False)}

探索性全局检索词，注意这些词只用于理解主题，不参与最终论文召回：
{json.dumps(global_queries, ensure_ascii=False)}

Seed paper queries：
{json.dumps(seed_queries, ensure_ascii=False)}

请生成一个多路召回学术检索计划。

核心原则：
1. global_queries 绝对不能进入正式召回 queries。
2. 正式召回必须基于 subdomain-specific queries。
3. 每个子领域给出 weight、queries、preferred_venues、must_cover。
4. 如果该领域近年可能有 LLM / VLM / Foundation Model / Reinforcement Learning / Agent / Diffusion / World Model 趋势，必须单独作为候选子领域，哪怕权重较低。
5. queries 使用自然语言，不要使用 AND / OR / 括号 / 通配符。
6. preferred_venues 写会议/期刊/数据库名，比如 NeurIPS, ICML, ICLR, CVPR, ACL, EMNLP, ICRA, IROS, CoRL, SIGGRAPH, Nature, Science, IEEE Transactions。
7. arXiv 只能作为前沿补充。
8. 子领域不超过 {MAX_SUBDOMAINS} 个，每个子领域 queries 不超过 {MAX_QUERIES_PER_SUBDOMAIN} 个。
9. 所有字符串内部不要包含换行符。
10. 只返回 JSON，不要 Markdown。

JSON格式：
{{
  "global_queries": ["only for exploration, not for final recall"],
  "seed_paper_queries": ["survey query", "benchmark query"],
  "source_weights": {{"openalex": 0.70, "arxiv": 0.12, "venue_aware": 0.18}},
  "recall_channels": {{"topic": 0.34, "recent": 0.25, "venue_aware": 0.21, "survey": 0.10, "frontier": 0.10}},
  "subdomains": [
    {{
      "name": "subdomain name",
      "weight": 0.25,
      "must_cover": true,
      "description": "why this direction matters",
      "queries": ["specific query 1"],
      "preferred_venues": ["NeurIPS", "ICML", "ICLR"]
    }}
  ]
}}
"""
    plan = call_qwen_json(prompt, fallback=fallback)
    plan.setdefault("global_queries", global_queries)
    plan.setdefault("seed_paper_queries", seed_queries)
    plan.setdefault("source_weights", fallback["source_weights"])
    plan.setdefault("recall_channels", fallback["recall_channels"])
    plan.setdefault("subdomains", fallback["subdomains"])
    plan["subdomains"] = sanitize_subdomains(plan.get("subdomains", []), user_query)
    return plan


def sanitize_subdomains(subdomains: List[Dict[str, Any]], user_query: str) -> List[Dict[str, Any]]:
    cleaned: List[Dict[str, Any]] = []
    seen = set()
    for sub in subdomains[:MAX_SUBDOMAINS]:
        name = str(sub.get("name") or "Unnamed Subdomain").strip()
        if not name or name.lower() in seen:
            continue
        seen.add(name.lower())
        queries = [clean_search_query(q) for q in sub.get("queries", []) if clean_search_query(q)]
        if not queries:
            queries = [clean_search_query(user_query)]
        venues = [str(v).strip() for v in sub.get("preferred_venues", []) if str(v).strip()]
        cleaned.append({
            "name": name,
            "weight": float(sub.get("weight", 0.2) or 0.2),
            "must_cover": bool(sub.get("must_cover", True)),
            "description": str(sub.get("description", "")),
            "queries": queries[:MAX_QUERIES_PER_SUBDOMAIN],
            "preferred_venues": venues[:8],
        })
    if not cleaned:
        cleaned.append({
            "name": "Core Research Direction",
            "weight": 1.0,
            "must_cover": True,
            "description": "Fallback core direction.",
            "queries": [clean_search_query(user_query)],
            "preferred_venues": [],
        })
    return cleaned


# -----------------------------
# Retrieval
# -----------------------------


def get_venue_score(paper: Dict[str, Any], preferred_venues: List[str]) -> float:
    venue_text = " ".join([
        str(paper.get("venue", "")),
        str(paper.get("source_display_name", "")),
        str(paper.get("host_venue", "")),
    ]).lower()
    for venue in preferred_venues:
        if venue and venue.lower() in venue_text:
            return 1.0
    return 0.0


def parse_openalex_item(item: Dict[str, Any], query: str, subdomain_name: str, channel: str, preferred_venues: List[str]) -> Optional[Dict[str, Any]]:
    paper_id = item.get("id")
    title = item.get("display_name") or ""
    if not paper_id or not title:
        return None
    primary_location = item.get("primary_location") or {}
    source = primary_location.get("source") or {}
    venue_name = source.get("display_name", "") or ""
    doi = normalize_doi(item.get("doi") or "")
    paper = {
        "id": paper_id,
        "openalex_id": paper_id,
        "doi": doi,
        "arxiv_id": "",
        "title": title,
        "year": item.get("publication_year"),
        "publication_date": item.get("publication_date"),
        "citations": item.get("cited_by_count", 0) or 0,
        "abstract": recover_abstract(item.get("abstract_inverted_index")),
        "url": item.get("doi") or item.get("id"),
        "source": "openalex",
        "versions": ["openalex"],
        "matched_query": query,
        "matched_subdomain": subdomain_name,
        "recall_channel": channel,
        "relevance_score": item.get("relevance_score", 0),
        "venue": venue_name,
        "source_display_name": venue_name,
        "publication_status": "published" if venue_name or doi else "indexed",
        "is_frontier": False,
    }
    paper["venue_score"] = get_venue_score(paper, preferred_venues)
    return paper


def search_openalex_for_query(
    query: str,
    subdomain_name: str,
    preferred_venues: List[str],
    recall_channel: str = "topic",
    per_query: int = DEFAULT_PER_QUERY_OPENALEX,
    venue_filter: Optional[str] = None,
) -> List[Dict[str, Any]]:
    papers: List[Dict[str, Any]] = []
    query = clean_search_query(query)
    if not query:
        return papers

    filter_parts = ["has_abstract:true", "type:article"]
    sort = "relevance_score:desc"

    if recall_channel in {"recent", "frontier"}:
        filter_parts.append("from_publication_date:2022-01-01")
        sort = "publication_date:desc"
    elif recall_channel == "citation":
        sort = "cited_by_count:desc"
    elif recall_channel == "survey":
        sort = "cited_by_count:desc"

    # OpenAlex source filtering by venue name is not perfectly direct without resolving source IDs.
    # Here venue-aware recall uses search text plus venue phrase. A later improvement can resolve sources IDs.
    search_text = query
    if venue_filter:
        search_text = clean_search_query(f"{query} {venue_filter}")

    params = {
        "search": search_text,
        "per-page": per_query,
        "sort": sort,
        "filter": ",".join(filter_parts),
    }

    data = openalex_get(params)
    if not data:
        return papers

    for item in data.get("results", []):
        paper = parse_openalex_item(item, query, subdomain_name, recall_channel, preferred_venues)
        if paper:
            if venue_filter:
                paper["matched_venue_query"] = venue_filter
            papers.append(paper)
    return papers


def parse_arxiv_id(link: str) -> str:
    link = link or ""
    if "/abs/" in link:
        return link.split("/abs/", 1)[1]
    return link.rstrip("/").split("/")[-1]


def search_arxiv_for_query(
    query: str,
    subdomain_name: str,
    recall_channel: str = "frontier",
    per_query: int = DEFAULT_PER_QUERY_ARXIV,
) -> List[Dict[str, Any]]:
    papers: List[Dict[str, Any]] = []
    query = clean_search_query(query)
    if not query:
        return papers
    xml_text = arxiv_get(query, per_query)
    if not xml_text:
        return papers
    try:
        root = ET.fromstring(xml_text)
    except Exception as exc:
        print(f"[arXiv XML Error] {exc}")
        return papers

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    for entry in root.findall("atom:entry", ns):
        title = entry.findtext("atom:title", default="", namespaces=ns)
        abstract = entry.findtext("atom:summary", default="", namespaces=ns)
        link = entry.findtext("atom:id", default="", namespaces=ns)
        published = entry.findtext("atom:published", default="", namespaces=ns)
        try:
            year = int(published[:4]) if published else None
        except Exception:
            year = None
        title = re.sub(r"\s+", " ", title).strip()
        abstract = re.sub(r"\s+", " ", abstract).strip()
        if not title:
            continue
        paper = {
            "id": link,
            "openalex_id": "",
            "doi": "",
            "arxiv_id": parse_arxiv_id(link),
            "title": title,
            "year": year,
            "publication_date": published[:10] if published else "",
            "citations": 0,
            "abstract": abstract,
            "url": link,
            "source": "arxiv",
            "versions": ["arxiv"],
            "matched_query": query,
            "matched_subdomain": subdomain_name,
            "recall_channel": recall_channel,
            "relevance_score": 0,
            "venue": "arXiv",
            "source_display_name": "arXiv",
            "venue_score": 0.0,
            "publication_status": "preprint",
            "is_frontier": True,
        }
        papers.append(paper)
    return papers


def seed_recall(plan: Dict[str, Any], per_query_openalex: int) -> List[Dict[str, Any]]:
    papers: List[Dict[str, Any]] = []
    # In light mode, do not spend the first OpenAlex calls on broad seed queries.
    if OPENALEX_LIGHT_MODE or not openalex_can_try():
        return papers
    seed_limit = 2
    for q in plan.get("seed_paper_queries", [])[:seed_limit]:
        q = clean_search_query(q)
        if not q:
            continue
        papers.extend(search_openalex_for_query(q, "Seed Papers", [], "survey", per_query=max(3, per_query_openalex)))
    return papers


def multi_source_search(plan: Dict[str, Any], per_query_openalex: int = DEFAULT_PER_QUERY_OPENALEX, per_query_arxiv: int = DEFAULT_PER_QUERY_ARXIV) -> List[Dict[str, Any]]:
    all_papers: List[Dict[str, Any]] = []
    recall_channels = plan.get("recall_channels", {})

    print("[Recall] Seed papers...")
    all_papers.extend(seed_recall(plan, per_query_openalex=max(5, per_query_openalex // 2)))

    for subdomain in plan.get("subdomains", []):
        subdomain_name = subdomain.get("name", "unknown")
        preferred_venues = subdomain.get("preferred_venues", [])
        queries = subdomain.get("queries", [])[:MAX_QUERIES_PER_SUBDOMAIN]

        for query in queries:
            query = clean_search_query(query)
            if not query:
                continue

            # arXiv first: it is less likely to block and keeps the pipeline moving.
            if recall_channels.get("frontier", 0) > 0:
                all_papers.extend(search_arxiv_for_query(query, subdomain_name, "frontier", per_query_arxiv))

            if recall_channels.get("topic", 0) > 0 and openalex_can_try():
                all_papers.extend(search_openalex_for_query(query, subdomain_name, preferred_venues, "topic", per_query_openalex))

            # Light mode disables the heaviest OpenAlex channels by default.
            if openalex_can_try() and not OPENALEX_LIGHT_MODE and recall_channels.get("recent", 0) > 0:
                all_papers.extend(search_openalex_for_query(query, subdomain_name, preferred_venues, "recent", per_query_openalex))

            if openalex_can_try() and not OPENALEX_LIGHT_MODE and recall_channels.get("survey", 0) > 0:
                survey_query = clean_search_query(f"{query} survey review benchmark")
                all_papers.extend(search_openalex_for_query(survey_query, subdomain_name, preferred_venues, "survey", max(3, per_query_openalex // 2)))

            if openalex_can_try() and not OPENALEX_LIGHT_MODE and recall_channels.get("venue_aware", 0) > 0 and preferred_venues:
                for venue in preferred_venues[:MAX_VENUES_PER_QUERY]:
                    all_papers.extend(search_openalex_for_query(query, subdomain_name, preferred_venues, "venue_aware", max(3, per_query_openalex // 2), venue_filter=venue))

    return deduplicate_and_merge_papers(all_papers)


# -----------------------------
# Dedup and merge
# -----------------------------


def paper_identity_key(p: Dict[str, Any]) -> str:
    doi = normalize_doi(p.get("doi", ""))
    if doi:
        return f"doi:{doi}"
    arxiv_id = p.get("arxiv_id", "")
    if arxiv_id:
        return f"arxiv:{arxiv_id.lower()}"
    return f"title:{normalize_title(p.get('title', ''))}"


def prefer_canonical(old: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
    # Prefer published/OpenAlex metadata as canonical, but merge useful preprint version data.
    old_source = old.get("source")
    new_source = new.get("source")
    if old_source == "arxiv" and new_source == "openalex":
        canonical, secondary = new, old
    elif old_source == "openalex" and new_source == "arxiv":
        canonical, secondary = old, new
    elif (new.get("citations", 0) or 0) > (old.get("citations", 0) or 0):
        canonical, secondary = new, old
    elif (new.get("venue_score", 0) or 0) > (old.get("venue_score", 0) or 0):
        canonical, secondary = new, old
    else:
        canonical, secondary = old, new

    versions = set(canonical.get("versions", [])) | set(secondary.get("versions", []))
    canonical["versions"] = sorted(versions)
    if not canonical.get("arxiv_id") and secondary.get("arxiv_id"):
        canonical["arxiv_id"] = secondary.get("arxiv_id")
    if not canonical.get("doi") and secondary.get("doi"):
        canonical["doi"] = secondary.get("doi")
    if not canonical.get("abstract") and secondary.get("abstract"):
        canonical["abstract"] = secondary.get("abstract")
    if secondary.get("url") and secondary.get("source") == "arxiv":
        canonical["arxiv_url"] = secondary.get("url")
    if secondary.get("url") and secondary.get("source") == "openalex":
        canonical["openalex_url"] = secondary.get("url")
    if "openalex" in versions and canonical.get("venue") != "arXiv":
        canonical["publication_status"] = "published" if canonical.get("venue") or canonical.get("doi") else "indexed"
    return canonical


def deduplicate_and_merge_papers(papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    deduped: Dict[str, Dict[str, Any]] = {}
    title_index: Dict[str, str] = {}

    for paper in papers:
        title_key = normalize_title(paper.get("title", ""))
        if not title_key:
            continue
        key = paper_identity_key(paper)
        if key.startswith("title:") and title_key in title_index:
            key = title_index[title_key]
        else:
            title_index[title_key] = key

        if key not in deduped:
            deduped[key] = paper
        else:
            deduped[key] = prefer_canonical(deduped[key], paper)

    return list(deduped.values())


# -----------------------------
# Rerank and feedback
# -----------------------------


def get_subdomain_weight(plan: Dict[str, Any], subdomain_name: str) -> float:
    if subdomain_name == "Seed Papers":
        return 0.8
    for sub in plan.get("subdomains", []):
        if sub.get("name") == subdomain_name:
            try:
                return float(sub.get("weight", 0.2))
            except Exception:
                return 0.2
    return 0.1


def detect_paper_trends(paper: Dict[str, Any]) -> List[str]:
    text = f"{paper.get('title', '')} {paper.get('abstract', '')}".lower()
    hits = []
    for trend, terms in TREND_TERMS.items():
        if any(term in text for term in terms):
            hits.append(trend)
    return hits


def rerank_papers(papers: List[Dict[str, Any]], user_query: str, plan: Dict[str, Any]) -> List[Dict[str, Any]]:
    for paper in papers:
        rel = relevance_score(paper.get("relevance_score", 0))
        cite = citation_score(paper.get("citations", 0) or 0)
        rec = year_score(paper.get("year"))
        venue = float(paper.get("venue_score", 0.0) or 0.0)
        src = source_score(paper.get("source", ""))
        ch = channel_score(paper.get("recall_channel", ""))
        subw = get_subdomain_weight(plan, paper.get("matched_subdomain", ""))
        trends = detect_paper_trends(paper)
        trend_bonus = 0.08 if trends and (paper.get("year") or 0) >= 2022 else 0.0

        final = (
            0.25 * rel
            + 0.22 * rec
            + 0.17 * venue
            + 0.13 * cite
            + 0.09 * ch
            + 0.06 * src
            + 0.04 * subw
            + trend_bonus
        )

        if paper.get("source") == "arxiv":
            final *= 0.96 if (paper.get("year") or 0) >= 2024 else 0.78

        paper["trend_hits"] = trends
        paper["score_detail"] = {
            "relevance_score": round(rel, 4),
            "recency_score": round(rec, 4),
            "venue_score": round(venue, 4),
            "citation_score": round(cite, 4),
            "channel_score": round(ch, 4),
            "source_score": round(src, 4),
            "subdomain_weight": round(subw, 4),
            "trend_bonus": round(trend_bonus, 4),
        }
        paper["final_score"] = round(final, 4)

    return sorted(papers, key=lambda p: p.get("final_score", 0), reverse=True)


def analyze_feedback(papers: List[Dict[str, Any]], plan: Dict[str, Any], top_k: int = 30) -> Dict[str, Any]:
    top_papers = papers[:top_k]
    source_stats: Dict[str, Dict[str, Any]] = {}
    subdomain_stats: Dict[str, Dict[str, Any]] = {}
    channel_stats: Dict[str, Dict[str, Any]] = {}
    trend_stats: Dict[str, Dict[str, Any]] = {}

    planned_subdomains = [s.get("name") for s in plan.get("subdomains", [])]
    must_cover_subdomains = [s.get("name") for s in plan.get("subdomains", []) if s.get("must_cover", True)]
    planned_text = json.dumps(plan.get("subdomains", []), ensure_ascii=False).lower()

    for paper in papers:
        source = paper.get("source", "unknown")
        subdomain = paper.get("matched_subdomain", "unknown")
        channel = paper.get("recall_channel", "unknown")
        score = paper.get("final_score", 0)

        source_stats.setdefault(source, {"retrieved": 0, "top_selected": 0, "scores": []})
        subdomain_stats.setdefault(subdomain, {"retrieved": 0, "top_selected": 0, "scores": [], "venue_hits": 0})
        channel_stats.setdefault(channel, {"retrieved": 0, "top_selected": 0, "scores": []})

        source_stats[source]["retrieved"] += 1
        source_stats[source]["scores"].append(score)
        subdomain_stats[subdomain]["retrieved"] += 1
        subdomain_stats[subdomain]["scores"].append(score)
        if paper.get("venue_score", 0) > 0:
            subdomain_stats[subdomain]["venue_hits"] += 1
        channel_stats[channel]["retrieved"] += 1
        channel_stats[channel]["scores"].append(score)

        if (paper.get("year") or 0) >= 2022:
            for trend in paper.get("trend_hits", []):
                trend_stats.setdefault(trend, {"retrieved_recent": 0, "top_selected_recent": 0, "example_titles": []})
                trend_stats[trend]["retrieved_recent"] += 1
                if len(trend_stats[trend]["example_titles"]) < 5:
                    trend_stats[trend]["example_titles"].append(paper.get("title", ""))

    for paper in top_papers:
        source = paper.get("source", "unknown")
        subdomain = paper.get("matched_subdomain", "unknown")
        channel = paper.get("recall_channel", "unknown")
        if source in source_stats:
            source_stats[source]["top_selected"] += 1
        if subdomain in subdomain_stats:
            subdomain_stats[subdomain]["top_selected"] += 1
        if channel in channel_stats:
            channel_stats[channel]["top_selected"] += 1
        if (paper.get("year") or 0) >= 2022:
            for trend in paper.get("trend_hits", []):
                trend_stats.setdefault(trend, {"retrieved_recent": 0, "top_selected_recent": 0, "example_titles": []})
                trend_stats[trend]["top_selected_recent"] += 1

    def finish_stats(stats_dict: Dict[str, Dict[str, Any]]) -> None:
        for stats in stats_dict.values():
            scores = stats.pop("scores", [])
            stats["avg_score"] = round(sum(scores) / len(scores), 4) if scores else 0.0

    finish_stats(source_stats)
    finish_stats(channel_stats)
    for stats in subdomain_stats.values():
        scores = stats.pop("scores", [])
        stats["avg_score"] = round(sum(scores) / len(scores), 4) if scores else 0.0
        retrieved = stats["retrieved"] or 1
        stats["venue_hit_rate"] = round(stats["venue_hits"] / retrieved, 4)

    covered_subdomains = [s for s in planned_subdomains if subdomain_stats.get(s, {}).get("top_selected", 0) > 0]
    missing_subdomains = [s for s in planned_subdomains if s not in covered_subdomains]
    must_cover_missing = [s for s in must_cover_subdomains if s not in covered_subdomains]
    coverage_score = len(covered_subdomains) / len(planned_subdomains) if planned_subdomains else 0.0

    unplanned_trends = []
    for trend, stats in trend_stats.items():
        if stats.get("top_selected_recent", 0) >= 2 or stats.get("retrieved_recent", 0) >= 5:
            trend_words = [trend.replace("_", " ")] + TREND_TERMS.get(trend, [])
            if not any(w.lower() in planned_text for w in trend_words):
                unplanned_trends.append(trend)

    suggestions: List[str] = []
    if coverage_score < 0.8:
        suggestions.append(f"Topic coverage 不足：计划覆盖 {len(planned_subdomains)} 个子领域，Top{top_k} 只覆盖 {len(covered_subdomains)} 个，需要二次检索。")
    for subdomain in missing_subdomains:
        suggestions.append(f"{subdomain} 在 Top{top_k} 中没有代表论文，应扩展该方向 query，并提高该方向二次检索配额。")
    for subdomain, stats in subdomain_stats.items():
        if subdomain == "Seed Papers":
            continue
        if stats["retrieved"] >= 15 and stats["top_selected"] == 0:
            suggestions.append(f"{subdomain} 召回不少但没有进入 Top{top_k}，query 可能偏离主题，应重写 query。")
        elif stats["retrieved"] < 8:
            suggestions.append(f"{subdomain} 召回数量过少，应扩展 query 或增加 venue-aware recall。")
        if stats["venue_hit_rate"] < 0.03:
            suggestions.append(f"{subdomain} preferred venue 命中率较低，应检查 preferred venues 或改用更具体 venue-aware query。")
    if unplanned_trends:
        suggestions.append(f"近年趋势未被计划覆盖：{', '.join(unplanned_trends)}。应新增对应子领域或 query。")

    return {
        "coverage": {
            "planned_subdomains": planned_subdomains,
            "covered_subdomains": covered_subdomains,
            "missing_subdomains": missing_subdomains,
            "must_cover_missing": must_cover_missing,
            "coverage_score": round(coverage_score, 4),
        },
        "source_stats": source_stats,
        "subdomain_stats": subdomain_stats,
        "channel_stats": channel_stats,
        "trend_stats": trend_stats,
        "unplanned_trends": unplanned_trends,
        "suggestions": suggestions,
    }


def refine_queries(user_query: str, plan: Dict[str, Any], feedback: Dict[str, Any]) -> Dict[str, Any]:
    fallback = plan
    prompt = f"""
用户研究主题：{user_query}

当前检索计划：
{json.dumps(plan, ensure_ascii=False, indent=2)}

检索反馈：
{json.dumps(feedback, ensure_ascii=False, indent=2)}

请根据反馈更新检索计划。

重点：
1. 如果 must_cover 子领域缺失，必须增加更具体 queries。
2. 如果某个子领域召回多但没有进入 Top，必须重写 query。
3. 如果 venue_hit_rate 低，必须检查 preferred_venues 或增加更可能命中顶会/顶刊的表达。
4. 如果 unplanned_trends 里出现 LLM / VLM / Foundation Model / Reinforcement Learning / Agent / Diffusion / World Model，必须新增对应子领域或把 query 加入相关子领域。
5. 不要删除表现好的子领域。
6. global_queries 仍然只用于探索，不参与正式检索。
7. queries 使用普通自然语言，不要使用 AND / OR / 括号 / 通配符。
8. 子领域不超过 {MAX_SUBDOMAINS} 个，每个子领域 queries 不超过 {MAX_QUERIES_PER_SUBDOMAIN} 个。
9. 所有字符串内部不要包含换行符，不要使用未转义双引号。
10. 只返回 JSON，格式与原 plan 一致。
"""
    refined = call_qwen_json(prompt, temperature=0.2, fallback=fallback)
    refined.setdefault("global_queries", plan.get("global_queries", []))
    refined.setdefault("seed_paper_queries", plan.get("seed_paper_queries", []))
    refined.setdefault("source_weights", plan.get("source_weights", {}))
    refined.setdefault("recall_channels", plan.get("recall_channels", {}))
    refined.setdefault("subdomains", plan.get("subdomains", []))
    refined["subdomains"] = sanitize_subdomains(refined.get("subdomains", []), user_query)
    return refined


# -----------------------------
# Clustering, learning path, report
# -----------------------------


def cluster_topics(papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    fallback = {"clusters": []}
    paper_text = "\n\n".join([
        f"Title: {p.get('title', '')}\nYear: {p.get('year')}\nCitations: {p.get('citations')}\nSource: {p.get('source')}\nVenue: {p.get('venue')}\nSubdomain: {p.get('matched_subdomain')}\nTrends: {', '.join(p.get('trend_hits', []))}\nAbstract: {p.get('abstract', '')[:700]}"
        for p in papers[:25]
    ])
    prompt = f"""
下面是一个研究主题下经过多源、多路召回和 rerank 后的论文列表。

请根据论文标题和摘要，把它们聚类成 4-6 个研究方向。

要求：
- 每个方向包含 direction_name
- 每个方向包含 description
- 每个方向包含 related_papers，必须使用给定论文标题，不要编造
- 所有字符串内部不要包含换行符
- 只返回 JSON，不要 Markdown

论文列表：
{paper_text}

JSON格式：
{{
  "clusters": [
    {{"direction_name": "", "description": "", "related_papers": []}}
  ]
}}
"""
    result = call_qwen_json(prompt, fallback=fallback)
    return result.get("clusters", [])


def generate_learning_path(user_query: str, terms: List[str], clusters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    fallback = {"learning_path": []}
    prompt = f"""
用户想研究：{user_query}

术语列表：
{json.dumps(terms, ensure_ascii=False)}

研究方向聚类：
{json.dumps(clusters, ensure_ascii=False)}

请为新手生成一个学习路径。

要求：
- 分成 4-6 个阶段
- 每个阶段包含目标、要学的概念、推荐阅读方向
- 不要编造具体论文
- 所有字符串内部不要包含换行符
- 只返回 JSON

JSON格式：
{{
  "learning_path": [
    {{"stage": "", "goal": "", "concepts": [], "reading_suggestion": ""}}
  ]
}}
"""
    result = call_qwen_json(prompt, fallback=fallback)
    return result.get("learning_path", [])


def format_paper_markdown(p: Dict[str, Any]) -> str:
    versions = ", ".join(p.get("versions", []))
    trends = ", ".join(p.get("trend_hits", []))
    doi = p.get("doi") or ""
    arxiv_id = p.get("arxiv_id") or ""
    arxiv_url = p.get("arxiv_url") or ""
    return (
        f"### {p.get('title', '')}\n\n"
        f"- Year: {p.get('year')}\n"
        f"- Citations: {p.get('citations')}\n"
        f"- Source: {p.get('source')}\n"
        f"- Versions: {versions}\n"
        f"- Publication Status: {p.get('publication_status', '')}\n"
        f"- Venue: {p.get('venue', '')}\n"
        f"- DOI: {doi}\n"
        f"- arXiv ID: {arxiv_id}\n"
        f"- arXiv URL: {arxiv_url}\n"
        f"- Subdomain: {p.get('matched_subdomain', '')}\n"
        f"- Recall Channel: {p.get('recall_channel', '')}\n"
        f"- Query: {p.get('matched_query', '')}\n"
        f"- Trend Hits: {trends}\n"
        f"- Final Score: {p.get('final_score')}\n"
        f"- URL: {p.get('url', '')}\n"
        f"- Abstract: {p.get('abstract', '')[:650]}...\n\n"
    )


def generate_report(user_query: str, terms: List[str], papers: List[Dict[str, Any]], clusters: List[Dict[str, Any]], learning_path: List[Dict[str, Any]], plan: Dict[str, Any], feedback: Dict[str, Any]) -> str:
    ensure_dirs()
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
    report += "### 0.0 Global Query Policy\n\n"
    report += "Global queries are used only for topic exploration and planning. They are not directly used as final paper retrieval queries.\n\n"

    report += "### 0.1 Source Weights\n\n| Source | Weight |\n|---|---:|\n"
    for source, weight in plan.get("source_weights", {}).items():
        report += f"| {source} | {weight} |\n"

    report += "\n### 0.2 Recall Channels\n\n| Channel | Weight |\n|---|---:|\n"
    for channel, weight in plan.get("recall_channels", {}).items():
        report += f"| {channel} | {weight} |\n"

    report += "\n### 0.3 Subdomain Routing\n\n| Subdomain | Weight | Must Cover | Preferred Venues | Queries |\n|---|---:|---|---|---|\n"
    for sub in plan.get("subdomains", []):
        venues = ", ".join(sub.get("preferred_venues", []))
        queries = "; ".join(sub.get("queries", []))
        report += f"| {sub.get('name')} | {sub.get('weight')} | {sub.get('must_cover', True)} | {venues} | {queries} |\n"

    report += "\n### 0.4 Exploratory Global Queries\n\n"
    for q in plan.get("global_queries", []):
        report += f"- {q}\n"

    coverage = feedback.get("coverage", {})
    report += "\n### 0.5 Coverage Feedback\n\n"
    report += f"- Coverage Score: {coverage.get('coverage_score')}\n"
    report += f"- Planned Subdomains: {', '.join(coverage.get('planned_subdomains', []))}\n"
    report += f"- Covered Subdomains: {', '.join(coverage.get('covered_subdomains', []))}\n"
    report += f"- Missing Subdomains: {', '.join(coverage.get('missing_subdomains', []))}\n"
    report += f"- Must-cover Missing: {', '.join(coverage.get('must_cover_missing', []))}\n"
    report += f"- Unplanned Trends: {', '.join(feedback.get('unplanned_trends', []))}\n"

    report += "\n### 0.6 Source Feedback\n\n| Source | Retrieved | Top Selected | Avg Score |\n|---|---:|---:|---:|\n"
    for source, stats in feedback.get("source_stats", {}).items():
        report += f"| {source} | {stats['retrieved']} | {stats['top_selected']} | {stats['avg_score']} |\n"

    report += "\n### 0.7 Recall Channel Feedback\n\n| Channel | Retrieved | Top Selected | Avg Score |\n|---|---:|---:|---:|\n"
    for channel, stats in feedback.get("channel_stats", {}).items():
        report += f"| {channel} | {stats['retrieved']} | {stats['top_selected']} | {stats['avg_score']} |\n"

    report += "\n### 0.8 Subdomain Feedback\n\n| Subdomain | Retrieved | Top Selected | Avg Score | Venue Hit Rate |\n|---|---:|---:|---:|---:|\n"
    for subdomain, stats in feedback.get("subdomain_stats", {}).items():
        report += f"| {subdomain} | {stats['retrieved']} | {stats['top_selected']} | {stats['avg_score']} | {stats['venue_hit_rate']} |\n"

    report += "\n### 0.9 Trend Feedback\n\n"
    for trend, stats in feedback.get("trend_stats", {}).items():
        report += f"- {trend}: recent retrieved={stats.get('retrieved_recent')}, top selected={stats.get('top_selected_recent')}, examples={'; '.join(stats.get('example_titles', [])[:3])}\n"

    report += "\n### 0.10 Feedback Suggestions\n\n"
    for s in feedback.get("suggestions", []):
        report += f"- {s}\n"

    report += "\n## 1. 术语发现\n\n"
    for term in terms:
        report += f"- {term}\n"

    report += "\n## 2. 领域结构 / 研究方向聚类\n\n"
    for cluster in clusters:
        report += f"### {cluster.get('direction_name', '')}\n\n"
        report += f"{cluster.get('description', '')}\n\n相关论文：\n"
        for title in cluster.get("related_papers", []):
            report += f"- {title}\n"
        report += "\n"

    report += "\n## 3. 必读论文\n\n"
    for p in must_read:
        report += format_paper_markdown(p)

    report += "\n## 4. 前沿论文\n\n"
    for p in frontier:
        report += format_paper_markdown(p)

    report += "\n## 5. 新手学习路径\n\n"
    for i, stage in enumerate(learning_path, 1):
        report += f"### 阶段 {i}: {stage.get('stage', '')}\n\n"
        report += f"- 目标：{stage.get('goal', '')}\n"
        report += f"- 概念：{', '.join(stage.get('concepts', []))}\n"
        report += f"- 阅读建议：{stage.get('reading_suggestion', '')}\n\n"

    report += "\n## 6. 推荐 Github / Code Search 检索词\n\n"
    github_keywords = list(terms)
    for cluster in clusters:
        if cluster.get("direction_name"):
            github_keywords.append(cluster.get("direction_name"))
    for kw in github_keywords[:15]:
        if kw:
            report += f"- {kw}\n"

    report += "\n## 7. Top Papers with Source Trace\n\n"
    report += "| Rank | Title | Year | Source | Versions | Channel | Subdomain | Trends | Score |\n"
    report += "|---:|---|---:|---|---|---|---|---|---:|\n"
    for i, p in enumerate(papers[:30], 1):
        title = (p.get("title") or "").replace("|", " ")
        versions = ", ".join(p.get("versions", []))
        trends = ", ".join(p.get("trend_hits", []))
        report += f"| {i} | {title} | {p.get('year')} | {p.get('source')} | {versions} | {p.get('recall_channel')} | {p.get('matched_subdomain')} | {trends} | {p.get('final_score')} |\n"

    path = os.path.join(OUTPUT_DIR, "report.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(report)
    return path


def save_json_debug(name: str, data: Any) -> str:
    ensure_dirs()
    path = os.path.join(OUTPUT_DIR, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path


# -----------------------------
# Main
# -----------------------------


def main() -> None:
    ensure_dirs()
    user_query = input("Research topic: ").strip()
    if not user_query:
        print("请输入研究主题")
        return

    print("\n[1/8] 正在生成术语、探索性全局检索词和 seed queries...")
    discovered = discover_terms(user_query)
    terms = discovered.get("terms", [])
    global_queries = discovered.get("global_queries", [])
    seed_queries = discovered.get("seed_paper_queries", [])
    save_json_debug("01_discovered.json", discovered)

    print("\n## Terms")
    for term in terms:
        print("-", term)
    print("\n## Exploratory Global Queries, not used for final recall")
    for query in global_queries:
        print("-", query)
    print("\n## Seed Paper Queries")
    for query in seed_queries:
        print("-", query)

    print("\n[2/8] 正在生成多源、多路召回计划...")
    plan = plan_retrieval_sources(user_query, terms, global_queries, seed_queries)
    save_json_debug("02_plan.json", plan)
    print("\n## Retrieval Plan")
    print(json.dumps(plan, ensure_ascii=False, indent=2))

    print("\n[3/8] 第一轮多路召回...")
    papers = multi_source_search(plan)
    print(f"第一轮检索后合并去重论文数：{len(papers)}")
    save_json_debug("03_papers_round1.json", papers)

    print("\n[4/8] Reranking 与质量评分...")
    ranked = rerank_papers(papers, user_query, plan)
    save_json_debug("04_ranked_round1.json", ranked[:100])

    print("\n[5/8] 分析反馈和近年趋势...")
    feedback = analyze_feedback(ranked, plan)
    save_json_debug("05_feedback_round1.json", feedback)
    print("\n## Feedback")
    print(json.dumps(feedback, ensure_ascii=False, indent=2))

    coverage = feedback.get("coverage", {})
    need_second_round = False
    if coverage.get("coverage_score", 1.0) < 0.8:
        need_second_round = True
    if coverage.get("must_cover_missing"):
        need_second_round = True
    if feedback.get("unplanned_trends"):
        need_second_round = True
    if any("query" in s.lower() or "缺失" in s or "重写" in s for s in feedback.get("suggestions", [])):
        need_second_round = True

    if need_second_round:
        print("\n[6/8] 覆盖或趋势不足，尝试第二轮检索...")
        try:
            refined_plan = refine_queries(user_query, plan, feedback)
            save_json_debug("06_refined_plan.json", refined_plan)
            second_papers = multi_source_search(refined_plan)
            merged = deduplicate_and_merge_papers(ranked + second_papers)
            ranked = rerank_papers(merged, user_query, refined_plan)
            feedback = analyze_feedback(ranked, refined_plan)
            plan = refined_plan
            save_json_debug("07_ranked_round2.json", ranked[:150])
            save_json_debug("08_feedback_round2.json", feedback)
            print(f"第二轮检索后总论文数：{len(ranked)}")
        except Exception as exc:
            print(f"\n[Second Round Failed] {exc}")
            print("跳过第二轮检索，使用第一轮结果继续生成报告。")
    else:
        print("\n[6/8] 第一轮结果可接受，不进行第二轮检索。")

    top_papers = ranked[:30]

    print("\n[7/8] 正在生成研究方向聚类和学习路径...")
    clusters = cluster_topics(top_papers)
    learning_path = generate_learning_path(user_query, terms, clusters)
    save_json_debug("09_clusters.json", clusters)
    save_json_debug("10_learning_path.json", learning_path)

    print("\n[8/8] 正在生成 Markdown 报告...")
    report_path = generate_report(user_query, terms, top_papers, clusters, learning_path, plan, feedback)

    print(f"\n报告已生成：{report_path}")
    print("\n## Top Papers")
    for i, paper in enumerate(top_papers[:20], 1):
        print(f"\n### {i}. {paper.get('title')}")
        print("Year:", paper.get("year"))
        print("Citations:", paper.get("citations"))
        print("Source:", paper.get("source"))
        print("Versions:", ", ".join(paper.get("versions", [])))
        print("Status:", paper.get("publication_status"))
        print("Venue:", paper.get("venue"))
        print("Channel:", paper.get("recall_channel"))
        print("Subdomain:", paper.get("matched_subdomain"))
        print("Trends:", ", ".join(paper.get("trend_hits", [])))
        print("Query:", paper.get("matched_query"))
        print("Final Score:", paper.get("final_score"))
        print("URL:", paper.get("url"))


if __name__ == "__main__":
    main()