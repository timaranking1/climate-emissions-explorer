import pytest

from app import create_app
from extensions import db
from models import Country, EmissionRecord


@pytest.fixture()
def app(tmp_path):
    test_database = tmp_path / "test_emissions.db"

    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{test_database}",
    })

    with app.app_context():
        db.create_all()

        nigeria = Country(name="Nigeria", iso_code="NGA")
        ghana = Country(name="Ghana", iso_code="GHA")

        db.session.add_all([nigeria, ghana])
        db.session.commit()

        nigeria_record = EmissionRecord(
            country_id=nigeria.id,
            year=2020,
            co2=120.5,
            co2_per_capita=0.6,
            population=206000000,
            gdp=432000000000
        )

        ghana_record = EmissionRecord(
            country_id=ghana.id,
            year=2020,
            co2=25.3,
            co2_per_capita=0.8,
            population=31000000,
            gdp=70000000000
        )

        db.session.add_all([nigeria_record, ghana_record])
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def test_home_page_loads(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Climate Emissions Explorer" in response.data


def test_countries_page_loads(client):
    response = client.get("/countries")

    assert response.status_code == 200
    assert b"Nigeria" in response.data
    assert b"Ghana" in response.data


def test_country_detail_page_loads(client):
    response = client.get("/country/1")

    assert response.status_code == 200
    assert b"Nigeria" in response.data
    assert b"2020" in response.data


def test_compare_page_loads(client):
    response = client.get("/compare")

    assert response.status_code == 200
    assert b"Compare Countries" in response.data


def test_compare_results_show(client):
    response = client.get("/compare?country1=1&country2=2&year=2020")

    assert response.status_code == 200
    assert b"Nigeria" in response.data
    assert b"Ghana" in response.data
    assert b"CO" in response.data


def test_404_page(client):
    response = client.get("/this-page-does-not-exist")

    assert response.status_code == 404
    assert b"Page Not Found" in response.data