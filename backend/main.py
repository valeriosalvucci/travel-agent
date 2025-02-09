from fastapi import FastAPI
import uvicorn
from agent import make_activities
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}

@app.post("/upload")
async def upload(
    destination: str = "Tokyo", daterange: str = "2025-02-15 - 2025-02-20", comments: str = "I love art and ramen"
):
    places = []
    restaurants = []
    activities = []
    
    # activities = make_activities(destination, daterange, comments)
    result = f"""
    here are my suggestions for {daterange} in {destination}, considering your comments: {comments}
    places {places}
    restaurants {restaurants}
    activities {activities}
    """
    return result

# if __name__ == "__main__":
#     uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)
