# Climate Emissions Explorer

Climate Emissions Explorer is a database-driven Flask web application that allows users to explore and compare CO₂ emissions data by country and year.

The application uses open data from the Our World in Data CO₂ and Greenhouse Gas Emissions dataset. The original dataset contains more than 45,000 rows, but this application loads a filtered subset of 5,000 records to meet the assessment requirement of using between 2,000 and 7,000 records.

## Project Aim

The aim of this project is to demonstrate how open data can be loaded into a relational database and displayed through a Flask web application.

Users can:

- View a summary of the database on the homepage
- Browse countries included in the dataset
- Search for countries
- View yearly CO₂ emission records for a selected country
- Compare two countries side by side for a selected year
- Read information about the data source and database design

## Data Source

The data used in this application comes from:

Our World in Data CO₂ and Greenhouse Gas Emissions dataset  
https://github.com/owid/co2-data

The CSV file used is:

https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv

The application uses the following columns from the dataset:

- country
- iso_code
- year
- co2
- co2_per_capita
- population
- gdp

## Database Design

The application uses SQLite and Flask-SQLAlchemy.

There are two linked tables:

### Countries table

The countries table stores country information.

Fields:

- id
- name
- iso_code

### Emission records table

The emission records table stores yearly emissions data.

Fields:

- id
- country_id
- year
- co2
- co2_per_capita
- population
- gdp

The relationship is:

```text
One country can have many emission records.
```

This creates a one-to-many relationship between the `countries` table and the `emission_records` table.

## Application Structure

```text
climate_emissions_explorer/
│
├── app.py
├── models.py
├── extensions.py
├── load_data.py
├── init_db.py
├── requirements.txt
├── README.md
├── git-log.txt
│
├── data/
│   └── owid-co2-data.csv
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── countries.html
│   ├── country_detail.html
│   ├── compare.html
│   ├── about.html
│   └── 404.html
│
├── static/
│   └── style.css
│
└── tests/
    └── test_app.py
```

## Main Files

### app.py

This file contains the Flask application factory and the route definitions.

Main routes:

- `/` homepage
- `/countries` country list and search page
- `/country/<country_id>` country detail page
- `/compare` country comparison page
- `/about` about page
- custom 404 error handler

### models.py

This file defines the database models:

- Country
- EmissionRecord

### extensions.py

This file creates the shared SQLAlchemy database object used across the application.

### load_data.py

This file reads the open-data CSV file, filters it, and loads 5,000 records into the database.

### init_db.py

This file creates the database tables and loads the data.

### templates/

This folder contains the HTML templates used by Flask.

### static/style.css

This file contains the CSS styling for the application.

### tests/test_app.py

This file contains pytest tests for the main application routes.

## Installation

First, clone or download the project folder.

Move into the project directory:

```bash
cd climate_emissions_explorer
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Setting Up the Database

Make sure the dataset is saved in this location:

```text
data/owid-co2-data.csv
```

Then run:

```bash
python init_db.py
```

This command creates the SQLite database and loads 5,000 emission records.

## Running the Application Locally

Start the Flask application with:

```bash
python app.py
```

Then open this address in a web browser:

```text
http://127.0.0.1:5000
```

## Running Tests

The project uses pytest.

To run the tests:

```bash
python -m pytest
```

The tests check that:

- the homepage loads
- the countries page loads
- the country detail page loads
- the comparison page loads
- comparison results display
- the custom 404 page works

## Error Handling

The application includes a custom 404 error page.

If a user visits a page that does not exist, Flask returns the custom `404.html` template.

The country detail route also checks whether a country exists before displaying the page.

## Maintenance Notes

To reload the database from the CSV file, run:

```bash
python init_db.py
```

This will delete the existing database tables, recreate them, and load the filtered dataset again.

If the dataset changes in future, the application can be updated by replacing the CSV file inside the `data/` folder and running the database initialization script again.

The number of loaded records can be changed in `load_data.py` by editing:

```python
MAX_RECORDS = 5000
```

However, for this assessment the number should remain between 2,000 and 7,000 records.

## Deployment

The application is intended to be deployed on Render.

Suggested Render build command:

```bash
pip install -r requirements.txt
```

Suggested Render start command:

```bash
python init_db.py && gunicorn app:app
```

After deployment, the Render URL should be added to the final report.

## Git

Git was used during development for source control.

The git log was generated using:

```bash
git log --pretty=format:'%h : %s' --graph > git-log.txt
```

## Author

Emmanuel Effa