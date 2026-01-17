# GitHub Copilot Instructions for django_carlog

## Project Overview

This is a Django REST API for car trip tracking (carlog2). It allows tracking car trips, odometer readings, and car information through a RESTful API.

**Tech Stack:**
- Django 3.0.10
- Django REST Framework 3.11.1
- MySQL database (via mysqlclient)
- Python 3.6+
- Additional: django-extensions, django-filter, django-model-utils

## Project Structure

```
django_carlog/
├── django_carlog/          # Main Django project settings
│   ├── settings/           # Settings split by environment (base, local, test)
│   ├── urls.py             # Root URL configuration
│   └── wsgi.py             # WSGI configuration
├── trips/                  # Main app for trip tracking
│   ├── models.py           # Models: Car, Trip, Odometer
│   ├── serializers.py      # DRF serializers
│   ├── views.py            # API views
│   ├── urls.py             # App URL configuration
│   └── migrations/         # Database migrations
├── static/                 # Static files
├── manage.py               # Django management script
└── requirements.txt        # Python dependencies
```

## Common Commands

### Development Setup
```bash
# Create virtual environment
./createVirtualEnv.sh

# Set local environment
source ./setlocal.sh

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Run development server
python manage.py runserver
```

### Linting & Code Quality
```bash
# Run pre-commit hooks on all files
pre-commit run --all-files

# Black formatter (automatically formats code)
black .

# isort (automatically sorts imports)
isort . --multi-line 3 --trailing-comma

# Prospector (static analysis - pylint, pyflakes, mccabe, etc.)
prospector -X
```

### Database Operations
```bash
# Backup local database
./backupLocalDB.sh

# Copy to remote database
./copyToRemoteDb.sh

# Load remote database
./loadRemoteDb.sh

# Drop all tables
./dropAllTables.sh

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Deployment
```bash
# Set production environment
source ./setproduction.sh

# Deploy using Fabric
fab update          # Pull latest code
fab schema          # Run migrations
fab restart         # Restart uWSGI
fab backupdb        # Backup database
```

## Testing Practices

- Test files should be named with `test_` prefix or `_test.py` suffix (enforced by pre-commit hook)
- Django test settings are in `django_carlog/settings/test.py`
- Run tests with: `python manage.py test`
- Keep tests focused on model behavior, serializers, and API endpoints

## Code Style

This project enforces strict code quality standards:

### Formatting
- **Black**: Code formatter with default configuration (line length 88)
- **isort**: Import sorting with settings: `--multi-line 3 --trailing-comma`
- Configuration in `.isort.cfg`

### Linting
- **Prospector**: Comprehensive static analysis tool that includes:
  - pylint
  - pyflakes
  - mccabe (complexity checker)
  - pep8/pycodestyle
  - And more
- Excluded paths: `docs/conf.py`, `trips/migrations/`, `fabfile.py`
- Run with `-X` flag to show extra information

### Pre-commit Hooks
All commits must pass pre-commit hooks (`.pre-commit-config.yaml`):
- Black formatting
- isort import sorting
- File checks (large files, executables, JSON, YAML, merge conflicts)
- Trailing whitespace removal
- End-of-file fixer
- Debug statement detection
- Prospector linting
- pyupgrade (Python 3.6+ syntax)

### Python Style Conventions
- Use f-strings for string formatting (enforced by pyupgrade)
- Python 3.6+ syntax
- Follow PEP 8 conventions
- Use model_utils.models.TimeStampedModel for models with timestamps
- Models should have `__str__()` methods
- Models should define `Meta.ordering`

### Django Conventions
- Use `models.CASCADE` for foreign key deletions
- Use `models.CharField` with `max_length` for strings
- Use `models.DecimalField` with `max_digits` and `decimal_places` for decimal values
- Date fields should use `models.DateField()`
- Settings are split by environment (base, local, test, production)

## Git Workflow

1. All commits must pass pre-commit hooks
2. Pre-commit hooks run automatically before each commit
3. To run hooks manually: `pre-commit run --all-files`
4. Commits should have clear, descriptive messages
5. The project uses rebase workflow (see `git pull --rebase` in scripts)

## Boundaries and Constraints

### DO NOT modify:
- **Settings files**: `django_carlog/settings/*.py` (unless explicitly required)
  - Settings are environment-specific and carefully configured
  - Changes could break local/test/production environments
- **Migration files**: `trips/migrations/*.py` (unless creating new migrations)
  - Never edit existing migrations
  - Always use `python manage.py makemigrations` to create new ones
- **Deployment scripts**: Shell scripts in root directory
  - These are environment-specific and carefully tuned
- **`fabfile.py`**: Deployment automation (excluded from linting)

### DO NOT commit:
- Local settings: `django_carlog/settings/local.py` (use `local.py.example` as template)
- Virtual environment: `env/` or `venv/`
- Database files: `*.db`, `*.sqlite3`
- Secrets or credentials
- `__pycache__/`, `*.pyc` files
- IDE-specific files

### Always ensure:
- All code is formatted with Black before committing
- Imports are sorted with isort
- No linting errors from Prospector
- Tests pass (if test infrastructure exists)
- Database migrations are created for model changes
- Changes follow Django best practices

## Security Considerations

- Never commit database credentials
- Use environment variables for sensitive configuration
- Follow Django security best practices
- Keep dependencies up to date (see `upgradeDependencies.sh`)
- Be careful with SQL queries (use Django ORM when possible)

## REST API Structure

- API endpoints are defined in `trips/urls.py`
- Views use Django REST Framework
- Serializers are in `trips/serializers.py`
- Models: Car, Trip, Odometer
- Use django-filter for API filtering capabilities

## Additional Notes

- The project uses django-debug-toolbar for development debugging
- MySQL is the database backend (not SQLite)
- The project appears to have a React frontend component (react-cms with TypeScript/TSLint/ESLint)
- Uses django-extensions for enhanced management commands
