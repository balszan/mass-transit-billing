from typing import Dict
from models.user import User
from models.zone import Zone
from datetime import date

BASE_FEE = 2.00
ZONE_COSTS = {1: 0.80, 2: 0.50, 3: 0.50, 4: 0.30, 5: 0.30}
DEFAULT_ZONE_COST = 0.10
INCOMPLETE_JOURNEY_FEE = 5.00
DAILY_CAP = 15.00
MONTHLY_CAP = 100.00

def calculate_journey_cost(start_zone: int, end_zone: int) -> float:
    """
    Calculate the cost of a journey

    Args:
    start_zone (int): The zone number at entry
    end_zone (int): The zone number at exit

    Returns:
    float: Cost of the journey
    """
    start_cost = ZONE_COSTS.get(start_zone, DEFAULT_ZONE_COST)
    end_cost = ZONE_COSTS.get(end_zone, DEFAULT_ZONE_COST)
    return BASE_FEE + start_cost + end_cost

def calculate_user_bill(user: User, zone_map: Dict[str, Zone]) -> float:
    """
    Calculate the total bill for a user based on all their journeys

    Args:
    user (User): The user object containing the user's journeys
    zone_map (Dict[str, Zone]): Dictionary mapping station names to zone objects

    Returns:
    float: The total bill for the user after applying daily and monthly caps
    """
    daily_totals = {}
    monthly_totals = {}
    current_journey = None

    for journey in user.get_journeys():
        journey_date = journey.timestamp.date()
        journey_month = journey.timestamp.strftime("%Y-%m")

        if journey.direction == 'IN':
            if current_journey:
                # Incomplete journey ('IN' journey when there's already a current_journey)
                apply_cost(daily_totals, monthly_totals, current_journey.timestamp.date(), 
                           current_journey.timestamp.strftime("%Y-%m"), INCOMPLETE_JOURNEY_FEE)
            current_journey = journey
        elif journey.direction == 'OUT':
            if current_journey and current_journey.timestamp.date() == journey_date:
                # Complete journey
                start_zone = zone_map[current_journey.station].number
                end_zone = zone_map[journey.station].number
                cost = calculate_journey_cost(start_zone, end_zone)
                apply_cost(daily_totals, monthly_totals, journey_date, journey_month, cost)
            else:
                # Incomplete journey ('OUT' journey when there's no current_journey or when the current_journey is from a different date)
                apply_cost(daily_totals, monthly_totals, journey_date, journey_month, INCOMPLETE_JOURNEY_FEE)
            current_journey = None

    # Any remaining incomplete journey
    if current_journey:
        last_date = current_journey.timestamp.date()
        last_month = current_journey.timestamp.strftime("%Y-%m")
        apply_cost(daily_totals, monthly_totals, last_date, last_month, INCOMPLETE_JOURNEY_FEE)

    return sum(monthly_totals.values())

def apply_cost(daily_totals: Dict[date, float], monthly_totals: Dict[str, float], 
               journey_date: date, journey_month: str, cost: float):
    """
    Apply the cost of a journey to daily and monthly totals (also applying caps)

    Args:
    daily_totals (Dict[date, float]): Dictionary of daily totals
    monthly_totals (Dict[str, float]): Dictionary of monthly totals
    journey_date (date): The date of the journey
    journey_month (str): The month of the journey (format: "YYYY-MM")
    cost (float): The cost to apply
    """
    # Apply daily cap
    current_daily_total = daily_totals.get(journey_date, 0)
    new_daily_total = min(current_daily_total + cost, DAILY_CAP)
    daily_totals[journey_date] = new_daily_total

    # Calculate the actual cost added to the daily total
    actual_cost_added = new_daily_total - current_daily_total

    # Apply monthly cap
    current_monthly_total = monthly_totals.get(journey_month, 0)
    new_monthly_total = min(current_monthly_total + actual_cost_added, MONTHLY_CAP)
    monthly_totals[journey_month] = new_monthly_total