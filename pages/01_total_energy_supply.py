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
df_readeble=pd.read_csv("data/Statistical-Review-of-World-Energy-Data-2025-forpy.csv")
df_readeble["Region"].unique()
df_readeble["Country"].unique()
df_raw=pd.read_csv("data/panel.csv")
df=df_raw

#✅------------------------DATA ELABORATION---------------------------------------------

#BREAKDOWN ENERGY BY SOURCE
#Selection : Country --> stacked bar graph along years
# Ensure Year is numeric if needed
df['Year'] = pd.to_numeric(df['Year'])

#extract the last valur TES World 
# Find the last (max) year
latest_year = df['Year'].max()
filtered_value = df.loc[(df['Country'] == 'Total World') & (df['Year'] == latest_year),'tes_ej'].values
ej_value_world_last = filtered_value[0] if len(filtered_value) > 0 else None


df["renewables_ex_hyd_ej"]=df["renewables_ej"]-df["hydro_ej"]
#df["yoy_change"] = df["tes_ej"].diff().fillna(0)


country_selection=(
                    df["Country"]
                   .unique()
                   .tolist()
)

palette_blue = [
    "#A7D5F2",  # light blue
    "#94CCE8",
    "#81C3DD",
    "#6FBBD3",
    "#5DB2C8",
    "#A9DEF9",  # baby blue
]

palette_green = [
    "#6DC0B8",  # pastel teal
    "#7DCFA8",
    "#8DDC99",
    "#9CE98A",
    "#ABF67B",
    "#C9F9D3",  # mint green
    "#C4E17F",  # lime green
]

palette_other = [
    "#FFD7BA",  # pastel orange
    "#FFE29A",  # pastel yellow
    "#FFB6C1",  # pastel pink
    "#D7BDE2",  # pastel purple
    "#F6C6EA",  # light rose
    "#F7D794",  # peach
    "#E4C1F9",  # lavender
]
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
            source: Energy Institute (2024), Country Transition Tracker 2024, Energy Institute, London.
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
    .assign(fossil_share=lambda x:(x["oilcons_ej"]+ x["coalcons_ej"]+x["gascons_ej"])/x["tes_ej"]*100)
)
# **************************************************************************************

#----------------------------------------------------
st.markdown("---")  # horizontal line separator
#----------------------------------------------------

last_data_year=df_filtered.index.values[-1]
last_tes_value=df_filtered["tes_ej"].iloc[-1]
last_variation=df_filtered["yoy_change_pct"].iloc[-1]
last_fossile_share=df_filtered["fossil_share"].iloc[-1]
country_share=last_tes_value/ej_value_world_last*100



# Create 2 columns for side-by-side KPI cards
col1, col2, col3= st.columns(3)

with col1:
    st.markdown(
        f"""
        <div style='background-color: #005680; padding: 30px; border-radius: 10px; text-align: center;'>
            <h3>TES |{selected_country} | {last_data_year} </h3>
            <h1 style='color: #E67E22;'>{last_tes_value:.0f} EJ</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
   st.markdown(
        f"""
        <div style='background-color: #005680; padding: 30px; border-radius: 10px; text-align: center;'>
            <h3>Fossil Share |{selected_country} | {last_data_year} </h3>
            <h1 style='color: #C19A6B";'>{last_fossile_share:.1f} %</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
   st.markdown(
        f"""
        <div style='background-color: #005680; padding: 30px; border-radius: 10px; text-align: center;'>
            <h3>TES Share|{selected_country} | {last_data_year} </h3>
            <h1 style='color: #E67E22;'>{country_share:.1f} %</h1>
        </div>
        """,
        unsafe_allow_html=True
    )


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



#----------------------------------------------------
st.markdown("---")  # horizontal line separator
#----------------------------------------------------

#NARRATIVE BOX
# Narrative text with f-string + HTML styling
narrative = f"""
<div style="
    border: 2px solid {palette_green[3]};
    padding: 15px;
    border-radius: 10px;
    background-color: rgba(255, 255, 255, 0.05);
    color: white;
">
<b>📊 Key Insights</b>

-In **{last_data_year}** the Total Energy Supply for **{selected_country}** was **{last_tes_value:.0f}** [EJ] with a variation of 
**{last_variation:.1f}** [%] comparing the previous year.

</div>
"""

st.markdown(narrative, unsafe_allow_html=True)


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

#-----------------------------------------------------------------
#----------------------------------------------------
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

