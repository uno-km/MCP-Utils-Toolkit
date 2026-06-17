import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

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
                # Merge multiple selected blocks
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
