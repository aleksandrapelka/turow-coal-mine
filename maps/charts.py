import ee
import streamlit as st
import pandas as pd
import ast
import plotly.express as px
import data.data as data
from maps.indexes import get_image, projection
from maps.visualization import get_breaks, get_palette, get_labels


def create_line_chart(index_name, data, series_name):
   fig = px.line(data, x='Date', y=[f'{index_name}_mean', f'{index_name}_median', f'{index_name}_mode'], markers=True, color_discrete_sequence=get_palette()['line_chart'])
   fig.update_layout(title=f'{series_name} {index_name} Time Series', xaxis_title='Date', yaxis_title=None,
                   legend_title=None, legend=dict(orientation="h", yanchor="top", y=1.05))
   
   st.plotly_chart(fig, use_container_width=True)  


def create_multi_year_chart(index_name, statistic_name, data, series, series_name):
   data = pd.DataFrame(data)
   data['Date'] = pd.to_datetime(data['Date'])
   data['Day of Year'] = data['Date'].dt.dayofyear
   data['Month'] = data['Date'].dt.month
   data['Year'] = data['Date'].dt.year

   if series != 'Month': 
      series = 'Day of Year'
  
   fig = px.line(data, x=series, y=f'{index_name}_{statistic_name}', color='Year', markers=True, color_discrete_sequence=get_palette()['multi_year_chart'])
   fig.update_layout(title=f'{index_name} time series by year ({statistic_name}) {series_name}', xaxis_title=series, yaxis_title=None, legend_title=None, legend=dict(orientation="h", yanchor="top", y=1.05))
   
   st.plotly_chart(fig, use_container_width=True)


def create_multi_year_histogram(index_name, statistic_name, data, series_name):
   data['Date'] = pd.to_datetime(data['Date'])
   data['Year'] = data['Date'].dt.year
   obs_per_year = data.groupby('Year').size().reset_index(name='obs_count')
   fig = px.bar(x=data['Date'], y=data[f'{index_name}_{statistic_name}'])
   fig.update_layout(title=f'Histogram of {index_name} ({statistic_name}) {series_name}', xaxis_title='Date', yaxis_title=None)
   fig.update_traces(marker_color=get_palette()['multi_year_histogram'])

   for i, row in obs_per_year.iterrows():
      fig.add_annotation(x=pd.to_datetime(str(row['Year'])), y=0,
                        text=f"Count: {row['obs_count']}", showarrow=False, xshift=10, yshift=300)
      
   st.plotly_chart(fig, use_container_width=True) 


def create_histogram(index_name, date, collection):
   image = get_image(index_name, date, collection)
   index_data = image.reduceRegion(reducer=ee.Reducer.toList(), geometry=data.selected_units.geometry(),scale=1000,maxPixels=1e12).get(index_name).getInfo()

   df = pd.DataFrame({index_name: index_data})
   df['Class'] = pd.cut(df[index_name], bins=get_breaks()[index_name], labels=get_labels()[index_name], ordered=True)

   class_counts = df['Class'].value_counts().reset_index()
   class_counts.columns = ['Class', 'Count']

   fig = px.bar(class_counts, x='Class', y='Count', color='Class', 
                color_discrete_sequence=get_palette()[index_name], 
                category_orders={'Class': get_labels()[index_name]}, height=350)
   fig.update_layout(title=f'Histogram of {index_name} (scale: 1000 m) - {date}', 
                     xaxis_title=None, yaxis_title=None, showlegend=False)

   st.plotly_chart(fig, use_container_width=True)


def get_image_classes(image, index_name):
   breaks = get_breaks()[index_name]
   image = image.reproject(crs=projection['crs'], crsTransform=projection['transform'])
   classes = []
   
   for i in range(len(breaks) - 1):
      image_class = image.gt(breaks[i]).And(image.lte(breaks[i+1])).rename(f'Class_{i+1}')
      image_class = image_class.reduceRegion(reducer=ee.Reducer.sum(), geometry=data.selected_units.geometry(), scale=10)
      classes.append(image_class)

   return classes
   

def multi_histogram(index_name, collection, series_name):
   list_of_dicts = []

   for _, dict in collection[index_name].items():
      list_of_dicts.append(ast.literal_eval(dict))

   df = pd.DataFrame(list_of_dicts)

   fig = px.bar(df, x='Date', y=df.columns[1:], barmode='stack', color_discrete_sequence=get_palette()[index_name])
   fig.update_layout(title=f'Multi-year {index_name} histogram by class {series_name}', 
                     xaxis_title='Date', yaxis_title=None, showlegend=False)

   st.plotly_chart(fig, use_container_width=True)


def create_pie_chart(changes):
    positive = changes.updateMask(changes.eq(3)).rename('positive')
    negative = changes.updateMask(changes.eq(2)).rename('negative')
    strong_positive = changes.updateMask(changes.eq(4)).rename('strong_positive')
    strong_negative = changes.updateMask(changes.eq(1)).rename('strong_negative')
    total_changes = changes.updateMask(changes).rename('total_changes')
    
    negative = negative.reduceRegion(reducer=ee.Reducer.count(), geometry=data.selected_units.geometry(), scale=100).get('negative').getInfo()
    positive = positive.reduceRegion(reducer=ee.Reducer.count(), geometry=data.selected_units.geometry(), scale=100).get('positive').getInfo()
    strong_negative = strong_negative.reduceRegion(reducer=ee.Reducer.count(), geometry=data.selected_units.geometry(), scale=100).get('strong_negative').getInfo()
    strong_positive = strong_positive.reduceRegion(reducer=ee.Reducer.count(), geometry=data.selected_units.geometry(), scale=100).get('strong_positive').getInfo()
    total_changes = total_changes.reduceRegion(reducer=ee.Reducer.count(), geometry=data.selected_units.geometry(), scale=100).get('total_changes').getInfo()

    if total_changes > 0:
        percent_positive = (positive / total_changes) * 100
        percent_negative = (negative / total_changes) * 100
        percent_strong_positive = (strong_positive / total_changes) * 100
        percent_strong_negative = (strong_negative / total_changes) * 100
    else:
        percent_positive = 0
        percent_negative = 0
        percent_strong_positive = 0
        percent_strong_negative = 0
    
    df = pd.DataFrame({'tip': ['Strong negative changes', 'Negative changes', 'Positive changes', 'Strong positive changes'], 'percent': [percent_strong_negative, percent_negative, percent_positive, percent_strong_positive],'color': get_palette()['changes']})

    fig = px.pie(df, values='percent', names='tip', color='color', title='Changes', color_discrete_sequence=get_palette()['changes'])
    st.plotly_chart(fig, use_container_width=True)   


def create_control_point_chart(point_data, index_name, point_id):
   fig = px.line(point_data, x=point_data['id'], y=point_data[index_name], markers=True)
   fig.update_layout(title=f'Control point: {point_id} ({index_name})', xaxis_title='Date', yaxis_title=None, legend_title=None, legend=dict(orientation="h", yanchor="top", y=1.05))

   st.plotly_chart(fig, use_container_width=True)
 