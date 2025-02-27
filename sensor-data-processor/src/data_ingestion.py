import pandas as pd
import os
from error_handling import log_error

DATA_PATH = r"C:\Users\ShreyaSwain\OneDrive - Atyeti Inc\Desktop\sensor-data-processor\data"

EXPECTED_COLUMNS = {
    "sensor_data.csv": {"date", "sensor_type", "value", "unit", "location_id"},
    "thresholds.csv": {"sensor_type", "min_threshold", "max_threshold"},
}

def read_csv(filename):
    """Reads a CSV file and validates its format and content."""
    file_path = os.path.join(DATA_PATH, filename)

    try:
        df = pd.read_csv(file_path)

        #Checking required columns
        expected_cols = EXPECTED_COLUMNS.get(filename, set())
        if not expected_cols.issubset(df.columns):
            log_error("ERR002", f"Invalid columns in {filename}. Expected: {expected_cols}, Found: {df.columns}")
            return None
        
        #Checking for missing values
        if df.isnull().sum().sum() > 0:
            log_error("ERR002", f"Missing values found in {filename}")
            return None

        #Validating numeric columns
        if filename == "sensor_data.csv":
            if not pd.api.types.is_numeric_dtype(df["value"]):
                log_error("ERR002", f"Invalid data type in 'value' column of {filename}")
                return None
        elif filename == "thresholds.csv":
            if not all(pd.api.types.is_numeric_dtype(df[col]) for col in ["min_threshold", "max_threshold"]):
                log_error("ERR002", f"Invalid data type in 'min_threshold' or 'max_threshold' of {filename}")
                return None

        #Validating date format for sensor_data.csv
        if filename == "sensor_data.csv":
            try:
                pd.to_datetime(df["date"], format="%Y-%m-%d", errors="raise")
            except ValueError:
                log_error("ERR002", f"Invalid date format in {filename}. Expected YYYY-MM-DD.")
                return None

        return df

    except FileNotFoundError:
        log_error("ERR001", f"File not found: {file_path}")
        return None
    except pd.errors.ParserError:
        log_error("ERR002", f"Invalid data format in {filename}")
        return None

#Loading sensor data & thresholds
sensor_data = read_csv("sensor_data.csv")
thresholds = read_csv("thresholds.csv")

#Printing it for debugging
if sensor_data is not None:
    print(sensor_data.head())
if thresholds is not None:
    print(thresholds.head())
