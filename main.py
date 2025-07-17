from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# To run the app, use the command:
# uvicorn main:app --host 0.0.0.0 --port 8000
