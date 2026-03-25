import asyncio
from httpx import AsyncClient
from app.main import app
from app.db.session import SessionLocal
from app.models.user import User

def run_test():
    # 1. Get a test user token
    db = SessionLocal()
    user = db.query(User).first()
    db.close()
    
    if not user:
        print("No users in DB")
        return
        
    print(f"Testing with user: {user.email}")
    
    from app.models.lead import Lead
    import requests
    
    db = SessionLocal()
    count_before = db.query(Lead).count()
    print(f"Leads before: {count_before}")
    
    # 2. Upload file
    with open("sample_leads_import.csv", "rb") as f:
        response = client.post(
            "/leads/import", 
            files={"file": ("sample_leads_import.csv", f, "text/csv")},
            follow_redirects=False
        )
        
    count_after = db.query(Lead).count()
    print(f"Leads after: {count_after}")
    db.close()
        
    print("Status code:", response.status_code)
    print("Headers:", response.headers)

if __name__ == "__main__":
    run_test()
