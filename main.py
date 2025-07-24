from fastapi import FastAPI, HTTPException, Form, Depends, Query
from invoice_reader import save_invoice_to_db, get_user_invoices
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from users import *
from models import *
from auth import *
from users import get_db
from sqlalchemy.orm import Session


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root():
    # return {"message": "Hello, FastAPI!"}
    return RedirectResponse(url="/signup-form")


@app.get("/read-invoice-by-url")
def read_invoice_by_url(url: str = Query(..., description="Direct image URL")):
    try:
        data = analyze_invoice_url(url)
        # data["file_key"] = file_key
        data["user_id"] = current_user.id
        save_invoice_to_db(data)
        return {"status": "saved", "invoice": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/upload-invoice-file")
def upload_invoice_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    try:
        file_bytes = file.file.read()
        file_key, url = upload_and_get_presigned_url(file_bytes, file.filename, file.content_type)
        print(f"Presigned s3 url: {url}")
        data = analyze_invoice_url(url)
        data["file_key"] = file_key
        data["user_id"] = current_user.id
        save_invoice_to_db(data)
        return {"status": "success", "invoice": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/my-invoices")
def my_invoices(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    invoices = get_user_invoices(current_user.id, db)
    return [invoice.__dict__ for invoice in invoices]
    

@app.post("/signup")
def signup(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    try:
        user = create_user(username, email, password)
        return {"msg": "User created", "user_id": user.id}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = validate_user_credentials(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token(data={"sub": str(user.username)})
    return {"access_token": token, "token_type": "bearer"}
@app.get("/me")
def read_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }


@app.get("/signup-form")
def signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})
@app.get("/login-form")
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
@app.get("/upload-invoice-form")
def upload_invoice_form(request: Request):
    return templates.TemplateResponse("upload_invoice.html", {"request": request})
@app.get("/my-invoices", response_class=HTMLResponse)
def my_invoices_page(
    request: Request
):
    return templates.TemplateResponse("my_invoices.html", {"request": request})
    
        
# To run the app, use the command:
# uvicorn main:app --host 0.0.0.0 --port 8000
