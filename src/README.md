# AMEVA MCP Server Core Sources (src)

이 디렉토리는 AMEVA MCP Toolkit의 핵심 실행 코드 및 모듈들을 포함하고 있습니다.

## tools와 utils의 구조적 차이점

서버 아키텍처는 에이전트 노출 영역(	ools)과 내부 지원 인프라 영역(utils)으로 관심사가 완전히 분리되어 있습니다.

| 구분 | tools (에이전트 도구) | utils (내부 유틸리티) |
| :--- | :--- | :--- |
| **목적** | LLM/에이전트가 직접 호출하여 사용하는 API 제공 | 서버 구동 및 동작을 보조하는 시스템 헬퍼 |
| **MCP 노출** | **노출됨** (@mcp.tool 데코레이터 등록) | **비노출** (내부 모듈식 Import) |
| **주요 역할** | Git 제어, DB 연산, SSH 명령 실행, 웹 크롤링 등 | 쓰기 감사 기록(Audit Logging), 모니터링 통계 등 |
| **상세 이동** | [👉 tools 디렉토리 상세 명세 바로가기](tools/README.md) | [👉 utils 디렉토리 상세 명세 바로가기](utils/README.md) |
