import streamlit as st
from streamlit_option_menu import option_menu


st.set_page_config(page_title="Turów Coal Mine", page_icon="⚒️", layout="wide") 

st.title('⚒️ Turów Coal Mine')

st.markdown("""
    <p style='font-size:22px'>
    The Turów Brown Coal Mine, located in the southwestern part of the Lower Silesian Voivodeship, between the borders of the Czech Republic and Germany, is one of the most important and oldest mines in Poland. The brown coal deposits in the Turoszów Basin are among the richest in the country. Turów Mine is owned by the company PGE Mining and Conventional Energy. The surface area of the open-pit mine covers 2,487 hectares, and its annual coal extraction is estimated at around 8 million tons.
    </p><br>
    """, unsafe_allow_html=True)

cols_empty1, cols1, cols2, cols_empty2 = st.columns((0.8, 2, 2, 0.5)) 
with cols1:
    st.image("base map.png", caption="Overview map of the study area with key elements highlighted", width=600)
with cols2:  
    st.image("land cover.png", caption="Map of the study area presenting various land cover types", width=558)

