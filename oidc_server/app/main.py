from fastapi import FastAPI

from routers import oidc_admin

app = FastAPI()


app.include_router(oidc_admin.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
