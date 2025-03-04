# This is where the SQL has beed added for the user sor far, 
# Other SQL will will be added on stock models.
from models import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    buyers_power = db.Column(db.Float, default=10000.00)
