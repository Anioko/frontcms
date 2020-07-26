from app import db


class PaymentSetting(db.Model):
    __tablename__ = 'payment_settings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String())
    display_name = db.Column(db.String())
    value = db.Column(db.String(), default=None)

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

