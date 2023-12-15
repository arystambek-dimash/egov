from fastapi import FastAPI

import app.router as router

app = FastAPI()


@app.get("/")
async def home():
    return "Welcome Home"


app.include_router(router.router)
