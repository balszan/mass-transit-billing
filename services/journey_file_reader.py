import csv
from datetime import datetime
from typing import Dict
from models import Journey, User, Zone

def read_journey_data(file_path: str, zone_map: Dict[str, Zone]) -> Dict[str, User]:
    """
    Read journey data from a CSV file and return a dictionary of User objects

    Args:
    file_path (str): Path to the journey data CSV file
    zone_map (Dict[str, Zone]): Dictionary mapping station names to Zone objects

    Returns:
    Dict[str, User]: A dictionary with user IDs as keys and User objects as values

    Raises:
    FileNotFoundError: If the specified file is not found.
    ValueError: If the CSV file is not in the expected format or contains invalid data
    """
    users = {}
    try:
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if set(row.keys()) != {'user_id', 'station', 'direction', 'time'}:
                    raise ValueError(f"Invalid CSV header. Expected: user_id, station, direction, time")
                
                user_id = row['user_id']
                if user_id not in users:
                    users[user_id] = User(user_id)
                
                if row['station'] not in zone_map:
                    raise ValueError(f"Unknown station: {row['station']}")
                
                journey = Journey(
                    user_id=user_id,
                    station=row['station'],
                    direction=row['direction'],
                    timestamp=parse_timestamp(row['time'])
                )
                
                if journey.direction not in ['IN', 'OUT']:
                    raise ValueError(f"Invalid direction: {journey.direction}. Expected 'IN' or 'OUT'")
                
                users[user_id].add_journey(journey)
    except FileNotFoundError:
        raise FileNotFoundError(f"Journey data file not found: {file_path}")
    
    if not users:
        raise ValueError("Journey data file is empty")
    
    return users

def parse_timestamp(timestamp_str: str) -> datetime:
    """
    Parse a timestamp string into a datetime object

    Args:
    timestamp_str (str): Timestamp string in the format 'YYYY-MM-DDTHH:MM:SS'

    Returns:
    datetime: Parsed datetime object

    Raises:
    ValueError: If the timestamp string is not in the expected format
    """
    try:
        return datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        raise ValueError(f"Invalid timestamp format: {timestamp_str}. Expected format: YYYY-MM-DDTHH:MM:SS")