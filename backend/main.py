
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from fastapi import FastAPI
import uvicorn
from agent import make_activities, make_restaurants, make_events, summarize_itinerary, make_fe
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
    destination: str = Form(...),
    date_range: str = Form(...),
    vibe: str = Form(...),
    travel_with: str = Form(...),
    comments: str = Form(...)
):
    # Process the form data as needed
    events = []
    restaurants = []
    activities = []
    
    activities = make_activities(destination, date_range, comments)
    # restaurants = make_restaurants(destination, daterange, comments)
    events = make_events(destination, date_range, comments)
    # result = f"""
    # here are my suggestions for {daterange} in {destination}, considering your comments: {comments}
    # events {events}
    # restaurants {restaurants}
    # activities {activities}
    # """
    result = summarize_itinerary(destination, date_range, comments, activities, restaurants, events)
    
    # result = make_fe(destination, daterange, comments, activities, restaurants, events)
    return result

# if __name__ == "__main__":
#     uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)
