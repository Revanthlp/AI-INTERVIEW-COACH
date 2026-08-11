from fastapi import FastAPI

app = FastAPI(title="AI Interview Coach")


@app.get("/")
def home():
    return {
        "message": "AI Interview Coach API is running!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }