# AMEVA MCP Toolkit - Metadata Specification

이 명세서는 AMEVA-MCP-Toolkit-Utils 내에서 관리되는 도구(Tool) 및 문서(Document) 리소스의 메타데이터 표준을 정의합니다.
이 규칙에 따라 코드와 도구를 체계적으로 분류하고 관리하여, 병목을 최소화하고 시스템의 일관성을 유지합니다.

## 1. Tool Category (도구 분류 메타데이터)

새로운 MCP 도구를 `src/tools/` 하위에 추가할 때, 다음과 같은 도메인(Category) 메타데이터를 소스 코드 내 주석이나 데코레이터 메타에 포함해야 합니다.

| Category | 설명 | I/O 유형 | 락(Lock) 민감도 | 병목(Bottleneck) 위험도 |
| :--- | :--- | :--- | :--- | :--- |
| **`DOC`** | 문서 변환, 마크다운 렌더링, 텍스트 파싱 등 | File I/O, CPU (Light) | 낮음 | 낮음 |
| **`GIT`** | 형상 관리, 코드 푸시, 풀, 상태 조회 등 | File I/O, Network | **높음 (index.lock)** | 중간 (충돌 주의) |
| **`CODE`** | 린트(Lint), 코드 분석, 정적 검사 등 | CPU (Light) | 낮음 | 낮음 |
| **`INF`** | AI 모델 추론, 이미지 분석 (Inference) | GPU / CPU (Heavy) | 낮음 | **매우 높음 (100% 점유)** |

## 2. Resource Format (문서/리소스 메타데이터)

도구가 입력받고 출력하는 파일의 명세입니다. 
도구를 선언할 때 `input_format`과 `output_format`을 명확히 문서화해야 합니다.

*   `markdown` (`.md`): 일반적인 텍스트 기반 입력 문서
*   `docx` (`.docx`): `DOC` 도구가 출력하는 최종 워드 문서
*   `jsonl` (`.jsonl`): 감사 로그(Audit Log) 및 스트리밍 데이터 구조체
*   `repo` (Directory): `GIT` 도구가 다루는 폴더 단위의 리소스

## 3. 로깅 메타데이터 (Audit Log Schema)

모든 도구 실행은 `mcp_audit.jsonl`에 기록되며, 다음 스키마를 따릅니다.

```json
{
  "time": "YYYY-MM-DD HH:MM:SS",
  "caller": "호출한 에이전트/클라이언트 식별자 (예: Window-Assistant)",
  "tool": "도구 이름 (예: convert_md_to_docx)",
  "args": {
    "key": "value"
  },
  "status": "success | error",
  "result_preview": "결과값 앞 200자 요약"
}
```

이 메타데이터 규칙을 통해 AMEVA 생태계의 모든 도구가 1,000줄 이상의 복잡한 스파게티 코드로 변질되는 것을 막고, 각 도구가 가볍고 예측 가능하게 동작하도록 유지합니다.
