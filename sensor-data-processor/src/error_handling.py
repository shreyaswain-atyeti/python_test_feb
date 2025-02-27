import logging
import os

# Ensure logs directory exists
LOG_DIR = "../logs"
LOG_FILE = os.path.join(LOG_DIR, "errors.log")
os.makedirs(LOG_DIR, exist_ok=True)  # Create logs folder if missing

# Set up logging
logging.basicConfig(filename=LOG_FILE, level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

# Error messages mapping
ERROR_MESSAGES = {
    "ERR001": "File not found",
    "ERR002": "Invalid data format",
    "ERR003": "Processing error",
    "ERR004": "Thresholds not defined",
}

def log_error(error_code, details=""):
    """Logs errors with error code, message, and additional details."""
    message = ERROR_MESSAGES.get(error_code, "Unknown error")
    log_entry = f"{error_code}: {message}. {details}" if details else f"{error_code}: {message}"
    logging.error(log_entry)
    print(f"Error Logged: {log_entry}")

# Example usage
if __name__ == "__main__":
    log_error("ERR001", "File 'sensor_data.csv' is missing.")
    log_error("ERR002", "Sensor values contain non-numeric data.")
    log_error("ERR003", "Failed to compute monthly statistics due to division by zero.")
    log_error("ERR004", "Thresholds not found for sensor type 'CO2'.")
