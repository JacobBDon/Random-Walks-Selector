import streamlit as st
import pandas as pd
import time

tab1, tab2 = st.tabs(['Trip Selector', 'Itinerary Selector'])
data = pd.read_excel(https://raw.githubusercontent.com/JacobBDon/Random-Walks-Selector/main/Continents.xlsx, index_col=False)



with tab1:

    
    st.title('Chicago Booth Random Walks 2026')
    
    with st.container(border=True):

        filtertype = st.radio('**Would you like to filter or compare?**', ['Filter (show trips that share ALL selected criteria)', 'Compare (show trips that have ANY of the selected criteria)'])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        tripname = st.multiselect(label='Trip Name', options=data['Trip Name'].unique().tolist(), placeholder='')
    
    with col2:
        continent = st.multiselect(label = 'Continent', options=data['Continent'].unique().tolist(), placeholder='')
    
    with col3:
        triptype = st.multiselect(label='Trip Type', options=["FILL IN SELECTORS HERE"], placeholder='')
   
    pricelist = data['Price'].tolist()
    
    min_absolute = min(pricelist)
    max_absolute = max(pricelist)
    
    price_selected = False
    

    with st.container(border=True):
        
        if st.toggle("Select Price Range"):
             
            with st.container(border=True):

                min_price, max_price = st.slider(
                    'Trip Price',
                    min_value=min_absolute,
                    max_value=max_absolute,
                    value = (min_absolute, max_absolute),
                    label_visibility="collapsed",
                    format="$%d"
                 )
    
            price_selected = True
    
            data['in_pricerange'] = (data['Price'] >= min_price) & (data['Price'] <= max_price)
    
    cols = st.columns(5)
    ratings = []
    
    for i in range(5):
    
        with cols[i]:
    
            options = data.iloc[:, i+2].unique().tolist()
            options.sort()
            rating = st.multiselect(label=data.columns[i+2], options=options, placeholder='')
            ratings.append(rating)
    
    for i in range(5):
        checkcol = data.iloc[:, i+2]
        checkval = ratings[i]
    
        data[f'keeprating{i+1}'] = checkcol.isin(checkval)
        data[f'missingrating{i+1}'] = (not checkval)
    
    data['keeprating_or'] = (data['keeprating1'] | data['keeprating2'] | data['keeprating3'] | data['keeprating4'] | data['keeprating5']) & ~(data['missingrating1'] & data['missingrating2'] & data['missingrating3'] & data['missingrating4'] & data['missingrating5'])
    
    
    data['keeprating_and'] = (data['keeprating1'] | data['missingrating1']) & (data['keeprating2'] | data['missingrating2']) & (data['keeprating3'] | data['missingrating3']) & (data['keeprating4'] | data['missingrating4']) & (data['keeprating5'] | data['missingrating5'])
    
    filtered_data = data
    
    if (filtertype == 'Filter (keep trips that share ALL selected criteria)') and not price_selected:
        filtered_data = data[
            (
                (
                    (data['Continent'].isin(continent) | (not continent))
                    &
                    (data['Trip Name'].isin(tripname) | (not tripname))
                )
                & (data['keeprating_and'] == 1) 
            )]
    
    
    elif (filtertype == 'Filter (keep trips that share ALL selected criteria)') and price_selected:
        filtered_data = data[
            (
                (
                    (data['Continent'].isin(continent) | (not continent))
                    &
                    (data['Trip Name'].isin(tripname) | (not tripname))
                )
                & (data['keeprating_and'] == 1) 
                & (data['in_pricerange'] == 1) 
            )]
    
    

    elif (filtertype == 'Compare (keep trips that have ANY of the selected criteria)') and not price_selected:
        filtered_data = data[(
                             (data['Continent'].isin(continent))
                             | (data['Trip Name'].isin(tripname))
                             | (data['keeprating_or'] == 1)
                             )]
    
    elif (filtertype == 'Compare (keep trips that have ANY of the selected criteria)') and price_selected:
        filtered_data = data[(
                             ((data['Continent'].isin(continent))
                             | (data['Trip Name'].isin(tripname))
                             | (data['keeprating_or'] == 1))
                             & (data['in_pricerange'] == 1)
                             )]
    
    filtered_data_output = filtered_data[['Trip Name', 'Continent', 'Price', 'Nightlife', 'Physical Activity', 'Relaxation', 'Nature', 'Culture']]

    st.markdown('**To sort, press column header**')

    st.dataframe(
        filtered_data_output,
        hide_index=True
    )

with tab1:

    st.title("Activity Charts")
        
    import plotly.graph_objects as go
    
    categories = ['Nightlife', 'Physical Activity', 'Relaxation', 'Nature', 'Culture']

    if st.toggle("See trips from Trip Selector"):
        
        data_want = filtered_data

    else:

        tripname = st.multiselect('Select Trip', data['Trip Name'].unique().tolist())
        
        data_want = data[data['Trip Name'].isin(tripname)]

    cols_tab2 = st.columns(3)
    
    for i in range(len(data_want)):

        row = data_want.iloc[i]
        values = row[categories].tolist()
    
        values += values[:1]
        categories_closed = categories + categories[:1]

        fig = go.Figure()
    
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories_closed,
            fill='toself',
            name='Observation'
        ))
    
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True)),
            showlegend=False,
            width=300,
            height=300
        )
	
        if i % 3 < 3:
            with cols_tab2[i % 3]:
                st.markdown(row['Trip Name'])
                st.plotly_chart(fig)
                          
        else:
            cols_tab2 = st.columns(3)
            with cols_tab2[i % 3]:

                st.markdown(row['Trip Name'])
                st.plotly_chart(fig)
                  
with tab2:
    with st.container(border=True):
        st.write("Test")
