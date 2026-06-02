import csv
import os
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from urllib.parse import quote_plus


class KmlRouteParser:
    """
    Parse KML/KMZ files and generate Google Maps URLs.
    """

    KML_NS = {
        "kml": "http://www.opengis.net/kml/2.2"
    }

    def __init__(self, file_path):
        self.file_path = file_path
        self.points = []

    def load(self):
        """
        Load points from KML/KMZ.
        """

        self.points = self._parse_points(
            self.file_path
        )

        return self.points

    def get_points(self):
        """
        Return loaded points.
        """

        return self.points

    def get_google_maps_url(
        self,
        use_names=True
    ):
        """
        Generate Google Maps directions URL.
        """

        if len(self.points) < 2:
            raise ValueError(
                "Need at least two points."
            )

        locations = []

        for point in self.points:

            if use_names:

                if point["name"].strip():

                    locations.append(
                        quote_plus(
                            point["name"]
                        )
                    )

                else:

                    locations.append(
                        f"{point['latitude']},"
                        f"{point['longitude']}"
                    )

            else:

                locations.append(
                    f"{point['latitude']},"
                    f"{point['longitude']}"
                )

        return (
            "https://www.google.com/maps/dir/"
            + "/".join(locations)
            + "/data=!4m2!4m1!3e0"
        )

    def save_csv(
        self,
        filename
    ):
        """
        Export points to CSV.
        """

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as csvfile:

            writer = csv.writer(
                csvfile
            )

            writer.writerow([
                "Name",
                "Latitude",
                "Longitude",
                "Description"
            ])

            for point in self.points:

                writer.writerow([
                    point["name"],
                    point["latitude"],
                    point["longitude"],
                    point["description"]
                ])

    @staticmethod
    def _extract_kml_from_kmz(
        kmz_file
    ):
        """
        Extract KML from KMZ.
        """

        with zipfile.ZipFile(
            kmz_file,
            "r"
        ) as kmz:

            kml_files = [
                f
                for f in kmz.namelist()
                if f.lower().endswith(
                    ".kml"
                )
            ]

            if not kml_files:
                raise ValueError(
                    f"No KML found in {kmz_file}"
                )

            temp_file = (
                tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".kml"
                )
            )

            temp_file.write(
                kmz.read(kml_files[0])
            )

            temp_file.close()

            return temp_file.name

    def _parse_points(
        self,
        input_file
    ):

        temp_kml = None

        try:

            ext = os.path.splitext(
                input_file
            )[1].lower()

            if ext == ".kmz":

                temp_kml = (
                    self._extract_kml_from_kmz(
                        input_file
                    )
                )

                kml_file = temp_kml

            elif ext == ".kml":

                kml_file = input_file

            else:

                raise ValueError(
                    "Only KML and KMZ files are supported."
                )

            tree = ET.parse(
                kml_file
            )

            root = tree.getroot()

            points = []

            for placemark in root.findall(
                ".//kml:Placemark",
                self.KML_NS
            ):

                name = (
                    placemark.findtext(
                        "kml:name",
                        default="Unnamed",
                        namespaces=self.KML_NS
                    )
                )

                description = (
                    placemark.findtext(
                        "kml:description",
                        default="",
                        namespaces=self.KML_NS
                    )
                )

                coord_node = (
                    placemark.find(
                        ".//kml:Point/kml:coordinates",
                        self.KML_NS
                    )
                )

                if coord_node is None:
                    continue

                lon, lat, *_ = (
                    coord_node.text
                    .strip()
                    .split(",")
                )

                points.append({
                    "name": name,
                    "description": description,
                    "latitude": float(lat),
                    "longitude": float(lon)
                })

            return points

        finally:

            if (
                temp_kml
                and os.path.exists(
                    temp_kml
                )
            ):
                os.remove(
                    temp_kml
                )
