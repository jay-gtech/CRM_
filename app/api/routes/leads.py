from fastapi import APIRouter, Request, Depends, Form, HTTPException, status, File, UploadFile
import shutil
import os
import csv
from io import StringIO
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.lead import Lead
from app.models.activity import Activity
from app.models.note import Note
from app.models.attachment import Attachment
from app.api.deps import get_current_user
from app.services import lead as lead_service
from app.schemas.lead import LeadCreate
from app.schemas.note import NoteCreate
from app.schemas.activity import ActivityCreate
from app.schemas.bulk import BulkStatusUpdate, BulkDelete

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/leads", response_class=HTMLResponse)
async def list_leads(
    request: Request, 
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    leads = lead_service.get_leads(db)
    all_users = db.query(User).all()
    return templates.TemplateResponse("leads.html", {
        "request": request, 
        "leads": leads, 
        "all_users": all_users,
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
    salutation: str = Form(None),
    secondary_email: str = Form(None),
    skype_id: str = Form(None),
    twitter: str = Form(None),
    website: str = Form(None),
    title: str = Form(None),
    source: str = Form(None),
    owner_id: int = Form(None),
    rating: int = Form(0),
    tag: str = Form(None),
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
        salutation=salutation,
        secondary_email=secondary_email,
        skype_id=skype_id,
        twitter=twitter,
        website=website,
        title=title,
        source=source,
        owner_id=owner_id,
        rating=rating,
        tag=tag,
        status="New"
    )
    lead_service.create_lead(db, lead_in)
    
    return RedirectResponse(url="/leads", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/leads/{lead_id}", response_class=HTMLResponse)
async def get_lead_detail(
    request: Request,
    lead_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    activities = db.query(Activity).filter(Activity.lead_id == lead_id).order_by(Activity.created_at.desc()).all()
    notes = db.query(Note).filter(Note.lead_id == lead_id).order_by(Note.created_at.desc()).all()
    attachments = db.query(Attachment).filter(Attachment.lead_id == lead_id).all()
    
    return templates.TemplateResponse("lead_detail.html", {
        "request": request,
        "lead": lead,
        "activities": activities,
        "notes": notes,
        "attachments": attachments,
        "user": user,
        "title": f"Lead: {lead.first_name}"
    })

@router.patch("/leads/{lead_id}/score")
async def update_lead_score(
    lead_id: int,
    body: dict,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    score = body.get("lead_score")
    if score is None or not isinstance(score, int) or score < 0 or score > 100:
        raise HTTPException(status_code=400, detail="lead_score must be an integer between 0 and 100")
    lead.lead_score = score
    db.commit()
    db.refresh(lead)
    return {"id": lead.id, "lead_score": lead.lead_score}

@router.post("/leads/{lead_id}/notes")
async def add_lead_note(
    lead_id: int,
    note: NoteCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    db_note = Note(content=note.content, lead_id=lead_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.post("/leads/{lead_id}/activities")
async def add_lead_activity(
    lead_id: int,
    activity: ActivityCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    db_activity = Activity(
        activity_type=activity.activity_type,
        subject=activity.subject,
        description=activity.description,
        status=activity.status,
        priority=activity.priority,
        due_date=activity.due_date,
        lead_id=lead_id
    )
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

@router.post("/leads/{lead_id}/attachments")
async def add_lead_attachment(
    lead_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    upload_dir = f"uploads/leads/{lead_id}"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    db_attachment = Attachment(
        filename=file.filename,
        file_path=file_path,
        file_type=file.content_type,
        lead_id=lead_id
    )
    db.add(db_attachment)
    db.commit()
    db.refresh(db_attachment)
    return db_attachment

@router.post("/leads/import")
async def import_leads(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    content = await file.read()
    # Use utf-8-sig to automatically handle Byte Order Marks (BOM) from Excel CSVs
    decoded = content.decode('utf-8-sig')
    csv_reader = csv.DictReader(StringIO(decoded))
    
    imported_count = 0
    for row in csv_reader:
        # Normalize keys to lowercase and strip whitespace
        row_data = {k.strip().lower(): v.strip() for k, v in row.items() if k and v}
        
        first_name = row_data.get('first_name')
        last_name = row_data.get('last_name')
        email = row_data.get('email')
        
        if not first_name or not last_name or not email:
            continue  # Skip rows missing mandatory fields
            
        phone = row_data.get('phone', '')
        
        # Check for duplicates to avoid IntegrityError crashing the batch
        if lead_service.get_lead_by_email(db, email) or (phone and lead_service.get_lead_by_phone(db, phone)):
            continue
            
        try:
            lead_in = LeadCreate(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                company=row_data.get('company', ''),
                status="New",
                source="Import"
            )
            lead_service.create_lead(db, lead_in)
            imported_count += 1
        except Exception as e:
            # Optionally log the error, but continue processing the rest
            print(f"Error importing row: {row_data} - {e}")
            continue
            
    return RedirectResponse(url="/leads", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/leads/bulk-status")
async def bulk_update_lead_status(
    request: BulkStatusUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    lead_service.bulk_update_status(db, request.lead_ids, request.status)
    return {"message": f"Successfully updated {len(request.lead_ids)} leads"}

@router.post("/leads/bulk-delete")
async def bulk_delete_leads(
    request: BulkDelete,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    lead_service.bulk_delete(db, request.lead_ids)
    return {"message": f"Successfully deleted {len(request.lead_ids)} leads"}
