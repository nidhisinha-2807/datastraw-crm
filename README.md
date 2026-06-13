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
## 📊 Live Monitoring & Mock Data Architecture

To ensure immediate operational visualization upon initial deployment, the Support Operations Center dashboard integrates a dynamic dataset fallback layer:

* **Production Database Mode**: Real-time entries dynamically fetched from the live SQLite instance (e.g., active customer updates, status switches, and manual notes).
* **Visual Enrichment Mode (Demo Workspace)**: When the core query layer identifies an empty relational state (0 active ledger entries), the controller layer safely populates the grid with **8 hardcoded Indian Enterprise & SaaS tech company profiles** (`TKT-001` through `TKT-008`).

### ⚙️ Deterministic Server-Side Filtering
Unlike basic client-side templates, all filtering parameters are executed natively within the Python ASGI backend:
* **Dropdown Status Hooks**: Filtering parameters (`Open`, `In Progress`, `Closed`) evaluate both database rows and mock structures prior to template serialization.
* **Regular Expression Text Queries**: The universal search field parses token sub-strings against target fields (`customer_name`, `customer_email`, `ticket_id`, `subject`) globally.
* **Atomic Metric Counters**: Priority allocations (`High`, `Medium`, `Low`) and proportional percentage indicators are pre-calculated as server-side context scalars to maintain lightweight frontend render execution.