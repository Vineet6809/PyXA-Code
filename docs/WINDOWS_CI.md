# Windows CI Instructions

This project includes Windows-only integration tests marked with `windows_integration`.

## Local Windows run

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements-mvp.txt
python -m pytest -q
python -m pytest -q -m windows_integration
```

## GitHub Actions

A Windows workflow is provided in `.github/workflows/windows-tests.yml`.
It runs both standard tests and Windows integration tests.
