import streamlit as st
from maps.index_panel import index_panel 


st.set_page_config(page_title="NDWI_II", page_icon="💧", layout="wide")
index = 'NDWI_II'
icon = "💧"

index_panel(index, icon)