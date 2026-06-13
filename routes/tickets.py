from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models import TicketCreate, TicketUpdate
from database import get_db
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def generate_ticket_id(count: int) -> str:
    return f"TKT-{str(count).zfill(3)}"

# ─── API ROUTES ───────────────────────────────────────────

@router.post("/api/tickets")
async def create_ticket(ticket: TicketCreate):
    db = await get_db()
    try:
        cursor = await db.execute("SELECT COUNT(*) FROM tickets")
        row = await cursor.fetchone()
        count = row[0] + 1
        ticket_id = generate_ticket_id(count)
        now = datetime.utcnow().isoformat()
        await db.execute("""
            INSERT INTO tickets (ticket_id, customer_name, customer_email, subject, description, priority, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (ticket_id, ticket.customer_name, ticket.customer_email,
              ticket.subject, ticket.description, ticket.priority, now, now))
        await db.commit()
        return {"ticket_id": ticket_id, "created_at": now}
    finally:
        await db.close()

@router.get("/api/tickets")
async def get_tickets(status: str = None, search: str = None):
    db = await get_db()
    try:
        query = "SELECT * FROM tickets WHERE 1=1"
        params = []
        if status:
            query += " AND status = ?"
            params.append(status)
        if search:
            query += " AND (customer_name LIKE ? OR customer_email LIKE ? OR ticket_id LIKE ? OR description LIKE ?)"
            like = f"%{search}%"
            params.extend([like, like, like, like])
        query += " ORDER BY created_at DESC"
        cursor = await db.execute(query, params)
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        await db.close()

@router.get("/api/tickets/{ticket_id}")
async def get_ticket(ticket_id: str):
    db = await get_db()
    try:
        cursor = await db.execute("SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,))
        ticket = await cursor.fetchone()
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        cursor2 = await db.execute("SELECT * FROM notes WHERE ticket_id = ? ORDER BY created_at DESC", (ticket_id,))
        notes = await cursor2.fetchall()
        result = dict(ticket)
        result["notes"] = [dict(n) for n in notes]
        return result
    finally:
        await db.close()

@router.put("/api/tickets/{ticket_id}")
async def update_ticket(ticket_id: str, update: TicketUpdate):
    db = await get_db()
    try:
        now = datetime.utcnow().isoformat()
        if update.status:
            await db.execute("UPDATE tickets SET status=?, updated_at=? WHERE ticket_id=?",
                             (update.status, now, ticket_id))
        if update.priority:
            await db.execute("UPDATE tickets SET priority=?, updated_at=? WHERE ticket_id=?",
                             (update.priority, now, ticket_id))
        if update.note:
            await db.execute("INSERT INTO notes (ticket_id, note_text, created_at) VALUES (?, ?, ?)",
                             (ticket_id, update.note, now))
        await db.commit()
        return {"success": True, "updated_at": now}
    finally:
        await db.close()

# ─── PAGE ROUTES ──────────────────────────────────────────

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, status: str = None, search: str = None):
    db = await get_db()
    try:
        query = "SELECT * FROM tickets WHERE 1=1"
        params = []
        if status:
            query += " AND status = ?"
            params.append(status)
        if search:
            query += " AND (customer_name LIKE ? OR customer_email LIKE ? OR ticket_id LIKE ? OR description LIKE ?)"
            like = f"%{search}%"
            params.extend([like, like, like, like])
        query += " ORDER BY created_at DESC"
        cursor = await db.execute(query, params)
        rows = await cursor.fetchall()
        tickets = [dict(row) for row in rows]
        return templates.TemplateResponse("index.html", {
            "request": request,
            "tickets": tickets,
            "current_status": status or "",
            "current_search": search or ""
        })
    finally:
        await db.close()

@router.get("/create", response_class=HTMLResponse)
async def create_page(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})

@router.get("/tickets/{ticket_id}", response_class=HTMLResponse)
async def ticket_detail_page(request: Request, ticket_id: str):
    db = await get_db()
    try:
        cursor = await db.execute("SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,))
        ticket = await cursor.fetchone()
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        cursor2 = await db.execute("SELECT * FROM notes WHERE ticket_id = ? ORDER BY created_at DESC", (ticket_id,))
        notes = await cursor2.fetchall()
        return templates.TemplateResponse("ticket_detail.html", {
            "request": request,
            "ticket": dict(ticket),
            "notes": [dict(n) for n in notes]
        })
    finally:
        await db.close()
