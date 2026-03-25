from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.lead import Lead
from app.api.deps import get_current_user
from app.services import contact as contact_service
from app.services import lead as lead_service
from app.schemas.contact import ContactCreate

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/contacts", response_class=HTMLResponse)
async def list_contacts(
    request: Request, 
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    contacts = contact_service.get_contacts(db)
    return templates.TemplateResponse("contacts.html", {
        "request": request, "contacts": contacts, "user": user, "title": "Contacts"
    })

@router.post("/contacts")
async def create_contact(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(""),
    company: str = Form(""),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    contact_in = ContactCreate(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        company=company
    )
    contact_service.create_contact(db, contact_in)
    return RedirectResponse(url="/contacts", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/contacts/convert/{lead_id}")
async def convert_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    lead = lead_service.get_lead(db, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
        
    # Create contact
    contact_in = ContactCreate(
        first_name=lead.first_name,
        last_name=lead.last_name,
        email=lead.email,
        phone=lead.phone,
        company=lead.company,
        lead_id=lead.id
    )
    contact_service.create_contact(db, contact_in)
    
    # Update lead status
    lead.status = "Qualified"
    db.commit()
    
    return RedirectResponse(url="/contacts", status_code=status.HTTP_303_SEE_OTHER)
