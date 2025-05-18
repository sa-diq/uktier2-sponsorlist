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
    .stApp { background: var(--background-color); }

    /* General Styling (Optional, from your original) */
    h1 { font-size: 2.5rem !important; font-weight: 700 !important; color: var(--text-color) !important; margin-bottom: 0.5rem !important; }
    h2 { font-size: 1.8rem !important; font-weight: 600 !important; color: var(--text-color) !important; margin-top: 2rem !important; }
    .block-container { padding-top: 1rem !important; }
    header[data-testid="stHeader"] { background: none; border-bottom: 1px solid rgba(59, 70, 122, 0.2); }
    section[data-testid="stSidebar"] { background-color: var(--background-secondary-color); border-right: 1px solid rgba(59, 70, 122, 0.2); padding-top: 1rem; }

    /* Center Plotly chart titles regardless of sidebar */
    .js-plotly-plot .gtitle {
        text-align: center !important;
        justify-content: center !important;
        width: 100% !important;
        display: flex !important;
    }
    .js-plotly-plot .gtitle > text {
        text-anchor: middle !important;
    }
</style>
""", unsafe_allow_html=True)

# Title section
st.title("UK Sponsor License Tracker")
st.write("Track companies with UK sponsor licenses for work visas")

# Sidebar filters
st.sidebar.markdown("### 🏠 Dashboard")
st.sidebar.markdown("---")
st.sidebar.markdown("###  Filters")
with st.sidebar:
    with st.expander("Date Range", expanded=True):
        days_filter = st.slider("Show Sponsors Added in Last X Days", 1, 90, 30)

    recent_sponsors = get_recent_sponsors(days=days_filter)
    available_cities = recent_sponsors['town_city'].unique().tolist()
    available_routes = recent_sponsors['route'].unique().tolist()

    with st.expander("Location", expanded=True):
        city_filter = st.multiselect("🏢 Filter by City", available_cities)

    with st.expander("Visa Routes", expanded=True):
        route_filter = st.multiselect("🛂 Filter by Visa Route", available_routes)

    with st.expander("View Options", expanded=True):
        time_period = st.radio("📅 Time Aggregation", ["Daily", "Weekly", "Monthly"], horizontal=True)

# Stats
stats = get_sponsor_stats()

# Apply city filter to stats
if city_filter:
    filtered_sponsors = recent_sponsors[recent_sponsors['town_city'].isin(city_filter)]
    stats['total_sponsors'] = len(filtered_sponsors)
    stats['recent_additions_7d'] = len(filtered_sponsors[
        filtered_sponsors['first_appeared_date'] >= (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    ])

# Custom CSS for Metrics Cards Row
st.markdown("""
<style>
div[data-testid="stHorizontalBlock"] > div {
    padding: 0 !important;
}
div[data-testid="metric-container"] {
    background: var(--background-secondary-color, #f7f8fa);
    border-radius: 16px;
    padding: 1rem 0.6rem;
    margin: 0 0.15rem;
    box-shadow: 0 6px 24px rgba(30, 34, 90, 0.13), 0 2px 8px rgba(30, 34, 90, 0.08);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border: 1px solid rgba(60,70,130,0.07);
    transition: box-shadow 0.18s cubic-bezier(.4,0,.2,1), transform 0.18s cubic-bezier(.4,0,.2,1);
    transform: translateY(-4px) scale(1.025);
}
div[data-testid="metric-container"]:hover {
    /* No further lift, just keep the same as default */
    box-shadow: 0 6px 24px rgba(30, 34, 90, 0.13), 0 2px 8px rgba(30, 34, 90, 0.08);
    transform: translateY(-4px) scale(1.025);
}
div[data-testid="metric-container"] .stMetricLabel {
    font-size: 1.05rem !important;
    font-weight: 500 !important;
    color: #3a4266 !important;
    margin-bottom: 0.18rem;
    letter-spacing: 0.01em;
    font-family: 'Segoe UI', 'Inter', 'Roboto', Arial, sans-serif !important;
}
div[data-testid="metric-container"] .stMetricValue {
    font-size: 1.7rem !important;
    font-weight: 700 !important;
    color: #2531a4 !important;
    font-family: 'Segoe UI', 'Inter', 'Roboto', Arial, sans-serif !important;
}
@media (max-width: 900px) {
    div[data-testid="metric-container"] {
        padding: 0.7rem 0.3rem;
    }
}
@media (max-width: 700px) {
    div[data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
    }
    div[data-testid="stHorizontalBlock"] > div {
        margin-bottom: 0.7rem;
    }
}
</style>
""", unsafe_allow_html=True)

# Metrics Cards Row (no custom div, just st.columns)
cols = st.columns(3, gap="small")
with cols[0]:
    st.metric("Total", f"{stats['total_sponsors']:,}", help="Total number of companies with active sponsor licenses")
with cols[1]:
    st.metric("New (7d)", f"{stats['recent_additions_7d']:,}", help="New sponsors added in the last 7 days")
with cols[2]:
    st.metric("Updated", datetime.now().strftime("%Y-%m-%d"), help="Data last refreshed on this date")

# Apply filters
filtered_sponsors = recent_sponsors
if route_filter:
    filtered_sponsors = filtered_sponsors[filtered_sponsors['route'].isin(route_filter)]
if city_filter:
    filtered_sponsors = filtered_sponsors[filtered_sponsors['town_city'].isin(city_filter)]

# Charts section

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

    fig1.update_traces(line_color='#3851C2', marker_color='#3851C2')
    fig1.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        title_font_size=22, title_x=0.5, showlegend=False,
        margin=dict(t=60, l=50, r=30, b=50),
        xaxis=dict(tickformat="%d %b", dtick=5 * 86400000, showgrid=True, gridcolor="rgba(128,128,128,0.1)"),
        yaxis=dict(showgrid=True, gridcolor="rgba(128,128,128,0.1)", title="Number of Companies")
    )
    st.plotly_chart(fig1, use_container_width=True)

# Top Cities Treemap
if not recent_sponsors.empty:
    recent_top_cities = filtered_sponsors['town_city'].value_counts().reset_index()
    recent_top_cities.columns = ['town_city', 'count']
    recent_top_cities = recent_top_cities.head(10)

    fig2 = px.treemap(
        recent_top_cities, path=['town_city'], values='count',
        title=f"Top 10 Cities (New Sponsors in Last {days_filter} Days)",
        template="plotly" if st.get_option("theme.base") == "light" else "plotly_dark",
        color='count', color_continuous_scale='Blues'
    )

    fig2.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        title_font_size=22, title_x=0.5, margin=dict(t=60, l=10, r=10, b=10)
    )
    fig2.update_traces(textinfo="label+value", hovertemplate="<b>%{label}</b><br>New Sponsors: %{value}<extra></extra>")
    st.plotly_chart(fig2, use_container_width=True)

# Footer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("Data source: [GOV.UK Register of Licensed Sponsors](https://www.gov.uk/government/publications/register-of-licensed-sponsors-workers)")