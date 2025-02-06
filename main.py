from fastapi import FastAPI, Form, Request, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
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

@app.get("/get_images/{folder}")
async def get_images(folder: str):
    """Retrieve images for a specific category"""
    category_path = os.path.join(UPLOAD_FOLDER, folder)

    if not os.path.exists(category_path) or not os.path.isdir(category_path):
        return JSONResponse(content={"error": "Category not found"}, status_code=404)

    images = [
        {"src": f"/{storage_folder}/{folder}/{img}", "alt": img}
        for img in os.listdir(category_path) if img.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'webp'))
    ]

    return JSONResponse(content={"images": images})


@app.post("/upload")
async def upload_file(file: UploadFile = File(...), category: str = Form(...)):
    # Validate category selection
    if not category:
        return JSONResponse(
            content={"error": "Please select a category"},
            status_code=400
        )
    
    # Check if category directory exists
    category_path = os.path.join(UPLOAD_FOLDER, category)
    if not os.path.isdir(category_path):
        return JSONResponse(
            content={"error": "Category does not exist"},
            status_code=400
        )
    
    # Save the file
    file_path = os.path.join(category_path, file.filename)
    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        return JSONResponse(
            content={"error": f"Failed to save file: {str(e)}"},
            status_code=500
        )
    
    return RedirectResponse(url="/", status_code=303)