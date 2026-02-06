import jwt
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.core.config import settings
from app.models import Branch, Item, Stock, Order, OrderLine, OrderStatus

engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False})
TestingSessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def token(roles):
    return jwt.encode({'sub': '1', 'roles': roles}, settings.jwt_secret, algorithm='HS256')


def auth_headers(roles):
    return {'Authorization': f'Bearer {token(roles)}'}


def seed(db):
    b = Branch(name='HQ', location='X', timezone='UTC')
    i = Item(sku='A1', name='ItemA', unit='pcs', min_stock_level=1)
    db.add_all([b, i]); db.commit(); db.refresh(b); db.refresh(i)
    db.add(Stock(branch_id=b.id, item_id=i.id, quantity=10))
    db.commit()
    return b, i


def test_auth_required():
    r = client.get('/v1/stock')
    assert r.status_code == 403


def test_worker_cannot_adjust_stock():
    db = TestingSessionLocal(); seed(db); db.close()
    r = client.put('/v1/stock', json={'branch_id': 1, 'item_id': 1, 'quantity': 5}, headers=auth_headers(['Worker']))
    assert r.status_code == 403


def test_fulfill_atomic():
    db = TestingSessionLocal()
    b, i = seed(db)
    order = Order(branch_id=b.id, status=OrderStatus.submitted, created_by=1)
    db.add(order); db.commit(); db.refresh(order)
    db.add(OrderLine(order_id=order.id, item_id=i.id, requested_qty=4, fulfilled_qty=0)); db.commit(); db.close()

    r = client.post(f'/v1/orders/{order.id}/fulfill', headers=auth_headers(['Manager']))
    assert r.status_code == 200

    db2 = TestingSessionLocal()
    stock = db2.query(Stock).filter_by(branch_id=1, item_id=1).first()
    assert stock.quantity == 6
    db2.close()
