from fastapi import FastAPI
import routesUsers

app = FastAPI()

app.include_router(routesUsers.router, prefix="/users", tags=["users"])

@app.get("/")
async def root():
    return {"message": "Hello World"}