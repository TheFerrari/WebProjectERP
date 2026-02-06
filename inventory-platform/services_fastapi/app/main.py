from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
import uuid
from app.core.config import settings
from app.core.logging import configure_logging
from app.db.session import get_db
from app.api.v1.routes import branches, items, stock, orders, audit

configure_logging()
app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(','),
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.middleware('http')
async def request_id_middleware(request, call_next):
    request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))
    response = await call_next(request)
    response.headers['X-Request-ID'] = request_id
    return response

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.get('/ready')
def ready(db: Session = Depends(get_db)):
    db.execute(text('SELECT 1'))
    return {'status': 'ready'}

app.include_router(branches.router, prefix='/v1')
app.include_router(items.router, prefix='/v1')
app.include_router(stock.router, prefix='/v1')
app.include_router(orders.router, prefix='/v1')
app.include_router(audit.router, prefix='/v1')
