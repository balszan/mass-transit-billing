import csv
from typing import Dict

def export_billing_results(results: Dict[str, float], output_file: str):
    """
    Export billing results to a CSV file

    Args:
    results (Dict[str, float]): Dictionary with user IDs as keys and total bills as values
    output_file (str): Path to the output CSV file

    Raises:
    IOError: If there's an error writing to the file
    """
    try:
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['user_id', 'total_bill']) 
            for user_id, total_bill in sorted(results.items()):
                writer.writerow([user_id, f'{total_bill:.2f}'])
        print(f"Billing results exported to {output_file}")
    except IOError as e:
        raise IOError(f"Error writing to output file: {e}")