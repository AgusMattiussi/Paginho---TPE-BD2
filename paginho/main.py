from fastapi import FastAPI
import routesUsers, routesLinkedAccounts

app = FastAPI()

app.include_router(routesUsers.router, prefix="/users", tags=["users"])
app.include_router(routesLinkedAccounts.router, prefix="/linkedAccounts", tags=["linkedAccounts"])

@app.get("/")
async def root():
    return {"message": "Hello World"}