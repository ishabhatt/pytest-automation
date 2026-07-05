import csv
from pathlib import Path


class DataReader:
    @staticmethod
    def load_csv_data(filename) -> list:
        """
        Load test data from a CSV file located in the 'testdata/' directory.
        Returns a list of dictionaries, one per row.
        """
        root_dir = Path(__file__).resolve().parent.parent
        data_file = root_dir / "testdata" / filename
        with open(data_file, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            return list(reader)
