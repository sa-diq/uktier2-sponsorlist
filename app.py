# app.py - Debug version to identify mobile navigation issues
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

# Minimal CSS that doesn't interfere with navigation functionality
st.markdown("""
<style>
/* Temporary debug styles - remove all navigation hiding */
/* Let's see what elements are actually present on mobile */

/* Add visible borders to help identify navigation elements */
nav[data-testid="stSidebarNav"] {
    border: 2px solid red !important;
    background: yellow !important;
}

section[data-testid="stSidebar"] {
    border: 2px solid blue !important;
    background: lightblue !important;
}

button[data-testid="collapsedControl"] {
    border: 3px solid green !important;
    background: lightgreen !important;
    min-height: 50px !important;
    min-width: 50px !important;
}

/* Style any navigation elements that might be at the top */
[data-testid="stHeader"] {
    border: 2px solid purple !important;
    background: lavender !important;
}

/* Look for any navigation containers */
div[data-testid*="nav"] {
    border: 2px solid orange !important;
    background: lightyellow !important;
}

/* Mobile-specific debugging */
@media (max-width: 768px) {
    body::before {
        content: "MOBILE VIEW ACTIVE";
        position: fixed;
        top: 0;
        left: 0;
        background: red;
        color: white;
        padding: 10px;
        z-index: 9999;
        font-weight: bold;
    }
}

/* Desktop-specific debugging */
@media (min-width: 769px) {
    body::before {
        content: "DESKTOP VIEW ACTIVE";
        position: fixed;
        top: 0;
        left: 0;
        background: green;
        color: white;
        padding: 10px;
        z-index: 9999;
        font-weight: bold;
    }
}
</style>
""", unsafe_allow_html=True)

# Run the selected page
pg.run()