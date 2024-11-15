import csv
from typing import Dict
from models import Zone

def read_zone_map(file_path: str) -> Dict[str, Zone]:
    """
    Read the zone map from a CSV file and return a dictionary mapping stations to zones

    Args:
    file_path (str): Path to the zone map CSV file

    Returns:
    Dict[str, Zone]: A dictionary with station names as keys and Zone objects as values

    Raises:
    FileNotFoundError: If the specified file is not found.
    ValueError: If the CSV file is not in the expected format or contains invalid data
    """
    zone_map = {}
    try:
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader) 
            for row in reader:
                if len(row) != 2:
                    raise ValueError(f"Invalid row in zone map file: {row}")
                station_name, zone_number = row
                try:
                    zone_map[station_name] = Zone(int(zone_number))
                except ValueError:
                    raise ValueError(f"Invalid zone number for station {station_name}: {zone_number}")
    except FileNotFoundError:
        raise FileNotFoundError(f"Zone map file not found: {file_path}")
    
    if not zone_map:
        raise ValueError("Zone map file is empty")
    
    return zone_map