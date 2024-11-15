from typing import List
from .journey import Journey

class User:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.journeys: List[Journey] = []

    def add_journey(self, journey: Journey):
        self.journeys.append(journey)

    def get_journeys(self) -> List[Journey]:
        return sorted(self.journeys, key=lambda j: j.timestamp)