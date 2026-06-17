from mcp.server.fastmcp import FastMCP
from tools.document.md_converter import convert_md_to_docx_logic
from tools.git import git_manager

def create_server() -> FastMCP:
    """
    서버 초기화 및 도구 등록을 담당하는 진입점.
    비즈니스 로직은 src/tools 하위의 모듈에서 가져와 연결만 합니다.
    """
    mcp = FastMCP("AMEVA_Toolkit_Utils")

    @mcp.tool(name="convert_md_to_docx", description="Convert Markdown file to Word DOCX format")
    def tool_md_to_docx(input_md_path: str, output_docx_path: str) -> str:
        return convert_md_to_docx_logic(input_md_path, output_docx_path)
        
    @mcp.tool(name="git_status", description="Get the git status of a repository (e.g., AMEVA-Doc-AI)")
    def tool_git_status(repo_name: str) -> str:
        return git_manager.git_status(repo_name)

    @mcp.tool(name="git_pull", description="Pull the latest changes for a repository (e.g., AMEVA-Window-Assistant)")
    def tool_git_pull(repo_name: str) -> str:
        return git_manager.git_pull(repo_name)

    @mcp.tool(name="git_commit_and_push", description="Stage all changes, commit with a message, and push for a repository")
    def tool_git_commit_and_push(repo_name: str, commit_message: str) -> str:
        return git_manager.git_commit_and_push(repo_name, commit_message)

    return mcp

if __name__ == "__main__":
    server = create_server()
    server.run()
