import uvicorn
from fastapi import FastAPI

from src.api.routes import router

app = FastAPI(title="Discord Service Gateway")

app.include_router(router)


def main():
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
