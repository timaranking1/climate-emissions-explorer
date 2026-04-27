import pandas as pd
from extensions import db
from models import Country, EmissionRecord


DATA_FILE = "data/owid-co2-data.csv"
MAX_RECORDS = 5000
START_YEAR = 2000
END_YEAR = 2023


def clean_number(value):
    if pd.isna(value):
        return None
    return float(value)


def load_data():
    print("Reading CSV file...")

    df = pd.read_csv(DATA_FILE)

    required_columns = [
        "country",
        "iso_code",
        "year",
        "co2",
        "co2_per_capita",
        "population",
        "gdp"
    ]

    df = df[required_columns]

    df = df[
        (df["year"] >= START_YEAR) &
        (df["year"] <= END_YEAR) &
        (df["iso_code"].notna()) &
        (df["co2"].notna())
    ]

    df = df.head(MAX_RECORDS)

    print(f"Loading {len(df)} records into the database...")

    for _, row in df.iterrows():
        country = Country.query.filter_by(name=row["country"]).first()

        if country is None:
            country = Country(
                name=row["country"],
                iso_code=row["iso_code"]
            )
            db.session.add(country)
            db.session.commit()

        emission_record = EmissionRecord(
            country_id=country.id,
            year=int(row["year"]),
            co2=clean_number(row["co2"]),
            co2_per_capita=clean_number(row["co2_per_capita"]),
            population=clean_number(row["population"]),
            gdp=clean_number(row["gdp"])
        )

        db.session.add(emission_record)

    db.session.commit()

    print("Data loading complete.")