import csv
from collections import defaultdict
import os

# Define the correct path for the output file
OUTPUT_FILE = "../data/monthly_stats.csv"

def calculate_monthly_statistics(sensor_data):
    """Calculates unique monthly average, max, and min values for each sensor type."""
    stats = defaultdict(lambda: {"count": 0, "total": 0, "max": float('-inf'), "min": float('inf')})

    for row in sensor_data:
        month = row["date"][:7]  # Extract YYYY-MM
        sensor_type = row["sensor_type"]
        
        try:
            value = float(row["value"])  # Convert value to float
        except ValueError:
            continue  # Skip rows with invalid numerical values
        
        stats[(sensor_type, month)]["count"] += 1
        stats[(sensor_type, month)]["total"] += value
        stats[(sensor_type, month)]["max"] = max(stats[(sensor_type, month)]["max"], value)
        stats[(sensor_type, month)]["min"] = min(stats[(sensor_type, month)]["min"], value)

    return stats

def write_monthly_stats(stats, output_file):
    """Writes unique monthly statistics to a CSV file under the 'data' folder."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)  # Ensure 'data' directory exists

    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["sensor_type", "month", "avg_value", "max_value", "min_value"])  # CSV Header

        for (sensor_type, month), data in stats.items():
            if data["count"] > 0:  # Avoid division by zero
                avg_value = data["total"] / data["count"]
                writer.writerow([sensor_type, month, round(avg_value, 2), data["max"], data["min"]])

# Example usage
if __name__ == "__main__":
    input_file = "../data/sensor_data.csv"

    # Read data from sensor_data.csv
    sensor_data = []
    try:
        with open(input_file, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                sensor_data.append(row)
    except FileNotFoundError:
        print(f"Error: File {input_file} not found.")
        exit(1)

    stats = calculate_monthly_statistics(sensor_data)
    write_monthly_stats(stats, OUTPUT_FILE)

    print(f"Monthly statistics saved to: {OUTPUT_FILE}")
