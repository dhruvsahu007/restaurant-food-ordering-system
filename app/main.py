from fastapi import FastAPI
from app.api.endpoints.menu import router as menu_router
from app.api.endpoints.orders import router as orders_router

app = FastAPI(
    title="Restaurant Ordering System",
    description="API for managing restaurant menu and orders",
    version="1.0.0"
)

app.include_router(menu_router, prefix="/menu", tags=["menu"])
app.include_router(orders_router, tags=["orders"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Restaurant Ordering System API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)