import os
from docx import Document

def map_path(path: str) -> str:
    if os.environ.get("AMEVA_IN_CONTAINER") == "true":
        import re
        normalized = path.replace("\\", "/")
        return re.sub(r'^[Cc]:/ameva', '/app/workspace', normalized)
    return path

def convert_md_to_docx_logic(input_md_path: str, output_docx_path: str) -> str:
    """
    순수 비즈니스 로직: 마크다운을 DOCX로 변환합니다.
    MCP 의존성이 전혀 없는 순수 파이썬 함수 (느슨한 결합)
    """
    orig_input = input_md_path
    orig_output = output_docx_path
    input_md_path = map_path(input_md_path)
    output_docx_path = map_path(output_docx_path)
    
    # Ensure parent directory for output path exists inside container
    out_dir = os.path.dirname(output_docx_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    if not os.path.exists(input_md_path):
        return f"Error: Input file does not exist at {orig_input} (mapped to {input_md_path})"

        
    try:
        doc = Document()
        with open(input_md_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('# '):
                doc.add_heading(line[2:].strip(), level=1)
            elif line.startswith('## '):
                doc.add_heading(line[3:].strip(), level=2)
            elif line.startswith('### '):
                doc.add_heading(line[4:].strip(), level=3)
            elif line.startswith('- ') or line.startswith('* '):
                doc.add_paragraph(line[2:].strip(), style='List Bullet')
            else:
                doc.add_paragraph(line)
                
        doc.save(output_docx_path)
        return f"Success: Converted {orig_input} to {orig_output}"
        
    except Exception as e:
        return f"Error during conversion: {str(e)}"
