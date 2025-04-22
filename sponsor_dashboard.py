import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from sponsor_analytics import get_recent_sponsors, get_sponsor_stats, get_daily_additions

st.set_page_config(
    page_title="UK Sponsor License Tracker",
    page_icon="📊",
    layout="wide"
)

st.title("UK Sponsor License Tracker")
st.write("Track companies with UK sponsor licenses for work visas")

# Get basic stats
stats = get_sponsor_stats()

# Display key metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Licensed Sponsors", stats['total_sponsors'])
col2.metric("Recent Additions (30 days)", stats['recent_additions'])

# Get today's date and format it
today = datetime.now().strftime("%Y-%m-%d")
col3.metric("Last Updated", today)

# Sidebar filters
st.sidebar.header("Filters")
days_filter = st.sidebar.slider("Show sponsors added in the last X days", 1, 90, 30)

# Get data based on filters
recent_sponsors = get_recent_sponsors(days=days_filter)

# Route filter
available_routes = recent_sponsors['route'].unique().tolist()
route_filter = st.sidebar.multiselect("Filter by visa route", available_routes)

# City filter
available_cities = recent_sponsors['town_city'].unique().tolist()
city_filter = st.sidebar.multiselect("Filter by city", available_cities)

# Apply filters
filtered_sponsors = recent_sponsors
if route_filter:
    filtered_sponsors = filtered_sponsors[filtered_sponsors['route'].isin(route_filter)]
if city_filter:
    filtered_sponsors = filtered_sponsors[filtered_sponsors['town_city'].isin(city_filter)]

# Display charts
st.header(f"Sponsors Added in the Last {days_filter} Days")

# Daily additions chart
daily_additions = get_daily_additions()
if not daily_additions.empty:
    # Filter to last X days
    cutoff_date = (datetime.now() - timedelta(days=days_filter)).strftime("%Y-%m-%d")
    daily_additions = daily_additions[daily_additions['date'] >= cutoff_date]

    fig1 = px.bar(
        daily_additions,
        x='date',
        y='added_count',
        title="Daily New Sponsors"
    )
    st.plotly_chart(fig1, use_container_width=True)

# Top cities chart
if not filtered_sponsors.empty:
    top_cities = filtered_sponsors['town_city'].value_counts().reset_index()
    top_cities.columns = ['town_city', 'count']
    top_cities = top_cities.head(10)

    fig2 = px.bar(
        top_cities,
        x='town_city',
        y='count',
        title="Top Cities (Recent Sponsors)"
    )
    st.plotly_chart(fig2, use_container_width=True)

# Display the data table
st.header("Recent Sponsors")
if not filtered_sponsors.empty:
    st.dataframe(
        filtered_sponsors[['organisation_name', 'town_city', 'county', 'type_rating', 'route', 'first_appeared_date']]
    )
else:
    st.write("No sponsors found matching your criteria.")

# Footer
st.markdown("---")
st.markdown("Data source: [GOV.UK Register of Licensed Sponsors](https://www.gov.uk/government/publications/register-of-licensed-sponsors-workers)")