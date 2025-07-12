# app.py - Fixed mobile navigation
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

# Create the navigation with top position
pg = st.navigation(pages, position="top")

# Fixed CSS with proper mobile navigation support
st.markdown("""
<style>
/* Hide the default sidebar on desktop only - allow it on mobile */
@media (min-width: 769px) {
    section[data-testid="stSidebar"] {
        display: none !important;
    }
}

/* On mobile, ensure the sidebar navigation is properly styled when visible */
@media (max-width: 768px) {
    section[data-testid="stSidebar"] {
        background: var(--background-secondary-color, #f8f9fa) !important;
    }
    
    /* Style the sidebar navigation on mobile */
    section[data-testid="stSidebar"] nav[data-testid="stSidebarNav"] {
        background: var(--background-secondary-color, #f8f9fa) !important;
        border-radius: 12px !important;
        margin: 1rem !important;
        border: 1px solid rgba(60,70,130,0.1) !important;
        box-shadow: 0 2px 8px rgba(30, 34, 90, 0.05) !important;
        padding: 0.5rem !important;
    }
    
    /* Ensure navigation items are properly sized on mobile */
    section[data-testid="stSidebar"] nav[data-testid="stSidebarNav"] a {
        padding: 0.75rem 1rem !important;
        margin: 0.25rem 0 !important;
        border-radius: 8px !important;
        font-size: 1rem !important;
    }
}

/* Style the top navigation on desktop */
@media (min-width: 769px) {
    nav[data-testid="stSidebarNav"] {
        background: var(--background-secondary-color, #f8f9fa) !important;
        border-radius: 12px !important;
        margin-bottom: 2rem !important;
        border: 1px solid rgba(60,70,130,0.1) !important;
        box-shadow: 0 2px 8px rgba(30, 34, 90, 0.05) !important;
        padding: 0.5rem !important;
    }
}

/* Ensure the mobile menu button is visible and functional */
@media (max-width: 768px) {
    button[data-testid="collapsedControl"] {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        background: var(--background-secondary-color, #f8f9fa) !important;
        border: 1px solid rgba(60,70,130,0.2) !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
        margin: 0.5rem !important;
    }
}

/* Style the main content area properly on mobile */
@media (max-width: 768px) {
    .main .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-top: 1rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

# Run the selected page
pg.run()