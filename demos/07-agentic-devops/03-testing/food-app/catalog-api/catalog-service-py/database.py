from models import db, CatalogItem
from decimal import Decimal

def init_db(app):
    with app.app_context():
        db.create_all()
        
        if CatalogItem.query.count() == 0:
            items = [
                CatalogItem(
                    id=1,
                    name="Hand pulled Noodles",
                    in_stock=9,
                    price=Decimal('17.0000'),
                    picture_url="hand-pulled-noodles.png",
                    description="Hand pulled noodles made with love by our experienced cooks from Sichuan. Served with your choice of meat, vegetables, and smashed cucumber salad."
                ),
                CatalogItem(
                    id=2,
                    name="Pad Kra Pao",
                    in_stock=12,
                    price=Decimal('16.0000'),
                    picture_url="pad-kra-pao.png",
                    description="Pad Kra Pao definitely one of the most popular spicy dishes in Thailand. Cooked with thai holy basil, long beans and chicken. Served with jasmine rice and fried egg."
                ),
                CatalogItem(
                    id=3,
                    name="Wiener Schnitzel",
                    in_stock=13,
                    price=Decimal('18.0000'),
                    picture_url="schnitzel.jpg",
                    description="Wiener Schnitzel is a traditional Austrian dish consisting of a thin slice of veal coated in breadcrumbs and fried. Served with potato salad and lemon."
                ),
                CatalogItem(
                    id=4,
                    name="Falafel Plate",
                    in_stock=9,
                    price=Decimal('12.0000'),
                    picture_url="falafel.jpg",
                    description="Falafel is a deep-fried ball, doughnut or patty made from ground chickpeas. Served with hummus, pita bread, and salad."
                ),
                CatalogItem(
                    id=5,
                    name="Pizza Tartufo",
                    in_stock=4,
                    price=Decimal('24.0000'),
                    picture_url="pizza.jpg",
                    description="Pizza truffle is well tasting, exclusive joy for your taste bud. A delight of white pizza where the protagonist is our cheese with truffle flakes."
                ),
            ]
            db.session.add_all(items)
            db.session.commit()
