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
