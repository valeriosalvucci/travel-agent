from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import uvicorn
from agent import make_activities
app = FastAPI()

# Define the path to the directory containing index.html
static_dir = Path(__file__).parent.parent / "index.html"

# Mount the static directory
app.mount("/", StaticFiles(directory=static_dir.parent, html=True), name="static")

# @app.get("/")
# async def root():
#     # use static file html
#     return {"message": "Hello World"}
#     # return {"message": "Hello World"}

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
