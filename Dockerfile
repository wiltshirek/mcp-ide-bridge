FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY pyproject.toml ./
COPY src/ ./src/

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Create non-root user
RUN useradd --create-home --shell /bin/bash mcp
RUN chown -R mcp:mcp /app
USER mcp

# Expose port
EXPOSE 8123

# Set environment variables
ENV MCP_SERVER_HOST=0.0.0.0
ENV MCP_SERVER_PORT=8123
ENV LOG_LEVEL=INFO

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8123/health || exit 1

# Run the server
CMD ["python", "-m", "mcp_messaging.server", "--host", "0.0.0.0", "--port", "8123"] 