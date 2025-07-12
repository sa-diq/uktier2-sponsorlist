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
    .stApp {
        background: var(--background-color);
        font-family: 'Inter', 'Segoe UI', 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide sidebar */
    section[data-testid="stSidebar"] {
        display: none !important;
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

    /* Modern Search Box */
    .search-container {
        background: var(--background-secondary-color, #ffffff);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(226, 232, 240, 0.8);
        box-shadow: 
            0 1px 3px rgba(0, 0, 0, 0.06),
            0 10px 15px -3px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .search-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px 16px 0 0;
    }
    
    /* Search input styling */
    .search-container div[data-testid="stTextInput"] > label {
        display: none;
    }
    
    .search-container div[data-testid="stTextInput"] input {
        border: 2px solid rgba(226, 232, 240, 0.8) !important;
        border-radius: 12px !important;
        padding: 1rem 1.5rem !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        background: var(--background-secondary-color, #fff) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
    }
    
    .search-container div[data-testid="stTextInput"] input:focus {
        border: 2px solid #667eea !important;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1) !important;
        transform: translateY(-1px) !important;
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

    /* Modern Results Summary */
    .results-summary {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin-bottom: 1.5rem;
        font-weight: 600;
        color: #5a67d8;
        font-size: 1.1rem;
    }

    /* Modern Table Styling */
    .dataframe {
        border-radius: 16px !important;
        overflow: hidden !important;
        border: 1px solid rgba(226, 232, 240, 0.8) !important;
        background: var(--background-secondary-color, #ffffff) !important;
        box-shadow: 
            0 1px 3px rgba(0, 0, 0, 0.06),
            0 20px 25px -5px rgba(0, 0, 0, 0.1),
            0 10px 10px -5px rgba(0, 0, 0, 0.04) !important;
    }
    
    .dataframe th {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
        padding: 1.25rem 1.5rem !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        color: #475569 !important;
        border-bottom: 2px solid rgba(102, 126, 234, 0.1) !important;
    }
    
    .dataframe td {
        padding: 1rem 1.5rem !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        border-bottom: 1px solid rgba(226, 232, 240, 0.5) !important;
        transition: all 0.2s ease !important;
    }
    
    .dataframe tr:hover td {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.02) 0%, rgba(118, 75, 162, 0.02) 100%) !important;
        transform: scale(1.001) !important;
    }
    
    .dataframe tr:nth-child(even) td {
        background: rgba(248, 250, 252, 0.5) !important;
    }

    /* Warning styling */
    .stAlert > div {
        background: linear-gradient(135deg, rgba(251, 146, 60, 0.05) 0%, rgba(251, 191, 36, 0.05) 100%) !important;
        border: 1px solid rgba(251, 146, 60, 0.2) !important;
        border-radius: 12px !important;
        padding: 1rem 1.5rem !important;
    }

    /* Mobile responsiveness */
    @media (max-width: 900px) {
        h1 { font-size: 2.25rem !important; }
        .block-container { padding-top: 0.5rem !important; }
        .filter-container { 
            padding: 1.5rem; 
            margin-bottom: 2rem; 
            border-radius: 16px;
        }
        .search-container {
            padding: 1.25rem;
            margin-bottom: 1.5rem;
            border-radius: 16px;
        }
    }
    
    @media (max-width: 700px) {
        .filter-container {
            padding: 1.25rem;
            margin-bottom: 1.5rem;
            border-radius: 16px;
        }
        .search-container {
            padding: 1rem;
            border-radius: 12px;
        }
        .block-container {
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
        }
        h1 { font-size: 2rem !important; }
        .dataframe th {
            padding: 1rem !important;
            font-size: 0.85rem !important;
        }
        .dataframe td {
            padding: 0.875rem !important;
            font-size: 0.875rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("📋 Sponsor List")

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
    st.markdown(f'<div class="results-summary">📊 Showing {len(table_df):,} sponsors (filtered from {len(recent_sponsors):,} total)</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="results-summary">📊 Showing {len(table_df):,} sponsors</div>', unsafe_allow_html=True)

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