from fastapi import FastAPI
from routes.rooms import router as rooms_router

app = FastAPI(title="Secret Chat Backend")

app.include_router(rooms_router)

@app.get("/ping")
def ping():
    return {"message": "Server is running 🚀"}
