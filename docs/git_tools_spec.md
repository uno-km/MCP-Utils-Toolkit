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
