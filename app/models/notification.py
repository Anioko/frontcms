from app import db
import time

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    related_id = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def get_data(self):
        return json.loads(str(self.payload_json))

    def parsed(self):
        user = User.query.filter_by(id=self.related_id).first()
        if 'unread_message' in self.name:
            msg = Message.query.filter_by(id=json.loads(self.payload_json)['message']).first()
            if user and msg:
                return {
                    "type": self.name,
                    "link": url_for('main.read_notification', notification_id=self.id),
                    "text": "<p><b>{}</b> sent you a message <u>{} ...</u></strong></p>".format(
                        user.full_name, msg.body[:40].replace("\n", " ")),
                    "timestamp": datetime.fromtimestamp(self.timestamp).ctime(),
                    "time": self.timestamp,
                    "user": user,
                    "read": self.read
                }
            else:
                self.read = True
                db.session.add(self)
                db.session.commit()
