import os
import subprocess
import re
import math
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup


def web_readability_cleaner(url: str) -> str:
    """
    웹 페이지에서 광고, 네비게이션, 사이드바 등을 제거하고
    본문 콘텐츠만 추출해 깔끔한 마크다운으로 변환한다.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AMEVA-Reader/1.0"
        }
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return f"Error: HTTP {res.status_code} {res.reason}"

        soup = BeautifulSoup(res.text, "html.parser")

        # 노이즈 태그 제거 (광고, 네비, 푸터, 사이드바, 스크립트 등)
        noise_tags = [
            "script", "style", "noscript", "header", "footer", "nav",
            "aside", "form", "iframe", "button", "svg", "img",
            "figure", "figcaption", "advertisement", "ads", "banner"
        ]
        noise_classes = [
            "nav", "navigation", "sidebar", "menu", "footer", "header",
            "ad", "advertisement", "banner", "cookie", "popup", "modal",
            "social", "share", "comment", "related", "breadcrumb"
        ]

        for tag in soup(noise_tags):
            tag.decompose()

        # 클래스 기반 노이즈 제거
        for cls in noise_classes:
            for el in soup.find_all(class_=re.compile(cls, re.IGNORECASE)):
                el.decompose()

        # 본문 후보 탐색 (article > main > body 순)
        content_el = (
            soup.find("article") or
            soup.find("main") or
            soup.find(id=re.compile(r"(content|main|article|post)", re.IGNORECASE)) or
            soup.find(class_=re.compile(r"(content|main|article|post)", re.IGNORECASE)) or
            soup.body
        )

        if not content_el:
            return "Error: Could not extract readable content from this page."

        # HTML → Markdown 변환
        markdown_lines = []
        title_tag = soup.title
        if title_tag:
            markdown_lines.append(f"# {title_tag.string.strip()}\n")
            markdown_lines.append(f"> Source: {url}\n")
            markdown_lines.append("---\n")

        for el in content_el.descendants:
            if not hasattr(el, "name"):
                continue
            if el.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                level = int(el.name[1])
                text = el.get_text(strip=True)
                if text:
                    markdown_lines.append(f"\n{'#' * level} {text}\n")
            elif el.name == "p":
                text = el.get_text(strip=True)
                if text and len(text) > 20:
                    markdown_lines.append(f"\n{text}\n")
            elif el.name in ["ul", "ol"]:
                for li in el.find_all("li", recursive=False):
                    text = li.get_text(strip=True)
                    if text:
                        markdown_lines.append(f"- {text}")
            elif el.name == "pre":
                code = el.get_text()
                markdown_lines.append(f"\n```\n{code.strip()}\n```\n")
            elif el.name == "blockquote":
                text = el.get_text(strip=True)
                if text:
                    markdown_lines.append(f"\n> {text}\n")

        result = "\n".join(markdown_lines)
        result = re.sub(r"\n{3,}", "\n\n", result)

        if len(result) > 5000:
            return result[:5000] + "\n\n... (truncated to 5000 chars)"
        return result if result.strip() else "No readable content found."

    except Exception as e:
        return f"Error in web_readability_cleaner: {str(e)}"


def dead_link_scanner(md_file_path: str) -> str:
    """
    마크다운 파일 내의 모든 URL 링크를 추출하고 
    HTTP HEAD 요청으로 응답 상태를 전수 검사한다 (404 데드링크 식별).
    """
    # 경로 보안 검사
    normalized = os.path.abspath(md_file_path)
    if not normalized.lower().startswith(r"c:\ameva"):
        return f"Security Error: Access to path '{normalized}' is denied."

    if not os.path.exists(normalized):
        return f"Error: File not found at {md_file_path}"

    try:
        with open(normalized, "r", encoding="utf-8") as f:
            content = f.read()

        # 마크다운 링크 패턴: [text](url) 및 bare URL
        url_pattern = re.compile(
            r"\[.*?\]\((https?://[^\s\)]+)\)|"
            r"(?<!\()(https?://[^\s\)>\]\"\',]+)"
        )
        found_urls = list(set(url_pattern.findall(content)))
        # findall은 그룹 튜플 반환 — flatten
        flat_urls = []
        for match in found_urls:
            if isinstance(match, tuple):
                flat_urls.extend([m for m in match if m])
            else:
                flat_urls.append(match)
        flat_urls = list(set(flat_urls))

        if not flat_urls:
            return f"No URLs found in {md_file_path}."

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AMEVA-LinkChecker/1.0"
        }

        results = {"alive": [], "dead": [], "error": []}

        for url in flat_urls:
            try:
                r = requests.head(url, headers=headers, timeout=8, allow_redirects=True)
                if r.status_code < 400:
                    results["alive"].append({"url": url, "status": r.status_code})
                else:
                    results["dead"].append({"url": url, "status": r.status_code})
            except requests.exceptions.ConnectionError:
                results["dead"].append({"url": url, "status": "CONNECTION_ERROR"})
            except requests.exceptions.Timeout:
                results["error"].append({"url": url, "status": "TIMEOUT"})
            except Exception as ex:
                results["error"].append({"url": url, "status": str(ex)[:50]})

        total = len(flat_urls)
        report = (
            f"## 🔗 Dead Link Scanner Report\n"
            f"**File**: `{md_file_path}`  \n"
            f"**Total URLs scanned**: {total}  \n"
            f"**✅ Alive**: {len(results['alive'])}  \n"
            f"**❌ Dead**: {len(results['dead'])}  \n"
            f"**⚠️ Error**: {len(results['error'])}\n\n"
        )

        if results["dead"]:
            report += "### ❌ Dead Links\n"
            report += "| URL | Status |\n| :--- | :--- |\n"
            for item in results["dead"]:
                report += f"| `{item['url']}` | `{item['status']}` |\n"
            report += "\n"

        if results["error"]:
            report += "### ⚠️ Error Links\n"
            report += "| URL | Reason |\n| :--- | :--- |\n"
            for item in results["error"]:
                report += f"| `{item['url']}` | `{item['status']}` |\n"
            report += "\n"

        if results["alive"]:
            report += "### ✅ Alive Links\n"
            report += "| URL | Status |\n| :--- | :--- |\n"
            for item in results["alive"][:20]:  # 최대 20개 표시
                report += f"| `{item['url']}` | `{item['status']}` |\n"
            if len(results["alive"]) > 20:
                report += f"| ... | ({len(results['alive']) - 20} more) |\n"

        return report

    except Exception as e:
        return f"Error in dead_link_scanner: {str(e)}"


def crawl_website(url: str, selector: str = None) -> str:
    """
    Crawls a website URL, extracts the Title, Metadata, clean Text content, 
    and lists all unique internal & external links.
    Optionally filters by a CSS selector.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AMEVA-Crawler/1.0"
        }
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return f"Error crawling {url}: HTTP {res.status_code} {res.reason}"
            
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 1. Metadata
        title = soup.title.string.strip() if soup.title else "No Title"
        meta_desc = ""
        desc_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
        if desc_tag:
            meta_desc = desc_tag.get("content", "").strip()
            
        # 2. Main Content (filter by selector if provided)
        content_soup = soup
        if selector:
            selected = soup.select(selector)
            if selected:
                content_soup = BeautifulSoup("".join(str(s) for s in selected), 'html.parser')
                
        # Strip script/style
        for tag in content_soup(["script", "style", "meta", "noscript", "header", "footer"]):
            tag.decompose()
            
        raw_text = content_soup.get_text()
        lines = (line.strip() for line in raw_text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = "\n".join(chunk for chunk in chunks if chunk)
        
        # 3. Links analysis
        parsed_base = urlparse(url)
        base_domain = parsed_base.netloc
        
        internal_links = set()
        external_links = set()
        
        for link in soup.find_all("a", href=True):
            href = link.get("href").strip()
            if not href or href.startswith("#") or href.startswith("javascript:"):
                continue
            full_url = urljoin(url, href)
            parsed_link = urlparse(full_url)
            
            if parsed_link.netloc == base_domain:
                internal_links.add(full_url)
            else:
                external_links.add(full_url)
                
        # Format the output
        summary = (
            f"=== CRAWL REPORT FOR: {url} ===\n"
            f"Title: {title}\n"
            f"Meta Description: {meta_desc}\n\n"
            f"--- CLEAN TEXT CONTENT (Preview) ---\n"
            f"{clean_text[:1200]}\n"
            f"... (Truncated, total length: {len(clean_text)} chars)\n\n"
            f"--- LINKS ANALYSIS ---\n"
            f"Internal Links found: {len(internal_links)}\n"
            f"External Links found: {len(external_links)}\n"
        )
        
        if internal_links:
            summary += "\nInternal Links sample (max 5):\n" + "\n".join(list(internal_links)[:5])
        if external_links:
            summary += "\nExternal Links sample (max 5):\n" + "\n".join(list(external_links)[:5])
            
        return summary
    except Exception as e:
        return f"Exception while crawling {url}: {str(e)}"
