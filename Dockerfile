FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies for mysqlclient and uv
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install Python dependencies with uv
RUN uv sync --frozen --no-dev

# Copy project
COPY . .

# Expose port (Render uses $PORT env var)
EXPOSE 8000

# Default command - can be overridden by Render
CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "django_carlog.wsgi:application"]
