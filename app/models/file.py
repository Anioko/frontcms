from app import db


class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    path = db.Column(db.String(255))
    uploaded_date = db.Column(db.DateTime)
    photogalleryitems = db.relationship('PhotoGalleryItem',
                                        backref='file', lazy='dynamic')


    def __repr__(self):
        return '<File {!r}>'.format(self.name)
