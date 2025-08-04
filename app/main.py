from fastapi import FastAPI
from app.api.endpoints.menu import router as menu_router

app = FastAPI()

app.include_router(menu_router, prefix="/menu", tags=["menu"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Restaurant Food Ordering System API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)