from data_ingestion import read_csv
from processing import calculate_monthly_statistics, write_monthly_stats
from outlier_detection import detect_outliers, write_outliers
from error_handling import log_error

def main():
    try:
        # Read sensor data and thresholds
        sensor_data = read_csv("../data/sensor_data.csv")
        thresholds_data = read_csv("../data/thresholds.csv")

        # Convert thresholds to dictionary
        thresholds = {row["sensor_type"]: {"min_threshold": float(row["min_threshold"]), "max_threshold": float(row["max_threshold"])}
                      for row in thresholds_data}

        # Process monthly statistics
        stats = calculate_monthly_statistics(sensor_data)
        write_monthly_stats(stats, "../data/monthly_stats.csv")

        # Detect and log outliers
        outliers = detect_outliers(sensor_data, thresholds)
        write_outliers(outliers, "../data/outliers.csv")

        print("Processing completed successfully!")

    except Exception as e:
        log_error("ERR003", str(e))
        print("An error occurred. Check logs for details.")

if __name__ == "__main__":
    main()
