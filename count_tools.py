import re

with open('src/server.py', 'r', encoding='utf-8') as f:
    content = f.read()

tools = re.findall(r'@mcp\.tool\(name="([^"]+)"', content)
print(f'Total tools in server.py: {len(tools)}')
for i, t in enumerate(tools, 1):
    print(f'  {i:2d}. {t}')
