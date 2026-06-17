import os
import psutil
import socket
import uuid
import json
import base64
import hashlib
import requests
import subprocess
import platform
import threading
import time
import re
from datetime import datetime
from urllib.parse import urlparse


# ──────────────────────────────────────────────
# 기존 유틸리티 (유지)
# ──────────────────────────────────────────────

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
    return re.sub(r'^[Cc]:/ameva', '/app/workspace', normalized)

def docker_calculate_file_hash(file_path: str, algorithm: str = "sha256") -> str:
    """Calculate file checksum hash inside a Docker container for isolation."""
    container_path = map_path_to_container(file_path)
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
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        internal_ip = s.getsockname()[0]
        s.close()
    except Exception:
        pass
        
    try:
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
        from bs4 import BeautifulSoup
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AMEVA-Agent/1.0"}
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return f"Error: HTTP {res.status_code}"
            
        soup = BeautifulSoup(res.text, "html.parser")
        for script in soup(["script", "style"]):
            script.decompose()
            
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = "\n".join(chunk for chunk in chunks if chunk)
        
        return clean_text[:3000] + "\n... (truncated to 3000 chars)" if len(clean_text) > 3000 else clean_text
    except Exception as e:
        return f"Error extracting text: {str(e)}"


# ──────────────────────────────────────────────
# 신규 유틸리티 (고도화 추가)
# ──────────────────────────────────────────────

def gpu_monitor() -> str:
    """
    nvidia-smi를 통해 실시간 GPU 상태를 조회한다.
    GPU명, 사용률, VRAM 점유율, 온도, 전력을 표 형식으로 반환.
    """
    try:
        # nvidia-smi query
        query_fields = (
            "index,name,utilization.gpu,memory.used,memory.total,"
            "temperature.gpu,power.draw,power.limit,driver_version"
        )
        cmd = [
            "nvidia-smi",
            f"--query-gpu={query_fields}",
            "--format=csv,noheader,nounits"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=10, stdin=subprocess.DEVNULL)
        
        if res.returncode != 0:
            # GPU가 없거나 nvidia-smi 미설치 — 대안으로 wmic 시도 (Windows)
            if os.name == "nt":
                wmic_cmd = ["wmic", "path", "Win32_VideoController", "get",
                           "Name,AdapterRAM,VideoMemoryType", "/format:list"]
                wmic = subprocess.run(wmic_cmd, capture_output=True, text=True, timeout=10, stdin=subprocess.DEVNULL)
                if wmic.returncode == 0:
                    return f"nvidia-smi not available. GPU info via WMI:\n{wmic.stdout.strip()}"
            return f"GPU monitor unavailable: {res.stderr.strip() or 'nvidia-smi not found'}"
        
        lines = [l.strip() for l in res.stdout.strip().split("\n") if l.strip()]
        if not lines:
            return "No GPU devices detected."
        
        report = "## 🖥️ GPU Monitor\n\n"
        report += "| # | GPU | Util% | VRAM Used | VRAM Total | Temp°C | Power | Driver |\n"
        report += "| :- | :-- | :---: | :-------: | :--------: | :----: | :---- | :----- |\n"
        
        for line in lines:
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 9:
                idx, name, util, vram_used, vram_total, temp, pwr_draw, pwr_limit, drv = parts[:9]
                vram_pct = round(int(vram_used) / int(vram_total) * 100, 1) if vram_total.isdigit() else "?"
                report += (
                    f"| {idx} | {name} | {util}% | {vram_used}MB ({vram_pct}%) | "
                    f"{vram_total}MB | {temp}°C | {pwr_draw}W / {pwr_limit}W | {drv} |\n"
                )
        
        return report

    except FileNotFoundError:
        return "Error: nvidia-smi is not installed or not in PATH."
    except Exception as e:
        return f"Error in gpu_monitor: {str(e)}"


def system_thermal_scanner() -> str:
    """
    CPU 온도, 클럭, 코어별 사용률을 스캔한다.
    Windows: WMI, Linux/Mac: psutil sensors 활용.
    """
    try:
        report = "## 🌡️ System Thermal & Clock Scanner\n\n"
        
        # CPU 기본 정보
        cpu_freq = psutil.cpu_freq()
        cpu_pct_per_core = psutil.cpu_percent(interval=0.5, percpu=True)
        cpu_count_logical = psutil.cpu_count(logical=True)
        cpu_count_physical = psutil.cpu_count(logical=False)

        report += f"**CPU Cores**: Physical={cpu_count_physical}, Logical={cpu_count_logical}\n"
        if cpu_freq:
            report += (
                f"**Clock**: Current={cpu_freq.current:.0f}MHz, "
                f"Min={cpu_freq.min:.0f}MHz, Max={cpu_freq.max:.0f}MHz\n\n"
            )

        # 코어별 사용률 테이블
        report += "### Core Usage\n"
        report += "| Core | Usage% |\n| :--- | :----: |\n"
        for i, pct in enumerate(cpu_pct_per_core):
            bar = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
            report += f"| Core {i} | {bar} {pct:.1f}% |\n"

        # 온도 센서 (Linux/Mac)
        if hasattr(psutil, "sensors_temperatures"):
            temps = psutil.sensors_temperatures()
            if temps:
                report += "\n### Temperature Sensors\n"
                report += "| Sensor | Label | Current°C | High°C | Critical°C |\n"
                report += "| :----- | :---- | :-------: | :----: | :--------: |\n"
                for name, entries in temps.items():
                    for entry in entries:
                        report += (
                            f"| {name} | {entry.label or '-'} | "
                            f"{entry.current:.1f} | "
                            f"{entry.high or '-'} | "
                            f"{entry.critical or '-'} |\n"
                        )
            else:
                report += "\n*Temperature sensors not accessible on this system.*\n"
        else:
            # Windows — WMI 시도
            if os.name == "nt":
                try:
                    wmi_cmd = (
                        'powershell -Command "Get-WmiObject MSAcpi_ThermalZoneTemperature '
                        '-Namespace root/wmi | Select-Object CurrentTemperature | '
                        'ForEach-Object { ($_.CurrentTemperature / 10 - 273.15).ToString(\'F1\') }"'
                    )
                    wmi_res = subprocess.run(wmi_cmd, shell=True, capture_output=True, text=True, timeout=10)
                    if wmi_res.returncode == 0 and wmi_res.stdout.strip():
                        report += f"\n**CPU Temperature (WMI)**: {wmi_res.stdout.strip()}°C\n"
                    else:
                        report += "\n*WMI thermal sensor not accessible (admin required).*\n"
                except Exception:
                    report += "\n*Temperature data unavailable on Windows without admin.*\n"

        return report

    except Exception as e:
        return f"Error in system_thermal_scanner: {str(e)}"


def process_watchdog(action: str, process_name: str = None) -> str:
    """
    활성 프로세스 목록 스캔, 특정 프로세스 감시, 강제 종료를 수행한다.
    action: 'list' | 'find' | 'kill' | 'restart'
    process_name: 대상 프로세스명 (find/kill/restart 시 필요)
    """
    try:
        if action == "list":
            procs = []
            for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_info", "status"]):
                try:
                    info = proc.info
                    mem_mb = info["memory_info"].rss // (1024 * 1024) if info["memory_info"] else 0
                    procs.append((info["pid"], info["name"], info["cpu_percent"], mem_mb, info["status"]))
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            # CPU 사용률 기준 내림차순 정렬
            procs.sort(key=lambda x: x[2], reverse=True)
            
            report = "## ⚙️ Active Process Watchdog\n\n"
            report += f"**Total Processes**: {len(procs)}\n\n"
            report += "| PID | Name | CPU% | Mem(MB) | Status |\n"
            report += "| :-- | :--- | :--: | :-----: | :----- |\n"
            for pid, name, cpu, mem, status in procs[:30]:
                report += f"| {pid} | {name} | {cpu:.1f} | {mem} | {status} |\n"
            if len(procs) > 30:
                report += f"\n*... and {len(procs) - 30} more processes*\n"
            return report

        elif action == "find":
            if not process_name:
                return "Error: process_name is required for 'find' action."
            
            found = []
            for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_info", "status", "cmdline"]):
                try:
                    if process_name.lower() in proc.info["name"].lower():
                        mem_mb = proc.info["memory_info"].rss // (1024 * 1024) if proc.info["memory_info"] else 0
                        cmdline = " ".join(proc.info["cmdline"] or [])[:80]
                        found.append(f"PID={proc.info['pid']}, Name={proc.info['name']}, "
                                     f"CPU={proc.info['cpu_percent']:.1f}%, Mem={mem_mb}MB, "
                                     f"Status={proc.info['status']}\nCMD: {cmdline}")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if not found:
                return f"No process matching '{process_name}' found."
            return f"### Found {len(found)} process(es) matching '{process_name}':\n\n" + "\n---\n".join(found)

        elif action == "kill":
            if not process_name:
                return "Error: process_name is required for 'kill' action."
            
            killed = []
            for proc in psutil.process_iter(["pid", "name"]):
                try:
                    if process_name.lower() in proc.info["name"].lower():
                        proc.terminate()
                        killed.append(f"PID={proc.info['pid']}, Name={proc.info['name']}")
                except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                    killed.append(f"Failed to kill PID={proc.info.get('pid','?')}: {e}")
            
            if not killed:
                return f"No process matching '{process_name}' found to kill."
            return f"### Terminated {len(killed)} process(es):\n" + "\n".join(killed)

        else:
            return f"Error: Unknown action '{action}'. Use 'list', 'find', or 'kill'."

    except Exception as e:
        return f"Error in process_watchdog: {str(e)}"


def task_cron_scheduler(action: str, job_name: str = None, cron_expression: str = None, command: str = None) -> str:
    """
    Windows Task Scheduler 또는 cron 작업을 관리한다.
    action: 'list' | 'create' | 'delete' | 'run'
    Windows 환경에서는 schtasks 커맨드를 래핑한다.
    """
    try:
        if os.name != "nt":
            # Linux/Mac: crontab 기반
            if action == "list":
                res = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=10)
                if res.returncode != 0:
                    return "No crontab found for current user."
                return f"### Current Crontab:\n```\n{res.stdout.strip()}\n```"
            elif action == "create":
                if not job_name or not cron_expression or not command:
                    return "Error: job_name, cron_expression, and command are all required for 'create'."
                # 기존 crontab 읽기 후 추가
                existing = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
                existing_content = existing.stdout if existing.returncode == 0 else ""
                new_line = f"{cron_expression} {command} # AMEVA:{job_name}\n"
                new_content = existing_content + new_line
                proc = subprocess.run(["crontab", "-"], input=new_content, text=True, timeout=10)
                if proc.returncode == 0:
                    return f"Cron job '{job_name}' created: `{cron_expression} {command}`"
                return f"Error creating cron job: {proc.stderr}"
            elif action == "delete":
                if not job_name:
                    return "Error: job_name is required for 'delete'."
                existing = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
                if existing.returncode != 0:
                    return "No crontab to delete from."
                lines = [l for l in existing.stdout.splitlines() if f"# AMEVA:{job_name}" not in l]
                subprocess.run(["crontab", "-"], input="\n".join(lines) + "\n", text=True, timeout=10)
                return f"Cron job '{job_name}' deleted."
            else:
                return f"Unknown action '{action}' for cron."

        # Windows: schtasks
        if action == "list":
            res = subprocess.run(
                ["schtasks", "/query", "/fo", "TABLE", "/nh"],
                capture_output=True, text=True, timeout=15, stdin=subprocess.DEVNULL
            )
            if res.returncode != 0:
                return f"Error listing tasks: {res.stderr.strip()}"
            lines = res.stdout.strip().splitlines()
            report = f"### Scheduled Tasks ({len(lines)} found)\n```\n"
            report += "\n".join(lines[:50])
            if len(lines) > 50:
                report += f"\n... ({len(lines)-50} more)"
            report += "\n```"
            return report

        elif action == "create":
            if not job_name or not command:
                return "Error: job_name and command are required for 'create'."
            # cron_expression을 Windows 스케줄로 간단 변환 (분 단위)
            trigger = "/SC MINUTE /MO 60"  # 기본: 1시간마다
            if cron_expression:
                parts = cron_expression.split()
                if len(parts) >= 2 and parts[0] == "*" and parts[1] == "*":
                    trigger = "/SC MINUTE /MO 1"
                elif len(parts) >= 2 and parts[1].isdigit():
                    trigger = f"/SC DAILY /ST {int(parts[1]):02d}:00"
            
            cmd_str = (
                f'schtasks /create /tn "AMEVA\\{job_name}" /tr "{command}" '
                f'{trigger} /f'
            )
            res = subprocess.run(cmd_str, shell=True, capture_output=True, text=True, timeout=15)
            if res.returncode == 0:
                return f"Task '{job_name}' created successfully."
            return f"Error creating task: {res.stderr.strip()}"

        elif action == "delete":
            if not job_name:
                return "Error: job_name is required for 'delete'."
            res = subprocess.run(
                ["schtasks", "/delete", "/tn", f"AMEVA\\{job_name}", "/f"],
                capture_output=True, text=True, timeout=10, stdin=subprocess.DEVNULL
            )
            if res.returncode == 0:
                return f"Task '{job_name}' deleted."
            return f"Error deleting task: {res.stderr.strip()}"

        elif action == "run":
            if not job_name:
                return "Error: job_name is required for 'run'."
            res = subprocess.run(
                ["schtasks", "/run", "/tn", f"AMEVA\\{job_name}"],
                capture_output=True, text=True, timeout=10, stdin=subprocess.DEVNULL
            )
            if res.returncode == 0:
                return f"Task '{job_name}' triggered manually."
            return f"Error running task: {res.stderr.strip()}"

        else:
            return f"Error: Unknown action '{action}'. Use 'list', 'create', 'delete', or 'run'."

    except Exception as e:
        return f"Error in task_cron_scheduler: {str(e)}"


def rest_client_simulator(method: str, url: str, payload_json: str = None, headers_json: str = None) -> str:
    """
    REST API 모의 요청 클라이언트. curl 없이 REST API를 테스트한다.
    응답을 보기 좋은 포맷으로 반환하며 curl 등가 명령어도 출력한다.
    """
    try:
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            return f"Error: Invalid URL '{url}'"

        headers = json.loads(headers_json) if headers_json else {}
        payload = None
        if payload_json:
            try:
                payload = json.loads(payload_json)
                if "Content-Type" not in headers:
                    headers["Content-Type"] = "application/json"
            except json.JSONDecodeError:
                payload = payload_json  # raw string

        method_upper = method.upper()

        # curl 등가 명령어 생성
        curl_headers = " ".join([f'-H "{k}: {v}"' for k, v in headers.items()])
        curl_body = f"-d '{payload_json}'" if payload_json else ""
        curl_equiv = f"curl -X {method_upper} {curl_headers} {curl_body} \"{url}\""

        # 요청 실행
        start = time.time()
        if isinstance(payload, dict):
            res = requests.request(method_upper, url, headers=headers, json=payload, timeout=15)
        else:
            res = requests.request(method_upper, url, headers=headers, data=payload, timeout=15)
        elapsed_ms = round((time.time() - start) * 1000, 1)

        # 응답 파싱
        content_type = res.headers.get("Content-Type", "")
        try:
            if "json" in content_type:
                body_parsed = json.dumps(res.json(), indent=2, ensure_ascii=False)
            else:
                body_parsed = res.text[:2000]
        except Exception:
            body_parsed = res.text[:2000]

        report = (
            f"## 🌐 REST Client Simulator\n\n"
            f"**Request**: `{method_upper} {url}`  \n"
            f"**Status**: `{res.status_code} {res.reason}`  \n"
            f"**Response Time**: `{elapsed_ms}ms`  \n"
            f"**Content-Type**: `{content_type}`  \n\n"
            f"### Response Headers\n```\n"
        )
        for k, v in dict(res.headers).items():
            report += f"{k}: {v}\n"
        report += f"```\n\n### Response Body\n```json\n{body_parsed}\n```\n\n"
        report += f"### curl Equivalent\n```bash\n{curl_equiv}\n```\n"

        return report

    except requests.exceptions.Timeout:
        return f"Error: Request to {url} timed out after 15 seconds."
    except requests.exceptions.ConnectionError as e:
        return f"Error: Could not connect to {url}. {str(e)}"
    except Exception as e:
        return f"Error in rest_client_simulator: {str(e)}"


def html_to_pdf_renderer(html_path_or_url: str, output_pdf_path: str) -> str:
    """
    HTML 파일 또는 URL을 PDF로 변환한다.
    우선순위: weasyprint → pdfkit(wkhtmltopdf) → 불가 시 안내 메시지.
    출력 경로는 C:\\ameva 하위만 허용.
    """
    # 출력 경로 보안 검사
    out_norm = os.path.abspath(output_pdf_path)
    if not out_norm.lower().startswith(r"c:\ameva"):
        return f"Security Error: Output path must be under C:\\ameva. Got: {out_norm}"

    os.makedirs(os.path.dirname(out_norm), exist_ok=True) if os.path.dirname(out_norm) else None

    # 입력 소스 결정
    is_url = html_path_or_url.startswith("http://") or html_path_or_url.startswith("https://")
    if not is_url:
        src_norm = os.path.abspath(html_path_or_url)
        if not src_norm.lower().startswith(r"c:\ameva"):
            return f"Security Error: Source path must be under C:\\ameva. Got: {src_norm}"
        if not os.path.exists(src_norm):
            return f"Error: HTML file not found at {src_norm}"
        source = f"file:///{src_norm.replace(chr(92), '/')}"
    else:
        source = html_path_or_url

    # 방법 1: weasyprint
    try:
        import weasyprint
        if is_url:
            weasyprint.HTML(url=source).write_pdf(out_norm)
        else:
            weasyprint.HTML(filename=os.path.abspath(html_path_or_url)).write_pdf(out_norm)
        size_kb = os.path.getsize(out_norm) // 1024
        return f"✅ PDF rendered via WeasyPrint.\nOutput: {out_norm} ({size_kb}KB)"
    except ImportError:
        pass
    except Exception as e:
        pass

    # 방법 2: pdfkit (wkhtmltopdf wrapper)
    try:
        import pdfkit
        pdfkit.from_url(source, out_norm)
        size_kb = os.path.getsize(out_norm) // 1024
        return f"✅ PDF rendered via pdfkit (wkhtmltopdf).\nOutput: {out_norm} ({size_kb}KB)"
    except ImportError:
        pass
    except Exception as e:
        pass

    # 방법 3: Windows — Edge/Chrome CLI headless
    if os.name == "nt":
        edge_paths = [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        ]
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
        for browser_path in edge_paths + chrome_paths:
            if os.path.exists(browser_path):
                try:
                    cmd = [
                        browser_path,
                        "--headless",
                        "--disable-gpu",
                        f"--print-to-pdf={out_norm}",
                        source
                    ]
                    res = subprocess.run(cmd, capture_output=True, timeout=30, stdin=subprocess.DEVNULL)
                    if os.path.exists(out_norm) and os.path.getsize(out_norm) > 0:
                        size_kb = os.path.getsize(out_norm) // 1024
                        return f"✅ PDF rendered via {os.path.basename(browser_path)} headless.\nOutput: {out_norm} ({size_kb}KB)"
                except Exception:
                    continue

    return (
        "⚠️ HTML to PDF conversion failed. No compatible renderer found.\n"
        "Install one of the following:\n"
        "  pip install weasyprint\n"
        "  pip install pdfkit  (requires wkhtmltopdf binary)\n"
        "  Or ensure Microsoft Edge / Google Chrome is installed."
    )
