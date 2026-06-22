# Codebase Consolidation Report
- **Target Directory**: `C:\ameva\AMEVA-MCP-Toolkit-Utils`

## 1. Directory Structure
```text
- [Dir] .github/
  - [Dir] workflows/
    - [File] notify-ameva.yml
- [File] .gitignore
- [File] Dockerfile
- [File] MCP_IDEAS.md
- [File] README.md
- [File] count_tools.py
- [File] mcp_audit.jsonl
- [File] mcp_manifest.json
- [File] mcp_metadata_spec.md
- [Dir] output/
  - [File] codebase_consolidation.md
- [File] requirements.txt
- [Dir] src/
  - [File] README.md
  - [File] server.py
  - [Dir] tools/
    - [File] README.md
    - [Dir] database/
      - [File] README.md
      - [File] db_consolidator.py
    - [Dir] dataset/
      - [File] __init__.py
      - [File] dataset_aggregator.py
    - [Dir] docker/
      - [File] __init__.py
      - [File] docker_manager.py
    - [Dir] document/
      - [File] code_consolidator.py
      - [File] file_manager.py
      - [File] md_converter.py
    - [Dir] git/
      - [File] README.md
      - [File] __init__.py
      - [File] git_manager.py
    - [Dir] network/
      - [File] __init__.py
      - [File] net_discovery.py
    - [Dir] search/
      - [File] __init__.py
      - [File] code_searcher.py
    - [Dir] ssh/
      - [File] ssh_manager.py
    - [Dir] utils/
      - [File] README.md
      - [File] utils_manager.py
    - [Dir] web/
      - [File] crawl_bot.py
  - [Dir] utils/
    - [File] README.md
    - [File] __init__.py
    - [File] audit_logger.py
    - [File] view_stats.py
```

---

## 2. Database Schema
No SQLite databases detected in the directory.

---

## 3. Source Codes
### File: `count_tools.py`
```python
import re

with open('src/server.py', 'r', encoding='utf-8') as f:
    content = f.read()

tools = re.findall(r'@mcp\.tool\(name="([^"]+)"', content)
print(f'Total tools in server.py: {len(tools)}')
for i, t in enumerate(tools, 1):
    print(f'  {i:2d}. {t}')
```

---

### File: `MCP_IDEAS.md`
```markdown
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
```

---

### File: `mcp_manifest.json`
```json
{
  "version": "2.0",
  "name": "AMEVA Utils Toolkit",
  "repo": "uno-km/MCP-Utils-Toolkit",
  "description": "AMEVA 공식 MCP 도구 모음 — GitHub에서 직접 브라우저로 실행",
  "ntfy_channel": "uno-km-mcp-utils-toolkit",
  "tools": [
    {
      "name": "format_json",
      "description": "JSON 문자열을 파싱하고 보기 좋게 pretty-print합니다",
      "type": "python",
      "entry": "json.loads(__args__['json_string'])",
      "inline": "import json\ntry:\n    parsed = json.loads(__args__['json_string'])\n    print(json.dumps(parsed, indent=2, ensure_ascii=False))\nexcept Exception as e:\n    print(f'Error: {e}')",
      "inputSchema": {
        "type": "object",
        "properties": {
          "json_string": { "type": "string", "description": "포맷할 JSON 문자열" }
        },
        "required": ["json_string"]
      }
    },
    {
      "name": "base64_encode",
      "description": "텍스트를 Base64로 인코딩하거나 디코딩합니다",
      "type": "python",
      "inline": "import base64\nmode = __args__.get('mode', 'encode')\ndata = __args__['data']\ntry:\n    if mode == 'encode':\n        print(base64.b64encode(data.encode()).decode())\n    else:\n        print(base64.b64decode(data.encode()).decode())\nexcept Exception as e:\n    print(f'Error: {e}')",
      "inputSchema": {
        "type": "object",
        "properties": {
          "data": { "type": "string", "description": "인코딩/디코딩할 데이터" },
          "mode": { "type": "string", "description": "'encode' 또는 'decode'" }
        },
        "required": ["data"]
      }
    },
    {
      "name": "text_transform",
      "description": "텍스트를 변환합니다. mode: upper / lower / reverse / title / snake_case / count",
      "type": "python",
      "inline": "text = __args__['text']\nmode = __args__.get('mode', 'upper')\nif mode == 'upper': print(text.upper())\nelif mode == 'lower': print(text.lower())\nelif mode == 'reverse': print(text[::-1])\nelif mode == 'title': print(text.title())\nelif mode == 'snake_case': print('_'.join(text.lower().split()))\nelif mode == 'count': print(f'chars={len(text)}, words={len(text.split())}, lines={len(text.splitlines())}')\nelse: print(f'Unknown mode: {mode}')",
      "inputSchema": {
        "type": "object",
        "properties": {
          "text": { "type": "string", "description": "변환할 텍스트" },
          "mode": { "type": "string", "description": "upper|lower|reverse|title|snake_case|count" }
        },
        "required": ["text"]
      }
    },
    {
      "name": "calc",
      "description": "수식을 안전하게 계산합니다. 사칙연산, 지수, 나머지 등 기본 수식 지원.",
      "type": "python",
      "inline": "import math\nexpr = __args__['expression']\nallowed = set('0123456789+-*/().,** %')\nif all(c in allowed or c.isspace() for c in expr):\n    try:\n        result = eval(expr, {'__builtins__': {}, 'math': math, 'sqrt': math.sqrt, 'pi': math.pi, 'e': math.e})\n        print(f'{expr} = {result}')\n    except Exception as ex:\n        print(f'Error: {ex}')\nelse:\n    print('Error: Invalid expression. Only basic math allowed.')",
      "inputSchema": {
        "type": "object",
        "properties": {
          "expression": { "type": "string", "description": "계산할 수식 (예: '2 ** 10 + 3 * 4')" }
        },
        "required": ["expression"]
      }
    },
    {
      "name": "generate_uuid",
      "description": "랜덤 UUID v4를 생성합니다",
      "type": "python",
      "inline": "import uuid\ncount = int(__args__.get('count', 1))\nfor _ in range(min(count, 20)):\n    print(str(uuid.uuid4()))",
      "inputSchema": {
        "type": "object",
        "properties": {
          "count": { "type": "number", "description": "생성할 UUID 개수 (기본값: 1, 최대 20)" }
        },
        "required": []
      }
    },
    {
      "name": "timestamp_convert",
      "description": "Unix timestamp와 날짜 문자열을 상호 변환합니다",
      "type": "python",
      "inline": "from datetime import datetime, timezone\nimport time\nmode = __args__.get('mode', 'now')\nif mode == 'now':\n    ts = int(time.time())\n    dt = datetime.now(timezone.utc)\n    print(f'Unix: {ts}\\nUTC: {dt.strftime(\"%Y-%m-%d %H:%M:%S UTC\")}\\nLocal: {datetime.now().strftime(\"%Y-%m-%d %H:%M:%S\")}')\nelif mode == 'from_ts':\n    ts = int(__args__['value'])\n    print(datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))\nelif mode == 'to_ts':\n    dt = datetime.fromisoformat(__args__['value'])\n    print(int(dt.timestamp()))\nelse:\n    print('mode: now|from_ts|to_ts')",
      "inputSchema": {
        "type": "object",
        "properties": {
          "mode": { "type": "string", "description": "'now' (현재 시각) | 'from_ts' (ts→날짜) | 'to_ts' (날짜→ts)" },
          "value": { "type": "string", "description": "변환할 값 (from_ts: Unix timestamp 숫자, to_ts: ISO 날짜 문자열)" }
        },
        "required": []
      }
    },
    {
      "name": "hash_text",
      "description": "문자열의 해시값을 계산합니다. 알고리즘: md5, sha1, sha256, sha512",
      "type": "python",
      "inline": "import hashlib\ntext = __args__['text'].encode()\nalgo = __args__.get('algorithm', 'sha256')\ntry:\n    h = hashlib.new(algo)\n    h.update(text)\n    print(f'{algo.upper()}: {h.hexdigest()}')\nexcept Exception as e:\n    print(f'Error: {e}. Supported: md5, sha1, sha256, sha512')",
      "inputSchema": {
        "type": "object",
        "properties": {
          "text": { "type": "string", "description": "해시할 텍스트" },
          "algorithm": { "type": "string", "description": "해시 알고리즘: md5|sha1|sha256|sha512 (기본값: sha256)" }
        },
        "required": ["text"]
      }
    },
    {
      "name": "regex_match",
      "description": "정규표현식으로 텍스트에서 패턴을 검색합니다",
      "type": "python",
      "inline": "import re\npattern = __args__['pattern']\ntext = __args__['text']\nmode = __args__.get('mode', 'findall')\ntry:\n    if mode == 'findall':\n        matches = re.findall(pattern, text)\n        print(f'Found {len(matches)} match(es):\\n' + '\\n'.join(matches))\n    elif mode == 'match':\n        m = re.match(pattern, text)\n        print(f'Match: {m.group() if m else None}')\n    elif mode == 'sub':\n        repl = __args__.get('replacement', '')\n        print(re.sub(pattern, repl, text))\nexcept Exception as e:\n    print(f'Error: {e}')",
      "inputSchema": {
        "type": "object",
        "properties": {
          "pattern": { "type": "string", "description": "정규표현식 패턴" },
          "text": { "type": "string", "description": "검색할 텍스트" },
          "mode": { "type": "string", "description": "findall|match|sub (기본값: findall)" },
          "replacement": { "type": "string", "description": "sub 모드일 때 교체할 문자열" }
        },
        "required": ["pattern", "text"]
      }
    },
    {
      "name": "mermaid_to_png",
      "description": "Mermaid 다이어그램 코드를 해석하여 PNG 이미지 파일로 변환한 뒤 VFS 가상 디렉토리에 저장합니다.",
      "type": "js",
      "inline": "const mermaidCode = __args__.mermaid_code;\nconst outputPath = __args__.output_path || 'home/diagram.png';\nif (!mermaidCode) return 'Error: mermaid_code is required';\n\nif (typeof mermaid === 'undefined') {\n  await new Promise((resolve, reject) => {\n    const script = document.createElement('script');\n    script.src = 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js';\n    script.onload = () => {\n      mermaid.initialize({ startOnLoad: false });\n      resolve();\n    };\n    script.onerror = reject;\n    document.head.appendChild(script);\n  });\n}\n\nconst uniqueId = 'mermaid-' + Date.now();\nconst container = document.createElement('div');\ncontainer.style.visibility = 'hidden';\ncontainer.style.position = 'absolute';\ncontainer.id = uniqueId + '-container';\ndocument.body.appendChild(container);\n\nlet svgText;\ntry {\n  const { svg } = await mermaid.render(uniqueId, mermaidCode, container);\n  svgText = svg;\n} catch (err) {\n  container.remove();\n  return 'Mermaid Render Error: ' + err.message;\n}\ncontainer.remove();\n\nreturn await new Promise((resolve) => {\n  const img = new Image();\n  const svgBlob = new Blob([svgText], { type: 'image/svg+xml;charset=utf-8' });\n  const url = URL.createObjectURL(svgBlob);\n  \n  img.onload = () => {\n    const canvas = document.createElement('canvas');\n    const scale = 2;\n    canvas.width = img.naturalWidth * scale;\n    canvas.height = img.naturalHeight * scale;\n    \n    const ctx = canvas.getContext('2d');\n    ctx.fillStyle = 'white';\n    ctx.fillRect(0, 0, canvas.width, canvas.height);\n    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);\n    \n    URL.revokeObjectURL(url);\n    \n    try {\n      const pngDataUrl = canvas.toDataURL('image/png');\n      if (window.amevaOS && typeof window.amevaOS.writeFile === 'function') {\n        window.amevaOS.writeFile(outputPath, pngDataUrl);\n        resolve('Successfully rendered Mermaid to PNG and saved to VFS: ' + outputPath);\n      } else {\n        resolve('Rendered successfully (VFS write skipped): ' + pngDataUrl.substring(0, 60) + '...');\n      } \n    } catch (e) {\n      resolve('Canvas toDataURL conversion error: ' + e.message);\n    }\n  };\n  img.onerror = () => {\n    URL.revokeObjectURL(url);\n    resolve('Image load error during SVG conversion');\n  };\n  img.src = url;\n});",
      "inputSchema": {
        "type": "object",
        "properties": {
          "mermaid_code": { "type": "string", "description": "변환할 Mermaid 다이어그램 코드 문자열" },
          "output_path": { "type": "string", "description": "저장할 VFS 경로 (예: 'home/diagram.png')" }
        },
        "required": ["mermaid_code"]
      }
    },
    {
      "name": "md_to_docx",
      "description": "마크다운(.md) 파일을 MS 워드(.docx) 파일로 변환합니다.",
      "type": "python",
      "inline": "import sys\nimport os\nsys.path.append('/app/workspace/src/tools/document')\nimport md_converter\ntry:\n    res = md_converter.convert_md_to_docx_logic(__args__['input_md_path'], __args__['output_docx_path'])\n    print(res)\nexcept Exception as e:\n    print(f'Error: {e}')",
      "inputSchema": {
        "type": "object",
        "properties": {
          "input_md_path": { "type": "string", "description": "입력 마크다운 파일 경로" },
          "output_docx_path": { "type": "string", "description": "출력 DOCX 파일 경로" }
        },
        "required": ["input_md_path", "output_docx_path"]
      }
    },
    {
      "name": "docx_to_md",
      "description": "MS 워드(.docx) 파일을 마크다운(.md) 파일로 변환합니다.",
      "type": "python",
      "inline": "import sys\nimport os\nsys.path.append('/app/workspace/src/tools/document')\nimport md_converter\ntry:\n    res = md_converter.docx_to_markdown(__args__['docx_path'], __args__.get('output_md_path'))\n    print(res)\nexcept Exception as e:\n    print(f'Error: {e}')",
      "inputSchema": {
        "type": "object",
        "properties": {
          "docx_path": { "type": "string", "description": "입력 DOCX 파일 경로" },
          "output_md_path": { "type": "string", "description": "출력 마크다운 파일 경로 (생략 시 텍스트 반환)" }
        },
        "required": ["docx_path"]
      }
    },
    {
      "name": "consolidate_codebase",
      "description": "대상 디렉터리의 구조, 라이브러리를 제외한 전체 소스 코드, 그리고 존재하는 SQLite DB 스키마를 하나의 마크다운 파일로 병합 및 추출합니다.",
      "type": "python",
      "inline": "import sys\nimport os\nsys.path.append('/app/workspace/src/tools/document')\nimport code_consolidator\ntry:\n    res = code_consolidator.consolidate_codebase_logic(__args__['target_dir'], __args__.get('output_file'))\n    print(res)\nexcept Exception as e:\n    print(f'Error: {e}')",
      "inputSchema": {
        "type": "object",
        "properties": {
          "target_dir": { "type": "string", "description": "병합할 대상 디렉터리 경로" },
          "output_file": { "type": "string", "description": "저장할 마크다운 파일 경로 (생략 시 병합된 텍스트 반환)" }
        },
        "required": ["target_dir"]
      }
    }
  ]
}
```

---

### File: `mcp_metadata_spec.md`
```markdown
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
```

---

### File: `README.md`
```markdown
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
```

---

### File: `requirements.txt`
```
mcp>=1.0.0
python-docx>=1.1.0
paramiko>=3.4.0
beautifulsoup4>=4.12.0
psutil>=5.9.0
requests>=2.31.0

```

---

### File: `.github/workflows/notify-ameva.yml`
```yaml
name: Notify AMEVA OS on Push

on:
  push:
    branches:
      - main

jobs:
  notify-ameva-hub:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Get commit info
        id: info
        run: |
          echo "sha=${GITHUB_SHA::7}" >> $GITHUB_OUTPUT
          echo "msg=$(git log -1 --pretty='%s')" >> $GITHUB_OUTPUT
          echo "author=$(git log -1 --pretty='%an')" >> $GITHUB_OUTPUT
          echo "ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $GITHUB_OUTPUT

      - name: Push update signal to ntfy.sh
        run: |
          curl -s \
            -H "Title: MCP-Utils-Toolkit Updated" \
            -H "Priority: default" \
            -H "Tags: arrow_up,package" \
            -H "X-Commit: ${{ steps.info.outputs.sha }}" \
            -H "X-Message: ${{ steps.info.outputs.msg }}" \
            -H "X-Author: ${{ steps.info.outputs.author }}" \
            -H "X-Timestamp: ${{ steps.info.outputs.ts }}" \
            -d "${{ steps.info.outputs.sha }}|${{ steps.info.outputs.msg }}|${{ steps.info.outputs.author }}|${{ steps.info.outputs.ts }}" \
            https://ntfy.sh/uno-km-mcp-utils-toolkit

      - name: Log
        run: |
          echo "✅ AMEVA OS Hub notified."
          echo "   Commit : ${{ steps.info.outputs.sha }}"
          echo "   Message: ${{ steps.info.outputs.msg }}"
```

---

### File: `output/codebase_consolidation.md`
```markdown
# Codebase Consolidation Report
- **Target Directory**: `C:\ameva\AMEVA-MCP-Toolkit-Utils`

## 1. Directory Structure
```text
- [Dir] .github/
  - [Dir] workflows/
    - [File] notify-ameva.yml
- [File] .gitignore
- [File] Dockerfile
- [File] MCP_IDEAS.md
- [File] README.md
- [File] count_tools.py
- [File] mcp_audit.jsonl
- [File] mcp_manifest.json
- [File] mcp_metadata_spec.md
- [File] requirements.txt
- [Dir] src/
  - [File] README.md
  - [File] server.py
  - [Dir] tools/
    - [File] README.md
    - [Dir] database/
      - [File] README.md
      - [File] db_consolidator.py
    - [Dir] dataset/
      - [File] __init__.py
      - [File] dataset_aggregator.py
    - [Dir] docker/
      - [File] __init__.py
      - [File] docker_manager.py
    - [Dir] document/
      - [File] code_consolidator.py
      - [File] file_manager.py
      - [File] md_converter.py
    - [Dir] git/
      - [File] README.md
      - [File] __init__.py
      - [File] git_manager.py
    - [Dir] network/
      - [File] __init__.py
      - [File] net_discovery.py
    - [Dir] search/
      - [File] __init__.py
      - [File] code_searcher.py
    - [Dir] ssh/
      - [File] ssh_manager.py
    - [Dir] utils/
      - [File] README.md
      - [File] utils_manager.py
    - [Dir] web/
      - [File] crawl_bot.py
  - [Dir] utils/
    - [File] README.md
    - [File] __init__.py
    - [File] audit_logger.py
    - [File] view_stats.py
```

---

## 2. Database Schema
No SQLite databases detected in the directory.

---

## 3. Source Codes
### File: `count_tools.py`
```python
import re

with open('src/server.py', 'r', encoding='utf-8') as f:
    content = f.read()

tools = re.findall(r'@mcp\.tool\(name="([^"]+)"', content)
print(f'Total tools in server.py: {len(tools)}')
for i, t in enumerate(tools, 1):
    print(f'  {i:2d}. {t}')
```

---

### File: `MCP_IDEAS.md`
```markdown
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
```

---

### File: `mcp_manifest.json`
```json
{
  "version": "2.0",
  "name": "AMEVA Utils Toolkit",
  "repo": "uno-km/MCP-Utils-Toolkit",
  "description": "AMEVA 공식 MCP 도구 모음 — GitHub에서 직접 브라우저로 실행",
  "ntfy_channel": "uno-km-mcp-utils-toolkit",
  "tools": [
    {
      "name": "format_json",
      "description": "JSON 문자열을 파싱하고 보기 좋게 pretty-print합니다",
      "type": "python",
      "entry": "json.loads(__args__['json_string'])",
      "inline": "import json\ntry:\n    parsed = json.loads(__args__['json_string'])\n    print(json.dumps(parsed, indent=2, ensure_ascii=False))\nexcept Exception as e:\n    print(f'Error: {e}')",
      "inputSchema": {
        "type": "object",
        "properties": {
          "json_string": { "type": "string", "description": "포맷할 JSON 문자열" }
        },
        "required": ["json_string"]
      }
    },
    {
      "name": "base64_encode",
      "description": "텍스트를 Base64로 인코딩하거나 디코딩합니다",
      "type": "python",
      "inline": "import base64\nmode = __args__.get('mode', 'encode')\ndata = __args__['data']\ntry:\n    if mode == 'encode':\n        print(base64.b64encode(data.encode()).decode())\n    else:\n        print(base64.b64decode(data.encode()).decode())\nexcept Exception as e:\n    print(f'Error: {e}')",
      "inputSchema": {
        "type": "object",
        "properties": {
          "data": { "type": "string", "description": "인코딩/디코딩할 데이터" },
          "mode": { "type": "string", "description": "'encode' 또는 'decode'" }
        },
        "required": ["data"]
      }
    },
    {
      "name": "text_transform",
      "description": "텍스트를 변환합니다. mode: upper / lower / reverse / title / snake_case / count",
      "type": "python",
      "inline": "text = __args__['text']\nmode = __args__.get('mode', 'upper')\nif mode == 'upper': print(text.upper())\nelif mode == 'lower': print(text.lower())\nelif mode == 'reverse': print(text[::-1])\nelif mode == 'title': print(text.title())\nelif mode == 'snake_case': print('_'.join(text.lower().split()))\nelif mode == 'count': print(f'chars={len(text)}, words={len(text.split())}, lines={len(text.splitlines())}')\nelse: print(f'Unknown mode: {mode}')",
      "inputSchema": {
        "type": "object",
        "properties": {
          "text": { "type": "string", "description": "변환할 텍스트" },
          "mode": { "type": "string", "description": "upper|lower|reverse|title|snake_case|count" }
        },
        "required": ["text"]
      }
    },
    {
      "name": "calc",
      "description": "수식을 안전하게 계산합니다. 사칙연산, 지수, 나머지 등 기본 수식 지원.",
      "type": "python",
      "inline": "import math\nexpr = __args__['expression']\nallowed = set('0123456789+-*/().,** %')\nif all(c in allowed or c.isspace() for c in expr):\n    try:\n        result = eval(expr, {'__builtins__': {}, 'math': math, 'sqrt': math.sqrt, 'pi': math.pi, 'e': math.e})\n        print(f'{expr} = {result}')\n    except Exception as ex:\n        print(f'Error: {ex}')\nelse:\n    print('Error: Invalid expression. Only basic math allowed.')",
      "inputSchema": {
        "type": "object",
        "properties": {
          "expression": { "type": "string", "description": "계산할 수식 (예: '2 ** 10 + 3 * 4')" }
        },
        "required": ["expression"]
      }
    },
    {
      "name": "generate_uuid",
      "description": "랜덤 UUID v4를 생성합니다",
      "type": "python",
      "inline": "import uuid\ncount = int(__args__.get('count', 1))\nfor _ in range(min(count, 20)):\n    print(str(uuid.uuid4()))",
      "inputSchema": {
        "type": "object",
        "properties": {
          "count": { "type": "number", "description": "생성할 UUID 개수 (기본값: 1, 최대 20)" }
        },
        "required": []
      }
    },
    {
      "name": "timestamp_convert",
      "description": "Unix timestamp와 날짜 문자열을 상호 변환합니다",
      "type": "python",
      "inline": "from datetime import datetime, timezone\nimport time\nmode = __args__.get('mode', 'now')\nif mode == 'now':\n    ts = int(time.time())\n    dt = datetime.now(timezone.utc)\n    print(f'Unix: {ts}\\nUTC: {dt.strftime(\"%Y-%m-%d %H:%M:%S UTC\")}\\nLocal: {datetime.now().strftime(\"%Y-%m-%d %H:%M:%S\")}')\nelif mode == 'from_ts':\n    ts = int(__args__['value'])\n    print(datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))\nelif mode == 'to_ts':\n    dt = datetime.fromisoformat(__args__['value'])\n    print(int(dt.timestamp()))\nelse:\n    print('mode: now|from_ts|to_ts')",
      "inputSchema": {
        "type": "object",
        "properties": {
          "mode": { "type": "string", "description": "'now' (현재 시각) | 'from_ts' (ts→날짜) | 'to_ts' (날짜→ts)" },
          "value": { "type": "string", "description": "변환할 값 (from_ts: Unix timestamp 숫자, to_ts: ISO 날짜 문자열)" }
        },
        "required": []
      }
    },
    {
      "name": "hash_text",
      "description": "문자열의 해시값을 계산합니다. 알고리즘: md5, sha1, sha256, sha512",
      "type": "python",
      "inline": "import hashlib\ntext = __args__['text'].encode()\nalgo = __args__.get('algorithm', 'sha256')\ntry:\n    h = hashlib.new(algo)\n    h.update(text)\n    print(f'{algo.upper()}: {h.hexdigest()}')\nexcept Exception as e:\n    print(f'Error: {e}. Supported: md5, sha1, sha256, sha512')",
      "inputSchema": {
        "type": "object",
        "properties": {
          "text": { "type": "string", "description": "해시할 텍스트" },
          "algorithm": { "type": "string", "description": "해시 알고리즘: md5|sha1|sha256|sha512 (기본값: sha256)" }
        },
        "required": ["text"]
      }
    },
    {
      "name": "regex_match",
      "description": "정규표현식으로 텍스트에서 패턴을 검색합니다",
      "type": "python",
      "inline": "import re\npattern = __args__['pattern']\ntext = __args__['text']\nmode = __args__.get('mode', 'findall')\ntry:\n    if mode == 'findall':\n        matches = re.findall(pattern, text)\n        print(f'Found {len(matches)} match(es):\\n' + '\\n'.join(matches))\n    elif mode == 'match':\n        m = re.match(pattern, text)\n        print(f'Match: {m.group() if m else None}')\n    elif mode == 'sub':\n        repl = __args__.get('replacement', '')\n        print(re.sub(pattern, repl, text))\nexcept Exception as e:\n    print(f'Error: {e}')",
      "inputSchema": {
        "type": "object",
        "properties": {
          "pattern": { "type": "string", "description": "정규표현식 패턴" },
          "text": { "type": "string", "description": "검색할 텍스트" },
          "mode": { "type": "string", "description": "findall|match|sub (기본값: findall)" },
          "replacement": { "type": "string", "description": "sub 모드일 때 교체할 문자열" }
        },
        "required": ["pattern", "text"]
      }
    },
    {
      "name": "mermaid_to_png",
      "description": "Mermaid 다이어그램 코드를 해석하여 PNG 이미지 파일로 변환한 뒤 VFS 가상 디렉토리에 저장합니다.",
      "type": "js",
      "inline": "const mermaidCode = __args__.mermaid_code;\nconst outputPath = __args__.output_path || 'home/diagram.png';\nif (!mermaidCode) return 'Error: mermaid_code is required';\n\nif (typeof mermaid === 'undefined') {\n  await new Promise((resolve, reject) => {\n    const script = document.createElement('script');\n    script.src = 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js';\n    script.onload = () => {\n      mermaid.initialize({ startOnLoad: false });\n      resolve();\n    };\n    script.onerror = reject;\n    document.head.appendChild(script);\n  });\n}\n\nconst uniqueId = 'mermaid-' + Date.now();\nconst container = document.createElement('div');\ncontainer.style.visibility = 'hidden';\ncontainer.style.position = 'absolute';\ncontainer.id = uniqueId + '-container';\ndocument.body.appendChild(container);\n\nlet svgText;\ntry {\n  const { svg } = await mermaid.render(uniqueId, mermaidCode, container);\n  svgText = svg;\n} catch (err) {\n  container.remove();\n  return 'Mermaid Render Error: ' + err.message;\n}\ncontainer.remove();\n\nreturn await new Promise((resolve) => {\n  const img = new Image();\n  const svgBlob = new Blob([svgText], { type: 'image/svg+xml;charset=utf-8' });\n  const url = URL.createObjectURL(svgBlob);\n  \n  img.onload = () => {\n    const canvas = document.createElement('canvas');\n    const scale = 2;\n    canvas.width = img.naturalWidth * scale;\n    canvas.height = img.naturalHeight * scale;\n    \n    const ctx = canvas.getContext('2d');\n    ctx.fillStyle = 'white';\n    ctx.fillRect(0, 0, canvas.width, canvas.height);\n    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);\n    \n    URL.revokeObjectURL(url);\n    \n    try {\n      const pngDataUrl = canvas.toDataURL('image/png');\n      if (window.amevaOS && typeof window.amevaOS.writeFile === 'function') {\n        window.amevaOS.writeFile(outputPath, pngDataUrl);\n        resolve('Successfully rendered Mermaid to PNG and saved to VFS: ' + outputPath);\n      } else {\n        resolve('Rendered successfully (VFS write skipped): ' + pngDataUrl.substring(0, 60) + '...');\n      } \n    } catch (e) {\n      resolve('Canvas toDataURL conversion error: ' + e.message);\n    }\n  };\n  img.onerror = () => {\n    URL.revokeObjectURL(url);\n    resolve('Image load error during SVG conversion');\n  };\n  img.src = url;\n});",
      "inputSchema": {
        "type": "object",
        "properties": {
          "mermaid_code": { "type": "string", "description": "변환할 Mermaid 다이어그램 코드 문자열" },
          "output_path": { "type": "string", "description": "저장할 VFS 경로 (예: 'home/diagram.png')" }
        },
        "required": ["mermaid_code"]
      }
    },
    {
      "name": "md_to_docx",
      "description": "마크다운(.md) 파일을 MS 워드(.docx) 파일로 변환합니다.",
      "type": "python",
      "inline": "import sys\nimport os\nsys.path.append('/app/workspace/src/tools/document')\nimport md_converter\ntry:\n    res = md_converter.convert_md_to_docx_logic(__args__['input_md_path'], __args__['output_docx_path'])\n    print(res)\nexcept Exception as e:\n    print(f'Error: {e}')",
      "inputSchema": {
        "type": "object",
        "properties": {
          "input_md_path": { "type": "string", "description": "입력 마크다운 파일 경로" },
          "output_docx_path": { "type": "string", "description": "출력 DOCX 파일 경로" }
        },
        "required": ["input_md_path", "output_docx_path"]
      }
    },
    {
      "name": "docx_to_md",
      "description": "MS 워드(.docx) 파일을 마크다운(.md) 파일로 변환합니다.",
      "type": "python",
      "inline": "import sys\nimport os\nsys.path.append('/app/workspace/src/tools/document')\nimport md_converter\ntry:\n    res = md_converter.docx_to_markdown(__args__['docx_path'], __args__.get('output_md_path'))\n    print(res)\nexcept Exception as e:\n    print(f'Error: {e}')",
      "inputSchema": {
        "type": "object",
        "properties": {
          "docx_path": { "type": "string", "description": "입력 DOCX 파일 경로" },
          "output_md_path": { "type": "string", "description": "출력 마크다운 파일 경로 (생략 시 텍스트 반환)" }
        },
        "required": ["docx_path"]
      }
    },
    {
      "name": "consolidate_codebase",
      "description": "대상 디렉터리의 구조, 라이브러리를 제외한 전체 소스 코드, 그리고 존재하는 SQLite DB 스키마를 하나의 마크다운 파일로 병합 및 추출합니다.",
      "type": "python",
      "inline": "import sys\nimport os\nsys.path.append('/app/workspace/src/tools/document')\nimport code_consolidator\ntry:\n    res = code_consolidator.consolidate_codebase_logic(__args__['target_dir'], __args__.get('output_file'))\n    print(res)\nexcept Exception as e:\n    print(f'Error: {e}')",
      "inputSchema": {
        "type": "object",
        "properties": {
          "target_dir": { "type": "string", "description": "병합할 대상 디렉터리 경로" },
          "output_file": { "type": "string", "description": "저장할 마크다운 파일 경로 (생략 시 병합된 텍스트 반환)" }
        },
        "required": ["target_dir"]
      }
    }
  ]
}
```

---

### File: `mcp_metadata_spec.md`
```markdown
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
```

---

### File: `README.md`
```markdown
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
```

---

### File: `requirements.txt`
```
mcp>=1.0.0
python-docx>=1.1.0
paramiko>=3.4.0
beautifulsoup4>=4.12.0
psutil>=5.9.0
requests>=2.31.0

```

---

### File: `.github/workflows/notify-ameva.yml`
```yaml
name: Notify AMEVA OS on Push

on:
  push:
    branches:
      - main

jobs:
  notify-ameva-hub:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Get commit info
        id: info
        run: |
          echo "sha=${GITHUB_SHA::7}" >> $GITHUB_OUTPUT
          echo "msg=$(git log -1 --pretty='%s')" >> $GITHUB_OUTPUT
          echo "author=$(git log -1 --pretty='%an')" >> $GITHUB_OUTPUT
          echo "ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $GITHUB_OUTPUT

      - name: Push update signal to ntfy.sh
        run: |
          curl -s \
            -H "Title: MCP-Utils-Toolkit Updated" \
            -H "Priority: default" \
            -H "Tags: arrow_up,package" \
            -H "X-Commit: ${{ steps.info.outputs.sha }}" \
            -H "X-Message: ${{ steps.info.outputs.msg }}" \
            -H "X-Author: ${{ steps.info.outputs.author }}" \
            -H "X-Timestamp: ${{ steps.info.outputs.ts }}" \
            -d "${{ steps.info.outputs.sha }}|${{ steps.info.outputs.msg }}|${{ steps.info.outputs.author }}|${{ steps.info.outputs.ts }}" \
            https://ntfy.sh/uno-km-mcp-utils-toolkit

      - name: Log
        run: |
          echo "✅ AMEVA OS Hub notified."
          echo "   Commit : ${{ steps.info.outputs.sha }}"
          echo "   Message: ${{ steps.info.outputs.msg }}"
```

---

### File: `src/README.md`
```markdown
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
```

---

### File: `src/server.py`
```python
from mcp.server.fastmcp import FastMCP
from tools.document.file_manager import docker_delete_file, docker_move_file
from tools.document.md_converter import convert_md_to_docx_logic, docx_to_markdown, md_image_path_fixer
from tools.document.code_consolidator import consolidate_codebase_logic
from tools.git import git_manager
from tools.ssh import ssh_manager
from tools.utils import utils_manager
from tools.web import crawl_bot
from tools.database import db_consolidator
from tools.docker import docker_manager
from tools.dataset import dataset_aggregator
from tools.search import code_searcher
from tools.network import net_discovery
from utils.audit_logger import log_mcp_action

def create_server() -> FastMCP:
    """
    서버 초기화 및 도구 등록을 담당하는 진입점.
    비즈니스 로직은 src/tools 하위의 모듈에서 가져와 연결만 합니다.
    """
    mcp = FastMCP("AMEVA_Toolkit_Utils")

    # ──────────────────────────────────────────────────────────────────
    # Document & File Tools
    # ──────────────────────────────────────────────────────────────────

    @mcp.tool(name="consolidate_codebase", description="Consolidate target directory codebase into a single Markdown file containing directory structure, SQLite DB schemas, and source code contents.")
    def tool_consolidate_codebase(target_dir: str, output_file: str = None) -> str:
        res = consolidate_codebase_logic(target_dir, output_file)
        log_mcp_action("consolidate_codebase", {"target_dir": target_dir, "output_file": output_file}, res if len(res) < 1000 else f"Consolidated report ({len(res)} characters)")
        return res

    @mcp.tool(name="convert_md_to_docx", description="Convert Markdown file to Word DOCX format. Supports headings, bullets, code blocks, bold, numbered lists.")
    def tool_md_to_docx(input_md_path: str, output_docx_path: str) -> str:
        res = convert_md_to_docx_logic(input_md_path, output_docx_path)
        log_mcp_action("convert_md_to_docx", {"input": input_md_path, "output": output_docx_path}, res)
        return res

    @mcp.tool(name="docx_to_markdown", description="Convert a Word DOCX file to structured Markdown. Parses headings, lists, bold/italic, and tables. Set output_md_path to save to file, or leave empty to return text directly.")
    def tool_docx_to_markdown(docx_path: str, output_md_path: str = None) -> str:
        res = docx_to_markdown(docx_path, output_md_path)
        log_mcp_action("docx_to_markdown", {"docx_path": docx_path, "output": output_md_path}, res)
        return res

    @mcp.tool(name="md_image_path_fixer", description="Scan a Markdown file for broken image paths and auto-fix them by searching the base_image_dir for matching filenames.")
    def tool_md_image_path_fixer(doc_path: str, base_image_dir: str) -> str:
        res = md_image_path_fixer(doc_path, base_image_dir)
        log_mcp_action("md_image_path_fixer", {"doc_path": doc_path, "base_image_dir": base_image_dir}, res)
        return res

    @mcp.tool(name="delete_file_in_docker", description="Delete a file inside the Docker container")
    def tool_delete_file_in_docker(file_path: str) -> str:
        res = docker_delete_file(file_path)
        log_mcp_action("delete_file_in_docker", {"file_path": file_path}, res)
        return res

    @mcp.tool(name="move_file_in_docker", description="Move/rename a file inside the Docker container")
    def tool_move_file_in_docker(src_path: str, dest_path: str) -> str:
        res = docker_move_file(src_path, dest_path)
        log_mcp_action("move_file_in_docker", {"src_path": src_path, "dest_path": dest_path}, res)
        return res

    # ──────────────────────────────────────────────────────────────────
    # Git & SSH Tools
    # ──────────────────────────────────────────────────────────────────

    @mcp.tool(name="git_status", description="Get the git status of a repository (e.g., AMEVA-Doc-AI)")
    def tool_git_status(repo_name: str) -> str:
        res = git_manager.git_status(repo_name)
        log_mcp_action("git_status", {"repo": repo_name}, res)
        return res

    @mcp.tool(name="git_pull", description="Pull the latest changes for a repository")
    def tool_git_pull(repo_name: str) -> str:
        res = git_manager.git_pull(repo_name)
        log_mcp_action("git_pull", {"repo": repo_name}, res)
        return res

    @mcp.tool(name="git_commit_and_push", description="Stage all changes, commit with a message, and push for a repository")
    def tool_git_commit_and_push(repo_name: str, commit_message: str) -> str:
        res = git_manager.git_commit_and_push(repo_name, commit_message)
        log_mcp_action("git_commit_and_push", {"repo": repo_name, "msg": commit_message}, res)
        return res

    @mcp.tool(name="git_clone", description="Clone a remote git repository to the local system under the specified folder name")
    def tool_git_clone(repo_url: str, repo_name: str) -> str:
        res = git_manager.git_clone(repo_url, repo_name)
        log_mcp_action("git_clone", {"url": repo_url, "repo_name": repo_name}, res)
        return res

    @mcp.tool(name="git_log", description="Get the git commit log/history (e.g. limit=10 commits)")
    def tool_git_log(repo_name: str, limit: int = 10) -> str:
        res = git_manager.git_log(repo_name, limit)
        log_mcp_action("git_log", {"repo": repo_name, "limit": limit}, res)
        return res

    @mcp.tool(name="git_diff", description="Get git diff comparison of modified files in working directory")
    def tool_git_diff(repo_name: str, file_path: str = None) -> str:
        res = git_manager.git_diff(repo_name, file_path)
        log_mcp_action("git_diff", {"repo": repo_name, "file_path": file_path}, res)
        return res

    @mcp.tool(name="git_branch", description="Manage git branches. action can be: 'list', 'new', 'delete'")
    def tool_git_branch(repo_name: str, action: str = "list", branch_name: str = None) -> str:
        res = git_manager.git_branch(repo_name, action, branch_name)
        log_mcp_action("git_branch", {"repo": repo_name, "action": action, "branch_name": branch_name}, res)
        return res

    @mcp.tool(name="git_checkout", description="Checkout branch or restore files. Set create=True to create a new branch (-b)")
    def tool_git_checkout(repo_name: str, branch_or_file: str, create: bool = False) -> str:
        res = git_manager.git_checkout(repo_name, branch_or_file, create)
        log_mcp_action("git_checkout", {"repo": repo_name, "target": branch_or_file, "create": create}, res)
        return res

    @mcp.tool(name="git_merge", description="Merge a specified branch into the current branch")
    def tool_git_merge(repo_name: str, branch_name: str) -> str:
        res = git_manager.git_merge(repo_name, branch_name)
        log_mcp_action("git_merge", {"repo": repo_name, "branch": branch_name}, res)
        return res

    @mcp.tool(name="git_reset", description="Reset current HEAD to a state. mode: 'soft', 'mixed', 'hard'")
    def tool_git_reset(repo_name: str, mode: str = "mixed", commit_hash: str = "HEAD") -> str:
        res = git_manager.git_reset(repo_name, mode, commit_hash)
        log_mcp_action("git_reset", {"repo": repo_name, "mode": mode, "commit": commit_hash}, res)
        return res

    @mcp.tool(name="git_stash", description="Stash local changes. action: 'push', 'pop', 'list', 'apply', 'clear'")
    def tool_git_stash(repo_name: str, action: str = "push", stash_id: str = None) -> str:
        res = git_manager.git_stash(repo_name, action, stash_id)
        log_mcp_action("git_stash", {"repo": repo_name, "action": action, "stash_id": stash_id}, res)
        return res

    @mcp.tool(name="workspace_git_broadcaster", description="Scan all AMEVA repositories under C:\\ameva and report each repo's branch, ahead/behind status, and changed file count in one consolidated table.")
    def tool_workspace_git_broadcaster() -> str:
        res = git_manager.workspace_git_broadcaster()
        log_mcp_action("workspace_git_broadcaster", {}, res)
        return res

    @mcp.tool(name="git_commit_helper", description="Analyze staged git diff and auto-generate Conventional Commits message suggestions (feat/fix/docs/chore etc.) for the specified repository.")
    def tool_git_commit_helper(repo_name: str) -> str:
        res = git_manager.git_commit_helper(repo_name)
        log_mcp_action("git_commit_helper", {"repo": repo_name}, res)
        return res

    @mcp.tool(name="ssh_run_command", description="Run a shell command on a remote server via SSH")
    def tool_ssh_run_command(host: str, username: str, command: str, port: int = 22, password: str = None, key_content: str = None) -> str:
        res = ssh_manager.ssh_run_command(host, username, command, port, password, key_content)
        log_mcp_action("ssh_run_command", {"host": host, "username": username, "command": command, "port": port}, res)
        return res

    # ──────────────────────────────────────────────────────────────────
    # Web Crawling & Readability
    # ──────────────────────────────────────────────────────────────────

    @mcp.tool(name="crawl_website", description="Crawls a website URL, extracts title, text content, and analyzes internal/external links")
    def tool_crawl_website(url: str, selector: str = None) -> str:
        res = crawl_bot.crawl_website(url, selector)
        log_mcp_action("crawl_website", {"url": url, "selector": selector}, res)
        return res

    @mcp.tool(name="web_readability_cleaner", description="Extract clean readable content from a URL by stripping ads, navigation, sidebars and converting to Markdown.")
    def tool_web_readability_cleaner(url: str) -> str:
        res = crawl_bot.web_readability_cleaner(url)
        log_mcp_action("web_readability_cleaner", {"url": url}, res)
        return res

    @mcp.tool(name="dead_link_scanner", description="Parse all URLs inside a Markdown file and check each one via HTTP HEAD request to identify 404 dead links.")
    def tool_dead_link_scanner(md_file_path: str) -> str:
        res = crawl_bot.dead_link_scanner(md_file_path)
        log_mcp_action("dead_link_scanner", {"md_file_path": md_file_path}, res)
        return res

    # ──────────────────────────────────────────────────────────────────
    # Database Centralization & Operations
    # ──────────────────────────────────────────────────────────────────

    @mcp.tool(name="db_get_schema", description="Get the schema (tables, columns, SQL) of a SQLite database")
    def tool_db_get_schema(db_path: str) -> str:
        res = db_consolidator.db_get_schema(db_path)
        log_mcp_action("db_get_schema", {"db_path": db_path}, res)
        return res

    @mcp.tool(name="db_execute_query", description="Execute a SQLite query safely. Modifying queries are blocked if read_only=True. output_format: markdown | json | csv | html | xml | plain")
    def tool_db_execute_query(db_path: str, query: str, read_only: bool = True, output_format: str = "markdown", client_token: str = None) -> str:
        res = db_consolidator.db_execute_query(db_path, query, read_only, output_format, client_token)
        log_mcp_action("db_execute_query", {"db_path": db_path, "query": query, "read_only": read_only, "output_format": output_format, "client_token": client_token}, res)
        return res

    @mcp.tool(name="db_merge_tables", description="Merge table records from source SQLite DB into destination SQLite DB using a unique key column")
    def tool_db_merge_tables(src_db: str, dest_db: str, table_name: str, key_column: str, client_token: str = None) -> str:
        res = db_consolidator.db_merge_tables(src_db, dest_db, table_name, key_column, client_token)
        log_mcp_action("db_merge_tables", {"src_db": src_db, "dest_db": dest_db, "table_name": table_name, "key_column": key_column, "client_token": client_token}, res)
        return res

    @mcp.tool(name="db_generate_erd", description="Generate a copy-pasteable Mermaid ER Diagram of a SQLite database schema")
    def tool_db_generate_erd(db_path: str) -> str:
        res = db_consolidator.db_generate_erd(db_path)
        log_mcp_action("db_generate_erd", {"db_path": db_path}, res)
        return res

    @mcp.tool(name="db_generate_mock_data", description="Generate realistic mock data and insert it into a table respecting foreign keys")
    def tool_db_generate_mock_data(db_path: str, table_name: str, count: int = 50, client_token: str = None) -> str:
        res = db_consolidator.db_generate_mock_data(db_path, table_name, count, client_token)
        log_mcp_action("db_generate_mock_data", {"db_path": db_path, "table_name": table_name, "count": count, "client_token": client_token}, res)
        return res

    @mcp.tool(name="db_global_search_value", description="Search for a specific string value across all text columns of all tables in the database")
    def tool_db_global_search_value(db_path: str, search_query: str) -> str:
        res = db_consolidator.db_global_search_value(db_path, search_query)
        log_mcp_action("db_global_search_value", {"db_path": db_path, "search_query": search_query}, res)
        return res

    @mcp.tool(name="db_transpile_sqlite_to_other", description="Transpile SQLite schema and data into PostgreSQL or MySQL DDL/DML script")
    def tool_db_transpile_sqlite_to_other(db_path: str, target_dialect: str) -> str:
        res = db_consolidator.db_transpile_sqlite_to_other(db_path, target_dialect)
        log_mcp_action("db_transpile_sqlite_to_other", {"db_path": db_path, "target_dialect": target_dialect}, res)
        return res

    @mcp.tool(name="db_profile_and_scan_health", description="Scan database health: analyze indices, verify referential integrity, detect outliers")
    def tool_db_profile_and_scan_health(db_path: str) -> str:
        res = db_consolidator.db_profile_and_scan_health(db_path)
        log_mcp_action("db_profile_and_scan_health", {"db_path": db_path}, res)
        return res

    @mcp.tool(name="db_format_sql", description="Beautify, uppercase keywords, and format raw SQL query for better readability")
    def tool_db_format_sql(query: str) -> str:
        res = db_consolidator.db_format_sql(query)
        log_mcp_action("db_format_sql", {"query": query}, res)
        return res

    @mcp.tool(name="db_compare_schemas", description="Compare schemas of two databases and generate missing DDL synchronization script")
    def tool_db_compare_schemas(src_db: str, dest_db: str) -> str:
        res = db_consolidator.db_compare_schemas(src_db, dest_db)
        log_mcp_action("db_compare_schemas", {"src_db": src_db, "dest_db": dest_db}, res)
        return res

    @mcp.tool(name="db_mask_table_data", description="Anonymize/mask sensitive table columns (GDPR-compliant email, name, phone masking)")
    def tool_db_mask_table_data(db_path: str, table_name: str, mask_rules_json: str, client_token: str = None) -> str:
        res = db_consolidator.db_mask_table_data(db_path, table_name, mask_rules_json, client_token)
        log_mcp_action("db_mask_table_data", {"db_path": db_path, "table_name": table_name, "mask_rules_json": mask_rules_json, "client_token": client_token}, res)
        return res

    @mcp.tool(name="db_unmask_table_data", description="Restore previously masked columns using shadow table or unmask_rules. Requires write client_token. unmask_rules_json: {\"col\": {\"mask_type\": \"static\", \"original_value\": \"...\"}}")
    def tool_db_unmask_table_data(db_path: str, table_name: str, unmask_rules_json: str, client_token: str = None) -> str:
        res = db_consolidator.db_unmask_table_data(db_path, table_name, unmask_rules_json, client_token)
        log_mcp_action("db_unmask_table_data", {"db_path": db_path, "table_name": table_name, "client_token": client_token}, res)
        return res

    @mcp.tool(name="db_sync_connector", description="Bulk sync a table from one SQLite DB to another. Creates table if missing, upserts rows. Requires write client_token.")
    def tool_db_sync_connector(src_db: str, dest_db: str, table_name: str, client_token: str = None) -> str:
        res = db_consolidator.db_sync_connector(src_db, dest_db, table_name, client_token)
        log_mcp_action("db_sync_connector", {"src_db": src_db, "dest_db": dest_db, "table_name": table_name, "client_token": client_token}, res)
        return res

    @mcp.tool(name="db_optimize_query_tuning", description="Analyze SQL query and suggest optimal missing CREATE INDEX index statements")
    def tool_db_optimize_query_tuning(db_path: str, slow_query: str) -> str:
        res = db_consolidator.db_optimize_query_tuning(db_path, slow_query)
        log_mcp_action("db_optimize_query_tuning", {"db_path": db_path, "slow_query": slow_query}, res)
        return res

    @mcp.tool(name="db_enable_time_travel", description="Enable historical change logs (shadow ledger table + triggers) on a table")
    def tool_db_enable_time_travel(db_path: str, table_name: str, client_token: str = None) -> str:
        res = db_consolidator.db_enable_time_travel(db_path, table_name, client_token)
        log_mcp_action("db_enable_time_travel", {"db_path": db_path, "table_name": table_name, "client_token": client_token}, res)
        return res

    @mcp.tool(name="db_restore_time_travel", description="Restore table data state back to a specific timestamp in the past")
    def tool_db_restore_time_travel(db_path: str, table_name: str, target_timestamp: str, client_token: str = None) -> str:
        res = db_consolidator.db_restore_time_travel(db_path, table_name, target_timestamp, client_token)
        log_mcp_action("db_restore_time_travel", {"db_path": db_path, "table_name": table_name, "target_timestamp": target_timestamp, "client_token": client_token}, res)
        return res

    @mcp.tool(name="db_view_table_data", description="Browse and query table data with paging, sorting, filtering, and custom output formatting (markdown, json, csv, html, xml, plain)")
    def tool_db_view_table_data(db_path: str, table_name: str, limit: int = 50, offset: int = 0, sort_by: str = None, sort_order: str = "DESC", filter_conditions: str = None, output_format: str = "markdown") -> str:
        res = db_consolidator.db_view_table_data(db_path, table_name, limit, offset, sort_by, sort_order, filter_conditions, output_format)
        log_mcp_action("db_view_table_data", {"db_path": db_path, "table_name": table_name, "limit": limit, "offset": offset, "output_format": output_format}, res)
        return res

    @mcp.tool(name="db_summarize_table", description="Generate a visual markdown profile containing column structures, record stats, and sample data for a table")
    def tool_db_summarize_table(db_path: str, table_name: str) -> str:
        res = db_consolidator.db_summarize_table(db_path, table_name)
        log_mcp_action("db_summarize_table", {"db_path": db_path, "table_name": table_name}, res)
        return res

    @mcp.tool(name="db_search_schema", description="Find tables, columns, or indexes whose names contain the given search keyword")
    def tool_db_search_schema(db_path: str, search_term: str) -> str:
        res = db_consolidator.db_search_schema(db_path, search_term)
        log_mcp_action("db_search_schema", {"db_path": db_path, "search_term": search_term}, res)
        return res

    # ──────────────────────────────────────────────────────────────────
    # System & Developer Utilities
    # ──────────────────────────────────────────────────────────────────

    @mcp.tool(name="get_system_info", description="Get host system metrics (CPU, memory, disk usage, OS)")
    def tool_get_system_info() -> str:
        res = utils_manager.get_system_info()
        log_mcp_action("get_system_info", {}, res)
        return res

    @mcp.tool(name="check_port", description="Check if a specific host TCP port is open")
    def tool_check_port(host: str, port: int) -> str:
        res = utils_manager.check_port(host, port)
        log_mcp_action("check_port", {"host": host, "port": port}, res)
        return res

    @mcp.tool(name="generate_uuid", description="Generate a random UUID v4")
    def tool_generate_uuid() -> str:
        res = utils_manager.generate_uuid()
        log_mcp_action("generate_uuid", {}, res)
        return res

    @mcp.tool(name="format_json", description="Validate and pretty print a JSON string")
    def tool_format_json(json_str: str) -> str:
        res = utils_manager.format_json(json_str)
        log_mcp_action("format_json", {"json_str": json_str}, res)
        return res

    @mcp.tool(name="base64_encode_decode", description="Encode or decode a base64 string. mode can be 'encode' or 'decode'")
    def tool_base64_encode_decode(mode: str, data: str) -> str:
        res = utils_manager.base64_encode_decode(mode, data)
        log_mcp_action("base64_encode_decode", {"mode": mode, "data": data}, res)
        return res

    @mcp.tool(name="calculate_file_hash", description="Calculate the MD5 or SHA256 checksum of a file (executed inside Docker)")
    def tool_calculate_file_hash(file_path: str, algorithm: str = "sha256") -> str:
        res = utils_manager.docker_calculate_file_hash(file_path, algorithm)
        log_mcp_action("calculate_file_hash", {"file_path": file_path, "algorithm": algorithm}, res)
        return res

    @mcp.tool(name="get_external_ip", description="Get host's internal and external network IP addresses")
    def tool_get_external_ip() -> str:
        res = utils_manager.get_external_ip()
        log_mcp_action("get_external_ip", {}, res)
        return res

    @mcp.tool(name="send_http_request", description="Send an arbitrary HTTP request and return response details")
    def tool_send_http_request(method: str, url: str, headers_json: str = None, body: str = None) -> str:
        res = utils_manager.send_http_request(method, url, headers_json, body)
        log_mcp_action("send_http_request", {"method": method, "url": url}, res)
        return res

    @mcp.tool(name="find_large_files", description="Find files larger than size_mb MB inside the directory (executed inside Docker)")
    def tool_find_large_files(dir_path: str, size_mb: int = 50) -> str:
        res = utils_manager.docker_find_large_files(dir_path, size_mb)
        log_mcp_action("find_large_files", {"dir_path": dir_path, "size_mb": size_mb}, res)
        return res

    @mcp.tool(name="extract_text_from_url", description="Extract raw clean text from a web URL, removing HTML tags")
    def tool_extract_text_from_url(url: str) -> str:
        res = utils_manager.extract_text_from_url(url)
        log_mcp_action("extract_text_from_url", {"url": url}, res)
        return res

    @mcp.tool(name="gpu_monitor", description="Query nvidia-smi for real-time GPU utilization, VRAM usage, temperature, and power draw. Falls back to WMI on Windows if nvidia-smi unavailable.")
    def tool_gpu_monitor() -> str:
        res = utils_manager.gpu_monitor()
        log_mcp_action("gpu_monitor", {}, res)
        return res

    @mcp.tool(name="system_thermal_scanner", description="Scan CPU temperature, clock speed, and per-core utilization. Uses psutil sensors on Linux/Mac, WMI on Windows.")
    def tool_system_thermal_scanner() -> str:
        res = utils_manager.system_thermal_scanner()
        log_mcp_action("system_thermal_scanner", {}, res)
        return res

    @mcp.tool(name="process_watchdog", description="Monitor and control system processes. action: 'list' (top 30 by CPU), 'find' (search by name), 'kill' (terminate by name). process_name required for find/kill.")
    def tool_process_watchdog(action: str, process_name: str = None) -> str:
        res = utils_manager.process_watchdog(action, process_name)
        log_mcp_action("process_watchdog", {"action": action, "process_name": process_name}, res)
        return res

    @mcp.tool(name="task_cron_scheduler", description="Manage scheduled tasks. action: 'list'|'create'|'delete'|'run'. Windows uses schtasks, Linux uses crontab. job_name, cron_expression, command required for create.")
    def tool_task_cron_scheduler(action: str, job_name: str = None, cron_expression: str = None, command: str = None) -> str:
        res = utils_manager.task_cron_scheduler(action, job_name, cron_expression, command)
        log_mcp_action("task_cron_scheduler", {"action": action, "job_name": job_name}, res)
        return res

    @mcp.tool(name="rest_client_simulator", description="Send REST API requests without curl. Returns formatted response headers, body (JSON pretty-printed), elapsed time, and the equivalent curl command.")
    def tool_rest_client_simulator(method: str, url: str, payload_json: str = None, headers_json: str = None) -> str:
        res = utils_manager.rest_client_simulator(method, url, payload_json, headers_json)
        log_mcp_action("rest_client_simulator", {"method": method, "url": url}, res)
        return res

    @mcp.tool(name="html_to_pdf_renderer", description="Convert an HTML file or URL to PDF. Tries weasyprint → pdfkit → headless browser in order. Output path must be under C:\\ameva.")
    def tool_html_to_pdf_renderer(html_path_or_url: str, output_pdf_path: str) -> str:
        res = utils_manager.html_to_pdf_renderer(html_path_or_url, output_pdf_path)
        log_mcp_action("html_to_pdf_renderer", {"source": html_path_or_url, "output": output_pdf_path}, res)
        return res

    # ──────────────────────────────────────────────────────────────────
    # Docker Container Control [NEW]
    # ──────────────────────────────────────────────────────────────────

    @mcp.tool(name="docker_container_manager", description="Manage local Docker containers. action: 'list'|'stats'|'start'|'stop'|'restart'|'logs'|'inspect'. container_name required for all except list/stats.")
    def tool_docker_container_manager(action: str, container_name: str = None, limit_lines: int = 50) -> str:
        res = docker_manager.docker_container_manager(action, container_name, limit_lines)
        log_mcp_action("docker_container_manager", {"action": action, "container": container_name}, res)
        return res

    # ──────────────────────────────────────────────────────────────────
    # Dataset & Audit Aggregation [NEW]
    # ──────────────────────────────────────────────────────────────────

    @mcp.tool(name="audit_log_aggregator", description="Scan all AMEVA projects for mcp_audit.jsonl files, merge them into a single dataset JSONL with source_project tags, sorted by timestamp. Outputs stats on tool usage per project.")
    def tool_audit_log_aggregator(output_dataset_path: str) -> str:
        res = dataset_aggregator.audit_log_aggregator(output_dataset_path)
        log_mcp_action("audit_log_aggregator", {"output": output_dataset_path}, res)
        return res

    # ──────────────────────────────────────────────────────────────────
    # Code Search [NEW]
    # ──────────────────────────────────────────────────────────────────

    @mcp.tool(name="vector_code_searcher", description="BM25-based full-text code search across AMEVA project files. Returns top matching files with highlighted context lines. file_ext: '.py' or '.py,.js,.ts'")
    def tool_vector_code_searcher(query: str, file_ext: str = ".py", search_root: str = None, top_k: int = 10, context_lines: int = 3) -> str:
        res = code_searcher.vector_code_searcher(query, file_ext, search_root, top_k, context_lines)
        log_mcp_action("vector_code_searcher", {"query": query, "file_ext": file_ext}, res)
        return res

    # ──────────────────────────────────────────────────────────────────
    # Network Service Discovery [NEW]
    # ──────────────────────────────────────────────────────────────────

    @mcp.tool(name="service_discovery", description="Parallel port scan a single IP or CIDR subnet. Identifies open ports and auto-detects AMEVA services (Streamlit, FastAPI, Gradio, Ollama, Redis). ports_json: '[22, 80, 8000, 8501]'")
    def tool_service_discovery(subnet: str = "127.0.0.1", ports_json: str = "[22, 80, 8000, 8080, 8501]", timeout: float = 0.5, max_hosts: int = 254) -> str:
        res = net_discovery.service_discovery(subnet, ports_json, timeout, max_hosts)
        log_mcp_action("service_discovery", {"subnet": subnet, "ports_json": ports_json}, res)
        return res

    return mcp

if __name__ == "__main__":
    server = create_server()
    server.run()
```

---

### File: `src/tools/README.md`
```markdown
# AMEVA MCP Tools Directory Specification

이 디렉토리는 AMEVA MCP Toolkit에서 제공하는 모든 에이전트 전용 도구(MCP Tools)의 비즈니스 로직 구현체를 모아둔 통합 디렉토리입니다.

## 디렉토리 구조 및 역할

- **database/**: SQLite 데이터베이스 연결 및 통합 데이터 연산을 처리합니다. ([상세 README](database/README.md))
  - 주요 도구: db_get_schema, db_execute_query, db_merge_tables
- **document/**: 디렉터리 및 코드베이스 병합, 마크다운 변환 및 Docker 컨테이너 내 파일 조작을 담당합니다.
  - 주요 도구: consolidate_codebase, convert_md_to_docx, delete_file_in_docker, move_file_in_docker
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
```

---

### File: `src/tools/database/db_consolidator.py`
```python
import sqlite3
import os
import re
import json
import random
from datetime import datetime

def _get_connection(db_path: str):
    """Safely return sqlite3 connection for the given absolute path."""
    # Enforce safe path validation inside C:\ameva
    normalized_path = os.path.abspath(db_path)
    if not normalized_path.lower().startswith(r"c:\ameva"):
        raise PermissionError(f"Security Error: Access to path '{normalized_path}' is denied. Only 'C:\\ameva' subfolders are allowed.")
        
    if not os.path.exists(normalized_path):
        raise FileNotFoundError(f"Database file not found at {normalized_path}")
    return sqlite3.connect(normalized_path)

def _validate_write_permission(client_token: str):
    """Validate if the client token is authorized for CUD operations."""
    expected_token = os.environ.get("AMEVA_DB_WRITE_TOKEN")
    if expected_token:
        if not client_token or client_token != expected_token:
            raise PermissionError("Security Error: CUD (Write) operation is restricted. Invalid or missing client_token.")

def db_get_schema(db_path: str) -> str:
    """Analyze and return schemas (tables, columns, SQL definition) of the SQLite database."""
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = cursor.fetchall()
        
        if not tables:
            conn.close()
            return f"Database at {db_path} has no tables."
            
        report = f"=== SCHEMA REPORT FOR: {db_path} ===\n\n"
        for table_name, create_sql in tables:
            report += f"Table: {table_name}\n"
            report += f"SQL definition:\n{create_sql}\n"
            
            cursor.execute(f"PRAGMA table_info({table_name});")
            cols = cursor.fetchall()
            report += "Columns:\n"
            for cid, name, type_name, notnull, dflt_value, pk in cols:
                pk_indicator = " [PRIMARY KEY]" if pk else ""
                nn_indicator = " [NOT NULL]" if notnull else ""
                report += f"  - {name} ({type_name}){pk_indicator}{nn_indicator}\n"
            report += "-" * 50 + "\n"
            
        conn.close()
        return report
    except Exception as e:
        return f"Error analyzing DB schema: {str(e)}"

def _format_output(headers: list, rows: list, output_format: str) -> str:
    """Format tabular data into markdown, json, csv, html, xml, or plain format."""
    output_format = output_format.lower().strip()
    if not rows:
        return f"Headers: {headers}\nResult: 0 rows returned."
        
    if output_format == "json":
        data = [dict(zip(headers, row)) for row in rows]
        return json.dumps(data, indent=2, ensure_ascii=False)
        
    elif output_format == "csv":
        import csv
        import io
        output = io.StringIO()
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(headers)
        writer.writerows(rows)
        return output.getvalue()
        
    elif output_format == "html":
        html = "<table border='1'>\n  <thead>\n    <tr>"
        for h in headers:
            html += f"<th>{h}</th>"
        html += "</tr>\n  </thead>\n  <tbody>\n"
        for row in rows:
            html += "    <tr>"
            for v in row:
                val = "" if v is None else str(v)
                html += f"<td>{val}</td>"
            html += "</tr>\n"
        html += "  </tbody>\n</table>"
        return html
        
    elif output_format == "xml":
        xml = "<records>\n"
        for row in rows:
            xml += "  <row>\n"
            for h, v in zip(headers, row):
                val = "" if v is None else str(v)
                clean_h = re.sub(r'[^a-zA-Z0-9_]', '', h) or "column"
                val_escaped = val.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                xml += f"    <{clean_h}>{val_escaped}</{clean_h}>\n"
            xml += "  </row>\n"
        xml += "</records>"
        return xml
        
    elif output_format == "plain":
        result = "\t".join(headers) + "\n"
        for row in rows:
            result += "\t".join(["" if v is None else str(v) for v in row]) + "\n"
        return result.strip()
        
    else:  # markdown
        widths = [len(str(h)) for h in headers]
        for row in rows:
            for i, v in enumerate(row):
                val_len = len(str(v)) if v is not None else 0
                if val_len > widths[i]:
                    widths[i] = val_len
                    
        header_line = "| " + " | ".join([str(h).ljust(widths[i]) for i, h in enumerate(headers)]) + " |"
        sep_line = "| " + " | ".join(["-" * widths[i] for i in range(len(headers))]) + " |"
        
        row_lines = []
        for row in rows:
            row_line = "| " + " | ".join([("" if v is None else str(v)).ljust(widths[i]) for i, v in enumerate(row)]) + " |"
            row_lines.append(row_line)
            
        return "\n".join([header_line, sep_line] + row_lines)

def db_execute_query(db_path: str, query: str, read_only: bool = True, output_format: str = "markdown", client_token: str = None) -> str:
    """Execute a SQL query/command safely. In read-only mode, only SELECT/PRAGMA/EXPLAIN is permitted."""
    query_stripped = re.sub(r'/\*.*?\*/', '', query, flags=re.DOTALL).strip().upper()
    
    if read_only:
        # Prevent any DDL or write DML
        dangerous_keywords = ["INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER", "REPLACE", "RENAME", "TRUNCATE"]
        for kw in dangerous_keywords:
            if re.search(r'\b' + kw + r'\b', query_stripped):
                return f"Security Error: Writing/Modifying operation '{kw}' is blocked in read-only mode."
    else:
        # Validate write permissions if client tries to run write operations
        try:
            _validate_write_permission(client_token)
        except PermissionError as pe:
            return str(pe)
        
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        cursor.execute(query)
        
        is_select = any(query_stripped.startswith(prefix) for prefix in ["SELECT", "PRAGMA", "EXPLAIN", "WITH"])
        if is_select:
            rows = cursor.fetchall()
            headers = [desc[0] for desc in cursor.description] if cursor.description else []
            conn.close()
            
            if not rows:
                return f"Query executed successfully. Headers: {headers}\nResult: 0 rows returned."
                
            return _format_output(headers, rows, output_format)
        else:
            conn.commit()
            changes = conn.changes()
            conn.close()
            return f"Command executed successfully. Database changes made: {changes} rows."
    except Exception as e:
        return f"Database Query Error: {str(e)}"

def db_merge_tables(src_db: str, dest_db: str, table_name: str, key_column: str, client_token: str = None) -> str:
    """
    Merge data from src_db.table_name into dest_db.table_name.
    Inserts missing records and updates matching records using key_column.
    """
    try:
        _validate_write_permission(client_token)
    except PermissionError as pe:
        return str(pe)
        
    try:
        # Enforce path safety
        src_db = os.path.abspath(src_db)
        dest_db = os.path.abspath(dest_db)
        if not src_db.lower().startswith(r"c:\ameva") or not dest_db.lower().startswith(r"c:\ameva"):
            return "Security Error: Both databases must be in the C:\\ameva directory."
            
        if not os.path.exists(src_db):
            return f"Error: Source database does not exist at {src_db}"
        if not os.path.exists(dest_db):
            return f"Error: Destination database does not exist at {dest_db}"
            
        src_conn = sqlite3.connect(src_db)
        src_cursor = src_conn.cursor()
        
        src_cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        if not src_cursor.fetchone():
            src_conn.close()
            return f"Error: Table '{table_name}' does not exist in source database."
            
        src_cursor.execute(f"PRAGMA table_info({table_name});")
        src_cols = [col[1] for col in src_cursor.fetchall()]
        
        if key_column not in src_cols:
            src_conn.close()
            return f"Error: Key column '{key_column}' not found in table '{table_name}'."
            
        src_cursor.execute(f"SELECT * FROM {table_name};")
        records = src_cursor.fetchall()
        src_conn.close()
        
        if not records:
            return f"No records found in source table '{table_name}' to merge."
            
        dest_conn = sqlite3.connect(dest_db)
        dest_cursor = dest_conn.cursor()
        
        dest_cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        if not dest_cursor.fetchone():
            src_conn_temp = sqlite3.connect(src_db)
            c_temp = src_conn_temp.cursor()
            c_temp.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
            create_sql = c_temp.fetchone()[0]
            src_conn_temp.close()
            
            dest_cursor.execute(create_sql)
            dest_conn.commit()
            
        dest_cursor.execute(f"SELECT {key_column} FROM {table_name};")
        dest_keys = {row[0] for row in dest_cursor.fetchall()}
        
        inserted = 0
        updated = 0
        
        col_names = ", ".join(src_cols)
        placeholders = ", ".join(["?"] * len(src_cols))
        insert_sql = f"INSERT INTO {table_name} ({col_names}) VALUES ({placeholders});"
        
        update_set = ", ".join([f"{col}=?" for col in src_cols if col != key_column])
        update_sql = f"UPDATE {table_name} SET {update_set} WHERE {key_column}=?;"
        
        key_index = src_cols.index(key_column)
        
        for record in records:
            rec_key = record[key_index]
            if rec_key in dest_keys:
                update_values = [record[i] for i in range(len(src_cols)) if i != key_index] + [rec_key]
                dest_cursor.execute(update_sql, update_values)
                updated += 1
            else:
                dest_cursor.execute(insert_sql, record)
                inserted += 1
                
        dest_conn.commit()
        dest_conn.close()
        
        return f"Successfully merged table '{table_name}': {inserted} rows inserted, {updated} rows updated in destination DB."
    except Exception as e:
        return f"Error during DB merge operation: {str(e)}"


# ==============================================================================
# ENTERPRISE PRO FEATURES IMPLEMENTATION
# ==============================================================================

def db_generate_erd(db_path: str) -> str:
    """Generate a copy-pasteable Mermaid ER Diagram of the database schema."""
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = [r[0] for r in cursor.fetchall()]
        
        if not tables:
            conn.close()
            return "No tables found in the database to generate an ERD."
            
        erd = "erDiagram\n"
        relationships = []
        
        for table in tables:
            erd += f"    {table} {{\n"
            
            # Get columns
            cursor.execute(f"PRAGMA table_info({table});")
            cols = cursor.fetchall()
            
            # Get foreign keys to mark them
            cursor.execute(f"PRAGMA foreign_key_list({table});")
            fks = cursor.fetchall()
            fk_cols = {f[3]: f for f in fks if f[3]}
            
            for cid, col_name, col_type, notnull, dflt, pk in cols:
                pk_flag = " PK" if pk else ""
                fk_flag = " FK" if col_name in fk_cols else ""
                clean_type = re.sub(r'[^a-zA-Z0-9]', '', col_type).lower() or "text"
                erd += f"        {clean_type} {col_name}{pk_flag}{fk_flag}\n"
            erd += "    }\n"
            
            for fk in fks:
                parent_table = fk[2]
                from_col = fk[3]
                to_col = fk[4]
                relationships.append(f"    {parent_table} ||--o{{ {table} : \"{from_col}->{to_col}\"")
                
        conn.close()
        
        erd += "\n" + "\n".join(relationships)
        return f"```mermaid\n{erd}\n```"
    except Exception as e:
        return f"Error generating Mermaid ERD: {str(e)}"


def db_generate_mock_data(db_path: str, table_name: str, count: int = 50, client_token: str = None) -> str:
    """Generate realistic mock data and populate the table automatically respecting FKs."""
    try:
        _validate_write_permission(client_token)
    except PermissionError as pe:
        return str(pe)
        
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        # Verify table
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        if not cursor.fetchone():
            conn.close()
            return f"Table '{table_name}' does not exist."
            
        # Get columns
        cursor.execute(f"PRAGMA table_info({table_name});")
        cols = cursor.fetchall()
        
        # Get foreign keys to resolve them dynamically
        cursor.execute(f"PRAGMA foreign_key_list({table_name});")
        fks = cursor.fetchall()
        fk_map = {f[3]: f[2] for f in fks if f[3]}
        
        # Pre-fetch parent table IDs to respect FK references
        parent_data = {}
        for col_name, parent_table in fk_map.items():
            cursor.execute(f"PRAGMA table_info({parent_table});")
            parent_cols = cursor.fetchall()
            pk_col = next((c[1] for c in parent_cols if c[5]), parent_cols[0][1])
            
            cursor.execute(f"SELECT {pk_col} FROM {parent_table} LIMIT 100;")
            parent_ids = [r[0] for r in cursor.fetchall()]
            if not parent_ids:
                conn.close()
                return f"Constraint Error: Parent table '{parent_table}' has no records. Populate it first before inserting into '{table_name}'."
            parent_data[col_name] = parent_ids
            
        first_names = ["Minsoo", "Jiho", "Yeon", "Jun", "Sujin", "Sunghwan", "Hyejin", "Gildong", "Chulsoo", "Younghee"]
        last_names = ["Kim", "Lee", "Park", "Choi", "Jung", "Kang", "Cho", "Yoon", "Jang", "Lim"]
        domains = ["gmail.com", "naver.com", "daum.net", "outlook.com", "yahoo.com"]
        
        inserted = 0
        col_names = [c[1] for c in cols]
        
        pk_col_info = next((c for c in cols if c[5]), None)
        is_integer_pk = pk_col_info and "INT" in pk_col_info[2].upper()
        
        insert_cols = [c for c in col_names if not (is_integer_pk and c == pk_col_info[1])]
        placeholders = ", ".join(["?"] * len(insert_cols))
        insert_sql = f"INSERT INTO {table_name} ({', '.join(insert_cols)}) VALUES ({placeholders});"
        
        for i in range(count):
            row_data = []
            for col in cols:
                name = col[1]
                col_type = col[2].upper()
                is_pk = col[5]
                
                if is_integer_pk and name == pk_col_info[1]:
                    continue
                    
                if name in parent_data:
                    row_data.append(random.choice(parent_data[name]))
                    continue
                    
                name_lower = name.lower()
                if "email" in name_lower:
                    row_data.append(f"{random.choice(first_names).lower()}{random.randint(10,99)}@{random.choice(domains)}")
                elif "phone" in name_lower or "tel" in name_lower:
                    row_data.append(f"010-{random.randint(1000,9999)}-{random.randint(1000,9999)}")
                elif "name" in name_lower:
                    row_data.append(f"{random.choice(first_names)} {random.choice(last_names)}")
                elif "uuid" in name_lower:
                    import uuid
                    row_data.append(str(uuid.uuid4()))
                elif "date" in name_lower or "time" in name_lower or "created" in name_lower or "updated" in name_lower:
                    row_data.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                elif "status" in name_lower:
                    row_data.append(random.choice(["ACTIVE", "PENDING", "INACTIVE"]))
                elif "INT" in col_type:
                    row_data.append(random.randint(1, 10000) if not is_pk else i + 100)
                elif "REAL" in col_type or "NUM" in col_type or "FLOAT" in col_type:
                    row_data.append(round(random.uniform(10.0, 1000.0), 2))
                else:
                    row_data.append(f"MockData_{name}_{i}")
                    
            cursor.execute(insert_sql, row_data)
            inserted += 1
            
        conn.commit()
        conn.close()
        return f"Successfully generated and inserted {inserted} mock records into table '{table_name}'."
    except Exception as e:
        return f"Error generating mock data: {str(e)}"


def db_global_search_value(db_path: str, search_query: str) -> str:
    """Search for a specific string value across all text columns of all tables."""
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = [r[0] for r in cursor.fetchall()]
        
        matches = []
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table});")
            cols = cursor.fetchall()
            text_cols = [c[1] for c in cols if any(t in c[2].upper() for t in ["TEXT", "CHAR", "VARCHAR", "CLOB"])]
            
            if not text_cols:
                continue
                
            where_clauses = " OR ".join([f"{col} LIKE ?" for col in text_cols])
            query = f"SELECT * FROM {table} WHERE {where_clauses};"
            
            params = [f"%{search_query}%"] * len(text_cols)
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            if rows:
                for row in rows[:10]:
                    matches.append(f"Table: {table} | Row: {row}")
                if len(rows) > 10:
                    matches.append(f"Table: {table} | ... and {len(rows)-10} more matches.")
                    
        conn.close()
        if not matches:
            return f"No matches found for search query '{search_query}'."
        return f"=== GLOBAL SEARCH RESULTS FOR '{search_query}' ===\n\n" + "\n".join(matches)
    except Exception as e:
        return f"Error during global search: {str(e)}"


def db_transpile_sqlite_to_other(db_path: str, target_dialect: str) -> str:
    """Transpile SQLite schema and data into PostgreSQL or MySQL DDL/DML script."""
    target_dialect = target_dialect.lower()
    if target_dialect not in ["postgresql", "mysql"]:
        return "Error: Target dialect must be either 'postgresql' or 'mysql'."
        
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = cursor.fetchall()
        
        sql_script = f"-- Generated Migration Script for {target_dialect.upper()}\n"
        sql_script += f"-- Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for table_name, create_sql in tables:
            new_ddl = create_sql
            if target_dialect == "postgresql":
                new_ddl = re.sub(
                    r'(?i)\bINTEGER\s+PRIMARY\s+KEY\s+AUTOINCREMENT\b', 
                    'SERIAL PRIMARY KEY', 
                    new_ddl
                )
                new_ddl = new_ddl.replace('"', '')
            elif target_dialect == "mysql":
                new_ddl = re.sub(
                    r'(?i)\bAUTOINCREMENT\b', 
                    'AUTO_INCREMENT', 
                    new_ddl
                )
                
            sql_script += f"{new_ddl};\n\n"
            
            cursor.execute(f"PRAGMA table_info({table_name});")
            cols = [c[1] for c in cursor.fetchall()]
            
            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()
            
            if rows:
                sql_script += f"-- Data insertion for {table_name}\n"
                col_str = ", ".join(cols)
                for row in rows:
                    val_list = []
                    for v in row:
                        if v is None:
                            val_list.append("NULL")
                        elif isinstance(v, (int, float)):
                            val_list.append(str(v))
                        else:
                            escaped = str(v).replace("'", "''")
                            val_list.append(f"'{escaped}'")
                    val_str = ", ".join(val_list)
                    sql_script += f"INSERT INTO {table_name} ({col_str}) VALUES ({val_str});\n"
                sql_script += "\n"
                
        conn.close()
        return sql_script
    except Exception as e:
        return f"Error transpiling SQLite to {target_dialect}: {str(e)}"


def db_profile_and_scan_health(db_path: str) -> str:
    """Analyze indices, scan orphaned rows (FK breaks), check high NULL rates, detect numeric outliers."""
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = [r[0] for r in cursor.fetchall()]
        
        report = f"=== DATABASE HEALTH & ANOMALY REPORT ===\n\n"
        
        cursor.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index';")
        indices = cursor.fetchall()
        idx_info = {}
        for idx_name, tbl_name in indices:
            cursor.execute(f"PRAGMA index_info({idx_name});")
            columns = [r[2] for r in cursor.fetchall()]
            key = (tbl_name, tuple(columns))
            if key in idx_info:
                idx_info[key].append(idx_name)
            else:
                idx_info[key] = [idx_name]
                
        dup_indices = {k: v for k, v in idx_info.items() if len(v) > 1}
        report += "1. Duplicate Index Check:\n"
        if dup_indices:
            for (tbl, cols), names in dup_indices.items():
                report += f"  - WARNING: Table '{tbl}' has duplicate indexes {names} covering columns {cols}.\n"
        else:
            report += "  - OK: No duplicate indexes found.\n"
        report += "\n"
        
        report += "2. Referential Integrity / Orphan Row Check:\n"
        orphans_found = False
        for table in tables:
            cursor.execute(f"PRAGMA foreign_key_list({table});")
            fks = cursor.fetchall()
            for fk in fks:
                parent_table = fk[2]
                child_col = fk[3]
                parent_col = fk[4] or "id"
                
                query = f"SELECT COUNT(*) FROM {table} WHERE {child_col} NOT IN (SELECT {parent_col} FROM {parent_table}) AND {child_col} IS NOT NULL;"
                cursor.execute(query)
                orphans = cursor.fetchone()[0]
                if orphans > 0:
                    report += f"  - DANGER: Table '{table}' has {orphans} orphan records violating foreign key reference to {parent_table}({parent_col})!\n"
                    orphans_found = True
        if not orphans_found:
            report += "  - OK: No orphan records found. Referential integrity intact.\n"
        report += "\n"
        
        report += "3. Columns Data Profiling & Anomalies:\n"
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table};")
            total_rows = cursor.fetchone()[0]
            if total_rows == 0:
                report += f"  - Table '{table}': Empty table.\n"
                continue
                
            cursor.execute(f"PRAGMA table_info({table});")
            cols = cursor.fetchall()
            for cid, col_name, col_type, notnull, dflt, pk in cols:
                cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {col_name} IS NULL;")
                nulls = cursor.fetchone()[0]
                null_rate = (nulls / total_rows) * 100
                if null_rate > 50:
                    report += f"  - WARNING: Table '{table}' column '{col_name}' has a high NULL rate of {null_rate:.1f}%.\n"
                    
                if any(t in col_type.upper() for t in ["INT", "REAL", "NUM", "FLOAT", "DOUBLE"]):
                    cursor.execute(f"SELECT AVG({col_name}), AVG({col_name}*{col_name}) FROM {table} WHERE {col_name} IS NOT NULL;")
                    stats = cursor.fetchone()
                    if stats and stats[0] is not None:
                        avg = stats[0]
                        variance = max(0, stats[1] - (avg * avg))
                        stddev = variance ** 0.5
                        
                        if stddev > 0:
                            upper_limit = avg + (3 * stddev)
                            lower_limit = avg - (3 * stddev)
                            cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {col_name} > ? OR {col_name} < ?;", (upper_limit, lower_limit))
                            outliers = cursor.fetchone()[0]
                            if outliers > 0:
                                report += f"  - INFO: Table '{table}' column '{col_name}' has {outliers} potential statistical outliers (> 3 stddev).\n"
                                
        conn.close()
        return report
    except Exception as e:
        return f"Error executing database health check: {str(e)}"


def db_format_sql(query: str) -> str:
    """Beautify, uppercase keywords, and format raw SQL string into pretty, readable SQL."""
    keywords = [
        r"\bselect\b", r"\bfrom\b", r"\bwhere\b", r"\bjoin\b", r"\bleft\b", r"\bright\b", r"\bouter\b",
        r"\binner\b", r"\bon\b", r"\bgroup\b", r"\bby\b", r"\border\b", r"\bhaving\b", r"\blimit\b",
        r"\band\b", r"\bor\b", r"\bas\b", r"\bin\b", r"\bis\b", r"\bnull\b", r"\bcreate\b", r"\btable\b",
        r"\binsert\b", r"\binto\b", r"\bvalues\b", r"\bupdate\b", r"\bset\b", r"\bdelete\b"
    ]
    
    formatted = query.strip()
    
    for kw in keywords:
        formatted = re.sub(kw, lambda m: m.group(0).upper(), formatted, flags=re.IGNORECASE)
        
    major_clauses = ["FROM", "WHERE", "LEFT JOIN", "RIGHT JOIN", "INNER JOIN", "JOIN", "GROUP BY", "ORDER BY", "HAVING", "LIMIT", "SET", "VALUES"]
    for clause in major_clauses:
        formatted = re.sub(r'\s+\b' + clause + r'\b', f'\n{clause}', formatted)
        
    return formatted


def db_compare_schemas(src_db: str, dest_db: str) -> str:
    """Compare src_db schema to dest_db and generate missing table/column DDL sync scripts."""
    try:
        src_db = os.path.abspath(src_db)
        dest_db = os.path.abspath(dest_db)
        if not src_db.lower().startswith(r"c:\ameva") or not dest_db.lower().startswith(r"c:\ameva"):
            return "Security Error: Both databases must be in the C:\\ameva directory."
            
        src_conn = sqlite3.connect(src_db)
        src_cursor = src_conn.cursor()
        dest_conn = sqlite3.connect(dest_db)
        dest_cursor = dest_conn.cursor()
        
        src_cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        src_tables = {r[0]: r[1] for r in src_cursor.fetchall()}
        
        dest_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        dest_tables = {r[0] for r in dest_cursor.fetchall()}
        
        diff_script = f"-- Schema Sync Script: {dest_db} -> match {src_db}\n\n"
        changes_detected = False
        
        for table, create_sql in src_tables.items():
            if table not in dest_tables:
                diff_script += f"-- Table '{table}' is missing in target. Creating...\n"
                diff_script += f"{create_sql};\n\n"
                changes_detected = True
                
        for table, create_sql in src_tables.items():
            if table in dest_tables:
                src_cursor.execute(f"PRAGMA table_info({table});")
                src_cols = {r[1]: (r[2], r[3], r[4]) for r in src_cursor.fetchall()}
                
                dest_cursor.execute(f"PRAGMA table_info({table});")
                dest_cols = {r[1] for r in dest_cursor.fetchall()}
                
                for col_name, (col_type, notnull, default) in src_cols.items():
                    if col_name not in dest_cols:
                        diff_script += f"-- Column '{col_name}' is missing in target table '{table}'. Adding...\n"
                        notnull_str = " NOT NULL" if notnull else ""
                        dflt_str = f" DEFAULT {default}" if default is not None else ""
                        diff_script += f"ALTER TABLE {table} ADD COLUMN {col_name} {col_type}{notnull_str}{dflt_str};\n"
                        changes_detected = True
                diff_script += "\n"
                
        src_conn.close()
        dest_conn.close()
        
        if not changes_detected:
            return "No schema differences detected between source and destination databases."
            
        return diff_script
    except Exception as e:
        return f"Error during schema comparison: {str(e)}"


def db_mask_table_data(db_path: str, table_name: str, mask_rules_json: str, client_token: str = None) -> str:
    """Mask sensitive columns inside a table based on GDPR-compliant rules."""
    try:
        _validate_write_permission(client_token)
    except PermissionError as pe:
        return str(pe)
        
    try:
        rules = json.loads(mask_rules_json)
    except Exception as e:
        return f"Error: Invalid mask_rules_json format: {str(e)}"
        
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        if not cursor.fetchone():
            conn.close()
            return f"Table '{table_name}' does not exist."
            
        cursor.execute(f"PRAGMA table_info({table_name});")
        table_cols = [c[1] for c in cursor.fetchall()]
        
        for col in rules.keys():
            if col not in table_cols:
                conn.close()
                return f"Error: Column '{col}' not found in table '{table_name}'."
                
        cursor.execute(f"SELECT rowid, * FROM {table_name};")
        rows = cursor.fetchall()
        
        updated = 0
        for row in rows:
            rowid = row[0]
            row_dict = {table_cols[i]: row[i+1] for i in range(len(table_cols))}
            
            update_clauses = []
            params = []
            
            for col, rule in rules.items():
                val = row_dict[col]
                if val is None:
                    continue
                    
                val_str = str(val)
                masked_val = val_str
                
                if rule == "mask_email":
                    if "@" in val_str:
                        local, domain = val_str.split("@", 1)
                        masked_local = local[0] + "***" if len(local) > 1 else local + "***"
                        masked_val = f"{masked_local}@{domain}"
                elif rule == "mask_name":
                    if len(val_str) >= 3:
                        masked_val = val_str[0] + "*" + val_str[2:]
                    elif len(val_str) == 2:
                        masked_val = val_str[0] + "*"
                    else:
                        masked_val = "*"
                elif rule == "mask_phone":
                    clean_phone = re.sub(r'[^0-9]', '', val_str)
                    if len(clean_phone) >= 10:
                        masked_val = f"{val_str[:3]}-****-{val_str[-4:]}"
                    else:
                        masked_val = "***-***-****"
                elif rule == "mask_hash":
                    import hashlib
                    masked_val = hashlib.sha256(val_str.encode()).hexdigest()[:16]
                else:
                    masked_val = "******"
                    
                update_clauses.append(f"{col}=?")
                params.append(masked_val)
                
            if update_clauses:
                params.append(rowid)
                query = f"UPDATE {table_name} SET {', '.join(update_clauses)} WHERE rowid=?;"
                cursor.execute(query, params)
                updated += 1
                
        conn.commit()
        conn.close()
        return f"Successfully masked data for {updated} rows in table '{table_name}'."
    except Exception as e:
        return f"Error masking table data: {str(e)}"


def db_optimize_query_tuning(db_path: str, slow_query: str) -> str:
    """Analyze query plan via EXPLAIN QUERY PLAN and output missing index recommendations."""
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        explain_query = f"EXPLAIN QUERY PLAN {slow_query}"
        cursor.execute(explain_query)
        plan_rows = cursor.fetchall()
        
        recommendations = []
        tuning_report = "=== SQL QUERY PLAN ANALYSIS ===\n\n"
        
        for row in plan_rows:
            detail = row[3]
            tuning_report += f"Plan detail: {detail}\n"
            
            if "SCAN TABLE" in detail:
                match = re.search(r'SCAN TABLE (\w+)', detail)
                if match:
                    table_name = match.group(1)
                    
                    where_match = re.search(r'(?i)WHERE\s+(.*)', slow_query)
                    candidate_cols = []
                    if where_match:
                        where_clause = where_match.group(1)
                        cols_in_where = re.findall(r'\b(?:' + table_name + r'\.)?(\w+)\s*[=<>!]+', where_clause)
                        candidate_cols.extend([c for c in cols_in_where if c.lower() not in ["null", "true", "false"]])
                        
                    seen = set()
                    candidate_cols = [c for c in candidate_cols if not (c in seen or seen.add(c))]
                    
                    if candidate_cols:
                        cols_str = ", ".join(candidate_cols)
                        idx_name = f"idx_{table_name}_{'_'.join(candidate_cols)}"
                        recommendations.append(f"CREATE INDEX {idx_name} ON {table_name}({cols_str});")
                    else:
                        recommendations.append(f"-- Suggestion: Analyze table '{table_name}' and create index on columns used in filtering/joining.")
                        
        conn.close()
        
        if recommendations:
            tuning_report += "\n=== INDEX OPTIMIZATION RECOMMENDATIONS ===\n"
            tuning_report += "\n".join(recommendations)
        else:
            tuning_report += "\n=== INDEX OPTIMIZATION RECOMMENDATIONS ===\n- OK: Query is already optimized and utilizes indices efficiently."
            
        return tuning_report
    except Exception as e:
        return f"Error during query optimization analysis: {str(e)}"


def db_enable_time_travel(db_path: str, table_name: str, client_token: str = None) -> str:
    """Enable time travel audit log shadow table and triggers for mutating operations."""
    try:
        _validate_write_permission(client_token)
    except PermissionError as pe:
        return str(pe)
        
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        if not cursor.fetchone():
            conn.close()
            return f"Table '{table_name}' does not exist."
            
        cursor.execute(f"PRAGMA table_info({table_name});")
        cols = [c[1] for c in cursor.fetchall()]
        
        ledger_table = f"{table_name}_ledger"
        
        create_ledger_sql = f"""
        CREATE TABLE IF NOT EXISTS {ledger_table} (
            ledger_id INTEGER PRIMARY KEY AUTOINCREMENT,
            row_id INTEGER,
            operation TEXT,
            old_data TEXT,
            new_data TEXT,
            changed_at TIMESTAMP DEFAULT (datetime('now', 'localtime'))
        );
        """
        cursor.execute(create_ledger_sql)
        
        old_json = "json_object(" + ", ".join([f"'{c}', OLD.{c}" for c in cols]) + ")"
        new_json = "json_object(" + ", ".join([f"'{c}', NEW.{c}" for c in cols]) + ")"
        
        cursor.execute(f"DROP TRIGGER IF EXISTS trg_{table_name}_insert;")
        cursor.execute(f"DROP TRIGGER IF EXISTS trg_{table_name}_update;")
        cursor.execute(f"DROP TRIGGER IF EXISTS trg_{table_name}_delete;")
        
        trg_insert = f"""
        CREATE TRIGGER trg_{table_name}_insert AFTER INSERT ON {table_name}
        BEGIN
            INSERT INTO {ledger_table} (row_id, operation, old_data, new_data)
            VALUES (NEW.rowid, 'INSERT', NULL, {new_json});
        END;
        """
        
        trg_update = f"""
        CREATE TRIGGER trg_{table_name}_update AFTER UPDATE ON {table_name}
        BEGIN
            INSERT INTO {ledger_table} (row_id, operation, old_data, new_data)
            VALUES (NEW.rowid, 'UPDATE', {old_json}, {new_json});
        END;
        """
        
        trg_delete = f"""
        CREATE TRIGGER trg_{table_name}_delete AFTER DELETE ON {table_name}
        BEGIN
            INSERT INTO {ledger_table} (row_id, operation, old_data, new_data)
            VALUES (OLD.rowid, 'DELETE', {old_json}, NULL);
        END;
        """
        
        cursor.execute(trg_insert)
        cursor.execute(trg_update)
        cursor.execute(trg_delete)
        
        conn.commit()
        conn.close()
        return f"Successfully enabled Time-Travel Audit on table '{table_name}'. Shadow ledger '{ledger_table}' and triggers are active."
    except Exception as e:
        return f"Error enabling time travel: {str(e)}"


def db_restore_time_travel(db_path: str, table_name: str, target_timestamp: str, client_token: str = None) -> str:
    """Restore table data back to a specific timestamp by executing mutations in reverse."""
    try:
        _validate_write_permission(client_token)
    except PermissionError as pe:
        return str(pe)
        
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        ledger_table = f"{table_name}_ledger"
        
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{ledger_table}';")
        if not cursor.fetchone():
            conn.close()
            return f"Time travel ledger '{ledger_table}' does not exist. Enable it first using db_enable_time_travel."
            
        cursor.execute(f"PRAGMA table_info({table_name});")
        cols = [c[1] for c in cursor.fetchall()]
        
        cursor.execute(f"PRAGMA table_info({table_name});")
        pk_col = next((c[1] for c in cursor.fetchall() if c[5]), None)
        
        cursor.execute(f"DROP TRIGGER IF EXISTS trg_{table_name}_insert;")
        cursor.execute(f"DROP TRIGGER IF EXISTS trg_{table_name}_update;")
        cursor.execute(f"DROP TRIGGER IF EXISTS trg_{table_name}_delete;")
        
        cursor.execute(f"SELECT operation, row_id, old_data, new_data, ledger_id FROM {ledger_table} WHERE changed_at > ? ORDER BY ledger_id DESC;", (target_timestamp,))
        ledger_rows = cursor.fetchall()
        
        if not ledger_rows:
            conn.close()
            db_enable_time_travel(db_path, table_name, client_token=client_token)
            return f"No changes detected since timestamp '{target_timestamp}'. Database is already at this state."
            
        restored_count = 0
        
        for op, row_id, old_data_json, new_data_json, ledger_id in ledger_rows:
            if op == "INSERT":
                cursor.execute(f"DELETE FROM {table_name} WHERE rowid=?;", (row_id,))
            elif op == "DELETE":
                old_data = json.loads(old_data_json)
                col_names = ", ".join(old_data.keys())
                placeholders = ", ".join(["?"] * len(old_data))
                vals = list(old_data.values())
                cursor.execute(f"INSERT INTO {table_name} ({col_names}) VALUES ({placeholders});", vals)
            elif op == "UPDATE":
                old_data = json.loads(old_data_json)
                set_clause = ", ".join([f"{k}=?" for k in old_data.keys()])
                vals = list(old_data.values())
                
                if pk_col and pk_col in old_data:
                    pk_val = old_data[pk_col]
                    vals.append(pk_val)
                    cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE {pk_col}=?;", vals)
                else:
                    vals.append(row_id)
                    cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE rowid=?;", vals)
                    
            restored_count += 1
            
        cursor.execute(f"DELETE FROM {ledger_table} WHERE changed_at > ?;", (target_timestamp,))
        
        conn.commit()
        conn.close()
        
        db_enable_time_travel(db_path, table_name, client_token=client_token)
        
        return f"Successfully restored '{table_name}' back to '{target_timestamp}'. Undid {restored_count} database mutations."
    except Exception as e:
        try:
            db_enable_time_travel(db_path, table_name, client_token=client_token)
        except:
            pass
        return f"Error during time-travel restore operation: {str(e)}"


def db_view_table_data(db_path: str, table_name: str, limit: int = 50, offset: int = 0, sort_by: str = None, sort_order: str = "DESC", filter_conditions: str = None, output_format: str = "markdown") -> str:
    """Browse and query table data with paging, sorting, filtering, and custom output formatting."""
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        if not cursor.fetchone():
            conn.close()
            return f"Error: Table '{table_name}' does not exist in the database."
            
        cursor.execute(f"PRAGMA table_info({table_name});")
        cols = [c[1] for c in cursor.fetchall()]
        
        query = f"SELECT * FROM {table_name}"
        params = []
        
        if filter_conditions:
            words = re.findall(r'\b\w+\b', filter_conditions)
            query += f" WHERE {filter_conditions}"
            
        if sort_by:
            if sort_by in cols:
                sort_order_clean = "ASC" if sort_order.upper() == "ASC" else "DESC"
                query += f" ORDER BY {sort_by} {sort_order_clean}"
            else:
                conn.close()
                return f"Error: Sort column '{sort_by}' does not exist in table '{table_name}'."
                
        query += f" LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return _format_output(cols, rows, output_format)
    except Exception as e:
        return f"Error browsing table data: {str(e)}"


def db_summarize_table(db_path: str, table_name: str) -> str:
    """Generate a visual markdown profile containing column structures, record stats, and sample data for a table."""
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        if not cursor.fetchone():
            conn.close()
            return f"Error: Table '{table_name}' does not exist."
            
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        row_count = cursor.fetchone()[0]
        
        cursor.execute(f"PRAGMA table_info({table_name});")
        cols = cursor.fetchall()
        
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
        samples = cursor.fetchall()
        col_names = [c[1] for c in cols]
        
        report = f"## Table Summary: `{table_name}`\n"
        report += f"- **Total Records**: {row_count} rows\n"
        report += f"- **Total Columns**: {len(cols)} columns\n\n"
        
        report += "### Column Schema\n"
        report += "| Col ID | Name | Type | Not Null? | Default Value | Primary Key? |\n"
        report += "| :--- | :--- | :--- | :--- | :--- | :--- |\n"
        for cid, name, col_type, notnull, dflt, pk in cols:
            nn_str = "Yes" if notnull else "No"
            pk_str = "Yes" if pk else "No"
            dflt_str = "None" if dflt is None else str(dflt)
            report += f"| {cid} | `{name}` | {col_type} | {nn_str} | `{dflt_str}` | {pk_str} |\n"
        report += "\n"
        
        report += "### Numeric Column Profiling\n"
        num_cols = [c[1] for c in cols if any(t in c[2].upper() for t in ["INT", "REAL", "NUM", "FLOAT", "DOUBLE"])]
        if num_cols:
            report += "| Column | Min | Max | Average |\n"
            report += "| :--- | :--- | :--- | :--- |\n"
            for col in num_cols:
                cursor.execute(f"SELECT MIN({col}), MAX({col}), AVG({col}) FROM {table_name};")
                stat = cursor.fetchone()
                if stat and stat[0] is not None:
                    report += f"| `{col}` | {stat[0]} | {stat[1]} | {stat[2]:.2f} |\n"
            report += "\n"
        else:
            report += "- No numeric columns to profile.\n\n"
            
        report += "### Sample Records (Recent 5 rows)\n"
        if samples:
            sample_md = _format_output(col_names, samples, "markdown")
            report += sample_md
        else:
            report += "*No records found in table.*"
            
        conn.close()
        return report
    except Exception as e:
        return f"Error profiling table: {str(e)}"


def db_search_schema(db_path: str, search_term: str) -> str:
    """Find tables, columns, or indexes whose names contain the given search keyword."""
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = [r[0] for r in cursor.fetchall()]
        
        matches = []
        search_term_lower = search_term.lower()
        
        for table in tables:
            if search_term_lower in table.lower():
                matches.append(f"- **Table (Name Match)**: `{table}`")
                
            cursor.execute(f"PRAGMA table_info({table});")
            cols = cursor.fetchall()
            for col in cols:
                col_name = col[1]
                col_type = col[2]
                if search_term_lower in col_name.lower():
                    matches.append(f"- **Column**: `{table}.{col_name}` (Type: {col_type})")
                    
        cursor.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index';")
        indexes = cursor.fetchall()
        for idx_name, tbl_name in indexes:
            if search_term_lower in idx_name.lower():
                matches.append(f"- **Index**: `{idx_name}` on table `{tbl_name}`")
                
        conn.close()
        
        if not matches:
            return f"No schema matches found for term '{search_term}'."
            
        return f"### Schema Search Results for '{search_term}'\n" + "\n".join(matches)
    except Exception as e:
        return f"Error searching schema: {str(e)}"


def db_unmask_table_data(db_path: str, table_name: str, unmask_rules_json: str, client_token: str = None) -> str:
    """
    db_mask_table_data로 마스킹 처리된 컬럼을 원래 값으로 복원한다.
    unmask_rules_json 예시: {"email": {"prefix_len": 3, "original_col": "email_raw"}}
    복원은 shadow 테이블(원본 저장용)이 있을 경우 JOIN으로 처리한다.
    write 권한 토큰 필수.
    """
    try:
        _validate_write_permission(client_token)
    except PermissionError as pe:
        return str(pe)

    try:
        rules = json.loads(unmask_rules_json)
    except json.JSONDecodeError as je:
        return f"Error: Invalid unmask_rules_json. {je}"

    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()

        # 테이블 컬럼 확인
        cursor.execute(f"PRAGMA table_info({table_name});")
        cols_info = {row[1]: row[2] for row in cursor.fetchall()}
        if not cols_info:
            conn.close()
            return f"Error: Table '{table_name}' not found in {db_path}."

        # shadow 테이블 존재 여부 확인
        shadow_table = f"{table_name}_shadow"
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        all_tables = [r[0] for r in cursor.fetchall()]
        has_shadow = shadow_table in all_tables

        restored_cols = []
        skipped_cols = []

        for col_name, rule in rules.items():
            if col_name not in cols_info:
                skipped_cols.append(f"{col_name} (not found in table)")
                continue

            if has_shadow:
                # shadow 테이블에서 original 복원
                try:
                    cursor.execute(f"PRAGMA table_info({shadow_table});")
                    shadow_cols = [r[1] for r in cursor.fetchall()]
                    if col_name in shadow_cols:
                        cursor.execute(f"""
                            UPDATE {table_name}
                            SET {col_name} = (
                                SELECT {col_name} FROM {shadow_table}
                                WHERE {shadow_table}.rowid = {table_name}.rowid
                            )
                        """)
                        conn.commit()
                        restored_cols.append(f"{col_name} (restored from shadow)")
                    else:
                        skipped_cols.append(f"{col_name} (shadow column not found)")
                except Exception as ex:
                    skipped_cols.append(f"{col_name} (shadow restore error: {ex})")
            else:
                # 규칙 기반 역변환 (제한적 — 해시 마스킹은 복원 불가, prefix 마스킹만 가능)
                mask_type = rule.get("mask_type", "prefix")
                if mask_type == "static":
                    original_value = rule.get("original_value")
                    if original_value:
                        cursor.execute(f"UPDATE {table_name} SET {col_name} = ?", (original_value,))
                        conn.commit()
                        restored_cols.append(f"{col_name} (restored to static value)")
                    else:
                        skipped_cols.append(f"{col_name} (no original_value provided for static restore)")
                else:
                    skipped_cols.append(f"{col_name} (irreversible mask type: {mask_type})")

        conn.close()

        report = f"## 🔓 DB Unmask Report: `{table_name}`\n\n"
        report += f"**Database**: `{db_path}`  \n"
        report += f"**Shadow Table**: {'Found ✅' if has_shadow else 'Not Found ⚠️'}\n\n"
        if restored_cols:
            report += "### ✅ Restored Columns\n"
            for c in restored_cols:
                report += f"- {c}\n"
        if skipped_cols:
            report += "\n### ⚠️ Skipped / Failed\n"
            for c in skipped_cols:
                report += f"- {c}\n"

        return report

    except Exception as e:
        return f"Error in db_unmask_table_data: {str(e)}"


def db_sync_connector(src_db: str, dest_db: str, table_name: str, client_token: str = None) -> str:
    """
    소스 SQLite DB의 특정 테이블 전체를 목적지 SQLite DB로 직접 동기화한다.
    목적지에 테이블이 없으면 자동 생성, 있으면 INSERT OR REPLACE로 upsert 처리.
    write 권한 토큰 필수. 두 경로 모두 C:\\ameva 하위만 허용.
    """
    try:
        _validate_write_permission(client_token)
    except PermissionError as pe:
        return str(pe)

    try:
        src_conn = _get_connection(src_db)
        src_cursor = src_conn.cursor()

        # 소스 테이블 스키마 가져오기
        src_cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        schema_row = src_cursor.fetchone()
        if not schema_row:
            src_conn.close()
            return f"Error: Table '{table_name}' not found in source DB '{src_db}'."

        create_sql = schema_row[0]

        # 소스 데이터 읽기
        src_cursor.execute(f"SELECT * FROM {table_name}")
        rows = src_cursor.fetchall()
        col_count = len(src_cursor.description)
        col_names = [d[0] for d in src_cursor.description]
        src_conn.close()

        # 목적지 DB 경로 보안 검사 — _get_connection 이 처리
        # 목적지 DB가 없으면 생성
        dest_norm = os.path.abspath(dest_db)
        if not dest_norm.lower().startswith(r"c:\ameva"):
            return f"Security Error: Destination path must be under C:\\ameva. Got: {dest_norm}"

        dest_conn = sqlite3.connect(dest_norm)
        dest_cursor = dest_conn.cursor()

        # 목적지 테이블 생성 (없으면)
        dest_cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if not dest_cursor.fetchone():
            dest_cursor.execute(create_sql)
            dest_conn.commit()
            table_action = "created"
        else:
            table_action = "already exists"

        # Bulk upsert
        placeholders = ", ".join(["?" for _ in col_names])
        upsert_sql = f"INSERT OR REPLACE INTO {table_name} ({', '.join(col_names)}) VALUES ({placeholders})"
        dest_cursor.executemany(upsert_sql, rows)
        dest_conn.commit()
        dest_conn.close()

        return (
            f"## 🔄 DB Sync Connector\n\n"
            f"**Source**: `{src_db}`  \n"
            f"**Destination**: `{dest_db}`  \n"
            f"**Table**: `{table_name}` ({table_action})  \n"
            f"**Rows Synced**: {len(rows)}  \n"
            f"**Columns**: {', '.join(col_names)}  \n\n"
            f"✅ Sync complete. {len(rows)} record(s) upserted."
        )

    except Exception as e:
        return f"Error in db_sync_connector: {str(e)}"
```

---

### File: `src/tools/database/README.md`
```markdown
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
```

---

### File: `src/tools/dataset/dataset_aggregator.py`
```python
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
```

---

### File: `src/tools/dataset/__init__.py`
```python
# dataset tools package
```

---

### File: `src/tools/docker/docker_manager.py`
```python
import os
import subprocess
import json


def docker_container_manager(action: str, container_name: str = None, limit_lines: int = 50) -> str:
    """
    로컬 Docker 컨테이너를 관리한다.
    action: 'list' | 'start' | 'stop' | 'restart' | 'logs' | 'inspect' | 'stats'
    container_name: 대상 컨테이너 이름 또는 ID (list/stats 제외)
    limit_lines: logs 출력 줄 제한 (기본 50)
    """
    def _run_docker(*args, timeout=15):
        cmd = ["docker"] + list(args)
        try:
            res = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                stdin=subprocess.DEVNULL
            )
            return res.returncode, res.stdout.strip(), res.stderr.strip()
        except FileNotFoundError:
            return -1, "", "Docker is not installed or not in PATH."
        except subprocess.TimeoutExpired:
            return -1, "", f"Docker command timed out after {timeout}s."
        except Exception as e:
            return -1, "", str(e)

    if action == "list":
        code, out, err = _run_docker("ps", "-a", "--format",
                                     "table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}")
        if code != 0:
            return f"Error listing containers: {err}"
        if not out:
            return "No Docker containers found."
        lines = out.splitlines()
        report = "## 🐳 Docker Container List\n\n"
        report += "| Container ID | Name | Image | Status | Ports |\n"
        report += "| :----------- | :--- | :---- | :----- | :---- |\n"
        for line in lines[1:]:  # skip header
            parts = line.split("\t")
            if len(parts) >= 5:
                cid, name, image, status, ports = parts[0], parts[1], parts[2], parts[3], parts[4]
                status_icon = "🟢" if "Up" in status else "🔴"
                report += f"| `{cid[:12]}` | `{name}` | `{image}` | {status_icon} {status} | {ports or '-'} |\n"
        return report

    elif action == "stats":
        code, out, err = _run_docker("stats", "--no-stream", "--format",
                                     "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}")
        if code != 0:
            return f"Error getting stats: {err}"
        if not out:
            return "No running containers to show stats for."
        lines = out.splitlines()
        report = "## 📊 Docker Container Stats (Live Snapshot)\n\n"
        report += "| Name | CPU% | Mem Usage | Mem% | Net I/O | Block I/O |\n"
        report += "| :--- | :--: | :-------- | :--: | :------ | :-------- |\n"
        for line in lines[1:]:
            parts = line.split("\t")
            if len(parts) >= 6:
                report += f"| `{parts[0]}` | {parts[1]} | {parts[2]} | {parts[3]} | {parts[4]} | {parts[5]} |\n"
        return report

    elif action == "start":
        if not container_name:
            return "Error: container_name is required for 'start'."
        code, out, err = _run_docker("start", container_name)
        if code != 0:
            return f"Error starting '{container_name}': {err}"
        return f"✅ Container '{container_name}' started successfully."

    elif action == "stop":
        if not container_name:
            return "Error: container_name is required for 'stop'."
        code, out, err = _run_docker("stop", container_name)
        if code != 0:
            return f"Error stopping '{container_name}': {err}"
        return f"🛑 Container '{container_name}' stopped successfully."

    elif action == "restart":
        if not container_name:
            return "Error: container_name is required for 'restart'."
        code, out, err = _run_docker("restart", container_name)
        if code != 0:
            return f"Error restarting '{container_name}': {err}"
        return f"🔄 Container '{container_name}' restarted successfully."

    elif action == "logs":
        if not container_name:
            return "Error: container_name is required for 'logs'."
        code, out, err = _run_docker("logs", "--tail", str(limit_lines), "--timestamps", container_name, timeout=20)
        if code != 0:
            # Docker logs outputs to stderr normally — check combined
            combined = out or err
            if not combined:
                return f"Error getting logs for '{container_name}': {err}"
        # Docker logs typically writes to stderr
        combined = (out + "\n" + err).strip()
        lines = combined.splitlines()[-limit_lines:]
        return (
            f"## 📋 Logs: `{container_name}` (last {limit_lines} lines)\n\n"
            f"```\n{chr(10).join(lines)}\n```"
        )

    elif action == "inspect":
        if not container_name:
            return "Error: container_name is required for 'inspect'."
        code, out, err = _run_docker("inspect", container_name)
        if code != 0:
            return f"Error inspecting '{container_name}': {err}"
        try:
            data = json.loads(out)
            if data:
                info = data[0]
                report = f"## 🔍 Container Inspect: `{container_name}`\n\n"
                report += f"**ID**: `{info.get('Id', '?')[:12]}`  \n"
                report += f"**Name**: `{info.get('Name', '?')}`  \n"
                report += f"**Image**: `{info.get('Config', {}).get('Image', '?')}`  \n"
                report += f"**Status**: `{info.get('State', {}).get('Status', '?')}`  \n"
                report += f"**Started At**: `{info.get('State', {}).get('StartedAt', '?')}`  \n"
                report += f"**RestartCount**: `{info.get('RestartCount', 0)}`  \n"
                
                # 네트워크
                networks = info.get("NetworkSettings", {}).get("Networks", {})
                if networks:
                    report += "\n### Networks\n"
                    for net_name, net_info in networks.items():
                        report += f"- `{net_name}`: IP=`{net_info.get('IPAddress', '-')}`\n"
                
                # 마운트
                mounts = info.get("Mounts", [])
                if mounts:
                    report += "\n### Mounts\n"
                    for m in mounts:
                        report += f"- `{m.get('Source', '?')}` → `{m.get('Destination', '?')}` ({m.get('Mode', 'rw')})\n"
                
                return report
        except Exception:
            return f"Inspect output:\n```json\n{out[:2000]}\n```"

    else:
        return f"Error: Unknown action '{action}'. Use: list | start | stop | restart | logs | inspect | stats"
```

---

### File: `src/tools/docker/__init__.py`
```python
# docker tools package
```

---

### File: `src/tools/document/code_consolidator.py`
```python
import os
import re
import sqlite3

CODE_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".c", ".cpp", ".h", ".hpp", 
    ".rs", ".go", ".html", ".css", ".json", ".yml", ".yaml", ".toml", 
    ".sql", ".ps1", ".sh", ".bat", ".md", ".txt", ".ini", ".conf", ".cfg"
}

def map_path(path: str) -> str:
    if os.environ.get("AMEVA_IN_CONTAINER") == "true":
        normalized = path.replace("\\", "/")
        return re.sub(r'^[Cc]:/ameva', '/app/workspace', normalized)
    return path

def build_dir_tree(dir_path: str, skip_dirs: set, max_depth: int = 5, current_depth: int = 0) -> list:
    if current_depth > max_depth:
        return ["  " * current_depth + "- ... (max depth reached)"]
    
    lines = []
    try:
        items = sorted(os.listdir(dir_path))
        for item in items:
            if item in skip_dirs:
                continue
            full_item_path = os.path.join(dir_path, item)
            indent = "  " * current_depth
            if os.path.isdir(full_item_path):
                lines.append(f"{indent}- [Dir] {item}/")
                lines.extend(build_dir_tree(full_item_path, skip_dirs, max_depth, current_depth + 1))
            else:
                lines.append(f"{indent}- [File] {item}")
    except Exception as e:
        lines.append(f"{'  ' * current_depth}- [Error] {str(e)}")
    return lines

def is_sqlite_file(file_path: str) -> bool:
    _, ext = os.path.splitext(file_path.lower())
    if ext in [".db", ".sqlite", ".sqlite3", ".db3"]:
        return True
    try:
        with open(file_path, "rb") as f:
            header = f.read(16)
            return header.startswith(b"SQLite format 3\0")
    except Exception:
        return False

def extract_sqlite_schema(db_path: str) -> str:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        
        if not tables:
            return "No tables found in SQLite database.\n"
            
        schema_lines = []
        for table_name, create_sql in tables:
            if create_sql:
                schema_lines.append(f"### Table: `{table_name}`")
                schema_lines.append("```sql")
                schema_lines.append(f"{create_sql};")
                schema_lines.append("```\n")
        return "\n".join(schema_lines)
    except Exception as e:
        return f"Error extracting schema from `{os.path.basename(db_path)}`: {str(e)}\n"

def is_code_file(file_path: str) -> bool:
    _, ext = os.path.splitext(file_path.lower())
    return ext in CODE_EXTENSIONS

def read_file_content(file_path: str) -> str:
    try:
        if os.path.getsize(file_path) > 1024 * 1024:
            return "# Error: File is larger than 1MB and was skipped.\n"
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception as e:
        return f"# Error reading file: {str(e)}\n"

def get_markdown_language(file_path: str) -> str:
    _, ext = os.path.splitext(file_path.lower())
    ext_map = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".jsx": "javascript",
        ".tsx": "typescript",
        ".c": "c",
        ".cpp": "cpp",
        ".h": "c",
        ".hpp": "cpp",
        ".rs": "rust",
        ".go": "go",
        ".html": "html",
        ".css": "css",
        ".json": "json",
        ".yml": "yaml",
        ".yaml": "yaml",
        ".toml": "toml",
        ".sql": "sql",
        ".sh": "bash",
        ".ps1": "powershell",
        ".bat": "batch",
        ".md": "markdown"
    }
    return ext_map.get(ext, "")

def consolidate_codebase_logic(target_dir: str, output_file: str = None) -> str:
    """
    Consolidate codebase into a single markdown file:
    1. Directory tree structure (excluding node_modules, .git, venv, etc.)
    2. SQLite database schemas if present
    3. Source code contents
    """
    orig_target_dir = target_dir
    target_dir = map_path(target_dir)
    
    if not os.path.exists(target_dir):
        return f"Error: Target directory does not exist: {orig_target_dir} (mapped to {target_dir})"
        
    skip_dirs = {
        ".git", "node_modules", "venv", "env", ".venv", 
        "__pycache__", ".idea", ".vscode", "build", "dist", 
        ".cache", ".system_generated", "logs"
    }
    
    md_lines = []
    md_lines.append("# Codebase Consolidation Report\n")
    md_lines.append(f"- **Target Directory**: `{orig_target_dir}`\n\n")
    
    # 1. Directory Tree
    md_lines.append("## 1. Directory Structure\n")
    md_lines.append("```text\n")
    tree_lines = build_dir_tree(target_dir, skip_dirs)
    md_lines.extend([line + "\n" for line in tree_lines])
    md_lines.append("```\n\n")
    md_lines.append("---\n\n")
    
    # Scan for files and databases
    db_files = []
    code_files = []
    
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for f in files:
            full_path = os.path.join(root, f)
            if is_sqlite_file(full_path):
                db_files.append(full_path)
            elif is_code_file(full_path):
                code_files.append(full_path)
                
    # 2. Database Schema
    md_lines.append("## 2. Database Schema\n")
    if db_files:
        for db in db_files:
            rel_path = os.path.relpath(db, target_dir).replace("\\", "/")
            md_lines.append(f"### Database File: `{rel_path}`\n")
            schema_data = extract_sqlite_schema(db)
            md_lines.append(schema_data)
            md_lines.append("\n")
    else:
        md_lines.append("No SQLite databases detected in the directory.\n\n")
    md_lines.append("---\n\n")
    
    # 3. Source Codes
    md_lines.append("## 3. Source Codes\n")
    if code_files:
        for file in code_files:
            rel_path = os.path.relpath(file, target_dir).replace("\\", "/")
            lang = get_markdown_language(file)
            content = read_file_content(file)
            
            md_lines.append(f"### File: `{rel_path}`\n")
            md_lines.append(f"```{lang}\n")
            md_lines.append(content)
            if not content.endswith("\n"):
                md_lines.append("\n")
            md_lines.append("```\n\n")
            md_lines.append("---\n\n")
            
        # Pop the trailing separator
        if md_lines[-1] == "---\n\n":
            md_lines.pop()
    else:
        md_lines.append("No readable source code files detected.\n")
        
    final_md = "".join(md_lines)
    
    if output_file:
        output_file_mapped = map_path(output_file)
        out_dir = os.path.dirname(output_file_mapped)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)
        try:
            with open(output_file_mapped, "w", encoding="utf-8") as f:
                f.write(final_md)
            return f"Successfully consolidated codebase from {orig_target_dir} into {output_file}."
        except Exception as e:
            return f"Error writing consolidated report: {str(e)}"
            
    return final_md
```

---

### File: `src/tools/document/file_manager.py`
```python
import os
import subprocess
import logging

logger = logging.getLogger(__name__)

def map_path_to_container(path: str) -> str:
    """Map Windows host path to Docker container path (/app/workspace)."""
    normalized = path.replace("\\", "/")
    import re
    return re.sub(r'^[Cc]:/ameva', '/app/workspace', normalized)

def docker_delete_file(file_path: str) -> str:
    """Delete a file securely inside a Docker container."""
    container_path = map_path_to_container(file_path)
    cmd = [
        "docker", "run", "--rm",
        "-v", r"C:\ameva:/app/workspace",
        "alpine",
        "rm", "-f", container_path
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=15, stdin=subprocess.DEVNULL)
        if res.returncode != 0:
            return f"Error deleting file inside Docker: {res.stderr.strip()}"
        return f"Successfully deleted {file_path} inside Docker container."
    except Exception as e:
        return f"Exception while deleting file: {str(e)}"

def docker_move_file(src_path: str, dest_path: str) -> str:
    """Move or rename a file securely inside a Docker container."""
    container_src = map_path_to_container(src_path)
    container_dest = map_path_to_container(dest_path)
    
    # Ensure destination directory inside container exists
    dest_dir = os.path.dirname(container_dest)
    mkdir_cmd = [
        "docker", "run", "--rm",
        "-v", r"C:\ameva:/app/workspace",
        "alpine",
        "mkdir", "-p", dest_dir
    ]
    
    cmd = [
        "docker", "run", "--rm",
        "-v", r"C:\ameva:/app/workspace",
        "alpine",
        "mv", container_src, container_dest
    ]
    try:
        # Create dir first
        subprocess.run(mkdir_cmd, capture_output=True, timeout=10, stdin=subprocess.DEVNULL)
        
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=15, stdin=subprocess.DEVNULL)
        if res.returncode != 0:
            return f"Error moving file inside Docker: {res.stderr.strip()}"
        return f"Successfully moved {src_path} to {dest_path} inside Docker container."
    except Exception as e:
        return f"Exception while moving file: {str(e)}"

def docker_convert_md_to_docx(input_md_path: str, output_docx_path: str) -> str:
    """Convert Markdown to DOCX inside the ameva-mcp-server Docker container."""
    container_input = map_path_to_container(input_md_path)
    container_output = map_path_to_container(output_docx_path)
    
    # Run python script inline inside the container
    python_code = f"from tools.document.md_converter import convert_md_to_docx_logic; print(convert_md_to_docx_logic('{container_input}', '{container_output}'))"
    
    cmd = [
        "docker", "run", "--rm",
        "-v", r"C:\ameva:/app/workspace",
        "-e", "AMEVA_IN_CONTAINER=true",
        "-e", "PYTHONPATH=/app/src",
        "ameva-mcp-server",
        "python", "-c", python_code
    ]

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30, stdin=subprocess.DEVNULL)
        if res.returncode != 0:
            return f"Error converting document inside Docker: {res.stderr.strip()}"
        return res.stdout.strip()
    except Exception as e:
        return f"Exception while converting document: {str(e)}"
```

---

### File: `src/tools/document/md_converter.py`
```python
import os
import re
from docx import Document


def map_path(path: str) -> str:
    if os.environ.get("AMEVA_IN_CONTAINER") == "true":
        normalized = path.replace("\\", "/")
        return re.sub(r'^[Cc]:/ameva', '/app/workspace', normalized)
    return path


def convert_md_to_docx_logic(input_md_path: str, output_docx_path: str) -> str:
    """
    마크다운을 DOCX로 변환합니다.
    MCP 의존성이 전혀 없는 순수 파이썬 함수 (느슨한 결합)
    헤딩, 불릿, 번호목록, 코드블록, 굵은글씨, 수평선 지원.
    """
    orig_input = input_md_path
    orig_output = output_docx_path
    input_md_path = map_path(input_md_path)
    output_docx_path = map_path(output_docx_path)
    
    out_dir = os.path.dirname(output_docx_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    if not os.path.exists(input_md_path):
        return f"Error: Input file does not exist at {orig_input} (mapped to {input_md_path})"

    try:
        doc = Document()
        in_code_block = False
        code_lines = []
        numbered_counter = 0

        with open(input_md_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for raw_line in lines:
            line = raw_line.rstrip()
            
            # 코드 블록 처리
            if line.startswith("```"):
                if in_code_block:
                    # 코드 블록 종료
                    code_text = "\n".join(code_lines)
                    p = doc.add_paragraph(style="No Spacing")
                    run = p.add_run(code_text)
                    run.font.name = "Courier New"
                    run.font.size = __import__("docx.shared", fromlist=["Pt"]).Pt(9) if False else None
                    code_lines = []
                    in_code_block = False
                else:
                    in_code_block = True
                continue
            
            if in_code_block:
                code_lines.append(line)
                continue

            # 빈 줄
            if not line.strip():
                numbered_counter = 0
                continue

            # 헤딩
            if line.startswith("#### "):
                doc.add_heading(line[5:].strip(), level=4)
            elif line.startswith("### "):
                doc.add_heading(line[4:].strip(), level=3)
            elif line.startswith("## "):
                doc.add_heading(line[3:].strip(), level=2)
            elif line.startswith("# "):
                doc.add_heading(line[2:].strip(), level=1)
            # 수평선
            elif line.strip() in ["---", "***", "___"]:
                doc.add_paragraph("─" * 50)
            # 불릿 리스트
            elif line.startswith("- ") or line.startswith("* ") or line.startswith("+ "):
                text = line[2:].strip()
                # 볼드 처리
                text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
                doc.add_paragraph(text, style='List Bullet')
            # 번호 리스트
            elif re.match(r'^\d+\. ', line):
                text = re.sub(r'^\d+\. ', '', line)
                text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
                doc.add_paragraph(text, style='List Number')
            # 인용문
            elif line.startswith("> "):
                text = line[2:].strip()
                p = doc.add_paragraph(style="Quote" if "Quote" in [s.name for s in doc.styles] else "Normal")
                p.add_run(f'"{text}"').italic = True
            # 일반 텍스트 (볼드 처리 포함)
            else:
                p = doc.add_paragraph()
                # **bold** 파싱
                parts = re.split(r'\*\*(.+?)\*\*', line)
                for i, part in enumerate(parts):
                    if part:
                        run = p.add_run(part)
                        run.bold = (i % 2 == 1)
                
        doc.save(output_docx_path)
        return f"Success: Converted {orig_input} to {orig_output}"
        
    except Exception as e:
        return f"Error during conversion: {str(e)}"


def docx_to_markdown(docx_path: str, output_md_path: str = None) -> str:
    """
    .docx 파일을 마크다운(.md)으로 변환한다.
    헤딩 스타일, 리스트, 일반 단락을 파싱하여 구조화된 MD로 저장.
    output_md_path가 없으면 결과 텍스트를 직접 반환.
    """
    norm_path = map_path(docx_path)
    
    # 보안 검사
    abs_path = os.path.abspath(norm_path)
    if not abs_path.lower().startswith(r"c:\ameva") and \
       not abs_path.lower().startswith("/app/workspace"):
        return f"Security Error: Access to path '{abs_path}' is denied."
    
    if not os.path.exists(abs_path):
        return f"Error: DOCX file not found at {docx_path}"

    try:
        doc = Document(abs_path)
        md_lines = []

        for para in doc.paragraphs:
            style_name = para.style.name if para.style else "Normal"
            text = para.text.strip()
            
            if not text:
                md_lines.append("")
                continue

            # 헤딩 스타일
            if "Heading 1" in style_name:
                md_lines.append(f"# {text}")
            elif "Heading 2" in style_name:
                md_lines.append(f"## {text}")
            elif "Heading 3" in style_name:
                md_lines.append(f"### {text}")
            elif "Heading 4" in style_name:
                md_lines.append(f"#### {text}")
            elif "Heading 5" in style_name or "Heading 6" in style_name:
                md_lines.append(f"##### {text}")
            # 리스트 스타일
            elif "List Bullet" in style_name:
                md_lines.append(f"- {text}")
            elif "List Number" in style_name:
                md_lines.append(f"1. {text}")
            # 코드 스타일
            elif "Code" in style_name or "No Spacing" in style_name:
                md_lines.append(f"```\n{text}\n```")
            # 인용
            elif "Quote" in style_name:
                md_lines.append(f"> {text}")
            else:
                # 볼드/이탤릭 처리
                md_text = ""
                for run in para.runs:
                    r_text = run.text
                    if run.bold and run.italic:
                        r_text = f"***{r_text}***"
                    elif run.bold:
                        r_text = f"**{r_text}**"
                    elif run.italic:
                        r_text = f"*{r_text}*"
                    md_text += r_text
                md_lines.append(md_text if md_text.strip() else text)

        # 표 처리
        for table in doc.tables:
            if not table.rows:
                continue
            header = [cell.text.strip() for cell in table.rows[0].cells]
            md_lines.append("\n| " + " | ".join(header) + " |")
            md_lines.append("| " + " | ".join(["---"] * len(header)) + " |")
            for row in table.rows[1:]:
                cells = [cell.text.strip() for cell in row.cells]
                md_lines.append("| " + " | ".join(cells) + " |")
            md_lines.append("")

        result = "\n".join(md_lines)
        # 연속 빈 줄 정리
        result = re.sub(r"\n{3,}", "\n\n", result).strip()

        if output_md_path:
            out_norm = map_path(output_md_path)
            out_abs = os.path.abspath(out_norm)
            if not out_abs.lower().startswith(r"c:\ameva") and \
               not out_abs.lower().startswith("/app/workspace"):
                return f"Security Error: Output path '{out_abs}' is denied."
            os.makedirs(os.path.dirname(out_abs), exist_ok=True) if os.path.dirname(out_abs) else None
            with open(out_abs, "w", encoding="utf-8") as f:
                f.write(result)
            return f"Success: Converted {docx_path} to {output_md_path} ({len(result)} chars)"
        
        # 직접 반환 (3000자 제한)
        preview = result[:3000]
        if len(result) > 3000:
            preview += f"\n\n... (truncated, full length: {len(result)} chars)"
        return preview

    except Exception as e:
        return f"Error converting DOCX to Markdown: {str(e)}"


def md_image_path_fixer(doc_path: str, base_image_dir: str) -> str:
    """
    마크다운 파일 내의 깨진 이미지 경로를 실제 로컬 이미지 경로로 자동 치환한다.
    base_image_dir 하위에서 동일한 파일명을 탐색하여 경로를 교정한다.
    """
    # 경로 보안 검사
    doc_abs = os.path.abspath(doc_path)
    base_abs = os.path.abspath(base_image_dir)
    for p in [doc_abs, base_abs]:
        if not p.lower().startswith(r"c:\ameva"):
            return f"Security Error: Path must be under C:\\ameva. Got: {p}"

    if not os.path.exists(doc_abs):
        return f"Error: Markdown file not found at {doc_path}"
    if not os.path.isdir(base_abs):
        return f"Error: base_image_dir is not a directory: {base_image_dir}"

    # base_image_dir 내 모든 이미지 파일 인덱싱 (파일명 → 절대경로)
    IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp"}
    image_index = {}
    for root, _, files in os.walk(base_abs):
        for fname in files:
            if any(fname.lower().endswith(ext) for ext in IMAGE_EXTS):
                # 중복 시 첫 번째 발견 우선
                if fname.lower() not in image_index:
                    image_index[fname.lower()] = os.path.join(root, fname)

    with open(doc_abs, "r", encoding="utf-8") as f:
        content = f.read()

    # 마크다운 이미지 패턴: ![alt](path)
    pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
    
    fixed_count = 0
    not_found = []
    
    def replace_path(match):
        nonlocal fixed_count
        alt = match.group(1)
        old_path = match.group(2)
        
        # 이미 유효한 URL 이면 스킵
        if old_path.startswith("http://") or old_path.startswith("https://"):
            return match.group(0)
        
        # 파일명 추출
        img_filename = os.path.basename(old_path).lower()
        
        if img_filename in image_index:
            new_path = image_index[img_filename].replace("\\", "/")
            fixed_count += 1
            return f"![{alt}]({new_path})"
        else:
            not_found.append(old_path)
            return match.group(0)  # 그대로 유지
    
    new_content = pattern.sub(replace_path, content)
    
    if fixed_count == 0 and not not_found:
        return f"No image references found in {doc_path}."
    
    if fixed_count > 0:
        # 수정된 내용 저장
        with open(doc_abs, "w", encoding="utf-8") as f:
            f.write(new_content)
    
    report = (
        f"## 🖼️ MD Image Path Fixer\n\n"
        f"**File**: `{doc_path}`  \n"
        f"**Fixed Paths**: {fixed_count}  \n"
        f"**Not Found**: {len(not_found)}  \n"
        f"**Image Index Size**: {len(image_index)} files indexed\n\n"
    )
    if not_found:
        report += "### ⚠️ Images Not Found (path kept as-is)\n"
        for p in not_found[:10]:
            report += f"- `{p}`\n"
    if fixed_count > 0:
        report += f"\n✅ File saved with {fixed_count} corrected image path(s)."
    
    return report
```

---

### File: `src/tools/git/git_manager.py`
```python
import os
import subprocess
import re
import logging

logger = logging.getLogger(__name__)

AMEVA_IN_CONTAINER = os.environ.get("AMEVA_IN_CONTAINER") == "true"
BASE_DIR = "/app/workspace" if AMEVA_IN_CONTAINER else r"C:\ameva"

# 모든 AMEVA 리포지토리 목록
AMEVA_REPOS = [
    "AMEVA-Agent-Orchestra",
    "AMEVA-Benchmark-Suite",
    "AMEVA-Dead-Internet-Threatre",
    "AMEVA-Doc-AI",
    "AMEVA-Edge-Agent",
    "AMEVA-MCP-Toolkit-Utils",
    "AMEVA-Model-Nexus",
    "AMEVA-STT-Agent",
    "AMEVA-STT-Trainer",
    "AMEVA-Window-Assistant",
]


def _get_safe_path(repo_name: str) -> str:
    """Validate and return safe absolute path for the repository."""
    safe_name = os.path.basename(repo_name)
    path = os.path.join(BASE_DIR, safe_name)
    if not os.path.exists(path):
        raise ValueError(f"Repository {safe_name} does not exist at {path}")
    return path


def _get_safe_path_for_clone(repo_name: str) -> str:
    """Validate and return safe path for cloning a new repository."""
    safe_name = os.path.basename(repo_name)
    path = os.path.join(BASE_DIR, safe_name)
    if os.path.exists(path):
        raise ValueError(f"Directory {safe_name} already exists at {path}")
    return path


def run_git_command(repo_name: str, command: list) -> str:
    """Run a git command safely in the specified repository."""
    try:
        path = _get_safe_path(repo_name)
        full_command = ["git"] + command
        
        logger.info(f"Running command `{' '.join(full_command)}` in {path}")
        
        result = subprocess.run(
            full_command,
            cwd=path,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            check=False,
            timeout=30,
            stdin=subprocess.DEVNULL
        )
        
        output = result.stdout.strip()
        if result.returncode != 0:
            error_output = result.stderr.strip()
            return f"Git Command Error ({result.returncode}):\nStdout: {output}\nStderr: {error_output}"
        
        return output if output else "Command executed successfully with no output."
    except subprocess.TimeoutExpired:
        return f"Git command timed out after 30 seconds."
    except Exception as e:
        return f"Error executing git command: {str(e)}"


def _get_auth_url(repo_url: str) -> str:
    """If AMEVA_GITHUB_TOKEN is in env, inject it into the HTTPS repository URL."""
    token = os.environ.get("AMEVA_GITHUB_TOKEN")
    if not token:
        return repo_url
    
    if repo_url.startswith("https://") and "@" not in repo_url:
        return repo_url.replace("https://", f"https://{token}@")
    return repo_url


def git_status(repo_name: str) -> str:
    """Get the git status of a repository."""
    return run_git_command(repo_name, ["status", "-sb"])


def git_pull(repo_name: str) -> str:
    """Pull the latest changes from origin."""
    try:
        path = _get_safe_path(repo_name)
        res = subprocess.run(["git", "remote", "get-url", "origin"], cwd=path, capture_output=True, text=True, stdin=subprocess.DEVNULL)
        if res.returncode == 0:
            auth_url = _get_auth_url(res.stdout.strip())
            return run_git_command(repo_name, ["pull", auth_url])
    except Exception:
        pass
    return run_git_command(repo_name, ["pull"])


def git_commit_and_push(repo_name: str, message: str) -> str:
    """Stage all changes, commit, and push."""
    add_result = run_git_command(repo_name, ["add", "."])
    if "Error" in add_result:
        return f"Failed during git add:\n{add_result}"
        
    commit_result = run_git_command(repo_name, ["commit", "-m", message])
    if "Error" in commit_result and "nothing to commit" not in commit_result:
        return f"Failed during git commit:\n{commit_result}"
        
    try:
        path = _get_safe_path(repo_name)
        res = subprocess.run(["git", "remote", "get-url", "origin"], cwd=path, capture_output=True, text=True, stdin=subprocess.DEVNULL)
        if res.returncode == 0:
            auth_url = _get_auth_url(res.stdout.strip())
            push_result = run_git_command(repo_name, ["push", auth_url, "main"])
        else:
            push_result = run_git_command(repo_name, ["push", "origin", "main"])
        # Fetch to update local refs/remotes/origin/main tracking branch
        run_git_command(repo_name, ["fetch"])
    except Exception:
        push_result = run_git_command(repo_name, ["push", "origin", "main"])
        try:
            run_git_command(repo_name, ["fetch"])
        except:
            pass
        
    if "Error" in push_result:
        return f"Failed during git push:\n{push_result}"
        
    return f"Successfully added, committed, and pushed.\nCommit Info:\n{commit_result}\nPush Info:\n{push_result}"


def git_clone(repo_url: str, repo_name: str) -> str:
    """Clone a remote repository into BASE_DIR under the specified repo_name."""
    try:
        dest_path = _get_safe_path_for_clone(repo_name)
        auth_url = _get_auth_url(repo_url)
        
        full_command = ["git", "clone", auth_url, dest_path]
        logger.info(f"Cloning {repo_url} to {dest_path}")
        
        result = subprocess.run(
            full_command,
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            check=False,
            timeout=60,
            stdin=subprocess.DEVNULL
        )
        
        output = result.stdout.strip()
        if result.returncode != 0:
            error_output = result.stderr.strip()
            token = os.environ.get("AMEVA_GITHUB_TOKEN")
            if token:
                error_output = error_output.replace(token, "******")
            return f"Git Clone Error ({result.returncode}):\nStderr: {error_output}"
        
        return f"Successfully cloned {repo_url} into {repo_name}."
    except Exception as e:
        return f"Error executing git clone: {str(e)}"


def git_log(repo_name: str, limit: int = 10) -> str:
    """Show the git commit logs."""
    return run_git_command(repo_name, ["log", f"-n", str(limit), "--oneline", "--decorate", "--graph"])


def git_diff(repo_name: str, file_path: str = None) -> str:
    """Show changes in the working directory or compared to the index."""
    cmd = ["diff"]
    if file_path:
        cmd.append(file_path)
    return run_git_command(repo_name, cmd)


def git_branch(repo_name: str, action: str = "list", branch_name: str = None) -> str:
    """Manage branches: list, create (new), or delete (delete)."""
    if action == "list":
        return run_git_command(repo_name, ["branch", "-a"])
    elif action == "new":
        if not branch_name:
            return "Error: branch_name is required to create a new branch."
        return run_git_command(repo_name, ["branch", branch_name])
    elif action == "delete":
        if not branch_name:
            return "Error: branch_name is required to delete a branch."
        return run_git_command(repo_name, ["branch", "-d", branch_name])
    else:
        return f"Error: Unknown branch action '{action}'. Use 'list', 'new', or 'delete'."


def git_checkout(repo_name: str, branch_or_file: str, create: bool = False) -> str:
    """Switch branches or restore files."""
    cmd = ["checkout"]
    if create:
        cmd.append("-b")
    cmd.append(branch_or_file)
    return run_git_command(repo_name, cmd)


def git_merge(repo_name: str, branch_name: str) -> str:
    """Merge the specified branch into the current branch."""
    return run_git_command(repo_name, ["merge", branch_name])


def git_reset(repo_name: str, mode: str = "mixed", commit_hash: str = "HEAD") -> str:
    """Reset the current HEAD to the specified state (soft, mixed, hard)."""
    if mode not in ["soft", "mixed", "hard"]:
        return f"Error: Unknown reset mode '{mode}'. Choose from: soft, mixed, hard."
    return run_git_command(repo_name, ["reset", f"--{mode}", commit_hash])


def git_stash(repo_name: str, action: str = "push", stash_id: str = None) -> str:
    """Manage stashes: push, pop, list, apply, or clear."""
    if action == "push":
        return run_git_command(repo_name, ["stash", "push", "-m", stash_id or "Stashed by MCP"])
    elif action == "pop":
        cmd = ["stash", "pop"]
        if stash_id:
            cmd.append(stash_id)
        return run_git_command(repo_name, cmd)
    elif action == "list":
        return run_git_command(repo_name, ["stash", "list"])
    elif action == "apply":
        cmd = ["stash", "apply"]
        if stash_id:
            cmd.append(stash_id)
        return run_git_command(repo_name, cmd)
    elif action == "clear":
        return run_git_command(repo_name, ["stash", "clear"])
    else:
        return f"Error: Unknown stash action '{action}'. Use 'push', 'pop', 'list', 'apply', or 'clear'."


# ──────────────────────────────────────────────
# 신규 Git 도구 (고도화)
# ──────────────────────────────────────────────

def workspace_git_broadcaster() -> str:
    """
    C:\\ameva 하위의 모든 AMEVA 리포지토리를 일괄 스캔하여
    각 레포의 현재 상태(브랜치, ahead/behind, 변경파일 수)를 종합 보고한다.
    """
    results = []
    report = "## 📡 AMEVA Workspace Git Broadcast\n\n"
    report += f"**Scanned Base Dir**: `{BASE_DIR}`  \n"
    report += f"**Timestamp**: `{__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`\n\n"
    report += "| Repository | Branch | Status | Changed Files | Ahead | Behind |\n"
    report += "| :--------- | :----- | :----- | :-----------: | :---: | :----: |\n"

    # BASE_DIR 내 실제 git 레포 탐색 (AMEVA_REPOS + 자동탐색)
    repos_to_scan = list(AMEVA_REPOS)
    try:
        for d in os.listdir(BASE_DIR):
            full = os.path.join(BASE_DIR, d)
            if os.path.isdir(full) and os.path.isdir(os.path.join(full, ".git")):
                if d not in repos_to_scan:
                    repos_to_scan.append(d)
    except Exception:
        pass

    for repo_name in repos_to_scan:
        repo_path = os.path.join(BASE_DIR, repo_name)
        if not os.path.isdir(os.path.join(repo_path, ".git")):
            report += f"| `{repo_name}` | - | ❌ Not a git repo | - | - | - |\n"
            continue

        try:
            # 브랜치명
            branch_res = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=repo_path, capture_output=True, text=True, timeout=5, stdin=subprocess.DEVNULL
            )
            branch = branch_res.stdout.strip() if branch_res.returncode == 0 else "?"

            # fetch (최신 원격 상태 반영)
            subprocess.run(
                ["git", "fetch", "--quiet"],
                cwd=repo_path, capture_output=True, timeout=10, stdin=subprocess.DEVNULL
            )

            # ahead/behind
            ab_res = subprocess.run(
                ["git", "rev-list", "--left-right", "--count", f"HEAD...origin/{branch}"],
                cwd=repo_path, capture_output=True, text=True, timeout=5, stdin=subprocess.DEVNULL
            )
            if ab_res.returncode == 0 and ab_res.stdout.strip():
                parts = ab_res.stdout.strip().split()
                ahead = parts[0] if len(parts) > 0 else "0"
                behind = parts[1] if len(parts) > 1 else "0"
            else:
                ahead, behind = "?", "?"

            # 변경된 파일 수
            status_res = subprocess.run(
                ["git", "status", "--short"],
                cwd=repo_path, capture_output=True, text=True, timeout=5, stdin=subprocess.DEVNULL
            )
            changed = len([l for l in status_res.stdout.strip().splitlines() if l.strip()])

            # 상태 아이콘
            if changed == 0 and ahead == "0" and behind == "0":
                status_icon = "✅ Clean"
            elif changed > 0:
                status_icon = f"📝 Modified"
            elif int(ahead) > 0 if ahead.isdigit() else False:
                status_icon = "⬆️ Ahead"
            elif int(behind) > 0 if behind.isdigit() else False:
                status_icon = "⬇️ Behind"
            else:
                status_icon = "⚠️ Unknown"

            report += f"| `{repo_name}` | `{branch}` | {status_icon} | {changed} | {ahead} | {behind} |\n"

        except Exception as ex:
            report += f"| `{repo_name}` | ? | ⚠️ Error: {str(ex)[:40]} | - | - | - |\n"

    return report


def git_commit_helper(repo_name: str) -> str:
    """
    현재 스테이징된 diff를 분석하고 Conventional Commits 스펙에 맞는
    커밋 메시지를 자동 생성하여 추천한다.
    변경 내용을 파싱해 type, scope, subject, body를 구성한다.
    """
    try:
        path = _get_safe_path(repo_name)

        # 스테이지 된 변경사항 가져오기
        staged = subprocess.run(
            ["git", "diff", "--staged", "--stat"],
            cwd=path, capture_output=True, text=True, timeout=10, stdin=subprocess.DEVNULL
        )
        staged_diff = subprocess.run(
            ["git", "diff", "--staged", "--name-only"],
            cwd=path, capture_output=True, text=True, timeout=10, stdin=subprocess.DEVNULL
        )

        if staged.returncode != 0:
            return f"Error getting staged diff: {staged.stderr.strip()}"

        stat_output = staged.stdout.strip()
        changed_files = [f.strip() for f in staged_diff.stdout.strip().splitlines() if f.strip()]

        if not changed_files:
            # 스테이지 안된 경우 — 현재 변경 파일도 확인
            unstaged = subprocess.run(
                ["git", "diff", "--name-only"],
                cwd=path, capture_output=True, text=True, timeout=10, stdin=subprocess.DEVNULL
            )
            unstaged_files = [f.strip() for f in unstaged.stdout.strip().splitlines() if f.strip()]
            if unstaged_files:
                return (
                    "⚠️ No staged changes found.\n"
                    f"Unstaged files ({len(unstaged_files)}):\n" +
                    "\n".join(f"  - {f}" for f in unstaged_files[:10]) +
                    "\n\nRun `git add .` or `git add <file>` first."
                )
            return "ℹ️ No changes detected (working tree is clean)."

        # 변경 타입 추론 로직
        def infer_type(files: list) -> str:
            paths_str = " ".join(files).lower()
            if any(f.endswith((".md", ".rst", ".txt")) for f in files):
                return "docs"
            if any("test" in f or "spec" in f for f in files):
                return "test"
            if any(f in paths_str for f in ["requirements", "dockerfile", "docker-compose", ".yml", ".yaml", "setup.py"]):
                return "build"
            if any("fix" in f or "bug" in f or "patch" in f for f in files):
                return "fix"
            if any(f.endswith(".py") for f in files):
                return "feat"
            return "chore"

        def infer_scope(files: list) -> str:
            dirs = set()
            for f in files:
                parts = f.replace("\\", "/").split("/")
                if len(parts) > 1:
                    dirs.add(parts[-2])  # 부모 폴더명
            if not dirs:
                return ""
            if len(dirs) == 1:
                return list(dirs)[0]
            return "multi"

        commit_type = infer_type(changed_files)
        scope = infer_scope(changed_files)
        scope_str = f"({scope})" if scope else ""

        # 변경 파일 기반 subject 생성
        file_names = [os.path.basename(f) for f in changed_files[:3]]
        subject_base = ", ".join(file_names)
        if len(changed_files) > 3:
            subject_base += f" and {len(changed_files) - 3} more"

        # 추천 메시지들
        suggestions = [
            f"{commit_type}{scope_str}: update {subject_base}",
            f"{commit_type}{scope_str}: add/modify {subject_base}",
            f"{commit_type}{scope_str}: refactor {subject_base}",
        ]

        report = (
            f"## 🤖 Git Commit Message Helper\n\n"
            f"**Repository**: `{repo_name}`  \n"
            f"**Staged Files** ({len(changed_files)}):\n"
        )
        for f in changed_files[:15]:
            report += f"  - `{f}`\n"
        if len(changed_files) > 15:
            report += f"  - *... and {len(changed_files)-15} more*\n"

        report += f"\n**Diff Summary**:\n```\n{stat_output}\n```\n\n"
        report += "### 💡 Recommended Commit Messages\n\n"
        for i, msg in enumerate(suggestions, 1):
            report += f"{i}. `{msg}`\n"

        report += (
            f"\n### Conventional Commits Format\n"
            f"```\n"
            f"<type>(<scope>): <short description>\n\n"
            f"[optional body]\n\n"
            f"[optional footer]\n"
            f"```\n\n"
            f"**Types**: feat | fix | docs | style | refactor | test | build | chore | perf | ci\n"
        )
        return report

    except ValueError as ve:
        return f"Error: {str(ve)}"
    except Exception as e:
        return f"Error in git_commit_helper: {str(e)}"
```

---

### File: `src/tools/git/README.md`
```markdown
# Git MCP API Specification for AI Agents

본 명세서는 AMEVA MCP Toolkit 내의 Git 관련 도구(Git MCP Tools)를 AI 에이전트가 오작동 없이 정확하게 활용할 수 있도록 돕는 API 명세 및 활용 가이드라인입니다.

---

## 1. 전제 조건 및 인증 규칙

- **작업 경로 기준**: 모든 Git 도구는 `repo_name` 파라미터를 입력받습니다. 이는 서버 내부에서 안전성 검증을 거쳐 `C:\ameva\<repo_name>`(컨테이너 외부 실행 기준) 경로로 매핑됩니다. 에이전트는 절대 경로를 전달하는 대신 저장소 디렉토리명만 주입해야 합니다.
- **인증 토큰 자동 주입**: 원격 관련 명령(`git_pull`, `git_commit_and_push`, `git_clone`) 수행 시, 환경 변수 `AMEVA_GITHUB_TOKEN`이 설정되어 있다면 HTTPS 주소에 개인 접근 토큰(PAT)이 자동으로 주입되어 무인증 푸시/풀을 수행합니다.

---

## 2. API 상세 명세

### 1) git_status
- **설명**: 작업 공간의 현재 상태 및 스테이징 상태를 간결하게 요약 조회합니다. (`git status -sb` 수준)
- **파라미터**:
  - `repo_name` (string, 필수): 검사할 저장소 이름 (예: `AMEVA-Doc-AI`)
- **반환값**: 현재 활성화된 브랜치 정보 및 수정/추적되지 않은 파일 목록.

### 2) git_log
- **설명**: 해당 저장소의 커밋 히스토리를 요약하여 반환합니다.
- **파라미터**:
  - `repo_name` (string, 필수): 저장소 이름
  - `limit` (integer, 기본값: 10): 조회할 최근 커밋 개수
- **반환값**: 커밋 그래프 정보가 담긴 단선 형식(`--oneline`)의 커밋 목록.

### 3) git_diff
- **설명**: 현재 작업 디렉토리에서 수정된 변경 사항(Diff)을 확인합니다.
- **파라미터**:
  - `repo_name` (string, 필수): 저장소 이름
  - `file_path` (string, 선택): 특정 파일의 변경 사항만 조회하고 싶을 때 상대 경로 전달
- **반환값**: 표준 unified diff 형식의 텍스트 결과물.

### 4) git_clone
- **설명**: 새로운 원격 저장소를 지정된 이름으로 로컬에 복제합니다.
- **파라미터**:
  - `repo_url` (string, 필수): 깃허브 등 원격 저장소 HTTPS 주소
  - `repo_name` (string, 필수): 복제하여 생성할 로컬 폴더 이름
- **반환값**: 성공 또는 실패 에러 메시지. (에러 발생 시 토큰 유출 방지를 마스킹 처리함)

### 5) git_pull
- **설명**: 원격 저장소(`origin`)로부터 최신 커밋을 가져와 현재 브랜치에 병합합니다.
- **파라미터**:
  - `repo_name` (string, 필수): 저장소 이름
- **반환값**: 풀 수행 결과 출력문.

### 6) git_commit_and_push
- **설명**: 로컬의 모든 변경 사항(신규 파일 포함)을 스테이징한 후 커밋 메시지와 함께 즉시 원격 저장소로 푸시합니다. (`git add . && git commit -m <message> && git push` 일괄 처리)
- **파라미터**:
  - `repo_name` (string, 필수): 저장소 이름
  - `commit_message` (string, 필수): 변경점을 요약한 커밋 메시지
- **반환값**: 커밋 결과 정보 및 푸시 성공 여부.

### 7) git_branch
- **설명**: 저장소 내의 브랜치를 조회, 생성 또는 삭제합니다.
- **파라미터**:
  - `repo_name` (string, 필수): 저장소 이름
  - `action` (string, 기본값: `list`): 수행할 작업 (`list`, `new`, `delete`)
  - `branch_name` (string, 선택): `action`이 `new` 또는 `delete`일 때 조작할 브랜치 명
- **반환값**: 브랜치 목록 혹은 변경/삭제 성공 상태 메시지.

### 8) git_checkout
- **설명**: 활성화된 브랜치를 전환하거나 특정 파일의 변경 상태를 복구합니다.
- **파라미터**:
  - `repo_name` (string, 필수): 저장소 이름
  - `branch_or_file` (string, 필수): 이동할 브랜치 명 또는 복구할 파일 경로
  - `create` (boolean, 기본값: `False`): `True`로 설정할 시 새 브랜치를 생성하여 전환 (`-b` 옵션)
- **반환값**: 전환/복구 결과 정보.

### 9) git_merge
- **설명**: 대상 브랜치의 변경 사항을 현재 브랜치로 가져와 병합합니다.
- **파라미터**:
  - `repo_name` (string, 필수): 저장소 이름
  - `branch_name` (string, 필수): 병합을 가져올 대상 브랜치 명
- **반환값**: 병합 결과 및 충돌(Conflict) 발생 유무.

### 10) git_reset
- **설명**: 현재 HEAD 위치를 특정 커밋 지점이나 상태로 되돌립니다.
- **파라미터**:
  - `repo_name` (string, 필수): 저장소 이름
  - `mode` (string, 기본값: `mixed`): 리셋 종류 (`soft`, `mixed`, `hard`)
  - `commit_hash` (string, 기본값: `HEAD`): 복구 기준 커밋 해시 값 또는 상대 위치
- **반환값**: 리셋 수행 성공 정보.

### 11) git_stash
- **설명**: 현재 작업 디렉토리의 변경 사항을 임시 저장(Stash) 공간으로 대피시킵니다.
- **파라미터**:
  - `repo_name` (string, 필수): 저장소 이름
  - `action` (string, 기본값: `push`): 수행할 stash 작업 (`push`, `pop`, `list`, `apply`, `clear`)
  - `stash_id` (string, 선택): push 할 때의 간단한 메시지명 또는 pop/apply 대상 인덱스 번호 (예: `stash@{0}`)
- **반환값**: 대피/복구 작업 수행 로그.

---

## 3. AI 에이전트 행동 가이드라인 (Best Practices)

1. **상태 조회의 의무화**:
   - `git_commit_and_push`를 수행하기 전에는 반드시 `git_status` 혹은 `git_diff`를 호출하여 현재 로컬 작업 디렉토리에 정확히 어떤 수정사항들이 반영되어 있는지 점검하십시오.
2. **충돌 처리 규칙**:
   - `git_merge` 또는 `git_pull` 수행 중 병합 충돌(Conflict)이 발생할 경우, 에이전트는 충돌 파일을 직접 읽어 수정한 후 `git_commit_and_push` 도구를 사용해 충돌을 해소하는 커밋을 생성해야 합니다.
3. **위험 도구 사용 지양**:
   - `git_reset --hard`는 로컬의 미커밋 변경분을 완전히 삭제할 수 있으므로, 예외 상황이 아니면 기본 모드(`--mixed` 또는 `--soft`)를 권장합니다.
```

---

### File: `src/tools/git/__init__.py`
```python
# Git toolkit
```

---

### File: `src/tools/network/net_discovery.py`
```python
import socket
import json
import concurrent.futures
import ipaddress
from datetime import datetime


def _scan_port(host: str, port: int, timeout: float = 0.5) -> tuple[int, bool, str]:
    """단일 포트 스캔 — (port, is_open, banner)"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((host, port))
        is_open = (result == 0)
        banner = ""
        if is_open:
            try:
                sock.settimeout(0.3)
                banner = sock.recv(256).decode("utf-8", errors="ignore").strip()[:60]
            except Exception:
                pass
        return port, is_open, banner
    except Exception:
        return port, False, ""
    finally:
        sock.close()


def _get_service_name(port: int) -> str:
    """알려진 포트 서비스명 반환."""
    WELL_KNOWN = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
        53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
        443: "HTTPS", 465: "SMTPS", 587: "SMTP-TLS",
        1433: "MSSQL", 3306: "MySQL", 3389: "RDP",
        5000: "Flask/Dev", 5432: "PostgreSQL", 5900: "VNC",
        6379: "Redis", 7860: "Gradio", 8000: "FastAPI/Dev",
        8080: "HTTP-Alt", 8443: "HTTPS-Alt", 8501: "Streamlit",
        8888: "Jupyter", 9200: "Elasticsearch", 11434: "Ollama",
        19530: "Milvus", 27017: "MongoDB", 50051: "gRPC",
    }
    try:
        return socket.getservbyport(port) if port not in WELL_KNOWN else WELL_KNOWN[port]
    except Exception:
        return WELL_KNOWN.get(port, "unknown")


def service_discovery(
    subnet: str = "127.0.0.1",
    ports_json: str = "[22, 80, 8000, 8080, 8501]",
    timeout: float = 0.5,
    max_hosts: int = 254
) -> str:
    """
    지정 서브넷 또는 단일 호스트를 스캔하여 활성 서비스 포트를 식별한다.
    AMEVA 노드(Streamlit, FastAPI, Gradio, Ollama 등)의 상태 파악에 최적화.

    subnet: 단일 IP (예: 192.168.0.1) 또는 CIDR (예: 192.168.0.0/24)
    ports_json: 스캔할 포트 목록 JSON (예: [22, 80, 8000, 8080, 8501])
    timeout: 포트당 타임아웃 초 (기본 0.5)
    max_hosts: 서브넷 스캔 시 최대 호스트 수 제한 (기본 254)
    """
    # 포트 파싱
    try:
        ports = json.loads(ports_json)
        if not isinstance(ports, list):
            return "Error: ports_json must be a JSON array (e.g., [22, 80, 8080])"
        ports = [int(p) for p in ports if 0 < int(p) < 65536]
    except Exception as e:
        return f"Error parsing ports_json: {e}"

    if not ports:
        return "Error: No valid ports provided."

    # 호스트 목록 결정
    hosts = []
    try:
        # CIDR 서브넷 여부 확인
        if "/" in subnet:
            network = ipaddress.ip_network(subnet, strict=False)
            host_list = list(network.hosts())
            if len(host_list) > max_hosts:
                return (
                    f"Error: Subnet '{subnet}' has {len(host_list)} hosts. "
                    f"Max allowed: {max_hosts}. Use a smaller range or increase max_hosts."
                )
            hosts = [str(h) for h in host_list]
        else:
            # 단일 호스트
            hosts = [subnet]
    except ValueError as ve:
        return f"Error: Invalid subnet/IP '{subnet}': {ve}"

    if not hosts:
        return f"No hosts to scan in {subnet}."

    start_time = datetime.now()
    results = {}  # host -> [(port, is_open, banner)]

    # 병렬 스캔 (스레드 풀)
    total_tasks = len(hosts) * len(ports)
    MAX_WORKERS = min(100, total_tasks)

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {}
        for host in hosts:
            for port in ports:
                fut = executor.submit(_scan_port, host, port, timeout)
                futures[fut] = host

        for fut in concurrent.futures.as_completed(futures):
            host = futures[fut]
            try:
                port, is_open, banner = fut.result()
                if host not in results:
                    results[host] = []
                results[host].append((port, is_open, banner))
            except Exception:
                pass

    elapsed = (datetime.now() - start_time).total_seconds()

    # 활성 호스트만 필터링
    active_hosts = {h: ports_res for h, ports_res in results.items()
                    if any(is_open for _, is_open, _ in ports_res)}

    # 리포트 작성
    report = (
        f"## 🌐 Network Service Discovery\n\n"
        f"**Target**: `{subnet}`  \n"
        f"**Ports Scanned**: `{ports}`  \n"
        f"**Hosts Scanned**: {len(hosts)}  \n"
        f"**Active Hosts**: {len(active_hosts)}  \n"
        f"**Scan Time**: {elapsed:.2f}s\n\n"
    )

    if not active_hosts:
        report += "🔴 No active hosts with open ports found.\n"
        return report

    report += "---\n\n"
    for host in sorted(active_hosts.keys()):
        open_ports = [(p, b) for p, is_open, b in sorted(active_hosts[host]) if is_open]
        closed_count = len(ports) - len(open_ports)

        # 호스트명 역방향 조회 시도
        try:
            hostname = socket.gethostbyaddr(host)[0]
        except Exception:
            hostname = ""

        report += f"### 🟢 Host: `{host}`"
        if hostname and hostname != host:
            report += f" (`{hostname}`)"
        report += f"\n\n"

        report += "| Port | Service | Status | Banner |\n"
        report += "| :--- | :------ | :----: | :----- |\n"
        for port, banner in open_ports:
            svc = _get_service_name(port)
            report += f"| `{port}` | {svc} | 🟢 OPEN | `{banner or '-'}` |\n"

        # AMEVA 특화 서비스 인식
        ameva_services = []
        open_port_nums = [p for p, _ in open_ports]
        if 8501 in open_port_nums:
            ameva_services.append("📊 Streamlit App")
        if any(p in open_port_nums for p in [8000, 5000]):
            ameva_services.append("⚡ FastAPI/Flask Server")
        if 7860 in open_port_nums:
            ameva_services.append("🎨 Gradio UI")
        if 11434 in open_port_nums:
            ameva_services.append("🤖 Ollama LLM Server")
        if 6379 in open_port_nums:
            ameva_services.append("💾 Redis Cache")
        if 19530 in open_port_nums:
            ameva_services.append("🔢 Milvus Vector DB")

        if ameva_services:
            report += f"\n**Detected AMEVA Services**: {', '.join(ameva_services)}\n"
        report += "\n---\n\n"

    return report.strip()
```

---

### File: `src/tools/network/__init__.py`
```python
# network tools package
```

---

### File: `src/tools/search/code_searcher.py`
```python
import os
import re
import math
from collections import defaultdict


AMEVA_BASE = r"C:\ameva"


def _tf_idf_search(query: str, corpus: list[dict], top_k: int = 10) -> list[dict]:
    """
    TF-IDF / BM25 기반 텍스트 검색. 
    corpus: [{"path": str, "text": str, "lines": [(lineno, line)]}]
    """
    # 토크나이징
    def tokenize(text: str) -> list[str]:
        return re.findall(r"[a-zA-Z_]\w*", text.lower())

    query_tokens = set(tokenize(query))
    if not query_tokens:
        return []

    N = len(corpus)
    # IDF 계산
    df = defaultdict(int)
    for doc in corpus:
        doc_tokens = set(tokenize(doc["text"]))
        for t in query_tokens:
            if t in doc_tokens:
                df[t] += 1

    idf = {t: math.log((N - df[t] + 0.5) / (df[t] + 0.5) + 1) for t in query_tokens}

    # BM25 파라미터
    k1 = 1.5
    b = 0.75
    avg_dl = sum(len(tokenize(d["text"])) for d in corpus) / max(N, 1)

    scores = []
    for doc in corpus:
        doc_tokens = tokenize(doc["text"])
        dl = len(doc_tokens)
        tf_map = defaultdict(int)
        for t in doc_tokens:
            tf_map[t] += 1

        score = 0.0
        for t in query_tokens:
            if t in tf_map:
                tf = tf_map[t]
                numerator = tf * (k1 + 1)
                denominator = tf + k1 * (1 - b + b * dl / max(avg_dl, 1))
                score += idf.get(t, 0) * (numerator / denominator)

        if score > 0:
            scores.append((score, doc))

    scores.sort(key=lambda x: -x[0])
    return [doc for _, doc in scores[:top_k]]


def vector_code_searcher(
    query: str,
    file_ext: str = ".py",
    search_root: str = None,
    top_k: int = 10,
    context_lines: int = 3
) -> str:
    """
    AMEVA 프로젝트 소스코드 전역을 BM25 알고리즘으로 검색하여
    질의어와 가장 유관한 코드 조각과 함수/클래스를 반환한다.
    
    query: 검색어 (자연어 또는 코드 키워드)
    file_ext: 검색할 파일 확장자 (기본: .py, 여러 개: ".py,.js,.ts")
    search_root: 검색 루트 경로 (기본: C:\\ameva)
    top_k: 반환할 최대 파일 수
    context_lines: 매칭 라인 주변 컨텍스트 줄 수
    """
    if not query or not query.strip():
        return "Error: query cannot be empty."

    base = search_root or AMEVA_BASE
    base_norm = os.path.abspath(base)
    if not base_norm.lower().startswith(r"c:\ameva"):
        return f"Security Error: search_root must be under C:\\ameva. Got: {base_norm}"

    # 확장자 파싱
    extensions = [e.strip().lower() for e in file_ext.split(",")]
    if not all(e.startswith(".") for e in extensions):
        return f"Error: file_ext must start with '.' (e.g., '.py' or '.py,.js')"

    # 파일 수집
    corpus = []
    file_count = 0
    for root, dirs, files in os.walk(base_norm):
        # 제외 폴더
        dirs[:] = [d for d in dirs if d not in {
            "__pycache__", ".git", "node_modules", ".venv", "venv",
            "dist", "build", ".mypy_cache", ".pytest_cache"
        }]
        for fname in files:
            if any(fname.lower().endswith(ext) for ext in extensions):
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                    text = "".join(lines)
                    corpus.append({
                        "path": fpath,
                        "text": text,
                        "lines": [(i + 1, l.rstrip()) for i, l in enumerate(lines)]
                    })
                    file_count += 1
                except Exception:
                    continue

    if not corpus:
        return f"No files with extension(s) '{file_ext}' found under {base_norm}."

    # BM25 검색
    results = _tf_idf_search(query, corpus, top_k=top_k)

    if not results:
        return f"No results found for query: '{query}'"

    # 결과 포맷
    report = (
        f"## 🔍 Code Searcher Results\n\n"
        f"**Query**: `{query}`  \n"
        f"**Extension(s)**: `{file_ext}`  \n"
        f"**Files Indexed**: {file_count}  \n"
        f"**Top Results**: {len(results)}\n\n"
    )
    report += "---\n\n"

    query_tokens = set(re.findall(r"[a-zA-Z_]\w*", query.lower()))

    for rank, doc in enumerate(results, 1):
        path = doc["path"]
        rel_path = os.path.relpath(path, AMEVA_BASE)
        all_lines = doc["lines"]

        # 쿼리 토큰과 매칭되는 라인 탐색
        matching_lines = []
        for lineno, line in all_lines:
            line_tokens = set(re.findall(r"[a-zA-Z_]\w*", line.lower()))
            if query_tokens & line_tokens:
                matching_lines.append(lineno)

        report += f"### #{rank} `{rel_path}`\n\n"

        if matching_lines:
            # 첫 번째 매칭 라인 주변 컨텍스트 출력
            for match_lineno in matching_lines[:3]:
                start = max(0, match_lineno - 1 - context_lines)
                end = min(len(all_lines), match_lineno + context_lines)
                snippet_lines = all_lines[start:end]

                report += f"*Line {match_lineno}:*\n```{file_ext.split(',')[0][1:]}\n"
                for lno, ltext in snippet_lines:
                    marker = ">>>" if lno == match_lineno else "   "
                    report += f"{marker} {lno:4d} | {ltext}\n"
                report += "```\n\n"
        else:
            # 파일 상위 표시
            preview_lines = all_lines[:10]
            report += "```\n"
            for lno, ltext in preview_lines:
                report += f"{lno:4d} | {ltext}\n"
            report += "```\n\n"

        report += "---\n\n"

    return report.strip()
```

---

### File: `src/tools/search/__init__.py`
```python
# search tools package
```

---

### File: `src/tools/ssh/ssh_manager.py`
```python
import paramiko
import logging
import io

logger = logging.getLogger(__name__)

def ssh_run_command(host: str, username: str, command: str, port: int = 22, password: str = None, key_content: str = None) -> str:
    """Run a shell command on a remote server via SSH."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        if key_content:
            key_file = io.StringIO(key_content.strip())
            # Try RSA key first, fallback to Ed25519/ECDSA
            try:
                pkey = paramiko.RSAKey.from_private_key(key_file)
            except Exception:
                key_file.seek(0)
                try:
                    pkey = paramiko.Ed25519Key.from_private_key(key_file)
                except Exception:
                    key_file.seek(0)
                    pkey = paramiko.ECDSAKey.from_private_key(key_file)
            client.connect(hostname=host, port=port, username=username, pkey=pkey, timeout=15)
        elif password:
            client.connect(hostname=host, port=port, username=username, password=password, timeout=15)
        else:
            return "Error: Either password or key_content must be provided for SSH authentication."
            
        stdin, stdout, stderr = client.exec_command(command, timeout=30)
        
        out = stdout.read().decode('utf-8', errors='replace')
        err = stderr.read().decode('utf-8', errors='replace')
        exit_status = stdout.channel.recv_exit_status()
        
        client.close()
        
        if exit_status != 0:
            return f"SSH Command Failed (exit code {exit_status}):\nStdout: {out}\nStderr: {err}"
        return out if out else "Command executed successfully with no output."
        
    except Exception as e:
        return f"SSH Connection/Execution Error: {str(e)}"
```

---

### File: `src/tools/utils/README.md`
```markdown
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
```

---

### File: `src/tools/utils/utils_manager.py`
```python
import os
import psutil
import socket
import uuid
import json
import base64
import hashlib
import requests
import subprocess
import platform
import threading
import time
import re
from datetime import datetime
from urllib.parse import urlparse


# ──────────────────────────────────────────────
# 기존 유틸리티 (유지)
# ──────────────────────────────────────────────

def get_system_info() -> str:
    """Retrieve host system information (CPU, Memory, Disk, OS)."""
    try:
        cpu_pct = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('C:\\' if os.name == 'nt' else '/')
        os_info = f"{os.name} ({psutil.users()[0].name if psutil.users() else 'Unknown'})"
        
        info = (
            f"OS: {os_info}\n"
            f"CPU Usage: {cpu_pct}%\n"
            f"RAM: Total={mem.total // (1024**2)}MB, Available={mem.available // (1024**2)}MB, Used={mem.percent}%\n"
            f"Disk (System): Total={disk.total // (1024**3)}GB, Free={disk.free // (1024**3)}GB, Used={disk.percent}%"
        )
        return info
    except Exception as e:
        return f"Error getting system info: {str(e)}"

def check_port(host: str, port: int) -> str:
    """Check if a specific TCP port on a host is open/active."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3.0)
    try:
        result = sock.connect_ex((host, port))
        if result == 0:
            return f"Port {port} on {host} is OPEN."
        else:
            return f"Port {port} on {host} is CLOSED (code {result})."
    except Exception as e:
        return f"Error checking port: {str(e)}"
    finally:
        sock.close()

def generate_uuid() -> str:
    """Generate a random UUID v4."""
    return str(uuid.uuid4())

def format_json(json_str: str) -> str:
    """Format and validate a JSON string (pretty print)."""
    try:
        parsed = json.loads(json_str)
        return json.dumps(parsed, indent=2, ensure_ascii=False)
    except json.JSONDecodeError as je:
        return f"Invalid JSON format. Error: {je.msg} at line {je.lineno}, col {je.colno}"
    except Exception as e:
        return f"Error parsing JSON: {str(e)}"

def base64_encode_decode(mode: str, data: str) -> str:
    """Encode or decode base64 strings. mode can be 'encode' or 'decode'."""
    try:
        if mode == 'encode':
            return base64.b64encode(data.encode('utf-8')).decode('utf-8')
        elif mode == 'decode':
            return base64.b64decode(data.encode('utf-8')).decode('utf-8')
        else:
            return "Error: Mode must be 'encode' or 'decode'."
    except Exception as e:
        return f"Error: {str(e)}"

def map_path_to_container(path: str) -> str:
    """Map Windows host path to Docker container path (/app/workspace)."""
    normalized = path.replace("\\", "/")
    return re.sub(r'^[Cc]:/ameva', '/app/workspace', normalized)

def docker_calculate_file_hash(file_path: str, algorithm: str = "sha256") -> str:
    """Calculate file checksum hash inside a Docker container for isolation."""
    container_path = map_path_to_container(file_path)
    prog = "sha256sum" if algorithm.lower() == "sha256" else "md5sum"
    cmd = [
        "docker", "run", "--rm",
        "-v", r"C:\ameva:/app/workspace",
        "alpine",
        prog, container_path
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=20, stdin=subprocess.DEVNULL)
        if res.returncode != 0:
            return f"Error calculating hash in Docker: {res.stderr.strip()}"
        return res.stdout.strip()
    except Exception as e:
        return f"Exception calculating file hash: {str(e)}"

def get_external_ip() -> str:
    """Retrieve the host's external IP address and internal network IP."""
    internal_ip = "Unknown"
    external_ip = "Unknown"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        internal_ip = s.getsockname()[0]
        s.close()
    except Exception:
        pass
        
    try:
        res = requests.get("https://api.ipify.org?format=json", timeout=5)
        if res.status_code == 200:
            external_ip = res.json().get("ip", "Unknown")
    except Exception:
        pass
        
    return f"Internal IP: {internal_ip}\nExternal IP: {external_ip}"

def send_http_request(method: str, url: str, headers_json: str = None, body: str = None) -> str:
    """Send an arbitrary HTTP request (GET/POST/PUT/DELETE) and return status/body."""
    try:
        headers = json.loads(headers_json) if headers_json else {}
        method_upper = method.upper()
        
        res = requests.request(
            method=method_upper,
            url=url,
            headers=headers,
            data=body,
            timeout=15
        )
        
        preview = res.text[:1000] + "\n... (truncated)" if len(res.text) > 1000 else res.text
        return f"Status: {res.status_code} {res.reason}\nHeaders: {dict(res.headers)}\nResponse:\n{preview}"
    except Exception as e:
        return f"HTTP Request Error: {str(e)}"

def docker_find_large_files(dir_path: str, size_mb: int = 50) -> str:
    """Find files larger than size_mb MB inside the directory, running in Docker."""
    container_path = map_path_to_container(dir_path)
    find_arg = f"+{size_mb}M"
    cmd = [
        "docker", "run", "--rm",
        "-v", r"C:\ameva:/app/workspace",
        "alpine",
        "find", container_path, "-type", "f", "-size", find_arg
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30, stdin=subprocess.DEVNULL)
        if res.returncode != 0:
            return f"Error finding large files in Docker: {res.stderr.strip()}"
        out = res.stdout.strip()
        if not out:
            return f"No files larger than {size_mb}MB found in {dir_path}."
        return f"Files larger than {size_mb}MB in {dir_path}:\n{out}"
    except Exception as e:
        return f"Exception finding large files: {str(e)}"

def extract_text_from_url(url: str) -> str:
    """Fetch URL and extract raw body text, stripping all HTML tags."""
    try:
        from bs4 import BeautifulSoup
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AMEVA-Agent/1.0"}
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return f"Error: HTTP {res.status_code}"
            
        soup = BeautifulSoup(res.text, "html.parser")
        for script in soup(["script", "style"]):
            script.decompose()
            
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = "\n".join(chunk for chunk in chunks if chunk)
        
        return clean_text[:3000] + "\n... (truncated to 3000 chars)" if len(clean_text) > 3000 else clean_text
    except Exception as e:
        return f"Error extracting text: {str(e)}"


# ──────────────────────────────────────────────
# 신규 유틸리티 (고도화 추가)
# ──────────────────────────────────────────────

def gpu_monitor() -> str:
    """
    nvidia-smi를 통해 실시간 GPU 상태를 조회한다.
    GPU명, 사용률, VRAM 점유율, 온도, 전력을 표 형식으로 반환.
    """
    try:
        # nvidia-smi query
        query_fields = (
            "index,name,utilization.gpu,memory.used,memory.total,"
            "temperature.gpu,power.draw,power.limit,driver_version"
        )
        cmd = [
            "nvidia-smi",
            f"--query-gpu={query_fields}",
            "--format=csv,noheader,nounits"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=10, stdin=subprocess.DEVNULL)
        
        if res.returncode != 0:
            # GPU가 없거나 nvidia-smi 미설치 — 대안으로 wmic 시도 (Windows)
            if os.name == "nt":
                wmic_cmd = ["wmic", "path", "Win32_VideoController", "get",
                           "Name,AdapterRAM,VideoMemoryType", "/format:list"]
                wmic = subprocess.run(wmic_cmd, capture_output=True, text=True, timeout=10, stdin=subprocess.DEVNULL)
                if wmic.returncode == 0:
                    return f"nvidia-smi not available. GPU info via WMI:\n{wmic.stdout.strip()}"
            return f"GPU monitor unavailable: {res.stderr.strip() or 'nvidia-smi not found'}"
        
        lines = [l.strip() for l in res.stdout.strip().split("\n") if l.strip()]
        if not lines:
            return "No GPU devices detected."
        
        report = "## 🖥️ GPU Monitor\n\n"
        report += "| # | GPU | Util% | VRAM Used | VRAM Total | Temp°C | Power | Driver |\n"
        report += "| :- | :-- | :---: | :-------: | :--------: | :----: | :---- | :----- |\n"
        
        for line in lines:
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 9:
                idx, name, util, vram_used, vram_total, temp, pwr_draw, pwr_limit, drv = parts[:9]
                vram_pct = round(int(vram_used) / int(vram_total) * 100, 1) if vram_total.isdigit() else "?"
                report += (
                    f"| {idx} | {name} | {util}% | {vram_used}MB ({vram_pct}%) | "
                    f"{vram_total}MB | {temp}°C | {pwr_draw}W / {pwr_limit}W | {drv} |\n"
                )
        
        return report

    except FileNotFoundError:
        return "Error: nvidia-smi is not installed or not in PATH."
    except Exception as e:
        return f"Error in gpu_monitor: {str(e)}"


def system_thermal_scanner() -> str:
    """
    CPU 온도, 클럭, 코어별 사용률을 스캔한다.
    Windows: WMI, Linux/Mac: psutil sensors 활용.
    """
    try:
        report = "## 🌡️ System Thermal & Clock Scanner\n\n"
        
        # CPU 기본 정보
        cpu_freq = psutil.cpu_freq()
        cpu_pct_per_core = psutil.cpu_percent(interval=0.5, percpu=True)
        cpu_count_logical = psutil.cpu_count(logical=True)
        cpu_count_physical = psutil.cpu_count(logical=False)

        report += f"**CPU Cores**: Physical={cpu_count_physical}, Logical={cpu_count_logical}\n"
        if cpu_freq:
            report += (
                f"**Clock**: Current={cpu_freq.current:.0f}MHz, "
                f"Min={cpu_freq.min:.0f}MHz, Max={cpu_freq.max:.0f}MHz\n\n"
            )

        # 코어별 사용률 테이블
        report += "### Core Usage\n"
        report += "| Core | Usage% |\n| :--- | :----: |\n"
        for i, pct in enumerate(cpu_pct_per_core):
            bar = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
            report += f"| Core {i} | {bar} {pct:.1f}% |\n"

        # 온도 센서 (Linux/Mac)
        if hasattr(psutil, "sensors_temperatures"):
            temps = psutil.sensors_temperatures()
            if temps:
                report += "\n### Temperature Sensors\n"
                report += "| Sensor | Label | Current°C | High°C | Critical°C |\n"
                report += "| :----- | :---- | :-------: | :----: | :--------: |\n"
                for name, entries in temps.items():
                    for entry in entries:
                        report += (
                            f"| {name} | {entry.label or '-'} | "
                            f"{entry.current:.1f} | "
                            f"{entry.high or '-'} | "
                            f"{entry.critical or '-'} |\n"
                        )
            else:
                report += "\n*Temperature sensors not accessible on this system.*\n"
        else:
            # Windows — WMI 시도
            if os.name == "nt":
                try:
                    wmi_cmd = (
                        'powershell -Command "Get-WmiObject MSAcpi_ThermalZoneTemperature '
                        '-Namespace root/wmi | Select-Object CurrentTemperature | '
                        'ForEach-Object { ($_.CurrentTemperature / 10 - 273.15).ToString(\'F1\') }"'
                    )
                    wmi_res = subprocess.run(wmi_cmd, shell=True, capture_output=True, text=True, timeout=10)
                    if wmi_res.returncode == 0 and wmi_res.stdout.strip():
                        report += f"\n**CPU Temperature (WMI)**: {wmi_res.stdout.strip()}°C\n"
                    else:
                        report += "\n*WMI thermal sensor not accessible (admin required).*\n"
                except Exception:
                    report += "\n*Temperature data unavailable on Windows without admin.*\n"

        return report

    except Exception as e:
        return f"Error in system_thermal_scanner: {str(e)}"


def process_watchdog(action: str, process_name: str = None) -> str:
    """
    활성 프로세스 목록 스캔, 특정 프로세스 감시, 강제 종료를 수행한다.
    action: 'list' | 'find' | 'kill' | 'restart'
    process_name: 대상 프로세스명 (find/kill/restart 시 필요)
    """
    try:
        if action == "list":
            procs = []
            for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_info", "status"]):
                try:
                    info = proc.info
                    mem_mb = info["memory_info"].rss // (1024 * 1024) if info["memory_info"] else 0
                    procs.append((info["pid"], info["name"], info["cpu_percent"], mem_mb, info["status"]))
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            # CPU 사용률 기준 내림차순 정렬
            procs.sort(key=lambda x: x[2], reverse=True)
            
            report = "## ⚙️ Active Process Watchdog\n\n"
            report += f"**Total Processes**: {len(procs)}\n\n"
            report += "| PID | Name | CPU% | Mem(MB) | Status |\n"
            report += "| :-- | :--- | :--: | :-----: | :----- |\n"
            for pid, name, cpu, mem, status in procs[:30]:
                report += f"| {pid} | {name} | {cpu:.1f} | {mem} | {status} |\n"
            if len(procs) > 30:
                report += f"\n*... and {len(procs) - 30} more processes*\n"
            return report

        elif action == "find":
            if not process_name:
                return "Error: process_name is required for 'find' action."
            
            found = []
            for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_info", "status", "cmdline"]):
                try:
                    if process_name.lower() in proc.info["name"].lower():
                        mem_mb = proc.info["memory_info"].rss // (1024 * 1024) if proc.info["memory_info"] else 0
                        cmdline = " ".join(proc.info["cmdline"] or [])[:80]
                        found.append(f"PID={proc.info['pid']}, Name={proc.info['name']}, "
                                     f"CPU={proc.info['cpu_percent']:.1f}%, Mem={mem_mb}MB, "
                                     f"Status={proc.info['status']}\nCMD: {cmdline}")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if not found:
                return f"No process matching '{process_name}' found."
            return f"### Found {len(found)} process(es) matching '{process_name}':\n\n" + "\n---\n".join(found)

        elif action == "kill":
            if not process_name:
                return "Error: process_name is required for 'kill' action."
            
            killed = []
            for proc in psutil.process_iter(["pid", "name"]):
                try:
                    if process_name.lower() in proc.info["name"].lower():
                        proc.terminate()
                        killed.append(f"PID={proc.info['pid']}, Name={proc.info['name']}")
                except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                    killed.append(f"Failed to kill PID={proc.info.get('pid','?')}: {e}")
            
            if not killed:
                return f"No process matching '{process_name}' found to kill."
            return f"### Terminated {len(killed)} process(es):\n" + "\n".join(killed)

        else:
            return f"Error: Unknown action '{action}'. Use 'list', 'find', or 'kill'."

    except Exception as e:
        return f"Error in process_watchdog: {str(e)}"


def task_cron_scheduler(action: str, job_name: str = None, cron_expression: str = None, command: str = None) -> str:
    """
    Windows Task Scheduler 또는 cron 작업을 관리한다.
    action: 'list' | 'create' | 'delete' | 'run'
    Windows 환경에서는 schtasks 커맨드를 래핑한다.
    """
    try:
        if os.name != "nt":
            # Linux/Mac: crontab 기반
            if action == "list":
                res = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=10)
                if res.returncode != 0:
                    return "No crontab found for current user."
                return f"### Current Crontab:\n```\n{res.stdout.strip()}\n```"
            elif action == "create":
                if not job_name or not cron_expression or not command:
                    return "Error: job_name, cron_expression, and command are all required for 'create'."
                # 기존 crontab 읽기 후 추가
                existing = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
                existing_content = existing.stdout if existing.returncode == 0 else ""
                new_line = f"{cron_expression} {command} # AMEVA:{job_name}\n"
                new_content = existing_content + new_line
                proc = subprocess.run(["crontab", "-"], input=new_content, text=True, timeout=10)
                if proc.returncode == 0:
                    return f"Cron job '{job_name}' created: `{cron_expression} {command}`"
                return f"Error creating cron job: {proc.stderr}"
            elif action == "delete":
                if not job_name:
                    return "Error: job_name is required for 'delete'."
                existing = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
                if existing.returncode != 0:
                    return "No crontab to delete from."
                lines = [l for l in existing.stdout.splitlines() if f"# AMEVA:{job_name}" not in l]
                subprocess.run(["crontab", "-"], input="\n".join(lines) + "\n", text=True, timeout=10)
                return f"Cron job '{job_name}' deleted."
            else:
                return f"Unknown action '{action}' for cron."

        # Windows: schtasks
        if action == "list":
            res = subprocess.run(
                ["schtasks", "/query", "/fo", "TABLE", "/nh"],
                capture_output=True, text=True, timeout=15, stdin=subprocess.DEVNULL
            )
            if res.returncode != 0:
                return f"Error listing tasks: {res.stderr.strip()}"
            lines = res.stdout.strip().splitlines()
            report = f"### Scheduled Tasks ({len(lines)} found)\n```\n"
            report += "\n".join(lines[:50])
            if len(lines) > 50:
                report += f"\n... ({len(lines)-50} more)"
            report += "\n```"
            return report

        elif action == "create":
            if not job_name or not command:
                return "Error: job_name and command are required for 'create'."
            # cron_expression을 Windows 스케줄로 간단 변환 (분 단위)
            trigger = "/SC MINUTE /MO 60"  # 기본: 1시간마다
            if cron_expression:
                parts = cron_expression.split()
                if len(parts) >= 2 and parts[0] == "*" and parts[1] == "*":
                    trigger = "/SC MINUTE /MO 1"
                elif len(parts) >= 2 and parts[1].isdigit():
                    trigger = f"/SC DAILY /ST {int(parts[1]):02d}:00"
            
            cmd_str = (
                f'schtasks /create /tn "AMEVA\\{job_name}" /tr "{command}" '
                f'{trigger} /f'
            )
            res = subprocess.run(cmd_str, shell=True, capture_output=True, text=True, timeout=15)
            if res.returncode == 0:
                return f"Task '{job_name}' created successfully."
            return f"Error creating task: {res.stderr.strip()}"

        elif action == "delete":
            if not job_name:
                return "Error: job_name is required for 'delete'."
            res = subprocess.run(
                ["schtasks", "/delete", "/tn", f"AMEVA\\{job_name}", "/f"],
                capture_output=True, text=True, timeout=10, stdin=subprocess.DEVNULL
            )
            if res.returncode == 0:
                return f"Task '{job_name}' deleted."
            return f"Error deleting task: {res.stderr.strip()}"

        elif action == "run":
            if not job_name:
                return "Error: job_name is required for 'run'."
            res = subprocess.run(
                ["schtasks", "/run", "/tn", f"AMEVA\\{job_name}"],
                capture_output=True, text=True, timeout=10, stdin=subprocess.DEVNULL
            )
            if res.returncode == 0:
                return f"Task '{job_name}' triggered manually."
            return f"Error running task: {res.stderr.strip()}"

        else:
            return f"Error: Unknown action '{action}'. Use 'list', 'create', 'delete', or 'run'."

    except Exception as e:
        return f"Error in task_cron_scheduler: {str(e)}"


def rest_client_simulator(method: str, url: str, payload_json: str = None, headers_json: str = None) -> str:
    """
    REST API 모의 요청 클라이언트. curl 없이 REST API를 테스트한다.
    응답을 보기 좋은 포맷으로 반환하며 curl 등가 명령어도 출력한다.
    """
    try:
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            return f"Error: Invalid URL '{url}'"

        headers = json.loads(headers_json) if headers_json else {}
        payload = None
        if payload_json:
            try:
                payload = json.loads(payload_json)
                if "Content-Type" not in headers:
                    headers["Content-Type"] = "application/json"
            except json.JSONDecodeError:
                payload = payload_json  # raw string

        method_upper = method.upper()

        # curl 등가 명령어 생성
        curl_headers = " ".join([f'-H "{k}: {v}"' for k, v in headers.items()])
        curl_body = f"-d '{payload_json}'" if payload_json else ""
        curl_equiv = f"curl -X {method_upper} {curl_headers} {curl_body} \"{url}\""

        # 요청 실행
        start = time.time()
        if isinstance(payload, dict):
            res = requests.request(method_upper, url, headers=headers, json=payload, timeout=15)
        else:
            res = requests.request(method_upper, url, headers=headers, data=payload, timeout=15)
        elapsed_ms = round((time.time() - start) * 1000, 1)

        # 응답 파싱
        content_type = res.headers.get("Content-Type", "")
        try:
            if "json" in content_type:
                body_parsed = json.dumps(res.json(), indent=2, ensure_ascii=False)
            else:
                body_parsed = res.text[:2000]
        except Exception:
            body_parsed = res.text[:2000]

        report = (
            f"## 🌐 REST Client Simulator\n\n"
            f"**Request**: `{method_upper} {url}`  \n"
            f"**Status**: `{res.status_code} {res.reason}`  \n"
            f"**Response Time**: `{elapsed_ms}ms`  \n"
            f"**Content-Type**: `{content_type}`  \n\n"
            f"### Response Headers\n```\n"
        )
        for k, v in dict(res.headers).items():
            report += f"{k}: {v}\n"
        report += f"```\n\n### Response Body\n```json\n{body_parsed}\n```\n\n"
        report += f"### curl Equivalent\n```bash\n{curl_equiv}\n```\n"

        return report

    except requests.exceptions.Timeout:
        return f"Error: Request to {url} timed out after 15 seconds."
    except requests.exceptions.ConnectionError as e:
        return f"Error: Could not connect to {url}. {str(e)}"
    except Exception as e:
        return f"Error in rest_client_simulator: {str(e)}"


def html_to_pdf_renderer(html_path_or_url: str, output_pdf_path: str) -> str:
    """
    HTML 파일 또는 URL을 PDF로 변환한다.
    우선순위: weasyprint → pdfkit(wkhtmltopdf) → 불가 시 안내 메시지.
    출력 경로는 C:\\ameva 하위만 허용.
    """
    # 출력 경로 보안 검사
    out_norm = os.path.abspath(output_pdf_path)
    if not out_norm.lower().startswith(r"c:\ameva"):
        return f"Security Error: Output path must be under C:\\ameva. Got: {out_norm}"

    os.makedirs(os.path.dirname(out_norm), exist_ok=True) if os.path.dirname(out_norm) else None

    # 입력 소스 결정
    is_url = html_path_or_url.startswith("http://") or html_path_or_url.startswith("https://")
    if not is_url:
        src_norm = os.path.abspath(html_path_or_url)
        if not src_norm.lower().startswith(r"c:\ameva"):
            return f"Security Error: Source path must be under C:\\ameva. Got: {src_norm}"
        if not os.path.exists(src_norm):
            return f"Error: HTML file not found at {src_norm}"
        source = f"file:///{src_norm.replace(chr(92), '/')}"
    else:
        source = html_path_or_url

    # 방법 1: weasyprint
    try:
        import weasyprint
        if is_url:
            weasyprint.HTML(url=source).write_pdf(out_norm)
        else:
            weasyprint.HTML(filename=os.path.abspath(html_path_or_url)).write_pdf(out_norm)
        size_kb = os.path.getsize(out_norm) // 1024
        return f"✅ PDF rendered via WeasyPrint.\nOutput: {out_norm} ({size_kb}KB)"
    except ImportError:
        pass
    except Exception as e:
        pass

    # 방법 2: pdfkit (wkhtmltopdf wrapper)
    try:
        import pdfkit
        pdfkit.from_url(source, out_norm)
        size_kb = os.path.getsize(out_norm) // 1024
        return f"✅ PDF rendered via pdfkit (wkhtmltopdf).\nOutput: {out_norm} ({size_kb}KB)"
    except ImportError:
        pass
    except Exception as e:
        pass

    # 방법 3: Windows — Edge/Chrome CLI headless
    if os.name == "nt":
        edge_paths = [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        ]
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
        for browser_path in edge_paths + chrome_paths:
            if os.path.exists(browser_path):
                try:
                    cmd = [
                        browser_path,
                        "--headless",
                        "--disable-gpu",
                        f"--print-to-pdf={out_norm}",
                        source
                    ]
                    res = subprocess.run(cmd, capture_output=True, timeout=30, stdin=subprocess.DEVNULL)
                    if os.path.exists(out_norm) and os.path.getsize(out_norm) > 0:
                        size_kb = os.path.getsize(out_norm) // 1024
                        return f"✅ PDF rendered via {os.path.basename(browser_path)} headless.\nOutput: {out_norm} ({size_kb}KB)"
                except Exception:
                    continue

    return (
        "⚠️ HTML to PDF conversion failed. No compatible renderer found.\n"
        "Install one of the following:\n"
        "  pip install weasyprint\n"
        "  pip install pdfkit  (requires wkhtmltopdf binary)\n"
        "  Or ensure Microsoft Edge / Google Chrome is installed."
    )
```

---

### File: `src/tools/web/crawl_bot.py`
```python
import os
import subprocess
import re
import math
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup


def web_readability_cleaner(url: str) -> str:
    """
    웹 페이지에서 광고, 네비게이션, 사이드바 등을 제거하고
    본문 콘텐츠만 추출해 깔끔한 마크다운으로 변환한다.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AMEVA-Reader/1.0"
        }
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return f"Error: HTTP {res.status_code} {res.reason}"

        soup = BeautifulSoup(res.text, "html.parser")

        # 노이즈 태그 제거 (광고, 네비, 푸터, 사이드바, 스크립트 등)
        noise_tags = [
            "script", "style", "noscript", "header", "footer", "nav",
            "aside", "form", "iframe", "button", "svg", "img",
            "figure", "figcaption", "advertisement", "ads", "banner"
        ]
        noise_classes = [
            "nav", "navigation", "sidebar", "menu", "footer", "header",
            "ad", "advertisement", "banner", "cookie", "popup", "modal",
            "social", "share", "comment", "related", "breadcrumb"
        ]

        for tag in soup(noise_tags):
            tag.decompose()

        # 클래스 기반 노이즈 제거
        for cls in noise_classes:
            for el in soup.find_all(class_=re.compile(cls, re.IGNORECASE)):
                el.decompose()

        # 본문 후보 탐색 (article > main > body 순)
        content_el = (
            soup.find("article") or
            soup.find("main") or
            soup.find(id=re.compile(r"(content|main|article|post)", re.IGNORECASE)) or
            soup.find(class_=re.compile(r"(content|main|article|post)", re.IGNORECASE)) or
            soup.body
        )

        if not content_el:
            return "Error: Could not extract readable content from this page."

        # HTML → Markdown 변환
        markdown_lines = []
        title_tag = soup.title
        if title_tag:
            markdown_lines.append(f"# {title_tag.string.strip()}\n")
            markdown_lines.append(f"> Source: {url}\n")
            markdown_lines.append("---\n")

        for el in content_el.descendants:
            if not hasattr(el, "name"):
                continue
            if el.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                level = int(el.name[1])
                text = el.get_text(strip=True)
                if text:
                    markdown_lines.append(f"\n{'#' * level} {text}\n")
            elif el.name == "p":
                text = el.get_text(strip=True)
                if text and len(text) > 20:
                    markdown_lines.append(f"\n{text}\n")
            elif el.name in ["ul", "ol"]:
                for li in el.find_all("li", recursive=False):
                    text = li.get_text(strip=True)
                    if text:
                        markdown_lines.append(f"- {text}")
            elif el.name == "pre":
                code = el.get_text()
                markdown_lines.append(f"\n```\n{code.strip()}\n```\n")
            elif el.name == "blockquote":
                text = el.get_text(strip=True)
                if text:
                    markdown_lines.append(f"\n> {text}\n")

        result = "\n".join(markdown_lines)
        result = re.sub(r"\n{3,}", "\n\n", result)

        if len(result) > 5000:
            return result[:5000] + "\n\n... (truncated to 5000 chars)"
        return result if result.strip() else "No readable content found."

    except Exception as e:
        return f"Error in web_readability_cleaner: {str(e)}"


def dead_link_scanner(md_file_path: str) -> str:
    """
    마크다운 파일 내의 모든 URL 링크를 추출하고 
    HTTP HEAD 요청으로 응답 상태를 전수 검사한다 (404 데드링크 식별).
    """
    # 경로 보안 검사
    normalized = os.path.abspath(md_file_path)
    if not normalized.lower().startswith(r"c:\ameva"):
        return f"Security Error: Access to path '{normalized}' is denied."

    if not os.path.exists(normalized):
        return f"Error: File not found at {md_file_path}"

    try:
        with open(normalized, "r", encoding="utf-8") as f:
            content = f.read()

        # 마크다운 링크 패턴: [text](url) 및 bare URL
        url_pattern = re.compile(
            r"\[.*?\]\((https?://[^\s\)]+)\)|"
            r"(?<!\()(https?://[^\s\)>\]\"\',]+)"
        )
        found_urls = list(set(url_pattern.findall(content)))
        # findall은 그룹 튜플 반환 — flatten
        flat_urls = []
        for match in found_urls:
            if isinstance(match, tuple):
                flat_urls.extend([m for m in match if m])
            else:
                flat_urls.append(match)
        flat_urls = list(set(flat_urls))

        if not flat_urls:
            return f"No URLs found in {md_file_path}."

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AMEVA-LinkChecker/1.0"
        }

        results = {"alive": [], "dead": [], "error": []}

        for url in flat_urls:
            try:
                r = requests.head(url, headers=headers, timeout=8, allow_redirects=True)
                if r.status_code < 400:
                    results["alive"].append({"url": url, "status": r.status_code})
                else:
                    results["dead"].append({"url": url, "status": r.status_code})
            except requests.exceptions.ConnectionError:
                results["dead"].append({"url": url, "status": "CONNECTION_ERROR"})
            except requests.exceptions.Timeout:
                results["error"].append({"url": url, "status": "TIMEOUT"})
            except Exception as ex:
                results["error"].append({"url": url, "status": str(ex)[:50]})

        total = len(flat_urls)
        report = (
            f"## 🔗 Dead Link Scanner Report\n"
            f"**File**: `{md_file_path}`  \n"
            f"**Total URLs scanned**: {total}  \n"
            f"**✅ Alive**: {len(results['alive'])}  \n"
            f"**❌ Dead**: {len(results['dead'])}  \n"
            f"**⚠️ Error**: {len(results['error'])}\n\n"
        )

        if results["dead"]:
            report += "### ❌ Dead Links\n"
            report += "| URL | Status |\n| :--- | :--- |\n"
            for item in results["dead"]:
                report += f"| `{item['url']}` | `{item['status']}` |\n"
            report += "\n"

        if results["error"]:
            report += "### ⚠️ Error Links\n"
            report += "| URL | Reason |\n| :--- | :--- |\n"
            for item in results["error"]:
                report += f"| `{item['url']}` | `{item['status']}` |\n"
            report += "\n"

        if results["alive"]:
            report += "### ✅ Alive Links\n"
            report += "| URL | Status |\n| :--- | :--- |\n"
            for item in results["alive"][:20]:  # 최대 20개 표시
                report += f"| `{item['url']}` | `{item['status']}` |\n"
            if len(results["alive"]) > 20:
                report += f"| ... | ({len(results['alive']) - 20} more) |\n"

        return report

    except Exception as e:
        return f"Error in dead_link_scanner: {str(e)}"


def crawl_website(url: str, selector: str = None) -> str:
    """
    Crawls a website URL, extracts the Title, Metadata, clean Text content, 
    and lists all unique internal & external links.
    Optionally filters by a CSS selector.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AMEVA-Crawler/1.0"
        }
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return f"Error crawling {url}: HTTP {res.status_code} {res.reason}"
            
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 1. Metadata
        title = soup.title.string.strip() if soup.title else "No Title"
        meta_desc = ""
        desc_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
        if desc_tag:
            meta_desc = desc_tag.get("content", "").strip()
            
        # 2. Main Content (filter by selector if provided)
        content_soup = soup
        if selector:
            selected = soup.select(selector)
            if selected:
                content_soup = BeautifulSoup("".join(str(s) for s in selected), 'html.parser')
                
        # Strip script/style
        for tag in content_soup(["script", "style", "meta", "noscript", "header", "footer"]):
            tag.decompose()
            
        raw_text = content_soup.get_text()
        lines = (line.strip() for line in raw_text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = "\n".join(chunk for chunk in chunks if chunk)
        
        # 3. Links analysis
        parsed_base = urlparse(url)
        base_domain = parsed_base.netloc
        
        internal_links = set()
        external_links = set()
        
        for link in soup.find_all("a", href=True):
            href = link.get("href").strip()
            if not href or href.startswith("#") or href.startswith("javascript:"):
                continue
            full_url = urljoin(url, href)
            parsed_link = urlparse(full_url)
            
            if parsed_link.netloc == base_domain:
                internal_links.add(full_url)
            else:
                external_links.add(full_url)
                
        # Format the output
        summary = (
            f"=== CRAWL REPORT FOR: {url} ===\n"
            f"Title: {title}\n"
            f"Meta Description: {meta_desc}\n\n"
            f"--- CLEAN TEXT CONTENT (Preview) ---\n"
            f"{clean_text[:1200]}\n"
            f"... (Truncated, total length: {len(clean_text)} chars)\n\n"
            f"--- LINKS ANALYSIS ---\n"
            f"Internal Links found: {len(internal_links)}\n"
            f"External Links found: {len(external_links)}\n"
        )
        
        if internal_links:
            summary += "\nInternal Links sample (max 5):\n" + "\n".join(list(internal_links)[:5])
        if external_links:
            summary += "\nExternal Links sample (max 5):\n" + "\n".join(list(external_links)[:5])
            
        return summary
    except Exception as e:
        return f"Exception while crawling {url}: {str(e)}"
```

---

### File: `src/utils/audit_logger.py`
```python
import os
import json
import time
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

AUDIT_LOG_PATH = "/app/workspace/AMEVA-MCP-Toolkit-Utils/mcp_audit.jsonl" if os.environ.get("AMEVA_IN_CONTAINER") == "true" else r"C:\ameva\AMEVA-MCP-Toolkit-Utils\mcp_audit.jsonl"

MAX_RETRIES = 5
RETRY_DELAY = 0.01  # 10ms

def log_mcp_action(tool_name: str, args: dict, result: str, status: str = "success", caller: str = "Unknown"):
    """
    Append an audit log record to a JSONL file using a Spin Lock to handle Windows I/O locks.
    """
    def _truncate_args(d: dict, max_len: int = 500) -> dict:
        truncated = {}
        for k, v in d.items():
            if isinstance(v, str) and len(v) > max_len:
                truncated[k] = f"{v[:max_len]}... (truncated, total length: {len(v)})"
            elif isinstance(v, dict):
                truncated[k] = _truncate_args(v, max_len)
            else:
                truncated[k] = v
        return truncated

    record = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "caller": caller,
        "tool": tool_name,
        "args": _truncate_args(args),
        "status": status,
        "result_preview": result[:200] + "..." if len(result) > 200 else result
    }
    
    line = json.dumps(record, ensure_ascii=False) + "\n"
    
    for attempt in range(MAX_RETRIES):
        try:
            with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
                f.write(line)
            return  # Success
        except PermissionError:
            # File is locked by another process, wait and retry
            logger.warning(f"I/O lock encountered on {AUDIT_LOG_PATH}. Retrying {attempt+1}/{MAX_RETRIES}...")
            time.sleep(RETRY_DELAY)
        except Exception as e:
            logger.error(f"Failed to write audit log: {e}")
            break
            
    logger.error(f"Failed to write audit log after {MAX_RETRIES} attempts.")
```

---

### File: `src/utils/README.md`
```markdown
# AMEVA MCP Internal Utilities (utils)

이 디렉토리는 MCP 서버 구동 및 관리에 필요한 내부 공통 헬퍼 스크립트를 모아둔 곳입니다.
이곳의 모듈들은 AI 에이전트에게 도구(Tool)로 직접 노출되지 않으며, 서버 시스템 내부에서만 호출됩니다.

## 주요 모듈 구성
- **[audit_logger.py](audit_logger.py)**: 도구 호출 이력 및 인수를 mcp_audit.jsonl에 동기식으로 기록하는 보안 감사 로거.
- **[view_stats.py](view_stats.py)**: 서버 사용 통계 및 메트릭 데이터를 취합하는 모듈.
```

---

### File: `src/utils/view_stats.py`
```python
import json
from collections import Counter
from pathlib import Path

AUDIT_LOG_PATH = Path(r"C:\ameva\AMEVA-MCP-Toolkit-Utils\mcp_audit.jsonl")

def print_audit_stats():
    if not AUDIT_LOG_PATH.exists():
        print("Audit log is empty.")
        return

    total = 0
    status_counts = Counter()
    tool_counts = Counter()

    with open(AUDIT_LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            try:
                record = json.loads(line)
                total += 1
                status_counts[record.get("status", "unknown")] += 1
                tool_counts[record.get("tool", "unknown")] += 1
            except json.JSONDecodeError:
                pass

    print("="*40)
    print(" [ AMEVA MCP Audit Log Statistics ] ")
    print("="*40)
    print(f"Total Tool Executions: {total}")
    print("\n[Status Breakdown]")
    for status, count in status_counts.items():
        print(f"  - {status.upper()}: {count} ({count/total*100:.1f}%)")
    
    print("\n[Most Used Tools]")
    for tool, count in tool_counts.most_common():
        print(f"  - {tool}: {count} times")
    print("="*40)

if __name__ == "__main__":
    print_audit_stats()
```

---

### File: `src/utils/__init__.py`
```python
# Utils package
```

```

---

### File: `src/README.md`
```markdown
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
```

---

### File: `src/server.py`
```python
from mcp.server.fastmcp import FastMCP
from tools.document.file_manager import docker_delete_file, docker_move_file
from tools.document.md_converter import convert_md_to_docx_logic, docx_to_markdown, md_image_path_fixer
from tools.document.code_consolidator import consolidate_codebase_logic
from tools.git import git_manager
from tools.ssh import ssh_manager
from tools.utils import utils_manager
from tools.web import crawl_bot
from tools.database import db_consolidator
from tools.docker import docker_manager
from tools.dataset import dataset_aggregator
from tools.search import code_searcher
from tools.network import net_discovery
from utils.audit_logger import log_mcp_action

def create_server() -> FastMCP:
    """
    서버 초기화 및 도구 등록을 담당하는 진입점.
    비즈니스 로직은 src/tools 하위의 모듈에서 가져와 연결만 합니다.
    """
    mcp = FastMCP("AMEVA_Toolkit_Utils")

    # ──────────────────────────────────────────────────────────────────
    # Document & File Tools
    # ──────────────────────────────────────────────────────────────────

    @mcp.tool(name="consolidate_codebase", description="Consolidate target directory codebase into a single Markdown file containing directory structure, SQLite DB schemas, and source code contents.")
    def tool_consolidate_codebase(target_dir: str, output_file: str = None) -> str:
        res = consolidate_codebase_logic(target_dir, output_file)
        log_mcp_action("consolidate_codebase", {"target_dir": target_dir, "output_file": output_file}, res if len(res) < 1000 else f"Consolidated report ({len(res)} characters)")
        return res

    @mcp.tool(name="convert_md_to_docx", description="Convert Markdown file to Word DOCX format. Supports headings, bullets, code blocks, bold, numbered lists.")
    def tool_md_to_docx(input_md_path: str, output_docx_path: str) -> str:
        res = convert_md_to_docx_logic(input_md_path, output_docx_path)
        log_mcp_action("convert_md_to_docx", {"input": input_md_path, "output": output_docx_path}, res)
        return res

    @mcp.tool(name="docx_to_markdown", description="Convert a Word DOCX file to structured Markdown. Parses headings, lists, bold/italic, and tables. Set output_md_path to save to file, or leave empty to return text directly.")
    def tool_docx_to_markdown(docx_path: str, output_md_path: str = None) -> str:
        res = docx_to_markdown(docx_path, output_md_path)
        log_mcp_action("docx_to_markdown", {"docx_path": docx_path, "output": output_md_path}, res)
        return res

    @mcp.tool(name="md_image_path_fixer", description="Scan a Markdown file for broken image paths and auto-fix them by searching the base_image_dir for matching filenames.")
    def tool_md_image_path_fixer(doc_path: str, base_image_dir: str) -> str:
        res = md_image_path_fixer(doc_path, base_image_dir)
        log_mcp_action("md_image_path_fixer", {"doc_path": doc_path, "base_image_dir": base_image_dir}, res)
        return res

    @mcp.tool(name="delete_file_in_docker", description="Delete a file inside the Docker container")
    def tool_delete_file_in_docker(file_path: str) -> str:
        res = docker_delete_file(file_path)
        log_mcp_action("delete_file_in_docker", {"file_path": file_path}, res)
        return res

    @mcp.tool(name="move_file_in_docker", description="Move/rename a file inside the Docker container")
    def tool_move_file_in_docker(src_path: str, dest_path: str) -> str:
        res = docker_move_file(src_path, dest_path)
        log_mcp_action("move_file_in_docker", {"src_path": src_path, "dest_path": dest_path}, res)
        return res

    # ──────────────────────────────────────────────────────────────────
    # Git & SSH Tools
    # ──────────────────────────────────────────────────────────────────

    @mcp.tool(name="git_status", description="Get the git status of a repository (e.g., AMEVA-Doc-AI)")
    def tool_git_status(repo_name: str) -> str:
        res = git_manager.git_status(repo_name)
        log_mcp_action("git_status", {"repo": repo_name}, res)
        return res

    @mcp.tool(name="git_pull", description="Pull the latest changes for a repository")
    def tool_git_pull(repo_name: str) -> str:
        res = git_manager.git_pull(repo_name)
        log_mcp_action("git_pull", {"repo": repo_name}, res)
        return res

    @mcp.tool(name="git_commit_and_push", description="Stage all changes, commit with a message, and push for a repository")
    def tool_git_commit_and_push(repo_name: str, commit_message: str) -> str:
        res = git_manager.git_commit_and_push(repo_name, commit_message)
        log_mcp_action("git_commit_and_push", {"repo": repo_name, "msg": commit_message}, res)
        return res

    @mcp.tool(name="git_clone", description="Clone a remote git repository to the local system under the specified folder name")
    def tool_git_clone(repo_url: str, repo_name: str) -> str:
        res = git_manager.git_clone(repo_url, repo_name)
        log_mcp_action("git_clone", {"url": repo_url, "repo_name": repo_name}, res)
        return res

    @mcp.tool(name="git_log", description="Get the git commit log/history (e.g. limit=10 commits)")
    def tool_git_log(repo_name: str, limit: int = 10) -> str:
        res = git_manager.git_log(repo_name, limit)
        log_mcp_action("git_log", {"repo": repo_name, "limit": limit}, res)
        return res

    @mcp.tool(name="git_diff", description="Get git diff comparison of modified files in working directory")
    def tool_git_diff(repo_name: str, file_path: str = None) -> str:
        res = git_manager.git_diff(repo_name, file_path)
        log_mcp_action("git_diff", {"repo": repo_name, "file_path": file_path}, res)
        return res

    @mcp.tool(name="git_branch", description="Manage git branches. action can be: 'list', 'new', 'delete'")
    def tool_git_branch(repo_name: str, action: str = "list", branch_name: str = None) -> str:
        res = git_manager.git_branch(repo_name, action, branch_name)
        log_mcp_action("git_branch", {"repo": repo_name, "action": action, "branch_name": branch_name}, res)
        return res

    @mcp.tool(name="git_checkout", description="Checkout branch or restore files. Set create=True to create a new branch (-b)")
    def tool_git_checkout(repo_name: str, branch_or_file: str, create: bool = False) -> str:
        res = git_manager.git_checkout(repo_name, branch_or_file, create)
        log_mcp_action("git_checkout", {"repo": repo_name, "target": branch_or_file, "create": create}, res)
        return res

    @mcp.tool(name="git_merge", description="Merge a specified branch into the current branch")
    def tool_git_merge(repo_name: str, branch_name: str) -> str:
        res = git_manager.git_merge(repo_name, branch_name)
        log_mcp_action("git_merge", {"repo": repo_name, "branch": branch_name}, res)
        return res

    @mcp.tool(name="git_reset", description="Reset current HEAD to a state. mode: 'soft', 'mixed', 'hard'")
    def tool_git_reset(repo_name: str, mode: str = "mixed", commit_hash: str = "HEAD") -> str:
        res = git_manager.git_reset(repo_name, mode, commit_hash)
        log_mcp_action("git_reset", {"repo": repo_name, "mode": mode, "commit": commit_hash}, res)
        return res

    @mcp.tool(name="git_stash", description="Stash local changes. action: 'push', 'pop', 'list', 'apply', 'clear'")
    def tool_git_stash(repo_name: str, action: str = "push", stash_id: str = None) -> str:
        res = git_manager.git_stash(repo_name, action, stash_id)
        log_mcp_action("git_stash", {"repo": repo_name, "action": action, "stash_id": stash_id}, res)
        return res

    @mcp.tool(name="workspace_git_broadcaster", description="Scan all AMEVA repositories under C:\\ameva and report each repo's branch, ahead/behind status, and changed file count in one consolidated table.")
    def tool_workspace_git_broadcaster() -> str:
        res = git_manager.workspace_git_broadcaster()
        log_mcp_action("workspace_git_broadcaster", {}, res)
        return res

    @mcp.tool(name="git_commit_helper", description="Analyze staged git diff and auto-generate Conventional Commits message suggestions (feat/fix/docs/chore etc.) for the specified repository.")
    def tool_git_commit_helper(repo_name: str) -> str:
        res = git_manager.git_commit_helper(repo_name)
        log_mcp_action("git_commit_helper", {"repo": repo_name}, res)
        return res

    @mcp.tool(name="ssh_run_command", description="Run a shell command on a remote server via SSH")
    def tool_ssh_run_command(host: str, username: str, command: str, port: int = 22, password: str = None, key_content: str = None) -> str:
        res = ssh_manager.ssh_run_command(host, username, command, port, password, key_content)
        log_mcp_action("ssh_run_command", {"host": host, "username": username, "command": command, "port": port}, res)
        return res

    # ──────────────────────────────────────────────────────────────────
    # Web Crawling & Readability
    # ──────────────────────────────────────────────────────────────────

    @mcp.tool(name="crawl_website", description="Crawls a website URL, extracts title, text content, and analyzes internal/external links")
    def tool_crawl_website(url: str, selector: str = None) -> str:
        res = crawl_bot.crawl_website(url, selector)
        log_mcp_action("crawl_website", {"url": url, "selector": selector}, res)
        return res

    @mcp.tool(name="web_readability_cleaner", description="Extract clean readable content from a URL by stripping ads, navigation, sidebars and converting to Markdown.")
    def tool_web_readability_cleaner(url: str) -> str:
        res = crawl_bot.web_readability_cleaner(url)
        log_mcp_action("web_readability_cleaner", {"url": url}, res)
        return res

    @mcp.tool(name="dead_link_scanner", description="Parse all URLs inside a Markdown file and check each one via HTTP HEAD request to identify 404 dead links.")
    def tool_dead_link_scanner(md_file_path: str) -> str:
        res = crawl_bot.dead_link_scanner(md_file_path)
        log_mcp_action("dead_link_scanner", {"md_file_path": md_file_path}, res)
        return res

    # ──────────────────────────────────────────────────────────────────
    # Database Centralization & Operations
    # ──────────────────────────────────────────────────────────────────

    @mcp.tool(name="db_get_schema", description="Get the schema (tables, columns, SQL) of a SQLite database")
    def tool_db_get_schema(db_path: str) -> str:
        res = db_consolidator.db_get_schema(db_path)
        log_mcp_action("db_get_schema", {"db_path": db_path}, res)
        return res

    @mcp.tool(name="db_execute_query", description="Execute a SQLite query safely. Modifying queries are blocked if read_only=True. output_format: markdown | json | csv | html | xml | plain")
    def tool_db_execute_query(db_path: str, query: str, read_only: bool = True, output_format: str = "markdown", client_token: str = None) -> str:
        res = db_consolidator.db_execute_query(db_path, query, read_only, output_format, client_token)
        log_mcp_action("db_execute_query", {"db_path": db_path, "query": query, "read_only": read_only, "output_format": output_format, "client_token": client_token}, res)
        return res

    @mcp.tool(name="db_merge_tables", description="Merge table records from source SQLite DB into destination SQLite DB using a unique key column")
    def tool_db_merge_tables(src_db: str, dest_db: str, table_name: str, key_column: str, client_token: str = None) -> str:
        res = db_consolidator.db_merge_tables(src_db, dest_db, table_name, key_column, client_token)
        log_mcp_action("db_merge_tables", {"src_db": src_db, "dest_db": dest_db, "table_name": table_name, "key_column": key_column, "client_token": client_token}, res)
        return res

    @mcp.tool(name="db_generate_erd", description="Generate a copy-pasteable Mermaid ER Diagram of a SQLite database schema")
    def tool_db_generate_erd(db_path: str) -> str:
        res = db_consolidator.db_generate_erd(db_path)
        log_mcp_action("db_generate_erd", {"db_path": db_path}, res)
        return res

    @mcp.tool(name="db_generate_mock_data", description="Generate realistic mock data and insert it into a table respecting foreign keys")
    def tool_db_generate_mock_data(db_path: str, table_name: str, count: int = 50, client_token: str = None) -> str:
        res = db_consolidator.db_generate_mock_data(db_path, table_name, count, client_token)
        log_mcp_action("db_generate_mock_data", {"db_path": db_path, "table_name": table_name, "count": count, "client_token": client_token}, res)
        return res

    @mcp.tool(name="db_global_search_value", description="Search for a specific string value across all text columns of all tables in the database")
    def tool_db_global_search_value(db_path: str, search_query: str) -> str:
        res = db_consolidator.db_global_search_value(db_path, search_query)
        log_mcp_action("db_global_search_value", {"db_path": db_path, "search_query": search_query}, res)
        return res

    @mcp.tool(name="db_transpile_sqlite_to_other", description="Transpile SQLite schema and data into PostgreSQL or MySQL DDL/DML script")
    def tool_db_transpile_sqlite_to_other(db_path: str, target_dialect: str) -> str:
        res = db_consolidator.db_transpile_sqlite_to_other(db_path, target_dialect)
        log_mcp_action("db_transpile_sqlite_to_other", {"db_path": db_path, "target_dialect": target_dialect}, res)
        return res

    @mcp.tool(name="db_profile_and_scan_health", description="Scan database health: analyze indices, verify referential integrity, detect outliers")
    def tool_db_profile_and_scan_health(db_path: str) -> str:
        res = db_consolidator.db_profile_and_scan_health(db_path)
        log_mcp_action("db_profile_and_scan_health", {"db_path": db_path}, res)
        return res

    @mcp.tool(name="db_format_sql", description="Beautify, uppercase keywords, and format raw SQL query for better readability")
    def tool_db_format_sql(query: str) -> str:
        res = db_consolidator.db_format_sql(query)
        log_mcp_action("db_format_sql", {"query": query}, res)
        return res

    @mcp.tool(name="db_compare_schemas", description="Compare schemas of two databases and generate missing DDL synchronization script")
    def tool_db_compare_schemas(src_db: str, dest_db: str) -> str:
        res = db_consolidator.db_compare_schemas(src_db, dest_db)
        log_mcp_action("db_compare_schemas", {"src_db": src_db, "dest_db": dest_db}, res)
        return res

    @mcp.tool(name="db_mask_table_data", description="Anonymize/mask sensitive table columns (GDPR-compliant email, name, phone masking)")
    def tool_db_mask_table_data(db_path: str, table_name: str, mask_rules_json: str, client_token: str = None) -> str:
        res = db_consolidator.db_mask_table_data(db_path, table_name, mask_rules_json, client_token)
        log_mcp_action("db_mask_table_data", {"db_path": db_path, "table_name": table_name, "mask_rules_json": mask_rules_json, "client_token": client_token}, res)
        return res

    @mcp.tool(name="db_unmask_table_data", description="Restore previously masked columns using shadow table or unmask_rules. Requires write client_token. unmask_rules_json: {\"col\": {\"mask_type\": \"static\", \"original_value\": \"...\"}}")
    def tool_db_unmask_table_data(db_path: str, table_name: str, unmask_rules_json: str, client_token: str = None) -> str:
        res = db_consolidator.db_unmask_table_data(db_path, table_name, unmask_rules_json, client_token)
        log_mcp_action("db_unmask_table_data", {"db_path": db_path, "table_name": table_name, "client_token": client_token}, res)
        return res

    @mcp.tool(name="db_sync_connector", description="Bulk sync a table from one SQLite DB to another. Creates table if missing, upserts rows. Requires write client_token.")
    def tool_db_sync_connector(src_db: str, dest_db: str, table_name: str, client_token: str = None) -> str:
        res = db_consolidator.db_sync_connector(src_db, dest_db, table_name, client_token)
        log_mcp_action("db_sync_connector", {"src_db": src_db, "dest_db": dest_db, "table_name": table_name, "client_token": client_token}, res)
        return res

    @mcp.tool(name="db_optimize_query_tuning", description="Analyze SQL query and suggest optimal missing CREATE INDEX index statements")
    def tool_db_optimize_query_tuning(db_path: str, slow_query: str) -> str:
        res = db_consolidator.db_optimize_query_tuning(db_path, slow_query)
        log_mcp_action("db_optimize_query_tuning", {"db_path": db_path, "slow_query": slow_query}, res)
        return res

    @mcp.tool(name="db_enable_time_travel", description="Enable historical change logs (shadow ledger table + triggers) on a table")
    def tool_db_enable_time_travel(db_path: str, table_name: str, client_token: str = None) -> str:
        res = db_consolidator.db_enable_time_travel(db_path, table_name, client_token)
        log_mcp_action("db_enable_time_travel", {"db_path": db_path, "table_name": table_name, "client_token": client_token}, res)
        return res

    @mcp.tool(name="db_restore_time_travel", description="Restore table data state back to a specific timestamp in the past")
    def tool_db_restore_time_travel(db_path: str, table_name: str, target_timestamp: str, client_token: str = None) -> str:
        res = db_consolidator.db_restore_time_travel(db_path, table_name, target_timestamp, client_token)
        log_mcp_action("db_restore_time_travel", {"db_path": db_path, "table_name": table_name, "target_timestamp": target_timestamp, "client_token": client_token}, res)
        return res

    @mcp.tool(name="db_view_table_data", description="Browse and query table data with paging, sorting, filtering, and custom output formatting (markdown, json, csv, html, xml, plain)")
    def tool_db_view_table_data(db_path: str, table_name: str, limit: int = 50, offset: int = 0, sort_by: str = None, sort_order: str = "DESC", filter_conditions: str = None, output_format: str = "markdown") -> str:
        res = db_consolidator.db_view_table_data(db_path, table_name, limit, offset, sort_by, sort_order, filter_conditions, output_format)
        log_mcp_action("db_view_table_data", {"db_path": db_path, "table_name": table_name, "limit": limit, "offset": offset, "output_format": output_format}, res)
        return res

    @mcp.tool(name="db_summarize_table", description="Generate a visual markdown profile containing column structures, record stats, and sample data for a table")
    def tool_db_summarize_table(db_path: str, table_name: str) -> str:
        res = db_consolidator.db_summarize_table(db_path, table_name)
        log_mcp_action("db_summarize_table", {"db_path": db_path, "table_name": table_name}, res)
        return res

    @mcp.tool(name="db_search_schema", description="Find tables, columns, or indexes whose names contain the given search keyword")
    def tool_db_search_schema(db_path: str, search_term: str) -> str:
        res = db_consolidator.db_search_schema(db_path, search_term)
        log_mcp_action("db_search_schema", {"db_path": db_path, "search_term": search_term}, res)
        return res

    # ──────────────────────────────────────────────────────────────────
    # System & Developer Utilities
    # ──────────────────────────────────────────────────────────────────

    @mcp.tool(name="get_system_info", description="Get host system metrics (CPU, memory, disk usage, OS)")
    def tool_get_system_info() -> str:
        res = utils_manager.get_system_info()
        log_mcp_action("get_system_info", {}, res)
        return res

    @mcp.tool(name="check_port", description="Check if a specific host TCP port is open")
    def tool_check_port(host: str, port: int) -> str:
        res = utils_manager.check_port(host, port)
        log_mcp_action("check_port", {"host": host, "port": port}, res)
        return res

    @mcp.tool(name="generate_uuid", description="Generate a random UUID v4")
    def tool_generate_uuid() -> str:
        res = utils_manager.generate_uuid()
        log_mcp_action("generate_uuid", {}, res)
        return res

    @mcp.tool(name="format_json", description="Validate and pretty print a JSON string")
    def tool_format_json(json_str: str) -> str:
        res = utils_manager.format_json(json_str)
        log_mcp_action("format_json", {"json_str": json_str}, res)
        return res

    @mcp.tool(name="base64_encode_decode", description="Encode or decode a base64 string. mode can be 'encode' or 'decode'")
    def tool_base64_encode_decode(mode: str, data: str) -> str:
        res = utils_manager.base64_encode_decode(mode, data)
        log_mcp_action("base64_encode_decode", {"mode": mode, "data": data}, res)
        return res

    @mcp.tool(name="calculate_file_hash", description="Calculate the MD5 or SHA256 checksum of a file (executed inside Docker)")
    def tool_calculate_file_hash(file_path: str, algorithm: str = "sha256") -> str:
        res = utils_manager.docker_calculate_file_hash(file_path, algorithm)
        log_mcp_action("calculate_file_hash", {"file_path": file_path, "algorithm": algorithm}, res)
        return res

    @mcp.tool(name="get_external_ip", description="Get host's internal and external network IP addresses")
    def tool_get_external_ip() -> str:
        res = utils_manager.get_external_ip()
        log_mcp_action("get_external_ip", {}, res)
        return res

    @mcp.tool(name="send_http_request", description="Send an arbitrary HTTP request and return response details")
    def tool_send_http_request(method: str, url: str, headers_json: str = None, body: str = None) -> str:
        res = utils_manager.send_http_request(method, url, headers_json, body)
        log_mcp_action("send_http_request", {"method": method, "url": url}, res)
        return res

    @mcp.tool(name="find_large_files", description="Find files larger than size_mb MB inside the directory (executed inside Docker)")
    def tool_find_large_files(dir_path: str, size_mb: int = 50) -> str:
        res = utils_manager.docker_find_large_files(dir_path, size_mb)
        log_mcp_action("find_large_files", {"dir_path": dir_path, "size_mb": size_mb}, res)
        return res

    @mcp.tool(name="extract_text_from_url", description="Extract raw clean text from a web URL, removing HTML tags")
    def tool_extract_text_from_url(url: str) -> str:
        res = utils_manager.extract_text_from_url(url)
        log_mcp_action("extract_text_from_url", {"url": url}, res)
        return res

    @mcp.tool(name="gpu_monitor", description="Query nvidia-smi for real-time GPU utilization, VRAM usage, temperature, and power draw. Falls back to WMI on Windows if nvidia-smi unavailable.")
    def tool_gpu_monitor() -> str:
        res = utils_manager.gpu_monitor()
        log_mcp_action("gpu_monitor", {}, res)
        return res

    @mcp.tool(name="system_thermal_scanner", description="Scan CPU temperature, clock speed, and per-core utilization. Uses psutil sensors on Linux/Mac, WMI on Windows.")
    def tool_system_thermal_scanner() -> str:
        res = utils_manager.system_thermal_scanner()
        log_mcp_action("system_thermal_scanner", {}, res)
        return res

    @mcp.tool(name="process_watchdog", description="Monitor and control system processes. action: 'list' (top 30 by CPU), 'find' (search by name), 'kill' (terminate by name). process_name required for find/kill.")
    def tool_process_watchdog(action: str, process_name: str = None) -> str:
        res = utils_manager.process_watchdog(action, process_name)
        log_mcp_action("process_watchdog", {"action": action, "process_name": process_name}, res)
        return res

    @mcp.tool(name="task_cron_scheduler", description="Manage scheduled tasks. action: 'list'|'create'|'delete'|'run'. Windows uses schtasks, Linux uses crontab. job_name, cron_expression, command required for create.")
    def tool_task_cron_scheduler(action: str, job_name: str = None, cron_expression: str = None, command: str = None) -> str:
        res = utils_manager.task_cron_scheduler(action, job_name, cron_expression, command)
        log_mcp_action("task_cron_scheduler", {"action": action, "job_name": job_name}, res)
        return res

    @mcp.tool(name="rest_client_simulator", description="Send REST API requests without curl. Returns formatted response headers, body (JSON pretty-printed), elapsed time, and the equivalent curl command.")
    def tool_rest_client_simulator(method: str, url: str, payload_json: str = None, headers_json: str = None) -> str:
        res = utils_manager.rest_client_simulator(method, url, payload_json, headers_json)
        log_mcp_action("rest_client_simulator", {"method": method, "url": url}, res)
        return res

    @mcp.tool(name="html_to_pdf_renderer", description="Convert an HTML file or URL to PDF. Tries weasyprint → pdfkit → headless browser in order. Output path must be under C:\\ameva.")
    def tool_html_to_pdf_renderer(html_path_or_url: str, output_pdf_path: str) -> str:
        res = utils_manager.html_to_pdf_renderer(html_path_or_url, output_pdf_path)
        log_mcp_action("html_to_pdf_renderer", {"source": html_path_or_url, "output": output_pdf_path}, res)
        return res

    # ──────────────────────────────────────────────────────────────────
    # Docker Container Control [NEW]
    # ──────────────────────────────────────────────────────────────────

    @mcp.tool(name="docker_container_manager", description="Manage local Docker containers. action: 'list'|'stats'|'start'|'stop'|'restart'|'logs'|'inspect'. container_name required for all except list/stats.")
    def tool_docker_container_manager(action: str, container_name: str = None, limit_lines: int = 50) -> str:
        res = docker_manager.docker_container_manager(action, container_name, limit_lines)
        log_mcp_action("docker_container_manager", {"action": action, "container": container_name}, res)
        return res

    # ──────────────────────────────────────────────────────────────────
    # Dataset & Audit Aggregation [NEW]
    # ──────────────────────────────────────────────────────────────────

    @mcp.tool(name="audit_log_aggregator", description="Scan all AMEVA projects for mcp_audit.jsonl files, merge them into a single dataset JSONL with source_project tags, sorted by timestamp. Outputs stats on tool usage per project.")
    def tool_audit_log_aggregator(output_dataset_path: str) -> str:
        res = dataset_aggregator.audit_log_aggregator(output_dataset_path)
        log_mcp_action("audit_log_aggregator", {"output": output_dataset_path}, res)
        return res

    # ──────────────────────────────────────────────────────────────────
    # Code Search [NEW]
    # ──────────────────────────────────────────────────────────────────

    @mcp.tool(name="vector_code_searcher", description="BM25-based full-text code search across AMEVA project files. Returns top matching files with highlighted context lines. file_ext: '.py' or '.py,.js,.ts'")
    def tool_vector_code_searcher(query: str, file_ext: str = ".py", search_root: str = None, top_k: int = 10, context_lines: int = 3) -> str:
        res = code_searcher.vector_code_searcher(query, file_ext, search_root, top_k, context_lines)
        log_mcp_action("vector_code_searcher", {"query": query, "file_ext": file_ext}, res)
        return res

    # ──────────────────────────────────────────────────────────────────
    # Network Service Discovery [NEW]
    # ──────────────────────────────────────────────────────────────────

    @mcp.tool(name="service_discovery", description="Parallel port scan a single IP or CIDR subnet. Identifies open ports and auto-detects AMEVA services (Streamlit, FastAPI, Gradio, Ollama, Redis). ports_json: '[22, 80, 8000, 8501]'")
    def tool_service_discovery(subnet: str = "127.0.0.1", ports_json: str = "[22, 80, 8000, 8080, 8501]", timeout: float = 0.5, max_hosts: int = 254) -> str:
        res = net_discovery.service_discovery(subnet, ports_json, timeout, max_hosts)
        log_mcp_action("service_discovery", {"subnet": subnet, "ports_json": ports_json}, res)
        return res

    return mcp

if __name__ == "__main__":
    server = create_server()
    server.run()
```

---

### File: `src/tools/README.md`
```markdown
# AMEVA MCP Tools Directory Specification

이 디렉토리는 AMEVA MCP Toolkit에서 제공하는 모든 에이전트 전용 도구(MCP Tools)의 비즈니스 로직 구현체를 모아둔 통합 디렉토리입니다.

## 디렉토리 구조 및 역할

- **database/**: SQLite 데이터베이스 연결 및 통합 데이터 연산을 처리합니다. ([상세 README](database/README.md))
  - 주요 도구: db_get_schema, db_execute_query, db_merge_tables
- **document/**: 디렉터리 및 코드베이스 병합, 마크다운 변환 및 Docker 컨테이너 내 파일 조작을 담당합니다.
  - 주요 도구: consolidate_codebase, convert_md_to_docx, delete_file_in_docker, move_file_in_docker
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
```

---

### File: `src/tools/database/db_consolidator.py`
```python
import sqlite3
import os
import re
import json
import random
from datetime import datetime

def _get_connection(db_path: str):
    """Safely return sqlite3 connection for the given absolute path."""
    # Enforce safe path validation inside C:\ameva
    normalized_path = os.path.abspath(db_path)
    if not normalized_path.lower().startswith(r"c:\ameva"):
        raise PermissionError(f"Security Error: Access to path '{normalized_path}' is denied. Only 'C:\\ameva' subfolders are allowed.")
        
    if not os.path.exists(normalized_path):
        raise FileNotFoundError(f"Database file not found at {normalized_path}")
    return sqlite3.connect(normalized_path)

def _validate_write_permission(client_token: str):
    """Validate if the client token is authorized for CUD operations."""
    expected_token = os.environ.get("AMEVA_DB_WRITE_TOKEN")
    if expected_token:
        if not client_token or client_token != expected_token:
            raise PermissionError("Security Error: CUD (Write) operation is restricted. Invalid or missing client_token.")

def db_get_schema(db_path: str) -> str:
    """Analyze and return schemas (tables, columns, SQL definition) of the SQLite database."""
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = cursor.fetchall()
        
        if not tables:
            conn.close()
            return f"Database at {db_path} has no tables."
            
        report = f"=== SCHEMA REPORT FOR: {db_path} ===\n\n"
        for table_name, create_sql in tables:
            report += f"Table: {table_name}\n"
            report += f"SQL definition:\n{create_sql}\n"
            
            cursor.execute(f"PRAGMA table_info({table_name});")
            cols = cursor.fetchall()
            report += "Columns:\n"
            for cid, name, type_name, notnull, dflt_value, pk in cols:
                pk_indicator = " [PRIMARY KEY]" if pk else ""
                nn_indicator = " [NOT NULL]" if notnull else ""
                report += f"  - {name} ({type_name}){pk_indicator}{nn_indicator}\n"
            report += "-" * 50 + "\n"
            
        conn.close()
        return report
    except Exception as e:
        return f"Error analyzing DB schema: {str(e)}"

def _format_output(headers: list, rows: list, output_format: str) -> str:
    """Format tabular data into markdown, json, csv, html, xml, or plain format."""
    output_format = output_format.lower().strip()
    if not rows:
        return f"Headers: {headers}\nResult: 0 rows returned."
        
    if output_format == "json":
        data = [dict(zip(headers, row)) for row in rows]
        return json.dumps(data, indent=2, ensure_ascii=False)
        
    elif output_format == "csv":
        import csv
        import io
        output = io.StringIO()
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(headers)
        writer.writerows(rows)
        return output.getvalue()
        
    elif output_format == "html":
        html = "<table border='1'>\n  <thead>\n    <tr>"
        for h in headers:
            html += f"<th>{h}</th>"
        html += "</tr>\n  </thead>\n  <tbody>\n"
        for row in rows:
            html += "    <tr>"
            for v in row:
                val = "" if v is None else str(v)
                html += f"<td>{val}</td>"
            html += "</tr>\n"
        html += "  </tbody>\n</table>"
        return html
        
    elif output_format == "xml":
        xml = "<records>\n"
        for row in rows:
            xml += "  <row>\n"
            for h, v in zip(headers, row):
                val = "" if v is None else str(v)
                clean_h = re.sub(r'[^a-zA-Z0-9_]', '', h) or "column"
                val_escaped = val.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                xml += f"    <{clean_h}>{val_escaped}</{clean_h}>\n"
            xml += "  </row>\n"
        xml += "</records>"
        return xml
        
    elif output_format == "plain":
        result = "\t".join(headers) + "\n"
        for row in rows:
            result += "\t".join(["" if v is None else str(v) for v in row]) + "\n"
        return result.strip()
        
    else:  # markdown
        widths = [len(str(h)) for h in headers]
        for row in rows:
            for i, v in enumerate(row):
                val_len = len(str(v)) if v is not None else 0
                if val_len > widths[i]:
                    widths[i] = val_len
                    
        header_line = "| " + " | ".join([str(h).ljust(widths[i]) for i, h in enumerate(headers)]) + " |"
        sep_line = "| " + " | ".join(["-" * widths[i] for i in range(len(headers))]) + " |"
        
        row_lines = []
        for row in rows:
            row_line = "| " + " | ".join([("" if v is None else str(v)).ljust(widths[i]) for i, v in enumerate(row)]) + " |"
            row_lines.append(row_line)
            
        return "\n".join([header_line, sep_line] + row_lines)

def db_execute_query(db_path: str, query: str, read_only: bool = True, output_format: str = "markdown", client_token: str = None) -> str:
    """Execute a SQL query/command safely. In read-only mode, only SELECT/PRAGMA/EXPLAIN is permitted."""
    query_stripped = re.sub(r'/\*.*?\*/', '', query, flags=re.DOTALL).strip().upper()
    
    if read_only:
        # Prevent any DDL or write DML
        dangerous_keywords = ["INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER", "REPLACE", "RENAME", "TRUNCATE"]
        for kw in dangerous_keywords:
            if re.search(r'\b' + kw + r'\b', query_stripped):
                return f"Security Error: Writing/Modifying operation '{kw}' is blocked in read-only mode."
    else:
        # Validate write permissions if client tries to run write operations
        try:
            _validate_write_permission(client_token)
        except PermissionError as pe:
            return str(pe)
        
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        cursor.execute(query)
        
        is_select = any(query_stripped.startswith(prefix) for prefix in ["SELECT", "PRAGMA", "EXPLAIN", "WITH"])
        if is_select:
            rows = cursor.fetchall()
            headers = [desc[0] for desc in cursor.description] if cursor.description else []
            conn.close()
            
            if not rows:
                return f"Query executed successfully. Headers: {headers}\nResult: 0 rows returned."
                
            return _format_output(headers, rows, output_format)
        else:
            conn.commit()
            changes = conn.changes()
            conn.close()
            return f"Command executed successfully. Database changes made: {changes} rows."
    except Exception as e:
        return f"Database Query Error: {str(e)}"

def db_merge_tables(src_db: str, dest_db: str, table_name: str, key_column: str, client_token: str = None) -> str:
    """
    Merge data from src_db.table_name into dest_db.table_name.
    Inserts missing records and updates matching records using key_column.
    """
    try:
        _validate_write_permission(client_token)
    except PermissionError as pe:
        return str(pe)
        
    try:
        # Enforce path safety
        src_db = os.path.abspath(src_db)
        dest_db = os.path.abspath(dest_db)
        if not src_db.lower().startswith(r"c:\ameva") or not dest_db.lower().startswith(r"c:\ameva"):
            return "Security Error: Both databases must be in the C:\\ameva directory."
            
        if not os.path.exists(src_db):
            return f"Error: Source database does not exist at {src_db}"
        if not os.path.exists(dest_db):
            return f"Error: Destination database does not exist at {dest_db}"
            
        src_conn = sqlite3.connect(src_db)
        src_cursor = src_conn.cursor()
        
        src_cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        if not src_cursor.fetchone():
            src_conn.close()
            return f"Error: Table '{table_name}' does not exist in source database."
            
        src_cursor.execute(f"PRAGMA table_info({table_name});")
        src_cols = [col[1] for col in src_cursor.fetchall()]
        
        if key_column not in src_cols:
            src_conn.close()
            return f"Error: Key column '{key_column}' not found in table '{table_name}'."
            
        src_cursor.execute(f"SELECT * FROM {table_name};")
        records = src_cursor.fetchall()
        src_conn.close()
        
        if not records:
            return f"No records found in source table '{table_name}' to merge."
            
        dest_conn = sqlite3.connect(dest_db)
        dest_cursor = dest_conn.cursor()
        
        dest_cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        if not dest_cursor.fetchone():
            src_conn_temp = sqlite3.connect(src_db)
            c_temp = src_conn_temp.cursor()
            c_temp.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
            create_sql = c_temp.fetchone()[0]
            src_conn_temp.close()
            
            dest_cursor.execute(create_sql)
            dest_conn.commit()
            
        dest_cursor.execute(f"SELECT {key_column} FROM {table_name};")
        dest_keys = {row[0] for row in dest_cursor.fetchall()}
        
        inserted = 0
        updated = 0
        
        col_names = ", ".join(src_cols)
        placeholders = ", ".join(["?"] * len(src_cols))
        insert_sql = f"INSERT INTO {table_name} ({col_names}) VALUES ({placeholders});"
        
        update_set = ", ".join([f"{col}=?" for col in src_cols if col != key_column])
        update_sql = f"UPDATE {table_name} SET {update_set} WHERE {key_column}=?;"
        
        key_index = src_cols.index(key_column)
        
        for record in records:
            rec_key = record[key_index]
            if rec_key in dest_keys:
                update_values = [record[i] for i in range(len(src_cols)) if i != key_index] + [rec_key]
                dest_cursor.execute(update_sql, update_values)
                updated += 1
            else:
                dest_cursor.execute(insert_sql, record)
                inserted += 1
                
        dest_conn.commit()
        dest_conn.close()
        
        return f"Successfully merged table '{table_name}': {inserted} rows inserted, {updated} rows updated in destination DB."
    except Exception as e:
        return f"Error during DB merge operation: {str(e)}"


# ==============================================================================
# ENTERPRISE PRO FEATURES IMPLEMENTATION
# ==============================================================================

def db_generate_erd(db_path: str) -> str:
    """Generate a copy-pasteable Mermaid ER Diagram of the database schema."""
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = [r[0] for r in cursor.fetchall()]
        
        if not tables:
            conn.close()
            return "No tables found in the database to generate an ERD."
            
        erd = "erDiagram\n"
        relationships = []
        
        for table in tables:
            erd += f"    {table} {{\n"
            
            # Get columns
            cursor.execute(f"PRAGMA table_info({table});")
            cols = cursor.fetchall()
            
            # Get foreign keys to mark them
            cursor.execute(f"PRAGMA foreign_key_list({table});")
            fks = cursor.fetchall()
            fk_cols = {f[3]: f for f in fks if f[3]}
            
            for cid, col_name, col_type, notnull, dflt, pk in cols:
                pk_flag = " PK" if pk else ""
                fk_flag = " FK" if col_name in fk_cols else ""
                clean_type = re.sub(r'[^a-zA-Z0-9]', '', col_type).lower() or "text"
                erd += f"        {clean_type} {col_name}{pk_flag}{fk_flag}\n"
            erd += "    }\n"
            
            for fk in fks:
                parent_table = fk[2]
                from_col = fk[3]
                to_col = fk[4]
                relationships.append(f"    {parent_table} ||--o{{ {table} : \"{from_col}->{to_col}\"")
                
        conn.close()
        
        erd += "\n" + "\n".join(relationships)
        return f"```mermaid\n{erd}\n```"
    except Exception as e:
        return f"Error generating Mermaid ERD: {str(e)}"


def db_generate_mock_data(db_path: str, table_name: str, count: int = 50, client_token: str = None) -> str:
    """Generate realistic mock data and populate the table automatically respecting FKs."""
    try:
        _validate_write_permission(client_token)
    except PermissionError as pe:
        return str(pe)
        
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        # Verify table
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        if not cursor.fetchone():
            conn.close()
            return f"Table '{table_name}' does not exist."
            
        # Get columns
        cursor.execute(f"PRAGMA table_info({table_name});")
        cols = cursor.fetchall()
        
        # Get foreign keys to resolve them dynamically
        cursor.execute(f"PRAGMA foreign_key_list({table_name});")
        fks = cursor.fetchall()
        fk_map = {f[3]: f[2] for f in fks if f[3]}
        
        # Pre-fetch parent table IDs to respect FK references
        parent_data = {}
        for col_name, parent_table in fk_map.items():
            cursor.execute(f"PRAGMA table_info({parent_table});")
            parent_cols = cursor.fetchall()
            pk_col = next((c[1] for c in parent_cols if c[5]), parent_cols[0][1])
            
            cursor.execute(f"SELECT {pk_col} FROM {parent_table} LIMIT 100;")
            parent_ids = [r[0] for r in cursor.fetchall()]
            if not parent_ids:
                conn.close()
                return f"Constraint Error: Parent table '{parent_table}' has no records. Populate it first before inserting into '{table_name}'."
            parent_data[col_name] = parent_ids
            
        first_names = ["Minsoo", "Jiho", "Yeon", "Jun", "Sujin", "Sunghwan", "Hyejin", "Gildong", "Chulsoo", "Younghee"]
        last_names = ["Kim", "Lee", "Park", "Choi", "Jung", "Kang", "Cho", "Yoon", "Jang", "Lim"]
        domains = ["gmail.com", "naver.com", "daum.net", "outlook.com", "yahoo.com"]
        
        inserted = 0
        col_names = [c[1] for c in cols]
        
        pk_col_info = next((c for c in cols if c[5]), None)
        is_integer_pk = pk_col_info and "INT" in pk_col_info[2].upper()
        
        insert_cols = [c for c in col_names if not (is_integer_pk and c == pk_col_info[1])]
        placeholders = ", ".join(["?"] * len(insert_cols))
        insert_sql = f"INSERT INTO {table_name} ({', '.join(insert_cols)}) VALUES ({placeholders});"
        
        for i in range(count):
            row_data = []
            for col in cols:
                name = col[1]
                col_type = col[2].upper()
                is_pk = col[5]
                
                if is_integer_pk and name == pk_col_info[1]:
                    continue
                    
                if name in parent_data:
                    row_data.append(random.choice(parent_data[name]))
                    continue
                    
                name_lower = name.lower()
                if "email" in name_lower:
                    row_data.append(f"{random.choice(first_names).lower()}{random.randint(10,99)}@{random.choice(domains)}")
                elif "phone" in name_lower or "tel" in name_lower:
                    row_data.append(f"010-{random.randint(1000,9999)}-{random.randint(1000,9999)}")
                elif "name" in name_lower:
                    row_data.append(f"{random.choice(first_names)} {random.choice(last_names)}")
                elif "uuid" in name_lower:
                    import uuid
                    row_data.append(str(uuid.uuid4()))
                elif "date" in name_lower or "time" in name_lower or "created" in name_lower or "updated" in name_lower:
                    row_data.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                elif "status" in name_lower:
                    row_data.append(random.choice(["ACTIVE", "PENDING", "INACTIVE"]))
                elif "INT" in col_type:
                    row_data.append(random.randint(1, 10000) if not is_pk else i + 100)
                elif "REAL" in col_type or "NUM" in col_type or "FLOAT" in col_type:
                    row_data.append(round(random.uniform(10.0, 1000.0), 2))
                else:
                    row_data.append(f"MockData_{name}_{i}")
                    
            cursor.execute(insert_sql, row_data)
            inserted += 1
            
        conn.commit()
        conn.close()
        return f"Successfully generated and inserted {inserted} mock records into table '{table_name}'."
    except Exception as e:
        return f"Error generating mock data: {str(e)}"


def db_global_search_value(db_path: str, search_query: str) -> str:
    """Search for a specific string value across all text columns of all tables."""
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = [r[0] for r in cursor.fetchall()]
        
        matches = []
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table});")
            cols = cursor.fetchall()
            text_cols = [c[1] for c in cols if any(t in c[2].upper() for t in ["TEXT", "CHAR", "VARCHAR", "CLOB"])]
            
            if not text_cols:
                continue
                
            where_clauses = " OR ".join([f"{col} LIKE ?" for col in text_cols])
            query = f"SELECT * FROM {table} WHERE {where_clauses};"
            
            params = [f"%{search_query}%"] * len(text_cols)
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            if rows:
                for row in rows[:10]:
                    matches.append(f"Table: {table} | Row: {row}")
                if len(rows) > 10:
                    matches.append(f"Table: {table} | ... and {len(rows)-10} more matches.")
                    
        conn.close()
        if not matches:
            return f"No matches found for search query '{search_query}'."
        return f"=== GLOBAL SEARCH RESULTS FOR '{search_query}' ===\n\n" + "\n".join(matches)
    except Exception as e:
        return f"Error during global search: {str(e)}"


def db_transpile_sqlite_to_other(db_path: str, target_dialect: str) -> str:
    """Transpile SQLite schema and data into PostgreSQL or MySQL DDL/DML script."""
    target_dialect = target_dialect.lower()
    if target_dialect not in ["postgresql", "mysql"]:
        return "Error: Target dialect must be either 'postgresql' or 'mysql'."
        
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = cursor.fetchall()
        
        sql_script = f"-- Generated Migration Script for {target_dialect.upper()}\n"
        sql_script += f"-- Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for table_name, create_sql in tables:
            new_ddl = create_sql
            if target_dialect == "postgresql":
                new_ddl = re.sub(
                    r'(?i)\bINTEGER\s+PRIMARY\s+KEY\s+AUTOINCREMENT\b', 
                    'SERIAL PRIMARY KEY', 
                    new_ddl
                )
                new_ddl = new_ddl.replace('"', '')
            elif target_dialect == "mysql":
                new_ddl = re.sub(
                    r'(?i)\bAUTOINCREMENT\b', 
                    'AUTO_INCREMENT', 
                    new_ddl
                )
                
            sql_script += f"{new_ddl};\n\n"
            
            cursor.execute(f"PRAGMA table_info({table_name});")
            cols = [c[1] for c in cursor.fetchall()]
            
            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()
            
            if rows:
                sql_script += f"-- Data insertion for {table_name}\n"
                col_str = ", ".join(cols)
                for row in rows:
                    val_list = []
                    for v in row:
                        if v is None:
                            val_list.append("NULL")
                        elif isinstance(v, (int, float)):
                            val_list.append(str(v))
                        else:
                            escaped = str(v).replace("'", "''")
                            val_list.append(f"'{escaped}'")
                    val_str = ", ".join(val_list)
                    sql_script += f"INSERT INTO {table_name} ({col_str}) VALUES ({val_str});\n"
                sql_script += "\n"
                
        conn.close()
        return sql_script
    except Exception as e:
        return f"Error transpiling SQLite to {target_dialect}: {str(e)}"


def db_profile_and_scan_health(db_path: str) -> str:
    """Analyze indices, scan orphaned rows (FK breaks), check high NULL rates, detect numeric outliers."""
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = [r[0] for r in cursor.fetchall()]
        
        report = f"=== DATABASE HEALTH & ANOMALY REPORT ===\n\n"
        
        cursor.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index';")
        indices = cursor.fetchall()
        idx_info = {}
        for idx_name, tbl_name in indices:
            cursor.execute(f"PRAGMA index_info({idx_name});")
            columns = [r[2] for r in cursor.fetchall()]
            key = (tbl_name, tuple(columns))
            if key in idx_info:
                idx_info[key].append(idx_name)
            else:
                idx_info[key] = [idx_name]
                
        dup_indices = {k: v for k, v in idx_info.items() if len(v) > 1}
        report += "1. Duplicate Index Check:\n"
        if dup_indices:
            for (tbl, cols), names in dup_indices.items():
                report += f"  - WARNING: Table '{tbl}' has duplicate indexes {names} covering columns {cols}.\n"
        else:
            report += "  - OK: No duplicate indexes found.\n"
        report += "\n"
        
        report += "2. Referential Integrity / Orphan Row Check:\n"
        orphans_found = False
        for table in tables:
            cursor.execute(f"PRAGMA foreign_key_list({table});")
            fks = cursor.fetchall()
            for fk in fks:
                parent_table = fk[2]
                child_col = fk[3]
                parent_col = fk[4] or "id"
                
                query = f"SELECT COUNT(*) FROM {table} WHERE {child_col} NOT IN (SELECT {parent_col} FROM {parent_table}) AND {child_col} IS NOT NULL;"
                cursor.execute(query)
                orphans = cursor.fetchone()[0]
                if orphans > 0:
                    report += f"  - DANGER: Table '{table}' has {orphans} orphan records violating foreign key reference to {parent_table}({parent_col})!\n"
                    orphans_found = True
        if not orphans_found:
            report += "  - OK: No orphan records found. Referential integrity intact.\n"
        report += "\n"
        
        report += "3. Columns Data Profiling & Anomalies:\n"
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table};")
            total_rows = cursor.fetchone()[0]
            if total_rows == 0:
                report += f"  - Table '{table}': Empty table.\n"
                continue
                
            cursor.execute(f"PRAGMA table_info({table});")
            cols = cursor.fetchall()
            for cid, col_name, col_type, notnull, dflt, pk in cols:
                cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {col_name} IS NULL;")
                nulls = cursor.fetchone()[0]
                null_rate = (nulls / total_rows) * 100
                if null_rate > 50:
                    report += f"  - WARNING: Table '{table}' column '{col_name}' has a high NULL rate of {null_rate:.1f}%.\n"
                    
                if any(t in col_type.upper() for t in ["INT", "REAL", "NUM", "FLOAT", "DOUBLE"]):
                    cursor.execute(f"SELECT AVG({col_name}), AVG({col_name}*{col_name}) FROM {table} WHERE {col_name} IS NOT NULL;")
                    stats = cursor.fetchone()
                    if stats and stats[0] is not None:
                        avg = stats[0]
                        variance = max(0, stats[1] - (avg * avg))
                        stddev = variance ** 0.5
                        
                        if stddev > 0:
                            upper_limit = avg + (3 * stddev)
                            lower_limit = avg - (3 * stddev)
                            cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {col_name} > ? OR {col_name} < ?;", (upper_limit, lower_limit))
                            outliers = cursor.fetchone()[0]
                            if outliers > 0:
                                report += f"  - INFO: Table '{table}' column '{col_name}' has {outliers} potential statistical outliers (> 3 stddev).\n"
                                
        conn.close()
        return report
    except Exception as e:
        return f"Error executing database health check: {str(e)}"


def db_format_sql(query: str) -> str:
    """Beautify, uppercase keywords, and format raw SQL string into pretty, readable SQL."""
    keywords = [
        r"\bselect\b", r"\bfrom\b", r"\bwhere\b", r"\bjoin\b", r"\bleft\b", r"\bright\b", r"\bouter\b",
        r"\binner\b", r"\bon\b", r"\bgroup\b", r"\bby\b", r"\border\b", r"\bhaving\b", r"\blimit\b",
        r"\band\b", r"\bor\b", r"\bas\b", r"\bin\b", r"\bis\b", r"\bnull\b", r"\bcreate\b", r"\btable\b",
        r"\binsert\b", r"\binto\b", r"\bvalues\b", r"\bupdate\b", r"\bset\b", r"\bdelete\b"
    ]
    
    formatted = query.strip()
    
    for kw in keywords:
        formatted = re.sub(kw, lambda m: m.group(0).upper(), formatted, flags=re.IGNORECASE)
        
    major_clauses = ["FROM", "WHERE", "LEFT JOIN", "RIGHT JOIN", "INNER JOIN", "JOIN", "GROUP BY", "ORDER BY", "HAVING", "LIMIT", "SET", "VALUES"]
    for clause in major_clauses:
        formatted = re.sub(r'\s+\b' + clause + r'\b', f'\n{clause}', formatted)
        
    return formatted


def db_compare_schemas(src_db: str, dest_db: str) -> str:
    """Compare src_db schema to dest_db and generate missing table/column DDL sync scripts."""
    try:
        src_db = os.path.abspath(src_db)
        dest_db = os.path.abspath(dest_db)
        if not src_db.lower().startswith(r"c:\ameva") or not dest_db.lower().startswith(r"c:\ameva"):
            return "Security Error: Both databases must be in the C:\\ameva directory."
            
        src_conn = sqlite3.connect(src_db)
        src_cursor = src_conn.cursor()
        dest_conn = sqlite3.connect(dest_db)
        dest_cursor = dest_conn.cursor()
        
        src_cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        src_tables = {r[0]: r[1] for r in src_cursor.fetchall()}
        
        dest_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        dest_tables = {r[0] for r in dest_cursor.fetchall()}
        
        diff_script = f"-- Schema Sync Script: {dest_db} -> match {src_db}\n\n"
        changes_detected = False
        
        for table, create_sql in src_tables.items():
            if table not in dest_tables:
                diff_script += f"-- Table '{table}' is missing in target. Creating...\n"
                diff_script += f"{create_sql};\n\n"
                changes_detected = True
                
        for table, create_sql in src_tables.items():
            if table in dest_tables:
                src_cursor.execute(f"PRAGMA table_info({table});")
                src_cols = {r[1]: (r[2], r[3], r[4]) for r in src_cursor.fetchall()}
                
                dest_cursor.execute(f"PRAGMA table_info({table});")
                dest_cols = {r[1] for r in dest_cursor.fetchall()}
                
                for col_name, (col_type, notnull, default) in src_cols.items():
                    if col_name not in dest_cols:
                        diff_script += f"-- Column '{col_name}' is missing in target table '{table}'. Adding...\n"
                        notnull_str = " NOT NULL" if notnull else ""
                        dflt_str = f" DEFAULT {default}" if default is not None else ""
                        diff_script += f"ALTER TABLE {table} ADD COLUMN {col_name} {col_type}{notnull_str}{dflt_str};\n"
                        changes_detected = True
                diff_script += "\n"
                
        src_conn.close()
        dest_conn.close()
        
        if not changes_detected:
            return "No schema differences detected between source and destination databases."
            
        return diff_script
    except Exception as e:
        return f"Error during schema comparison: {str(e)}"


def db_mask_table_data(db_path: str, table_name: str, mask_rules_json: str, client_token: str = None) -> str:
    """Mask sensitive columns inside a table based on GDPR-compliant rules."""
    try:
        _validate_write_permission(client_token)
    except PermissionError as pe:
        return str(pe)
        
    try:
        rules = json.loads(mask_rules_json)
    except Exception as e:
        return f"Error: Invalid mask_rules_json format: {str(e)}"
        
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        if not cursor.fetchone():
            conn.close()
            return f"Table '{table_name}' does not exist."
            
        cursor.execute(f"PRAGMA table_info({table_name});")
        table_cols = [c[1] for c in cursor.fetchall()]
        
        for col in rules.keys():
            if col not in table_cols:
                conn.close()
                return f"Error: Column '{col}' not found in table '{table_name}'."
                
        cursor.execute(f"SELECT rowid, * FROM {table_name};")
        rows = cursor.fetchall()
        
        updated = 0
        for row in rows:
            rowid = row[0]
            row_dict = {table_cols[i]: row[i+1] for i in range(len(table_cols))}
            
            update_clauses = []
            params = []
            
            for col, rule in rules.items():
                val = row_dict[col]
                if val is None:
                    continue
                    
                val_str = str(val)
                masked_val = val_str
                
                if rule == "mask_email":
                    if "@" in val_str:
                        local, domain = val_str.split("@", 1)
                        masked_local = local[0] + "***" if len(local) > 1 else local + "***"
                        masked_val = f"{masked_local}@{domain}"
                elif rule == "mask_name":
                    if len(val_str) >= 3:
                        masked_val = val_str[0] + "*" + val_str[2:]
                    elif len(val_str) == 2:
                        masked_val = val_str[0] + "*"
                    else:
                        masked_val = "*"
                elif rule == "mask_phone":
                    clean_phone = re.sub(r'[^0-9]', '', val_str)
                    if len(clean_phone) >= 10:
                        masked_val = f"{val_str[:3]}-****-{val_str[-4:]}"
                    else:
                        masked_val = "***-***-****"
                elif rule == "mask_hash":
                    import hashlib
                    masked_val = hashlib.sha256(val_str.encode()).hexdigest()[:16]
                else:
                    masked_val = "******"
                    
                update_clauses.append(f"{col}=?")
                params.append(masked_val)
                
            if update_clauses:
                params.append(rowid)
                query = f"UPDATE {table_name} SET {', '.join(update_clauses)} WHERE rowid=?;"
                cursor.execute(query, params)
                updated += 1
                
        conn.commit()
        conn.close()
        return f"Successfully masked data for {updated} rows in table '{table_name}'."
    except Exception as e:
        return f"Error masking table data: {str(e)}"


def db_optimize_query_tuning(db_path: str, slow_query: str) -> str:
    """Analyze query plan via EXPLAIN QUERY PLAN and output missing index recommendations."""
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        explain_query = f"EXPLAIN QUERY PLAN {slow_query}"
        cursor.execute(explain_query)
        plan_rows = cursor.fetchall()
        
        recommendations = []
        tuning_report = "=== SQL QUERY PLAN ANALYSIS ===\n\n"
        
        for row in plan_rows:
            detail = row[3]
            tuning_report += f"Plan detail: {detail}\n"
            
            if "SCAN TABLE" in detail:
                match = re.search(r'SCAN TABLE (\w+)', detail)
                if match:
                    table_name = match.group(1)
                    
                    where_match = re.search(r'(?i)WHERE\s+(.*)', slow_query)
                    candidate_cols = []
                    if where_match:
                        where_clause = where_match.group(1)
                        cols_in_where = re.findall(r'\b(?:' + table_name + r'\.)?(\w+)\s*[=<>!]+', where_clause)
                        candidate_cols.extend([c for c in cols_in_where if c.lower() not in ["null", "true", "false"]])
                        
                    seen = set()
                    candidate_cols = [c for c in candidate_cols if not (c in seen or seen.add(c))]
                    
                    if candidate_cols:
                        cols_str = ", ".join(candidate_cols)
                        idx_name = f"idx_{table_name}_{'_'.join(candidate_cols)}"
                        recommendations.append(f"CREATE INDEX {idx_name} ON {table_name}({cols_str});")
                    else:
                        recommendations.append(f"-- Suggestion: Analyze table '{table_name}' and create index on columns used in filtering/joining.")
                        
        conn.close()
        
        if recommendations:
            tuning_report += "\n=== INDEX OPTIMIZATION RECOMMENDATIONS ===\n"
            tuning_report += "\n".join(recommendations)
        else:
            tuning_report += "\n=== INDEX OPTIMIZATION RECOMMENDATIONS ===\n- OK: Query is already optimized and utilizes indices efficiently."
            
        return tuning_report
    except Exception as e:
        return f"Error during query optimization analysis: {str(e)}"


def db_enable_time_travel(db_path: str, table_name: str, client_token: str = None) -> str:
    """Enable time travel audit log shadow table and triggers for mutating operations."""
    try:
        _validate_write_permission(client_token)
    except PermissionError as pe:
        return str(pe)
        
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        if not cursor.fetchone():
            conn.close()
            return f"Table '{table_name}' does not exist."
            
        cursor.execute(f"PRAGMA table_info({table_name});")
        cols = [c[1] for c in cursor.fetchall()]
        
        ledger_table = f"{table_name}_ledger"
        
        create_ledger_sql = f"""
        CREATE TABLE IF NOT EXISTS {ledger_table} (
            ledger_id INTEGER PRIMARY KEY AUTOINCREMENT,
            row_id INTEGER,
            operation TEXT,
            old_data TEXT,
            new_data TEXT,
            changed_at TIMESTAMP DEFAULT (datetime('now', 'localtime'))
        );
        """
        cursor.execute(create_ledger_sql)
        
        old_json = "json_object(" + ", ".join([f"'{c}', OLD.{c}" for c in cols]) + ")"
        new_json = "json_object(" + ", ".join([f"'{c}', NEW.{c}" for c in cols]) + ")"
        
        cursor.execute(f"DROP TRIGGER IF EXISTS trg_{table_name}_insert;")
        cursor.execute(f"DROP TRIGGER IF EXISTS trg_{table_name}_update;")
        cursor.execute(f"DROP TRIGGER IF EXISTS trg_{table_name}_delete;")
        
        trg_insert = f"""
        CREATE TRIGGER trg_{table_name}_insert AFTER INSERT ON {table_name}
        BEGIN
            INSERT INTO {ledger_table} (row_id, operation, old_data, new_data)
            VALUES (NEW.rowid, 'INSERT', NULL, {new_json});
        END;
        """
        
        trg_update = f"""
        CREATE TRIGGER trg_{table_name}_update AFTER UPDATE ON {table_name}
        BEGIN
            INSERT INTO {ledger_table} (row_id, operation, old_data, new_data)
            VALUES (NEW.rowid, 'UPDATE', {old_json}, {new_json});
        END;
        """
        
        trg_delete = f"""
        CREATE TRIGGER trg_{table_name}_delete AFTER DELETE ON {table_name}
        BEGIN
            INSERT INTO {ledger_table} (row_id, operation, old_data, new_data)
            VALUES (OLD.rowid, 'DELETE', {old_json}, NULL);
        END;
        """
        
        cursor.execute(trg_insert)
        cursor.execute(trg_update)
        cursor.execute(trg_delete)
        
        conn.commit()
        conn.close()
        return f"Successfully enabled Time-Travel Audit on table '{table_name}'. Shadow ledger '{ledger_table}' and triggers are active."
    except Exception as e:
        return f"Error enabling time travel: {str(e)}"


def db_restore_time_travel(db_path: str, table_name: str, target_timestamp: str, client_token: str = None) -> str:
    """Restore table data back to a specific timestamp by executing mutations in reverse."""
    try:
        _validate_write_permission(client_token)
    except PermissionError as pe:
        return str(pe)
        
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        ledger_table = f"{table_name}_ledger"
        
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{ledger_table}';")
        if not cursor.fetchone():
            conn.close()
            return f"Time travel ledger '{ledger_table}' does not exist. Enable it first using db_enable_time_travel."
            
        cursor.execute(f"PRAGMA table_info({table_name});")
        cols = [c[1] for c in cursor.fetchall()]
        
        cursor.execute(f"PRAGMA table_info({table_name});")
        pk_col = next((c[1] for c in cursor.fetchall() if c[5]), None)
        
        cursor.execute(f"DROP TRIGGER IF EXISTS trg_{table_name}_insert;")
        cursor.execute(f"DROP TRIGGER IF EXISTS trg_{table_name}_update;")
        cursor.execute(f"DROP TRIGGER IF EXISTS trg_{table_name}_delete;")
        
        cursor.execute(f"SELECT operation, row_id, old_data, new_data, ledger_id FROM {ledger_table} WHERE changed_at > ? ORDER BY ledger_id DESC;", (target_timestamp,))
        ledger_rows = cursor.fetchall()
        
        if not ledger_rows:
            conn.close()
            db_enable_time_travel(db_path, table_name, client_token=client_token)
            return f"No changes detected since timestamp '{target_timestamp}'. Database is already at this state."
            
        restored_count = 0
        
        for op, row_id, old_data_json, new_data_json, ledger_id in ledger_rows:
            if op == "INSERT":
                cursor.execute(f"DELETE FROM {table_name} WHERE rowid=?;", (row_id,))
            elif op == "DELETE":
                old_data = json.loads(old_data_json)
                col_names = ", ".join(old_data.keys())
                placeholders = ", ".join(["?"] * len(old_data))
                vals = list(old_data.values())
                cursor.execute(f"INSERT INTO {table_name} ({col_names}) VALUES ({placeholders});", vals)
            elif op == "UPDATE":
                old_data = json.loads(old_data_json)
                set_clause = ", ".join([f"{k}=?" for k in old_data.keys()])
                vals = list(old_data.values())
                
                if pk_col and pk_col in old_data:
                    pk_val = old_data[pk_col]
                    vals.append(pk_val)
                    cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE {pk_col}=?;", vals)
                else:
                    vals.append(row_id)
                    cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE rowid=?;", vals)
                    
            restored_count += 1
            
        cursor.execute(f"DELETE FROM {ledger_table} WHERE changed_at > ?;", (target_timestamp,))
        
        conn.commit()
        conn.close()
        
        db_enable_time_travel(db_path, table_name, client_token=client_token)
        
        return f"Successfully restored '{table_name}' back to '{target_timestamp}'. Undid {restored_count} database mutations."
    except Exception as e:
        try:
            db_enable_time_travel(db_path, table_name, client_token=client_token)
        except:
            pass
        return f"Error during time-travel restore operation: {str(e)}"


def db_view_table_data(db_path: str, table_name: str, limit: int = 50, offset: int = 0, sort_by: str = None, sort_order: str = "DESC", filter_conditions: str = None, output_format: str = "markdown") -> str:
    """Browse and query table data with paging, sorting, filtering, and custom output formatting."""
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        if not cursor.fetchone():
            conn.close()
            return f"Error: Table '{table_name}' does not exist in the database."
            
        cursor.execute(f"PRAGMA table_info({table_name});")
        cols = [c[1] for c in cursor.fetchall()]
        
        query = f"SELECT * FROM {table_name}"
        params = []
        
        if filter_conditions:
            words = re.findall(r'\b\w+\b', filter_conditions)
            query += f" WHERE {filter_conditions}"
            
        if sort_by:
            if sort_by in cols:
                sort_order_clean = "ASC" if sort_order.upper() == "ASC" else "DESC"
                query += f" ORDER BY {sort_by} {sort_order_clean}"
            else:
                conn.close()
                return f"Error: Sort column '{sort_by}' does not exist in table '{table_name}'."
                
        query += f" LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return _format_output(cols, rows, output_format)
    except Exception as e:
        return f"Error browsing table data: {str(e)}"


def db_summarize_table(db_path: str, table_name: str) -> str:
    """Generate a visual markdown profile containing column structures, record stats, and sample data for a table."""
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        if not cursor.fetchone():
            conn.close()
            return f"Error: Table '{table_name}' does not exist."
            
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        row_count = cursor.fetchone()[0]
        
        cursor.execute(f"PRAGMA table_info({table_name});")
        cols = cursor.fetchall()
        
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
        samples = cursor.fetchall()
        col_names = [c[1] for c in cols]
        
        report = f"## Table Summary: `{table_name}`\n"
        report += f"- **Total Records**: {row_count} rows\n"
        report += f"- **Total Columns**: {len(cols)} columns\n\n"
        
        report += "### Column Schema\n"
        report += "| Col ID | Name | Type | Not Null? | Default Value | Primary Key? |\n"
        report += "| :--- | :--- | :--- | :--- | :--- | :--- |\n"
        for cid, name, col_type, notnull, dflt, pk in cols:
            nn_str = "Yes" if notnull else "No"
            pk_str = "Yes" if pk else "No"
            dflt_str = "None" if dflt is None else str(dflt)
            report += f"| {cid} | `{name}` | {col_type} | {nn_str} | `{dflt_str}` | {pk_str} |\n"
        report += "\n"
        
        report += "### Numeric Column Profiling\n"
        num_cols = [c[1] for c in cols if any(t in c[2].upper() for t in ["INT", "REAL", "NUM", "FLOAT", "DOUBLE"])]
        if num_cols:
            report += "| Column | Min | Max | Average |\n"
            report += "| :--- | :--- | :--- | :--- |\n"
            for col in num_cols:
                cursor.execute(f"SELECT MIN({col}), MAX({col}), AVG({col}) FROM {table_name};")
                stat = cursor.fetchone()
                if stat and stat[0] is not None:
                    report += f"| `{col}` | {stat[0]} | {stat[1]} | {stat[2]:.2f} |\n"
            report += "\n"
        else:
            report += "- No numeric columns to profile.\n\n"
            
        report += "### Sample Records (Recent 5 rows)\n"
        if samples:
            sample_md = _format_output(col_names, samples, "markdown")
            report += sample_md
        else:
            report += "*No records found in table.*"
            
        conn.close()
        return report
    except Exception as e:
        return f"Error profiling table: {str(e)}"


def db_search_schema(db_path: str, search_term: str) -> str:
    """Find tables, columns, or indexes whose names contain the given search keyword."""
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = [r[0] for r in cursor.fetchall()]
        
        matches = []
        search_term_lower = search_term.lower()
        
        for table in tables:
            if search_term_lower in table.lower():
                matches.append(f"- **Table (Name Match)**: `{table}`")
                
            cursor.execute(f"PRAGMA table_info({table});")
            cols = cursor.fetchall()
            for col in cols:
                col_name = col[1]
                col_type = col[2]
                if search_term_lower in col_name.lower():
                    matches.append(f"- **Column**: `{table}.{col_name}` (Type: {col_type})")
                    
        cursor.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index';")
        indexes = cursor.fetchall()
        for idx_name, tbl_name in indexes:
            if search_term_lower in idx_name.lower():
                matches.append(f"- **Index**: `{idx_name}` on table `{tbl_name}`")
                
        conn.close()
        
        if not matches:
            return f"No schema matches found for term '{search_term}'."
            
        return f"### Schema Search Results for '{search_term}'\n" + "\n".join(matches)
    except Exception as e:
        return f"Error searching schema: {str(e)}"


def db_unmask_table_data(db_path: str, table_name: str, unmask_rules_json: str, client_token: str = None) -> str:
    """
    db_mask_table_data로 마스킹 처리된 컬럼을 원래 값으로 복원한다.
    unmask_rules_json 예시: {"email": {"prefix_len": 3, "original_col": "email_raw"}}
    복원은 shadow 테이블(원본 저장용)이 있을 경우 JOIN으로 처리한다.
    write 권한 토큰 필수.
    """
    try:
        _validate_write_permission(client_token)
    except PermissionError as pe:
        return str(pe)

    try:
        rules = json.loads(unmask_rules_json)
    except json.JSONDecodeError as je:
        return f"Error: Invalid unmask_rules_json. {je}"

    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()

        # 테이블 컬럼 확인
        cursor.execute(f"PRAGMA table_info({table_name});")
        cols_info = {row[1]: row[2] for row in cursor.fetchall()}
        if not cols_info:
            conn.close()
            return f"Error: Table '{table_name}' not found in {db_path}."

        # shadow 테이블 존재 여부 확인
        shadow_table = f"{table_name}_shadow"
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        all_tables = [r[0] for r in cursor.fetchall()]
        has_shadow = shadow_table in all_tables

        restored_cols = []
        skipped_cols = []

        for col_name, rule in rules.items():
            if col_name not in cols_info:
                skipped_cols.append(f"{col_name} (not found in table)")
                continue

            if has_shadow:
                # shadow 테이블에서 original 복원
                try:
                    cursor.execute(f"PRAGMA table_info({shadow_table});")
                    shadow_cols = [r[1] for r in cursor.fetchall()]
                    if col_name in shadow_cols:
                        cursor.execute(f"""
                            UPDATE {table_name}
                            SET {col_name} = (
                                SELECT {col_name} FROM {shadow_table}
                                WHERE {shadow_table}.rowid = {table_name}.rowid
                            )
                        """)
                        conn.commit()
                        restored_cols.append(f"{col_name} (restored from shadow)")
                    else:
                        skipped_cols.append(f"{col_name} (shadow column not found)")
                except Exception as ex:
                    skipped_cols.append(f"{col_name} (shadow restore error: {ex})")
            else:
                # 규칙 기반 역변환 (제한적 — 해시 마스킹은 복원 불가, prefix 마스킹만 가능)
                mask_type = rule.get("mask_type", "prefix")
                if mask_type == "static":
                    original_value = rule.get("original_value")
                    if original_value:
                        cursor.execute(f"UPDATE {table_name} SET {col_name} = ?", (original_value,))
                        conn.commit()
                        restored_cols.append(f"{col_name} (restored to static value)")
                    else:
                        skipped_cols.append(f"{col_name} (no original_value provided for static restore)")
                else:
                    skipped_cols.append(f"{col_name} (irreversible mask type: {mask_type})")

        conn.close()

        report = f"## 🔓 DB Unmask Report: `{table_name}`\n\n"
        report += f"**Database**: `{db_path}`  \n"
        report += f"**Shadow Table**: {'Found ✅' if has_shadow else 'Not Found ⚠️'}\n\n"
        if restored_cols:
            report += "### ✅ Restored Columns\n"
            for c in restored_cols:
                report += f"- {c}\n"
        if skipped_cols:
            report += "\n### ⚠️ Skipped / Failed\n"
            for c in skipped_cols:
                report += f"- {c}\n"

        return report

    except Exception as e:
        return f"Error in db_unmask_table_data: {str(e)}"


def db_sync_connector(src_db: str, dest_db: str, table_name: str, client_token: str = None) -> str:
    """
    소스 SQLite DB의 특정 테이블 전체를 목적지 SQLite DB로 직접 동기화한다.
    목적지에 테이블이 없으면 자동 생성, 있으면 INSERT OR REPLACE로 upsert 처리.
    write 권한 토큰 필수. 두 경로 모두 C:\\ameva 하위만 허용.
    """
    try:
        _validate_write_permission(client_token)
    except PermissionError as pe:
        return str(pe)

    try:
        src_conn = _get_connection(src_db)
        src_cursor = src_conn.cursor()

        # 소스 테이블 스키마 가져오기
        src_cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        schema_row = src_cursor.fetchone()
        if not schema_row:
            src_conn.close()
            return f"Error: Table '{table_name}' not found in source DB '{src_db}'."

        create_sql = schema_row[0]

        # 소스 데이터 읽기
        src_cursor.execute(f"SELECT * FROM {table_name}")
        rows = src_cursor.fetchall()
        col_count = len(src_cursor.description)
        col_names = [d[0] for d in src_cursor.description]
        src_conn.close()

        # 목적지 DB 경로 보안 검사 — _get_connection 이 처리
        # 목적지 DB가 없으면 생성
        dest_norm = os.path.abspath(dest_db)
        if not dest_norm.lower().startswith(r"c:\ameva"):
            return f"Security Error: Destination path must be under C:\\ameva. Got: {dest_norm}"

        dest_conn = sqlite3.connect(dest_norm)
        dest_cursor = dest_conn.cursor()

        # 목적지 테이블 생성 (없으면)
        dest_cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if not dest_cursor.fetchone():
            dest_cursor.execute(create_sql)
            dest_conn.commit()
            table_action = "created"
        else:
            table_action = "already exists"

        # Bulk upsert
        placeholders = ", ".join(["?" for _ in col_names])
        upsert_sql = f"INSERT OR REPLACE INTO {table_name} ({', '.join(col_names)}) VALUES ({placeholders})"
        dest_cursor.executemany(upsert_sql, rows)
        dest_conn.commit()
        dest_conn.close()

        return (
            f"## 🔄 DB Sync Connector\n\n"
            f"**Source**: `{src_db}`  \n"
            f"**Destination**: `{dest_db}`  \n"
            f"**Table**: `{table_name}` ({table_action})  \n"
            f"**Rows Synced**: {len(rows)}  \n"
            f"**Columns**: {', '.join(col_names)}  \n\n"
            f"✅ Sync complete. {len(rows)} record(s) upserted."
        )

    except Exception as e:
        return f"Error in db_sync_connector: {str(e)}"
```

---

### File: `src/tools/database/README.md`
```markdown
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
```

---

### File: `src/tools/dataset/dataset_aggregator.py`
```python
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
```

---

### File: `src/tools/dataset/__init__.py`
```python
# dataset tools package
```

---

### File: `src/tools/docker/docker_manager.py`
```python
import os
import subprocess
import json


def docker_container_manager(action: str, container_name: str = None, limit_lines: int = 50) -> str:
    """
    로컬 Docker 컨테이너를 관리한다.
    action: 'list' | 'start' | 'stop' | 'restart' | 'logs' | 'inspect' | 'stats'
    container_name: 대상 컨테이너 이름 또는 ID (list/stats 제외)
    limit_lines: logs 출력 줄 제한 (기본 50)
    """
    def _run_docker(*args, timeout=15):
        cmd = ["docker"] + list(args)
        try:
            res = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                stdin=subprocess.DEVNULL
            )
            return res.returncode, res.stdout.strip(), res.stderr.strip()
        except FileNotFoundError:
            return -1, "", "Docker is not installed or not in PATH."
        except subprocess.TimeoutExpired:
            return -1, "", f"Docker command timed out after {timeout}s."
        except Exception as e:
            return -1, "", str(e)

    if action == "list":
        code, out, err = _run_docker("ps", "-a", "--format",
                                     "table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}")
        if code != 0:
            return f"Error listing containers: {err}"
        if not out:
            return "No Docker containers found."
        lines = out.splitlines()
        report = "## 🐳 Docker Container List\n\n"
        report += "| Container ID | Name | Image | Status | Ports |\n"
        report += "| :----------- | :--- | :---- | :----- | :---- |\n"
        for line in lines[1:]:  # skip header
            parts = line.split("\t")
            if len(parts) >= 5:
                cid, name, image, status, ports = parts[0], parts[1], parts[2], parts[3], parts[4]
                status_icon = "🟢" if "Up" in status else "🔴"
                report += f"| `{cid[:12]}` | `{name}` | `{image}` | {status_icon} {status} | {ports or '-'} |\n"
        return report

    elif action == "stats":
        code, out, err = _run_docker("stats", "--no-stream", "--format",
                                     "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}")
        if code != 0:
            return f"Error getting stats: {err}"
        if not out:
            return "No running containers to show stats for."
        lines = out.splitlines()
        report = "## 📊 Docker Container Stats (Live Snapshot)\n\n"
        report += "| Name | CPU% | Mem Usage | Mem% | Net I/O | Block I/O |\n"
        report += "| :--- | :--: | :-------- | :--: | :------ | :-------- |\n"
        for line in lines[1:]:
            parts = line.split("\t")
            if len(parts) >= 6:
                report += f"| `{parts[0]}` | {parts[1]} | {parts[2]} | {parts[3]} | {parts[4]} | {parts[5]} |\n"
        return report

    elif action == "start":
        if not container_name:
            return "Error: container_name is required for 'start'."
        code, out, err = _run_docker("start", container_name)
        if code != 0:
            return f"Error starting '{container_name}': {err}"
        return f"✅ Container '{container_name}' started successfully."

    elif action == "stop":
        if not container_name:
            return "Error: container_name is required for 'stop'."
        code, out, err = _run_docker("stop", container_name)
        if code != 0:
            return f"Error stopping '{container_name}': {err}"
        return f"🛑 Container '{container_name}' stopped successfully."

    elif action == "restart":
        if not container_name:
            return "Error: container_name is required for 'restart'."
        code, out, err = _run_docker("restart", container_name)
        if code != 0:
            return f"Error restarting '{container_name}': {err}"
        return f"🔄 Container '{container_name}' restarted successfully."

    elif action == "logs":
        if not container_name:
            return "Error: container_name is required for 'logs'."
        code, out, err = _run_docker("logs", "--tail", str(limit_lines), "--timestamps", container_name, timeout=20)
        if code != 0:
            # Docker logs outputs to stderr normally — check combined
            combined = out or err
            if not combined:
                return f"Error getting logs for '{container_name}': {err}"
        # Docker logs typically writes to stderr
        combined = (out + "\n" + err).strip()
        lines = combined.splitlines()[-limit_lines:]
        return (
            f"## 📋 Logs: `{container_name}` (last {limit_lines} lines)\n\n"
            f"```\n{chr(10).join(lines)}\n```"
        )

    elif action == "inspect":
        if not container_name:
            return "Error: container_name is required for 'inspect'."
        code, out, err = _run_docker("inspect", container_name)
        if code != 0:
            return f"Error inspecting '{container_name}': {err}"
        try:
            data = json.loads(out)
            if data:
                info = data[0]
                report = f"## 🔍 Container Inspect: `{container_name}`\n\n"
                report += f"**ID**: `{info.get('Id', '?')[:12]}`  \n"
                report += f"**Name**: `{info.get('Name', '?')}`  \n"
                report += f"**Image**: `{info.get('Config', {}).get('Image', '?')}`  \n"
                report += f"**Status**: `{info.get('State', {}).get('Status', '?')}`  \n"
                report += f"**Started At**: `{info.get('State', {}).get('StartedAt', '?')}`  \n"
                report += f"**RestartCount**: `{info.get('RestartCount', 0)}`  \n"
                
                # 네트워크
                networks = info.get("NetworkSettings", {}).get("Networks", {})
                if networks:
                    report += "\n### Networks\n"
                    for net_name, net_info in networks.items():
                        report += f"- `{net_name}`: IP=`{net_info.get('IPAddress', '-')}`\n"
                
                # 마운트
                mounts = info.get("Mounts", [])
                if mounts:
                    report += "\n### Mounts\n"
                    for m in mounts:
                        report += f"- `{m.get('Source', '?')}` → `{m.get('Destination', '?')}` ({m.get('Mode', 'rw')})\n"
                
                return report
        except Exception:
            return f"Inspect output:\n```json\n{out[:2000]}\n```"

    else:
        return f"Error: Unknown action '{action}'. Use: list | start | stop | restart | logs | inspect | stats"
```

---

### File: `src/tools/docker/__init__.py`
```python
# docker tools package
```

---

### File: `src/tools/document/code_consolidator.py`
```python
import os
import re
import sqlite3

CODE_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".c", ".cpp", ".h", ".hpp", 
    ".rs", ".go", ".html", ".css", ".json", ".yml", ".yaml", ".toml", 
    ".sql", ".ps1", ".sh", ".bat", ".md", ".txt", ".ini", ".conf", ".cfg"
}

def map_path(path: str) -> str:
    if os.environ.get("AMEVA_IN_CONTAINER") == "true":
        normalized = path.replace("\\", "/")
        return re.sub(r'^[Cc]:/ameva', '/app/workspace', normalized)
    return path

def build_dir_tree(dir_path: str, skip_dirs: set, max_depth: int = 5, current_depth: int = 0) -> list:
    if current_depth > max_depth:
        return ["  " * current_depth + "- ... (max depth reached)"]
    
    lines = []
    try:
        items = sorted(os.listdir(dir_path))
        for item in items:
            if item in skip_dirs:
                continue
            full_item_path = os.path.join(dir_path, item)
            indent = "  " * current_depth
            if os.path.isdir(full_item_path):
                lines.append(f"{indent}- [Dir] {item}/")
                lines.extend(build_dir_tree(full_item_path, skip_dirs, max_depth, current_depth + 1))
            else:
                lines.append(f"{indent}- [File] {item}")
    except Exception as e:
        lines.append(f"{'  ' * current_depth}- [Error] {str(e)}")
    return lines

def is_sqlite_file(file_path: str) -> bool:
    _, ext = os.path.splitext(file_path.lower())
    if ext in [".db", ".sqlite", ".sqlite3", ".db3"]:
        return True
    try:
        with open(file_path, "rb") as f:
            header = f.read(16)
            return header.startswith(b"SQLite format 3\0")
    except Exception:
        return False

def extract_sqlite_schema(db_path: str) -> str:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        
        if not tables:
            return "No tables found in SQLite database.\n"
            
        schema_lines = []
        for table_name, create_sql in tables:
            if create_sql:
                schema_lines.append(f"### Table: `{table_name}`")
                schema_lines.append("```sql")
                schema_lines.append(f"{create_sql};")
                schema_lines.append("```\n")
        return "\n".join(schema_lines)
    except Exception as e:
        return f"Error extracting schema from `{os.path.basename(db_path)}`: {str(e)}\n"

def is_code_file(file_path: str) -> bool:
    _, ext = os.path.splitext(file_path.lower())
    return ext in CODE_EXTENSIONS

def read_file_content(file_path: str) -> str:
    try:
        if os.path.getsize(file_path) > 1024 * 1024:
            return "# Error: File is larger than 1MB and was skipped.\n"
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception as e:
        return f"# Error reading file: {str(e)}\n"

def get_markdown_language(file_path: str) -> str:
    _, ext = os.path.splitext(file_path.lower())
    ext_map = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".jsx": "javascript",
        ".tsx": "typescript",
        ".c": "c",
        ".cpp": "cpp",
        ".h": "c",
        ".hpp": "cpp",
        ".rs": "rust",
        ".go": "go",
        ".html": "html",
        ".css": "css",
        ".json": "json",
        ".yml": "yaml",
        ".yaml": "yaml",
        ".toml": "toml",
        ".sql": "sql",
        ".sh": "bash",
        ".ps1": "powershell",
        ".bat": "batch",
        ".md": "markdown"
    }
    return ext_map.get(ext, "")

def consolidate_codebase_logic(target_dir: str, output_file: str = None) -> str:
    """
    Consolidate codebase into a single markdown file:
    1. Directory tree structure (excluding node_modules, .git, venv, etc.)
    2. SQLite database schemas if present
    3. Source code contents
    """
    orig_target_dir = target_dir
    target_dir = map_path(target_dir)
    
    if not os.path.exists(target_dir):
        return f"Error: Target directory does not exist: {orig_target_dir} (mapped to {target_dir})"
        
    skip_dirs = {
        ".git", "node_modules", "venv", "env", ".venv", 
        "__pycache__", ".idea", ".vscode", "build", "dist", 
        ".cache", ".system_generated", "logs"
    }
    
    md_lines = []
    md_lines.append("# Codebase Consolidation Report\n")
    md_lines.append(f"- **Target Directory**: `{orig_target_dir}`\n\n")
    
    # 1. Directory Tree
    md_lines.append("## 1. Directory Structure\n")
    md_lines.append("```text\n")
    tree_lines = build_dir_tree(target_dir, skip_dirs)
    md_lines.extend([line + "\n" for line in tree_lines])
    md_lines.append("```\n\n")
    md_lines.append("---\n\n")
    
    # Scan for files and databases
    db_files = []
    code_files = []
    
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for f in files:
            full_path = os.path.join(root, f)
            if is_sqlite_file(full_path):
                db_files.append(full_path)
            elif is_code_file(full_path):
                code_files.append(full_path)
                
    # 2. Database Schema
    md_lines.append("## 2. Database Schema\n")
    if db_files:
        for db in db_files:
            rel_path = os.path.relpath(db, target_dir).replace("\\", "/")
            md_lines.append(f"### Database File: `{rel_path}`\n")
            schema_data = extract_sqlite_schema(db)
            md_lines.append(schema_data)
            md_lines.append("\n")
    else:
        md_lines.append("No SQLite databases detected in the directory.\n\n")
    md_lines.append("---\n\n")
    
    # 3. Source Codes
    md_lines.append("## 3. Source Codes\n")
    if code_files:
        for file in code_files:
            rel_path = os.path.relpath(file, target_dir).replace("\\", "/")
            lang = get_markdown_language(file)
            content = read_file_content(file)
            
            md_lines.append(f"### File: `{rel_path}`\n")
            md_lines.append(f"```{lang}\n")
            md_lines.append(content)
            if not content.endswith("\n"):
                md_lines.append("\n")
            md_lines.append("```\n\n")
            md_lines.append("---\n\n")
            
        # Pop the trailing separator
        if md_lines[-1] == "---\n\n":
            md_lines.pop()
    else:
        md_lines.append("No readable source code files detected.\n")
        
    final_md = "".join(md_lines)
    
    if output_file:
        output_file_mapped = map_path(output_file)
        out_dir = os.path.dirname(output_file_mapped)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)
        try:
            with open(output_file_mapped, "w", encoding="utf-8") as f:
                f.write(final_md)
            return f"Successfully consolidated codebase from {orig_target_dir} into {output_file}."
        except Exception as e:
            return f"Error writing consolidated report: {str(e)}"
            
    return final_md
```

---

### File: `src/tools/document/file_manager.py`
```python
import os
import subprocess
import logging

logger = logging.getLogger(__name__)

def map_path_to_container(path: str) -> str:
    """Map Windows host path to Docker container path (/app/workspace)."""
    normalized = path.replace("\\", "/")
    import re
    return re.sub(r'^[Cc]:/ameva', '/app/workspace', normalized)

def docker_delete_file(file_path: str) -> str:
    """Delete a file securely inside a Docker container."""
    container_path = map_path_to_container(file_path)
    cmd = [
        "docker", "run", "--rm",
        "-v", r"C:\ameva:/app/workspace",
        "alpine",
        "rm", "-f", container_path
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=15, stdin=subprocess.DEVNULL)
        if res.returncode != 0:
            return f"Error deleting file inside Docker: {res.stderr.strip()}"
        return f"Successfully deleted {file_path} inside Docker container."
    except Exception as e:
        return f"Exception while deleting file: {str(e)}"

def docker_move_file(src_path: str, dest_path: str) -> str:
    """Move or rename a file securely inside a Docker container."""
    container_src = map_path_to_container(src_path)
    container_dest = map_path_to_container(dest_path)
    
    # Ensure destination directory inside container exists
    dest_dir = os.path.dirname(container_dest)
    mkdir_cmd = [
        "docker", "run", "--rm",
        "-v", r"C:\ameva:/app/workspace",
        "alpine",
        "mkdir", "-p", dest_dir
    ]
    
    cmd = [
        "docker", "run", "--rm",
        "-v", r"C:\ameva:/app/workspace",
        "alpine",
        "mv", container_src, container_dest
    ]
    try:
        # Create dir first
        subprocess.run(mkdir_cmd, capture_output=True, timeout=10, stdin=subprocess.DEVNULL)
        
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=15, stdin=subprocess.DEVNULL)
        if res.returncode != 0:
            return f"Error moving file inside Docker: {res.stderr.strip()}"
        return f"Successfully moved {src_path} to {dest_path} inside Docker container."
    except Exception as e:
        return f"Exception while moving file: {str(e)}"

def docker_convert_md_to_docx(input_md_path: str, output_docx_path: str) -> str:
    """Convert Markdown to DOCX inside the ameva-mcp-server Docker container."""
    container_input = map_path_to_container(input_md_path)
    container_output = map_path_to_container(output_docx_path)
    
    # Run python script inline inside the container
    python_code = f"from tools.document.md_converter import convert_md_to_docx_logic; print(convert_md_to_docx_logic('{container_input}', '{container_output}'))"
    
    cmd = [
        "docker", "run", "--rm",
        "-v", r"C:\ameva:/app/workspace",
        "-e", "AMEVA_IN_CONTAINER=true",
        "-e", "PYTHONPATH=/app/src",
        "ameva-mcp-server",
        "python", "-c", python_code
    ]

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30, stdin=subprocess.DEVNULL)
        if res.returncode != 0:
            return f"Error converting document inside Docker: {res.stderr.strip()}"
        return res.stdout.strip()
    except Exception as e:
        return f"Exception while converting document: {str(e)}"
```

---

### File: `src/tools/document/md_converter.py`
```python
import os
import re
from docx import Document


def map_path(path: str) -> str:
    if os.environ.get("AMEVA_IN_CONTAINER") == "true":
        normalized = path.replace("\\", "/")
        return re.sub(r'^[Cc]:/ameva', '/app/workspace', normalized)
    return path


def convert_md_to_docx_logic(input_md_path: str, output_docx_path: str) -> str:
    """
    마크다운을 DOCX로 변환합니다.
    MCP 의존성이 전혀 없는 순수 파이썬 함수 (느슨한 결합)
    헤딩, 불릿, 번호목록, 코드블록, 굵은글씨, 수평선 지원.
    """
    orig_input = input_md_path
    orig_output = output_docx_path
    input_md_path = map_path(input_md_path)
    output_docx_path = map_path(output_docx_path)
    
    out_dir = os.path.dirname(output_docx_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    if not os.path.exists(input_md_path):
        return f"Error: Input file does not exist at {orig_input} (mapped to {input_md_path})"

    try:
        doc = Document()
        in_code_block = False
        code_lines = []
        numbered_counter = 0

        with open(input_md_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for raw_line in lines:
            line = raw_line.rstrip()
            
            # 코드 블록 처리
            if line.startswith("```"):
                if in_code_block:
                    # 코드 블록 종료
                    code_text = "\n".join(code_lines)
                    p = doc.add_paragraph(style="No Spacing")
                    run = p.add_run(code_text)
                    run.font.name = "Courier New"
                    run.font.size = __import__("docx.shared", fromlist=["Pt"]).Pt(9) if False else None
                    code_lines = []
                    in_code_block = False
                else:
                    in_code_block = True
                continue
            
            if in_code_block:
                code_lines.append(line)
                continue

            # 빈 줄
            if not line.strip():
                numbered_counter = 0
                continue

            # 헤딩
            if line.startswith("#### "):
                doc.add_heading(line[5:].strip(), level=4)
            elif line.startswith("### "):
                doc.add_heading(line[4:].strip(), level=3)
            elif line.startswith("## "):
                doc.add_heading(line[3:].strip(), level=2)
            elif line.startswith("# "):
                doc.add_heading(line[2:].strip(), level=1)
            # 수평선
            elif line.strip() in ["---", "***", "___"]:
                doc.add_paragraph("─" * 50)
            # 불릿 리스트
            elif line.startswith("- ") or line.startswith("* ") or line.startswith("+ "):
                text = line[2:].strip()
                # 볼드 처리
                text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
                doc.add_paragraph(text, style='List Bullet')
            # 번호 리스트
            elif re.match(r'^\d+\. ', line):
                text = re.sub(r'^\d+\. ', '', line)
                text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
                doc.add_paragraph(text, style='List Number')
            # 인용문
            elif line.startswith("> "):
                text = line[2:].strip()
                p = doc.add_paragraph(style="Quote" if "Quote" in [s.name for s in doc.styles] else "Normal")
                p.add_run(f'"{text}"').italic = True
            # 일반 텍스트 (볼드 처리 포함)
            else:
                p = doc.add_paragraph()
                # **bold** 파싱
                parts = re.split(r'\*\*(.+?)\*\*', line)
                for i, part in enumerate(parts):
                    if part:
                        run = p.add_run(part)
                        run.bold = (i % 2 == 1)
                
        doc.save(output_docx_path)
        return f"Success: Converted {orig_input} to {orig_output}"
        
    except Exception as e:
        return f"Error during conversion: {str(e)}"


def docx_to_markdown(docx_path: str, output_md_path: str = None) -> str:
    """
    .docx 파일을 마크다운(.md)으로 변환한다.
    헤딩 스타일, 리스트, 일반 단락을 파싱하여 구조화된 MD로 저장.
    output_md_path가 없으면 결과 텍스트를 직접 반환.
    """
    norm_path = map_path(docx_path)
    
    # 보안 검사
    abs_path = os.path.abspath(norm_path)
    if not abs_path.lower().startswith(r"c:\ameva") and \
       not abs_path.lower().startswith("/app/workspace"):
        return f"Security Error: Access to path '{abs_path}' is denied."
    
    if not os.path.exists(abs_path):
        return f"Error: DOCX file not found at {docx_path}"

    try:
        doc = Document(abs_path)
        md_lines = []

        for para in doc.paragraphs:
            style_name = para.style.name if para.style else "Normal"
            text = para.text.strip()
            
            if not text:
                md_lines.append("")
                continue

            # 헤딩 스타일
            if "Heading 1" in style_name:
                md_lines.append(f"# {text}")
            elif "Heading 2" in style_name:
                md_lines.append(f"## {text}")
            elif "Heading 3" in style_name:
                md_lines.append(f"### {text}")
            elif "Heading 4" in style_name:
                md_lines.append(f"#### {text}")
            elif "Heading 5" in style_name or "Heading 6" in style_name:
                md_lines.append(f"##### {text}")
            # 리스트 스타일
            elif "List Bullet" in style_name:
                md_lines.append(f"- {text}")
            elif "List Number" in style_name:
                md_lines.append(f"1. {text}")
            # 코드 스타일
            elif "Code" in style_name or "No Spacing" in style_name:
                md_lines.append(f"```\n{text}\n```")
            # 인용
            elif "Quote" in style_name:
                md_lines.append(f"> {text}")
            else:
                # 볼드/이탤릭 처리
                md_text = ""
                for run in para.runs:
                    r_text = run.text
                    if run.bold and run.italic:
                        r_text = f"***{r_text}***"
                    elif run.bold:
                        r_text = f"**{r_text}**"
                    elif run.italic:
                        r_text = f"*{r_text}*"
                    md_text += r_text
                md_lines.append(md_text if md_text.strip() else text)

        # 표 처리
        for table in doc.tables:
            if not table.rows:
                continue
            header = [cell.text.strip() for cell in table.rows[0].cells]
            md_lines.append("\n| " + " | ".join(header) + " |")
            md_lines.append("| " + " | ".join(["---"] * len(header)) + " |")
            for row in table.rows[1:]:
                cells = [cell.text.strip() for cell in row.cells]
                md_lines.append("| " + " | ".join(cells) + " |")
            md_lines.append("")

        result = "\n".join(md_lines)
        # 연속 빈 줄 정리
        result = re.sub(r"\n{3,}", "\n\n", result).strip()

        if output_md_path:
            out_norm = map_path(output_md_path)
            out_abs = os.path.abspath(out_norm)
            if not out_abs.lower().startswith(r"c:\ameva") and \
               not out_abs.lower().startswith("/app/workspace"):
                return f"Security Error: Output path '{out_abs}' is denied."
            os.makedirs(os.path.dirname(out_abs), exist_ok=True) if os.path.dirname(out_abs) else None
            with open(out_abs, "w", encoding="utf-8") as f:
                f.write(result)
            return f"Success: Converted {docx_path} to {output_md_path} ({len(result)} chars)"
        
        # 직접 반환 (3000자 제한)
        preview = result[:3000]
        if len(result) > 3000:
            preview += f"\n\n... (truncated, full length: {len(result)} chars)"
        return preview

    except Exception as e:
        return f"Error converting DOCX to Markdown: {str(e)}"


def md_image_path_fixer(doc_path: str, base_image_dir: str) -> str:
    """
    마크다운 파일 내의 깨진 이미지 경로를 실제 로컬 이미지 경로로 자동 치환한다.
    base_image_dir 하위에서 동일한 파일명을 탐색하여 경로를 교정한다.
    """
    # 경로 보안 검사
    doc_abs = os.path.abspath(doc_path)
    base_abs = os.path.abspath(base_image_dir)
    for p in [doc_abs, base_abs]:
        if not p.lower().startswith(r"c:\ameva"):
            return f"Security Error: Path must be under C:\\ameva. Got: {p}"

    if not os.path.exists(doc_abs):
        return f"Error: Markdown file not found at {doc_path}"
    if not os.path.isdir(base_abs):
        return f"Error: base_image_dir is not a directory: {base_image_dir}"

    # base_image_dir 내 모든 이미지 파일 인덱싱 (파일명 → 절대경로)
    IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp"}
    image_index = {}
    for root, _, files in os.walk(base_abs):
        for fname in files:
            if any(fname.lower().endswith(ext) for ext in IMAGE_EXTS):
                # 중복 시 첫 번째 발견 우선
                if fname.lower() not in image_index:
                    image_index[fname.lower()] = os.path.join(root, fname)

    with open(doc_abs, "r", encoding="utf-8") as f:
        content = f.read()

    # 마크다운 이미지 패턴: ![alt](path)
    pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
    
    fixed_count = 0
    not_found = []
    
    def replace_path(match):
        nonlocal fixed_count
        alt = match.group(1)
        old_path = match.group(2)
        
        # 이미 유효한 URL 이면 스킵
        if old_path.startswith("http://") or old_path.startswith("https://"):
            return match.group(0)
        
        # 파일명 추출
        img_filename = os.path.basename(old_path).lower()
        
        if img_filename in image_index:
            new_path = image_index[img_filename].replace("\\", "/")
            fixed_count += 1
            return f"![{alt}]({new_path})"
        else:
            not_found.append(old_path)
            return match.group(0)  # 그대로 유지
    
    new_content = pattern.sub(replace_path, content)
    
    if fixed_count == 0 and not not_found:
        return f"No image references found in {doc_path}."
    
    if fixed_count > 0:
        # 수정된 내용 저장
        with open(doc_abs, "w", encoding="utf-8") as f:
            f.write(new_content)
    
    report = (
        f"## 🖼️ MD Image Path Fixer\n\n"
        f"**File**: `{doc_path}`  \n"
        f"**Fixed Paths**: {fixed_count}  \n"
        f"**Not Found**: {len(not_found)}  \n"
        f"**Image Index Size**: {len(image_index)} files indexed\n\n"
    )
    if not_found:
        report += "### ⚠️ Images Not Found (path kept as-is)\n"
        for p in not_found[:10]:
            report += f"- `{p}`\n"
    if fixed_count > 0:
        report += f"\n✅ File saved with {fixed_count} corrected image path(s)."
    
    return report
```

---

### File: `src/tools/git/git_manager.py`
```python
import os
import subprocess
import re
import logging

logger = logging.getLogger(__name__)

AMEVA_IN_CONTAINER = os.environ.get("AMEVA_IN_CONTAINER") == "true"
BASE_DIR = "/app/workspace" if AMEVA_IN_CONTAINER else r"C:\ameva"

# 모든 AMEVA 리포지토리 목록
AMEVA_REPOS = [
    "AMEVA-Agent-Orchestra",
    "AMEVA-Benchmark-Suite",
    "AMEVA-Dead-Internet-Threatre",
    "AMEVA-Doc-AI",
    "AMEVA-Edge-Agent",
    "AMEVA-MCP-Toolkit-Utils",
    "AMEVA-Model-Nexus",
    "AMEVA-STT-Agent",
    "AMEVA-STT-Trainer",
    "AMEVA-Window-Assistant",
]


def _get_safe_path(repo_name: str) -> str:
    """Validate and return safe absolute path for the repository."""
    safe_name = os.path.basename(repo_name)
    path = os.path.join(BASE_DIR, safe_name)
    if not os.path.exists(path):
        raise ValueError(f"Repository {safe_name} does not exist at {path}")
    return path


def _get_safe_path_for_clone(repo_name: str) -> str:
    """Validate and return safe path for cloning a new repository."""
    safe_name = os.path.basename(repo_name)
    path = os.path.join(BASE_DIR, safe_name)
    if os.path.exists(path):
        raise ValueError(f"Directory {safe_name} already exists at {path}")
    return path


def run_git_command(repo_name: str, command: list) -> str:
    """Run a git command safely in the specified repository."""
    try:
        path = _get_safe_path(repo_name)
        full_command = ["git"] + command
        
        logger.info(f"Running command `{' '.join(full_command)}` in {path}")
        
        result = subprocess.run(
            full_command,
            cwd=path,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            check=False,
            timeout=30,
            stdin=subprocess.DEVNULL
        )
        
        output = result.stdout.strip()
        if result.returncode != 0:
            error_output = result.stderr.strip()
            return f"Git Command Error ({result.returncode}):\nStdout: {output}\nStderr: {error_output}"
        
        return output if output else "Command executed successfully with no output."
    except subprocess.TimeoutExpired:
        return f"Git command timed out after 30 seconds."
    except Exception as e:
        return f"Error executing git command: {str(e)}"


def _get_auth_url(repo_url: str) -> str:
    """If AMEVA_GITHUB_TOKEN is in env, inject it into the HTTPS repository URL."""
    token = os.environ.get("AMEVA_GITHUB_TOKEN")
    if not token:
        return repo_url
    
    if repo_url.startswith("https://") and "@" not in repo_url:
        return repo_url.replace("https://", f"https://{token}@")
    return repo_url


def git_status(repo_name: str) -> str:
    """Get the git status of a repository."""
    return run_git_command(repo_name, ["status", "-sb"])


def git_pull(repo_name: str) -> str:
    """Pull the latest changes from origin."""
    try:
        path = _get_safe_path(repo_name)
        res = subprocess.run(["git", "remote", "get-url", "origin"], cwd=path, capture_output=True, text=True, stdin=subprocess.DEVNULL)
        if res.returncode == 0:
            auth_url = _get_auth_url(res.stdout.strip())
            return run_git_command(repo_name, ["pull", auth_url])
    except Exception:
        pass
    return run_git_command(repo_name, ["pull"])


def git_commit_and_push(repo_name: str, message: str) -> str:
    """Stage all changes, commit, and push."""
    add_result = run_git_command(repo_name, ["add", "."])
    if "Error" in add_result:
        return f"Failed during git add:\n{add_result}"
        
    commit_result = run_git_command(repo_name, ["commit", "-m", message])
    if "Error" in commit_result and "nothing to commit" not in commit_result:
        return f"Failed during git commit:\n{commit_result}"
        
    try:
        path = _get_safe_path(repo_name)
        res = subprocess.run(["git", "remote", "get-url", "origin"], cwd=path, capture_output=True, text=True, stdin=subprocess.DEVNULL)
        if res.returncode == 0:
            auth_url = _get_auth_url(res.stdout.strip())
            push_result = run_git_command(repo_name, ["push", auth_url, "main"])
        else:
            push_result = run_git_command(repo_name, ["push", "origin", "main"])
        # Fetch to update local refs/remotes/origin/main tracking branch
        run_git_command(repo_name, ["fetch"])
    except Exception:
        push_result = run_git_command(repo_name, ["push", "origin", "main"])
        try:
            run_git_command(repo_name, ["fetch"])
        except:
            pass
        
    if "Error" in push_result:
        return f"Failed during git push:\n{push_result}"
        
    return f"Successfully added, committed, and pushed.\nCommit Info:\n{commit_result}\nPush Info:\n{push_result}"


def git_clone(repo_url: str, repo_name: str) -> str:
    """Clone a remote repository into BASE_DIR under the specified repo_name."""
    try:
        dest_path = _get_safe_path_for_clone(repo_name)
        auth_url = _get_auth_url(repo_url)
        
        full_command = ["git", "clone", auth_url, dest_path]
        logger.info(f"Cloning {repo_url} to {dest_path}")
        
        result = subprocess.run(
            full_command,
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            check=False,
            timeout=60,
            stdin=subprocess.DEVNULL
        )
        
        output = result.stdout.strip()
        if result.returncode != 0:
            error_output = result.stderr.strip()
            token = os.environ.get("AMEVA_GITHUB_TOKEN")
            if token:
                error_output = error_output.replace(token, "******")
            return f"Git Clone Error ({result.returncode}):\nStderr: {error_output}"
        
        return f"Successfully cloned {repo_url} into {repo_name}."
    except Exception as e:
        return f"Error executing git clone: {str(e)}"


def git_log(repo_name: str, limit: int = 10) -> str:
    """Show the git commit logs."""
    return run_git_command(repo_name, ["log", f"-n", str(limit), "--oneline", "--decorate", "--graph"])


def git_diff(repo_name: str, file_path: str = None) -> str:
    """Show changes in the working directory or compared to the index."""
    cmd = ["diff"]
    if file_path:
        cmd.append(file_path)
    return run_git_command(repo_name, cmd)


def git_branch(repo_name: str, action: str = "list", branch_name: str = None) -> str:
    """Manage branches: list, create (new), or delete (delete)."""
    if action == "list":
        return run_git_command(repo_name, ["branch", "-a"])
    elif action == "new":
        if not branch_name:
            return "Error: branch_name is required to create a new branch."
        return run_git_command(repo_name, ["branch", branch_name])
    elif action == "delete":
        if not branch_name:
            return "Error: branch_name is required to delete a branch."
        return run_git_command(repo_name, ["branch", "-d", branch_name])
    else:
        return f"Error: Unknown branch action '{action}'. Use 'list', 'new', or 'delete'."


def git_checkout(repo_name: str, branch_or_file: str, create: bool = False) -> str:
    """Switch branches or restore files."""
    cmd = ["checkout"]
    if create:
        cmd.append("-b")
    cmd.append(branch_or_file)
    return run_git_command(repo_name, cmd)


def git_merge(repo_name: str, branch_name: str) -> str:
    """Merge the specified branch into the current branch."""
    return run_git_command(repo_name, ["merge", branch_name])


def git_reset(repo_name: str, mode: str = "mixed", commit_hash: str = "HEAD") -> str:
    """Reset the current HEAD to the specified state (soft, mixed, hard)."""
    if mode not in ["soft", "mixed", "hard"]:
        return f"Error: Unknown reset mode '{mode}'. Choose from: soft, mixed, hard."
    return run_git_command(repo_name, ["reset", f"--{mode}", commit_hash])


def git_stash(repo_name: str, action: str = "push", stash_id: str = None) -> str:
    """Manage stashes: push, pop, list, apply, or clear."""
    if action == "push":
        return run_git_command(repo_name, ["stash", "push", "-m", stash_id or "Stashed by MCP"])
    elif action == "pop":
        cmd = ["stash", "pop"]
        if stash_id:
            cmd.append(stash_id)
        return run_git_command(repo_name, cmd)
    elif action == "list":
        return run_git_command(repo_name, ["stash", "list"])
    elif action == "apply":
        cmd = ["stash", "apply"]
        if stash_id:
            cmd.append(stash_id)
        return run_git_command(repo_name, cmd)
    elif action == "clear":
        return run_git_command(repo_name, ["stash", "clear"])
    else:
        return f"Error: Unknown stash action '{action}'. Use 'push', 'pop', 'list', 'apply', or 'clear'."


# ──────────────────────────────────────────────
# 신규 Git 도구 (고도화)
# ──────────────────────────────────────────────

def workspace_git_broadcaster() -> str:
    """
    C:\\ameva 하위의 모든 AMEVA 리포지토리를 일괄 스캔하여
    각 레포의 현재 상태(브랜치, ahead/behind, 변경파일 수)를 종합 보고한다.
    """
    results = []
    report = "## 📡 AMEVA Workspace Git Broadcast\n\n"
    report += f"**Scanned Base Dir**: `{BASE_DIR}`  \n"
    report += f"**Timestamp**: `{__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`\n\n"
    report += "| Repository | Branch | Status | Changed Files | Ahead | Behind |\n"
    report += "| :--------- | :----- | :----- | :-----------: | :---: | :----: |\n"

    # BASE_DIR 내 실제 git 레포 탐색 (AMEVA_REPOS + 자동탐색)
    repos_to_scan = list(AMEVA_REPOS)
    try:
        for d in os.listdir(BASE_DIR):
            full = os.path.join(BASE_DIR, d)
            if os.path.isdir(full) and os.path.isdir(os.path.join(full, ".git")):
                if d not in repos_to_scan:
                    repos_to_scan.append(d)
    except Exception:
        pass

    for repo_name in repos_to_scan:
        repo_path = os.path.join(BASE_DIR, repo_name)
        if not os.path.isdir(os.path.join(repo_path, ".git")):
            report += f"| `{repo_name}` | - | ❌ Not a git repo | - | - | - |\n"
            continue

        try:
            # 브랜치명
            branch_res = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=repo_path, capture_output=True, text=True, timeout=5, stdin=subprocess.DEVNULL
            )
            branch = branch_res.stdout.strip() if branch_res.returncode == 0 else "?"

            # fetch (최신 원격 상태 반영)
            subprocess.run(
                ["git", "fetch", "--quiet"],
                cwd=repo_path, capture_output=True, timeout=10, stdin=subprocess.DEVNULL
            )

            # ahead/behind
            ab_res = subprocess.run(
                ["git", "rev-list", "--left-right", "--count", f"HEAD...origin/{branch}"],
                cwd=repo_path, capture_output=True, text=True, timeout=5, stdin=subprocess.DEVNULL
            )
            if ab_res.returncode == 0 and ab_res.stdout.strip():
                parts = ab_res.stdout.strip().split()
                ahead = parts[0] if len(parts) > 0 else "0"
                behind = parts[1] if len(parts) > 1 else "0"
            else:
                ahead, behind = "?", "?"

            # 변경된 파일 수
            status_res = subprocess.run(
                ["git", "status", "--short"],
                cwd=repo_path, capture_output=True, text=True, timeout=5, stdin=subprocess.DEVNULL
            )
            changed = len([l for l in status_res.stdout.strip().splitlines() if l.strip()])

            # 상태 아이콘
            if changed == 0 and ahead == "0" and behind == "0":
                status_icon = "✅ Clean"
            elif changed > 0:
                status_icon = f"📝 Modified"
            elif int(ahead) > 0 if ahead.isdigit() else False:
                status_icon = "⬆️ Ahead"
            elif int(behind) > 0 if behind.isdigit() else False:
                status_icon = "⬇️ Behind"
            else:
                status_icon = "⚠️ Unknown"

            report += f"| `{repo_name}` | `{branch}` | {status_icon} | {changed} | {ahead} | {behind} |\n"

        except Exception as ex:
            report += f"| `{repo_name}` | ? | ⚠️ Error: {str(ex)[:40]} | - | - | - |\n"

    return report


def git_commit_helper(repo_name: str) -> str:
    """
    현재 스테이징된 diff를 분석하고 Conventional Commits 스펙에 맞는
    커밋 메시지를 자동 생성하여 추천한다.
    변경 내용을 파싱해 type, scope, subject, body를 구성한다.
    """
    try:
        path = _get_safe_path(repo_name)

        # 스테이지 된 변경사항 가져오기
        staged = subprocess.run(
            ["git", "diff", "--staged", "--stat"],
            cwd=path, capture_output=True, text=True, timeout=10, stdin=subprocess.DEVNULL
        )
        staged_diff = subprocess.run(
            ["git", "diff", "--staged", "--name-only"],
            cwd=path, capture_output=True, text=True, timeout=10, stdin=subprocess.DEVNULL
        )

        if staged.returncode != 0:
            return f"Error getting staged diff: {staged.stderr.strip()}"

        stat_output = staged.stdout.strip()
        changed_files = [f.strip() for f in staged_diff.stdout.strip().splitlines() if f.strip()]

        if not changed_files:
            # 스테이지 안된 경우 — 현재 변경 파일도 확인
            unstaged = subprocess.run(
                ["git", "diff", "--name-only"],
                cwd=path, capture_output=True, text=True, timeout=10, stdin=subprocess.DEVNULL
            )
            unstaged_files = [f.strip() for f in unstaged.stdout.strip().splitlines() if f.strip()]
            if unstaged_files:
                return (
                    "⚠️ No staged changes found.\n"
                    f"Unstaged files ({len(unstaged_files)}):\n" +
                    "\n".join(f"  - {f}" for f in unstaged_files[:10]) +
                    "\n\nRun `git add .` or `git add <file>` first."
                )
            return "ℹ️ No changes detected (working tree is clean)."

        # 변경 타입 추론 로직
        def infer_type(files: list) -> str:
            paths_str = " ".join(files).lower()
            if any(f.endswith((".md", ".rst", ".txt")) for f in files):
                return "docs"
            if any("test" in f or "spec" in f for f in files):
                return "test"
            if any(f in paths_str for f in ["requirements", "dockerfile", "docker-compose", ".yml", ".yaml", "setup.py"]):
                return "build"
            if any("fix" in f or "bug" in f or "patch" in f for f in files):
                return "fix"
            if any(f.endswith(".py") for f in files):
                return "feat"
            return "chore"

        def infer_scope(files: list) -> str:
            dirs = set()
            for f in files:
                parts = f.replace("\\", "/").split("/")
                if len(parts) > 1:
                    dirs.add(parts[-2])  # 부모 폴더명
            if not dirs:
                return ""
            if len(dirs) == 1:
                return list(dirs)[0]
            return "multi"

        commit_type = infer_type(changed_files)
        scope = infer_scope(changed_files)
        scope_str = f"({scope})" if scope else ""

        # 변경 파일 기반 subject 생성
        file_names = [os.path.basename(f) for f in changed_files[:3]]
        subject_base = ", ".join(file_names)
        if len(changed_files) > 3:
            subject_base += f" and {len(changed_files) - 3} more"

        # 추천 메시지들
        suggestions = [
            f"{commit_type}{scope_str}: update {subject_base}",
            f"{commit_type}{scope_str}: add/modify {subject_base}",
            f"{commit_type}{scope_str}: refactor {subject_base}",
        ]

        report = (
            f"## 🤖 Git Commit Message Helper\n\n"
            f"**Repository**: `{repo_name}`  \n"
            f"**Staged Files** ({len(changed_files)}):\n"
        )
        for f in changed_files[:15]:
            report += f"  - `{f}`\n"
        if len(changed_files) > 15:
            report += f"  - *... and {len(changed_files)-15} more*\n"

        report += f"\n**Diff Summary**:\n```\n{stat_output}\n```\n\n"
        report += "### 💡 Recommended Commit Messages\n\n"
        for i, msg in enumerate(suggestions, 1):
            report += f"{i}. `{msg}`\n"

        report += (
            f"\n### Conventional Commits Format\n"
            f"```\n"
            f"<type>(<scope>): <short description>\n\n"
            f"[optional body]\n\n"
            f"[optional footer]\n"
            f"```\n\n"
            f"**Types**: feat | fix | docs | style | refactor | test | build | chore | perf | ci\n"
        )
        return report

    except ValueError as ve:
        return f"Error: {str(ve)}"
    except Exception as e:
        return f"Error in git_commit_helper: {str(e)}"
```

---

### File: `src/tools/git/README.md`
```markdown
# Git MCP API Specification for AI Agents

본 명세서는 AMEVA MCP Toolkit 내의 Git 관련 도구(Git MCP Tools)를 AI 에이전트가 오작동 없이 정확하게 활용할 수 있도록 돕는 API 명세 및 활용 가이드라인입니다.

---

## 1. 전제 조건 및 인증 규칙

- **작업 경로 기준**: 모든 Git 도구는 `repo_name` 파라미터를 입력받습니다. 이는 서버 내부에서 안전성 검증을 거쳐 `C:\ameva\<repo_name>`(컨테이너 외부 실행 기준) 경로로 매핑됩니다. 에이전트는 절대 경로를 전달하는 대신 저장소 디렉토리명만 주입해야 합니다.
- **인증 토큰 자동 주입**: 원격 관련 명령(`git_pull`, `git_commit_and_push`, `git_clone`) 수행 시, 환경 변수 `AMEVA_GITHUB_TOKEN`이 설정되어 있다면 HTTPS 주소에 개인 접근 토큰(PAT)이 자동으로 주입되어 무인증 푸시/풀을 수행합니다.

---

## 2. API 상세 명세

### 1) git_status
- **설명**: 작업 공간의 현재 상태 및 스테이징 상태를 간결하게 요약 조회합니다. (`git status -sb` 수준)
- **파라미터**:
  - `repo_name` (string, 필수): 검사할 저장소 이름 (예: `AMEVA-Doc-AI`)
- **반환값**: 현재 활성화된 브랜치 정보 및 수정/추적되지 않은 파일 목록.

### 2) git_log
- **설명**: 해당 저장소의 커밋 히스토리를 요약하여 반환합니다.
- **파라미터**:
  - `repo_name` (string, 필수): 저장소 이름
  - `limit` (integer, 기본값: 10): 조회할 최근 커밋 개수
- **반환값**: 커밋 그래프 정보가 담긴 단선 형식(`--oneline`)의 커밋 목록.

### 3) git_diff
- **설명**: 현재 작업 디렉토리에서 수정된 변경 사항(Diff)을 확인합니다.
- **파라미터**:
  - `repo_name` (string, 필수): 저장소 이름
  - `file_path` (string, 선택): 특정 파일의 변경 사항만 조회하고 싶을 때 상대 경로 전달
- **반환값**: 표준 unified diff 형식의 텍스트 결과물.

### 4) git_clone
- **설명**: 새로운 원격 저장소를 지정된 이름으로 로컬에 복제합니다.
- **파라미터**:
  - `repo_url` (string, 필수): 깃허브 등 원격 저장소 HTTPS 주소
  - `repo_name` (string, 필수): 복제하여 생성할 로컬 폴더 이름
- **반환값**: 성공 또는 실패 에러 메시지. (에러 발생 시 토큰 유출 방지를 마스킹 처리함)

### 5) git_pull
- **설명**: 원격 저장소(`origin`)로부터 최신 커밋을 가져와 현재 브랜치에 병합합니다.
- **파라미터**:
  - `repo_name` (string, 필수): 저장소 이름
- **반환값**: 풀 수행 결과 출력문.

### 6) git_commit_and_push
- **설명**: 로컬의 모든 변경 사항(신규 파일 포함)을 스테이징한 후 커밋 메시지와 함께 즉시 원격 저장소로 푸시합니다. (`git add . && git commit -m <message> && git push` 일괄 처리)
- **파라미터**:
  - `repo_name` (string, 필수): 저장소 이름
  - `commit_message` (string, 필수): 변경점을 요약한 커밋 메시지
- **반환값**: 커밋 결과 정보 및 푸시 성공 여부.

### 7) git_branch
- **설명**: 저장소 내의 브랜치를 조회, 생성 또는 삭제합니다.
- **파라미터**:
  - `repo_name` (string, 필수): 저장소 이름
  - `action` (string, 기본값: `list`): 수행할 작업 (`list`, `new`, `delete`)
  - `branch_name` (string, 선택): `action`이 `new` 또는 `delete`일 때 조작할 브랜치 명
- **반환값**: 브랜치 목록 혹은 변경/삭제 성공 상태 메시지.

### 8) git_checkout
- **설명**: 활성화된 브랜치를 전환하거나 특정 파일의 변경 상태를 복구합니다.
- **파라미터**:
  - `repo_name` (string, 필수): 저장소 이름
  - `branch_or_file` (string, 필수): 이동할 브랜치 명 또는 복구할 파일 경로
  - `create` (boolean, 기본값: `False`): `True`로 설정할 시 새 브랜치를 생성하여 전환 (`-b` 옵션)
- **반환값**: 전환/복구 결과 정보.

### 9) git_merge
- **설명**: 대상 브랜치의 변경 사항을 현재 브랜치로 가져와 병합합니다.
- **파라미터**:
  - `repo_name` (string, 필수): 저장소 이름
  - `branch_name` (string, 필수): 병합을 가져올 대상 브랜치 명
- **반환값**: 병합 결과 및 충돌(Conflict) 발생 유무.

### 10) git_reset
- **설명**: 현재 HEAD 위치를 특정 커밋 지점이나 상태로 되돌립니다.
- **파라미터**:
  - `repo_name` (string, 필수): 저장소 이름
  - `mode` (string, 기본값: `mixed`): 리셋 종류 (`soft`, `mixed`, `hard`)
  - `commit_hash` (string, 기본값: `HEAD`): 복구 기준 커밋 해시 값 또는 상대 위치
- **반환값**: 리셋 수행 성공 정보.

### 11) git_stash
- **설명**: 현재 작업 디렉토리의 변경 사항을 임시 저장(Stash) 공간으로 대피시킵니다.
- **파라미터**:
  - `repo_name` (string, 필수): 저장소 이름
  - `action` (string, 기본값: `push`): 수행할 stash 작업 (`push`, `pop`, `list`, `apply`, `clear`)
  - `stash_id` (string, 선택): push 할 때의 간단한 메시지명 또는 pop/apply 대상 인덱스 번호 (예: `stash@{0}`)
- **반환값**: 대피/복구 작업 수행 로그.

---

## 3. AI 에이전트 행동 가이드라인 (Best Practices)

1. **상태 조회의 의무화**:
   - `git_commit_and_push`를 수행하기 전에는 반드시 `git_status` 혹은 `git_diff`를 호출하여 현재 로컬 작업 디렉토리에 정확히 어떤 수정사항들이 반영되어 있는지 점검하십시오.
2. **충돌 처리 규칙**:
   - `git_merge` 또는 `git_pull` 수행 중 병합 충돌(Conflict)이 발생할 경우, 에이전트는 충돌 파일을 직접 읽어 수정한 후 `git_commit_and_push` 도구를 사용해 충돌을 해소하는 커밋을 생성해야 합니다.
3. **위험 도구 사용 지양**:
   - `git_reset --hard`는 로컬의 미커밋 변경분을 완전히 삭제할 수 있으므로, 예외 상황이 아니면 기본 모드(`--mixed` 또는 `--soft`)를 권장합니다.
```

---

### File: `src/tools/git/__init__.py`
```python
# Git toolkit
```

---

### File: `src/tools/network/net_discovery.py`
```python
import socket
import json
import concurrent.futures
import ipaddress
from datetime import datetime


def _scan_port(host: str, port: int, timeout: float = 0.5) -> tuple[int, bool, str]:
    """단일 포트 스캔 — (port, is_open, banner)"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((host, port))
        is_open = (result == 0)
        banner = ""
        if is_open:
            try:
                sock.settimeout(0.3)
                banner = sock.recv(256).decode("utf-8", errors="ignore").strip()[:60]
            except Exception:
                pass
        return port, is_open, banner
    except Exception:
        return port, False, ""
    finally:
        sock.close()


def _get_service_name(port: int) -> str:
    """알려진 포트 서비스명 반환."""
    WELL_KNOWN = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
        53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
        443: "HTTPS", 465: "SMTPS", 587: "SMTP-TLS",
        1433: "MSSQL", 3306: "MySQL", 3389: "RDP",
        5000: "Flask/Dev", 5432: "PostgreSQL", 5900: "VNC",
        6379: "Redis", 7860: "Gradio", 8000: "FastAPI/Dev",
        8080: "HTTP-Alt", 8443: "HTTPS-Alt", 8501: "Streamlit",
        8888: "Jupyter", 9200: "Elasticsearch", 11434: "Ollama",
        19530: "Milvus", 27017: "MongoDB", 50051: "gRPC",
    }
    try:
        return socket.getservbyport(port) if port not in WELL_KNOWN else WELL_KNOWN[port]
    except Exception:
        return WELL_KNOWN.get(port, "unknown")


def service_discovery(
    subnet: str = "127.0.0.1",
    ports_json: str = "[22, 80, 8000, 8080, 8501]",
    timeout: float = 0.5,
    max_hosts: int = 254
) -> str:
    """
    지정 서브넷 또는 단일 호스트를 스캔하여 활성 서비스 포트를 식별한다.
    AMEVA 노드(Streamlit, FastAPI, Gradio, Ollama 등)의 상태 파악에 최적화.

    subnet: 단일 IP (예: 192.168.0.1) 또는 CIDR (예: 192.168.0.0/24)
    ports_json: 스캔할 포트 목록 JSON (예: [22, 80, 8000, 8080, 8501])
    timeout: 포트당 타임아웃 초 (기본 0.5)
    max_hosts: 서브넷 스캔 시 최대 호스트 수 제한 (기본 254)
    """
    # 포트 파싱
    try:
        ports = json.loads(ports_json)
        if not isinstance(ports, list):
            return "Error: ports_json must be a JSON array (e.g., [22, 80, 8080])"
        ports = [int(p) for p in ports if 0 < int(p) < 65536]
    except Exception as e:
        return f"Error parsing ports_json: {e}"

    if not ports:
        return "Error: No valid ports provided."

    # 호스트 목록 결정
    hosts = []
    try:
        # CIDR 서브넷 여부 확인
        if "/" in subnet:
            network = ipaddress.ip_network(subnet, strict=False)
            host_list = list(network.hosts())
            if len(host_list) > max_hosts:
                return (
                    f"Error: Subnet '{subnet}' has {len(host_list)} hosts. "
                    f"Max allowed: {max_hosts}. Use a smaller range or increase max_hosts."
                )
            hosts = [str(h) for h in host_list]
        else:
            # 단일 호스트
            hosts = [subnet]
    except ValueError as ve:
        return f"Error: Invalid subnet/IP '{subnet}': {ve}"

    if not hosts:
        return f"No hosts to scan in {subnet}."

    start_time = datetime.now()
    results = {}  # host -> [(port, is_open, banner)]

    # 병렬 스캔 (스레드 풀)
    total_tasks = len(hosts) * len(ports)
    MAX_WORKERS = min(100, total_tasks)

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {}
        for host in hosts:
            for port in ports:
                fut = executor.submit(_scan_port, host, port, timeout)
                futures[fut] = host

        for fut in concurrent.futures.as_completed(futures):
            host = futures[fut]
            try:
                port, is_open, banner = fut.result()
                if host not in results:
                    results[host] = []
                results[host].append((port, is_open, banner))
            except Exception:
                pass

    elapsed = (datetime.now() - start_time).total_seconds()

    # 활성 호스트만 필터링
    active_hosts = {h: ports_res for h, ports_res in results.items()
                    if any(is_open for _, is_open, _ in ports_res)}

    # 리포트 작성
    report = (
        f"## 🌐 Network Service Discovery\n\n"
        f"**Target**: `{subnet}`  \n"
        f"**Ports Scanned**: `{ports}`  \n"
        f"**Hosts Scanned**: {len(hosts)}  \n"
        f"**Active Hosts**: {len(active_hosts)}  \n"
        f"**Scan Time**: {elapsed:.2f}s\n\n"
    )

    if not active_hosts:
        report += "🔴 No active hosts with open ports found.\n"
        return report

    report += "---\n\n"
    for host in sorted(active_hosts.keys()):
        open_ports = [(p, b) for p, is_open, b in sorted(active_hosts[host]) if is_open]
        closed_count = len(ports) - len(open_ports)

        # 호스트명 역방향 조회 시도
        try:
            hostname = socket.gethostbyaddr(host)[0]
        except Exception:
            hostname = ""

        report += f"### 🟢 Host: `{host}`"
        if hostname and hostname != host:
            report += f" (`{hostname}`)"
        report += f"\n\n"

        report += "| Port | Service | Status | Banner |\n"
        report += "| :--- | :------ | :----: | :----- |\n"
        for port, banner in open_ports:
            svc = _get_service_name(port)
            report += f"| `{port}` | {svc} | 🟢 OPEN | `{banner or '-'}` |\n"

        # AMEVA 특화 서비스 인식
        ameva_services = []
        open_port_nums = [p for p, _ in open_ports]
        if 8501 in open_port_nums:
            ameva_services.append("📊 Streamlit App")
        if any(p in open_port_nums for p in [8000, 5000]):
            ameva_services.append("⚡ FastAPI/Flask Server")
        if 7860 in open_port_nums:
            ameva_services.append("🎨 Gradio UI")
        if 11434 in open_port_nums:
            ameva_services.append("🤖 Ollama LLM Server")
        if 6379 in open_port_nums:
            ameva_services.append("💾 Redis Cache")
        if 19530 in open_port_nums:
            ameva_services.append("🔢 Milvus Vector DB")

        if ameva_services:
            report += f"\n**Detected AMEVA Services**: {', '.join(ameva_services)}\n"
        report += "\n---\n\n"

    return report.strip()
```

---

### File: `src/tools/network/__init__.py`
```python
# network tools package
```

---

### File: `src/tools/search/code_searcher.py`
```python
import os
import re
import math
from collections import defaultdict


AMEVA_BASE = r"C:\ameva"


def _tf_idf_search(query: str, corpus: list[dict], top_k: int = 10) -> list[dict]:
    """
    TF-IDF / BM25 기반 텍스트 검색. 
    corpus: [{"path": str, "text": str, "lines": [(lineno, line)]}]
    """
    # 토크나이징
    def tokenize(text: str) -> list[str]:
        return re.findall(r"[a-zA-Z_]\w*", text.lower())

    query_tokens = set(tokenize(query))
    if not query_tokens:
        return []

    N = len(corpus)
    # IDF 계산
    df = defaultdict(int)
    for doc in corpus:
        doc_tokens = set(tokenize(doc["text"]))
        for t in query_tokens:
            if t in doc_tokens:
                df[t] += 1

    idf = {t: math.log((N - df[t] + 0.5) / (df[t] + 0.5) + 1) for t in query_tokens}

    # BM25 파라미터
    k1 = 1.5
    b = 0.75
    avg_dl = sum(len(tokenize(d["text"])) for d in corpus) / max(N, 1)

    scores = []
    for doc in corpus:
        doc_tokens = tokenize(doc["text"])
        dl = len(doc_tokens)
        tf_map = defaultdict(int)
        for t in doc_tokens:
            tf_map[t] += 1

        score = 0.0
        for t in query_tokens:
            if t in tf_map:
                tf = tf_map[t]
                numerator = tf * (k1 + 1)
                denominator = tf + k1 * (1 - b + b * dl / max(avg_dl, 1))
                score += idf.get(t, 0) * (numerator / denominator)

        if score > 0:
            scores.append((score, doc))

    scores.sort(key=lambda x: -x[0])
    return [doc for _, doc in scores[:top_k]]


def vector_code_searcher(
    query: str,
    file_ext: str = ".py",
    search_root: str = None,
    top_k: int = 10,
    context_lines: int = 3
) -> str:
    """
    AMEVA 프로젝트 소스코드 전역을 BM25 알고리즘으로 검색하여
    질의어와 가장 유관한 코드 조각과 함수/클래스를 반환한다.
    
    query: 검색어 (자연어 또는 코드 키워드)
    file_ext: 검색할 파일 확장자 (기본: .py, 여러 개: ".py,.js,.ts")
    search_root: 검색 루트 경로 (기본: C:\\ameva)
    top_k: 반환할 최대 파일 수
    context_lines: 매칭 라인 주변 컨텍스트 줄 수
    """
    if not query or not query.strip():
        return "Error: query cannot be empty."

    base = search_root or AMEVA_BASE
    base_norm = os.path.abspath(base)
    if not base_norm.lower().startswith(r"c:\ameva"):
        return f"Security Error: search_root must be under C:\\ameva. Got: {base_norm}"

    # 확장자 파싱
    extensions = [e.strip().lower() for e in file_ext.split(",")]
    if not all(e.startswith(".") for e in extensions):
        return f"Error: file_ext must start with '.' (e.g., '.py' or '.py,.js')"

    # 파일 수집
    corpus = []
    file_count = 0
    for root, dirs, files in os.walk(base_norm):
        # 제외 폴더
        dirs[:] = [d for d in dirs if d not in {
            "__pycache__", ".git", "node_modules", ".venv", "venv",
            "dist", "build", ".mypy_cache", ".pytest_cache"
        }]
        for fname in files:
            if any(fname.lower().endswith(ext) for ext in extensions):
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                    text = "".join(lines)
                    corpus.append({
                        "path": fpath,
                        "text": text,
                        "lines": [(i + 1, l.rstrip()) for i, l in enumerate(lines)]
                    })
                    file_count += 1
                except Exception:
                    continue

    if not corpus:
        return f"No files with extension(s) '{file_ext}' found under {base_norm}."

    # BM25 검색
    results = _tf_idf_search(query, corpus, top_k=top_k)

    if not results:
        return f"No results found for query: '{query}'"

    # 결과 포맷
    report = (
        f"## 🔍 Code Searcher Results\n\n"
        f"**Query**: `{query}`  \n"
        f"**Extension(s)**: `{file_ext}`  \n"
        f"**Files Indexed**: {file_count}  \n"
        f"**Top Results**: {len(results)}\n\n"
    )
    report += "---\n\n"

    query_tokens = set(re.findall(r"[a-zA-Z_]\w*", query.lower()))

    for rank, doc in enumerate(results, 1):
        path = doc["path"]
        rel_path = os.path.relpath(path, AMEVA_BASE)
        all_lines = doc["lines"]

        # 쿼리 토큰과 매칭되는 라인 탐색
        matching_lines = []
        for lineno, line in all_lines:
            line_tokens = set(re.findall(r"[a-zA-Z_]\w*", line.lower()))
            if query_tokens & line_tokens:
                matching_lines.append(lineno)

        report += f"### #{rank} `{rel_path}`\n\n"

        if matching_lines:
            # 첫 번째 매칭 라인 주변 컨텍스트 출력
            for match_lineno in matching_lines[:3]:
                start = max(0, match_lineno - 1 - context_lines)
                end = min(len(all_lines), match_lineno + context_lines)
                snippet_lines = all_lines[start:end]

                report += f"*Line {match_lineno}:*\n```{file_ext.split(',')[0][1:]}\n"
                for lno, ltext in snippet_lines:
                    marker = ">>>" if lno == match_lineno else "   "
                    report += f"{marker} {lno:4d} | {ltext}\n"
                report += "```\n\n"
        else:
            # 파일 상위 표시
            preview_lines = all_lines[:10]
            report += "```\n"
            for lno, ltext in preview_lines:
                report += f"{lno:4d} | {ltext}\n"
            report += "```\n\n"

        report += "---\n\n"

    return report.strip()
```

---

### File: `src/tools/search/__init__.py`
```python
# search tools package
```

---

### File: `src/tools/ssh/ssh_manager.py`
```python
import paramiko
import logging
import io

logger = logging.getLogger(__name__)

def ssh_run_command(host: str, username: str, command: str, port: int = 22, password: str = None, key_content: str = None) -> str:
    """Run a shell command on a remote server via SSH."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        if key_content:
            key_file = io.StringIO(key_content.strip())
            # Try RSA key first, fallback to Ed25519/ECDSA
            try:
                pkey = paramiko.RSAKey.from_private_key(key_file)
            except Exception:
                key_file.seek(0)
                try:
                    pkey = paramiko.Ed25519Key.from_private_key(key_file)
                except Exception:
                    key_file.seek(0)
                    pkey = paramiko.ECDSAKey.from_private_key(key_file)
            client.connect(hostname=host, port=port, username=username, pkey=pkey, timeout=15)
        elif password:
            client.connect(hostname=host, port=port, username=username, password=password, timeout=15)
        else:
            return "Error: Either password or key_content must be provided for SSH authentication."
            
        stdin, stdout, stderr = client.exec_command(command, timeout=30)
        
        out = stdout.read().decode('utf-8', errors='replace')
        err = stderr.read().decode('utf-8', errors='replace')
        exit_status = stdout.channel.recv_exit_status()
        
        client.close()
        
        if exit_status != 0:
            return f"SSH Command Failed (exit code {exit_status}):\nStdout: {out}\nStderr: {err}"
        return out if out else "Command executed successfully with no output."
        
    except Exception as e:
        return f"SSH Connection/Execution Error: {str(e)}"
```

---

### File: `src/tools/utils/README.md`
```markdown
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
```

---

### File: `src/tools/utils/utils_manager.py`
```python
import os
import psutil
import socket
import uuid
import json
import base64
import hashlib
import requests
import subprocess
import platform
import threading
import time
import re
from datetime import datetime
from urllib.parse import urlparse


# ──────────────────────────────────────────────
# 기존 유틸리티 (유지)
# ──────────────────────────────────────────────

def get_system_info() -> str:
    """Retrieve host system information (CPU, Memory, Disk, OS)."""
    try:
        cpu_pct = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('C:\\' if os.name == 'nt' else '/')
        os_info = f"{os.name} ({psutil.users()[0].name if psutil.users() else 'Unknown'})"
        
        info = (
            f"OS: {os_info}\n"
            f"CPU Usage: {cpu_pct}%\n"
            f"RAM: Total={mem.total // (1024**2)}MB, Available={mem.available // (1024**2)}MB, Used={mem.percent}%\n"
            f"Disk (System): Total={disk.total // (1024**3)}GB, Free={disk.free // (1024**3)}GB, Used={disk.percent}%"
        )
        return info
    except Exception as e:
        return f"Error getting system info: {str(e)}"

def check_port(host: str, port: int) -> str:
    """Check if a specific TCP port on a host is open/active."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3.0)
    try:
        result = sock.connect_ex((host, port))
        if result == 0:
            return f"Port {port} on {host} is OPEN."
        else:
            return f"Port {port} on {host} is CLOSED (code {result})."
    except Exception as e:
        return f"Error checking port: {str(e)}"
    finally:
        sock.close()

def generate_uuid() -> str:
    """Generate a random UUID v4."""
    return str(uuid.uuid4())

def format_json(json_str: str) -> str:
    """Format and validate a JSON string (pretty print)."""
    try:
        parsed = json.loads(json_str)
        return json.dumps(parsed, indent=2, ensure_ascii=False)
    except json.JSONDecodeError as je:
        return f"Invalid JSON format. Error: {je.msg} at line {je.lineno}, col {je.colno}"
    except Exception as e:
        return f"Error parsing JSON: {str(e)}"

def base64_encode_decode(mode: str, data: str) -> str:
    """Encode or decode base64 strings. mode can be 'encode' or 'decode'."""
    try:
        if mode == 'encode':
            return base64.b64encode(data.encode('utf-8')).decode('utf-8')
        elif mode == 'decode':
            return base64.b64decode(data.encode('utf-8')).decode('utf-8')
        else:
            return "Error: Mode must be 'encode' or 'decode'."
    except Exception as e:
        return f"Error: {str(e)}"

def map_path_to_container(path: str) -> str:
    """Map Windows host path to Docker container path (/app/workspace)."""
    normalized = path.replace("\\", "/")
    return re.sub(r'^[Cc]:/ameva', '/app/workspace', normalized)

def docker_calculate_file_hash(file_path: str, algorithm: str = "sha256") -> str:
    """Calculate file checksum hash inside a Docker container for isolation."""
    container_path = map_path_to_container(file_path)
    prog = "sha256sum" if algorithm.lower() == "sha256" else "md5sum"
    cmd = [
        "docker", "run", "--rm",
        "-v", r"C:\ameva:/app/workspace",
        "alpine",
        prog, container_path
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=20, stdin=subprocess.DEVNULL)
        if res.returncode != 0:
            return f"Error calculating hash in Docker: {res.stderr.strip()}"
        return res.stdout.strip()
    except Exception as e:
        return f"Exception calculating file hash: {str(e)}"

def get_external_ip() -> str:
    """Retrieve the host's external IP address and internal network IP."""
    internal_ip = "Unknown"
    external_ip = "Unknown"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        internal_ip = s.getsockname()[0]
        s.close()
    except Exception:
        pass
        
    try:
        res = requests.get("https://api.ipify.org?format=json", timeout=5)
        if res.status_code == 200:
            external_ip = res.json().get("ip", "Unknown")
    except Exception:
        pass
        
    return f"Internal IP: {internal_ip}\nExternal IP: {external_ip}"

def send_http_request(method: str, url: str, headers_json: str = None, body: str = None) -> str:
    """Send an arbitrary HTTP request (GET/POST/PUT/DELETE) and return status/body."""
    try:
        headers = json.loads(headers_json) if headers_json else {}
        method_upper = method.upper()
        
        res = requests.request(
            method=method_upper,
            url=url,
            headers=headers,
            data=body,
            timeout=15
        )
        
        preview = res.text[:1000] + "\n... (truncated)" if len(res.text) > 1000 else res.text
        return f"Status: {res.status_code} {res.reason}\nHeaders: {dict(res.headers)}\nResponse:\n{preview}"
    except Exception as e:
        return f"HTTP Request Error: {str(e)}"

def docker_find_large_files(dir_path: str, size_mb: int = 50) -> str:
    """Find files larger than size_mb MB inside the directory, running in Docker."""
    container_path = map_path_to_container(dir_path)
    find_arg = f"+{size_mb}M"
    cmd = [
        "docker", "run", "--rm",
        "-v", r"C:\ameva:/app/workspace",
        "alpine",
        "find", container_path, "-type", "f", "-size", find_arg
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30, stdin=subprocess.DEVNULL)
        if res.returncode != 0:
            return f"Error finding large files in Docker: {res.stderr.strip()}"
        out = res.stdout.strip()
        if not out:
            return f"No files larger than {size_mb}MB found in {dir_path}."
        return f"Files larger than {size_mb}MB in {dir_path}:\n{out}"
    except Exception as e:
        return f"Exception finding large files: {str(e)}"

def extract_text_from_url(url: str) -> str:
    """Fetch URL and extract raw body text, stripping all HTML tags."""
    try:
        from bs4 import BeautifulSoup
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AMEVA-Agent/1.0"}
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return f"Error: HTTP {res.status_code}"
            
        soup = BeautifulSoup(res.text, "html.parser")
        for script in soup(["script", "style"]):
            script.decompose()
            
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = "\n".join(chunk for chunk in chunks if chunk)
        
        return clean_text[:3000] + "\n... (truncated to 3000 chars)" if len(clean_text) > 3000 else clean_text
    except Exception as e:
        return f"Error extracting text: {str(e)}"


# ──────────────────────────────────────────────
# 신규 유틸리티 (고도화 추가)
# ──────────────────────────────────────────────

def gpu_monitor() -> str:
    """
    nvidia-smi를 통해 실시간 GPU 상태를 조회한다.
    GPU명, 사용률, VRAM 점유율, 온도, 전력을 표 형식으로 반환.
    """
    try:
        # nvidia-smi query
        query_fields = (
            "index,name,utilization.gpu,memory.used,memory.total,"
            "temperature.gpu,power.draw,power.limit,driver_version"
        )
        cmd = [
            "nvidia-smi",
            f"--query-gpu={query_fields}",
            "--format=csv,noheader,nounits"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=10, stdin=subprocess.DEVNULL)
        
        if res.returncode != 0:
            # GPU가 없거나 nvidia-smi 미설치 — 대안으로 wmic 시도 (Windows)
            if os.name == "nt":
                wmic_cmd = ["wmic", "path", "Win32_VideoController", "get",
                           "Name,AdapterRAM,VideoMemoryType", "/format:list"]
                wmic = subprocess.run(wmic_cmd, capture_output=True, text=True, timeout=10, stdin=subprocess.DEVNULL)
                if wmic.returncode == 0:
                    return f"nvidia-smi not available. GPU info via WMI:\n{wmic.stdout.strip()}"
            return f"GPU monitor unavailable: {res.stderr.strip() or 'nvidia-smi not found'}"
        
        lines = [l.strip() for l in res.stdout.strip().split("\n") if l.strip()]
        if not lines:
            return "No GPU devices detected."
        
        report = "## 🖥️ GPU Monitor\n\n"
        report += "| # | GPU | Util% | VRAM Used | VRAM Total | Temp°C | Power | Driver |\n"
        report += "| :- | :-- | :---: | :-------: | :--------: | :----: | :---- | :----- |\n"
        
        for line in lines:
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 9:
                idx, name, util, vram_used, vram_total, temp, pwr_draw, pwr_limit, drv = parts[:9]
                vram_pct = round(int(vram_used) / int(vram_total) * 100, 1) if vram_total.isdigit() else "?"
                report += (
                    f"| {idx} | {name} | {util}% | {vram_used}MB ({vram_pct}%) | "
                    f"{vram_total}MB | {temp}°C | {pwr_draw}W / {pwr_limit}W | {drv} |\n"
                )
        
        return report

    except FileNotFoundError:
        return "Error: nvidia-smi is not installed or not in PATH."
    except Exception as e:
        return f"Error in gpu_monitor: {str(e)}"


def system_thermal_scanner() -> str:
    """
    CPU 온도, 클럭, 코어별 사용률을 스캔한다.
    Windows: WMI, Linux/Mac: psutil sensors 활용.
    """
    try:
        report = "## 🌡️ System Thermal & Clock Scanner\n\n"
        
        # CPU 기본 정보
        cpu_freq = psutil.cpu_freq()
        cpu_pct_per_core = psutil.cpu_percent(interval=0.5, percpu=True)
        cpu_count_logical = psutil.cpu_count(logical=True)
        cpu_count_physical = psutil.cpu_count(logical=False)

        report += f"**CPU Cores**: Physical={cpu_count_physical}, Logical={cpu_count_logical}\n"
        if cpu_freq:
            report += (
                f"**Clock**: Current={cpu_freq.current:.0f}MHz, "
                f"Min={cpu_freq.min:.0f}MHz, Max={cpu_freq.max:.0f}MHz\n\n"
            )

        # 코어별 사용률 테이블
        report += "### Core Usage\n"
        report += "| Core | Usage% |\n| :--- | :----: |\n"
        for i, pct in enumerate(cpu_pct_per_core):
            bar = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
            report += f"| Core {i} | {bar} {pct:.1f}% |\n"

        # 온도 센서 (Linux/Mac)
        if hasattr(psutil, "sensors_temperatures"):
            temps = psutil.sensors_temperatures()
            if temps:
                report += "\n### Temperature Sensors\n"
                report += "| Sensor | Label | Current°C | High°C | Critical°C |\n"
                report += "| :----- | :---- | :-------: | :----: | :--------: |\n"
                for name, entries in temps.items():
                    for entry in entries:
                        report += (
                            f"| {name} | {entry.label or '-'} | "
                            f"{entry.current:.1f} | "
                            f"{entry.high or '-'} | "
                            f"{entry.critical or '-'} |\n"
                        )
            else:
                report += "\n*Temperature sensors not accessible on this system.*\n"
        else:
            # Windows — WMI 시도
            if os.name == "nt":
                try:
                    wmi_cmd = (
                        'powershell -Command "Get-WmiObject MSAcpi_ThermalZoneTemperature '
                        '-Namespace root/wmi | Select-Object CurrentTemperature | '
                        'ForEach-Object { ($_.CurrentTemperature / 10 - 273.15).ToString(\'F1\') }"'
                    )
                    wmi_res = subprocess.run(wmi_cmd, shell=True, capture_output=True, text=True, timeout=10)
                    if wmi_res.returncode == 0 and wmi_res.stdout.strip():
                        report += f"\n**CPU Temperature (WMI)**: {wmi_res.stdout.strip()}°C\n"
                    else:
                        report += "\n*WMI thermal sensor not accessible (admin required).*\n"
                except Exception:
                    report += "\n*Temperature data unavailable on Windows without admin.*\n"

        return report

    except Exception as e:
        return f"Error in system_thermal_scanner: {str(e)}"


def process_watchdog(action: str, process_name: str = None) -> str:
    """
    활성 프로세스 목록 스캔, 특정 프로세스 감시, 강제 종료를 수행한다.
    action: 'list' | 'find' | 'kill' | 'restart'
    process_name: 대상 프로세스명 (find/kill/restart 시 필요)
    """
    try:
        if action == "list":
            procs = []
            for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_info", "status"]):
                try:
                    info = proc.info
                    mem_mb = info["memory_info"].rss // (1024 * 1024) if info["memory_info"] else 0
                    procs.append((info["pid"], info["name"], info["cpu_percent"], mem_mb, info["status"]))
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            # CPU 사용률 기준 내림차순 정렬
            procs.sort(key=lambda x: x[2], reverse=True)
            
            report = "## ⚙️ Active Process Watchdog\n\n"
            report += f"**Total Processes**: {len(procs)}\n\n"
            report += "| PID | Name | CPU% | Mem(MB) | Status |\n"
            report += "| :-- | :--- | :--: | :-----: | :----- |\n"
            for pid, name, cpu, mem, status in procs[:30]:
                report += f"| {pid} | {name} | {cpu:.1f} | {mem} | {status} |\n"
            if len(procs) > 30:
                report += f"\n*... and {len(procs) - 30} more processes*\n"
            return report

        elif action == "find":
            if not process_name:
                return "Error: process_name is required for 'find' action."
            
            found = []
            for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_info", "status", "cmdline"]):
                try:
                    if process_name.lower() in proc.info["name"].lower():
                        mem_mb = proc.info["memory_info"].rss // (1024 * 1024) if proc.info["memory_info"] else 0
                        cmdline = " ".join(proc.info["cmdline"] or [])[:80]
                        found.append(f"PID={proc.info['pid']}, Name={proc.info['name']}, "
                                     f"CPU={proc.info['cpu_percent']:.1f}%, Mem={mem_mb}MB, "
                                     f"Status={proc.info['status']}\nCMD: {cmdline}")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if not found:
                return f"No process matching '{process_name}' found."
            return f"### Found {len(found)} process(es) matching '{process_name}':\n\n" + "\n---\n".join(found)

        elif action == "kill":
            if not process_name:
                return "Error: process_name is required for 'kill' action."
            
            killed = []
            for proc in psutil.process_iter(["pid", "name"]):
                try:
                    if process_name.lower() in proc.info["name"].lower():
                        proc.terminate()
                        killed.append(f"PID={proc.info['pid']}, Name={proc.info['name']}")
                except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                    killed.append(f"Failed to kill PID={proc.info.get('pid','?')}: {e}")
            
            if not killed:
                return f"No process matching '{process_name}' found to kill."
            return f"### Terminated {len(killed)} process(es):\n" + "\n".join(killed)

        else:
            return f"Error: Unknown action '{action}'. Use 'list', 'find', or 'kill'."

    except Exception as e:
        return f"Error in process_watchdog: {str(e)}"


def task_cron_scheduler(action: str, job_name: str = None, cron_expression: str = None, command: str = None) -> str:
    """
    Windows Task Scheduler 또는 cron 작업을 관리한다.
    action: 'list' | 'create' | 'delete' | 'run'
    Windows 환경에서는 schtasks 커맨드를 래핑한다.
    """
    try:
        if os.name != "nt":
            # Linux/Mac: crontab 기반
            if action == "list":
                res = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=10)
                if res.returncode != 0:
                    return "No crontab found for current user."
                return f"### Current Crontab:\n```\n{res.stdout.strip()}\n```"
            elif action == "create":
                if not job_name or not cron_expression or not command:
                    return "Error: job_name, cron_expression, and command are all required for 'create'."
                # 기존 crontab 읽기 후 추가
                existing = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
                existing_content = existing.stdout if existing.returncode == 0 else ""
                new_line = f"{cron_expression} {command} # AMEVA:{job_name}\n"
                new_content = existing_content + new_line
                proc = subprocess.run(["crontab", "-"], input=new_content, text=True, timeout=10)
                if proc.returncode == 0:
                    return f"Cron job '{job_name}' created: `{cron_expression} {command}`"
                return f"Error creating cron job: {proc.stderr}"
            elif action == "delete":
                if not job_name:
                    return "Error: job_name is required for 'delete'."
                existing = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
                if existing.returncode != 0:
                    return "No crontab to delete from."
                lines = [l for l in existing.stdout.splitlines() if f"# AMEVA:{job_name}" not in l]
                subprocess.run(["crontab", "-"], input="\n".join(lines) + "\n", text=True, timeout=10)
                return f"Cron job '{job_name}' deleted."
            else:
                return f"Unknown action '{action}' for cron."

        # Windows: schtasks
        if action == "list":
            res = subprocess.run(
                ["schtasks", "/query", "/fo", "TABLE", "/nh"],
                capture_output=True, text=True, timeout=15, stdin=subprocess.DEVNULL
            )
            if res.returncode != 0:
                return f"Error listing tasks: {res.stderr.strip()}"
            lines = res.stdout.strip().splitlines()
            report = f"### Scheduled Tasks ({len(lines)} found)\n```\n"
            report += "\n".join(lines[:50])
            if len(lines) > 50:
                report += f"\n... ({len(lines)-50} more)"
            report += "\n```"
            return report

        elif action == "create":
            if not job_name or not command:
                return "Error: job_name and command are required for 'create'."
            # cron_expression을 Windows 스케줄로 간단 변환 (분 단위)
            trigger = "/SC MINUTE /MO 60"  # 기본: 1시간마다
            if cron_expression:
                parts = cron_expression.split()
                if len(parts) >= 2 and parts[0] == "*" and parts[1] == "*":
                    trigger = "/SC MINUTE /MO 1"
                elif len(parts) >= 2 and parts[1].isdigit():
                    trigger = f"/SC DAILY /ST {int(parts[1]):02d}:00"
            
            cmd_str = (
                f'schtasks /create /tn "AMEVA\\{job_name}" /tr "{command}" '
                f'{trigger} /f'
            )
            res = subprocess.run(cmd_str, shell=True, capture_output=True, text=True, timeout=15)
            if res.returncode == 0:
                return f"Task '{job_name}' created successfully."
            return f"Error creating task: {res.stderr.strip()}"

        elif action == "delete":
            if not job_name:
                return "Error: job_name is required for 'delete'."
            res = subprocess.run(
                ["schtasks", "/delete", "/tn", f"AMEVA\\{job_name}", "/f"],
                capture_output=True, text=True, timeout=10, stdin=subprocess.DEVNULL
            )
            if res.returncode == 0:
                return f"Task '{job_name}' deleted."
            return f"Error deleting task: {res.stderr.strip()}"

        elif action == "run":
            if not job_name:
                return "Error: job_name is required for 'run'."
            res = subprocess.run(
                ["schtasks", "/run", "/tn", f"AMEVA\\{job_name}"],
                capture_output=True, text=True, timeout=10, stdin=subprocess.DEVNULL
            )
            if res.returncode == 0:
                return f"Task '{job_name}' triggered manually."
            return f"Error running task: {res.stderr.strip()}"

        else:
            return f"Error: Unknown action '{action}'. Use 'list', 'create', 'delete', or 'run'."

    except Exception as e:
        return f"Error in task_cron_scheduler: {str(e)}"


def rest_client_simulator(method: str, url: str, payload_json: str = None, headers_json: str = None) -> str:
    """
    REST API 모의 요청 클라이언트. curl 없이 REST API를 테스트한다.
    응답을 보기 좋은 포맷으로 반환하며 curl 등가 명령어도 출력한다.
    """
    try:
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            return f"Error: Invalid URL '{url}'"

        headers = json.loads(headers_json) if headers_json else {}
        payload = None
        if payload_json:
            try:
                payload = json.loads(payload_json)
                if "Content-Type" not in headers:
                    headers["Content-Type"] = "application/json"
            except json.JSONDecodeError:
                payload = payload_json  # raw string

        method_upper = method.upper()

        # curl 등가 명령어 생성
        curl_headers = " ".join([f'-H "{k}: {v}"' for k, v in headers.items()])
        curl_body = f"-d '{payload_json}'" if payload_json else ""
        curl_equiv = f"curl -X {method_upper} {curl_headers} {curl_body} \"{url}\""

        # 요청 실행
        start = time.time()
        if isinstance(payload, dict):
            res = requests.request(method_upper, url, headers=headers, json=payload, timeout=15)
        else:
            res = requests.request(method_upper, url, headers=headers, data=payload, timeout=15)
        elapsed_ms = round((time.time() - start) * 1000, 1)

        # 응답 파싱
        content_type = res.headers.get("Content-Type", "")
        try:
            if "json" in content_type:
                body_parsed = json.dumps(res.json(), indent=2, ensure_ascii=False)
            else:
                body_parsed = res.text[:2000]
        except Exception:
            body_parsed = res.text[:2000]

        report = (
            f"## 🌐 REST Client Simulator\n\n"
            f"**Request**: `{method_upper} {url}`  \n"
            f"**Status**: `{res.status_code} {res.reason}`  \n"
            f"**Response Time**: `{elapsed_ms}ms`  \n"
            f"**Content-Type**: `{content_type}`  \n\n"
            f"### Response Headers\n```\n"
        )
        for k, v in dict(res.headers).items():
            report += f"{k}: {v}\n"
        report += f"```\n\n### Response Body\n```json\n{body_parsed}\n```\n\n"
        report += f"### curl Equivalent\n```bash\n{curl_equiv}\n```\n"

        return report

    except requests.exceptions.Timeout:
        return f"Error: Request to {url} timed out after 15 seconds."
    except requests.exceptions.ConnectionError as e:
        return f"Error: Could not connect to {url}. {str(e)}"
    except Exception as e:
        return f"Error in rest_client_simulator: {str(e)}"


def html_to_pdf_renderer(html_path_or_url: str, output_pdf_path: str) -> str:
    """
    HTML 파일 또는 URL을 PDF로 변환한다.
    우선순위: weasyprint → pdfkit(wkhtmltopdf) → 불가 시 안내 메시지.
    출력 경로는 C:\\ameva 하위만 허용.
    """
    # 출력 경로 보안 검사
    out_norm = os.path.abspath(output_pdf_path)
    if not out_norm.lower().startswith(r"c:\ameva"):
        return f"Security Error: Output path must be under C:\\ameva. Got: {out_norm}"

    os.makedirs(os.path.dirname(out_norm), exist_ok=True) if os.path.dirname(out_norm) else None

    # 입력 소스 결정
    is_url = html_path_or_url.startswith("http://") or html_path_or_url.startswith("https://")
    if not is_url:
        src_norm = os.path.abspath(html_path_or_url)
        if not src_norm.lower().startswith(r"c:\ameva"):
            return f"Security Error: Source path must be under C:\\ameva. Got: {src_norm}"
        if not os.path.exists(src_norm):
            return f"Error: HTML file not found at {src_norm}"
        source = f"file:///{src_norm.replace(chr(92), '/')}"
    else:
        source = html_path_or_url

    # 방법 1: weasyprint
    try:
        import weasyprint
        if is_url:
            weasyprint.HTML(url=source).write_pdf(out_norm)
        else:
            weasyprint.HTML(filename=os.path.abspath(html_path_or_url)).write_pdf(out_norm)
        size_kb = os.path.getsize(out_norm) // 1024
        return f"✅ PDF rendered via WeasyPrint.\nOutput: {out_norm} ({size_kb}KB)"
    except ImportError:
        pass
    except Exception as e:
        pass

    # 방법 2: pdfkit (wkhtmltopdf wrapper)
    try:
        import pdfkit
        pdfkit.from_url(source, out_norm)
        size_kb = os.path.getsize(out_norm) // 1024
        return f"✅ PDF rendered via pdfkit (wkhtmltopdf).\nOutput: {out_norm} ({size_kb}KB)"
    except ImportError:
        pass
    except Exception as e:
        pass

    # 방법 3: Windows — Edge/Chrome CLI headless
    if os.name == "nt":
        edge_paths = [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        ]
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
        for browser_path in edge_paths + chrome_paths:
            if os.path.exists(browser_path):
                try:
                    cmd = [
                        browser_path,
                        "--headless",
                        "--disable-gpu",
                        f"--print-to-pdf={out_norm}",
                        source
                    ]
                    res = subprocess.run(cmd, capture_output=True, timeout=30, stdin=subprocess.DEVNULL)
                    if os.path.exists(out_norm) and os.path.getsize(out_norm) > 0:
                        size_kb = os.path.getsize(out_norm) // 1024
                        return f"✅ PDF rendered via {os.path.basename(browser_path)} headless.\nOutput: {out_norm} ({size_kb}KB)"
                except Exception:
                    continue

    return (
        "⚠️ HTML to PDF conversion failed. No compatible renderer found.\n"
        "Install one of the following:\n"
        "  pip install weasyprint\n"
        "  pip install pdfkit  (requires wkhtmltopdf binary)\n"
        "  Or ensure Microsoft Edge / Google Chrome is installed."
    )
```

---

### File: `src/tools/web/crawl_bot.py`
```python
import os
import subprocess
import re
import math
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup


def web_readability_cleaner(url: str) -> str:
    """
    웹 페이지에서 광고, 네비게이션, 사이드바 등을 제거하고
    본문 콘텐츠만 추출해 깔끔한 마크다운으로 변환한다.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AMEVA-Reader/1.0"
        }
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return f"Error: HTTP {res.status_code} {res.reason}"

        soup = BeautifulSoup(res.text, "html.parser")

        # 노이즈 태그 제거 (광고, 네비, 푸터, 사이드바, 스크립트 등)
        noise_tags = [
            "script", "style", "noscript", "header", "footer", "nav",
            "aside", "form", "iframe", "button", "svg", "img",
            "figure", "figcaption", "advertisement", "ads", "banner"
        ]
        noise_classes = [
            "nav", "navigation", "sidebar", "menu", "footer", "header",
            "ad", "advertisement", "banner", "cookie", "popup", "modal",
            "social", "share", "comment", "related", "breadcrumb"
        ]

        for tag in soup(noise_tags):
            tag.decompose()

        # 클래스 기반 노이즈 제거
        for cls in noise_classes:
            for el in soup.find_all(class_=re.compile(cls, re.IGNORECASE)):
                el.decompose()

        # 본문 후보 탐색 (article > main > body 순)
        content_el = (
            soup.find("article") or
            soup.find("main") or
            soup.find(id=re.compile(r"(content|main|article|post)", re.IGNORECASE)) or
            soup.find(class_=re.compile(r"(content|main|article|post)", re.IGNORECASE)) or
            soup.body
        )

        if not content_el:
            return "Error: Could not extract readable content from this page."

        # HTML → Markdown 변환
        markdown_lines = []
        title_tag = soup.title
        if title_tag:
            markdown_lines.append(f"# {title_tag.string.strip()}\n")
            markdown_lines.append(f"> Source: {url}\n")
            markdown_lines.append("---\n")

        for el in content_el.descendants:
            if not hasattr(el, "name"):
                continue
            if el.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                level = int(el.name[1])
                text = el.get_text(strip=True)
                if text:
                    markdown_lines.append(f"\n{'#' * level} {text}\n")
            elif el.name == "p":
                text = el.get_text(strip=True)
                if text and len(text) > 20:
                    markdown_lines.append(f"\n{text}\n")
            elif el.name in ["ul", "ol"]:
                for li in el.find_all("li", recursive=False):
                    text = li.get_text(strip=True)
                    if text:
                        markdown_lines.append(f"- {text}")
            elif el.name == "pre":
                code = el.get_text()
                markdown_lines.append(f"\n```\n{code.strip()}\n```\n")
            elif el.name == "blockquote":
                text = el.get_text(strip=True)
                if text:
                    markdown_lines.append(f"\n> {text}\n")

        result = "\n".join(markdown_lines)
        result = re.sub(r"\n{3,}", "\n\n", result)

        if len(result) > 5000:
            return result[:5000] + "\n\n... (truncated to 5000 chars)"
        return result if result.strip() else "No readable content found."

    except Exception as e:
        return f"Error in web_readability_cleaner: {str(e)}"


def dead_link_scanner(md_file_path: str) -> str:
    """
    마크다운 파일 내의 모든 URL 링크를 추출하고 
    HTTP HEAD 요청으로 응답 상태를 전수 검사한다 (404 데드링크 식별).
    """
    # 경로 보안 검사
    normalized = os.path.abspath(md_file_path)
    if not normalized.lower().startswith(r"c:\ameva"):
        return f"Security Error: Access to path '{normalized}' is denied."

    if not os.path.exists(normalized):
        return f"Error: File not found at {md_file_path}"

    try:
        with open(normalized, "r", encoding="utf-8") as f:
            content = f.read()

        # 마크다운 링크 패턴: [text](url) 및 bare URL
        url_pattern = re.compile(
            r"\[.*?\]\((https?://[^\s\)]+)\)|"
            r"(?<!\()(https?://[^\s\)>\]\"\',]+)"
        )
        found_urls = list(set(url_pattern.findall(content)))
        # findall은 그룹 튜플 반환 — flatten
        flat_urls = []
        for match in found_urls:
            if isinstance(match, tuple):
                flat_urls.extend([m for m in match if m])
            else:
                flat_urls.append(match)
        flat_urls = list(set(flat_urls))

        if not flat_urls:
            return f"No URLs found in {md_file_path}."

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AMEVA-LinkChecker/1.0"
        }

        results = {"alive": [], "dead": [], "error": []}

        for url in flat_urls:
            try:
                r = requests.head(url, headers=headers, timeout=8, allow_redirects=True)
                if r.status_code < 400:
                    results["alive"].append({"url": url, "status": r.status_code})
                else:
                    results["dead"].append({"url": url, "status": r.status_code})
            except requests.exceptions.ConnectionError:
                results["dead"].append({"url": url, "status": "CONNECTION_ERROR"})
            except requests.exceptions.Timeout:
                results["error"].append({"url": url, "status": "TIMEOUT"})
            except Exception as ex:
                results["error"].append({"url": url, "status": str(ex)[:50]})

        total = len(flat_urls)
        report = (
            f"## 🔗 Dead Link Scanner Report\n"
            f"**File**: `{md_file_path}`  \n"
            f"**Total URLs scanned**: {total}  \n"
            f"**✅ Alive**: {len(results['alive'])}  \n"
            f"**❌ Dead**: {len(results['dead'])}  \n"
            f"**⚠️ Error**: {len(results['error'])}\n\n"
        )

        if results["dead"]:
            report += "### ❌ Dead Links\n"
            report += "| URL | Status |\n| :--- | :--- |\n"
            for item in results["dead"]:
                report += f"| `{item['url']}` | `{item['status']}` |\n"
            report += "\n"

        if results["error"]:
            report += "### ⚠️ Error Links\n"
            report += "| URL | Reason |\n| :--- | :--- |\n"
            for item in results["error"]:
                report += f"| `{item['url']}` | `{item['status']}` |\n"
            report += "\n"

        if results["alive"]:
            report += "### ✅ Alive Links\n"
            report += "| URL | Status |\n| :--- | :--- |\n"
            for item in results["alive"][:20]:  # 최대 20개 표시
                report += f"| `{item['url']}` | `{item['status']}` |\n"
            if len(results["alive"]) > 20:
                report += f"| ... | ({len(results['alive']) - 20} more) |\n"

        return report

    except Exception as e:
        return f"Error in dead_link_scanner: {str(e)}"


def crawl_website(url: str, selector: str = None) -> str:
    """
    Crawls a website URL, extracts the Title, Metadata, clean Text content, 
    and lists all unique internal & external links.
    Optionally filters by a CSS selector.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AMEVA-Crawler/1.0"
        }
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return f"Error crawling {url}: HTTP {res.status_code} {res.reason}"
            
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 1. Metadata
        title = soup.title.string.strip() if soup.title else "No Title"
        meta_desc = ""
        desc_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
        if desc_tag:
            meta_desc = desc_tag.get("content", "").strip()
            
        # 2. Main Content (filter by selector if provided)
        content_soup = soup
        if selector:
            selected = soup.select(selector)
            if selected:
                content_soup = BeautifulSoup("".join(str(s) for s in selected), 'html.parser')
                
        # Strip script/style
        for tag in content_soup(["script", "style", "meta", "noscript", "header", "footer"]):
            tag.decompose()
            
        raw_text = content_soup.get_text()
        lines = (line.strip() for line in raw_text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = "\n".join(chunk for chunk in chunks if chunk)
        
        # 3. Links analysis
        parsed_base = urlparse(url)
        base_domain = parsed_base.netloc
        
        internal_links = set()
        external_links = set()
        
        for link in soup.find_all("a", href=True):
            href = link.get("href").strip()
            if not href or href.startswith("#") or href.startswith("javascript:"):
                continue
            full_url = urljoin(url, href)
            parsed_link = urlparse(full_url)
            
            if parsed_link.netloc == base_domain:
                internal_links.add(full_url)
            else:
                external_links.add(full_url)
                
        # Format the output
        summary = (
            f"=== CRAWL REPORT FOR: {url} ===\n"
            f"Title: {title}\n"
            f"Meta Description: {meta_desc}\n\n"
            f"--- CLEAN TEXT CONTENT (Preview) ---\n"
            f"{clean_text[:1200]}\n"
            f"... (Truncated, total length: {len(clean_text)} chars)\n\n"
            f"--- LINKS ANALYSIS ---\n"
            f"Internal Links found: {len(internal_links)}\n"
            f"External Links found: {len(external_links)}\n"
        )
        
        if internal_links:
            summary += "\nInternal Links sample (max 5):\n" + "\n".join(list(internal_links)[:5])
        if external_links:
            summary += "\nExternal Links sample (max 5):\n" + "\n".join(list(external_links)[:5])
            
        return summary
    except Exception as e:
        return f"Exception while crawling {url}: {str(e)}"
```

---

### File: `src/utils/audit_logger.py`
```python
import os
import json
import time
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

AUDIT_LOG_PATH = "/app/workspace/AMEVA-MCP-Toolkit-Utils/mcp_audit.jsonl" if os.environ.get("AMEVA_IN_CONTAINER") == "true" else r"C:\ameva\AMEVA-MCP-Toolkit-Utils\mcp_audit.jsonl"

MAX_RETRIES = 5
RETRY_DELAY = 0.01  # 10ms

def log_mcp_action(tool_name: str, args: dict, result: str, status: str = "success", caller: str = "Unknown"):
    """
    Append an audit log record to a JSONL file using a Spin Lock to handle Windows I/O locks.
    """
    def _truncate_args(d: dict, max_len: int = 500) -> dict:
        truncated = {}
        for k, v in d.items():
            if isinstance(v, str) and len(v) > max_len:
                truncated[k] = f"{v[:max_len]}... (truncated, total length: {len(v)})"
            elif isinstance(v, dict):
                truncated[k] = _truncate_args(v, max_len)
            else:
                truncated[k] = v
        return truncated

    record = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "caller": caller,
        "tool": tool_name,
        "args": _truncate_args(args),
        "status": status,
        "result_preview": result[:200] + "..." if len(result) > 200 else result
    }
    
    line = json.dumps(record, ensure_ascii=False) + "\n"
    
    for attempt in range(MAX_RETRIES):
        try:
            with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
                f.write(line)
            return  # Success
        except PermissionError:
            # File is locked by another process, wait and retry
            logger.warning(f"I/O lock encountered on {AUDIT_LOG_PATH}. Retrying {attempt+1}/{MAX_RETRIES}...")
            time.sleep(RETRY_DELAY)
        except Exception as e:
            logger.error(f"Failed to write audit log: {e}")
            break
            
    logger.error(f"Failed to write audit log after {MAX_RETRIES} attempts.")
```

---

### File: `src/utils/README.md`
```markdown
# AMEVA MCP Internal Utilities (utils)

이 디렉토리는 MCP 서버 구동 및 관리에 필요한 내부 공통 헬퍼 스크립트를 모아둔 곳입니다.
이곳의 모듈들은 AI 에이전트에게 도구(Tool)로 직접 노출되지 않으며, 서버 시스템 내부에서만 호출됩니다.

## 주요 모듈 구성
- **[audit_logger.py](audit_logger.py)**: 도구 호출 이력 및 인수를 mcp_audit.jsonl에 동기식으로 기록하는 보안 감사 로거.
- **[view_stats.py](view_stats.py)**: 서버 사용 통계 및 메트릭 데이터를 취합하는 모듈.
```

---

### File: `src/utils/view_stats.py`
```python
import json
from collections import Counter
from pathlib import Path

AUDIT_LOG_PATH = Path(r"C:\ameva\AMEVA-MCP-Toolkit-Utils\mcp_audit.jsonl")

def print_audit_stats():
    if not AUDIT_LOG_PATH.exists():
        print("Audit log is empty.")
        return

    total = 0
    status_counts = Counter()
    tool_counts = Counter()

    with open(AUDIT_LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            try:
                record = json.loads(line)
                total += 1
                status_counts[record.get("status", "unknown")] += 1
                tool_counts[record.get("tool", "unknown")] += 1
            except json.JSONDecodeError:
                pass

    print("="*40)
    print(" [ AMEVA MCP Audit Log Statistics ] ")
    print("="*40)
    print(f"Total Tool Executions: {total}")
    print("\n[Status Breakdown]")
    for status, count in status_counts.items():
        print(f"  - {status.upper()}: {count} ({count/total*100:.1f}%)")
    
    print("\n[Most Used Tools]")
    for tool, count in tool_counts.most_common():
        print(f"  - {tool}: {count} times")
    print("="*40)

if __name__ == "__main__":
    print_audit_stats()
```

---

### File: `src/utils/__init__.py`
```python
# Utils package
```

