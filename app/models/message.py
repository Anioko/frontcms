from app import db


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=db.func.now())
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    read_at = db.Column(db.DateTime, default=None, nullable=True)

    user = db.relationship('User', primaryjoin="Message.user_id==User.id")

    def __repr__(self):
        return '<Message {}>'.format(self.body)
