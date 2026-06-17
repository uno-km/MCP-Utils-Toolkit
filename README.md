# AMEVA MCP Toolkit

AMEVA 에이전트 생태계의 자동화 및 개발 생산성 향상을 위한 모델 컨텍스트 프로토콜(MCP) 서버입니다. Git 제어, 문서 변환, 원격 명령어 실행, 데이터베이스 연산 등 다양한 개발자 도구를 단일 서버 인프라에 통합하여 제공합니다.

---

## 핵심 구조 및 아키텍처

- **src/server.py**: FastMCP 엔진 기반의 서버 진입점입니다. 각 도구의 API 명세를 정의하고 내부 구현체와 연결합니다.
- **src/tools/**: 도메인별 독립적인 비즈니스 로직 구현체들로 구성됩니다.
  - `database`: SQLite 데이터베이스 통합 및 마이그레이션 도구
  - `document`: 마크다운의 DOCX 변환 및 컨테이너 내부 파일 관리 도구
  - `git`: 로컬 작업 공간의 형상 관리 자동화 도구
  - `ssh`: 원격 서버 제어 및 셸 스크립트 실행 도구
  - `utils`: 시스템 상태 점검 및 네트워크 포트 스캔 도구
  - `web`: 웹 크롤링 및 데이터 수집 도구
- **src/utils/**: 감사 로깅 및 통계 모니터링 등 서버 운영에 필요한 내부 공통 헬퍼입니다.

---

## 제공 API 및 도구 명세 (API & Tool Reference)

전체 도구 API 리스트 및 요약 정보입니다. 상세 파라미터 정보 및 AI 활용 사례는 각 명세서 문서를 참고하십시오.

### 1. Git 도구군 (GIT)
> [상세 명세서 바로가기 (Git API Spec)](src/tools/git/README.md)

| 도구명 (Tool Name) | 설명 (Description) | 주요 파라미터 (Main Params) |
| :--- | :--- | :--- |
| `git_status` | 리포지토리의 작업 공간 상태 조회 (`git status -sb`) | `repo_name` |
| `git_log` | 커밋 로그 내역 조회 (단선 형태 그래프 출력) | `repo_name`, `limit` |
| `git_diff` | 수정되거나 스테이징된 변경 사항 비교 | `repo_name`, `file_path` |
| `git_clone` | 원격 저장소를 로컬 컴퓨터로 복제 | `repo_url`, `repo_name` |
| `git_pull` | 원격 저장소의 최신 커밋 풀 및 병합 | `repo_name` |
| `git_commit_and_push` | 전체 추가(`git add .`), 커밋 및 원격지 푸시 | `repo_name`, `commit_message` |
| `git_branch` | 브랜치 목록 조회, 신규 생성 및 삭제 | `repo_name`, `action`, `branch_name` |
| `git_checkout` | 브랜치 전환(신규 생성 포함) 및 파일 복구 | `repo_name`, `branch_or_file`, `create` |
| `git_merge` | 특정 브랜치를 현재 활성화된 브랜치에 병합 | `repo_name`, `branch_name` |
| `git_reset` | 현재 HEAD 포인터를 특정 해시로 복구/이동 | `repo_name`, `mode`, `commit_hash` |
| `git_stash` | 로컬 변경분을 임시 공간으로 대피 또는 복구 | `repo_name`, `action`, `stash_id` |

### 2. 시스템 및 유틸리티 도구군 (UTILS)
> [상세 명세서 바로가기 (Utils API Spec)](src/tools/utils/README.md)

| 도구명 (Tool Name) | 설명 (Description) | 주요 파라미터 (Main Params) |
| :--- | :--- | :--- |
| `get_system_info` | CPU, Memory, Disk 등 호스트 상태 지표 확인 | 없음 |
| `check_port` | 특정 호스트의 TCP 포트 개방 상태 진단 | `host`, `port` |
| `generate_uuid` | 고유한 UUID v4 문자열 무작위 생성 | 없음 |
| `format_json` | JSON 문자열 구문 검증 및 들여쓰기 정렬 포맷팅 | `json_str` |
| `base64_encode_decode` | Base64 인코딩 및 디코딩 기능 지원 | `mode`, `data` |
| `calculate_file_hash` | 파일 무결성 확인용 해시(MD5/SHA256) 연산 | `file_path`, `algorithm` |
| `get_external_ip` | 내부 로컬 및 외부 공인 IP 주소 조회 | 없음 |
| `send_http_request` | REST API 테스트를 위한 HTTP 요청 송신 | `method`, `url`, `headers_json`, `body` |
| `find_large_files` | 디렉토리 내 대용량 파일 탐색 | `dir_path`, `size_mb` |
| `extract_text_from_url` | HTML 문서를 제거한 순수 텍스트 본문 추출 | `url` |

---

## 설계 중점 사항 (Key Focus)

- **도구 도메인 분류 명세화**: `DOC`, `GIT`, `CODE`, `INF` 등 도구의 특성에 맞게 I/O 모델과 성능 락킹 범위를 구분하여 동작 안정성을 도모합니다.
- **감사 추적성(Audit Traceability)**: 호출 주체와 인수, 수행 결과 및 요약본을 `mcp_audit.jsonl`에 정형 데이터로 영구 보관합니다.
- **모듈화와 관심사 분리**: FastMCP 라우팅 로직과 실제 도구의 실행 구현체를 물리적으로 완전히 분리하여 유지보수 용이성을 확보했습니다.

---

## 트레이드오프 (Trade-offs)

- **동기식 감사 로그 기록과 병목 현상**:
  - 데이터 신뢰성을 위해 도구가 동작할 때마다 감사 로그 파일(`mcp_audit.jsonl`)을 동기식으로 기록합니다. 다수의 에이전트가 동시에 API를 고빈도로 호출할 경우 디스크 I/O 병목이 유발될 수 있습니다.
- **독립성과 호스트 직접 제어의 균형**:
  - 문서 변환 등 외부 종속성이 강한 기능은 Docker 컨테이너 격리를 통해 안전을 기하지만, Git 및 SSH 제어는 호스트 운영체제 환경의 프로세스를 직접 구동합니다. 이는 격리 수준을 낮추는 대신 시스템 전역 리소스에 즉각 접근할 수 있는 실용성을 취한 선택입니다.
- **FastMCP 프레임워크 선택**:
  - 빠른 스키마 생성과 신속한 기능 확장을 위해 FastMCP 래퍼를 활용합니다. 이로 인해 원시 MCP 프로토콜이 제공하는 세밀한 세션 제어나 커스텀 에러 핸들링을 적용하기가 다소 제한적입니다.

---

## 트러블슈팅 (Troubleshooting)

- **Git `index.lock` 충돌**:
  - 현상: 여러 에이전트가 동시에 특정 리포지토리에 git 작업을 요청하면 `index.lock` 파일이 선점되어 충돌이 발생합니다.
  - 해결: 동시 수정이 빈번할 경우 원격 브랜치 상태 확인(`git fetch`) 단계와 실제 쓰기 커밋 단계를 분리 호출하거나, 로컬 큐잉 처리를 도입해야 합니다.
- **Docker 볼륨 마운트 권한 및 경로 해석 오류**:
  - 현상: 컨테이너 외부 호스트 경로를 `convert_md_to_docx` 도구에 바로 주입할 시 경로 오매핑으로 인해 파일을 찾지 못합니다.
  - 해결: 도구 호출 전 호스트 절대 경로가 컨테이너와 정합하게 공유(마운트)되어 있는지 확인하고, 볼륨 맵 기준으로 상대 경로를 조정하십시오.
- **SSH 인증 오류 및 네트워크 제한**:
  - 현상: 원격 명령어 실행 중 `Auth failed` 또는 `Timeout` 오류가 발생합니다.
  - 해결: 대상 서버의 SSH 포트(기본 22번) 개방 상태를 `check_port` 도구로 먼저 확인한 후, 비밀번호 또는 프라이빗 키의 인코딩 형식과 특수문자 누락 여부를 확인하십시오.
