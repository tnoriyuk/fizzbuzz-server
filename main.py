from fastapi import FastAPI

from routers import settingfiles

app = FastAPI()

app.include_router(settingfiles.router)


@app.route("/")
def index() -> str:
    return "running"
