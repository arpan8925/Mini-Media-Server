from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()
storage_folder = "media_storage"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, storage_folder)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
app.mount(f"/{storage_folder}", StaticFiles(directory=storage_folder), name="media")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


def get_all_images():
    all_images = []

    for category in os.listdir(UPLOAD_FOLDER):
        category_path = os.path.join(UPLOAD_FOLDER, category)            
        for img in os.listdir(category_path):
            if img.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'webp')):
                image_path = f"/{storage_folder}/{category}/{img}"  # Adjust path to be served
                all_images.append({"src": image_path, "alt": f"{img}"})

    return all_images


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Ensure the directory exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    all_images = get_all_images()

    # Get folder names
    folders = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isdir(os.path.join(UPLOAD_FOLDER, f))]

    # Render the template and pass the folder names
    return templates.TemplateResponse("index.html", {"request": request, "folders": folders, "all_images": all_images})

@app.post("/create-category/")
async def create_category(category_name: str = Form(...)):
    category_path = os.path.join(UPLOAD_FOLDER, category_name)
    if not os.path.exists(category_path):
        os.makedirs(category_path, exist_ok=True)
    return RedirectResponse(url="/", status_code=303)