from app import db
from typing import List

class SiteSetting(db.Model):
    __tablename__ = 'sitesettings'

    id = db.Column(db.Integer, primary_key=True)
    site_title = db.Column(db.String(128), unique=True)
    siteaddress = db.Column(db.String(500))
    administration_user_address =db.Column(db.String(128),unique=True)
    site_Language=db.Column(db.String(120),unique=True)



    @classmethod
    def find_all(cls) -> List["SiteSetting"]:
        return cls.query.all()
