from fastapi import FastAPI
app = FastAPI(title="Chat Application Backend")
@app.get("/ping")
async def ping():
    return {"message":"Server is running"} 