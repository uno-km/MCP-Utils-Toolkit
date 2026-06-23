#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AMEVA OS: Git Pre-commit Hook Installer
Installs a Python-based Git hook that scans staged files for hardcoded tokens and rejects commits.
"""

import os
import sys
import stat

HOOK_CONTENT = """#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import subprocess
import re

# GitHub Token patterns: ghp_ (Personal Access Token), ghs_ (Server/GitHub Actions Token)
TOKEN_PATTERN = re.compile(r'\\b(ghp_|ghs_)[A-Za-z0-9_]{36,251}\\b')

def main():
    try:
        res = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True, text=True, check=True
        )
        staged_files = [f.strip() for f in res.stdout.splitlines() if f.strip()]
    except Exception as e:
        print(f"[PRE-COMMIT ERROR] Failed to query staged files: {e}")
        sys.exit(1)

    blocked = False
    for file_path in staged_files:
        # Check only code/doc files
        if not (file_path.endswith(".py") or file_path.endswith(".js") or file_path.endswith(".ts") or 
                file_path.endswith(".html") or file_path.endswith(".json") or file_path.endswith(".md")):
            continue
            
        try:
            # Retrieve staged content (not working tree content)
            content_res = subprocess.run(
                ["git", "show", f":{file_path}"],
                capture_output=True, text=True, check=True, errors="replace"
            )
            content = content_res.stdout
            
            matches = TOKEN_PATTERN.findall(content)
            if matches:
                print(f"\\n\\x1b[31m[COMMIT BLOCKED] Security Alert! Hardcoded GitHub Token detected in: {file_path}\\x1b[0m")
                print("\\x1b[33mAI 에이전트 및 개발자 토큰 누출 방지 정책에 의해 커밋이 강제 차단되었습니다.\\x1b[0m")
                print("\\x1b[33m코드 내부의 토큰 스트링을 제거하고 .env 환경변수 또는 config 설정을 경유하십시오.\\x1b[0m\\n")
                blocked = True
        except Exception:
            continue

    if blocked:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
"""

def install_hooks():
    git_dir = os.path.join(".", ".git")
    if not os.path.exists(git_dir):
        print("[Error] Not a git repository. Run 'git init' first.")
        return False
        
    hooks_dir = os.path.join(git_dir, "hooks")
    os.makedirs(hooks_dir, exist_ok=True)
    
    hook_path = os.path.join(hooks_dir, "pre-commit")
    
    try:
        with open(hook_path, "w", encoding="utf-8") as f:
            f.write(HOOK_CONTENT)
            
        # Give executable permissions to the hook file (important for Unix/macOS)
        try:
            st = os.stat(hook_path)
            os.chmod(hook_path, st.st_mode | stat.S_IEXEC)
        except Exception:
            pass
            
        print(f"[Success] Git pre-commit hook installed successfully at: {hook_path}")
        print("[Success] All staged commits will now be dynamically scanned to prevent GitHub Token leakages.")
        return True
    except Exception as e:
        print(f"[Error] Failed to write git hook: {e}")
        return False

if __name__ == "__main__":
    install_hooks()
