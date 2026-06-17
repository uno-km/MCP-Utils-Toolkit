# AMEVA MCP Internal Utilities (utils)

이 디렉토리는 MCP 서버 구동 및 관리에 필요한 내부 공통 헬퍼 스크립트를 모아둔 곳입니다.
이곳의 모듈들은 AI 에이전트에게 도구(Tool)로 직접 노출되지 않으며, 서버 시스템 내부에서만 호출됩니다.

## 주요 모듈 구성
- **[audit_logger.py](audit_logger.py)**: 도구 호출 이력 및 인수를 mcp_audit.jsonl에 동기식으로 기록하는 보안 감사 로거.
- **[view_stats.py](view_stats.py)**: 서버 사용 통계 및 메트릭 데이터를 취합하는 모듈.
