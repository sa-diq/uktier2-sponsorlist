import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from sponsor_analytics import get_recent_sponsors, get_sponsor_stats, get_daily_additions

st.set_page_config(
    page_title="UK Sponsor License Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with theme-aware colors
st.markdown("""
<style>
    /* Main theme - adapts to light/dark mode */
    .stApp {
        background: var(--background-color);
    }
    
    /* Minimal metric cards */
    [data-testid="metric-container"] {
        width: auto !important;
        min-width: 150px !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .stMetric {
        background: none !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        box-shadow: none !important;
    }
    
    [data-testid="metric-container"] > div {
        padding: 0 !important;
    }
    
    .metric-row {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        gap: 1rem;
    }
    
    /* Headers */
    h1 {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: var(--text-color) !important;
        margin-bottom: 0.5rem !important;
    }
    h2 {
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        color: var(--text-color) !important;
        margin-top: 2rem !important;
    }
    
    /* Table styling */
    .dataframe {
        border-radius: 15px !important;
        overflow: hidden !important;
        border: 1px solid var(--primary-container) !important;
        background: var(--background-secondary-color) !important;
    }
    .dataframe th {
        background: var(--background-secondary-color) !important;
        padding: 15px 20px !important;
        font-weight: 600 !important;
    }
    .dataframe td {
        padding: 12px 20px !important;
    }
    .dataframe tr:hover td {
        background-color: var(--hover-color) !important;
    }

    /* Reduce top margin and header spacing */
    .block-container {
        padding-top: 1rem !important;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: var(--background-secondary-color);
        border-right: 1px solid rgba(59, 70, 122, 0.2);
        padding-top: 1rem;
    }
    section[data-testid="stSidebar"] > div {
        padding-top: 0;
    }
    section[data-testid="stSidebar"] .element-container {
        margin-bottom: 0.5rem;
    }
    section[data-testid="stSidebar"] hr {
        margin: 0.5rem 0;
    }
    
    /* Filter section styling */
    .sidebar-filters {
        padding: 0.5rem;
        margin-top: 1rem;
        border-radius: 8px;
    }
    
    /* Clean up header spacing */
    header[data-testid="stHeader"] {
        background: none;
        border-bottom: 1px solid rgba(59, 70, 122, 0.2);
    }
    
    /* Main content padding adjustment */
    .main > div:first-of-type {
        padding-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Add custom spacing and container styling
st.markdown("""
    <style>
    /* Improved spacing and containers */
    .main-title {
        margin-bottom: 2rem !important;
    }
    .chart-section {
        margin: 2rem 0 !important;
    }
    
    /* Make charts more prominent */
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        background: linear-gradient(180deg, var(--background-secondary-color) 0%, rgba(30, 33, 48, 0.8) 100%);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 0.5rem;
        box-shadow: 
            0 10px 15px -3px rgba(0, 0, 0, 0.1),
            0 4px 6px -2px rgba(0, 0, 0, 0.05),
            0 25px 30px -5px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(128, 128, 128, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Title section with proper spacing
st.markdown('<div class="main-title">', unsafe_allow_html=True)
st.title("UK Sponsor License Tracker")
st.write("Track companies with UK sponsor licenses for work visas")
st.markdown('</div>', unsafe_allow_html=True)

# Sidebar filters with Title Case
st.sidebar.markdown("### 🏠 Dashboard")
st.sidebar.markdown("---")

st.sidebar.markdown("### 🔍 Filters")
with st.sidebar:
    with st.expander("Date Range", expanded=True):
        days_filter = st.slider("Show Sponsors Added in Last X Days", 1, 90, 30)

    # Get recent sponsors for filtering
    recent_sponsors = get_recent_sponsors(days=days_filter)
    available_cities = recent_sponsors['town_city'].unique().tolist()
    available_routes = recent_sponsors['route'].unique().tolist()

    with st.expander("Location", expanded=True):
        city_filter = st.multiselect("🏢 Filter by City", available_cities)

    with st.expander("Visa Routes", expanded=True):
        route_filter = st.multiselect("🛂 Filter by Visa Route", available_routes)

    with st.expander("View Options", expanded=True):
        time_period = st.radio(
            "📅 Time Aggregation",
            ["Daily", "Weekly", "Monthly"],
            horizontal=True
        )

# Get basic stats
stats = get_sponsor_stats()

# Apply city filter to stats if needed
if city_filter:
    filtered_sponsors = recent_sponsors[recent_sponsors['town_city'].isin(city_filter)]
    stats['total_sponsors'] = len(filtered_sponsors)
    stats['recent_additions_7d'] = len(filtered_sponsors[
        filtered_sponsors['first_appeared_date'] >= (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    ])

# Display compact metrics row
st.markdown('<div class="metric-row">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1,1,1])
with col1:
    st.metric(
        "Total",
        f"{stats['total_sponsors']:,}",
        help="Total number of companies with active sponsor licenses"
    )
with col2:
    st.metric(
        "New (7d)",
        f"{stats['recent_additions_7d']:,}",
        help="New sponsors added in the last 7 days"
    )
with col3:
    st.metric(
        "Updated",
        datetime.now().strftime("%Y-%m-%d"),
        help="Data last refreshed on this date"
    )
st.markdown('</div>', unsafe_allow_html=True)

# Apply filters
filtered_sponsors = recent_sponsors
if route_filter:
    filtered_sponsors = filtered_sponsors[filtered_sponsors['route'].isin(route_filter)]
if city_filter:
    filtered_sponsors = filtered_sponsors[filtered_sponsors['town_city'].isin(city_filter)]

# Charts section with improved layout
st.header(f"Sponsors Added in the Last {days_filter} Days")

# Daily additions chart
daily_additions = get_daily_additions()
if not daily_additions.empty:
    # Filter to last X days
    cutoff_date = (datetime.now() - timedelta(days=days_filter)).strftime("%Y-%m-%d")
    daily_additions = daily_additions[daily_additions['date'] >= cutoff_date]
    
    # Convert date column to datetime if it's not already
    daily_additions['date'] = pd.to_datetime(daily_additions['date'])
    
    # Aggregate based on selected time period
    if time_period == "Weekly":
        chart_data = daily_additions.resample('W', on='date').sum().reset_index()
        title = "Weekly New Sponsors"
    elif time_period == "Monthly":
        chart_data = daily_additions.resample('M', on='date').sum().reset_index()
        title = "Monthly New Sponsors"
    else:
        chart_data = daily_additions
        title = "Daily New Sponsors"

# 1. Line chart (full width)
if not daily_additions.empty:
    st.markdown('<div class="chart-section">', unsafe_allow_html=True)
    fig1 = px.line(
        chart_data,
        x='date',
        y='added_count',
        title=title,
        template="plotly" if st.get_option("theme.base") == "light" else "plotly_dark",
        line_shape="spline",
        markers=True,
        labels={"date": "Date", "added_count": "Number of Companies"}
    )
    
    fig1.update_traces(line_color='#3851C2', marker_color='#3851C2')
    fig1.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        title_font_size=22,
        title_x=0.5,
        showlegend=False,
        margin=dict(t=60, l=50, r=30, b=50),
        xaxis=dict(
            tickformat='%Y-%m-%d',
            dtick='D1',
            showgrid=True,
            gridcolor="rgba(128,128,128,0.1)",
            title_font_size=14,
            tickfont_size=12,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(128,128,128,0.1)",
            title="Number of Companies",
            title_font_size=14,
            tickfont_size=12,
        )
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 2. Top cities chart
if not recent_sponsors.empty:
    st.markdown('<div class="chart-section">', unsafe_allow_html=True)
    top_cities = recent_sponsors['town_city'].value_counts().reset_index()
    top_cities.columns = ['town_city', 'count']
    top_cities = top_cities.head(10)

    fig2 = px.bar(
        top_cities,
        x='town_city',
        y='count',
        title="Top 10 Cities (All Sponsors)",
        template="plotly" if st.get_option("theme.base") == "light" else "plotly_dark",
        color_discrete_sequence=['#3B467A']
    )

    fig2.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        title_font_size=22,
        title_x=0.5,
        showlegend=False,
        margin=dict(t=60, l=50, r=30, b=70),
        xaxis=dict(
            title_font_size=14,
            tickfont_size=12,
            tickangle=45,
            showgrid=False,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(128,128,128,0.1)",
            title_font_size=14,
            tickfont_size=12,
        )
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer with better spacing
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("Data source: [GOV.UK Register of Licensed Sponsors](https://www.gov.uk/government/publications/register-of-licensed-sponsors-workers)")