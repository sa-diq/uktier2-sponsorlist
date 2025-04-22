import sqlite3
import os
import pandas as pd

def setup_database():
    os.makedirs('data/db', exist_ok=True)
    conn = sqlite3.connect('data/db/sponsor_register.db')
    cursor = conn.cursor()

    # Create a table for the sponsor register
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sponsor_register(               
                   organisation_name TEXT,
                   town_city TEXT,
                   county TEXT,
                   type_rating TEXT,
                   route TEXT,
                   first_appeared_date DATE,
                   last_updated_date DATE,
                   PRIMARY KEY (organisation_name, route)
                   )
    ''')

    # Create daily update table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS daily_updates(
                   date DATE PRIMARY KEY,
                   added_count INTEGER,
                   removed_count INTEGER
                   )
''')
    
    conn.commit()
    return conn