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
