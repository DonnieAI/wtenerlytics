"""Country analysis

"""
import streamlit as st
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px 
from pathlib import Path
from plotly.subplots import make_subplots

st.set_page_config(page_title="Dashboard", layout="wide")
from utils import apply_style_and_logo
apply_style_and_logo()

#✅------------------------DATA EXTRACTION-----------------------------------------------------
df_readeble=pd.read_csv("data\Statistical-Review-of-World-Energy-Data-2025-forpy.csv")
df_readeble["Region"].unique()
df_readeble["Country"].unique()
glossary_da=pd.read_csv("data\Glossary.csv")
df_raw=pd.read_csv("data\panel.csv")
df=df_raw


#✅------------------------DATA ELABORATION---------------------------------------------

#GHG EMISSIONS
#Selection : Country --> stacked bar graph along years
biofuel_subset = [
    "biodiesel_cons_kboed",
    "biodiesel_prod_kboed",
    "biofuels_cons_kboed",
    "biofuels_prod_kboed",
    "ethanol_cons_kboed",
    "ethanol_prod_kboed"
]

color_map = {
    "biodiesel_cons_kboed": "#6BAED6",   # medium blue
    "biodiesel_prod_kboed": "#74C476",   # medium green

    "biofuels_cons_kboed": "#4292C6",    # darker blue
    "biofuels_prod_kboed": "#41AB5D",    # darker green

    "ethanol_cons_kboed": "#9ECAE1",     # light blue
    "ethanol_prod_kboed": "#A1D99B"      # light green
}

country_selection=(
                    df["Country"]
                   .unique()
                   .tolist()
)

year_thresold=1990


#✅--------------------------------------------------------------------
st.title(f" 🌱 Biofuels Production and Consumption")
st.markdown("""
            ### 📊 Biofuels Production and Consumption
            #### data in thousand of barrels of oil eqivalent per day [ kboepd]
            
            """)
st.markdown(""" 
            source: Energy Institute 2025
                        """)


selected_country = st.selectbox(
    "Select a Country or an Aggregate (Total World as default)",  # label
    options=country_selection,
    index=country_selection.index("Total Europe")  # 👈 set default selection by index
)



# **************************************************************************************
#selection for the different energy in EJ
df_filtered= (
    df
    .query("Country == @selected_country and Year >= @year_thresold")
    .set_index("Year")
    .sort_index()
    [biofuel_subset]  
     #.assign(yoy_change_pct=lambda x: x["co2_mtco2"].pct_change().fillna(0) * 100)# Select specific columns here
)
# **************************************************************************************

latest_data_produced = df_filtered["biofuels_prod_kboed"].iloc[-1]
latest_data_consumed= df_filtered["biofuels_cons_kboed"].iloc[-1]
last_biodiesel=df_filtered["biodiesel_prod_kboed"].iloc[-1]
last_ethanol=df_filtered["ethanol_prod_kboed"].iloc[-1]

col1, col2, col3= st.columns(3)

with col1:
    st.markdown(
        f"""
        <div style='background-color: #005680; padding: 30px; border-radius: 10px; text-align: center;'>
            <h3>Biofuels production/h3>
            <h1 style='color: #D5D8DC;'>{latest_data_produced:.1f} kboepd</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div style='background-color: #005680; padding: 30px; border-radius: 10px; text-align: center;'>
            <h3>Biodiesel production</h3>
            <h1 style='color: #D5D8DC;'>{last_biodiesel:.1f} kboepd</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div style='background-color: #005680; padding: 30px; border-radius: 10px; text-align: center;'>
            <h3>Ethanol production</h3>
            <h1 style='color: #D5D8DC;'>{last_ethanol:.1f} kboepd</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

#----------------------------------------------------
st.markdown("---")  # horizontal line separator
#----------------------------------------------------
# Create subplot: 2 rows, shared x-axis
fig = make_subplots(
    rows=2,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.12,
    row_heights=[0.5, 0.5],
    subplot_titles=(
        f"GHG Emissions [GtCO2eq] - {selected_country}",
        "YoY variation[%]"
    )
)


fig.add_trace(
    go.Scatter(
        x=df_filtered.index,
        y=df_filtered["biofuels_prod_kboed"] / 1000,  # Convert MtCO2 → GtCO2
        mode="lines",  # Add markers if you want dots on the line
        name="Biofuels - production ",
        line=dict(
                color=color_map.get("biofuels_prod_kboed", "#000"), 
                width=2, 
                dash="dash") , # Optional styling
        
        ),
        row=1,
        col=1
)

fig.add_trace(
    go.Scatter(
        x=df_filtered.index,
        y=df_filtered["biofuels_cons_kboed"] / 1000,  # Convert MtCO2 → GtCO2
        mode="lines",  # Add markers if you want dots on the line
        name="Biofuels - production ",
        line=dict(
                color=color_map.get("biofuels_cons_kboed", "#000"), 
                width=2, 
                dash="dash") , # Optional styling
        
        ),
        row=1,
        col=1
)


# Add YoY change bars (row 2)
fig.add_trace(
    go.Bar(
        x=df_filtered.index,
        y=df_filtered["biofuels_prod_kboed"],
        name="YoY Change",
        marker_color=[
            "#F5B7B1" if v < 0 else "#A9DFBF"
            for v in df_filtered["biofuels_prod_kboed"]
        ]
    ),
    row=2,
    col=1
)


fig.update_layout(height=600) 

# Show Plotly chart
st.plotly_chart(fig, use_container_width=True, key="country_chart")

#----------------------------------------------------------------------
st.markdown("---")  # horizontal line separator
#----------------------------------------------------------------------

# Prepare CSV for download
csv = df_filtered.to_csv(index=True).encode("utf-8")

# Download button
st.download_button(
    label=f"⬇️ Download data for GHG | {selected_country} ",
    data=csv,
    file_name=f"GHG_data_{selected_country}.csv",
    mime="text/csv",
)