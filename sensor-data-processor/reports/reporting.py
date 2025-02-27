import csv

# File paths
MONTHLY_STATS_FILE = "../data/monthly_stats.csv"
OUTLIERS_FILE = "../data/outliers.csv"
REPORTS_MONTHLY_STATS = "../reports/monthly_stats_report.csv"
REPORTS_OUTLIERS = "../reports/outliers_report.csv"

def generate_report(source_file, report_file):
    """Copies data from source CSV to the reports directory."""
    try:
        with open(source_file, mode="r", newline="") as file:
            reader = csv.reader(file)
            data = list(reader)  # Read all data
            
            if len(data) == 0:
                print(f"Warning: {source_file} is empty. No data to report.")
                return

        with open(report_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data)  # Copy content to report file

        print(f"Report generated: {report_file}")

    except FileNotFoundError:
        print(f"Error: {source_file} not found. Report not generated.")

if __name__ == "__main__":
    print("Generating Reports...")
    generate_report(MONTHLY_STATS_FILE, REPORTS_MONTHLY_STATS)
    generate_report(OUTLIERS_FILE, REPORTS_OUTLIERS)
    print("Reports successfully created in the 'reports' folder.")
