from fastapi import FastAPI

from routers import oicd_admin

app = FastAPI()


app.include_router(oicd_admin.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
