FROM python:3.11-slim

# Install system dependencies (Git)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Fix Git dubious ownership warning for mounted directories
RUN git config --global --add safe.directory '*'

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Run the MCP server
CMD ["python", "src/server.py"]
