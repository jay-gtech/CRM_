from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_db
from app.models.user import User
from app.api.deps import get_current_user
from app.services import activity as activity_service
from app.services import lead as lead_service
from app.services import contact as contact_service
from app.schemas.activity import ActivityCreate

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/activities", response_class=HTMLResponse)
async def list_activities(
    request: Request, 
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    activities = activity_service.get_activities(db)
    # We can also fetch leads/contacts for the dropdowns
    leads = lead_service.get_leads(db)
    contacts = contact_service.get_contacts(db)
    return templates.TemplateResponse("activities.html", {
        "request": request, 
        "activities": activities, 
        "leads": leads,
        "contacts": contacts,
        "user": user, 
        "title": "Activities"
    })

@router.post("/activities")
async def create_activity(
    request: Request,
    activity_type: str = Form(...),
    description: str = Form(...),
    lead_id: Optional[int] = Form(None),
    contact_id: Optional[int] = Form(None),
    deal_id: Optional[int] = Form(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # If empty string is sent, convert to None
    if lead_id == "": lead_id = None
    if contact_id == "": contact_id = None
    if deal_id == "": deal_id = None
    
    activity_in = ActivityCreate(
        activity_type=activity_type,
        description=description,
        lead_id=lead_id,
        contact_id=contact_id,
        deal_id=deal_id
    )
    activity_service.create_activity(db, activity_in)
    return RedirectResponse(url="/activities", status_code=status.HTTP_303_SEE_OTHER)
