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
