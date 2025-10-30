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
df_readeble=pd.read_csv("data/Statistical-Review-of-World-Energy-Data-2025-forpy.csv")
df_readeble["Region"].unique()
df_readeble["Country"].unique()
glossary_da=pd.read_csv("data/Glossary.csv")
df_raw=pd.read_csv("data/panel.csv")
df=df_raw

#✅------------------------DATA ELABORATION---------------------------------------------

#BREAKDOWN ENERGY BY SOURCE
#Selection : Country --> stacked bar graph along years
#df["renewables_ex_hyd_ej"]=df["renewables_ej"]-df["hydro_ej"]
#df["yoy_change"] = df["tes_ej"].diff().fillna(0)
df["wind_twh"]=df["wind_ej"]*277.7
df["solar_twh"]=df["solar_ej"]*277.7

country_selection=(
                    df["Country"]
                   .unique()
                   .tolist()
)

year_selection=(
                    df["Year"]
                   .unique()
                   .tolist()
)


color_map = {
    "electbyfuel_oil": "#A6BCD0",   # soft gray-blue
    "electbyfuel_coal": "#C19A6B",  # brownish
    "electbyfuel_gas": "#F9E79F",   # soft yellow
    "nuclear_twh": "#D7BDE2",       # light purple
    "hydro_twh": "#85C1E9",         # light blue
    "solar_twh": "#F7DC6F",         # 🌞 soft sun-yellow
    "wind_twh": "#5DADE2",          # 💨 sky blue
    "biogeo_twh": "#A3E4D7",        # 🌱 mint green / turquoise
    "electbyfuel_other": "#D5DBDB", 
    "elect_twh" :"#E67E22"# 
}


#✅--------------------------------------------------------------------
st.title(f" ⚡ Electricity")
st.markdown("""
            ### 📊 Electricity generation is based on gross electrical output.
            #### data in TWh
            
            """)
st.markdown(""" 
            source: Energy Institute 2025
                        """)


selected_country = st.selectbox(
    "Select a Country or an Aggregate (Total World as default)",  # label
    options=country_selection,
    index=country_selection.index("Total Europe")  # 👈 set default selection by index
)

#df["renewables_ex_hyd_ej"]=df["renewables_ej"]-df["hydro_ej"]
electricity_variables = [
    "elect_twh",
    "electbyfuel_oil",
    "electbyfuel_gas",
    "electbyfuel_coal",
    "nuclear_twh",
    "hydro_twh",
    "solar_twh",
    "wind_twh",
    "biogeo_twh",
    "electbyfuel_other"
]


selected_electricity_variables= st.selectbox(
    "Select an Electricity (Total Electricity as default)",  # label
    options=electricity_variables,
    index=electricity_variables.index("solar_twh")  # 👈 set default selection by index
)


# **************************************************************************************
#selection for the different energy in EJ
df_filtered = (
    df
    .query("Country == @selected_country")
    .set_index("Year")
    .sort_index()
    [electricity_variables]
    .assign(share_on_total_electricity=lambda x:x[selected_electricity_variables]/x["elect_twh"]*100)
   #.assign(renewables_ex_hyd_ej=lambda x: x["renewables_ej"] - x["hydro_ej"])
   # .assign(ren_pc=lambda x:x["renewables_ej"]/x["tes_ej"]*100)
   # .assign(hydro_ren_pc=lambda x: x["hydro_ej"]/x["renewables_ej"]*100)
)
# **************************************************************************************


# Create subplot: 2 rows, shared x-axis
fig = make_subplots(
    rows=2,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.12,
    row_heights=[0.7, 0.3],
    subplot_titles=(
        f"Electricity source [TWh] - {selected_country}",
        "Share component on Aggregated Electricity [%]"
    )
)

fig.add_trace(
    go.Scatter(
        x=df_filtered.index,
        y=df_filtered[selected_electricity_variables],
        name=selected_electricity_variables.replace("_", " ").title(),
        fill='tozeroy',
        line=dict(color=color_map[selected_electricity_variables])  # 👈 dynamic color
    ),
    row=1,
    col=1
)

fig.add_trace(
            go.Scatter(
                x=df_filtered.index,
                y=df_filtered["share_on_total_electricity"],
                name="share [%]",
                #marker_color=color_map[column]
                line=dict(color=color_map[selected_electricity_variables])  # 👈 dynamic color
            ),
            row=2,
            col=1
        )


fig.update_xaxes(
    title_text="years",
    row=2,
    col=1,
    title_font=dict(color='white'),
    tickfont=dict(color='white'),
    gridcolor="rgba(255,255,255,0.1)"
)



fig.update_yaxes(
    title_text="Electricity  (TWh)",
    row=1,
    col=1,
    title_font=dict(color='white'),
    tickfont=dict(color='white'),
    gridcolor="rgba(255,255,255,0.1)"
)

fig.update_yaxes(
    title_text="Share on Aggregated Electricity (%)",
    row=2,
    col=1,
    title_font=dict(color='white'),
    tickfont=dict(color='white'),
    gridcolor="rgba(255,255,255,0.1)"
)



fig.update_layout(height=600) 

# Show Plotly chart
st.plotly_chart(fig, use_container_width=True, key="country_chart")





# Prepare CSV for download
csv = df_filtered.to_csv(index=True).encode("utf-8")

# Download button
st.download_button(
    label=f"⬇️ Download data for {selected_country} ",
    data=csv,
    file_name=f"energy_supply_{selected_country}.csv",
    mime="text/csv",
)