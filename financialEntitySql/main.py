from fastapi import FastAPI
import routesAccounts, routesTransactions

app = FastAPI()

app.include_router(routesAccounts.router, prefix="/accounts", tags=["accounts"])
app.include_router(routesTransactions.router, prefix="/transactions", tags=["transactions"])

