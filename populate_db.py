import random
from datetime import datetime, timedelta
from faker import Faker
from models import db, Seller, Offer

fake = Faker()


def create_sellers_and_offers():
    # Create sellers and offers
    sellers_10_offers = [Seller(name=fake.company()) for _ in range(500)]
    sellers_5_offers = [Seller(name=fake.company()) for _ in range(500)]
    sellers_25_offers = [Seller(name=fake.company()) for _ in range(100)]

    # Add sellers to the session
    db.session.add_all(sellers_10_offers)
    db.session.add_all(sellers_5_offers)
    db.session.add_all(sellers_25_offers)
    db.session.commit()

    # Create offers for sellers
    def create_offers(seller, count):
        offers = [Offer(
            seller_id=seller.id,
            details=fake.text(max_nb_chars=100),
            offer_date=fake.date_time_this_year()
        ) for _ in range(count)]
        return offers

    # Add offers to sellers
    for seller in sellers_10_offers:
        offers = create_offers(seller, 10)
        db.session.add_all(offers)

    for seller in sellers_5_offers:
        offers = create_offers(seller, 5)
        db.session.add_all(offers)

    for seller in sellers_25_offers:
        offers = create_offers(seller, 25)
        db.session.add_all(offers)

    db.session.commit()


if __name__ == "__main__":
    from app import app  # Import app to ensure app context

    with app.app_context():
        db.create_all()  # Ensure tables are created
        create_sellers_and_offers()
