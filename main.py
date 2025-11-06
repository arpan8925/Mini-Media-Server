from fastapi import FastAPI, Form, Request, File, UploadFile, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import os

app = FastAPI()
storage_folder = "media_storage"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, storage_folder)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
app.mount(f"/{storage_folder}", StaticFiles(directory=storage_folder), name="media")
app.mount("/logo", StaticFiles(directory=os.path.join(BASE_DIR, "logo")), name="logo")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


# ----------------------
# Environment and Session
# ----------------------

def load_env_file(env_path: str) -> None:
    """Lightweight .env loader (KEY=VALUE lines, ignores # comments)."""
    if not os.path.isfile(env_path):
        return
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                # don't override existing env vars
                os.environ.setdefault(key, value)
    except Exception:
        # fail quietly; app can still read real env vars
        pass


# Attempt to load a local .env sitting next to main.py
load_env_file(os.path.join(BASE_DIR, ".env"))

SESSION_SECRET = os.environ.get("SESSION_SECRET", "change-this-in-production")
AUTH_USERNAME = os.environ.get("AUTH_USERNAME", "admin")
AUTH_PASSWORD = os.environ.get("AUTH_PASSWORD", "password")

# Add session middleware for simple cookie-based auth
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)


def get_all_images():
    all_images = []

    for category in os.listdir(UPLOAD_FOLDER):
        category_path = os.path.join(UPLOAD_FOLDER, category)            
        for img in os.listdir(category_path):
            if img.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'webp')):
                image_path = f"/{storage_folder}/{category}/{img}"  # Adjust path to be served
                all_images.append({"src": image_path, "alt": f"{img}"})

    return all_images


def require_auth(request: Request):
    """Simple guard to ensure a session user exists."""
    user = request.session.get("user") if hasattr(request, "session") else None
    if not user:
        # Redirect to login preserving next URL using HTTPException with Location header
        next_url = request.url.path
        raise HTTPException(status_code=303, headers={"Location": f"/login?next={next_url}"})
    return user


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, user: str = Depends(require_auth)):
    # Ensure the directory exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    all_images = get_all_images()

    # Get folder names
    folders = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isdir(os.path.join(UPLOAD_FOLDER, f))]

    # Render the template and pass the folder names
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "folders": folders, "all_images": all_images},
    )

@app.post("/create-category/")
async def create_category(request: Request, category_name: str = Form(...), user: str = Depends(require_auth)):
    category_path = os.path.join(UPLOAD_FOLDER, category_name)
    if not os.path.exists(category_path):
        os.makedirs(category_path, exist_ok=True)
    return RedirectResponse(url="/", status_code=303)

@app.get("/get_images/{folder}")
async def get_images(request: Request, folder: str, user: str = Depends(require_auth)):
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
async def upload_file(request: Request, file: UploadFile = File(...), category: str = Form(...), user: str = Depends(require_auth)):
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


# ----------------------
# Auth Endpoints
# ----------------------

@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    # If already logged in, go home
    if request.session.get("user"):
        return RedirectResponse(url="/", status_code=303)
    next_url = request.query_params.get("next", "/")
    return templates.TemplateResponse("login.html", {"request": request, "next": next_url})


@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...), next: str = Form("/")):
    if username == AUTH_USERNAME and password == AUTH_PASSWORD:
        request.session["user"] = username
        # Redirect to the page the user originally wanted
        return RedirectResponse(url=next or "/", status_code=303)
    # Invalid credentials
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": "Invalid username or password", "next": next},
        status_code=401,
    )


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)