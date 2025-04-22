import pandas as pd
import sqlite3
from datetime import datetime
import os
from db_utils import setup_database

def clean_csv_data(csv_file):
    """Clean and prepare the CSV data."""
    df = pd.read_csv(csv_file)

    # Fill NaN values with empty strings
    df = df.fillna('')

    # Clean city names
    if 'Town/City' in df.columns:
        df['Town/City'] = df['Town/City'].str.replace(r'[^a-zA-Z\s]', '', regex=True).str.strip().str.title()
    

    return df

def process_daily_update(csv_file):
    """Process the daily update and update the database."""
    today = datetime.now().strftime("%Y-%m-%d")

    # Ensure database exists
    conn = setup_database()

    # Clean and prepare the CSV data
    df_new = clean_csv_data(csv_file)

    print(f"Total entries in new data: {len(df_new)}")

    # Get existing data from database
    try:
        df_existing = pd.read_sql("SELECT * FROM sponsor_register", conn)
        print(f"Existing entries in database: {len(df_existing)}")
    except Exception as e:
        print(f"Error reading existing data: {str(e)}")
        # If table doesn't exist or is empty
        df_existing = pd.DataFrame(columns=['organisation_name', 'route'])
        print("Created empty DataFrame for existing data")

    # Create a composite key for comparison
    def create_composite_key(df, org_col, route_col):
        return df[org_col].astype(str) + '|' + df[route_col].astype(str)

    if not df_existing.empty:
        df_new['composite_key'] = create_composite_key(df_new, 'Organisation Name', 'Route')
        df_existing['composite_key'] = create_composite_key(df_existing, 'organisation_name', 'route')

        # Find new entries (in new but not in existing)
        new_entries = df_new[~df_new['composite_key'].isin(df_existing['composite_key'])]
        print(f"New entries identified: {len(new_entries)}")

        # Find removed entries (in existing but not in new)
        removed_entries = df_existing[~df_existing['composite_key'].isin(df_new['composite_key'])]
        print(f"Removed entries identified: {len(removed_entries)}")

        # Drop the temporary composite key
        new_entries = new_entries.drop(columns=['composite_key'])
        removed_entries = removed_entries.drop(columns=['composite_key'])
        df_new = df_new.drop(columns=['composite_key'])
        df_existing = df_existing.drop(columns=['composite_key'])
    else:
        new_entries = df_new
        removed_entries = pd.DataFrame()
        print("No existing data, treating all as new entries")

    # Prepare new entries for database insertion
    if not new_entries.empty:
        # Rename columns to match database schema
        new_entries_db = new_entries.rename(columns={
            'Organisation Name': 'organisation_name',
            'Town/City': 'town_city',
            'County': 'county',
            'Type & Rating': 'type_rating',
            'Route': 'route'
        })

        # Add tracking dates
        new_entries_db['first_appeared_date'] = today
        new_entries_db['last_updated_date'] = today

        # Instead of using to_sql, let's insert records one by one with proper error handling
        cursor = conn.cursor()
        inserted_count = 0
        error_count = 0

        for _, row in new_entries_db.iterrows():
            try:
                cursor.execute("""
                INSERT INTO sponsor_register
                (organisation_name, town_city, county, type_rating, route, first_appeared_date, last_updated_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    row['organisation_name'],
                    row['town_city'],
                    row['county'],
                    row['type_rating'],
                    row['route'],
                    row['first_appeared_date'],
                    row['last_updated_date']
                ))
                inserted_count += 1
            except sqlite3.IntegrityError as e:
                error_count += 1
                print(f"Error inserting: {row['organisation_name']} - {row['route']}: {str(e)}")
                # If it's a duplicate, update instead
                try:
                    cursor.execute("""
                    UPDATE sponsor_register
                    SET town_city = ?, county = ?, type_rating = ?, last_updated_date = ?
                    WHERE organisation_name = ? AND route = ?
                    """, (
                        row['town_city'],
                        row['county'],
                        row['type_rating'],
                        today,
                        row['organisation_name'],
                        row['route']
                    ))
                except Exception as update_error:
                    print(f"Error updating: {str(update_error)}")

        print(f"Inserted {inserted_count} new entries, encountered {error_count} errors")

    # Update last_updated_date for existing entries
    cursor = conn.cursor()
    update_count = 0
    for _, row in df_new.iterrows():
        try:
            cursor.execute(
                """
                UPDATE sponsor_register
                SET last_updated_date = ?
                WHERE organisation_name = ? AND route = ?
                """,
                (today, row['Organisation Name'], row['Route'])
            )
            if cursor.rowcount > 0:
                update_count += 1
        except Exception as e:
            print(f"Error updating last_updated_date: {str(e)}")

    print(f"Updated last_updated_date for {update_count} existing entries")

    # Log daily changes
    try:
        cursor.execute(
            "INSERT OR REPLACE INTO daily_updates (date, added_count, removed_count) VALUES (?, ?, ?)",
            (today, len(new_entries), len(removed_entries))
        )
        print(f"Logged daily changes: {len(new_entries)} added, {len(removed_entries)} removed")
    except Exception as e:
        print(f"Error logging daily changes: {str(e)}")

    conn.commit()
    conn.close()

    # Save processed data for reference
    os.makedirs('data/processed', exist_ok=True)
    if not new_entries.empty:
        new_entries.to_csv(f'data/processed/new_sponsors_{today}.csv', index=False)

    return {
        'date': today,
        'new_entries': len(new_entries),
        'removed_entries': len(removed_entries)
    }