from app import create_app
from extensions import db
from load_data import load_data


app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    load_data()