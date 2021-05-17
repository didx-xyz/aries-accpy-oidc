from fastapi import FastAPI

from routers import oidc_admin
from database import init_db

app = FastAPI()


app.include_router(oidc_admin.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


init_db()