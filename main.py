import sys
from services.zone_file_reader import read_zone_map
from services.journey_file_reader import read_journey_data
from services.billing_calculator import calculate_user_bill
from services.output_exporter import export_billing_results

def main(zones_file: str, journeys_file: str, output_file: str):
    try:
        # Read zone map
        zone_map = read_zone_map(zones_file)
        print("Zone map loaded successfully.")
        
        # Read journey data
        users = read_journey_data(journeys_file, zone_map)
        print(f"Journey data loaded successfully. Total users: {len(users)}")
        
        # Calculate bills for each user
        billing_results = {}
        for user_id, user in users.items():
            total_bill = calculate_user_bill(user, zone_map)
            billing_results[user_id] = total_bill
        
        # Export results to output file
        export_billing_results(billing_results, output_file)
        
    except (FileNotFoundError, ValueError, IOError) as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python main.py <zones_file_path> <journey_data_path> <output_file_path>")
        sys.exit(1)
    
    zones_file, journeys_file, output_file = sys.argv[1], sys.argv[2], sys.argv[3]
    main(zones_file, journeys_file, output_file)