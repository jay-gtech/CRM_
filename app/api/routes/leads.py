from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.api.deps import get_current_user
from app.services import lead as lead_service
from app.schemas.lead import LeadCreate

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/leads", response_class=HTMLResponse)
async def list_leads(
    request: Request, 
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    leads = lead_service.get_leads(db)
    return templates.TemplateResponse("leads.html", {
        "request": request, 
        "leads": leads, 
        "user": user,
        "title": "Leads"
    })

@router.post("/leads")
async def create_lead(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    company: str = Form(""),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # Check duplicates
    if lead_service.get_lead_by_email(db, email):
        leads = lead_service.get_leads(db)
        return templates.TemplateResponse("leads.html", {
            "request": request, "leads": leads, "user": user, "error": "Email already exists"
        }, status_code=status.HTTP_400_BAD_REQUEST)
    
    if lead_service.get_lead_by_phone(db, phone):
        leads = lead_service.get_leads(db)
        return templates.TemplateResponse("leads.html", {
            "request": request, "leads": leads, "user": user, "error": "Phone already exists"
        }, status_code=status.HTTP_400_BAD_REQUEST)

    lead_in = LeadCreate(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        company=company,
        status="New"
    )
    lead_service.create_lead(db, lead_in)
    
    return RedirectResponse(url="/leads", status_code=status.HTTP_303_SEE_OTHER)
