from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.config import settings
from app.routers import auth, bots, chats, contacts, settings as settings_router, webhook, ws

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.mount(
    f"/{settings.static_dir}",
    StaticFiles(directory=settings.static_dir),
    name="static",
)

templates = Jinja2Templates(directory=settings.templates_dir)

app.include_router(auth.router)
app.include_router(chats.router)
app.include_router(contacts.router)
app.include_router(settings_router.router)
app.include_router(bots.router)
app.include_router(webhook.router)
app.include_router(ws.router)
