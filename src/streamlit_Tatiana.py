# Streamlit live coding script
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy


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
    fig_source.add_trace(px.scatter_mapbox(df_location_filtering, lat='lat', lon='lon', size='production', hover_name="municipality", hover_data=["canton","production", "project_name","company"]).data[0])
    fig_source.update_traces(marker=dict(color='yellow', opacity=0.7),
                  selector=dict(mode='markers'))

st.plotly_chart(fig_source)  





mpg_df_raw = load_data(path="./data/mpg.csv")
mpg_df = deepcopy(mpg_df_raw)

# Add title and header
st.title("Introduction to Streamlit")
st.header("MPG Data Exploration")

# Widgets: checkbox (you can replace st.xx with st.sidebar.xx)
if st.checkbox("Show Dataframe"):
    st.subheader("This is my dataset:")
    st.dataframe(data=mpg_df)
    # st.table(data=mpg_df)

# Setting up columns
left_column, middle_column, right_column = st.columns([3, 1, 1])

# Widgets: selectbox
years = ["All"]+sorted(pd.unique(mpg_df['year']))
year = left_column.selectbox("Choose a Year", years)

# Widgets: radio buttons
show_means = middle_column.radio(
    label='Show Class Means', options=['Yes', 'No'])

plot_types = ["Matplotlib", "Plotly"]
plot_type = right_column.radio("Choose Plot Type", plot_types)

# Flow control and plotting
if year == "All":
    reduced_df = mpg_df
else:
    reduced_df = mpg_df[mpg_df["year"] == year]

means = reduced_df.groupby('class').mean(numeric_only=True)

# In Matplotlib
m_fig, ax = plt.subplots(figsize=(10, 8))
ax.scatter(reduced_df['displ'], reduced_df['hwy'], alpha=0.7)

if show_means == "Yes":
    ax.scatter(means['displ'], means['hwy'], alpha=0.7, color="red")

ax.set_title("Engine Size vs. Highway Fuel Mileage")
ax.set_xlabel('Displacement (Liters)')
ax.set_ylabel('MPG')

# In Plotly
p_fig = px.scatter(reduced_df, x='displ', y='hwy', opacity=0.5,
                   range_x=[1, 8], range_y=[10, 50],
                   width=750, height=600,
                   labels={"displ": "Displacement (Liters)",
                           "hwy": "MPG"},
                   title="Engine Size vs. Highway Fuel Mileage")
p_fig.update_layout(title_font_size=22)

if show_means == "Yes":
    p_fig.add_trace(go.Scatter(x=means['displ'], y=means['hwy'],
                               mode="markers"))
    p_fig.update_layout(showlegend=False)

# Select which plot to show
if plot_type == "Matplotlib":
    st.pyplot(m_fig)
else:
    st.plotly_chart(p_fig)

# We can write stuff
url = "https://archive.ics.uci.edu/ml/datasets/auto+mpg"
st.write("Data Source:", url)
# "This works too:", url

# Another header
st.header("Maps")

# Sample Streamlit Map
st.subheader("Streamlit Map")
ds_geo = px.data.carshare()
ds_geo['lat'] = ds_geo['centroid_lat']
ds_geo['lon'] = ds_geo['centroid_lon']
st.map(ds_geo)

# Sample Choropleth mapbox using Plotly GO
st.subheader("Plotly Map")

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                 dtype={"fips": str})

plotly_map = go.Figure(go.Choroplethmapbox(geojson=counties,
                                           locations=df.fips,
                                           z=df.unemp,
                                           colorscale="Viridis",
                                           zmin=0, zmax=12,
                                           marker={"opacity": 0.5, "line_width": 0}))
plotly_map.update_layout(mapbox_style="carto-positron",
                         mapbox_zoom=3,
                         mapbox_center={"lat": 37.0902, "lon": -95.7129},
                         margin={"r": 0, "t": 0, "l": 0, "b": 0})

st.plotly_chart(plotly_map)
