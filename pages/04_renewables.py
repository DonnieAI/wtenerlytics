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

df_raw=pd.read_csv("data/IRENA_Statistics_Extract_2025H2_csv.csv")
df=df_raw
#df = df.query("`RE or Non-RE` == 'Total Renewable'")   ` backtip!!!!
df = df[df["RE or Non-RE"] == "Total Renewable"]
df = df.fillna(0)
output_subset=["Electricity Generation (GWh)","Electricity Installed Capacity (MW)","Heat Generation (TJ)"]

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

technology_selection=(
                    df["Technology"]
                   .unique()
                   .tolist()
)

group_technology_selection=(
    df["Group Technology"]
    .unique()
    .tolist()
     
)
#✅--------------------------------------------------------------------
st.title(f" ☀️ Renewable Energy")
st.markdown("""
            ### 📊 Electricity generation is based on gross electrical output.
            #### data in TWh
            
            """)
st.markdown(""" 
            source: Irena 2024
                        """)



# Sort the country_selection list alphabetically
sorted_countries = sorted(country_selection)
selected_country = st.selectbox(
    "Select a Country or an Aggregate (Total World as default)",  # label
    options=sorted_countries,
    index=sorted_countries.index("Italy")  # 👈 set default selection by index
)

filtered_zero=df[df["Country"] == selected_country]
group_technology_selection_sorted=sorted(group_technology_selection)
selected_group_technology= st.selectbox(
    "Select a Group Technology  (Bioenergy as default)",  # label
    options=group_technology_selection_sorted,
    #index=group_technology_selection_sorted.index("Bioenergy")  # 👈 set default selection by index
)

filtered_one = filtered_zero[filtered_zero["Group Technology"] == selected_group_technology]
technology_selection_sorted=sorted(filtered_one["Technology"].unique().tolist())
selected_technology= st.selectbox(
    "Select a Technology",  # label
    options=technology_selection_sorted,
    #index=technology_selection_sorted.index("Biogas")  # 👈 set default selection by index
)

# 2️⃣ Filter df based on selected Technology
filtered_two = filtered_one[filtered_one["Technology"] == selected_technology]
sub_technology_options = sorted(filtered_two["Sub-Technology"].unique().tolist())
selected_sub_technology = st.selectbox(
    f"Select a Sub-Technology for {selected_technology}",
    options=sub_technology_options,
    #index=sub_technology_options.index("Biogas n.e.s.")
)

filtered_three=filtered_two[filtered_two["Sub-Technology"] == selected_sub_technology]
producer_type_options = sorted(filtered_three["Producer Type"].unique().tolist())
selected_producer_type = st.selectbox(
    f"Select a Sub-Technology for {selected_sub_technology}",
    options=producer_type_options,
    #index=producer_type_options.index("Heat (Commercial)")
)

df_filtered=filtered_three[filtered_three["Producer Type"]==selected_producer_type]
df_filtered = df_filtered.set_index("Year", drop=False)

#----------------------------------------------------------------------
st.markdown("---")  # horizontal line separator
#----------------------------------------------------------------------
# List of possible generation columns
generation_columns = ["Electricity Generation (GWh)", "Heat Generation (TJ)"]
color_map = {
    "Electricity Generation (GWh)": "#1f77b4",  # ⚡ Blue tone for electricity
    "Heat Generation (TJ)": "#ff7f0e"           # 🔥 Orange tone for heat
}

# Find the column that has non-NaN values
selected_column = next(
    (col for col in generation_columns if (df_filtered[col] != 0).any()),
    None  # fallback if all are zero
)
# ✅ Handle missing data safely
if not selected_column:
    st.warning("⚠️ No generation data available for this combination. Please try a different selection.")
    st.stop()


#-------------------------------------------------------

last_value=df_filtered[selected_column].iloc[-1]
data_to_plot = df_filtered[selected_column].copy()
last_year = data_to_plot.index.max()


col1, col2, col3= st.columns(3)

with col1:
    st.markdown(
        f"""
        <div style='background-color: #005680; padding: 30px; border-radius: 10px; text-align: center;'>
            <h3>{selected_country} | {selected_sub_technology} | {selected_column} </h3>
            <h1 style='color: #D5D8DC;'>{last_value:.0f} </h1>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div style='background-color: #005680; padding: 30px; border-radius: 10px; text-align: center;'>
            <h3>{selected_country} | {selected_sub_technology} | {selected_column} </h3>
            <h1 style='color: #D5D8DC;'>{last_value:.0f} </h1>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:
    st.markdown(
        f"""
        <div style='background-color: #005680; padding: 30px; border-radius: 10px; text-align: center;'>
            <h3>{selected_country} | {selected_sub_technology} | {selected_column} </h3>
            <h1 style='color: #D5D8DC;'>{last_value:.0f} </h1>
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
        f"{selected_country}|{selected_group_technology} | {selected_technology} | {selected_sub_technology} | {selected_producer_type}",
        f"Share component of {selected_producer_type}[%]"
    )
)

# 1. Copy the selected column into a new series


# 2. Calculate YoY % change before dropping last year
df_filtered["yoy_change_pct"] = df_filtered[selected_column].pct_change() * 100
df_filtered["yoy_change_pct"] = df_filtered["yoy_change_pct"].fillna(0)

# 3. Trim both series if the last year is 0

if data_to_plot.loc[last_year] == 0:
    data_to_plot = data_to_plot.drop(index=last_year)
    df_filtered = df_filtered.drop(index=last_year)  # drop same year from entire df

fig.add_trace(
    go.Bar(
        x=df_filtered.index,
        y=data_to_plot,
        name=selected_column,
        #name=selected_column.replace("_", " ").title(),
        #fill='tozeroy',
        marker_color=color_map[selected_column]  # 👈 dynamic color
    ),
    row=1,
    col=1
)

fig.add_trace(
    go.Scatter(
        x=df_filtered.index,
        y=data_to_plot,  # Convert MtCO2 → GtCO2
        mode="lines+markers",  # Add markers if you want dots on the line
        name=f"Total {selected_column} (line)",
        line=dict(
                color=color_map.get(selected_column, "#000"), 
                width=2, 
                dash="dash") , # Optional styling
        marker=dict(
                color=color_map.get(selected_column, "#000"),  # same as line color or choose different
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


fig.add_trace(
    go.Bar(
        x=df_filtered.index,
        y=df_filtered["yoy_change_pct"],
        name="YoY Change (%)",
        marker_color=[
            "#F5B7B1" if v < 0 else "#A9DFBF"
            for v in df_filtered["yoy_change_pct"]
        ]
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
    title_text=selected_column,
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
st.plotly_chart(fig, use_container_width=True, key="renewable_chart")


#----------------------------------------------------------------------
st.markdown("---")  # horizontal line separator
#----------------------------------------------------------------------

# Prepare CSV for download
csv = df_filtered.to_csv(index=True).encode("utf-8")

# Download button
st.download_button(
    label=f"⬇️ Renewable focus | {selected_sub_technology} | {selected_country} ",
    data=csv,
    file_name=f"Renewable focus_{selected_sub_technology}_{selected_country}.csv",
    mime="text/csv",
)
