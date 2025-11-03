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
df_raw=pd.read_csv("data/panel.csv")
df=df_raw


#✅------------------------DATA ELABORATION---------------------------------------------

#GHG EMISSIONS
#Selection : Country --> stacked bar graph along years

oil_products_subset = [
                    "diesel_gasoil_cons_kbd",
                    "fuel_oil_cons_kbd",
                    "gasoline_cons_kbd",
                    "kerosene_cons_kbd",
                    "light_dist_cons_kbd",
                    "lpg_cons_kbd",
                    "middle_dist_cons_kbd",
                    "naphtha_cons_kbd"
                ]


oil_products_name_mapping = {
        "diesel_gasoil_cons_kbd": "diesel",
        "fuel_oil_cons_kbd": "fuel_oil",
        "gasoline_cons_kbd": "gasoline",
        "kerosene_cons_kbd": "kerosene",
        "light_dist_cons_kbd": "light_distillates",
        "lpg_cons_kbd": "lpg",
        "middle_dist_cons_kbd": "middle_distillates",
        "naphtha_cons_kbd": "naphtha"
    }



refinery_subset=[
                    "refcap_kbd",
                    "refthru_kbd",
                ]


color_map = {
            # 🚛 Oil Products Consumption (warm tones)
            "diesel_gasoil_cons_kbd": "#E59866",   # burnt orange
            "fuel_oil_cons_kbd":      "#CA6F1E",   # heavy oil - dark amber
            "gasoline_cons_kbd":      "#F5B041",   # gasoline - golden yellow
            "kerosene_cons_kbd":      "#DC7633",   # jet fuel - copper
            "light_dist_cons_kbd":    "#FAD7A0",   # light distillates - pale orange
            "lpg_cons_kbd":           "#F0B27A",   # LPG - light brown/orange
            "middle_dist_cons_kbd":   "#E67E22",   # middle distillates - orange
            "naphtha_cons_kbd":       "#F4D03F",   # naphtha - yellow

            # 🏭 Refinery metrics (neutral/industrial tones)
            "refcap_kbd":             "#85929E",   # steel grey-blue (refinery capacity)
            "refthru_kbd":            "#5D6D7E"    # darker grey-blue (throughput)
}

country_selection=(
                    df["Country"]
                   .unique()
                   .tolist()
)

year_thresold=1990


#✅--------------------------------------------------------------------
st.title("🛢️ Oil Products Consumption & 🏭 Refinery Metrics")
st.markdown("""
            ### 📊 🛢️ Oil Products Consumption & 🏭 Refinery Metrics
            #### data in thousand of barrels of oil per day [kbpd]
            
            """)
st.markdown(""" 
            source: Energy Institute (2024), Country Transition Tracker 2024, Energy Institute, London.
                        """)

selected_country = st.selectbox(
    "Select a Country or an Aggregate (Total World as default)",  # label
    options=country_selection,
    index=country_selection.index("Total World")  # 👈 set default selection by index
)

selected_oil_products=st.selectbox(
        "Select a Oil product (Diesel as default)",  # label
    options=oil_products_subset,
    index=oil_products_subset.index("diesel_gasoil_cons_kbd")  # 👈 set default selection by index
)
    

# **************************************************************************************
#selection for the different energy in EJ
df_filtered= (
    df
    .query("Country == @selected_country and Year >= @year_thresold")
    .set_index("Year")
    .sort_index()
    [oil_products_subset + refinery_subset]  
     #.assign(yoy_change_pct=lambda x: x["co2_mtco2"].pct_change().fillna(0) * 100)# Select specific columns here
)
# **************************************************************************************

label=oil_products_name_mapping[selected_oil_products]
latest_data_produced = df_filtered[selected_oil_products].iloc[-1]
latest_refinery_capacity=df_filtered[refinery_subset[0]].iloc[-1]
latest_refinery_output=df_filtered[refinery_subset[1]].iloc[-1]


col1, col2, col3= st.columns(3)

with col1:
    st.markdown(
        f"""
        <div style='background-color: #005680; padding: 30px; border-radius: 10px; text-align: center;'>
            <h3>{label} consumption</h3>
            <h1 style='color: #D5D8DC;'>{latest_data_produced:.0f} kbpd</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div style='background-color: #005680; padding: 30px; border-radius: 10px; text-align: center;'>
           <h3>Refinery capacity </h3>
            <h1 style='color: #D5D8DC;'>{latest_refinery_capacity:.0f} kbpd</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div style='background-color: #005680; padding: 30px; border-radius: 10px; text-align: center;'>
           <h3>Refinery output </h3>
            <h1 style='color: #D5D8DC;'>{latest_refinery_output:.0f} kbpd</h1>
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
        f"Oil product consumption [kbpd] - {label} | {selected_country}",
        "Refinery Capacity and Output [kbpd]"
    )
)


fig.add_trace(
    go.Scatter(
        x=df_filtered.index,
        y=df_filtered[selected_oil_products],  # Convert MtCO2 → GtCO2
        mode="lines",  # Add markers if you want dots on the line
        name="{label} - consumption ",
        fill='tozeroy',
        line=dict(
                color=color_map.get(selected_oil_products, "#000"), 
                width=2, 
                dash="dash") , # Optional styling
        
        ),
        row=1,
        col=1
)

refinery_subset=[
                    "refcap_kbd",
                    "refthru_kbd",
                ]


# Add fug 2 in thge subplot
fig.add_trace(
    go.Bar(
        x=df_filtered.index,
        y=df_filtered[refinery_subset[0]],
        name=refinery_subset[0], 
        marker_color=color_map.get(refinery_subset[0], "#ccc")# Use dynamic name

    ),
    row=2,
    col=1
)
# Second bar (refinery_subset[1])
fig.add_trace(
    go.Bar(
        x=df_filtered.index,
        y=df_filtered[refinery_subset[1]],
        name=refinery_subset[1], 
        marker_color=color_map.get(refinery_subset[1], "#ccc")# Use dynamic name
    ),
    row=2,
    col=1
)

# Important: Set barmode to 'group' (not 'stack')
fig.update_layout(barmode='group')

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
    label=f"⬇️ Download data for Oil Products | {selected_country} ",
    data=csv,
    file_name=f"Oil_Products_{selected_country}.csv",
    mime="text/csv",
)