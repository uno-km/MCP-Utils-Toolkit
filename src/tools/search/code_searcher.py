import os
import re
import math
from collections import defaultdict


AMEVA_BASE = r"C:\ameva"


def _tf_idf_search(query: str, corpus: list[dict], top_k: int = 10) -> list[dict]:
    """
    TF-IDF / BM25 기반 텍스트 검색. 
    corpus: [{"path": str, "text": str, "lines": [(lineno, line)]}]
    """
    # 토크나이징
    def tokenize(text: str) -> list[str]:
        return re.findall(r"[a-zA-Z_]\w*", text.lower())

    query_tokens = set(tokenize(query))
    if not query_tokens:
        return []

    N = len(corpus)
    # IDF 계산
    df = defaultdict(int)
    for doc in corpus:
        doc_tokens = set(tokenize(doc["text"]))
        for t in query_tokens:
            if t in doc_tokens:
                df[t] += 1

    idf = {t: math.log((N - df[t] + 0.5) / (df[t] + 0.5) + 1) for t in query_tokens}

    # BM25 파라미터
    k1 = 1.5
    b = 0.75
    avg_dl = sum(len(tokenize(d["text"])) for d in corpus) / max(N, 1)

    scores = []
    for doc in corpus:
        doc_tokens = tokenize(doc["text"])
        dl = len(doc_tokens)
        tf_map = defaultdict(int)
        for t in doc_tokens:
            tf_map[t] += 1

        score = 0.0
        for t in query_tokens:
            if t in tf_map:
                tf = tf_map[t]
                numerator = tf * (k1 + 1)
                denominator = tf + k1 * (1 - b + b * dl / max(avg_dl, 1))
                score += idf.get(t, 0) * (numerator / denominator)

        if score > 0:
            scores.append((score, doc))

    scores.sort(key=lambda x: -x[0])
    return [doc for _, doc in scores[:top_k]]


def vector_code_searcher(
    query: str,
    file_ext: str = ".py",
    search_root: str = None,
    top_k: int = 10,
    context_lines: int = 3
) -> str:
    """
    AMEVA 프로젝트 소스코드 전역을 BM25 알고리즘으로 검색하여
    질의어와 가장 유관한 코드 조각과 함수/클래스를 반환한다.
    
    query: 검색어 (자연어 또는 코드 키워드)
    file_ext: 검색할 파일 확장자 (기본: .py, 여러 개: ".py,.js,.ts")
    search_root: 검색 루트 경로 (기본: C:\\ameva)
    top_k: 반환할 최대 파일 수
    context_lines: 매칭 라인 주변 컨텍스트 줄 수
    """
    if not query or not query.strip():
        return "Error: query cannot be empty."

    base = search_root or AMEVA_BASE
    base_norm = os.path.abspath(base)
    if not base_norm.lower().startswith(r"c:\ameva"):
        return f"Security Error: search_root must be under C:\\ameva. Got: {base_norm}"

    # 확장자 파싱
    extensions = [e.strip().lower() for e in file_ext.split(",")]
    if not all(e.startswith(".") for e in extensions):
        return f"Error: file_ext must start with '.' (e.g., '.py' or '.py,.js')"

    # 파일 수집
    corpus = []
    file_count = 0
    for root, dirs, files in os.walk(base_norm):
        # 제외 폴더
        dirs[:] = [d for d in dirs if d not in {
            "__pycache__", ".git", "node_modules", ".venv", "venv",
            "dist", "build", ".mypy_cache", ".pytest_cache"
        }]
        for fname in files:
            if any(fname.lower().endswith(ext) for ext in extensions):
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                    text = "".join(lines)
                    corpus.append({
                        "path": fpath,
                        "text": text,
                        "lines": [(i + 1, l.rstrip()) for i, l in enumerate(lines)]
                    })
                    file_count += 1
                except Exception:
                    continue

    if not corpus:
        return f"No files with extension(s) '{file_ext}' found under {base_norm}."

    # BM25 검색
    results = _tf_idf_search(query, corpus, top_k=top_k)

    if not results:
        return f"No results found for query: '{query}'"

    # 결과 포맷
    report = (
        f"## 🔍 Code Searcher Results\n\n"
        f"**Query**: `{query}`  \n"
        f"**Extension(s)**: `{file_ext}`  \n"
        f"**Files Indexed**: {file_count}  \n"
        f"**Top Results**: {len(results)}\n\n"
    )
    report += "---\n\n"

    query_tokens = set(re.findall(r"[a-zA-Z_]\w*", query.lower()))

    for rank, doc in enumerate(results, 1):
        path = doc["path"]
        rel_path = os.path.relpath(path, AMEVA_BASE)
        all_lines = doc["lines"]

        # 쿼리 토큰과 매칭되는 라인 탐색
        matching_lines = []
        for lineno, line in all_lines:
            line_tokens = set(re.findall(r"[a-zA-Z_]\w*", line.lower()))
            if query_tokens & line_tokens:
                matching_lines.append(lineno)

        report += f"### #{rank} `{rel_path}`\n\n"

        if matching_lines:
            # 첫 번째 매칭 라인 주변 컨텍스트 출력
            for match_lineno in matching_lines[:3]:
                start = max(0, match_lineno - 1 - context_lines)
                end = min(len(all_lines), match_lineno + context_lines)
                snippet_lines = all_lines[start:end]

                report += f"*Line {match_lineno}:*\n```{file_ext.split(',')[0][1:]}\n"
                for lno, ltext in snippet_lines:
                    marker = ">>>" if lno == match_lineno else "   "
                    report += f"{marker} {lno:4d} | {ltext}\n"
                report += "```\n\n"
        else:
            # 파일 상위 표시
            preview_lines = all_lines[:10]
            report += "```\n"
            for lno, ltext in preview_lines:
                report += f"{lno:4d} | {ltext}\n"
            report += "```\n\n"

        report += "---\n\n"

    return report.strip()
