# Agents Guide for facets-knowledge-panels

## Build/Test/Lint Commands
- **Docker setup**: `make build` (builds containers)
- **Full check**: `make all` (builds lang files, lints, and runs all checks)
- **Tests**: `make tests` or `docker compose run --rm --no-deps facets-api pytest .`
- **Single test**: `docker compose run --rm --no-deps facets-api pytest tests/test_main.py::test_function`
- **Lint**: `make lint` (runs isort + black)
- **Quality check**: `make quality` (runs flake8, isort --check, black --check)
- **Language files**: `make build_lang` (compiles .po files to .mo)

## Code Style
- **Line length**: 100 characters (configured in pyproject.toml, setup.cfg)
- **Formatting**: Use Black with isort for imports
- **Imports**: Multi-line output=3, trailing comma, parentheses (isort config)
- **Type hints**: Required for function parameters and return types (see models.py)
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Enums**: Use str, Enum pattern (see PanelName, Taxonomies in models.py)
- **FastAPI**: Use Pydantic models, type annotations, detailed docstrings
- **Async**: Use asyncer for concurrent tasks, async/await patterns

## Error Handling
- Use FastAPI HTTPException for API errors
- Include descriptive error messages and proper status codes
- Validate inputs using Pydantic models and Query parameters

## Project Structure
- **FastAPI app**: All code in `app/` directory
- **Tests**: pytest with asyncio support (pytest.ini configures async mode)
- **Docker**: All commands run via Docker containers (`facets-api` service)
- **i18n**: Multi-language support with .po/.mo files in `i18n/` directory