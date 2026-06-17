import os
import psutil
import socket
import uuid
import json
import base64
import hashlib
import requests
import subprocess
from urllib.parse import urlparse

def get_system_info() -> str:
    """Retrieve host system information (CPU, Memory, Disk, OS)."""
    try:
        cpu_pct = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('C:\\' if os.name == 'nt' else '/')
        os_info = f"{os.name} ({psutil.users()[0].name if psutil.users() else 'Unknown'})"
        
        info = (
            f"OS: {os_info}\n"
            f"CPU Usage: {cpu_pct}%\n"
            f"RAM: Total={mem.total // (1024**2)}MB, Available={mem.available // (1024**2)}MB, Used={mem.percent}%\n"
            f"Disk (System): Total={disk.total // (1024**3)}GB, Free={disk.free // (1024**3)}GB, Used={disk.percent}%"
        )
        return info
    except Exception as e:
        return f"Error getting system info: {str(e)}"

def check_port(host: str, port: int) -> str:
    """Check if a specific TCP port on a host is open/active."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3.0)
    try:
        result = sock.connect_ex((host, port))
        if result == 0:
            return f"Port {port} on {host} is OPEN."
        else:
            return f"Port {port} on {host} is CLOSED (code {result})."
    except Exception as e:
        return f"Error checking port: {str(e)}"
    finally:
        sock.close()

def generate_uuid() -> str:
    """Generate a random UUID v4."""
    return str(uuid.uuid4())

def format_json(json_str: str) -> str:
    """Format and validate a JSON string (pretty print)."""
    try:
        parsed = json.loads(json_str)
        return json.dumps(parsed, indent=2, ensure_ascii=False)
    except json.JSONDecodeError as je:
        return f"Invalid JSON format. Error: {je.msg} at line {je.lineno}, col {je.colno}"
    except Exception as e:
        return f"Error parsing JSON: {str(e)}"

def base64_encode_decode(mode: str, data: str) -> str:
    """Encode or decode base64 strings. mode can be 'encode' or 'decode'."""
    try:
        if mode == 'encode':
            return base64.b64encode(data.encode('utf-8')).decode('utf-8')
        elif mode == 'decode':
            return base64.b64decode(data.encode('utf-8')).decode('utf-8')
        else:
            return "Error: Mode must be 'encode' or 'decode'."
    except Exception as e:
        return f"Error: {str(e)}"

def map_path_to_container(path: str) -> str:
    """Map Windows host path to Docker container path (/app/workspace)."""
    normalized = path.replace("\\", "/")
    import re
    return re.sub(r'^[Cc]:/ameva', '/app/workspace', normalized)

def docker_calculate_file_hash(file_path: str, algorithm: str = "sha256") -> str:
    """Calculate file checksum hash inside a Docker container for isolation."""
    container_path = map_path_to_container(file_path)
    # Check if algorithm is md5 or sha256
    prog = "sha256sum" if algorithm.lower() == "sha256" else "md5sum"
    cmd = [
        "docker", "run", "--rm",
        "-v", r"C:\ameva:/app/workspace",
        "alpine",
        prog, container_path
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=20, stdin=subprocess.DEVNULL)
        if res.returncode != 0:
            return f"Error calculating hash in Docker: {res.stderr.strip()}"
        return res.stdout.strip()
    except Exception as e:
        return f"Exception calculating file hash: {str(e)}"

def get_external_ip() -> str:
    """Retrieve the host's external IP address and internal network IP."""
    internal_ip = "Unknown"
    external_ip = "Unknown"
    try:
        # Get internal IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        internal_ip = s.getsockname()[0]
        s.close()
    except Exception:
        pass
        
    try:
        # Get external IP
        res = requests.get("https://api.ipify.org?format=json", timeout=5)
        if res.status_code == 200:
            external_ip = res.json().get("ip", "Unknown")
    except Exception:
        pass
        
    return f"Internal IP: {internal_ip}\nExternal IP: {external_ip}"

def send_http_request(method: str, url: str, headers_json: str = None, body: str = None) -> str:
    """Send an arbitrary HTTP request (GET/POST/PUT/DELETE) and return status/body."""
    try:
        headers = json.loads(headers_json) if headers_json else {}
        method_upper = method.upper()
        
        res = requests.request(
            method=method_upper,
            url=url,
            headers=headers,
            data=body,
            timeout=15
        )
        
        preview = res.text[:1000] + "\n... (truncated)" if len(res.text) > 1000 else res.text
        return f"Status: {res.status_code} {res.reason}\nHeaders: {dict(res.headers)}\nResponse:\n{preview}"
    except Exception as e:
        return f"HTTP Request Error: {str(e)}"

def docker_find_large_files(dir_path: str, size_mb: int = 50) -> str:
    """Find files larger than size_mb MB inside the directory, running in Docker."""
    container_path = map_path_to_container(dir_path)
    
    # Run find command in Docker
    # size format for find: +50M
    find_arg = f"+{size_mb}M"
    cmd = [
        "docker", "run", "--rm",
        "-v", r"C:\ameva:/app/workspace",
        "alpine",
        "find", container_path, "-type", "f", "-size", find_arg
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30, stdin=subprocess.DEVNULL)
        if res.returncode != 0:
            return f"Error finding large files in Docker: {res.stderr.strip()}"
        out = res.stdout.strip()
        if not out:
            return f"No files larger than {size_mb}MB found in {dir_path}."
        return f"Files larger than {size_mb}MB in {dir_path}:\n{out}"
    except Exception as e:
        return f"Exception finding large files: {str(e)}"

def extract_text_from_url(url: str) -> str:
    """Fetch URL and extract raw body text, stripping all HTML tags."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AMEVA-Agent/1.0"}
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return f"Error: HTTP {res.status_code}"
            
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(res.text, "html.parser")
        
        # remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        clean_text = "\n".join(chunk for chunk in chunks if chunk)
        
        return clean_text[:3000] + "\n... (truncated to 3000 chars)" if len(clean_text) > 3000 else clean_text
    except Exception as e:
        return f"Error extracting text: {str(e)}"
