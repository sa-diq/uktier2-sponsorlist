import os
import sys
from datetime import datetime

# Import your modules
from fetch_sponsor_data import download_sponsor_register
from process_sponsor_data import process_daily_update

def run_daily_pipeline():
    """Run the complete daily pipeline."""
    print(f"=== Starting daily pipeline: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")

    try:
        # Step 1: Download the latest data
        print("Step 1: Downloading latest sponsor data...")
        csv_file = download_sponsor_register()
        if not csv_file:
            print("Failed to download data. Exiting pipeline.")
            return False

        # Step 2: Process the data and update the database
        print("Step 2: Processing data and updating database...")
        results = process_daily_update(csv_file)

        print(f"Pipeline completed successfully.")
        print(f"Date: {results['date']}")
        print(f"New sponsors: {results['new_entries']}")
        print(f"Removed sponsors: {results['removed_entries']}")

        return True

    except Exception as e:
        print(f"Error in pipeline: {str(e)}")
        return False

if __name__ == "__main__":
    success = run_daily_pipeline()
    sys.exit(0 if success else 1)