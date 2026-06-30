from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import database

app = FastAPI()

templates = Jinja2Templates(directory="templates")

database.init_db()
database.add_ticket("1", "Noah")
database.add_ticket("2", "Lucas")
database.add_ticket("3", "Axel")

@app.get("/scan/{numero}")
async def scan(numero: str):
    return database.validate_ticket(numero)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.get("/scan-page", response_class=HTMLResponse)
def scan_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="scan.html"
    )


@app.get("/scan/{ticket_id}")
def scan(ticket_id: str):

    ticket = database.get_ticket(ticket_id)

    if ticket is None:
        return {"status": "inconnu"}

    if ticket[2]:
        return {
            "status": "deja_utilise",
            "nom": ticket[1]
        }

    database.validate_ticket(ticket_id)

    return {
        "status": "valide",
        "nom": ticket[1]
    }