# Datastraw CRM — Customer Support Ticketing System

A full-stack web application for managing customer support tickets, built with Python + FastAPI, SQLite, and Jinja2 templates styled with Tailwind CSS.

## Tech Stack
- **Backend:** Python, FastAPI
- **Database:** SQLite (via aiosqlite)
- **Frontend:** Jinja2 HTML templates + Tailwind CSS (CDN)
- **Deployment:** Railway.app

## Features
- Create support tickets with auto-generated IDs (TKT-001, TKT-002...)
- List all tickets with search and filter by status
- View ticket details with full history
- Update ticket status (Open / In Progress / Closed)
- Set priority levels (Low / Medium / High)
- Add internal notes/comments to tickets
- Dashboard stats showing ticket counts by status

## Local Setup

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd datastraw-crm

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
uvicorn main:app --reload

# 5. Open in browser
# http://localhost:8000
```

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/tickets | Create a new ticket |
| GET | /api/tickets | List all tickets (supports ?status= and ?search=) |
| GET | /api/tickets/{ticket_id} | Get single ticket with notes |
| PUT | /api/tickets/{ticket_id} | Update status, priority, or add note |

## Project Structure
```
datastraw-crm/
├── main.py          # App entry point
├── database.py      # DB init and connection
├── models.py        # Pydantic schemas
├── routes/
│   └── tickets.py   # All routes (API + pages)
├── templates/       # Jinja2 HTML pages
├── static/          # CSS
└── requirements.txt
```
