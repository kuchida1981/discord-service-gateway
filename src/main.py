"""Discord Service Gateway application entry point."""

import asyncio
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.api.routes import router
from src.cli.register_commands import register_commands

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
    """Run startup tasks."""
    try:
        await asyncio.to_thread(register_commands)
    except Exception:
        logger.exception("Failed to register Discord commands; continuing startup")
    yield


app = FastAPI(title="Discord Service Gateway", lifespan=lifespan)

app.include_router(router)


def main() -> None:  # pragma: no cover
    """Start the uvicorn ASGI server."""
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":  # pragma: no cover
    main()
