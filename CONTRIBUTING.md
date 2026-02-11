# Contributing to LocalRAG

Thanks for your interest in contributing! Here's how to get started.

## Development Setup

```bash
# Fork and clone the repo
git clone https://github.com/yourusername/localrag.git
cd localrag

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dev dependencies
make dev
```

## Workflow

1. Create a branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Run tests: `make test`
4. Run linting: `make lint`
5. Submit a pull request

## Code Style

- We use [Ruff](https://github.com/astral-sh/ruff) for linting and formatting
- Type hints are required for all public functions
- Write docstrings for all modules, classes, and public methods

## Testing

- Write tests for all new features
- Tests go in `tests/unit/` or `tests/integration/`
- Run with: `make test`

## Questions?

Open an issue or reach out on [LinkedIn](https://linkedin.com/in/yourprofile).
