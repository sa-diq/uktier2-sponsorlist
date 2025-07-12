import streamlit as st
from sponsor_analytics import get_recent_sponsors
from datetime import datetime

st.set_page_config(
    page_title="Sponsor List",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern CSS matching the dashboard design
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

# Title
st.title("Sponsor List")

# Get data
recent_sponsors = get_recent_sponsors(days=90)

# Modern search container
st.markdown('<div class="search-container">', unsafe_allow_html=True)
search_query = st.text_input("Company Search", value="", placeholder="🔍 Search for a company name...", 
                           help="Type to search for a sponsor company name", label_visibility="hidden")
st.markdown('</div>', unsafe_allow_html=True)

# ===== FILTERS SECTION =====
st.markdown('<div class="filter-container">', unsafe_allow_html=True)
st.markdown('<div class="filter-header">🔍 Search & Filter Options</div>', unsafe_allow_html=True)

# Filter options in columns
filter_col1, filter_col2 = st.columns([1, 1])

with filter_col1:
    with st.expander("🏢 Location", expanded=True):
        city_filter = st.multiselect("Filter by City", options=sorted(recent_sponsors['town_city'].unique()))

with filter_col2:
    with st.expander("🛂 Visa Routes", expanded=True):
        route_filter = st.multiselect("Filter by Visa Route", options=sorted(recent_sponsors['route'].unique()))

st.markdown('</div>', unsafe_allow_html=True)

# Apply filters
filtered_sponsors = recent_sponsors
if city_filter:
    filtered_sponsors = filtered_sponsors[filtered_sponsors['town_city'].isin(city_filter)]
if route_filter:
    filtered_sponsors = filtered_sponsors[filtered_sponsors['route'].isin(route_filter)]

table_df = filtered_sponsors.copy()
if search_query:
    table_df = table_df[table_df['organisation_name'].str.contains(search_query, case=False, na=False)]

# Modern results summary
if search_query or city_filter or route_filter:
    st.markdown(f'<div class="results-summary"> Showing {len(table_df):,} sponsors (filtered from {len(recent_sponsors):,} total)</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="results-summary"> Showing {len(table_df):,} sponsors</div>', unsafe_allow_html=True)

# Display table
if not table_df.empty:
    sorted_sponsors = table_df.sort_values('first_appeared_date', ascending=False)
    st.dataframe(
        sorted_sponsors[['organisation_name', 'town_city', 'type_rating', 'route', 'first_appeared_date']],
        use_container_width=True,
        hide_index=True,
        height=650,
        column_config={
            "organisation_name": st.column_config.TextColumn("Company Name", width="large"),
            "town_city": st.column_config.TextColumn("City", width="medium"),
            "type_rating": st.column_config.TextColumn("Type & Rating", width="medium"),
            "route": st.column_config.TextColumn("Visa Route", width="medium"),
            "first_appeared_date": st.column_config.DateColumn("First Appeared", width="small")
        }
    )
else:
    st.warning("⚠️ No sponsors found matching your criteria. Try adjusting your filters.")

# Footer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("Data source: [GOV.UK Register of Licensed Sponsors](https://www.gov.uk/government/publications/register-of-licensed-sponsors-workers)")