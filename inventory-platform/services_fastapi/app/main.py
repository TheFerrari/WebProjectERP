from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.api.v1.routes import branches, items, stock, orders, audit
from app.core.config import settings
from app.core.logging import configure_logging
from app.db.session import get_db

configure_logging()
app = FastAPI(title=settings.fastapi_app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.fastapi_cors_origins.split(',')],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/health')
def health():
    return {'status': 'ok'}


@app.get('/ready')
def ready(db=Depends(get_db)):
    db.execute(text('SELECT 1'))
    return {'status': 'ready'}


app.include_router(branches.router, prefix='/v1')
app.include_router(items.router, prefix='/v1')
app.include_router(stock.router, prefix='/v1')
app.include_router(orders.router, prefix='/v1')
app.include_router(audit.router, prefix='/v1')
