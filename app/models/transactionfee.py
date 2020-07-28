from app import db



class TransactionFee(db.Model):
    __tablename__ = 'transactionfees'
    id = db.Column(db.Integer, primary_key=True)
    provider_name = db.Column(db.String)
    local_fee = db.Column(db.Integer)
    european_fee = db.Column(db.Integer)
    international_fee = db.Column(db.Integer)
    transfer_fee = db.Column(db.Integer)
    our_fee = db.Column(db.Integer)
    local_percentage = db.Column(db.Float)
    european_percentage = db.Column(db.Float)
    international_percentage = db.Column(db.Float)
    our_percentage = db.Column(db.Float)
    card_type = db.Column(db.String)
    currency_symbol = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)
