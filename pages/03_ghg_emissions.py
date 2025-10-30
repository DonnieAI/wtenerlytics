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


df["co2_ex_combustion"]=df["co2_mtco2"]-df["co2_combust_mtco2"]

country_selection=(
                    df["Country"]
                   .unique()
                   .tolist()
)

year_thresold=1990


color_map = {
    "co2_combust_mtco2": "#B0BEC5",   # pastel steel grey-blue (CO₂ from combustion)
    "co2_ex_combustion": "#A1887F",   # soft muted taupe (CO₂ from other sources)
    "co2_mtco2": "#D5D8DC",           # light silvery-grey (Total CO₂)
}


#✅--------------------------------------------------------------------
st.title(f" 🏭 GHG Emissions")
st.markdown("""
            ### 📊 GHG Emissions
            #### data in GtCO2eq
            
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
    [["co2_combust_mtco2", "co2_ex_combustion","co2_mtco2" ]]  
     .assign(yoy_change_pct=lambda x: x["co2_mtco2"].pct_change().fillna(0) * 100)# Select specific columns here
)
# **************************************************************************************

latest_data = df_filtered["co2_mtco2"].iloc[-1]/1000   # GtCO2eq
values_vs_1990=df_filtered.query("Year ==1990")["co2_mtco2"].iloc[0]/1000
values_vs_2005=df_filtered.query("Year ==2005")["co2_mtco2"].iloc[0]/1000
pc_change_1990=((latest_data-values_vs_1990)/values_vs_1990)*100
pc_change_2005=((latest_data-values_vs_2005)/values_vs_2005)*100
# Create 2 columns for side-by-side KPI cards
col1, col2, col3= st.columns(3)

with col1:
    st.markdown(
        f"""
        <div style='background-color: #005680; padding: 30px; border-radius: 10px; text-align: center;'>
            <h3>Total Energy Supply</h3>
            <h1 style='color: #D5D8DC;'>{latest_data:.2f} GtCO2eq</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div style='background-color: #005680; padding: 30px; border-radius: 10px; text-align: center;'>
            <h3>Delta vs 1990</h3>
            <h1 style='color: #D5D8DC;'>{pc_change_1990:.1f}%</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div style='background-color: #005680; padding: 30px; border-radius: 10px; text-align: center;'>
            <h3>Delta vs 2005</h3>
            <h1 style='color: #D5D8DC;'>{pc_change_2005:.1f}%</h1>
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
    row_heights=[0.7, 0.3],
    subplot_titles=(
        f"GHG Emissions [GtCO2eq] - {selected_country}",
        "YoY variation[%]"
    )
)

columns_for_bar_plot=["co2_combust_mtco2", "co2_ex_combustion"]
for col in columns_for_bar_plot:
        fig.add_trace(
            go.Bar(
                x=df_filtered.index,
                y=df_filtered[col]/1000,  # to transpormg in GtCO2
                name=col,
                marker_color=color_map.get(col, "#ccc")
            )
        )

fig.add_trace(
    go.Scatter(
        x=df_filtered.index,
        y=df_filtered["co2_mtco2"] / 1000,  # Convert MtCO2 → GtCO2
        mode="lines+markers",  # Add markers if you want dots on the line
        name="Total CO₂ (line)",
        line=dict(
                color=color_map.get("co2_mtco2", "#000"), 
                width=2, 
                dash="dash") , # Optional styling
        marker=dict(
                color=color_map.get("co2_mtco2", "#000"),  # same as line color or choose different
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
fig.update_layout(
        barmode='stack',
        title=f'Total GHG Emissions in {selected_country}',
       # xaxis_title='Year',
        yaxis_title='GHG Emissions (GtCO2eq)',
        legend_title='GHG contribution',
        template='plotly_white',
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