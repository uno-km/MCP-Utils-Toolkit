# AMEVA MCP Toolkit Utils

> **62개 MCP 도구**를 제공하는 AMEVA 에코시스템의 핵심 범용 유틸리티 서버.  
> Git, DB, 웹 크롤링, 시스템 모니터링, Docker, 네트워크 스캔, 코드 검색까지 단일 서버로 통합.

---

## 📦 도구 도메인 구조

| 도메인 | 경로 | 도구 수 | 설명 |
| :----- | :--- | :-----: | :--- |
| **Document** | `src/tools/document/` | 6 | 디렉터리 및 코드베이스 병합, MD↔DOCX 변환, 이미지 경로 수정, 파일 관리 |
| **Git** | `src/tools/git/` | 13 | git 전 작업 + 전체 레포 브로드캐스트, 커밋 메시지 생성 |
| **SSH** | `src/tools/ssh/` | 1 | 원격 SSH 커맨드 실행 |
| **Web** | `src/tools/web/` | 3 | 웹 크롤링, 가독성 클리너, 데드링크 스캐너 |
| **Database** | `src/tools/database/` | 19 | SQLite CRUD, 스키마, ERD, 마스킹/언마스킹, 동기화 |
| **System Utils** | `src/tools/utils/` | 16 | 시스템/GPU/온도, 프로세스, 스케줄러, REST 클라이언트, HTML→PDF |
| **Docker** | `src/tools/docker/` | 1 | 컨테이너 목록/시작/정지/로그/통계/inspect |
| **Dataset** | `src/tools/dataset/` | 1 | Audit 로그 전사 병합 및 통계 분석 |
| **Search** | `src/tools/search/` | 1 | BM25 기반 소스코드 전역 검색 |
| **Network** | `src/tools/network/` | 1 | 병렬 포트 스캔 & AMEVA 서비스 자동 인식 |
| **총계** | | **62** | |

---

## 🔐 보안 정책

### 경로 보안
- **모든** 파일시스템 접근은 `C:\ameva` 하위만 허용 (Path Traversal 방지)
- Docker 컨테이너 내부 실행 시 `/app/workspace` 자동 리매핑

### CUD 쓰기 토큰 보안
DB, 마스킹, 동기화 등 데이터 **변경** 작업은 `client_token` 필수:
```bash
# 환경변수 설정
AMEVA_DB_WRITE_TOKEN=your-secret-token-here
```
토큰이 일치하지 않으면 `Security Error: CUD (Write) operation is restricted.` 반환.

---

## 🛠️ 전체 도구 목록

### 📄 Document & File (6개)

| 도구명 | 설명 |
| :----- | :--- |
| `consolidate_codebase` | 대상 디렉터리의 구조, 라이브러리를 제외한 전체 소스 코드, 그리고 존재하는 SQLite DB 스키마를 하나의 마크다운 파일로 병합 및 추출합니다. |
| `convert_md_to_docx` | 마크다운 → DOCX (헤딩, 리스트, 코드블록, 볼드 지원) |
| `docx_to_markdown` | DOCX → 마크다운 (헤딩, 테이블, 볼드/이탤릭 파싱) |
| `md_image_path_fixer` | MD 내 깨진 이미지 경로 자동 교정 |
| `delete_file_in_docker` | Docker 내 파일 삭제 |
| `move_file_in_docker` | Docker 내 파일 이동/리네임 |

### 🌿 Git & Source Control (13개)

| 도구명 | 설명 |
| :----- | :--- |
| `git_status` | 레포 상태 조회 |
| `git_pull` | 원격 풀 (토큰 자동 주입) |
| `git_commit_and_push` | add + commit + push 원스텝 |
| `git_clone` | 원격 레포 클론 |
| `git_log` | 커밋 히스토리 조회 |
| `git_diff` | 변경사항 diff |
| `git_branch` | 브랜치 목록/생성/삭제 |
| `git_checkout` | 브랜치/파일 체크아웃 |
| `git_merge` | 브랜치 머지 |
| `git_reset` | soft/mixed/hard 리셋 |
| `git_stash` | stash push/pop/list/apply/clear |
| `workspace_git_broadcaster` | **전체 AMEVA 레포 일괄 상태 진단** |
| `git_commit_helper` | **staged diff 기반 커밋 메시지 자동 생성** |

### 🌐 Web & Crawling (3개)

| 도구명 | 설명 |
| :----- | :--- |
| `crawl_website` | 웹사이트 크롤 (링크/텍스트/메타) |
| `web_readability_cleaner` | 광고/네비 제거 후 순수 마크다운 변환 |
| `dead_link_scanner` | MD 파일 내 데드링크 전수 검사 |

### 🗄️ Database (19개)

| 도구명 | 쓰기 토큰 | 설명 |
| :----- | :-------: | :--- |
| `db_get_schema` | ❌ | 스키마 분석 |
| `db_execute_query` | 조건부 | SQL 실행 (output_format: markdown/json/csv/html/xml/plain) |
| `db_view_table_data` | ❌ | 테이블 브라우저 (페이징, 정렬, 필터) |
| `db_summarize_table` | ❌ | 테이블 프로파일링 |
| `db_search_schema` | ❌ | 스키마 키워드 검색 |
| `db_global_search_value` | ❌ | 전체 텍스트 컬럼 값 검색 |
| `db_generate_erd` | ❌ | Mermaid ERD 다이어그램 생성 |
| `db_generate_mock_data` | ✅ | 가짜 테스트 데이터 삽입 |
| `db_merge_tables` | ✅ | DB 간 테이블 머지 |
| `db_sync_connector` | ✅ | **DB 간 테이블 벌크 동기화 (upsert)** |
| `db_mask_table_data` | ✅ | 컬럼 GDPR 마스킹 |
| `db_unmask_table_data` | ✅ | **마스킹 복원 (shadow 테이블 또는 규칙 기반)** |
| `db_enable_time_travel` | ✅ | shadow ledger + 트리거 활성화 |
| `db_restore_time_travel` | ✅ | 타임스탬프 기반 데이터 복원 |
| `db_compare_schemas` | ❌ | 두 DB 스키마 비교 + 동기화 DDL |
| `db_transpile_sqlite_to_other` | ❌ | SQLite → PostgreSQL/MySQL 변환 |
| `db_optimize_query_tuning` | ❌ | 인덱스 추천 분석 |
| `db_format_sql` | ❌ | SQL 포매팅/키워드 대문자화 |
| `db_profile_and_scan_health` | ❌ | DB 헬스체크 (FK 무결성, 인덱스 분석) |

### ⚙️ System Utilities (16개)

| 도구명 | 설명 |
| :----- | :--- |
| `get_system_info` | CPU/메모리/디스크 현황 |
| `check_port` | TCP 포트 열림 여부 확인 |
| `generate_uuid` | UUID v4 생성 |
| `format_json` | JSON 포맷/검증 |
| `base64_encode_decode` | Base64 인코딩/디코딩 |
| `calculate_file_hash` | MD5/SHA256 해시 계산 (Docker) |
| `get_external_ip` | 내부/외부 IP 조회 |
| `send_http_request` | 임의 HTTP 요청 |
| `find_large_files` | 대용량 파일 탐색 (Docker) |
| `extract_text_from_url` | URL에서 순수 텍스트 추출 |
| `gpu_monitor` | **GPU 사용률/VRAM/온도/전력 실시간 조회** |
| `system_thermal_scanner` | **CPU 온도/클럭/코어별 사용률** |
| `process_watchdog` | **프로세스 스캔/탐색/강제종료** |
| `task_cron_scheduler` | **Windows schtasks / Linux crontab 관리** |
| `rest_client_simulator` | **curl 없는 REST API 테스트 + curl 등가 출력** |
| `html_to_pdf_renderer` | **HTML/URL → PDF 변환 (weasyprint/pdfkit/headless)** |

### 🐳 Docker Container Control (1개)

| 도구명 | 설명 |
| :----- | :--- |
| `docker_container_manager` | 컨테이너 list/stats/start/stop/restart/logs/inspect |

### 📦 Dataset & Audit (1개)

| 도구명 | 설명 |
| :----- | :--- |
| `audit_log_aggregator` | 전체 AMEVA 프로젝트 mcp_audit.jsonl 병합 및 통계 |

### 🔍 Code Search (1개)

| 도구명 | 설명 |
| :----- | :--- |
| `vector_code_searcher` | BM25 알고리즘 소스코드 전역 검색 (컨텍스트 하이라이팅) |

### 🌐 Network Discovery (1개)

| 도구명 | 설명 |
| :----- | :--- |
| `service_discovery` | 병렬 포트 스캔 + AMEVA 서비스 자동 인식 (Streamlit/Gradio/Ollama 등) |

---

## 🚀 빠른 시작

### 필수 환경변수

```bash
AMEVA_GITHUB_TOKEN=ghp_xxxx         # GitHub 인증 토큰 (git push/pull)
AMEVA_DB_WRITE_TOKEN=your-secret    # DB 쓰기 권한 토큰
AMEVA_IN_CONTAINER=true             # Docker 내부 실행 시
```

### 실행

```bash
# 로컬 직접 실행
cd src
python server.py

# Docker 실행
docker compose up -d
```

### MCP 클라이언트 연결 (Claude Desktop)

```json
{
  "mcpServers": {
    "ameva-toolkit-utils": {
      "command": "python",
      "args": ["C:/ameva/AMEVA-MCP-Toolkit-Utils/src/server.py"],
      "env": {
        "AMEVA_GITHUB_TOKEN": "ghp_xxxx",
        "AMEVA_DB_WRITE_TOKEN": "your-secret"
      }
    }
  }
}
```

---

## 📂 프로젝트 구조

```
AMEVA-MCP-Toolkit-Utils/
├── src/
│   ├── server.py              # FastMCP 서버 진입점 (62개 도구 등록)
│   ├── tools/
│   │   ├── document/          # MD↔DOCX, 파일 관리
│   │   ├── git/               # Git 전 작업 + 브로드캐스터
│   │   ├── ssh/               # 원격 SSH
│   │   ├── web/               # 크롤링, 가독성, 데드링크
│   │   ├── database/          # SQLite 전 기능
│   │   ├── utils/             # 시스템, GPU, 프로세스, 스케줄러
│   │   ├── docker/            # 컨테이너 관리
│   │   ├── dataset/           # Audit 로그 병합
│   │   ├── search/            # BM25 코드 검색
│   │   └── network/           # 포트 스캔
│   └── utils/
│       └── audit_logger.py    # MCP 액션 감사 로그
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## 📋 requirements.txt 의존성

```
mcp[cli]
fastmcp
requests
beautifulsoup4
psutil
python-docx
paramiko
```

> **선택적**: `weasyprint` 또는 `pdfkit` (HTML→PDF), `nvidia-smi` (GPU 모니터)

---

## 🌐 GitHub-Native MCP Hub Tools (WASM Browser Direct)

AMEVA OS 브라우저 샌드박스 내부에서 다운로드 없이 실행되는 경량 브라우저 전용 도구 모음 (`mcp_manifest.json`):

| 도구명 | 타입 | 설명 | 입력 스키마 (Arguments) |
| :--- | :---: | :--- | :--- |
| `format_json` | Python | JSON 포맷터 | `json_string` |
| `base64_encode` | Python | Base64 인코더/디코더 | `data`, `mode` |
| `text_transform` | Python | 영문 텍스트 대소문자/순서 변환 | `text`, `mode` |
| `calc` | Python | 수식 안전 계산기 | `expression` |
| `generate_uuid` | Python | UUID v4 생성 | `count` |
| `timestamp_convert` | Python | Unix Timestamp 변환 | `mode`, `value` |
| `hash_text` | Python | 해시값(md5, sha256 등) 생성 | `text`, `algorithm` |
| `regex_match` | Python | 정규표현식 패턴 매치/치환 | `pattern`, `text`, `mode`, `replacement` |
| `mermaid_to_png` | JS | **Mermaid 다이어그램 코드 → PNG 렌더링 후 VFS 저장** | `mermaid_code`, `output_path` |

---

## 🧠 Smart Dynamic Test Runner (동적 테스트 자동화)

개발 중 유닛 테스트 실행을 쾌적화하기 위해, 윈도우/리눅스 공통으로 가동되는 스마트 동적 테스트 러너([run_dynamic_tests.py](file:///C:/ameva/AMEVA-MCP-Toolkit-Utils/run_dynamic_tests.py))를 제공합니다.

### 🌟 핵심 기능
1. **PYTHONPATH 동적 자동 스캔/조립**: 상위 경로(`C:\ameva`) 하위의 모든 `AMEVA-` 서브 프로젝트들의 경로와 `src/` 폴더를 자동으로 찾아 환경 변수로 엮어 줍니다. (더 이상 구차하게 환경 변수 수동 지정을 위해 타이핑할 필요가 없습니다).
2. **Git Diff 스마트 핀포인트 테스트**: 최근 `git diff` 및 `git status`로 변경 감지된 소스 파일들과 명칭 매핑이 성립하는 유닛 테스트들만 선별적으로 찾아내어 초고속으로 수행합니다. (수정 사항이 없거나 매핑 실패 시 전체 테스트 실행으로 자동 안전 Fallback).

### 💻 실행 방법
* **수정된 파일과 연계된 타겟 유닛 테스트만 콕 집어 수행**:
  ```bash
  python run_dynamic_tests.py --modified
  ```
* **전체 유닛 테스트를 자동 조립된 PYTHONPATH 위에서 일괄 수행**:
  ```bash
  python run_dynamic_tests.py --all
  ```
* **특정 대상 서브 프로젝트를 지정하여 테스트 수행**:
  ```bash
  python run_dynamic_tests.py --modified --dir C:\ameva\AMEVA-Nexus-Platform
  ```

---

## 🔒 깃허브 토큰 및 보안 자격증명 유출 방지 규칙 (AI 에이전트 전용)

> [!WARNING]
> **AI 에이전트(LLM) 및 개발자는 깃허브 PAT 토큰(`AMEVA_GITHUB_TOKEN`)이나 보안 검증용 토큰을 소스코드, 구성 파일(`mcp_manifest.json` 등), 혹은 로컬 마크다운 문서 등에 하드코딩하거나 Git 커밋에 포함시켜 유출하는 행위를 강력하게 금지합니다.**

### 🛡️ 토큰 노출 원천 차단 가이드
1. **환경 변수 참조 절대화**: 모든 연동 코드 및 인증 모듈은 하드코딩된 값 대신 `os.environ.get("AMEVA_GITHUB_TOKEN")` 등 환경 변수로부터 값을 공급받아야 합니다.
2. **`.gitignore` 설정 준수**: `.env`, `.token`, `*secret*`, `*.pat` 등 모든 크레덴셜 정보 파일은 절대 Git이 트래킹하지 않도록 `.gitignore` 규칙에 등록되어 차단되고 있습니다.
3. **커밋 전 상태 검사**: Git 스테이징(`git add .`) 전, 파일 내부에 `ghp_` 또는 `ghs_`로 시작하는 실물 GitHub 토큰 스트링이 노출되어 기재되어 있지 않은지 철저히 교차 대조 후 커밋하십시오.

