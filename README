# Technical test EcoCO2

![https://www.ecoco2.com/wp-content/uploads/2020/12/logo-ecoco2.jpg](https://www.ecoco2.com/wp-content/uploads/2020/12/logo-ecoco2.jpg)

# Context

Simple app to gather CO2 info from public API, interpolate data and visualize the differences between real and interpolated data.

Instructions were to:
- Gather data relative to French co2 rate between 2017 and 2018 from this API https://api-recrutement.ecoco2.com/docs/#tag/v1
- Save data to a Django table.
- Filter data to obtain an hourly frequency and save it to a second table.
- From the hourly table, interpolate data to re(obtain) initial frequency of 30 minutes.
- Show last 20 points in a table with difference between real and interpolated data.
- For each data (real and interpolated), add a line with average rate for weekdays and weekends.
- Add a graph showing the difference between the two datasets.

# Installation

```
# Initialize and activate virtual environment 
python -m venv env
source env/bin/activate

# Upgrade pip and install required packages
pip install --upgrade pip
pip install -r requirements.txt
```

# Use

## Data import

CO2 data are loaded from [recruitment public API](http://api-recrutement.ecoco2.com/v1/data/) and interpolated using pandas.

You can reload all data or simply use provided db.sqlite3 file.

To re-import data:
```
# Flush existing data
python manage.py flush

# Load data from API
python manage.py import_data

# Interpolate data
python manage.py interpolate_data
```

## Running the server

```
# Load the environment if you haven't already
source env/bin/activate

# Runserver
python manage.py runserver
```

Access server and results by visiting [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
