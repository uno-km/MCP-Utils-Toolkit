import os
import subprocess
import logging

logger = logging.getLogger(__name__)

AMEVA_IN_CONTAINER = os.environ.get("AMEVA_IN_CONTAINER") == "true"
BASE_DIR = "/app/workspace" if AMEVA_IN_CONTAINER else r"C:\ameva"


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
    # Try to fetch original remote URL to inject token if present
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
            push_result = run_git_command(repo_name, ["push", auth_url])
        else:
            push_result = run_git_command(repo_name, ["push"])
    except Exception:
        push_result = run_git_command(repo_name, ["push"])
        
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
            # Clean url from error message if it has a token
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
