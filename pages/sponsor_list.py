import streamlit as st
from sponsor_analytics import get_recent_sponsors
from datetime import datetime

st.set_page_config(
    page_title="Sponsor List",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: var(--background-color);
    }
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
    .block-container {
        padding-top: 1rem !important;
    }
    section[data-testid="stSidebar"] {
        background-color: var(--background-secondary-color);
        border-right: 1px solid rgba(59, 70, 122, 0.2);
        padding-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Update title with icon and Title Case
st.title("📋 Sponsor List")

# Get data
recent_sponsors = get_recent_sponsors(days=90)  # Show last 90 days by default

# Update sidebar with icons and sections
st.sidebar.markdown("### 📋 Sponsor List")
st.sidebar.markdown("---")

st.sidebar.markdown("### 🔍 Filters")
with st.sidebar:
    with st.expander("Location", expanded=True):
        city_filter = st.multiselect("🏢 Filter by City", options=sorted(recent_sponsors['town_city'].unique()))

    with st.expander("Visa Routes", expanded=True):
        route_filter = st.multiselect("🛂 Filter by Visa Route", options=sorted(recent_sponsors['route'].unique()))

# Apply filters
filtered_sponsors = recent_sponsors
if city_filter:
    filtered_sponsors = filtered_sponsors[filtered_sponsors['town_city'].isin(city_filter)]
if route_filter:
    filtered_sponsors = filtered_sponsors[filtered_sponsors['route'].isin(route_filter)]

# Display table
if not filtered_sponsors.empty:
    st.info("💡 Select and copy company names to search")
    sorted_sponsors = filtered_sponsors.sort_values('first_appeared_date', ascending=False)
    st.dataframe(
        sorted_sponsors[['organisation_name', 'town_city', 'type_rating', 'route', 'first_appeared_date']],
        use_container_width=True,
        hide_index=True,
        height=700
    )
else:
    st.write("No sponsors found matching your criteria.")
