"""lcoe

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
df_raw=pd.read_csv("data/lcoe_trend.csv")
df=df_raw

color_map = {
    'Bioenergy': '#228B22',             # ForestGreen – represents biomass/organic material
    'Geothermal': '#8B4513',            # SaddleBrown – earthy color, links to underground heat
    'Hydro': '#1E90FF',                 # DodgerBlue – vibrant water blue
    'Offshore wind': '#0077BE',         # Ocean Blue – to represent sea-based wind
    'Onshore wind': '#66C2A5',          # Teal/Greenish – land-based and clean
    'Solar photovoltaic': '#FFD700',    # Gold – bright, sun-reflective
    'Solar thermal': '#FF8C00'          # DarkOrange – thermal heat from sun
}

#✅--------------------------------------------------------------------
st.title(f" 🌐 Levelized Cost of Energy - LCOE")
st.markdown("""
            ### 📊  lcoe [2024 USD/MWh] 
            
            """)
st.markdown(""" 
            source: IRENA 2024
                        """)


#selected_country = st.selectbox(
 #   "Select a Country or an Aggregate (Total World as default)",  # label
 #   options=country_selection,
 #   index=country_selection.index("EU")  # 👈 set default selection by index
#)


# **************************************************************************************
#selection for the different energy in EJ
df_filtered= (
    df
    .set_index("Year")
    .sort_index()
)
# **************************************************************************************

fig = go.Figure()


    # Get unique technologies
for source in df["Source"].unique():
    df_source = df[df["Source"] == source]
    fig.add_trace(go.Scatter(
        x=df_source["Year"],
        y=df_source["Value"]*1000,  #UESD/MWh 
        mode='lines+markers',
        name=source,
        line=dict(
            color=color_map.get(source, "#000"),
            width=4,
            #dash="dash"
        ),
        marker=dict(
            color=color_map.get(source, "#000"),  # same as line color or choose different
            size=8,           # marker size
            symbol="diamond",  # shape: "circle", "square", "diamond", "cross", etc.
            line=dict(
                width=2,
                color='white'  # marker border color
            )
        )
        
        
        #hovertemplate=f"<b>{source}</b><br>Year: %{x}<br>Value: %{y:.4f}<extra></extra>"
    ))

# Layout configuration
fig.update_layout(
    title="Trend by Energy Source",
    xaxis_title="Year",
    yaxis_title="Value",
    template="plotly_white"
)

fig.update_layout(height=600) 

# Show Plotly chart
st.plotly_chart(fig, use_container_width=True, key="lcoe_chart")