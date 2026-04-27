from extensions import db


class Country(db.Model):
    __tablename__ = "countries"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    iso_code = db.Column(db.String(20), nullable=True)

    records = db.relationship("EmissionRecord", backref="country", lazy=True)

    def __repr__(self):
        return f"<Country {self.name}>"


class EmissionRecord(db.Model):
    __tablename__ = "emission_records"

    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey("countries.id"), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    co2 = db.Column(db.Float, nullable=True)
    co2_per_capita = db.Column(db.Float, nullable=True)
    population = db.Column(db.Float, nullable=True)
    gdp = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"<EmissionRecord {self.year}>"