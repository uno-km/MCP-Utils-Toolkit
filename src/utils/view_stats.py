import json
from collections import Counter
from pathlib import Path

AUDIT_LOG_PATH = Path(r"C:\ameva\AMEVA-MCP-Toolkit-Utils\mcp_audit.jsonl")

def print_audit_stats():
    if not AUDIT_LOG_PATH.exists():
        print("Audit log is empty.")
        return

    total = 0
    status_counts = Counter()
    tool_counts = Counter()

    with open(AUDIT_LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            try:
                record = json.loads(line)
                total += 1
                status_counts[record.get("status", "unknown")] += 1
                tool_counts[record.get("tool", "unknown")] += 1
            except json.JSONDecodeError:
                pass

    print("="*40)
    print(" [ AMEVA MCP Audit Log Statistics ] ")
    print("="*40)
    print(f"Total Tool Executions: {total}")
    print("\n[Status Breakdown]")
    for status, count in status_counts.items():
        print(f"  - {status.upper()}: {count} ({count/total*100:.1f}%)")
    
    print("\n[Most Used Tools]")
    for tool, count in tool_counts.most_common():
        print(f"  - {tool}: {count} times")
    print("="*40)

if __name__ == "__main__":
    print_audit_stats()
