from datetime import datetime

class Journey:
    def __init__(self, user_id: str, station: str, direction: str, timestamp: datetime):
        self.user_id = user_id
        self.station = station
        self.direction = direction
        self.timestamp = timestamp