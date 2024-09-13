import streamlit as st
from maps.index_panel import index_panel 


st.set_page_config(page_title="MSI", page_icon="💧", layout="wide")
index = 'MSI'
icon = "💧"

index_panel(index, icon)