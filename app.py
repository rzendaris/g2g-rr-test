import math

import pymysql

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from models import db, Seller, Offer
from scheduler import RoundRobinScheduler
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/offers_db'
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
db.init_app(app)
cache = Cache(app)


def get_sellers():
    sellers = Seller.query.all()
    return sellers


@app.route('/offers', methods=['GET'])
def get_offers():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 100))
    filter_params = {k: v for k, v in request.args.items() if k not in ['page', 'per_page']}
    sort_params = request.args.get('sort', 'offer_date desc')

    sellers = get_sellers()
    scheduler = RoundRobinScheduler(sellers)

    # Get unique sellers for the current page
    get_index = math.floor((page - 1) * per_page / len(sellers))
    selected_sellers = scheduler.get_sellers_for_page(page, per_page)
    seller_ids = [seller.id for seller in selected_sellers]

    offers = []

    # Fetch offers for the selected sellers
    for seller_id in seller_ids:
        seller_offers = Offer.query.filter_by(seller_id=seller_id)

        for param, value in filter_params.items():
            seller_offers = seller_offers.filter(getattr(Offer, param) == value)

        if sort_params:
            column, order = sort_params.split()
            if order.lower() == 'desc':
                seller_offers = seller_offers.order_by(getattr(Offer, column).desc())
            else:
                seller_offers = seller_offers.order_by(getattr(Offer, column))

        # Extend the offers list with the current seller's offers if sequence still available
        current_seller_offers = seller_offers.all()
        if get_index < len(current_seller_offers):
            offers.append(current_seller_offers[get_index])

        # If we have enough offers, stop fetching more
        if len(offers) >= per_page:
            break

    # Limit the number of offers returned to per_page
    offers = offers[:per_page]

    return jsonify({
        'page': page,
        'per_page': per_page,
        'offers': [{
            'id': offer.id,
            'details': offer.details,
            'seller_id': offer.seller_id
        } for offer in offers]
    })


if __name__ == '__main__':
    app.run(debug=True)
