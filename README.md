# KML Route Parser

A Python library and command-line utility for parsing **KML** and **KMZ** files, extracting route points, generating **Google Maps Directions URLs**, and exporting route data to **CSV**.

## Features

* Parse KML files
* Parse KMZ files
* Automatic KMZ extraction
* Extract Placemark Point coordinates
* Generate Google Maps Directions URLs
* Support for name-based URLs
* Support for coordinate-based URLs
* Export route points to CSV
* Interactive file picker dialogs
* Interactive CSV save dialog
* Command-line automation support
* Reusable Python class for integration into other projects

---

## Project Structure

```text
project/
│
├── kml_route_parser.py    # Reusable library
├── main.py                # Command-line application
└── README.md
```

---

## Requirements

Python 3.8+

No third-party dependencies are required.

The project uses only Python standard library modules:

```text
argparse
csv
os
tempfile
tkinter
urllib
xml.etree.ElementTree
zipfile
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/razonklnbd/kml-to-google-map-url.git

cd kml-to-google-map-url
```

No additional installation steps are required.

---

## Supported Input Formats

### KML

```xml
<Placemark>
    <name>Home</name>
    <Point>
        <coordinates>
            72.5432,23.0345,0
        </coordinates>
    </Point>
</Placemark>
```

### KMZ

KMZ files are automatically extracted and processed.

---

# Command Line Usage

## Interactive Mode

Launch without parameters:

```bash
python main.py
```

The application will:

1. Open a file selection dialog
2. Ask whether to use names or coordinates
3. Ask where to save the CSV file
4. Display the generated Google Maps URL

---

## Specify Input File

```bash
python main.py route.kml
```

or

```bash
python main.py route.kmz
```

---

## Generate URL Using Place Names

```bash
python main.py route.kmz --url-mode name
```

Example output:

```text
https://www.google.com/maps/dir/Home/Office/Warehouse/data=!4m2!4m1!3e0
```

---

## Generate URL Using Coordinates

```bash
python main.py route.kmz --url-mode coord
```

Example output:

```text
https://www.google.com/maps/dir/23.0345,72.5432/23.0654,72.6021/data=!4m2!4m1!3e0
```

---

## Save CSV to Specific Location

```bash
python main.py route.kmz --csv points.csv
```

or

```bash
python main.py route.kmz --csv "C:\Routes\points.csv"
```

---

## Disable CSV Export

```bash
python main.py route.kmz --no-csv
```

---

## Fully Automated Example

```bash
python main.py route.kmz \
    --url-mode coord \
    --csv points.csv
```

This mode performs:

* KML/KMZ parsing
* Route extraction
* Google Maps URL generation
* CSV export

without any user interaction.

---

# Library Usage

The parser can be imported directly into other Python applications.

## Basic Example

```python
from kml_route_parser import KmlRouteParser

parser = KmlRouteParser(
    "route.kmz"
)

parser.load()

url = parser.get_google_maps_url(
    use_names=False
)

print(url)
```

---

## Get Extracted Points

```python
from kml_route_parser import KmlRouteParser

parser = KmlRouteParser(
    "route.kml"
)

parser.load()

points = parser.get_points()

for point in points:

    print(
        point["name"],
        point["latitude"],
        point["longitude"]
    )
```

Example output:

```python
[
    {
        "name": "Home",
        "description": "",
        "latitude": 23.0345,
        "longitude": 72.5432
    }
]
```

---

## Export CSV

```python
from kml_route_parser import KmlRouteParser

parser = KmlRouteParser(
    "route.kmz"
)

parser.load()

parser.save_csv(
    "points.csv"
)
```

---

## Generate URL Using Names

```python
url = parser.get_google_maps_url(
    use_names=True
)
```

Example:

```text
https://www.google.com/maps/dir/Home/Office/Warehouse/data=!4m2!4m1!3e0
```

---

## Generate URL Using Coordinates

```python
url = parser.get_google_maps_url(
    use_names=False
)
```

Example:

```text
https://www.google.com/maps/dir/23.0345,72.5432/23.0654,72.6021/data=!4m2!4m1!3e0
```

---

# API Reference

## KmlRouteParser

### Constructor

```python
KmlRouteParser(file_path)
```

Parameters:

| Parameter | Type | Description             |
| --------- | ---- | ----------------------- |
| file_path | str  | Path to KML or KMZ file |

---

### load()

Load and parse the KML/KMZ file.

```python
points = parser.load()
```

Returns:

```python
list[dict]
```

---

### get_points()

Return loaded points.

```python
points = parser.get_points()
```

---

### get_google_maps_url()

Generate Google Maps directions URL.

```python
url = parser.get_google_maps_url(
    use_names=True
)
```

Parameters:

| Parameter | Type | Description                            |
| --------- | ---- | -------------------------------------- |
| use_names | bool | Use place names instead of coordinates |

---

### save_csv()

Export points to CSV.

```python
parser.save_csv(
    "points.csv"
)
```

---

# Example Point Structure

```python
{
    "name": "Home",
    "description": "Starting Point",
    "latitude": 23.0345,
    "longitude": 72.5432
}
```

---

# Future Enhancements

Potential future features:

* GPX support
* GeoJSON export
* Distance calculations
* Route statistics
* Elevation analysis
* OpenStreetMap URL generation
* Batch processing
* Interactive map visualization

---

# License

MIT License

---

# Contributing

Contributions, bug reports, and feature requests are welcome.

Feel free to open an issue or submit a pull request.
