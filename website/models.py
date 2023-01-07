from . import db
from sqlalchemy.sql import func

class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    director_id = db.Column(db.String(50), unique=True)
    director_name = db.Column(db.String(150))
    ret_value = db.Column(db.String(750))
    count = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())