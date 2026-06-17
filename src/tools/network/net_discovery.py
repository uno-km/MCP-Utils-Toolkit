import socket
import json
import concurrent.futures
import ipaddress
from datetime import datetime


def _scan_port(host: str, port: int, timeout: float = 0.5) -> tuple[int, bool, str]:
    """단일 포트 스캔 — (port, is_open, banner)"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((host, port))
        is_open = (result == 0)
        banner = ""
        if is_open:
            try:
                sock.settimeout(0.3)
                banner = sock.recv(256).decode("utf-8", errors="ignore").strip()[:60]
            except Exception:
                pass
        return port, is_open, banner
    except Exception:
        return port, False, ""
    finally:
        sock.close()


def _get_service_name(port: int) -> str:
    """알려진 포트 서비스명 반환."""
    WELL_KNOWN = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
        53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
        443: "HTTPS", 465: "SMTPS", 587: "SMTP-TLS",
        1433: "MSSQL", 3306: "MySQL", 3389: "RDP",
        5000: "Flask/Dev", 5432: "PostgreSQL", 5900: "VNC",
        6379: "Redis", 7860: "Gradio", 8000: "FastAPI/Dev",
        8080: "HTTP-Alt", 8443: "HTTPS-Alt", 8501: "Streamlit",
        8888: "Jupyter", 9200: "Elasticsearch", 11434: "Ollama",
        19530: "Milvus", 27017: "MongoDB", 50051: "gRPC",
    }
    try:
        return socket.getservbyport(port) if port not in WELL_KNOWN else WELL_KNOWN[port]
    except Exception:
        return WELL_KNOWN.get(port, "unknown")


def service_discovery(
    subnet: str = "127.0.0.1",
    ports_json: str = "[22, 80, 8000, 8080, 8501]",
    timeout: float = 0.5,
    max_hosts: int = 254
) -> str:
    """
    지정 서브넷 또는 단일 호스트를 스캔하여 활성 서비스 포트를 식별한다.
    AMEVA 노드(Streamlit, FastAPI, Gradio, Ollama 등)의 상태 파악에 최적화.

    subnet: 단일 IP (예: 192.168.0.1) 또는 CIDR (예: 192.168.0.0/24)
    ports_json: 스캔할 포트 목록 JSON (예: [22, 80, 8000, 8080, 8501])
    timeout: 포트당 타임아웃 초 (기본 0.5)
    max_hosts: 서브넷 스캔 시 최대 호스트 수 제한 (기본 254)
    """
    # 포트 파싱
    try:
        ports = json.loads(ports_json)
        if not isinstance(ports, list):
            return "Error: ports_json must be a JSON array (e.g., [22, 80, 8080])"
        ports = [int(p) for p in ports if 0 < int(p) < 65536]
    except Exception as e:
        return f"Error parsing ports_json: {e}"

    if not ports:
        return "Error: No valid ports provided."

    # 호스트 목록 결정
    hosts = []
    try:
        # CIDR 서브넷 여부 확인
        if "/" in subnet:
            network = ipaddress.ip_network(subnet, strict=False)
            host_list = list(network.hosts())
            if len(host_list) > max_hosts:
                return (
                    f"Error: Subnet '{subnet}' has {len(host_list)} hosts. "
                    f"Max allowed: {max_hosts}. Use a smaller range or increase max_hosts."
                )
            hosts = [str(h) for h in host_list]
        else:
            # 단일 호스트
            hosts = [subnet]
    except ValueError as ve:
        return f"Error: Invalid subnet/IP '{subnet}': {ve}"

    if not hosts:
        return f"No hosts to scan in {subnet}."

    start_time = datetime.now()
    results = {}  # host -> [(port, is_open, banner)]

    # 병렬 스캔 (스레드 풀)
    total_tasks = len(hosts) * len(ports)
    MAX_WORKERS = min(100, total_tasks)

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {}
        for host in hosts:
            for port in ports:
                fut = executor.submit(_scan_port, host, port, timeout)
                futures[fut] = host

        for fut in concurrent.futures.as_completed(futures):
            host = futures[fut]
            try:
                port, is_open, banner = fut.result()
                if host not in results:
                    results[host] = []
                results[host].append((port, is_open, banner))
            except Exception:
                pass

    elapsed = (datetime.now() - start_time).total_seconds()

    # 활성 호스트만 필터링
    active_hosts = {h: ports_res for h, ports_res in results.items()
                    if any(is_open for _, is_open, _ in ports_res)}

    # 리포트 작성
    report = (
        f"## 🌐 Network Service Discovery\n\n"
        f"**Target**: `{subnet}`  \n"
        f"**Ports Scanned**: `{ports}`  \n"
        f"**Hosts Scanned**: {len(hosts)}  \n"
        f"**Active Hosts**: {len(active_hosts)}  \n"
        f"**Scan Time**: {elapsed:.2f}s\n\n"
    )

    if not active_hosts:
        report += "🔴 No active hosts with open ports found.\n"
        return report

    report += "---\n\n"
    for host in sorted(active_hosts.keys()):
        open_ports = [(p, b) for p, is_open, b in sorted(active_hosts[host]) if is_open]
        closed_count = len(ports) - len(open_ports)

        # 호스트명 역방향 조회 시도
        try:
            hostname = socket.gethostbyaddr(host)[0]
        except Exception:
            hostname = ""

        report += f"### 🟢 Host: `{host}`"
        if hostname and hostname != host:
            report += f" (`{hostname}`)"
        report += f"\n\n"

        report += "| Port | Service | Status | Banner |\n"
        report += "| :--- | :------ | :----: | :----- |\n"
        for port, banner in open_ports:
            svc = _get_service_name(port)
            report += f"| `{port}` | {svc} | 🟢 OPEN | `{banner or '-'}` |\n"

        # AMEVA 특화 서비스 인식
        ameva_services = []
        open_port_nums = [p for p, _ in open_ports]
        if 8501 in open_port_nums:
            ameva_services.append("📊 Streamlit App")
        if any(p in open_port_nums for p in [8000, 5000]):
            ameva_services.append("⚡ FastAPI/Flask Server")
        if 7860 in open_port_nums:
            ameva_services.append("🎨 Gradio UI")
        if 11434 in open_port_nums:
            ameva_services.append("🤖 Ollama LLM Server")
        if 6379 in open_port_nums:
            ameva_services.append("💾 Redis Cache")
        if 19530 in open_port_nums:
            ameva_services.append("🔢 Milvus Vector DB")

        if ameva_services:
            report += f"\n**Detected AMEVA Services**: {', '.join(ameva_services)}\n"
        report += "\n---\n\n"

    return report.strip()
