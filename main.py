import argparse
from tkinter import Tk, filedialog

from app.parser import (
    KmlRouteParser
)


def select_file():

    root = Tk()
    root.withdraw()

    filename = (
        filedialog.askopenfilename(
            title="Select KML/KMZ File",
            filetypes=[
                (
                    "KML/KMZ Files",
                    "*.kml *.kmz"
                ),
                (
                    "All Files",
                    "*.*"
                )
            ]
        )
    )

    root.destroy()

    if not filename:
        raise SystemExit(
            "No file selected."
        )

    return filename


def ask_csv_save_location():

    root = Tk()
    root.withdraw()

    filename = (
        filedialog.asksaveasfilename(
            title="Save CSV",
            defaultextension=".csv",
            initialfile="points.csv",
            filetypes=[
                (
                    "CSV Files",
                    "*.csv"
                )
            ]
        )
    )

    root.destroy()

    return filename or None


def ask_url_mode():

    while True:

        print(
            "\nBuild URL using:"
        )

        print(
            "1. Place Names"
        )

        print(
            "2. Coordinates"
        )

        choice = input(
            "\nSelect option (1/2): "
        )

        if choice == "1":
            return True

        if choice == "2":
            return False


def main():

    parser = argparse.ArgumentParser(
        description=(
            "KML/KMZ Route Parser"
        )
    )

    parser.add_argument(
        "file",
        nargs="?"
    )

    parser.add_argument(
        "--url-mode",
        choices=[
            "name",
            "coord"
        ]
    )

    parser.add_argument(
        "--csv"
    )

    parser.add_argument(
        "--no-csv",
        action="store_true"
    )

    args = parser.parse_args()

    file_path = (
        args.file
        if args.file
        else select_file()
    )

    parser_obj = (
        KmlRouteParser(
            file_path
        )
    )

    points = (
        parser_obj.load()
    )

    print(
        f"\nFound {len(points)} points\n"
    )

    for idx, point in enumerate(
        points,
        start=1
    ):

        print(
            f"{idx}. "
            f"{point['name']} "
            f"({point['latitude']}, "
            f"{point['longitude']})"
        )

    if args.url_mode:

        use_names = (
            args.url_mode
            == "name"
        )

    else:

        use_names = (
            ask_url_mode()
        )

    maps_url = (
        parser_obj
        .get_google_maps_url(
            use_names
        )
    )

    print(
        "\nGoogle Maps URL:"
    )

    print(
        maps_url
    )

    if args.no_csv:

        print(
            "\nCSV export disabled."
        )

    elif args.csv:

        parser_obj.save_csv(
            args.csv
        )

        print(
            f"\nCSV saved: "
            f"{args.csv}"
        )

    else:

        csv_file = (
            ask_csv_save_location()
        )

        if csv_file:

            parser_obj.save_csv(
                csv_file
            )

            print(
                f"\nCSV saved: "
                f"{csv_file}"
            )

        else:

            print(
                "\nCSV export cancelled."
            )


# https://www.google.com/maps/dir/31.242048,-85.436355/30.1957355,-90.1232442/29.7355472,-94.9775848/30.5549354,-100.8121479/30.3561191,-103.669709/32.7700697,-108.2802686/34.1333566,-109.2858713/36.0356516,-111.830458/35.25146,-112.1477502/35.1914292,-114.0522602/35.1914292,-114.0522602/34.7346559,-120.0882259/37.9318643,-121.6957932/@33.2284132,-114.291973,5z/am=t/data=!4m2!4m1!3e0?entry=ttu&g_ep=EgoyMDI2MDUyNy4wIKXMDSoASAFQAw%3D%3D
# https://www.google.com/maps/dir/31.242048,-85.436355/30.1957355,-90.1232442/29.7355472,-94.9775848/30.5549354,-100.8121479/30.3561191,-103.669709/32.7700697,-108.2802686/34.1333566,-109.2858713/36.0356516,-111.830458/35.25146,-112.1477502/35.1914292,-114.0522602/35.1914292,-114.0522602/34.7346559,-120.0882259/37.9318643,-121.6957932/@33.2284132,-114.291973,5z/data=!4m2!4m1!3e0
# https://www.google.com/maps/dir/31.242048,-85.436355/30.1957355,-90.1232442/29.7355472,-94.9775848/30.5549354,-100.8121479/30.3561191,-103.669709/32.7700697,-108.2802686/34.1333566,-109.2858713/36.0356516,-111.830458/35.25146,-112.1477502/35.1914292,-114.0522602/35.1914292,-114.0522602/34.7346559,-120.0882259/37.9318643,-121.6957932/@33.2284132,-114.291973/data=!4m2!4m1!3e0
if __name__ == "__main__":
    main()
