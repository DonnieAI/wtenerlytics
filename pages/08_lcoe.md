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
df_raw=pd.read_csv("data/lcoe.csv")
df=df_raw

country_selection=(
                    df["Country"]
                   .unique()
                   .tolist()
)

#✅--------------------------------------------------------------------
st.title(f" 🌐 Levelized Cost of Energy - LCOE")
st.markdown("""
            ### 📊  locee [2024 USD/MWh] 
            
            """)
st.markdown(""" 
            source: IRENA 2024
                        """)


selected_country = st.selectbox(
    "Select a Country or an Aggregate (Total World as default)",  # label
    options=country_selection,
    index=country_selection.index("EU")  # 👈 set default selection by index
)


# **************************************************************************************
#selection for the different energy in EJ
df_filtered= (
    df
    .query("Country == @selected_country") 
    .set_index("Year")
    .sort_index()
    [["Technology", "LCOE" ]]  
    # .assign(yoy_change_pct=lambda x: x["co2_mtco2"].pct_change().fillna(0) * 100)# Select specific columns here
)
# **************************************************************************************

fig = go.Figure()


    # Get unique technologies
for tech in df_filtered['Technology'].unique():
        df_tech = df_filtered[df_filtered['Technology'] == tech]
        fig.add_trace(go.Scatter(
            x=df_tech.index,
            y=df_tech['LCOE'],
            mode='lines+markers',
            name=tech,
            #hovertemplate=f"<b>{tech}</b><br>Year: %{x}<br>LCOE: %{y} USD/MWh<extra></extra>"
        ))

# Layout configuration
fig.update_layout(
        title='LCOE Trends by Technology',
        xaxis=dict(title='Year'),
        yaxis=dict(title='LCOE (USD/MWh)'),
        hovermode='x unified',
        template='plotly_white'
    )
fig.update_layout(height=600) 

# Show Plotly chart
st.plotly_chart(fig, use_container_width=True, key="country_chart")