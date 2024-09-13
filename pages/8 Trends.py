import streamlit as st
from data.data import get_imagery_collections, get_control_points_data
from maps.indexes import create_control_points_map
from maps.charts import create_control_point_chart


st.set_page_config(page_title="Trends", page_icon="📉", layout="wide")

series = ['daily_collection','weekly_collection','monthly_collection']
series_name = st.selectbox('Choose series:', (series))
indexes = ['NDWI_I','NDWI_II','NDVI','MSAVI2','EVI', 'NMDI','MSI']
index_name = st.selectbox('Choose index:', (indexes))

collection = get_imagery_collections(index_name)[series_name]
points, features = get_control_points_data(index_name, series_name)

points_id = list(range(0, points['point_id'].nunique(), 1))
point_id = st.selectbox('Choose control point:', (points_id))

point_data = points.loc[points['point_id'] == point_id]

cols1, cols2 = st.columns((1, 3))
with cols1:
    st.write(point_data)
with cols2:    
    create_control_points_map(features, collection, index_name)
create_control_point_chart(point_data, index_name, point_id)


col1, col2, col3 = st.columns(3)
button2_clicked = st.button('📉 See all')

charts = []
if button2_clicked:
    for i in range(0, points['point_id'].nunique(), 3):
        with col1:
            point_data = points.loc[points['point_id'] == i]
            create_control_point_chart(point_data, index_name, i)
        with col2:
            point_data = points.loc[points['point_id'] == i+1]
            create_control_point_chart(point_data, index_name, i+1)
        with col3:
            point_data = points.loc[points['point_id'] == i+2]
            create_control_point_chart(point_data, index_name, i+2)