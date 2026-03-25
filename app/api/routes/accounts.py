from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.account import Account
from app.schemas.account import AccountCreate, AccountUpdate, AccountResponse

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/accounts", response_class=HTMLResponse)
async def list_accounts(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    accounts = db.query(Account).all()
    return templates.TemplateResponse("accounts.html", {
        "request": request,
        "accounts": accounts,
        "user": user,
        "title": "Accounts"
    })

@router.post("/accounts")
async def create_account(
    name: str = Form(...),
    website: str = Form(None),
    industry: str = Form(None),
    description: str = Form(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    db_account = Account(
        name=name,
        website=website,
        industry=industry,
        description=description
    )
    db.add(db_account)
    db.commit()
    return RedirectResponse(url="/accounts", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/accounts/{account_id}", response_class=HTMLResponse)
async def get_account(
    request: Request,
    account_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return templates.TemplateResponse("account_detail.html", {
        "request": request,
        "account": account,
        "user": user,
        "title": f"Account: {account.name}"
    })
