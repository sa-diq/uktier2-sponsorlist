import pandas as pd
import sqlite3
from datetime import datetime, timedelta

def get_connection():
    """Get a connection to the database."""
    return sqlite3.connect('data/db/sponsor_register.db')

def get_recent_sponsors(days=30):
    """Get sponsors added in the last X days."""
    conn = get_connection()
    cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    query = f"""
    SELECT * FROM sponsor_register
    WHERE first_appeared_date >= '{cutoff_date}'
    ORDER BY first_appeared_date DESC
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df

def get_sponsor_stats():
    """Get basic statistics about the sponsors database."""
    conn = get_connection()

    # Total sponsors
    total = pd.read_sql("SELECT COUNT(*) as count FROM sponsor_register", conn).iloc[0]['count']

    # Recent additions (last 30 days)
    cutoff_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    recent = pd.read_sql(
        f"SELECT COUNT(*) as count FROM sponsor_register WHERE first_appeared_date >= '{cutoff_date}'",
        conn
    ).iloc[0]['count']

    # Top cities
    cities = pd.read_sql(
        "SELECT town_city, COUNT(*) as count FROM sponsor_register GROUP BY town_city ORDER BY count DESC LIMIT 10",
        conn
    ).to_dict(orient='records')

    # Sponsors by route
    routes = pd.read_sql(
        "SELECT route, COUNT(*) as count FROM sponsor_register GROUP BY route ORDER BY count DESC",
        conn
    ).to_dict(orient='records')

    conn.close()

    return {
        'total_sponsors': total,
        'recent_additions': recent,
        'top_cities': cities,
        'sponsor_routes': routes
    }

def get_daily_additions():
    """Get the count of daily additions over time."""
    conn = get_connection()

    query = """
    SELECT date, added_count FROM daily_updates
    ORDER BY date
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df