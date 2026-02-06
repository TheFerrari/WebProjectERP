from app.db.session import SessionLocal
from app.models.domain import Branch, Item, Stock


def main():
    db = SessionLocal()
    if not db.query(Branch).count():
        b = Branch(name='HQ', location='City Center', timezone='UTC')
        i = Item(sku='SKU-1', name='Laptop', description='Demo item', unit='pcs', min_stock_level=5)
        db.add_all([b, i])
        db.commit()
        db.refresh(b)
        db.refresh(i)
        db.add(Stock(branch_id=b.id, item_id=i.id, quantity=30))
        db.commit()
    db.close()


if __name__ == '__main__':
    main()
