import streamlit as st
import plotly.express as px
import geemap.foliumap as geemap
import folium
import data.data as data
from maps.visualization import get_palette
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

#https://fontawesome.com/icons?d=gallery

def create_line_chart(data, title):
   fig = make_subplots(specs=[[{"secondary_y": True}]])
   fig.add_trace(go.Bar(x=data['Date'], y=data['Precip'], name='Precipitation', marker=dict(color='#5fcdd9')), secondary_y=False)
   fig.add_trace(go.Scatter(x=data['Date'], y=data['Temp'], mode='lines+markers', name='Temperature', line=dict(color='red')), secondary_y=True)

   fig.update_layout(title=title,
                     xaxis_title='Date', legend=dict(orientation="h", yanchor="top", y=1.07))
   fig.update_yaxes(title_text="Precipitation (mm)", secondary_y=False)
   fig.update_yaxes(title_text="Temperature (°C)", secondary_y=True)
   
   st.plotly_chart(fig, use_container_width=True)


def create_meteo_map():
   meteo_df = data.get_stations_info()
   points_data = [
    {'coordinates': [meteo_df['Latitude'][0], meteo_df['Longitude'][0]], 'name': 'Legnica'},
    {'coordinates': [meteo_df['Latitude'][1], meteo_df['Longitude'][1]], 'name': 'Jelenia Gora'},
    {'coordinates': [meteo_df['Latitude'][2], meteo_df['Longitude'][2]], 'name': 'Bertsdorf-Hornitz'},
    {'coordinates': [meteo_df['Latitude'][3], meteo_df['Longitude'][3]], 'name': 'Liberec'},
    {'coordinates': [meteo_df['Latitude'][4], meteo_df['Longitude'][4]], 'name': 'Ostritz'}
   ]
   
   Map = geemap.Map(basemap="Esri.WorldGrayCanvas", center=(50.95, 15.7), zoom=8)

   for point in points_data:
      icon = folium.Icon(color='red', icon='cloud-sun-rain', icon_color="lightblue", prefix='fa')
      marker = folium.Marker(location=point['coordinates'], popup=point['name'], icon=icon)
      Map.add_child(marker)
   Map.addLayer(data.selected_units, {}, "Research area")  

   Map.to_streamlit(height=250)


def create_multi_year_chart(data, series, meteo_attribute, title):
   data = pd.DataFrame(data)
   data['Date'] = pd.to_datetime(data['Date'])
   data['Day of Year'] = data['Date'].dt.dayofyear
   data['Month'] = data['Date'].dt.month
   data['Year'] = data['Date'].dt.year

   series = 'Day of Year' if series == 'Daily' else 'Month'   

   fig = px.line(data, x=series, y=meteo_attribute, color='Year', markers=True, color_discrete_sequence=get_palette()['multi_year_chart'])
   fig.update_layout(title=title, xaxis_title=series, yaxis_title=None, 
                  legend_title=None, legend=dict(orientation="h", yanchor="top", y=1.05))
   
   st.plotly_chart(fig, use_container_width=True)