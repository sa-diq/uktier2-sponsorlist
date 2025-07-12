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

/* Hide sidebar on desktop only */
@media (min-width: 769px) {
    section[data-testid="stSidebar"] {
        display: none;
    }
}

/* Basic typography improvements */
h1 { 
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    color: #1e293b;
}

h2 { 
    font-size: 1.75rem;
    font-weight: 600;
    margin-top: 2rem;
    color: #334155;
}

/* Container spacing */
.block-container { 
    padding-top: 1rem;
    max-width: 1200px;
}

/* Simple card styling */
.filter-container {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 2rem;
    border: 1px solid #e2e8f0;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* Clean metric cards */
div[data-testid="metric-container"] {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    border: 1px solid #e2e8f0;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* Simple button styling */
button {
    border-radius: 6px;
    font-weight: 500;
    transition: all 0.2s ease;
}

button:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Mobile responsiveness - one clean breakpoint */
@media (max-width: 768px) {
    h1 { font-size: 2rem; }
    h2 { font-size: 1.5rem; }
    
    .filter-container {
        padding: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
}
</style>
""", unsafe_allow_html=True)

# Title section
st.title("UK Sponsor License Tracker")
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

# with options_col2:
#     with st.expander("ℹ️ About", expanded=False):
#         st.write("Data updates weekdays at 8 AM UTC")
#         st.write("Source: GOV.UK Register of Licensed Sponsors")

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
if not recent_sponsors.empty:
    recent_top_cities = recent_sponsors['town_city'].value_counts().reset_index()
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

# Contact
st.markdown("""
<div style="text-align: center; margin-top: 2rem; padding: 1rem;">
    <p style="margin-bottom: 0.5rem; font-weight: 600;">Built by: Sadiq Balogun</p>
    <div style="display: flex; justify-content: center; gap: 1rem; align-items: center;">
        <a href="mailto:ballosadiq@gmail.com" style="text-decoration: none;" title="Email">
            <img src="https://img.icons8.com/?size=100&id=P7UIlhbpWzZm&format=png&color=000000" width="34" height="34"/>
        </a>
        <a href="https://linkedin.com/in/sadiq-balogun" target="_blank" style="text-decoration: none;" title="LinkedIn">
            <img src="https://img.icons8.com/?size=100&id=xuvGCOXi8Wyg&format=png&color=000000" width="34" height="34"/>
        </a>
    </div>
</div>
""", unsafe_allow_html=True)
