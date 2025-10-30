# P2Xplorer

#cdm
#     projenv\Scripts\activate
#     streamlit run home.py

import streamlit as st
import pandas as pd


# ✅ Must be the first Streamlit call
st.set_page_config(
    page_title="Home",   # Browser tab title
    page_icon="🌍",      # Optional favicon (emoji or path to .png/.ico)
    layout="wide"        # "centered" or "wide"
)


# ── Load user credentials and profiles ────────────────────────
CREDENTIALS = dict(st.secrets["auth"])
PROFILES = st.secrets.get("profile", {})

# ── Login form ────────────────────────────────────────────────
def login():
    st.title("🔐 Login Required")

    user = st.text_input("Username", key="username_input")
    password = st.text_input("Password", type="password", key="password_input")

    if st.button("Login", key="login_button"):
        if user in CREDENTIALS and password == CREDENTIALS[user]:
            st.session_state["authenticated"] = True
            st.session_state["username"] = user
            st.session_state["first_name"] = PROFILES.get(user, {}).get("first_name", user)
        else:
            st.error("❌ Invalid username or password")

# ── Auth state setup ──────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# ── Login gate ────────────────────────────────────────────────
if not st.session_state["authenticated"]:
    login()
    st.stop()

# ── App begins after login ────────────────────────────────────

# ---------------Sidebar
from utils import apply_style_and_logo

st.sidebar.success(f"Welcome {st.session_state['first_name']}!")
st.sidebar.button("Logout", on_click=lambda: st.session_state.update(authenticated=False))

# Spacer to push the link to the bottom (optional tweak for better placement)
st.sidebar.markdown("<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)

# Company website link
st.sidebar.markdown(
    '<p style="text-align:center;">'
    '<a href="https://www.wavetransition.com" target="_blank">🌐 Visit WaveTransition</a>'
    '</p>',
    unsafe_allow_html=True
)

# ---------Main content
st.title("**Enerlytics**")

# --- Centered cover image ---
from PIL import Image
cover_img = Image.open("cover.png")
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
st.image(cover_img, use_container_width=False, width=800)  # updated
#st.image(cover_img, use_container_width=True)  # auto fit


st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
## Enerlytics – Data-Driven Insights Across the Global Energy Landscape  

**Enerlytics** is a powerful, web-based analytics platform designed to help you **explore, analyze, and visualize the full spectrum of global energy data**. Built on a comprehensive, high-resolution dataset, Enerlytics empowers users to create **original, customized analyses** across fuels, technologies, sectors, and geographies.

Whether you're investigating **fossil fuel trends**, **renewable energy growth**, or **emissions trajectories**, Enerlytics offers a flexible and intuitive environment for **insight generation and scenario exploration**.

---

### 🌐 Coverage: Global Energy System Data

Enerlytics provides a **structured and up-to-date dataset** that spans the key dimensions of the global energy system:

- **Primary energy consumption** (oil, gas, coal, nuclear, renewables, hydro)  
- **Power generation and electricity use**  
- **Biofuels production and consumption**  
- **Greenhouse gas emissions** and sectoral breakdowns  
- **Energy intensity**, per capita metrics, and YoY change rates  
- **Country-level and global aggregates**, from 1965 to the present  

---

### 🎯 Purpose

The goal of **Enerlytics** is to enable **open, flexible, and data-rich energy analysis** through an intuitive interface, making it an ideal tool for:

- **Researchers** exploring historical trends and forecasting  
- **Policymakers** assessing decarbonization progress  
- **Energy analysts and consultants** developing custom dashboards  
- **Educators and students** learning through interactive exploration  

---

### 🔍 Key Features

- ✅ **Custom KPI cards**, charts, and comparisons across countries and years  
- 📊 **Interactive visualizations** powered by Plotly (bar, line, stacked, YoY plots)  
- 🧪 **Derived metrics** like renewable shares, CO₂ per capita, intensity ratios  
- 🌍 **Region/country selector** with streamlined time filtering  
- 📁 **Ready-to-analyze datasets**, filtered on-the-fly  
- 🧩 Built entirely in **Python + Streamlit** for transparency and extensibility  

---

### 📈 Use Cases

With Enerlytics, you can:

- Compare **energy supply structures** across countries or regions  
- Track **renewables share growth** and fossil fuel decline  
- Analyze **CO₂ emissions trajectories** and YoY changes  
- Understand **biofuel trends** across consumption and production  
- Build **custom scenarios** or export filtered data for further modeling  

---

### ⚠️ Note

Enerlytics is intended for **exploratory, high-level energy system analysis**. For deep policy modeling, investment-grade forecasting, or lifecycle assessments, external models and detailed sectoral data should be used in combination.

---

### 🚀 Start Exploring

Use the sidebar to select a country, year, or fuel type — and begin building **your own energy story** with data that matters.
""")


