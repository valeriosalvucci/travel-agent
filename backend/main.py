from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

# Define the path to the directory containing index.html
base_path = Path(__file__).resolve().parent.parent
index_file = base_path / "index.html"

# Serve the index.html at the root URL
@app.get("/")
async def serve_index():
    return FileResponse(index_file)

# Mount the static directory for other static assets
static_dir = base_path / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

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
    Here are my suggestions for {daterange} in {destination}, considering your comments: {comments}
    Places: {places}
    Restaurants: {restaurants}
    Activities: {activities}
    """
    return result
