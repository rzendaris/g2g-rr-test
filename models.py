from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Seller(db.Model):
    __tablename__ = 'sellers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    offers = db.relationship('Offer', backref='seller', lazy=True)


class Offer(db.Model):
    __tablename__ = 'offers'
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.id'), nullable=False)
    details = db.Column(db.String(255), nullable=False)
    offer_date = db.Column(db.DateTime, nullable=False)
