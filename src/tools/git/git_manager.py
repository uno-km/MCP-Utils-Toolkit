import os
import subprocess
import logging

logger = logging.getLogger(__name__)

BASE_DIR = r"C:\ameva"

def _get_safe_path(repo_name: str) -> str:
    """Validate and return safe absolute path for the repository."""
    # Ensure no directory traversal
    safe_name = os.path.basename(repo_name)
    path = os.path.join(BASE_DIR, safe_name)
    if not os.path.exists(path):
        raise ValueError(f"Repository {safe_name} does not exist at {path}")
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
            check=False
        )
        
        output = result.stdout.strip()
        if result.returncode != 0:
            error_output = result.stderr.strip()
            return f"Git Command Error ({result.returncode}):\nStdout: {output}\nStderr: {error_output}"
        
        return output if output else "Command executed successfully with no output."
    except Exception as e:
        return f"Error executing git command: {str(e)}"

def git_status(repo_name: str) -> str:
    """Get the git status of a repository."""
    return run_git_command(repo_name, ["status"])

def git_pull(repo_name: str) -> str:
    """Pull the latest changes from origin."""
    return run_git_command(repo_name, ["pull"])

def git_commit_and_push(repo_name: str, message: str) -> str:
    """Stage all changes, commit, and push."""
    # Add all
    add_result = run_git_command(repo_name, ["add", "."])
    if "Error" in add_result:
        return f"Failed during git add:\n{add_result}"
        
    # Commit
    commit_result = run_git_command(repo_name, ["commit", "-m", message])
    # Note: git commit returns non-zero if there's nothing to commit.
    if "Error" in commit_result and "nothing to commit" not in commit_result:
        return f"Failed during git commit:\n{commit_result}"
        
    if "nothing to commit" in commit_result or "nothing to commit" in run_git_command(repo_name, ["status"]):
        # If nothing to commit, we might still need to push if there are unpushed commits, 
        # but typically it's clean. Let's just try pushing anyway.
        pass
        
    # Push
    push_result = run_git_command(repo_name, ["push"])
    if "Error" in push_result:
        return f"Failed during git push:\n{push_result}"
        
    return f"Successfully added, committed, and pushed.\nCommit Info:\n{commit_result}\nPush Info:\n{push_result}"
