import streamlit as st
from maps.indexes import add_image_to_map, get_classified_image
from maps.charts import create_line_chart, create_multi_year_chart, create_histogram, create_multi_year_histogram, multi_histogram
from data.data import get_statistics_data, get_imagery_collections, daily_multihist, weekly_multihist, monthly_multihist


def index_panel(index, icon):
    tab1, tab2, tab3, tab4 = st.tabs(["📆 Daily", "📆 Weekly", "📆 Monthly", "📉 Statistics"])
    stats = get_statistics_data(index)
    collections = get_imagery_collections(index)

    with tab1:
        st.subheader(f"Daily {index} Time Series")
        selected_date = st.select_slider('Select date:', options=stats['daily']['Date'], value=stats['daily']['Date'][int(len(stats['daily']['Date'])/4)])

        col1, col2 = st.columns((1, 3))
        with st.container():
            with col1:
                st.dataframe(stats['daily'], hide_index=True, use_container_width=True, height=250)
                create_histogram(index, selected_date, collections['daily_collection'])
            with col2:
                image = get_classified_image(index, selected_date, collections['daily_collection'])
                add_image_to_map(image, index, f'{index} {selected_date}')
    
    with tab2:
        st.subheader(f"Weekly {index} Time Series")
        selected_date = st.select_slider('Select date:', options=stats['weekly']['Date'], value=stats['weekly']['Date'][int(len(stats['weekly']['Date'])/4)])

        col1, col2 = st.columns((1, 3))
        with st.container():
            with col1:
                st.dataframe(stats['weekly'], hide_index=True, use_container_width=True, height=250)
                create_histogram(index, selected_date, collections['weekly_collection'])
            with col2:
                image = get_classified_image(index, selected_date, collections['weekly_collection'])
                add_image_to_map(image, index, f'{index} {selected_date}')

    with tab3:
        st.subheader(f"Monthly {index} Time Series")
        selected_date = st.select_slider('Select date:', options=stats['monthly']['Date'], value=stats['monthly']['Date'][int(len(stats['monthly']['Date'])/4)])

        col1, col2 = st.columns((1, 3))
        with st.container():
            with col1:
                st.dataframe(stats['monthly'], hide_index=True, use_container_width=True, height=250)
                create_histogram(index, selected_date, collections['monthly_collection'])
            with col2:
                image = get_classified_image(index, selected_date, collections['monthly_collection'])
                add_image_to_map(image, index, f'{index} {selected_date}')

    with tab4:
        with st.expander(f"{icon} See {index} daily series statistics:"):     
            create_line_chart(index, stats['daily'], 'Daily') 
            
            tab_mean, tab_median, tab_mode = st.tabs(["📉 Mean", "📉 Median", "📉 Mode"])
            with tab_mean:
                create_multi_year_histogram(index, 'mean', stats['daily'], '- daily collection') 
            with tab_median:
                create_multi_year_histogram(index, 'median', stats['daily'], '- daily collection') 
            with tab_mode:
                create_multi_year_histogram(index, 'mode', stats['daily'], '- daily collection') 

            tab_mean1, tab_median1, tab_mode1 = st.tabs(["📉 Mean", "📉 Median", "📉 Mode"])
            with tab_mean1:
                create_multi_year_chart(index, 'mean', stats['daily'], 'Day of Year', '- daily collection') 
            with tab_median1:
                create_multi_year_chart(index, 'median', stats['daily'], 'Day of Year', '- daily collection') 
            with tab_mode1:
                create_multi_year_chart(index, 'mode', stats['daily'], 'Day of Year', '- daily collection') 

            multi_histogram(index, daily_multihist, '- daily collection')

        with st.expander(f"{icon} See {index} weekly series statistics:"):
            create_line_chart(index, stats['weekly'], 'Weekly')

            tab_mean2, tab_median2, tab_mode2 = st.tabs(["📉 Mean", "📉 Median", "📉 Mode"])
            with tab_mean2: 
                create_multi_year_histogram(index, 'mean', stats['weekly'], '- weekly collection')
            with tab_median2:
                    create_multi_year_histogram(index, 'median', stats['weekly'], '- weekly collection')
            with tab_mode2:
                    create_multi_year_histogram(index, 'mode', stats['weekly'], '- weekly collection')

            tab_mean3, tab_median3, tab_mode3 = st.tabs(["📉 Mean", "📉 Median", "📉 Mode"])
            with tab_mean3: 
                create_multi_year_chart(index, 'mean', stats['weekly'], 'Day of Year', '- weekly collection')
            with tab_median3: 
                create_multi_year_chart(index, 'median', stats['weekly'], 'Day of Year', '- weekly collection')
            with tab_mode3: 
                create_multi_year_chart(index, 'mode', stats['weekly'], 'Day of Year', '- weekly collection')

            multi_histogram(index, weekly_multihist, '- weekly collection')

        with st.expander(f"{icon} See {index} monthly series statistics:"):
            create_line_chart(index, stats['monthly'], 'Monthly') 

            tab_mean4, tab_median4, tab_mode4 = st.tabs(["📉 Mean", "📉 Median", "📉 Mode"])
            with tab_mean4: 
                create_multi_year_histogram(index, 'mean', stats['monthly'], '- monthly collection')
            with tab_median4: 
                create_multi_year_histogram(index, 'median', stats['monthly'], '- monthly collection')
            with tab_mode4: 
                create_multi_year_histogram(index, 'mode', stats['monthly'], '- monthly collection')

            tab_mean5, tab_median5, tab_mode5 = st.tabs(["📉 Mean", "📉 Median", "📉 Mode"])
            with tab_mean5: 
                create_multi_year_chart(index, 'mean', stats['monthly'], 'Month', '- monthly collection')  
            with tab_median5: 
                create_multi_year_chart(index, 'median', stats['monthly'], 'Month', '- monthly collection')                
            with tab_mode5: 
                create_multi_year_chart(index, 'mode', stats['monthly'], 'Month', '- monthly collection')  

            multi_histogram(index, monthly_multihist, '- monthly collection')    

    