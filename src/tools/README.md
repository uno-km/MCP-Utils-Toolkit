# AMEVA MCP Tools Directory Specification

이 디렉토리는 AMEVA MCP Toolkit에서 제공하는 모든 에이전트 전용 도구(MCP Tools)의 비즈니스 로직 구현체를 모아둔 통합 디렉토리입니다.

## 디렉토리 구조 및 역할

- **database/**: SQLite 데이터베이스 연결 및 통합 데이터 연산을 처리합니다. ([상세 README](database/README.md))
  - 주요 도구: db_get_schema, db_execute_query, db_merge_tables
- **document/**: 마크다운 변환 및 Docker 컨테이너 내 파일 조작을 담당합니다.
  - 주요 도구: convert_md_to_docx, delete_file_in_docker, move_file_in_docker
- **git/**: 로컬 워크스페이스 형상 관리 기능을 제공합니다. ([상세 README](git/README.md))
  - 주요 도구: git_status, git_log, git_diff, git_clone, git_pull, git_commit_and_push 등
- **ssh/**: SSH 연결을 통한 원격 서버 셸 명령어 실행을 담당합니다.
  - 주요 도구: ssh_run_command
- **utils/**: 시스템 리소스 모니터링 및 네트워크 상태 점검을 지원합니다. ([상세 README](utils/README.md))
  - 주요 도구: get_system_info, check_port 등
- **web/**: 외부 웹 페이지 데이터 수집 및 본문 텍스트 추출을 수행합니다.
  - 주요 도구: crawl_website

---

## 도구 추가 및 확장 규칙 (Developer Guide)

새로운 도구를 개발하여 에이전트에게 제공할 때는 다음 설계 규칙을 엄격히 준수해야 합니다.

### 1. 관심사의 분리 (Decoupling)
- src/tools/ 내부 모듈은 **FastMCP 데코레이터 및 MCP 관련 프레임워크 라이브러리(mcp.server.fastmcp)에 절대 의존하지 않아야 합니다.**
- 모든 도구는 순수 파이썬 함수(Pure Python Function)로 작성하며, 외부 환경 설정(예: 도커 내부 실행 여부 등)은 환경 변수(os.environ)를 통해서만 판단합니다.

### 2. 예외 처리 (Error Handling)
- 비정상 종료(Exception)가 발생하여 MCP 서버 전체가 정지하지 않도록, 도구 내부의 최상위 실행단에서 	ry-except 예외 처리를 거치고 정제된 에러 메시지를 문자열(string)로 반환해야 합니다.

### 3. 경로 검증 (Path Safety)
- 호스트의 주요 시스템 영역을 침범하지 않도록, 입력받는 작업 디렉토리나 파일 경로는 _get_safe_path와 같은 검증 함수를 거쳐 안전한 허용 기준 디렉토리(C:\\ameva) 내부로 제한해야 합니다.

### 4. 서버 등록 절차
- 신규 구현된 파이썬 함수는 [src/server.py](../server.py) 파일 상단에 임포트하고, @mcp.tool 데코레이터를 사용하여 등록합니다.
- 이때 기입하는 description과 파라미터 타입 힌트는 AI 에이전트가 도구를 호출할지 판단하는 직접적인 기준이 되므로 **자연어로 명확하게 명세**해야 합니다.
