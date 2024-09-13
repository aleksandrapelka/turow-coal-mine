import streamlit as st
from maps.index_panel import index_panel 


st.set_page_config(page_title="MSAVI2", page_icon="🌱", layout="wide")
index = 'MSAVI2'
icon = "🌱"

index_panel(index, icon)