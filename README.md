# Django CarLog

Car trip tracking REST API built with Django 5.1 and Django REST Framework.

## Features

- Track car trips with destination, reason, and distance
- Multiple car support
- Odometer readings tracking
- REST API for all operations
- Google OAuth authentication
- Admin interface for data management

## Tech Stack

- **Python 3.12** with **Django 5.1**
- **Django REST Framework** for API
- **MySQL** database (external)
- **django-allauth** for Google OAuth
- **uv** for package management
- **ruff** for linting
- **mypy** for type checking
- **pytest** for testing
- **Playwright** for E2E tests
- **Docker** for production deployment
- **GitHub Actions** for CI/CD

## Quick Start

### Prerequisites

- Python 3.12+
- MySQL server
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/dgrant/django_carlog.git
cd django_carlog

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync --dev

# Create local settings
cp django_carlog/settings/local.py.example django_carlog/settings/local.py
# Edit local.py with your database credentials

# Run migrations
uv run python manage.py migrate --settings=django_carlog.settings.local

# Create a superuser
uv run python manage.py createsuperuser --settings=django_carlog.settings.local

# Run the development server
uv run python manage.py runserver --settings=django_carlog.settings.local
```

### Running Tests

```bash
# Run unit tests
uv run pytest trips/tests/

# Run with coverage
uv run pytest trips/tests/ --cov=trips --cov-report=html

# Run E2E tests (requires Playwright browsers)
uv run playwright install chromium
uv run pytest e2e/ --browser chromium
```

### Linting & Type Checking

```bash
# Run ruff linter
uv run ruff check .

# Run ruff formatter
uv run ruff format .

# Run mypy type checking
uv run mypy trips/ django_carlog/

# Run pre-commit hooks
uv run pre-commit run --all-files
```

## Docker (Production)

```bash
# Build the Docker image
docker build -t django-carlog .

# Run with docker-compose
docker-compose up -d
```

### Environment Variables

Create a `.env.production` file with:

```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DB_HOST=your-mysql-host
DB_PORT=3306
DB_NAME=carlog
DB_USER=carlog_user
DB_PASSWORD=your-password
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

## Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs:
   - `http://localhost:8000/accounts/google/login/callback/` (development)
   - `https://your-domain.com/accounts/google/login/callback/` (production)
6. Add credentials to Django admin under "Social applications"

## CI/CD

GitHub Actions pipeline includes:
- **Lint**: ruff and mypy checks
- **Test**: Unit tests with coverage
- **E2E**: Playwright browser tests
- **Docker Build**: Verify Docker image builds
- **Deploy**: Auto-deploy to Linode on main branch

### Required GitHub Secrets for Deployment

- `LINODE_HOST`: Your Linode server IP/hostname
- `LINODE_USERNAME`: SSH username
- `LINODE_SSH_KEY`: SSH private key
- `LINODE_SSH_PORT`: SSH port (usually 22)
- `LINODE_APP_PATH`: Path to app on server

## API Endpoints

- `GET /trips/api/` - API root
- `GET /trips/api/cars/` - List cars
- `GET /trips/api/trips/` - List trips
- `GET /trips/api/odometers/` - List odometer readings
- `GET /admin/` - Django admin interface

## Future Features

- [ ] Quick "Hospital Trip" button for easy logging
- [ ] Pre-saved frequent destinations
- [ ] Mobile-friendly interface
- [ ] Trip statistics and reporting

## License

MIT
