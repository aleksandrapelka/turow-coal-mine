import streamlit as st
from maps.index_panel import index_panel 


st.set_page_config(page_title="NDVI", page_icon="🌱", layout="wide")
index = 'NDVI'
icon = "🌱"

index_panel(index, icon)