import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Config
st.set_page_config(
    page_title="Fraud Guard Mobile", 
    page_icon="📱", 
    layout="wide", 
    initial_sidebar_state="auto"
)

# --- SESSION STATE INITIALIZATION ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    
# Initialize Dark Mode State
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# --- CALLBACKS & FUNCTIONS ---
def login_user():
    st.session_state.logged_in = True
    st.rerun()

def logout_user():
    st.session_state.logged_in = False
    st.rerun()

def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode

# --- CSS STYLING ---
custom_css = """
<style>
    /* --- SIDEBAR STYLING --- */
    /* Hide the standard radio button circle */
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
        display: none;
    }
    
    /* MENU ITEMS */
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label {
        padding: 15px 20px;      
        margin-bottom: 8px;
        border-radius: 8px;
        border: none;
        width: 100%;
        cursor: pointer;
        font-size: 16px;         
        transition: background-color 0.2s;
    }
    
    /* Hover Effect */
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:hover {
        background-color: rgba(150, 150, 150, 0.1);
    }
    
    /* Active State */
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
        background-color: rgba(150, 150, 150, 0.2); 
        font-weight: 600;
        border-left: 4px solid #ff4b4b; 
    }

    /* --- MOBILE SPECIFIC TWEAKS --- */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    
    .stButton > button {
        width: 100%;             
        border-radius: 8px;
        height: 3em;
    }
    
    .footer-button > button {
        background-color: transparent;
        border: none;
        color: #888;
        font-size: 14px;
        text-align: left;
        width: auto;             
        height: auto;
        padding-left: 0;
    }
    .footer-button > button:hover {
        color: #ff4b4b;
        text-decoration: underline;
        background-color: transparent;
    }
</style>
"""

# DARK MODE OVERRIDES
if st.session_state.dark_mode:
    custom_css += """
<style>
    /* 1. Force Main Background to Dark */
    [data-testid="stAppViewContainer"], .stApp {
        background-color: #0E1117 !important; 
        color: #FAFAFA !important;
    }
    
    /* 2. Force Sidebar to slightly lighter Dark */
    [data-testid="stSidebar"] {
        background-color: #262730 !important; 
    }
    
    /* 3. Fix Header (Top bar) */
    [data-testid="stHeader"] {
        background-color: #0E1117 !important;
    }
    
    /* 4. Fix Input Fields (Text inputs) */
    div[data-baseweb="input"] > div, .stTextInput > div > div > input {
        color: white !important;
        background-color: #262730 !important;
    }
    
    /* 5. Fix Buttons (Dark background, white text) */
    .stButton > button {
        background-color: #262730 !important;
        color: white !important;
        border: 1px solid #4A4A4A !important;
    }
    .stButton > button:hover {
        border-color: #ff4b4b !important;
        color: #ff4b4b !important;
    }
    
    /* 6. Fix General Text */
    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: #FAFAFA !important;
    }
    
    /* 7. FIX EXPANDER (System Status) */
    /* Target the details/summary elements specifically */
    div[data-testid="stExpander"] details {
        background-color: #262730 !important;
        border-color: #4A4A4A !important;
        color: #FAFAFA !important;
    }
    div[data-testid="stExpander"] summary {
        background-color: #262730 !important;
        color: #FAFAFA !important; 
    }
    div[data-testid="stExpander"] summary:hover {
        color: #ff4b4b !important;
    }
    
    /* 8. FIX DATAFRAME (Table) */
    /* Since we can't change the theme prop dynamically, we visually invert the table */
    [data-testid="stDataFrame"] {
        filter: invert(1) hue-rotate(180deg);
    }
</style>
"""

# Inject the combined CSS
st.markdown(custom_css, unsafe_allow_html=True)


# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🛡️ Fraud Guard")
    
    if st.session_state.logged_in:
        menu_options = ["🏠 Home", "📊 Dashboard", "⚡ Velocity", "🌍 Maps", "⚙️ Settings"]
    else:
        menu_options = ["🏠 Home", "🔐 Login"]
        
    selected_menu = st.radio(
        "Navigation", 
        menu_options, 
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    if st.session_state.logged_in:
        st.caption("User: **Analyst**")
        st.markdown('<div class="footer-button">', unsafe_allow_html=True)
        if st.button("↪ Log out"):
            logout_user()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.caption("Status: **Guest**")


# --- MAIN CONTENT LOGIC ---

# 1. PUBLIC PAGE
if selected_menu == "🏠 Home":
    st.title("Fraud Guard")
    
    with st.expander("ℹ️ System Status", expanded=True):
        st.markdown("""
        * **API Gateway:** ✅ Online
        * **Risk Engine:** ✅ Active
        * **Database:** ✅ Connected
        """)
    
    st.write("### Mobile Ops Center")
    st.write("Welcome to the mobile field unit. Access your fraud investigation tools on the go.")
    
    if not st.session_state.logged_in:
        st.info("Tap the **> Arrow** (top left) to open the menu and Login.")
        
    st.divider()
    st.caption("v2.1.0 | Authorized Personnel Only")

# 2. LOGIN PAGE
elif selected_menu == "🔐 Login":
    st.header("🔐 Sign In")
    with st.container():
        st.write("Enter your credentials")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        st.write("") 
        if st.button("Login", type="primary"):
            if username:
                st.success("Authenticated.")
                login_user()
            else:
                st.error("Please enter a username.")

# 3. DASHBOARD
elif selected_menu == "📊 Dashboard":
    st.header("📊 Daily Overview")
    st.caption(f"Last updated: {pd.Timestamp.now().strftime('%H:%M')}")
    
    st.metric("Alerts Today", "12", "+2")
    st.metric("Pending Review", "5", "-1")
    st.metric("Blocked Amount", "$45,200", "+8%")
    
    st.divider()
    st.subheader("Recent Flags")
    
    data = [
        {"ID": "TRX-1092", "Risk": "High", "Time": "10:23 AM", "Amount": "$500"},
        {"ID": "TRX-1091", "Risk": "Med",  "Time": "09:45 AM", "Amount": "$120"},
        {"ID": "TRX-1090", "Risk": "Low",  "Time": "09:12 AM", "Amount": "$45"},
    ]
    st.dataframe(data, width='stretch')

# 4. VELOCITY CHECKER
elif selected_menu == "⚡ Velocity":
    st.header("⚡ Velocity Check")
    tab1, tab2 = st.tabs(["Manual Input", "File Upload"])
    
    with tab1:
        st.write("Quick scan for a specific User ID.")
        uid = st.text_input("User ID")
        if st.button("Scan Velocity"):
            st.info(f"Scanning 12 recent transactions for {uid}...")
            st.success("Velocity Normal (0.2 tx/min)")
            
    with tab2:
        st.write("Batch process transaction logs.")
        st.file_uploader("Upload CSV", type=['csv'])

# 5. MAPS
elif selected_menu == "🌍 Maps":
    st.header("🌍 Geo View")
    st.write("Live feed of flagged IP locations.")
    map_data = pd.DataFrame(
        np.random.randn(5, 2) / [50, 50] + [37.76, -122.4],
        columns=['lat', 'lon'])
    st.map(map_data, zoom=4) 

# 6. SETTINGS
elif selected_menu == "⚙️ Settings":
    st.header("⚙️ Settings")
    
    st.subheader("Appearance")
    
    st.toggle(
        "Enable Dark Mode", 
        value=st.session_state.dark_mode, 
        on_change=toggle_dark_mode
    )
    
    st.divider()
    
    st.subheader("Notifications")
    st.toggle("Email Alerts", value=True)
    st.toggle("SMS Alerts", value=False)
    st.toggle("Push Notifications", value=True)
    
    st.divider()
    st.subheader("Risk Thresholds")
    st.slider("Auto-Block Score", 0, 100, 85)