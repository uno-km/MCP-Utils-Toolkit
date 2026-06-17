# 🧠 AMEVA MCP 아이디어 노트

> 이번 작업하면서 자주 요청된 패턴 분석 및 신규 MCP 바인딩 아이디어

---

## 📊 자주 요청된 명령어 TOP 패턴 (이번 세션 기준)

| 순위 | 요청 패턴 | 빈도 | 현재 상태 |
| :--: | :-------- | :--: | :-------: |
| 1 | `git_commit_and_push` | ★★★★★ | ✅ 구현됨 |
| 2 | `git_status` (전체 레포) | ★★★★★ | ✅ `workspace_git_broadcaster` |
| 3 | 파일 쓰기 / 코드 수정 | ★★★★★ | 🔒 에이전트 직접 수행 |
| 4 | `git_fetch` (동기화) | ★★★★ | ✅ `git_pull` 내부에 포함 |
| 5 | DB 스키마 조회 | ★★★★ | ✅ `db_get_schema` |
| 6 | 파이썬 스크립트 실행 검증 | ★★★★ | ✅ 내부적으로 `subprocess` |
| 7 | README 작성 / 업데이트 | ★★★ | 🔒 에이전트 직접 수행 |
| 8 | 커밋 메시지 생성 | ★★★ | ✅ `git_commit_helper` |
| 9 | 포트/서비스 상태 확인 | ★★★ | ✅ `service_discovery` |
| 10 | 데이터 포맷 변환 | ★★★ | ✅ `db_execute_query (output_format)` |

---

## 💡 다음 MCP 바인딩 아이디어

> 역대 대화 분석 기반 + 이번 세션에서 반복된 수동 작업 → MCP 자동화 후보

### 🔥 HIGH PRIORITY (자주 쓴다, 바로 만들자)

#### 1. `file_editor` — 에이전트 수동 편집을 MCP로
```
file_editor(action: "read"|"write"|"append"|"replace", 
            path: str, content: str = None, 
            start_line: int = None, end_line: int = None)
```
> 현재 에이전트가 직접 파일을 쓰는데, 이걸 MCP로 노출하면  
> Antigravity나 다른 LLM 클라이언트도 표준으로 편집 가능.  
> **경로 보안**: `C:\ameva` 화이트리스트 필수.

#### 2. `python_runner` — 파이썬 스크립트 샌드박스 실행
```
python_runner(script_path: str = None, code: str = None, 
              timeout: int = 30, capture_output: bool = True)
```
> 매번 `subprocess.run(["python", ...])` 패턴이 반복됨.  
> 코드 문자열 또는 파일 경로를 받아 격리 실행.  
> Docker 샌드박스 옵션 포함.

#### 3. `ameva_config_manager` — 프로젝트 config.json 중앙 관리
```
ameva_config_manager(action: "get"|"set"|"list", 
                     key: str = None, value: str = None)
```
> `C:\ameva\config.json`을 읽고 쓰는 작업이 반복됨.  
> 환경변수, 토큰, 경로 설정을 한 곳에서 관리.

#### 4. `workspace_health_checker` — AMEVA 생태계 전체 헬스체크
```
workspace_health_checker() -> str
```
> 매 세션 시작 시 상태 파악에 시간이 많이 걸림.  
> 체크 항목: git 상태, Docker 실행 여부, Python 버전, 필수 env 변수, 포트 상태.  
> 한 번 호출로 전체 상태 리포트.

---

### ⚡ MEDIUM PRIORITY (있으면 꽤 유용함)

#### 5. `log_viewer` — 실시간 로그 테일러
```
log_viewer(log_path: str, lines: int = 100, 
           filter_keyword: str = None, level: str = None)
```
> `mcp_audit.jsonl`, `debug.log` 등 로그 파일을 직접 tail하는 요청 반복.  
> 레벨 필터(ERROR/WARNING), 키워드 필터 포함.

#### 6. `markdown_renderer` — MD를 HTML로 변환 후 미리보기
```
markdown_renderer(md_path: str, output_html_path: str = None) -> str
```
> README 작성 후 바로 미리보기 확인 요청이 자주 있었음.  
> Python `markdown` 라이브러리로 HTML 생성.

#### 7. `dependency_scanner` — requirements.txt 취약점/버전 스캔
```
dependency_scanner(requirements_path: str) -> str
```
> `requirements.txt`를 읽어 PyPI에서 최신 버전과 비교.  
> 레거시/보안 취약 패키지 감지.

#### 8. `env_manager` — .env 파일 안전 관리
```
env_manager(action: "get"|"set"|"list"|"delete", 
            env_file_path: str, key: str = None, value: str = None)
```
> `.env` 파일 읽기/쓰기 요청 반복.  
> 값 마스킹 출력 (TOKEN, SECRET, PASSWORD 등은 `***` 처리).

#### 9. `project_scaffolder` — AMEVA 신규 프로젝트 스캐폴딩
```
project_scaffolder(project_name: str, template: str = "python-mcp")
```
> 새 AMEVA 프로젝트 생성 요청 패턴:  
> 표준 폴더 구조, `.gitignore`, `README.md`, `requirements.txt` 자동 생성.  
> 템플릿: `python-mcp`, `fastapi`, `streamlit`, `agent`

#### 10. `text_diff_viewer` — 두 텍스트/파일 차이 비교
```
text_diff_viewer(text_a: str = None, text_b: str = None,
                 file_a: str = None, file_b: str = None,
                 output_format: str = "unified") -> str
```
> 파일 변경 전후 비교 요청이 자주 있었음.  
> unified diff, side-by-side, HTML 포맷 지원.

---

### 🤔 LOWER PRIORITY (나중에 별도 툴킷으로)

#### 11. `llm_chain_tester` — 로컬 LLM API 체인 테스트
```
llm_chain_tester(model: str, prompt: str, 
                 endpoint: str = "http://localhost:11434")
```
> Ollama 로컬 LLM 호출 테스트 반복.  
> `rest_client_simulator`로 대체 가능하나, LLM 특화 응답 파싱 추가.

#### 12. `vector_db_manager` — Milvus/Chroma 벡터 DB 관리
```
vector_db_manager(action: "collections"|"search"|"insert",
                  collection: str, query: str = None)
```
> AMEVA 에코시스템에서 벡터 DB 사용 빈도 증가 중.

#### 13. `model_benchmark_runner` — 모델 성능 벤치마크 실행
```
model_benchmark_runner(model_path: str, dataset_path: str,
                       metric: str = "wer")
```
> AMEVA-Benchmark-Suite 레포와 연동.

#### 14. `ameva_news_digest` — AMEVA 레포 변경사항 뉴스레터
```
ameva_news_digest(days: int = 7) -> str
```
> 최근 N일 동안 모든 AMEVA 레포의 커밋/변경을 요약.  
> `workspace_git_broadcaster` + `git_log` 조합.

---

## 🏗️ 추천 바인딩 방법

### 방법 A: 기존 AMEVA-MCP-Toolkit-Utils에 추가
- `file_editor`, `python_runner`, `ameva_config_manager`, `log_viewer`는  
  기존 `src/tools/utils/` 또는 `src/tools/document/`에 자연스럽게 합류 가능.

### 방법 B: 신규 AMEVA-MCP-DevOps 툴킷 생성
```
AMEVA-MCP-DevOps/
├── src/tools/
│   ├── scaffold/       # project_scaffolder
│   ├── benchmark/      # model_benchmark_runner
│   ├── deps/           # dependency_scanner
│   ├── env/            # env_manager
│   └── llm/            # llm_chain_tester
```

### 방법 C: 에이전트 내장 스킬로 정의
- `workspace_health_checker`처럼 여러 도구를 조합하는 도구는  
  MCP보다 에이전트 스킬(Antigravity Skill)로 정의하는 게 더 효율적.

---

## 📝 이번 세션 자주 쓴 커맨드 패턴 (참고용)

```python
# 1. 파이썬 문법 체크 (반복 사용)
python -c "import ast; ast.parse(open('file.py').read()); print('OK')"

# 2. MCP 래퍼로 git push (규칙: 직접 git commit 금지)
python -c "from tools.git.git_manager import git_commit_and_push; print(git_commit_and_push('REPO', 'msg'))"

# 3. 도구 등록 수 확인
python count_tools.py

# 4. 특정 함수 유무 확인
grep -r "def function_name" src/tools/

# 5. 파일 라인 수 확인
python -c "print(len(open('file.py').readlines()))"
```

> **→ `python_runner` MCP 도구를 만들면 에이전트가 더 빠르게 검증 가능!**
