# app.py - New main application file
import streamlit as st

# Set page config first
st.set_page_config(
    page_title="UK Sponsor License Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Define the pages for navigation
pages = [
    st.Page("pages/sponsor_dashboard.py", title="Dashboard", icon="📊"),
    st.Page("pages/sponsor_list.py", title="Sponsor List", icon="📋")
]

# Create the navigation with top position - this is the new Streamlit 1.46.0 feature!
pg = st.navigation(pages, position="top")

# Custom CSS to style the top navigation
st.markdown("""
<style>
/* Hide the default sidebar since we're using top navigation */
section[data-testid="stSidebar"] {
    display: none !important;
}

/* Style the top navigation */
nav[data-testid="stSidebarNav"] {
    background: var(--background-secondary-color, #f8f9fa) !important;
    border-radius: 12px !important;
    margin-bottom: 2rem !important;
    border: 1px solid rgba(60,70,130,0.1) !important;
    box-shadow: 0 2px 8px rgba(30, 34, 90, 0.05) !important;
    padding: 0.5rem !important;
}

/* Mobile responsiveness */
@media (max-width: 700px) {
    nav[data-testid="stSidebarNav"] {
        margin-bottom: 1rem !important;
        padding: 0.25rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

# Run the selected page
pg.run()