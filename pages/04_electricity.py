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
#some data shall be converte into TWh
df["wind_twh"]=df["wind_ej"]*277.7
df["solar_twh"]=df["solar_ej"]*277.7
total_world_last_year_twh = df.query("Country == 'Total World' and Year == 2024")["elect_twh"].values[0]


color_map = {
            "elect_twh" :"#E67E22",# 
            "electbyfuel_oil": "#A6BCD0",   # soft gray-blue
            "electbyfuel_coal": "#C19A6B",  # brownish
            "electbyfuel_gas": "#F9E79F",   # soft yellow
            "nuclear_twh": "#D7BDE2",       # light purple
            "hydro_twh": "#85C1E9",         # light blue
            "solar_twh": "#F7DC6F",         # 🌞 soft sun-yellow
            "wind_twh": "#5DADE2",          # 💨 sky blue
            "biogeo_twh": "#A3E4D7",        # 🌱 mint green / turquoise
            "electbyfuel_other": "#D5DBDB", 
 
            }

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


#✅--------------------------------------------------------------------
st.title(f" ⚡ Electricity")
st.markdown("""
            ### 📊 Electricity generation is based on gross electrical output.
            #### data in TWh
            
            """)
st.markdown(""" 
            source: source: Energy Institute (2024), Country Transition Tracker 2024, Energy Institute, London.
                        """)


selected_country = st.selectbox(
    "Select a Country or an Aggregate (Total World as default)",  # label
    options=country_selection,
    index=country_selection.index("Total Europe")  # 👈 set default selection by index
)


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
#----------------------------------------------------------------------
st.markdown("---")  # horizontal line separator
#----------------------------------------------------------------------
latest_total=df_filtered["elect_twh"].iloc[-1]
country_ele_share=latest_total/total_world_last_year_twh*100
latest_share=df_filtered[selected_electricity_variables].iloc[-1]/df_filtered["elect_twh"].iloc[-1]*100

col1, col2, col3= st.columns(3)

with col1:
    st.markdown(
        f"""
        <div style='background-color: #005680; padding: 30px; border-radius: 10px; text-align: center;'>
            <h3>{selected_country} electricity production </h3>
            <h1 style='color: #D5D8DC;'>{latest_total:.0f} TWh</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div style='background-color: #005680; padding: 30px; border-radius: 10px; text-align: center;'>
            <h3>{selected_country} share on total world electricity </h3>
            <h1 style='color: #D5D8DC;'>{country_ele_share:.1f} %</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div style='background-color: #005680; padding: 30px; border-radius: 10px; text-align: center;'>
            <h3>{selected_country} {selected_electricity_variables} share </h3>
            <h1 style='color: #D5D8DC;'>{latest_share:.1f} %</h1>
        </div>
        """,
        unsafe_allow_html=True
    )


#----------------------------------------------------------------------
st.markdown("---")  # horizontal line separator
#----------------------------------------------------------------------
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