# System & Developer Utility MCP API Specification for AI Agents

본 명세서는 AMEVA MCP Toolkit 내의 시스템 상태 진단 및 개발 보조용 유틸리티 도구(Utils MCP Tools)를 AI 에이전트가 오작동 없이 정확하게 활용할 수 있도록 돕는 API 명세입니다.

---

## 1. API 상세 명세

### 1) get_system_info
- **설명**: 호스트 컴퓨터의 CPU 사용량, 메모리(RAM) 잔여량, 디스크 용량, 운영체제(OS) 환경 등 기본적인 시스템 하드웨어 지표를 반환합니다.
- **파라미터**: 없음
- **반환값**: 호스트 시스템의 메트릭 정보 요약 텍스트.

### 2) check_port
- **설명**: 특정 호스트의 TCP 포트가 열려있는지(연결 가능한지) 확인합니다.
- **파라미터**:
  - `host` (string, 필수): 타겟 IP 주소 또는 도메인명
  - `port` (integer, 필수): 테스트할 포트 번호
- **반환값**: 포트 오픈 성공 여부 및 지연 시간(Rtt) 또는 실패 메시지.

### 3) generate_uuid
- **설명**: 무작위의 고유 UUID v4 문자열을 생성합니다.
- **파라미터**: 없음
- **반환값**: 표준 UUID v4 형식 문자열.

### 4) format_json
- **설명**: 문자열 형태의 JSON이 유효한지 검증하고 들여쓰기가 적용된 예쁜 형식(Pretty-printed)으로 포맷팅합니다.
- **파라미터**:
  - `json_str` (string, 필수): 포맷팅할 원본 JSON 문자열
- **반환값**: 포맷팅된 JSON 문자열 혹은 문법 분석 오류 정보.

### 5) base64_encode_decode
- **설명**: 데이터를 Base64 표준 포맷으로 인코딩하거나 디코딩합니다.
- **파라미터**:
  - `mode` (string, 필수): 실행 모드 (`encode` 또는 `decode`)
  - `data` (string, 필수): 변환 대상 문자열 데이터
- **반환값**: 변환된 Base64 인코딩/디코딩 결과 문자열.

### 6) calculate_file_hash
- **설명**: 지정된 파일의 무결성 검증을 위한 MD5 또는 SHA256 체크섬 해시값을 계산합니다.
- **파라미터**:
  - `file_path` (string, 필수): 타겟 파일 절대/상대 경로 (도커 컨테이너 내부 실행)
  - `algorithm` (string, 기본값: `sha256`): 계산할 알고리즘 (`sha256` 또는 `md5`)
- **반환값**: 계산된 체크섬 문자열.

### 7) get_external_ip
- **설명**: 호스트의 내부 로컬 IP 및 공인 외부 IP 주소를 동시 조회합니다.
- **파라미터**: 없음
- **반환값**: 내부/외부 네트워크 IP 주소 정보.

### 8) send_http_request
- **설명**: 원격 서버에 임의의 HTTP 요청(GET, POST 등)을 송신하고 응답 메타데이터 및 바디를 받아옵니다.
- **파라미터**:
  - `method` (string, 필수): HTTP 메서드 (예: `GET`, `POST`, `PUT`, `DELETE`)
  - `url` (string, 필수): 요청을 전송할 원격지 주소 URL
  - `headers_json` (string, 선택): 커스텀 헤더를 포함한 JSON 형식의 문자열
  - `body` (string, 선택): POST/PUT 시 전송할 페이로드 데이터
- **반환값**: 상태 코드, 응답 헤더 및 바디 문자열 요약.

### 9) find_large_files
- **설명**: 지정된 디렉토리 하위에서 설정된 기준 용량보다 큰 대용량 파일들을 탐색하여 정렬 보고합니다.
- **파라미터**:
  - `dir_path` (string, 필수): 탐색할 디렉토리 경로 (도커 컨테이너 내부 실행)
  - `size_mb` (integer, 기본값: 50): 기준 용량 제한 크기 (단위: Megabytes)
- **반환값**: 기준 초과 대용량 파일 정보 리스트.

### 10) extract_text_from_url
- **설명**: 특정 웹 URL 페이지에서 HTML 마크업 태그와 스타일, 스크립트 영역을 완전히 배제한 순수 텍스트 본문 데이터만을 정제 추출합니다.
- **파라미터**:
  - `url` (string, 필수): 웹 페이지 URL 주소
- **반환값**: 정제된 순수 텍스트 데이터.
