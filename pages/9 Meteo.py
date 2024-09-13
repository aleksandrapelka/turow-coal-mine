import streamlit as st
from maps.meteo import create_line_chart, create_meteo_map, create_multi_year_chart
import data.data as data
from data.data import get_meteostat_data, get_stations_info

st.set_page_config(page_title="Meteo", page_icon="🌦️", layout="wide")

st.title('🌦️ Meteo')
st.divider()
st.link_button("Source", "https://dev.meteostat.net/python/monthly.html#example")
stations_names = ['Legnica', 'Jelenia Góra', 'Bertsdorf-Hörnitz', 'Liberec', 'Ostritz']


def meteo_panel(station_name, data, series_name):
    st.dataframe(data[["Date", "Temp", "Precip", "Name"]], hide_index=True, use_container_width=True, height=250)
    create_line_chart(data, f'{series_name} precipitation totals [mm] and {series_name} average temperature values [°C] - {station_name}')
    create_multi_year_chart(data, series_name, 'Temp', f'{series_name} average temperature values [°C] - {station_name}')
    create_multi_year_chart(data, series_name, 'Precip', f'{series_name} precipitation totals [mm] - {station_name}')


col1, col2 = st.columns((2, 3))
with st.container():
    with col1:
        st.dataframe(get_stations_info(), hide_index=True, use_container_width=True, height=250)
    with col2:    
        create_meteo_map()

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🌤️ Legnica", "🌤️ Jelenia Góra", "🌤️ Bertsdorf-Hörnitz", "🌤️ Liberec", "🌤️ Ostritz"])

with tab1:
    name = stations_names[0]
    
    st.subheader(f"🌤️ {name} synoptic station - daily data")
    meteo_panel(name, data.legnica_meteo, 'Daily') 

    st.subheader(f"🌤️ {name} synoptic station - monthly data")
    meteo_panel(name, data.legnica_meteo_m, 'Monthly')


with tab2:
    name = stations_names[1]

    st.subheader(f"🌤️ {name} synoptic station - daily data")
    meteo_panel(name, data.jelenia_gora_meteo, 'Daily') 

    st.subheader(f"🌤️ {name} synoptic station - monthly data")
    meteo_panel(name, data.jelenia_gora_meteo_m, 'Monthly')


with tab3:
    name = stations_names[2]
    meteostat_data = get_meteostat_data('Daily')[0]
    meteostat_data_m = get_meteostat_data('Monthly')[0]

    st.subheader(f"🌤️ {name} synoptic station - daily data")
    meteo_panel(name, meteostat_data, 'Daily') 

    st.subheader(f"🌤️ {name} synoptic station - monthly data")
    meteo_panel(name, meteostat_data_m, 'Monthly')


with tab4:
    name = stations_names[3]
    meteostat_data = get_meteostat_data('Daily')[2]
    meteostat_data_m = get_meteostat_data('Monthly')[2]

    st.subheader(f"🌤️ {name} synoptic station - daily data")
    meteo_panel(name, meteostat_data, 'Daily') 

    st.subheader(f"🌤️ {name} synoptic station - monthly data")
    meteo_panel(name, meteostat_data_m, 'Monthly')


with tab5:
    name = stations_names[4]
    meteostat_data = get_meteostat_data('Daily')[1]
    meteostat_data_m = get_meteostat_data('Monthly')[1]

    st.subheader(f"🌤️ {name} synoptic station - daily data")
    meteo_panel(name, meteostat_data, 'Daily') 

    st.subheader(f"🌤️ {name} synoptic station - monthly data")
    meteo_panel(name, meteostat_data_m, 'Monthly')