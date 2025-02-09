from fastapi import FastAPI, Form
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
    destination: str = Form(...),
    date_range: str = Form(...),
    vibe: str = Form(...),
    travel_with: str = Form(...),
    comments: str = Form(...)
):
    # Process the form data as needed
    result = f"""
    Here are my suggestions for {date_range} in {destination}, considering your preferences:
    - Vibe: {vibe}
    - Traveling with: {travel_with}
    - Additional comments: {comments}
    """
    return {"message": result}
