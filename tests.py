import pytest
from datetime import datetime, timedelta
from services.zone_file_reader import read_zone_map
from services.journey_file_reader import read_journey_data
from services.billing_calculator import calculate_user_bill, calculate_journey_cost
from services.output_exporter import export_billing_results
from models.zone import Zone
from models.journey import Journey
from models.user import User

@pytest.fixture
def zone_map():
    return {
        "station1": Zone(1),
        "station2": Zone(2),
        "station3": Zone(3),
        "station4": Zone(4),
        "station5": Zone(5)
    }

@pytest.fixture
def sample_user():
    user = User("user1")
    user.add_journey(Journey("user1", "station1", "IN", datetime(2022, 1, 1, 10, 0)))
    user.add_journey(Journey("user1", "station2", "OUT", datetime(2022, 1, 1, 11, 0)))
    return user

def test_read_zone_map(tmp_path):
    zone_file = tmp_path / "zone_map.csv"
    zone_file.write_text("station,zone\nstation1,1\nstation2,2\n")
    zone_map = read_zone_map(str(zone_file))
    assert len(zone_map) == 2
    assert zone_map["station1"].number == 1
    assert zone_map["station2"].number == 2

def test_read_zone_map_invalid_data(tmp_path):
    zone_file = tmp_path / "invalid_zone_map.csv"
    zone_file.write_text("station,zone\nstation1,invalid\n")
    with pytest.raises(ValueError):
        read_zone_map(str(zone_file))

def test_read_journey_data(tmp_path, zone_map):
    journey_file = tmp_path / "journey_data.csv"
    journey_file.write_text("user_id,station,direction,time\nuser1,station1,IN,2022-01-01T10:00:00\n")
    users = read_journey_data(str(journey_file), zone_map)
    assert len(users) == 1
    assert len(users["user1"].journeys) == 1
    assert users["user1"].journeys[0].station == "station1"

def test_read_journey_data_invalid_station(tmp_path, zone_map):
    journey_file = tmp_path / "invalid_journey_data.csv"
    journey_file.write_text("user_id,station,direction,time\nuser1,invalid_station,IN,2022-01-01T10:00:00\n")
    with pytest.raises(ValueError):
        read_journey_data(str(journey_file), zone_map)

@pytest.mark.parametrize("start_zone,end_zone,expected_cost", [
    (1, 1, 3.60),  # 2.00 + 0.80 + 0.80
    (1, 2, 3.30),  # 2.00 + 0.80 + 0.50
    (1, 3, 3.30),  # 2.00 + 0.80 + 0.50
    (1, 4, 3.10),  # 2.00 + 0.80 + 0.30
    (1, 5, 3.10),  # 2.00 + 0.80 + 0.30
    (1, 6, 2.90),  # 2.00 + 0.80 + 0.10
])
def test_calculate_journey_cost(start_zone, end_zone, expected_cost):
    assert calculate_journey_cost(start_zone, end_zone) == pytest.approx(expected_cost, abs=1e-9)

def test_daily_cap(zone_map):
    user = User("user1")
    for i in range(5):
        user.add_journey(Journey("user1", "station1", "IN", datetime(2022, 1, 1, 8, i*2)))
        user.add_journey(Journey("user1", "station2", "OUT", datetime(2022, 1, 1, 9, i*2)))
    total_bill = calculate_user_bill(user, zone_map)
    assert total_bill == pytest.approx(15.00, abs=1e-9) 

def test_monthly_cap(zone_map):
    user = User("user1")
    for day in range(1, 32):
        user.add_journey(Journey("user1", "station1", "IN", datetime(2022, 1, day, 8, 0)))
        user.add_journey(Journey("user1", "station2", "OUT", datetime(2022, 1, day, 17, 0)))
    total_bill = calculate_user_bill(user, zone_map)
    assert total_bill == pytest.approx(100.00, abs=1e-9) 

def test_incomplete_journey(zone_map):
    user = User("user1")
    user.add_journey(Journey("user1", "station1", "IN", datetime(2022, 1, 1, 10, 0)))
    total_bill = calculate_user_bill(user, zone_map)
    assert total_bill == pytest.approx(5.00, abs=1e-9) 

def test_cross_midnight_journey(zone_map):
    user = User("user1")
    user.add_journey(Journey("user1", "station1", "IN", datetime(2022, 1, 1, 23, 50)))
    user.add_journey(Journey("user1", "station2", "OUT", datetime(2022, 1, 2, 0, 10)))
    total_bill = calculate_user_bill(user, zone_map)
    assert total_bill == pytest.approx(5.00, abs=1e-9) 

def test_export_billing_results(tmp_path):
    billing_results = {"user1": 10.50, "user2": 15.75}
    output_file = tmp_path / "output.csv"
    export_billing_results(billing_results, str(output_file))
    
    content = output_file.read_text().split('\n')
    assert content[0] == "user_id,total_bill"
    assert content[1] == "user1,10.50"
    assert content[2] == "user2,15.75"