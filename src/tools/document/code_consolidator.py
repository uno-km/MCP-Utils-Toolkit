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
            md_lines.append(f"- **Relative Path**: `{rel_path}`\n")
            md_lines.append(f"- **Full Path**: `{file}`\n\n")
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
