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

# Collect static files at build time (uses base settings with default SECRET_KEY)
RUN uv run python manage.py collectstatic --noinput --settings=django_carlog.settings.base

# Expose port (Render uses $PORT env var)
EXPOSE 8000

# Default command - run migrations then start gunicorn
# Uses $PORT env var (Render sets this), defaults to 8000
CMD ["sh", "-c", "uv run python manage.py migrate && uv run gunicorn --bind 0.0.0.0:${PORT:-8000} django_carlog.wsgi:application"]
