# Mass Transit Billing System

## Overview

Calculates user bills for a mass transit system based on journey data, applying zone-based pricing and daily/monthly caps

## Task Requirements

1. Produce production-quality code with tests
2. Take command line arguments for input/output files
3. Calculate total charge for each customer's transit journeys
4. Apply pricing rules:

- £2 base fee per journey
- Additional zone-based costs:

Zone 1: £0.80
Zones 2-3: £0.50
Zones 4-5: £0.30
Zone 6+: £0.10

- £5 fee for erroneous journeys
- Daily cap: £15
- Monthly cap: £100

## Requirements

- Python 3.7+
- pytest (for testing)

## Usage

```
python main.py <zones_file_path> <journey_data_path> <output_file_path>
```

Example:

```
python main.py zone_map.csv journey_data.csv billing_results.csv
```

## Testing

Run tests with:

```
pytest tests.py
```

### Test Descriptions

1. `test_read_zone_map`: Validates correct reading of zone map from CSV
2. `test_read_zone_map_invalid_data`: Checks handling of invalid zone data
3. `test_read_journey_data`: Verifies correct reading of journey data
4. `test_read_journey_data_invalid_station`: Tests handling of unknown stations
5. `test_calculate_journey_cost`: Checks journey cost calculations for various zones
6. `test_daily_cap`: Ensures daily spending cap (£15) is applied correctly
7. `test_monthly_cap`: Verifies monthly spending cap (£100) is applied correctly
8. `test_incomplete_journey`: Checks application of incomplete journey fee (£5)
9. `test_cross_midnight_journey`: Verifies handling of journeys spanning midnight
10. `test_export_billing_results`: Checks correct formatting of billing results CSV

## Assumptions

- Valid journeys completed before midnight
- £2 base fee per journey
- £5 fee for incomplete journeys
- Daily cap: £15, Monthly cap: £100
- Input data is chronologically sorted
