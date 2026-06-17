import os
import json
import time
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

AUDIT_LOG_PATH = r"C:\ameva\AMEVA-MCP-Toolkit-Utils\mcp_audit.jsonl"
MAX_RETRIES = 5
RETRY_DELAY = 0.01  # 10ms

def log_mcp_action(tool_name: str, args: dict, result: str, status: str = "success", caller: str = "Unknown"):
    """
    Append an audit log record to a JSONL file using a Spin Lock to handle Windows I/O locks.
    """
    def _truncate_args(d: dict, max_len: int = 500) -> dict:
        truncated = {}
        for k, v in d.items():
            if isinstance(v, str) and len(v) > max_len:
                truncated[k] = f"{v[:max_len]}... (truncated, total length: {len(v)})"
            elif isinstance(v, dict):
                truncated[k] = _truncate_args(v, max_len)
            else:
                truncated[k] = v
        return truncated

    record = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "caller": caller,
        "tool": tool_name,
        "args": _truncate_args(args),
        "status": status,
        "result_preview": result[:200] + "..." if len(result) > 200 else result
    }
    
    line = json.dumps(record, ensure_ascii=False) + "\n"
    
    for attempt in range(MAX_RETRIES):
        try:
            with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
                f.write(line)
            return  # Success
        except PermissionError:
            # File is locked by another process, wait and retry
            logger.warning(f"I/O lock encountered on {AUDIT_LOG_PATH}. Retrying {attempt+1}/{MAX_RETRIES}...")
            time.sleep(RETRY_DELAY)
        except Exception as e:
            logger.error(f"Failed to write audit log: {e}")
            break
            
    logger.error(f"Failed to write audit log after {MAX_RETRIES} attempts.")
