from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.models.domain import Branch, Item, Stock

SQLALCHEMY_DATABASE_URL = 'sqlite:///./test.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def token(roles, sub='1'):
    return jwt.encode({'sub': sub, 'roles': roles}, 'change-me-jwt', algorithm='HS256')


def setup_module(_):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    b = Branch(name='B1', location='loc', timezone='UTC')
    i = Item(sku='A1', name='Item1', description='', unit='pcs', min_stock_level=0)
    db.add_all([b, i])
    db.commit()
    db.refresh(b)
    db.refresh(i)
    db.add(Stock(branch_id=b.id, item_id=i.id, quantity=20))
    db.commit()
    db.close()


def test_auth_verification_required():
    resp = client.get('/v1/items')
    assert resp.status_code == 403 or resp.status_code == 401


def test_worker_cannot_adjust_stock():
    resp = client.put('/v1/stock', json={'branch_id': 1, 'item_id': 1, 'quantity': 10}, headers={'Authorization': f'Bearer {token(["Worker"])}'})
    assert resp.status_code == 403


def test_fulfill_order_atomic():
    hdr = {'Authorization': f'Bearer {token(["Manager"])}'}
    order_resp = client.post('/v1/orders', json={'branch_id': 1, 'lines': [{'item_id': 1, 'requested_qty': 5}]}, headers=hdr)
    assert order_resp.status_code == 200
    oid = order_resp.json()['id']
    sub = client.post(f'/v1/orders/{oid}/submit', headers=hdr)
    assert sub.status_code == 200
    full = client.post(f'/v1/orders/{oid}/fulfill', headers=hdr)
    assert full.status_code == 200
    stock = client.get('/v1/stock', headers=hdr).json()[0]
    assert stock['quantity'] == 15
