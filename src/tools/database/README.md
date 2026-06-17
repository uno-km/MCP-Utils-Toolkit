# Database MCP API Specification for AI Agents

본 명세서는 AMEVA MCP Toolkit 내의 데이터베이스 관련 도구(Database MCP Tools)를 AI 에이전트가 오작동 없이 정확하게 활용할 수 있도록 돕는 API 명세 및 활용 가이드라인입니다.

---

## 1. 전제 조건 및 인증 규칙

- **작업 경로 기준**: 모든 데이터베이스 도구는 `db_path` (또는 `src_db`, `dest_db`) 파라미터를 입력받습니다. 이는 서버 내부에서 안전성 검증을 거쳐 `C:\ameva\` 하위 경로의 절대 경로에 있는 SQLite 데이터베이스 파일에만 접근을 허용합니다. 허용되지 않은 경로 접근 시 `PermissionError`를 반환합니다.
- **안전 모드 (Read Only)**: `db_execute_query`는 `read_only=True` 플래그가 설정된 경우, 구문 분석을 통해 데이터를 변조하는 임의의 DDL/DML 구문을 사전에 정규식으로 탐색하여 차단합니다.
- **다중 출력 포맷팅 (Output Formatting)**: 데이터를 조회하는 도구(`db_execute_query`, `db_view_table_data`)는 `output_format` 파라미터를 지원합니다. 다음 포맷 중 필요한 형태로 가공하여 반환받을 수 있습니다:
  - `markdown` (기본값): 기호 `|` 와 `-` 를 활용하여 마크다운 테이블 형식으로 보기 좋게 반환합니다.
  - `json`: 헤더와 값을 키-값 쌍으로 매핑한 JSON 배열 문자열을 반환합니다.
  - `csv`: 콤마 구분자 CSV 문자열을 반환합니다.
  - `html`: 정형화된 `<table>` 구조를 반환합니다.
  - `xml`: `<records><row>...</row></records>` XML 형식의 구조를 반환합니다.
  - `plain`: 탭 구분자로 구분된 담백하고 단순한 텍스트 데이터셋을 반환합니다.

---

## 2. API 상세 명세

### 1) db_get_schema
- **설명**: SQLite 데이터베이스 내의 모든 테이블 정의, SQL 스키마 스크립트, 컬럼 구조 및 기본키 정보를 파싱하여 상세 요약 제공합니다.
- **파라미터**:
  - `db_path` (string, 필수): SQLite 데이터베이스 파일의 절대/상대 경로

### 2) db_execute_query
- **설명**: SQL 쿼리 혹은 명령을 직접 실행합니다. SELECT 등 조회 쿼리 시 지정된 포맷으로 변환되어 출력됩니다.
- **파라미터**:
  - `db_path` (string, 필수): 데이터베이스 파일 경로
  - `query` (string, 필수): 실행할 SQL 쿼리
  - `read_only` (boolean, 기본값: `True`): 수정 및 파괴 명령 방지 여부
  - `output_format` (string, 기본값: `markdown`): 출력 가공 포맷 (`markdown`, `json`, `csv`, `html`, `xml`, `plain`)

### 3) db_view_table_data
- **설명**: 특정 테이블의 레코드를 페이징, 정렬, 조건 필터링하여 특정 포맷 형식으로 조회합니다. 에이전트가 직접 파썬 코드를 짜지 않고 테이블 값을 조회할 때 최우선적으로 호출해야 하는 데이터 브라우징 전용 API입니다.
- **파라미터**:
  - `db_path` (string, 필수): 데이터베이스 파일 경로
  - `table_name` (string, 필수): 조회할 테이블명
  - `limit` (integer, 기본값: 50): 최대 조회 로우 수
  - `offset` (integer, 기본값: 0): 페이징 오프셋
  - `sort_by` (string, 선택): 정렬 기준이 될 컬럼명
  - `sort_order` (string, 기본값: `DESC`): 정렬 순서 (`ASC` 또는 `DESC`)
  - `filter_conditions` (string, 선택): WHERE 조건절에 들어갈 필터 구문 (예: `status='ACTIVE'`)
  - `output_format` (string, 기본값: `markdown`): 출력 가공 포맷 (`markdown`, `json`, `csv`, `html`, `xml`, `plain`)

### 4) db_summarize_table
- **설명**: 특정 테이블의 총 레코드 수, 컬럼 스키마 세부 사항, 수치형 변수의 최댓값/최솟값/평균 요약 통계 및 최근 샘플 데이터 5줄을 수록한 시각적 마크다운 분석 보고서를 제공합니다.
- **파라미터**:
  - `db_path` (string, 필수): 데이터베이스 파일 경로
  - `table_name` (string, 필수): 분석할 테이블명

### 5) db_search_schema
- **설명**: 스키마 전역에서 키워드와 매칭되는 테이블명, 컬럼명, 인덱스명을 고속 탐색하여 목록화합니다.
- **파라미터**:
  - `db_path` (string, 필수): 데이터베이스 파일 경로
  - `search_term` (string, 필수): 검색할 키워드

### 6) db_merge_tables
- **설명**: 소스 데이터베이스의 특정 테이블 레코드를 대상 데이터베이스로 병합하며, 고유 키를 비교하여 신규 로우는 INSERT 하고 일치하는 로우는 UPDATE 합니다.
- **파라미터**:
  - `src_db` (string, 필수): 소스 데이터베이스 파일 경로
  - `dest_db` (string, 필수): 대상 데이터베이스 파일 경로
  - `table_name` (string, 필수): 병합할 대상 테이블명
  - `key_column` (string, 필수): 일치 여부를 판별할 기준 고유 키 컬럼명

### 7) db_generate_erd
- **설명**: 데이터베이스 테이블들과 외래키(FK) 참조 제약 조건을 분석하여 Mermaid ER Diagram 코드를 출력합니다.
- **파라미터**:
  - `db_path` (string, 필수): 데이터베이스 파일 경로
- **반환값**: 마크다운 렌더링용 `erDiagram` 문법 문자열

### 8) db_generate_mock_data
- **설명**: 테이블의 각 컬럼 도메인 속성(이름, 타입, 제약) 및 상위 외래키 참조 관계를 추적하여 부합하는 가상의 무작위 한글/영문 데이터셋을 대량 삽입합니다.
- **파라미터**:
  - `db_path` (string, 필수): 데이터베이스 파일 경로
  - `table_name` (string, 필수): 대상 테이블명
  - `count` (integer, 기본값: 50): 생성 및 삽입할 가상 로우(Row) 수

### 9) db_global_search_value
- **설명**: 전체 데이터베이스 내의 모든 테이블과 텍스트 필드를 전수 스캔하여 주어진 키워드와 매칭되는 로우의 위치를 반환합니다.
- **파라미터**:
  - `db_path` (string, 필수): 데이터베이스 파일 경로
  - `search_query` (string, 필수): 검색할 텍스트 키워

### 10) db_transpile_sqlite_to_other
- **설명**: SQLite 스키마 DDL 및 적재된 레코드 DML 데이터를 PostgreSQL 또는 MySQL에 호환되는 이기종 마이그레이션 SQL 스크립트로 자동 번역합니다.
- **파라미터**:
  - `db_path` (string, 필수): 데이터베이스 파일 경로
  - `target_dialect` (string, 필수): 타겟 다이얼렉트 종류 (`postgresql` 또는 `mysql`)

### 11) db_profile_and_scan_health
- **설명**: 중복 인덱스, 고아 외래키 위반 데이터, 50% 이상의 과도한 NULL 필드 비율, 3-시그마 표준편차를 초과하는 수치 이상값(Outlier) 등을 스캔하여 품질 보고서를 생성합니다.
- **파라미터**:
  - `db_path` (string, 필수): 데이터베이스 파일 경로

### 12) db_format_sql
- **설명**: 줄바꿈 및 예약어 대문자 정렬 등을 통해 복잡한 SQL문을 보기 좋게 개행 포맷팅합니다.
- **파라미터**:
  - `query` (string, 필수): 포맷팅할 원본 SQL 구문

### 13) db_compare_schemas
- **설명**: 두 데이터베이스의 구조적 차이점(미생성 테이블, 미존재 컬럼 등)을 비교 분석하여 대상 데이터베이스를 동기화하기 위한 `ALTER TABLE`/`CREATE TABLE` DDL 스크립트를 반환합니다.
- **파라미터**:
  - `src_db` (string, 필수): 기준 소스 데이터베이스 파일 경로
  - `dest_db` (string, 필수): 동기화시킬 대상 데이터베이스 파일 경로

### 14) db_mask_table_data
- **설명**: 주민번호, 이름, 이메일, 전화번호 등의 열을 비식별 규칙(GDPR 준수 가명화)에 맞춰 무작위 마스킹 처리하여 레코드를 업데이트합니다.
- **파라미터**:
  - `db_path` (string, 필수): 데이터베이스 파일 경로
  - `table_name` (string, 필수): 대상 테이블명
  - `mask_rules_json` (string, 필수): 컬럼별 규칙 매핑 JSON (예: `{"email": "mask_email", "name": "mask_name"}`)

### 15) db_optimize_query_tuning
- **설명**: 쿼리를 `EXPLAIN QUERY PLAN`으로 시뮬레이션하여 테이블 풀 스캔(Full Scan) 병목을 감지하고, 성능을 비약적으로 개선할 수 있는 최적의 `CREATE INDEX` 구문을 추천합니다.
- **파라미터**:
  - `db_path` (string, 필수): 데이터베이스 파일 경로
  - `slow_query` (string, 필수): 튜닝 대상 SQL 쿼리

### 16) db_enable_time_travel
- **설명**: 대상 테이블에 변경 기록용 원장(`_ledger`) 및 변경 추적 트리거들을 자동 설치하여 시간 여행 조회가 가능하게 합니다.
- **파라미터**:
  - `db_path` (string, 필수): 데이터베이스 파일 경로
  - `table_name` (string, 필수): 대상 테이블명

### 17) db_restore_time_travel
- **설명**: 설치된 시간 여행 원장을 바탕으로 특정 과거 시점(Timestamp)으로 테이블 상태를 완전히 롤백 복구합니다.
- **파라미터**:
  - `db_path` (string, 필수): 데이터베이스 파일 경로
  - `table_name` (string, 필수): 대상 테이블명
  - `target_timestamp` (string, 필수): 되돌릴 기준 시각 (예: `2026-06-17 15:30:00`)
