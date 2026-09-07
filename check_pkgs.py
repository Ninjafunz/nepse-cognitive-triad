import sys

for pkg in ["fastapi", "uvicorn", "pydantic", "pydantic_settings", "sqlalchemy"]:
    try:
        __import__(pkg)
        print(f"{pkg}: INSTALLED")
    except ImportError:
        print(f"{pkg}: NOT INSTALLED")
