import os
import json
import glob
from datetime import datetime


AMEVA_BASE = r"C:\ameva"

def audit_log_aggregator(output_dataset_path: str) -> str:
    """
    C:\\ameva 하위 모든 AMEVA 프로젝트에 흩어진 mcp_audit.jsonl 파일들을 수집,
    병합, 파싱하여 단일 통합 데이터셋 JSONL 파일로 저장한다.
    각 레코드에 source_project 필드를 추가하여 출처를 표시한다.
    """
    # 출력 경로 보안 검사
    out_norm = os.path.abspath(output_dataset_path)
    if not out_norm.lower().startswith(r"c:\ameva"):
        return f"Security Error: Output path must be under C:\\ameva. Got: {out_norm}"

    os.makedirs(os.path.dirname(out_norm), exist_ok=True) if os.path.dirname(out_norm) else None

    # 모든 mcp_audit.jsonl 파일 탐색
    pattern = os.path.join(AMEVA_BASE, "**", "mcp_audit.jsonl")
    found_files = glob.glob(pattern, recursive=True)

    if not found_files:
        return f"No mcp_audit.jsonl files found under {AMEVA_BASE}."

    all_records = []
    parse_errors = []
    file_stats = []

    for filepath in found_files:
        # 출처 프로젝트 이름 추출
        rel = os.path.relpath(filepath, AMEVA_BASE)
        project_name = rel.split(os.sep)[0] if os.sep in rel else "root"
        
        file_count = 0
        file_error = 0
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line_no, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        record = json.loads(line)
                        record["source_project"] = project_name
                        record["source_file"] = filepath
                        all_records.append(record)
                        file_count += 1
                    except json.JSONDecodeError as je:
                        parse_errors.append(f"{filepath}:{line_no} - {je}")
                        file_error += 1
        except Exception as e:
            parse_errors.append(f"Failed to read {filepath}: {e}")
            continue

        file_stats.append({
            "file": filepath,
            "project": project_name,
            "records": file_count,
            "errors": file_error
        })

    # 타임스탬프 기준 정렬 (있을 경우)
    def sort_key(r):
        return r.get("timestamp", r.get("time", r.get("ts", "")))

    all_records.sort(key=sort_key)

    # 통합 JSONL 저장
    with open(out_norm, "w", encoding="utf-8") as f:
        for record in all_records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    # 통계 분석
    tool_counts = {}
    project_counts = {}
    for rec in all_records:
        tool = rec.get("tool_name", rec.get("tool", rec.get("action", "unknown")))
        proj = rec.get("source_project", "?")
        tool_counts[tool] = tool_counts.get(tool, 0) + 1
        project_counts[proj] = project_counts.get(proj, 0) + 1

    # 보고서 생성
    report = (
        f"## 📦 Audit Log Aggregator\n\n"
        f"**Output**: `{out_norm}`  \n"
        f"**Total Records**: {len(all_records)}  \n"
        f"**Files Scanned**: {len(found_files)}  \n"
        f"**Parse Errors**: {len(parse_errors)}  \n\n"
    )

    report += "### 📁 Source Files\n"
    report += "| Project | File | Records | Errors |\n"
    report += "| :------ | :--- | :-----: | :----: |\n"
    for stat in file_stats:
        fname = os.path.basename(stat["file"])
        report += f"| `{stat['project']}` | `{fname}` | {stat['records']} | {stat['errors']} |\n"

    report += "\n### 🔧 Top Tool Calls\n"
    report += "| Tool | Count |\n| :--- | :---: |\n"
    for tool, cnt in sorted(tool_counts.items(), key=lambda x: -x[1])[:15]:
        report += f"| `{tool}` | {cnt} |\n"

    report += "\n### 📊 Per-Project Record Count\n"
    report += "| Project | Records |\n| :------ | :-----: |\n"
    for proj, cnt in sorted(project_counts.items(), key=lambda x: -x[1]):
        report += f"| `{proj}` | {cnt} |\n"

    if parse_errors:
        report += f"\n### ⚠️ Parse Errors (first 5)\n"
        for err in parse_errors[:5]:
            report += f"- `{err}`\n"

    return report
