import os
import subprocess
import json


def docker_container_manager(action: str, container_name: str = None, limit_lines: int = 50) -> str:
    """
    로컬 Docker 컨테이너를 관리한다.
    action: 'list' | 'start' | 'stop' | 'restart' | 'logs' | 'inspect' | 'stats'
    container_name: 대상 컨테이너 이름 또는 ID (list/stats 제외)
    limit_lines: logs 출력 줄 제한 (기본 50)
    """
    def _run_docker(*args, timeout=15):
        cmd = ["docker"] + list(args)
        try:
            res = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                stdin=subprocess.DEVNULL
            )
            return res.returncode, res.stdout.strip(), res.stderr.strip()
        except FileNotFoundError:
            return -1, "", "Docker is not installed or not in PATH."
        except subprocess.TimeoutExpired:
            return -1, "", f"Docker command timed out after {timeout}s."
        except Exception as e:
            return -1, "", str(e)

    if action == "list":
        code, out, err = _run_docker("ps", "-a", "--format",
                                     "table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}")
        if code != 0:
            return f"Error listing containers: {err}"
        if not out:
            return "No Docker containers found."
        lines = out.splitlines()
        report = "## 🐳 Docker Container List\n\n"
        report += "| Container ID | Name | Image | Status | Ports |\n"
        report += "| :----------- | :--- | :---- | :----- | :---- |\n"
        for line in lines[1:]:  # skip header
            parts = line.split("\t")
            if len(parts) >= 5:
                cid, name, image, status, ports = parts[0], parts[1], parts[2], parts[3], parts[4]
                status_icon = "🟢" if "Up" in status else "🔴"
                report += f"| `{cid[:12]}` | `{name}` | `{image}` | {status_icon} {status} | {ports or '-'} |\n"
        return report

    elif action == "stats":
        code, out, err = _run_docker("stats", "--no-stream", "--format",
                                     "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}")
        if code != 0:
            return f"Error getting stats: {err}"
        if not out:
            return "No running containers to show stats for."
        lines = out.splitlines()
        report = "## 📊 Docker Container Stats (Live Snapshot)\n\n"
        report += "| Name | CPU% | Mem Usage | Mem% | Net I/O | Block I/O |\n"
        report += "| :--- | :--: | :-------- | :--: | :------ | :-------- |\n"
        for line in lines[1:]:
            parts = line.split("\t")
            if len(parts) >= 6:
                report += f"| `{parts[0]}` | {parts[1]} | {parts[2]} | {parts[3]} | {parts[4]} | {parts[5]} |\n"
        return report

    elif action == "start":
        if not container_name:
            return "Error: container_name is required for 'start'."
        code, out, err = _run_docker("start", container_name)
        if code != 0:
            return f"Error starting '{container_name}': {err}"
        return f"✅ Container '{container_name}' started successfully."

    elif action == "stop":
        if not container_name:
            return "Error: container_name is required for 'stop'."
        code, out, err = _run_docker("stop", container_name)
        if code != 0:
            return f"Error stopping '{container_name}': {err}"
        return f"🛑 Container '{container_name}' stopped successfully."

    elif action == "restart":
        if not container_name:
            return "Error: container_name is required for 'restart'."
        code, out, err = _run_docker("restart", container_name)
        if code != 0:
            return f"Error restarting '{container_name}': {err}"
        return f"🔄 Container '{container_name}' restarted successfully."

    elif action == "logs":
        if not container_name:
            return "Error: container_name is required for 'logs'."
        code, out, err = _run_docker("logs", "--tail", str(limit_lines), "--timestamps", container_name, timeout=20)
        if code != 0:
            # Docker logs outputs to stderr normally — check combined
            combined = out or err
            if not combined:
                return f"Error getting logs for '{container_name}': {err}"
        # Docker logs typically writes to stderr
        combined = (out + "\n" + err).strip()
        lines = combined.splitlines()[-limit_lines:]
        return (
            f"## 📋 Logs: `{container_name}` (last {limit_lines} lines)\n\n"
            f"```\n{chr(10).join(lines)}\n```"
        )

    elif action == "inspect":
        if not container_name:
            return "Error: container_name is required for 'inspect'."
        code, out, err = _run_docker("inspect", container_name)
        if code != 0:
            return f"Error inspecting '{container_name}': {err}"
        try:
            data = json.loads(out)
            if data:
                info = data[0]
                report = f"## 🔍 Container Inspect: `{container_name}`\n\n"
                report += f"**ID**: `{info.get('Id', '?')[:12]}`  \n"
                report += f"**Name**: `{info.get('Name', '?')}`  \n"
                report += f"**Image**: `{info.get('Config', {}).get('Image', '?')}`  \n"
                report += f"**Status**: `{info.get('State', {}).get('Status', '?')}`  \n"
                report += f"**Started At**: `{info.get('State', {}).get('StartedAt', '?')}`  \n"
                report += f"**RestartCount**: `{info.get('RestartCount', 0)}`  \n"
                
                # 네트워크
                networks = info.get("NetworkSettings", {}).get("Networks", {})
                if networks:
                    report += "\n### Networks\n"
                    for net_name, net_info in networks.items():
                        report += f"- `{net_name}`: IP=`{net_info.get('IPAddress', '-')}`\n"
                
                # 마운트
                mounts = info.get("Mounts", [])
                if mounts:
                    report += "\n### Mounts\n"
                    for m in mounts:
                        report += f"- `{m.get('Source', '?')}` → `{m.get('Destination', '?')}` ({m.get('Mode', 'rw')})\n"
                
                return report
        except Exception:
            return f"Inspect output:\n```json\n{out[:2000]}\n```"

    else:
        return f"Error: Unknown action '{action}'. Use: list | start | stop | restart | logs | inspect | stats"
