from app import db


class OrgStaff(db.Model):
    __tablename__ = 'org_staff'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    invited_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    org_id = db.Column(db.Integer, db.ForeignKey('organisations.id', ondelete="CASCADE"))
    user = db.relationship("User", primaryjoin="User.id==OrgStaff.user_id")
    referer = db.relationship("User", primaryjoin="User.id==OrgStaff.invited_by")
    org = db.relationship("Organisation", primaryjoin="Organisation.id==OrgStaff.org_id", backref='staff')
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

