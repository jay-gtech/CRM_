import os
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from app.core.config import settings
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.routes import auth, leads, contacts, deals, activities, ai
from app.models.lead import Lead
from app.models.deal import Deal
from app.models.activity import Activity
from app.api.deps import get_current_user

app = FastAPI(title=settings.PROJECT_NAME)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(auth.router)
app.include_router(leads.router)
app.include_router(contacts.router)
app.include_router(deals.router)
app.include_router(activities.router)
app.include_router(ai.router)

@app.exception_handler(401)
async def custom_401_handler(request: Request, __):
    return RedirectResponse("/login")

@app.get("/")
async def read_root(
    request: Request, 
    db: Session = Depends(get_db), 
    user=Depends(get_current_user)
):
    lead_count = db.query(Lead).count()
    deal_count = db.query(Deal).count()
    task_count = db.query(Activity).count()
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "title": "Dashboard", 
        "user": user,
        "lead_count": lead_count,
        "deal_count": deal_count,
        "task_count": task_count
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
