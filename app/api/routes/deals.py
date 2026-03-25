from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.api.deps import get_current_user
from app.services import deal as deal_service
from app.schemas.deal import DealCreate, DealUpdate

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/deals", response_class=HTMLResponse)
async def list_deals(
    request: Request, 
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    deals = deal_service.get_deals(db)
    # Organize deals by stage for Pipeline view
    pipeline = {
        "New": [],
        "Contacted": [],
        "Qualified": [],
        "Negotiation": [],
        "Won": [],
        "Lost": []
    }
    for deal in deals:
        if deal.stage in pipeline:
            pipeline[deal.stage].append(deal)
        else:
            pipeline["New"].append(deal) # Fallback

    return templates.TemplateResponse("deals.html", {
        "request": request, "pipeline": pipeline, "user": user, "title": "Pipeline"
    })

@router.post("/deals")
async def create_deal(
    request: Request,
    name: str = Form(...),
    amount: float = Form(...),
    contact_id: int = Form(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    deal_in = DealCreate(
        name=name,
        amount=amount,
        contact_id=contact_id,
        stage="New"
    )
    deal_service.create_deal(db, deal_in)
    return RedirectResponse(url="/deals", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/deals/move/{deal_id}")
async def move_deal(
    deal_id: int,
    stage: str = Form(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    deal_service.update_deal(db, deal_id, DealUpdate(stage=stage))
    return RedirectResponse(url="/deals", status_code=status.HTTP_303_SEE_OTHER)
