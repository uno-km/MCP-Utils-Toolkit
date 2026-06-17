import os
from docx import Document

def convert_md_to_docx_logic(input_md_path: str, output_docx_path: str) -> str:
    """
    순수 비즈니스 로직: 마크다운을 DOCX로 변환합니다.
    MCP 의존성이 전혀 없는 순수 파이썬 함수 (느슨한 결합)
    """
    if not os.path.exists(input_md_path):
        return f"Error: Input file does not exist at {input_md_path}"
        
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
        return f"Success: Converted {input_md_path} to {output_docx_path}"
        
    except Exception as e:
        return f"Error during conversion: {str(e)}"
