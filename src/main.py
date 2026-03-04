"""Discord Service Gateway application entry point."""

import uvicorn
from fastapi import FastAPI

from src.api.routes import router

app = FastAPI(title="Discord Service Gateway")

app.include_router(router)


def main() -> None:  # pragma: no cover
    """Start the uvicorn ASGI server."""
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)  # noqa: S104


if __name__ == "__main__":  # pragma: no cover
    main()