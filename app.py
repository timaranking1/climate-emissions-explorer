from flask import Flask, render_template, request
from extensions import db
from models import Country, EmissionRecord


def create_app(test_config=None):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///emissions.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)

    @app.route("/")
    def index():
        country_count = Country.query.count()
        record_count = EmissionRecord.query.count()

        return render_template(
            "index.html",
            country_count=country_count,
            record_count=record_count
        )

    @app.route("/countries")
    def countries():
        search = request.args.get("search", "").strip()

        if search:
            countries = Country.query.filter(
                Country.name.ilike(f"%{search}%")
            ).order_by(Country.name.asc()).all()
        else:
            countries = Country.query.order_by(Country.name.asc()).all()

        return render_template(
            "countries.html",
            countries=countries,
            search=search
        )

    @app.route("/country/<int:country_id>")
    def country_detail(country_id):
        country = Country.query.get_or_404(country_id)

        records = EmissionRecord.query.filter_by(
            country_id=country.id
        ).order_by(
            EmissionRecord.year.asc()
        ).all()

        latest_record = EmissionRecord.query.filter_by(
            country_id=country.id
        ).order_by(
            EmissionRecord.year.desc()
        ).first()

        return render_template(
            "country_detail.html",
            country=country,
            records=records,
            latest_record=latest_record
        )
    
    @app.route("/compare")
    def compare():
        countries = Country.query.order_by(Country.name.asc()).all()

        years_query = db.session.query(
            EmissionRecord.year
        ).distinct().order_by(
            EmissionRecord.year.desc()
        ).all()

        years = [year[0] for year in years_query]

        country1_id = request.args.get("country1", type=int)
        country2_id = request.args.get("country2", type=int)
        selected_year = request.args.get("year", type=int)

        country1 = None
        country2 = None
        record1 = None
        record2 = None
        difference = None

        if country1_id and country2_id and selected_year:
            country1 = Country.query.get(country1_id)
            country2 = Country.query.get(country2_id)

            record1 = EmissionRecord.query.filter_by(
                country_id=country1_id,
                year=selected_year
            ).first()

            record2 = EmissionRecord.query.filter_by(
                country_id=country2_id,
                year=selected_year
            ).first()

            if record1 and record2 and record1.co2 is not None and record2.co2 is not None:
                difference = abs(record1.co2 - record2.co2)

        return render_template(
            "compare.html",
            countries=countries,
            years=years,
            country1=country1,
            country2=country2,
            record1=record1,
            record2=record2,
            difference=difference,
            selected_country1=country1_id,
            selected_country2=country2_id,
            selected_year=selected_year
        )

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)