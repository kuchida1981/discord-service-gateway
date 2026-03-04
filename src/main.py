"""Discord Service Gateway application entry point."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from scripts.register_commands import register_commands
from src.api.routes import router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Run startup tasks."""
    register_commands()
    yield


app = FastAPI(title="Discord Service Gateway", lifespan=lifespan)

app.include_router(router)


def main() -> None:  # pragma: no cover
    """Start the uvicorn ASGI server."""
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)  # noqa: S104


if __name__ == "__main__":  # pragma: no cover
    main()
