"""Key Minerals

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

# filter only on countries that have critical material data

df = df[
    (df["cobalt_kt"] > 0) |
    (df["graphite_kt"] > 0) |
    (df["lithium_kt"] > 0) |
    (df["rareearths_kt"] > 0)
]

country_selection=(
                    df["Country"]
                   .unique()
                   .tolist()
)


production_variables= [
    "cobalt_kt",   
    "graphite_kt",   
    "lithium_kt"  , 
    "rareearths_kt" 
    ]


color_map = {
    "cobalt_kt": "#EF9A9A",     # pastel red (cobalt)
    "graphite_kt": "#B0BEC5",   # pastel blue-grey (graphite)
    "lithium_kt": "#81D4FA",    # pastel sky blue (lithium)
    "rareearths_kt": "#CE93D8", # pastel lavender (rare earths)
}

#✅--------------------------------------------------------------------
st.title(f" 🪨 Key Materials")
st.markdown("""
            ### 🪨 Key Materials
            #### data in thousand of tons [kt]
            
            """)
st.markdown(""" 
            source: Energy Institute (2024), Country Transition Tracker 2024, Energy Institute, London.
                        """)

selected_key_material= st.selectbox(
    "Select a Key Material",  # label
    options=production_variables,
    #index=country_selection.index("Total Europe")  # 👈 set default selection by index
)



selected_country = st.selectbox(
    "Select a Country or an Aggregate (Total World as default)",  # label
    options=country_selection,
    index=country_selection.index("Australia")  # 👈 set default selection by index
)




# **************************************************************************************
#selection for the different key material production
df_filtered= (
    df
    .query("Country == @selected_country")
    .set_index("Year")
    .sort_index()
    [[selected_key_material]]  
     .assign(yoy_change_pct=lambda x: x[selected_key_material].pct_change().fillna(0) * 100)# Select specific columns here
)
# **************************************************************************************

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
        f"{selected_key_material }[kt] - {selected_country}",
        "YoY variation[%]"
    )
)

fig.add_trace(
    go.Scatter(
        x=df_filtered.index,
        y=df_filtered[selected_key_material] / 1000,  # Convert MtCO2 → GtCO2
        mode="lines+markers",  # Add markers if you want dots on the line
        name=f"{selected_key_material} [kt]",
        line=dict(
                color=color_map.get(selected_key_material, "#000"), 
                width=2, 
                dash="dash") , # Optional styling
        marker=dict(
                color=color_map.get(selected_key_material, "#000"),  # same as line color or choose different
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
        title=f'{selected_key_material} in {selected_country}',
       # xaxis_title='Year',
        yaxis_title='kt',
        legend_title='key material',
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
st.plotly_chart(fig, use_container_width=True, key="key_material_chart")