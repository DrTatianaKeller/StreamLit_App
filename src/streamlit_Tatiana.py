# Streamlit live coding script
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy
from scicolorscales import *

# First some MPG Data Exploration
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

# Start your code here
df=pd.read_csv('./data/renewable_power_plants_CH.csv')
df_canton=df[df["energy_source_level_2"] == "Solar"].groupby('canton').size() #.agg({'energy_source_level_2':"size"})

#df_canton

df['canton']=df['canton'].map({
'TG':'Thurgau', 
'GR':'Graubünden', 
'LU':'Luzern', 
'BE':'Bern', 
'VS':'Valais',                
'BL':'Basel-Landschaft', 
'SO':'Solothurn', 
'VD':'Vaud', 
'SH':'Schaffhausen', 
'ZH':'Zürich', 
'AG':'Aargau', 
'UR':'Uri', 
'NE':'Neuchâtel', 
'TI':'Ticino', 
'SG':'St. Gallen', 
'GE':'Genève',
'GL':'Glarus', 
'JU':'Jura', 
'ZG':'Zug', 
'OW':'Obwalden', 
'FR':'Fribourg', 
'SZ':'Schwyz', 
'AR':'Appenzell Ausserrhoden', 
'AI':'Appenzell Innerrhoden', 
'NW':'Nidwalden', 
'BS':'Basel-Stadt'})










df_canton_prod_solar=df[df["energy_source_level_2"] == "Solar"].groupby('canton').agg({'production':"sum"})
#df_canton_prod_solar

df_canton_prod_hydro=df[df["energy_source_level_2"] == "Hydro"].groupby('canton').agg({'production':"sum"})
#df_canton_prod_hydro

df_canton_prod_wind=df[df["energy_source_level_2"] == "Wind"].groupby('canton').agg({'production':"sum"})
#df_canton_prod_wind

df_canton_prod_bio=df[df["energy_source_level_2"] == "Bioenergy"].groupby('canton').agg({'production':"sum"})
#df_canton_prod_bio

df_canton_prod_total=df.groupby('canton').agg({'production':"sum"})
#df_canton_prod_total



with open("./data/georef-switzerland-kanton.geojson") as response:
    geojson = json.load(response)


st.header("Renewable Sources Energy Production in Cantons of Switzerland")
url = "https://data.open-power-system-data.org/renewable_power_plants/2020-08-25/"
st.write("Data Source:", url)

# Setting up columns
left_column, right_column = st.columns([2, 1])


# Widgets: selectbox
sources = ["All"]+sorted(pd.unique(df["energy_source_level_2"]))
source = left_column.selectbox("Choose an Energy Source", sources)

# Flow control and plotting
if source == "All":
    df_canton_prod = df.groupby('canton').agg({'production':"sum"})
    df_location=df
else:
    df_canton_prod = df[df["energy_source_level_2"] == source].groupby('canton').agg({'production':"sum"})

    df_location = df[df["energy_source_level_2"] == source]

df_location_filtering = df_location[df_location['production'] >= 0]

# Widgets: radio buttons
show_sources = right_column.radio(
    label='Show Sources Position', options=['Yes', 'No'])

#Production of energy per canton

fig_source = px.choropleth_mapbox(df_canton_prod, geojson=geojson, featureidkey='properties.kan_name', title=f"Total {source} Energy Production per Canton",
                           locations=df_canton_prod.index, color="production", height=500, opacity=0.7)

fig_source.update_layout(mapbox_style="carto-positron",
                 mapbox_zoom=6, mapbox_center = {"lat": 46.8182, "lon": 8.2275})
fig_source.update_layout(margin={"r":0,"t":50,"l":0,"b":0})
#fig.update_layout(title_text = "Total Hydro Energy Production per Canton")
if show_sources == "Yes":
    if source == "All":
        fig_source.add_trace(px.scatter_mapbox(df_location_filtering, lat='lat', lon='lon', size='production', hover_name="municipality", hover_data=["canton","production", "project_name","company","energy_source_level_2"]).data[0])
        fig_source.update_traces(marker=dict(color='yellow', opacity=0.7),
                  selector=dict(mode='markers'))
    else:
        fig_source.add_trace(px.scatter_mapbox(df_location_filtering, lat='lat', lon='lon', size='production', hover_name="municipality", hover_data=["canton","production", "project_name","company"]).data[0])
        fig_source.update_traces(marker=dict(color='yellow', opacity=0.7),
                  selector=dict(mode='markers'))
        
st.plotly_chart(fig_source)  

