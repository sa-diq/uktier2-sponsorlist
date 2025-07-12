import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from sponsor_analytics import get_recent_sponsors, get_sponsor_stats, get_daily_additions

st.set_page_config(
    page_title="UK Sponsor License Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern CSS with contemporary design elements
st.markdown("""
<style>
    .stApp { 
        background: var(--background-color);
        font-family: 'Inter', 'Segoe UI', 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Hide sidebar on desktop only */
@media (min-width: 769px) {
    section[data-testid="stSidebar"] {
        display: none !important;
    }
}

    /* Modern Typography */
    h1 { 
        font-size: 2.75rem !important; 
        font-weight: 800 !important; 
        color: var(--text-color) !important; 
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.025em !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h2 { 
        font-size: 1.875rem !important; 
        font-weight: 700 !important; 
        color: var(--text-color) !important; 
        margin-top: 2rem !important;
        letter-spacing: -0.01em !important;
    }
    
    .block-container { 
        padding-top: 1rem !important; 
        max-width: 1200px !important;
    }

    /* Modern Filter Container */
    .filter-container {
        background: var(--background-secondary-color, #ffffff);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2.5rem;
        border: 1px solid rgba(226, 232, 240, 0.8);
        box-shadow: 
            0 1px 3px rgba(0, 0, 0, 0.06),
            0 20px 25px -5px rgba(0, 0, 0, 0.1),
            0 10px 10px -5px rgba(0, 0, 0, 0.04);
        backdrop-filter: blur(16px);
        position: relative;
        overflow: hidden;
    }
    
    .filter-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        border-radius: 20px 20px 0 0;
    }
    
    .filter-header {
        font-size: 1.375rem !important;
        font-weight: 700 !important;
        color: var(--text-color) !important;
        margin-bottom: 1.5rem !important;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        letter-spacing: -0.01em !important;
    }

    /* Modern Metric Cards - Force override existing styles */
    .stApp div[data-testid="metric-container"] {
        background: #ffffff !important;
        border-radius: 20px !important;
        padding: 2rem 1.5rem !important;
        margin: 0 0.75rem !important;
        border: 1px solid rgba(226, 232, 240, 0.8) !important;
        box-shadow: 
            0 4px 6px -1px rgba(0, 0, 0, 0.1) !important,
            0 20px 25px -5px rgba(0, 0, 0, 0.1) !important,
            0 10px 10px -5px rgba(0, 0, 0, 0.04) !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
        transform: translateY(0px) scale(1) !important;
    }
    
    .stApp div[data-testid="metric-container"]::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 5px !important;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%) !important;
        border-radius: 20px 20px 0 0 !important;
    }
    
    .stApp div[data-testid="metric-container"]:hover {
        transform: translateY(-12px) scale(1.03) !important;
        box-shadow: 
            0 25px 50px -12px rgba(102, 126, 234, 0.25) !important,
            0 20px 25px -5px rgba(0, 0, 0, 0.15) !important;
        border-color: rgba(102, 126, 234, 0.4) !important;
    }
    
    .stApp div[data-testid="metric-container"] .stMetricLabel {
        font-size: 1.125rem !important;
        font-weight: 700 !important;
        color: #64748b !important;
        margin-bottom: 0.75rem !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
        font-family: 'Inter', 'Segoe UI', sans-serif !important;
    }
    
    .stApp div[data-testid="metric-container"] .stMetricValue {
        font-size: 2.5rem !important;
        font-weight: 900 !important;
        color: #1e293b !important;
        font-family: 'Inter', 'Segoe UI', sans-serif !important;
        letter-spacing: -0.025em !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }

    /* Modern Button Styling */
    .filter-container button {
        background: var(--background-secondary-color, #ffffff) !important;
        border: 1.5px solid rgba(226, 232, 240, 0.8) !important;
        border-radius: 12px !important;
        padding: 0.875rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
        margin: 0.375rem !important;
        letter-spacing: 0.025em !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .filter-container button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        transition: left 0.6s ease;
    }
    
    .filter-container button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15) !important;
        border-color: rgba(102, 126, 234, 0.4) !important;
        background: rgba(102, 126, 234, 0.02) !important;
    }
    
    .filter-container button:hover::before {
        left: 100%;
    }
    
    .filter-container button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-color: transparent !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    }
    
    .filter-container button[data-testid="baseButton-primary"]:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.5) !important;
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%) !important;
    }

    /* Modern Form Elements */
    .filter-container div[data-baseweb="select"],
    .filter-container .stSelectbox > div > div,
    .filter-container .stMultiSelect > div > div {
        border-radius: 12px !important;
        border: 1.5px solid rgba(226, 232, 240, 0.8) !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .filter-container div[data-baseweb="select"]:focus-within,
    .filter-container .stSelectbox > div > div:focus-within,
    .filter-container .stMultiSelect > div > div:focus-within {
        border-color: rgba(102, 126, 234, 0.6) !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    .filter-container .stSlider {
        background: var(--background-secondary-color, #ffffff);
        border-radius: 12px;
        padding: 1rem;
        border: 1.5px solid rgba(226, 232, 240, 0.8);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }

    /* Modern Expander Styling */
    .filter-container details {
        border: 1.5px solid rgba(226, 232, 240, 0.8);
        border-radius: 12px;
        margin-bottom: 1rem;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .filter-container details:hover {
        border-color: rgba(102, 126, 234, 0.3);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
    }
    
    .filter-container details summary {
        padding: 1rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        background: rgba(248, 250, 252, 0.8);
        border-bottom: 1px solid rgba(226, 232, 240, 0.8);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .filter-container details[open] summary {
        background: rgba(102, 126, 234, 0.05);
        color: #5a67d8;
    }

    /* Chart Styling */
    .js-plotly-plot .gtitle {
        text-align: center !important;
        justify-content: center !important;
        width: 100% !important;
        display: flex !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em !important;
    }
    .js-plotly-plot .gtitle > text {
        text-anchor: middle !important;
    }

    /* Enhanced Mobile Responsiveness */
    @media (max-width: 900px) {
        h1 { font-size: 2.25rem !important; }
        h2 { font-size: 1.5rem !important; }
        .block-container { padding-top: 0.5rem !important; }
        .filter-container { 
            padding: 1.5rem; 
            margin-bottom: 2rem; 
            border-radius: 16px;
        }
        div[data-testid="metric-container"] {
            padding: 1.5rem 1rem !important;
            margin: 0.25rem !important;
            border-radius: 16px;
        }
    }
    
    @media (max-width: 700px) {
        .filter-container {
            padding: 1.25rem;
            margin-bottom: 1.5rem;
            border-radius: 16px;
        }
        div[data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
        }
        div[data-testid="stHorizontalBlock"] > div {
            margin-bottom: 1rem;
        }
        div[data-testid="metric-container"] {
            min-width: 0 !important;
            width: 100% !important;
            margin: 0.5rem 0 !important;
            border-radius: 16px;
        }
        .block-container {
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
        }
        .js-plotly-plot {
            min-width: 320px !important;
            overflow-x: auto !important;
        }
        h1 { font-size: 2rem !important; }
    }
</style>
""", unsafe_allow_html=True)

# Title section
st.title("📊 UK Sponsor License Tracker")
st.write("Track companies with UK sponsor licenses for work visas")

# ===== FILTERS SECTION =====
st.markdown('<div class="filter-container">', unsafe_allow_html=True)
st.markdown('<div class="filter-header">🔍 Filters & Options</div>', unsafe_allow_html=True)

# Get initial data for filter options
initial_sponsors = get_recent_sponsors(days=90)
available_cities = sorted(initial_sponsors['town_city'].unique().tolist())
available_routes = sorted(initial_sponsors['route'].unique().tolist())

# Create responsive filter layout
filter_col1, filter_col2, filter_col3 = st.columns([1, 1, 1])

with filter_col1:
    with st.expander("📅 Date Range", expanded=True):
        days_filter = st.slider("Show Sponsors Added in Last X Days", 1, 90, 30)

with filter_col2:
    with st.expander("🏢 Location", expanded=False):
        city_filter = st.multiselect("Filter by City", available_cities, key="city_filter")

with filter_col3:
    with st.expander("🛂 Visa Routes", expanded=False):
        route_filter = st.multiselect("Filter by Visa Route", available_routes, key="route_filter")

# Additional options row
options_col1, options_col2 = st.columns([1, 1])

with options_col1:
    with st.expander("📊 View Options", expanded=False):
        time_period = st.radio("Time Aggregation", ["Daily", "Weekly", "Monthly"], horizontal=True)

with options_col2:
    with st.expander("ℹ️ About", expanded=False):
        st.write("Data updates weekdays at 8 AM UTC")
        st.write("Source: GOV.UK Register of Licensed Sponsors")

st.markdown('</div>', unsafe_allow_html=True)

# ===== GET FILTERED DATA =====
recent_sponsors = get_recent_sponsors(days=days_filter)

# Apply filters
filtered_sponsors = recent_sponsors
if route_filter:
    filtered_sponsors = filtered_sponsors[filtered_sponsors['route'].isin(route_filter)]
if city_filter:
    filtered_sponsors = filtered_sponsors[filtered_sponsors['town_city'].isin(city_filter)]

# ===== STATS SECTION =====
stats = get_sponsor_stats()

# Update stats based on filters
if city_filter or route_filter:
    stats['total_sponsors'] = len(filtered_sponsors)
    stats['recent_additions_7d'] = len(filtered_sponsors[
        filtered_sponsors['first_appeared_date'] >= (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    ])

# Metrics Cards Row
cols = st.columns(3, gap="medium")
with cols[0]:
    st.metric("Total", f"{stats['total_sponsors']:,}", help="Total number of companies with active sponsor licenses")
with cols[1]:
    st.metric("New (7d)", f"{stats['recent_additions_7d']:,}", help="New sponsors added in the last 7 days")
with cols[2]:
    st.metric("Updated", datetime.now().strftime("%Y-%m-%d"), help="Data last refreshed on this date")

# ===== CHARTS SECTION =====

# Daily additions chart
daily_additions = get_daily_additions()

if not daily_additions.empty:
    cutoff_date = (datetime.now() - timedelta(days=days_filter)).strftime("%Y-%m-%d")
    daily_additions = daily_additions[daily_additions['date'] >= cutoff_date]
    daily_additions['date'] = pd.to_datetime(daily_additions['date'])

    if time_period == "Weekly":
        chart_data = daily_additions.resample('W', on='date').sum().reset_index()
        title = "Weekly New Sponsors"
    elif time_period == "Monthly":
        chart_data = daily_additions.resample('M', on='date').sum().reset_index()
        title = "Monthly New Sponsors"
    else:
        chart_data = daily_additions
        title = "Daily New Sponsors"

    fig1 = px.line(
        chart_data, x='date', y='added_count', title=title,
        template="plotly" if st.get_option("theme.base") == "light" else "plotly_dark",
        line_shape="spline", markers=True,
        labels={"date": "Date", "added_count": "Number of Companies"}
    )

    fig1.update_traces(line_color='#667eea', marker_color='#667eea')
    fig1.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        title_font_size=24, title_x=0.5, showlegend=False,
        margin=dict(t=80, l=50, r=30, b=50),
        xaxis=dict(tickformat="%d %b", dtick=5 * 86400000, showgrid=True, gridcolor="rgba(128,128,128,0.1)"),
        yaxis=dict(showgrid=True, gridcolor="rgba(128,128,128,0.1)", title="Number of Companies")
    )
    st.plotly_chart(fig1, use_container_width=True)

# Top Cities Treemap
if not filtered_sponsors.empty:
    recent_top_cities = filtered_sponsors['town_city'].value_counts().reset_index()
    recent_top_cities.columns = ['town_city', 'count']
    recent_top_cities = recent_top_cities.head(10)

    fig2 = px.treemap(
        recent_top_cities, path=['town_city'], values='count',
        title=f"Top 10 Cities (New Sponsors in Last {days_filter} Days)",
        template="plotly" if st.get_option("theme.base") == "light" else "plotly_dark",
        color='count', color_continuous_scale='Viridis'
    )

    fig2.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        title={
            'text': f"Top 10 Cities (New Sponsors in Last {days_filter} Days)",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 24}
        },
        margin=dict(t=80, l=10, r=10, b=10)
    )
    fig2.update_traces(textinfo="label+value", hovertemplate="<b>%{label}</b><br>New Sponsors: %{value}<extra></extra>")
    st.plotly_chart(fig2, use_container_width=True)

# Footer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("Data Source: [GOV.UK Register of Licensed Sponsors](https://www.gov.uk/government/publications/register-of-licensed-sponsors-workers)")