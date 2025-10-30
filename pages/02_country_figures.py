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

#BREAKDOWN ENERGY BY SOURCE
#Selection : Country --> stacked bar graph along years
#df["renewables_ex_hyd_ej"]=df["renewables_ej"]-df["hydro_ej"]
#df["yoy_change"] = df["tes_ej"].diff().fillna(0)
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
    "oilcons_ej": "#A6BCD0",
    "coalcons_ej": "#C19A6B",
    "gascons_ej": "#F9E79F",
    "nuclear_ej": "#D7BDE2",
    "hydro_ej": "#85C1E9",
    "renewables_ex_hyd_ej": "#ABEBC6",
    "tes_ej": "#E67E22"
}

#✅--------------------------------------------------------------------
st.title(f" 🌐 Country Energy Breakdown")
st.markdown("""
            ### 📊 energy supply comprises commercially-traded fuels, including modern renewables used to generate electricity
            #### data in ExaJoule [EJ]
            
            """)
st.markdown(""" 
            source: Energy Institute 2025
                        """)


selected_country = st.selectbox(
    "Select a Country or an Aggregate (Total World as default)",  # label
    options=country_selection,
    index=country_selection.index("Norway")  # 👈 set default selection by index
)

selected_year= st.selectbox(
    "Select a Country or an Aggregate (Total World as default)",  # label
    options=year_selection,
    index=year_selection.index(2024)  # 👈 set default selection by index
)


# **************************************************************************************
#selection for the different energy in EJ
df_filtered = (
    df
    .query("Country == @selected_country and Year==@selected_year")
    .set_index("Year")
    .sort_index()
    [["oilcons_ej", "coalcons_ej" ,"gascons_ej","nuclear_ej","hydro_ej","renewables_ej","tes_ej"]]
    .assign(renewables_ex_hyd_ej=lambda x: x["renewables_ej"] - x["hydro_ej"])
    .assign(ren_pc=lambda x:x["renewables_ej"]/x["tes_ej"]*100)
    .assign(hydro_ren_pc=lambda x: x["hydro_ej"]/x["renewables_ej"]*100)
)
# **************************************************************************************
#----------------------------------------------------
st.markdown("---")  # horizontal line separator
#----------------------------------------------------
# Assuming df_filtered has only 1 row (one country & year)
latest_data = df_filtered.iloc[0]

# Extract values
total_energy = latest_data["tes_ej"]
renewable_share = latest_data["ren_pc"]
hydro_share=latest_data["hydro_ren_pc"]

# Create 2 columns for side-by-side KPI cards
col1, col2, col3= st.columns(3)

with col1:
    st.markdown(
        f"""
        <div style='background-color: #005680; padding: 30px; border-radius: 10px; text-align: center;'>
            <h3>Total Energy Supply</h3>
            <h1 style='color: #E67E22;'>{total_energy:.2f} EJ</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div style='background-color: #005680; padding: 30px; border-radius: 10px; text-align: center;'>
            <h3>Renewables Share of TES</h3>
            <h1 style='color: #ABEBC6;'>{renewable_share:.1f}%</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div style='background-color: #005680; padding: 30px; border-radius: 10px; text-align: center;'>
            <h3>Hydro Share of RES</h3>
            <h1 style='color: #85C1E9;'>{hydro_share:.1f}%</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
#----------------------------------------------------
st.markdown("---")  # horizontal line separator
#----------------------------------------------------
# 💹FIG💹---------------------------------------------------------------------
data_to_plot = df_filtered.drop(columns=["tes_ej","renewables_ej","ren_pc","hydro_ren_pc"]).iloc[0]
bar_colors = [color_map.get(etype, "#CCCCCC") for etype in data_to_plot.index]


fig = go.Figure()
fig.add_trace(go.Bar(
        x=data_to_plot.values,
        y=data_to_plot.index,
        orientation='h',
       marker=dict(color=bar_colors),
        text=[f"{v:.2f} EJ" for v in data_to_plot.values],
        textposition='auto',
        hovertemplate='%{y}: %{x:.2f} EJ<extra></extra>'
    ))

fig.update_layout(
        title=f"Energy Consumption by Type - {df_filtered.index[0]}",
        xaxis_title="Energy Consumption (EJ)",
        yaxis_title="Energy Type",
        template="plotly_white",
        height=400
    )

fig.update_layout(height=600) 

# Show Plotly chart
st.plotly_chart(fig, use_container_width=True, key="country_chart")

#----------------------------------------------------------------------
st.markdown("---")  # horizontal line separator



# Prepare CSV for download
csv = df_filtered.to_csv(index=True).encode("utf-8")

# Download button
st.download_button(
    label=f"⬇️ Download data | {selected_country} ",
    data=csv,
    file_name=f"energy_supply_{selected_country}.csv",
    mime="text/csv",
)

st.markdown("---")  # horizontal line separator

st.markdown(
    """
    <small><i>
            Note: TES is a measure of the
        total amount of energy that a country needs
        to supply to meet its final end-use demand.
        It reflects the energy that is either produced
        domestically or imported, minus what is exported
        or stored. Some energy sources are consumed
        directly while others may be converted into
        fuels or electricity for final consumption with
        transmission, distribution, and efficiency losses
        occurring throughout the system.
    </i></small>
    """,
    unsafe_allow_html=True
)