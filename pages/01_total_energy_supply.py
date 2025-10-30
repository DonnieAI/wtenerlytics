"""Energy consumption weekly data 

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
df["renewables_ex_hyd_ej"]=df["renewables_ej"]-df["hydro_ej"]
#df["yoy_change"] = df["tes_ej"].diff().fillna(0)
country_selection=(
                    df["Country"]
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
st.title(f" 🌐 Total Energly Supply [TES]")
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
    index=country_selection.index("Total World")  # 👈 set default selection by index
)




# **************************************************************************************
#selection for the different energy in EJ
df_filtered = (
    df
    .query("Country == @selected_country")
    .set_index("Year")
    .sort_index()
    [["oilcons_ej", "coalcons_ej" ,"gascons_ej","nuclear_ej","hydro_ej","renewables_ex_hyd_ej","tes_ej"]]
    .assign(yoy_change_pct=lambda x: x["tes_ej"].pct_change().fillna(0) * 100)
)
# **************************************************************************************


# 💹FIG💹---------------------------------------------------------------------

# Create subplot: 2 rows, shared x-axis
fig = make_subplots(
    rows=2,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.12,
    row_heights=[0.7, 0.3],
    subplot_titles=(
        f"TES [EJ] - {selected_country}",
        "Year-over-Year Change [%]"
    )
)

# Define which energy sources to show as stacked bars
columns_for_bar_plot = [
    "oilcons_ej", "coalcons_ej", "gascons_ej",
    "nuclear_ej", "hydro_ej", "renewables_ex_hyd_ej"
]

# Add stacked bars (row 1)
for col in columns_for_bar_plot:
    fig.add_trace(
        go.Bar(
            x=df_filtered.index,
            y=df_filtered[col],
            name=col.replace("_ej", "").capitalize(),
            marker_color=color_map.get(col, "#ccc")
        ),
        row=1,
        col=1
    )

# Add total TES line (row 1)
fig.add_trace(
    go.Scatter(
        x=df_filtered.index,
        y=df_filtered["tes_ej"],
        mode="lines+markers",
        name="Total TES",
        line=dict(
            color=color_map.get("tes_ej", "#000"),
            width=4,
            dash="dash"
        ),
        marker=dict(
            color=color_map.get("tes_ej", "#000"),  # same as line color or choose different
            size=8,           # marker size
            symbol="diamond",  # shape: "circle", "square", "diamond", "cross", etc.
            line=dict(
                width=1,
                color='white'  # marker border color
            )
        )
    ),
    row=1,
    col=1
)

# Add YoY change bars (row 2)
fig.add_trace(
    go.Bar(
        x=df_filtered.index,
        y=df_filtered["yoy_change_pct"],
        name="YoY Change",
        marker_color=[
            "#F5B7B1" if v < 0 else "#A9DFBF"
            for v in df_filtered["yoy_change_pct"]
        ]
    ),
    row=2,
    col=1
)

# Format Y-axis for second subplot (YoY)
fig.update_yaxes(
    title_text="YoY Change (%)",
    row=2,
    col=1,
    title_font=dict(color='white'),
    tickfont=dict(color='white'),
    gridcolor="rgba(255,255,255,0.1)"
)

# General layout updates
fig.update_layout(
    barmode='stack',
    height=600,
    template='plotly_white',
    title=f'Total Energy Consumption by Source in {selected_country}',
    title_font=dict(color='white'),
    font=dict(color='white'),
    legend_title='Energy Source',
    legend=dict(font=dict(color='white')),

    yaxis=dict(
        title='TES (EJ)',
        title_font=dict(color='white'),
        tickfont=dict(color='white'),
        gridcolor="rgba(255,255,255,0.1)"
    )
)

fig.update_layout(height=600) 
# Show Plotly chart
st.plotly_chart(fig, use_container_width=True, key="TES_chart")


#----------------------------------------------------------------------
st.markdown("---")  # horizontal line separator
#----------------------------------------------------------------------
# Prepare CSV for download
csv = df_filtered.to_csv(index=True).encode("utf-8")

# Download button
st.download_button(
    label=f"⬇️ Download data for TES | {selected_country} ",
    data=csv,
    file_name=f"energy_supply_TES_{selected_country}.csv",
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

