from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
import uuid
from fastapi import Request

from database.db import SessionLocal
from models.qr_models import QREvent, QRScan
from utils.timezone import ist_to_utc, get_current_utc
from utils.qr import generate_qr
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Form
templates = Jinja2Templates(directory="templates")
from fastapi import Depends
from utils.role_checker import require_roles


# 👉 import your RBAC dependency (adjust based on your project)
# from app.dependencies import get_current_user

router = APIRouter(prefix="/qr", tags=["QR"])


@router.get("/create-pageeee", response_class=HTMLResponse)
def create_qr_page(request: Request):
    return templates.TemplateResponse("qr_form.html", {"request": request})

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create")
def create_qr(
    request: Request,
    name: str,
    date: str,
    start_time: str,
    end_time: str,
    db: Session = Depends(get_db),
    current_user = Depends(require_roles(["admin"]))   # ✅ RBAC

):
    token = str(uuid.uuid4())

    start_utc = ist_to_utc(date, start_time)
    end_utc = ist_to_utc(date, end_time)

    qr_event = QREvent(
        name=name,
        token=token,
        start_time_utc=start_utc,
        end_time_utc=end_utc,
        created_by = current_user["user_id"]
    )

    db.add(qr_event)
    db.commit()
    db.refresh(qr_event)

    # ✅ Dynamic base URL (VERY IMPORTANT)
    base_url = str(request.base_url).rstrip("/")

    # ✅ Generate QR with URL
    qr_path = generate_qr(base_url, token)

    return {
        "message": "QR created",
        "token": token,
        "scan_url": f"{base_url}/qr/scan?token={token}",
        "qr_image": f"{base_url}/{qr_path}"
    }

# ✅ SCAN QR
@router.get("/scan", response_class=HTMLResponse)
def scan_qr(token: str, request: Request, db: Session = Depends(get_db)):

    qr = db.query(QREvent).filter(QREvent.token == token).first()

    if not qr:
        return "<h2>Invalid QR</h2>"

    now = get_current_utc()

    if not (qr.start_time_utc <= now <= qr.end_time_utc):
        return "<h2>QR expired or not active</h2>"

    # ✅ SHOW FORM INSTEAD OF SAVING
    return f"""
    <html>
        <body style="text-align:center;font-family:sans-serif;margin-top:50px;">
            <h2>Enter Your Name</h2>
            <form action="/qr/submit-scan" method="post">
                <input type="hidden" name="token" value="{token}" />
                <input type="text" name="user_name" placeholder="Your Name" required />
                <br><br>
                <button type="submit">Submit</button>
            </form>
        </body>
    </html>
    """

@router.post("/submit-scan", response_class=HTMLResponse)
def submit_scan(
    token: str = Form(...),
    user_name: str = Form(...),
    request: Request = None,
    db: Session = Depends(get_db)
):
    qr = db.query(QREvent).filter(QREvent.token == token).first()

    if not qr:
        return "<h2>Invalid QR</h2>"

    now = get_current_utc()

    if not (qr.start_time_utc <= now <= qr.end_time_utc):
        return "<h2>QR expired or not active</h2>"

    # ✅ NOW SAVE DATA HERE
    scan = QRScan(
        qr_id=qr.id,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        user_name=user_name   # 👈 NEW FIELD
    )

    db.add(scan)
    db.commit()

    return f"<h2>✅ Thank you {user_name}, Scan Successful</h2>"