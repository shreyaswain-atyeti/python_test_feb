'''import csv

# File paths
SENSOR_DATA_FILE = "../data/sensor_data.csv"
THRESHOLDS_FILE = "../data/thresholds.csv"
OUTLIERS_FILE = "../data/outliers.csv"

def load_thresholds(thresholds_file):
    """Reads thresholds from CSV and returns a dictionary."""
    thresholds = {}

    try:
        with open(thresholds_file, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                sensor_type = row["sensor_type"]
                try:
                    min_threshold = float(row["min_threshold"])
                    max_threshold = float(row["max_threshold"])
                    thresholds[sensor_type] = (min_threshold, max_threshold)
                except ValueError:
                    print(f"Warning: Invalid threshold values for {sensor_type}, skipping...")
    except FileNotFoundError:
        print(f"Error: File {thresholds_file} not found.")
        exit(1)

    return thresholds

def detect_outliers(sensor_data_file, thresholds, output_file):
    """Identifies outliers based on thresholds and writes them to a CSV file."""
    outliers = []

    try:
        with open(sensor_data_file, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                sensor_type = row["sensor_type"]
                try:
                    value = float(row["value"])
                except ValueError:
                    continue  # to skip invalid values

                # Checking if sensor type has defined thresholds
                if sensor_type in thresholds:
                    min_threshold, max_threshold = thresholds[sensor_type]

                    # Identify outliers
                    if value < min_threshold:
                        row["threshold_exceeded"] = "Min"
                        outliers.append(row)
                    elif value > max_threshold:
                        row["threshold_exceeded"] = "Max"
                        outliers.append(row)

        # Removing 'month' field from each row before writing to outliers.csv
        for row in outliers:
            row.pop("month", None)  # Removes 'month' key if it exists

        # Writing outliers to CSV
        with open(output_file, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["date", "sensor_type", "value", "unit", "location_id", "threshold_exceeded"])
            writer.writeheader()
            writer.writerows(outliers)

        print(f"Outliers saved to: {output_file}")

    except FileNotFoundError:
        print(f"Error: File {sensor_data_file} not found.")
        exit(1)

# Main execution
if __name__ == "__main__":
    thresholds = load_thresholds(THRESHOLDS_FILE)
    detect_outliers(SENSOR_DATA_FILE, thresholds, OUTLIERS_FILE)
'''

import csv

# File paths
SENSOR_DATA_FILE = "../data/sensor_data.csv"
THRESHOLDS_FILE = "../data/thresholds.csv"
OUTLIERS_FILE = "../data/outliers.csv"

def load_thresholds(thresholds_file):
    """Reads thresholds from CSV and returns a dictionary."""
    thresholds = {}

    try:
        with open(thresholds_file, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                sensor_type = row["sensor_type"]
                try:
                    min_threshold = float(row["min_threshold"])
                    max_threshold = float(row["max_threshold"])
                    thresholds[sensor_type] = (min_threshold, max_threshold)
                except ValueError:
                    print(f"Warning: Invalid threshold values for {sensor_type}, skipping...")
    except FileNotFoundError:
        print(f"Error: File {thresholds_file} not found.")
        exit(1)

    return thresholds

def detect_outliers(sensor_data_file, thresholds):
    """Identifies outliers based on thresholds and returns them."""
    outliers = []

    try:
        with open(sensor_data_file, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                sensor_type = row["sensor_type"]
                try:
                    value = float(row["value"])
                except ValueError:
                    continue  # Skip invalid values

                # Checking if sensor type has defined thresholds
                if sensor_type in thresholds:
                    min_threshold, max_threshold = thresholds[sensor_type]

                    # Identify outliers
                    if value < min_threshold:
                        row["threshold_exceeded"] = "Min"
                        outliers.append(row)
                    elif value > max_threshold:
                        row["threshold_exceeded"] = "Max"
                        outliers.append(row)

        # Removing 'month' field from each row before writing to outliers.csv
        for row in outliers:
            row.pop("month", None)  # Removes 'month' key if it exists

    except FileNotFoundError:
        print(f"Error: File {sensor_data_file} not found.")
        exit(1)

    return outliers  # Return the detected outliers instead of writing them

def write_outliers(outliers, output_file):
    """Writes detected outliers to a CSV file."""
    if not outliers:
        print("No outliers detected.")
        return

    with open(output_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["date", "sensor_type", "value", "unit", "location_id", "threshold_exceeded"])
        writer.writeheader()
        writer.writerows(outliers)

    print(f"Outliers saved to: {output_file}")

# Main execution
if __name__ == "__main__":
    thresholds = load_thresholds(THRESHOLDS_FILE)
    outliers = detect_outliers(SENSOR_DATA_FILE, thresholds)
    write_outliers(outliers, OUTLIERS_FILE)
