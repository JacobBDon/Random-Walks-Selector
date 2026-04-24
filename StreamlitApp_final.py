import streamlit as st
import pandas as pd
import time
import plotly.graph_objects as go

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    data = pd.read_excel("https://raw.githubusercontent.com/JacobBDon/Random-Walks-Selector/main/Full_Random_Walks_Dataset.xlsx", index_col=False)
    data['Price_temp'] = data.loc[data['Trip Name'] != "US - Puerto Rico", 'Price'].str.replace("$","").str.replace(",","")
    data['Days'] = data['Number of Days']
    data.loc[data['Trip Name'] == "US - Puerto Rico", 'Price_temp'] = "2347"
    data.loc[data['Trip Name'] == "US - Virgin Islands", 'Price_temp'] = "0"
    data.loc[data['Trip Name'] == "US - Virgin Islands", 'Price'] = "Missing"
    data.loc[data['Trip Name'] != "US - Virgin Islands", 'Price_int'] = data['Price_temp'].astype(int)
    for col in ['Nightlife', 'Physical Activity', 'Relaxation', 'Nature', 'Culture']:
        data.loc[data[col].isnull(), col] = 0
        data[f'{col}_int'] = data[col].astype(int)
        data[f'{col}_str'] = data[f'{col}_int'].astype(str)
        data.loc[data[f'{col}_str'] == "0", f'{col}_str'] = "Missing"
    return data

data = load_data()

tab = st.sidebar.radio(
    "Select a page",
    ["Trip Selector", "Itinerary Selector", "Easy Ranker"]
)

st.sidebar.caption("Copyright © 2026 Jacob Don")

categories = ['Nightlife', 'Physical Activity', 'Relaxation', 'Nature', 'Culture']

if "welcomed" not in st.session_state:
    st.session_state["welcomed"] = False

@st.dialog("Welcome to the Random Walks 2026 Trip Selector!")
def welcome_dialog():
    st.markdown("""To select a page, open the sidebar:
	\n\n- To create a list of trips according to your selected criteria, use the Trip Selector.
	\n\n- To view trip itineraries, use the Itinerary Selector.
	\n\n- For an easy way to create your trip rankings (1-10 minutes), use the Easy Ranker.
	\n\nThis tool represents a fraction of the rich information provided by the Official Random Walks website.
	\nFor trip leaders, as well as tips, tricks, and detailed information on each itinerary, please visit https://www.randomwalksbooth.org/
	\n\nThis tool collects no data, and sessions are cleared upon refresh.""")
    st.session_state["welcomed"] = True

if not st.session_state["welcomed"]:
    welcome_dialog()

if tab == "Trip Selector":

    if 'ts_datesnogo' in st.session_state:
        st.session_state['_saved_ts_datesnogo'] = st.session_state['ts_datesnogo']
    if 'ts_countriesnogo' in st.session_state:
        st.session_state['_saved_ts_countriesnogo'] = st.session_state['ts_countriesnogo']
    if 'ts_filtertype' in st.session_state:
        st.session_state['_saved_ts_filtertype'] = st.session_state['ts_filtertype']
    if 'ts_tripname' in st.session_state:
        st.session_state['_saved_ts_tripname'] = st.session_state['ts_tripname']
    if 'ts_continent' in st.session_state:
        st.session_state['_saved_ts_continent'] = st.session_state['ts_continent']
    if 'ts_triptype' in st.session_state:
        st.session_state['_saved_ts_triptype'] = st.session_state['ts_triptype']
    if 'ts_numdays' in st.session_state:
        st.session_state['_saved_ts_numdays'] = st.session_state['ts_numdays']
    if 'ts_activitylevel' in st.session_state:
        st.session_state['_saved_ts_activitylevel'] = st.session_state['ts_activitylevel']
    if 'ts_pricerange' in st.session_state:
        st.session_state['_saved_ts_pricerange'] = st.session_state['ts_pricerange']
    if 'ts_price_slider' in st.session_state:
        st.session_state['_saved_ts_price_slider'] = st.session_state['ts_price_slider']
    if 'ts_sortselect_ratings' in st.session_state:
        st.session_state['_saved_ts_sortselect_ratings'] = st.session_state['ts_sortselect_ratings']
    if 'ts_sortselect_noratings' in st.session_state:
        st.session_state['_saved_ts_sortselect_noratings'] = st.session_state['ts_sortselect_noratings']
    if 'ts_seetrips' in st.session_state:
        st.session_state['_saved_ts_seetrips'] = st.session_state['ts_seetrips']
    if 'ts_chart_tripname' in st.session_state:
        st.session_state['_saved_ts_chart_tripname'] = st.session_state['ts_chart_tripname']

    data = data.copy()

    

    for _key in ['ts_datesnogo', 'ts_countriesnogo', 'ts_filtertype', 'ts_tripname',
             'ts_continent', 'ts_triptype', 'ts_numdays', 'ts_activitylevel',
             'ts_pricerange', 'ts_price_slider', 'ts_sortselect_ratings',
             'ts_sortselect_noratings', 'ts_seetrips', 'ts_chart_tripname']:
        if _key not in st.session_state and f'_saved_{_key}' in st.session_state:
            st.session_state[_key] = st.session_state[f'_saved_{_key}']
		
    cols_main = st.columns([2,3])	
    with cols_main[0]:
        st.title('Chicago Booth Random Walks 2026')
    
        filtertype = st.radio('**Would you like to filter or compare?**', ['Filter (keep trips that share ALL selected criteria)', 'Compare (show trips that have ANY of the selected criteria)'], key='ts_filtertype')
    
        min_date = data['Start Date'].min()
        max_date = data['End Date'].max()
    
        num_days = (max_date - min_date).days
    
        date_list = []
    
        for x in range(num_days+1):
            date0 = min_date + pd.Timedelta(days=x)
            date = date0.date()
            date_list.append(date)
    
    
        with st.container(border=True):
    
            dates_nogo = st.multiselect(label="Select dates you cannot attend", options=date_list, placeholder='', key='ts_datesnogo')
            st.write("Note: Panama Random Walks website states August 26 - 31; itinerary states August 27 - September 3.")

        data['nogo'] = 0

		
        data['Start Date'] = data['Start Date Final'].dt.date
        data['End Date'] = data['End Date Final'].dt.date

        for date in dates_nogo:
            data.loc[(date >= data['Start Date']) & (date <= data['End Date']), 'nogo'] = 1

        data2 = data[data['nogo'] == 0]
			
        with st.container(border=True):
    
            _nogo_opts = data2['Trip Name'].drop_duplicates().sort_values().tolist()
            countries_nogo = st.multiselect(
                label="Select trips to exclude",
                options=_nogo_opts,
                default=[v for v in st.session_state.get('ts_countriesnogo', []) if v in _nogo_opts],
                placeholder='',
                key='ts_countriesnogo'
            )

        for trip in countries_nogo:
        	data2.loc[trip == data2['Trip Name'], 'nogo'] = 1

        if data['nogo'].min() == 1:
            st.write("Sorry, there are no trips available :(")
    
        col1, col2 = st.columns([3,3])


        with col1:
            _tripname_opts = data2['Trip Name'].sort_values().unique().tolist()
            tripname = st.multiselect(
                label='Trip Name',
                options=_tripname_opts,
                default=[v for v in st.session_state.get('ts_tripname', []) if v in _tripname_opts],
                placeholder='',
                key='ts_tripname'
            )

        with col2:
            continent = st.multiselect(label = 'Continent', options=data2['Continent'].sort_values().unique().tolist(), placeholder='', key='ts_continent')

        with col1:
            triptype = st.multiselect(label='Trip Type', options=data2['Trip Type'].sort_values().unique().tolist(), placeholder='', key='ts_triptype')

        with col2:
            numdays = st.multiselect(label='Number of Days', options=data2['Number of Days'].sort_values().unique().tolist(), placeholder='',  key='ts_numdays')

        ratings_selected = False
        ratings = []

        cols = st.columns([3,3])

        price_selected = False


        with cols[0]:
            with st.container(border=True):
                activity_selected = st.toggle("Select Activity Level",  key='ts_activitylevel')

        with cols[1]:

            with st.container(border=True):

                price_selected = st.toggle("Select Price Range", key='ts_pricerange')

        if activity_selected:

            cols = st.columns([12,12,12,12,12])

            i = 0
			
            ratingcols_str = ['Nightlife_str', 'Physical Activity_str', 'Relaxation_str', 'Nature_str', 'Culture_str']
            for col in ratingcols_str:

                with cols[i]:

                    options = data[col].unique().tolist()
                    options.sort()
                    rating = st.multiselect(label=ratingcols[i], options=options, placeholder='', key=f"ts_pricerange_{col}")

                ratings.append(rating)
  
                checkval = ratings[i]

                data[f'keeprating{i+1}'] = data[col].isin(checkval)
                data[f'missingrating{i+1}'] = (not checkval)

                i = i+1

            data['keeprating_or'] = (data['keeprating1'] | data['keeprating2'] | data['keeprating3'] | data['keeprating4'] | data['keeprating5']) & ~(data['missingrating1'] & data['missingrating2'] & data['missingrating3'] & data['missingrating4'] & data['missingrating5'])
            data['keeprating_and'] = (data['keeprating1'] | data['missingrating1']) & (data['keeprating2'] | data['missingrating2']) & (data['keeprating3'] | data['missingrating3']) & (data['keeprating4'] | data['missingrating4']) & (data['keeprating5'] | data['missingrating5'])
            ratings_selected = True

    filtered_data = data2

    if (filtertype == 'Filter (keep trips that share ALL selected criteria)') and ratings_selected:

        filtered_data = data2[(
                             ((data['Continent'].isin(continent) | (not continent))
                             & (data['Trip Name'].isin(tripname) | (not tripname))
                             & (data['Number of Days'].isin(numdays) | (not numdays))
                             & (data['Trip Type'].isin(triptype) | (not triptype))
                             )
                             & (data['keeprating_and'] == 1) 
                             )]


    elif (filtertype == 'Compare (show trips that have ANY of the selected criteria)') and ratings_selected:
        filtered_data = data2[(
                             (data['Continent'].isin(continent))
                             | (data['Trip Name'].isin(tripname))
                             | (data['keeprating_or'] == 1)
                             | (data['Number of Days'].isin(numdays))
                             | (data['Trip Type'].isin(triptype))
                             )]

    elif (filtertype == 'Filter (keep trips that share ALL selected criteria)') and not ratings_selected:

        filtered_data = data2[(
                             ((data['Continent'].isin(continent) | (not continent))
                             & (data['Trip Name'].isin(tripname) | (not tripname))
                             & (data['Number of Days'].isin(numdays) | (not numdays))
                             & (data['Trip Type'].isin(triptype) | (not triptype))
                             )
                            )]


    elif (filtertype == 'Compare (show trips that have ANY of the selected criteria)') and not ratings_selected:
        filtered_data = data2[(
                             (data['Continent'].isin(continent))
                             | (data['Trip Name'].isin(tripname))
                             | (data['Number of Days'].isin(numdays))
                             | (data['Trip Type'].isin(triptype))
                             )]


    prices = filtered_data['Price_int']
    prices_full = data['Price_int']

    pricelist = prices.drop_duplicates().tolist()

    if 0 in pricelist:
        pricelist.remove(0)

    pricelist_full = prices_full.drop_duplicates().tolist()

    if 0 in pricelist_full:
        pricelist_full.remove(0)

    filtered_data_final = filtered_data

    if len(pricelist) > 1 or filtertype == 'Compare (show trips that have ANY of the selected criteria)':

        if price_selected:

            if len(pricelist) != 0:

                min_absolute = min(pricelist)
                max_absolute = max(pricelist)

            else:

                min_absolute = min(pricelist_full)
                max_absolute = max(pricelist_full)

    
            with cols_main[0]:  
              
                 with st.container(border=True):

                     min_price, max_price = st.slider(
                         'Trip Price',
                         min_value=min_absolute,
                         max_value=max_absolute,
                         value = (min_absolute, max_absolute),
                         label_visibility="collapsed",
                         format="$%d",
                         key='ts_price_slider'
                     )
                 st.markdown("""Notes:\n\n(1) US - Virgin Islands is missing a price.\n\n(2) US - Puerto Rico price does not include flight.""")


            filtered_data['in_pricerange'] = (filtered_data['Price_int'] >= min_price) & (filtered_data['Price_int'] <= max_price)

            filtered_data_final = filtered_data[filtered_data['in_pricerange']]

    filtered_data_unique = filtered_data_final.drop_duplicates(["Trip Name"])

    if ratings_selected:
        filtered_data_unique_final = filtered_data_unique[['Trip Name', 'Continent', 'Price', 'Start Date', 'End Date', 'Days', 'Nightlife_str', 'Physical Activity_str', 'Relaxation_str', 'Nature_str', 'Culture_str']]
        for str in ['Nightlife', 'Physical Activity', 'Relaxation', 'Nature', 'Culture']:
             filtered_data_unique_final = filtered_data_unique_final.rename(columns={f'{str}_str': str})
    else:
       filtered_data_unique_final = filtered_data_unique[['Trip Name', 'Continent', 'Price', 'Start Date', 'End Date', 'Days']]


    with cols_main[1]:
        with st.container(border=True):

            st.markdown('**Your trips:**')
            if ratings_selected:
                sortselect = st.selectbox('**Sort by:**', options=['Trip Name', 'Continent', 'Price', 'Start Date', 'End Date', 'Days', 'Nightlife', 'Physical Activity', 'Relaxation', 'Nature', 'Culture'], placeholder='', key='ts_sortselect_ratings')
            else:
                sortselect = st.selectbox('**Sort by:**', options=['Trip Name', 'Continent', 'Price', 'Start Date', 'End Date', 'Days'], placeholder='', key='ts_sortselect_noratings')
				
            if not sortselect:
                filtered_data_unique_final = filtered_data_unique_final.sort_values(['Trip Name'])
            else:
                filtered_data_unique_final = filtered_data_unique_final.sort_values(sortselect)

            styled_df = filtered_data_unique_final.style.set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#8B0000'), ('color', 'white')]}
            ])
            st.table(
            styled_df,
            hide_index=True,
            height=800
            )

    st.session_state["filtered_data"] = filtered_data
    st.session_state["filtered_data_unique_final"] = filtered_data_unique_final

    st.title("Activity Charts")

    if st.toggle("See trips from Trip Selector", key='ts_seetrips'):
        
        data_want = filtered_data_unique

    else:
        cols = st.columns([1,2])
        with cols[0]:

            tripname = st.multiselect('Select trips', filtered_data_unique['Trip Name'].unique().tolist(), placeholder='', key='ts_chart_tripname')
        
        data_want = filtered_data_unique[filtered_data_unique['Trip Name'].isin(tripname)]

    cols_tab2 = st.columns(3)
    
    for i in range(len(data_want)):

        row = data_want.iloc[i]

        values = row[categories].tolist()
        trip = row['Trip Name']
    
        values += values[:1]
        categories_closed = categories + categories[:1]

        fig = go.Figure()
    
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories_closed,
            fill='toself',
            line=dict(color="#8B0000"),
            fillcolor='rgba(139, 0, 0, 0.2)',
            name='Observation'
        ))
    
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, showticklabels=False)),
            showlegend=False,
            width=400,
            height=400
        )
	
        if i % 3 < 3:
            with cols_tab2[i % 3]:
                st.write(row['Trip Name'])
                st.plotly_chart(fig, key=f'{trip}1')
                          
        else:
            cols_tab2 = st.columns(3)
            with cols_tab2[i % 3]:
                st.write(row['Trip Name'])
                st.plotly_chart(fig, key=f'{trip}1')
                  
if tab == "Itinerary Selector":

    data = data.copy()

    cols = st.columns(4)

    with cols[0]:

        selecttype = st.selectbox('Which itineraries would you like to view?', ['Trip Selector', 'Choose your own'], placeholder='')

        if selecttype == 'Trip Selector':
            data_itin = st.session_state["filtered_data"]
        else:
            data_itin = data

        trips = data_itin['Trip Name'].unique().tolist()

        placeh = 'Select trip to view itinerary'
        countries = st.multiselect('Select trips', trips, placeholder=placeh, key='trip_multiselect')
        data_itin = data_itin[data_itin['Trip Name'].isin(countries)]

    
    data_itin_unique = data_itin[['Trip Name','Start Date Final','End Date Final','Number of Days','Price', 'Random Walk Website Link', 'Itinerary Link']].drop_duplicates(['Trip Name'])

    data_itin_unique['Start Date'] = data_itin_unique['Start Date Final'].dt.date
    data_itin_unique['End Date'] = data_itin_unique['End Date Final'].dt.date
    data_itin['Date'] =  pd.to_datetime(data_itin['Itinerary Date'], format='%m/%d/%Y').dt.date

    cols = st.columns(2)

    i = 0

    if len(countries) > 1:

        for country in countries:

            with cols[i%2]:

                with st.container(border=True):
                    st.write(country)

                    styled_df = (st.session_state["filtered_data_unique_final"][['Start Date','End Date','Days','Price']].iloc[[i]]).style.set_table_styles([
                        {'selector': 'th', 'props': [('background-color', '#8B0000'), ('color', 'white')]}
                    ])
                    st.table(
                    styled_df,
                    hide_index=True
                    )

                    styled_df = (data_itin_unique[['Random Walk Website Link', 'Itinerary Link']].iloc[[i]]).style.set_table_styles([
                        {'selector': 'th', 'props': [('background-color', '#8B0000'), ('color', 'white')]}
                    ])
                    st.table(
                    styled_df,
                    hide_index=True
                    )

                    data_itin_country = data_itin[data_itin['Trip Name'] == country]
                    data_itin_country['Day Number'] = (data_itin_country['Day Number']).astype(int).astype(str)
                    data_itin_country['Date'] = data_itin_country['Date'].astype(str)
                
                    for vars in ['Day Number', 'Date', 'Activity']:
                        data_itin_country.loc[data_itin_country['Event Number'] != 1, vars] = ''

                    data_itin_country.loc[data_itin_country['Event Time'].isnull(), 'Event Time'] = ''

                    st.write(data_itin_country['Trip Description'].drop_duplicates().iloc[0])

                    cols2 = st.columns([1,3,1])

                    with cols2[1]:

                        row = data_itin_country.iloc[0]

                        values = row[categories].tolist()
                        trip = row['Trip Name']
    
                        values += values[:1]
                        categories_closed = categories + categories[:1]

                        fig = go.Figure()
    
                        fig.add_trace(go.Scatterpolar(
                        r=values,
                        theta=categories_closed,
                        fill='toself',
                        line=dict(color="#8B0000"),
                        fillcolor='rgba(139, 0, 0, 0.2)',
                        name='Observation'
                        ))
    
                        fig.update_layout(
                        polar=dict(radialaxis=dict(visible=True, showticklabels=False)),
                        showlegend=False,
                        width=400,
                        height=400
                        )
                        st.plotly_chart(fig, key=f'{trip}2')

                    styled_df = (data_itin_country[['Day Number','Date','Activity','Event Title','Event Time']]).style.set_table_styles([
                        {'selector': 'th', 'props': [('background-color', '#8B0000'), ('color', 'white')]}
                    ])
                    st.table(
                    styled_df,
                    hide_index=True
                    )


            i = i + 1

    elif len(countries) == 1:

        with st.container(border=True):
            st.write(countries[0])

            styled_df = (data_itin_unique[['Start Date','End Date','Number of Days','Price']].iloc[[i]]).style.set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#8B0000'), ('color', 'white')]}
            ])
            st.table(
            styled_df,
            hide_index=True
            )

            styled_df = (data_itin_unique[['Random Walk Website Link', 'Itinerary Link']].iloc[[i]]).style.set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#8B0000'), ('color', 'white')]}
            ])
            st.table(
            styled_df,
            hide_index=True
            )

            data_itin_country = data_itin[data_itin['Trip Name'] == countries[0]]
            data_itin_country['Day Number'] = data_itin_country['Day Number'].astype(int).astype(str)
            data_itin_country['Date'] = data_itin_country['Date'].astype(str)
                
            for vars in ['Day Number', 'Date', 'Activity']:
                data_itin_country.loc[data_itin_country['Event Number'] != 1, vars] = ''
            data_itin_country.loc[data_itin_country['Event Time'].isnull(), 'Event Time'] = ''

            st.write(data_itin_country['Trip Description'].iloc[0])

            cols = st.columns([1,3,1])

            with cols[1]:

                row = data_itin_country.iloc[0]

                values = row[categories].tolist()
                trip = row['Trip Name']
    
                values += values[:1]
                categories_closed = categories + categories[:1]

                fig = go.Figure()
   
                fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories_closed,
                fill='toself',
                line=dict(color="#8B0000"),
                fillcolor='rgba(139, 0, 0, 0.2)',
                name='Observation'
                ))
    
                fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, showticklabels=False)),
                showlegend=False,
                width=400,
                height=400
                )

                st.plotly_chart(fig, key=f'{trip}2')

if tab == "Easy Ranker":

    data = data.copy()
 
    st.markdown("""**INSTRUCTIONS:**\n\n(1). Create the list of trips you would like to include in your rankings.\n\n(2). Press "BEGIN EASY RANKING"\n\n(3). Select your preferred trip out of each presented pair (fewer trips to choose from = faster ranking)\n\n(4). Keep playing until rankings stabilize (up to top-7)""")
 
    cols = st.columns([3,1,1,1,1,1,])
 
    with cols[0]:
 
        selecttype = st.selectbox('Which trips would you like to rank?', ['Start with Trip Selector', 'Choose your own'], placeholder='')
 
        if selecttype == 'Start with Trip Selector':
            data_itin = st.session_state["filtered_data"]
        else:
            data_itin = data
 
        trips = data_itin['Trip Name'].unique().tolist()

        if 'trip_multiselect' in st.session_state:
            st.session_state['_saved_trip_multiselect'] = st.session_state['trip_multiselect']

        if 'trip_multiselect' not in st.session_state and '_saved_trip_multiselect' in st.session_state:
            st.session_state['trip_multiselect'] = st.session_state['_saved_trip_multiselect']
       
 
        countries = st.multiselect('Select trips', trips, placeholder='Select trip to include in ranking', key='trip_multiselect')
        
        data_itin = data_itin[data_itin['Trip Name'].isin(countries)]
 
        data_itin_unique = data_itin[['Trip Name','Start Date Final','End Date Final','Number of Days','Price', 'Random Walk Website Link', 'Itinerary Link', 'Trip Description', 'Nightlife', 'Physical Activity', 'Relaxation', 'Nature', 'Culture']].drop_duplicates(['Trip Name'])
 
        data_itin_unique['Start Date'] = data_itin_unique['Start Date Final'].dt.date
        data_itin_unique['End Date'] = data_itin_unique['End Date Final'].dt.date
        data_itin['Date'] =  pd.to_datetime(data_itin['Itinerary Date'], format='%m/%d/%Y').dt.date
 
        st.markdown("""
        <style>
        div.stButton > button {
            background-color: #8B0000;
            color: white;
            border: none;
        }
 
        div.stButton > button:hover {
            background-color: #A30000;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)
 
 
    if "begin" not in st.session_state:
        st.session_state["begin"] = False
    if "completed" not in st.session_state:
        st.session_state["completed"] = False
 
    if not st.session_state.begin and not st.session_state.completed:
        if len(countries) > 1:
            if st.button("BEGIN EASY RANKING"):
                st.session_state.begin = True
                st.session_state.initialized = False 
                st.rerun()
        else:
            st.write("Please select at least two trips.")
 
    if st.session_state["begin"]:
 
        import random
        import math
        from itertools import combinations
 
        # ------------------ Elo + Uncertainty ------------------
        def elo_update(r1, r2, score1, k=32):
            expected1 = 1 / (1 + 10 ** ((r2 - r1) / 400))
            return r1 + k * (score1 - expected1)
        
        # simple uncertainty proxy (decreases with matches)
        def uncertainty(n_matches):
            return 1 / math.sqrt(n_matches + 1)
        
        # ------------------ Batch Refinement (Bradley-Terry style) ------------------
        def batch_refine(ratings, history, lr=0.01, steps=50):
            items = list(ratings.keys())
            idx = {item: i for i, item in enumerate(items)}
            scores = [ratings[item] for item in items]
        
            for _ in range(steps):
                grad = [0.0] * len(items)
        
                for (a, b, sa, sb) in history:
                    i, j = idx[a], idx[b]
                    ra, rb = scores[i], scores[j]
        
                    p = 1 / (1 + math.exp(-(ra - rb) / 400))
                    outcome = sa  # 1, 0, or 0.5
        
                    grad[i] += (outcome - p)
                    grad[j] += ((1 - outcome) - (1 - p))
 
                for i in range(len(scores)):
                    scores[i] += lr * grad[i]
        
            return {item: scores[idx[item]] for item in items}
 
        # ------------------ Normalize Elo to exaggerated 0-10 scale ------------------
        def normalize_ratings(ratings):
            if not ratings:
                return {}
            values = list(ratings.values())
            min_r, max_r = min(values), max(values)
            if max_r == min_r:
                return {k: 5.0 for k in ratings}
            normalized = {}
            for k, v in ratings.items():
                linear = (v - min_r) / (max_r - min_r)
                exaggerated = linear ** 0.6
                normalized[k] = round(exaggerated * 10, 2)
            return normalized
 
        if "initialized" not in st.session_state or st.session_state.initialized is False:
 
            trip_choices = [row.to_frame().T for _, row in data_itin_unique.iterrows()] 
        
            st.session_state.trip_choices = trip_choices
            st.session_state.ratings = {i: 1500 for i in range(len(trip_choices))}
            st.session_state.match_counts = {i: 0 for i in range(len(trip_choices))}
            st.session_state.comparisons = set()
            st.session_state.total_rounds = 0
            st.session_state.rating_history = []
            st.session_state.full_history = []
            st.session_state.current_pair = None
        
            n = len(trip_choices)
            if n <= 7:
                st.session_state.mode = "full"
            elif n <= 20:
                st.session_state.mode = "random"
            else:
                st.session_state.mode = "adaptive"
        
            st.session_state.initialized = True
 
        
        n = len(st.session_state.trip_choices)
        
        if n <= 7:
            st.session_state.mode = "full"
        elif n <= 20:
            st.session_state.mode = "random"
        else:
            st.session_state.mode = "adaptive"
 
    # ------------------ Pair Selection ------------------
        def smart_pair():
            trip_choices = st.session_state.trip_choices
            ratings = st.session_state.ratings
            counts = st.session_state.match_counts
            comps = st.session_state.comparisons
            mode = st.session_state.mode
        
            if len(trip_choices) < 2:
                return None, None
 
            st.session_state.ids = list(range(len(trip_choices)))
        
            # FULL
            if mode == "full":
                st.session_state.all_pairs = list(combinations(st.session_state.ids, 2))
                remaining = [
                    p for p in st.session_state.all_pairs
                    if tuple(sorted(p)) not in comps
                    and tuple(sorted(p)) != tuple(sorted(st.session_state.get("current_pair") or (-1,-1)))
                ]
                return random.choice(remaining) if remaining else (None, None)
                if not remaining:
                    # all pairs answered or only current pair left — clear current and finish
                    st.session_state.current_pair = None
                    return random.choice([p for p in st.session_state.all_pairs if tuple(sorted(p)) not in comps]) if len(comps) < len(st.session_state.all_pairs) else (None, None)
                chosen = random.choice(remaining)
                st.session_state.current_pair = chosen
                return chosen
        
        # RANDOM
            if mode == "random":
                target = int(len(trip_choices) * 4)
                if st.session_state.total_rounds >= target:
                    return None, None

                ids_sorted = sorted(st.session_state.ids, key=lambda x: counts[x])

                # Guard: if the same trip has been `first` 3 times in a row,
                # rotate to the next least-seen trip instead
                last_lefts = st.session_state.get("last_lefts", [])
                for candidate in ids_sorted:
                    if last_lefts.count(candidate) < 3:
                        first = candidate
                        break
                else:
                    first = ids_sorted[0]  # fallback

                # Guard: avoid showing the exact same pair back-to-back
                last_pair = st.session_state.get("last_pair", None)
                other_ids = [i for i in st.session_state.ids if i != first]
                if len(other_ids) > 1 and last_pair is not None:
                    last_opponent = last_pair[1] if last_pair[0] == first else last_pair[0]
                    filtered = [i for i in other_ids if i != last_opponent]
                    second = random.choice(filtered if filtered else other_ids)
                else:
                    second = random.choice(other_ids)

                st.session_state.last_lefts = (last_lefts + [first])[-6:]
                st.session_state.last_pair = (first, second)
                return first, second

            # ADAPTIVE
            if st.session_state.total_rounds >= int(len(trip_choices) * 5):
                return None, None

            if random.random() < 0.2:
                return random.sample(st.session_state.ids, 2)
        
            best_pair = None
            best_score = -1
        
            for _ in range(50):
                a, b = random.sample(st.session_state.ids, 2)
                rating_gap = abs(ratings[a] - ratings[b])
                unc = uncertainty(counts[a]) + uncertainty(counts[b])
                score = unc / (1 + rating_gap)
        
                if score > best_score:
                    best_score = score
                    best_pair = (a, b)
        
            return best_pair
        
        # ------------------ Convergence Check ------------------
        def check_convergence():
            hist = st.session_state.rating_history
 
            if st.session_state.mode == "full":
                return True
        
            if len(hist) < 5:
                return False
        
            diffs = []
            for i in range(1, len(hist)):
                prev, curr = hist[i - 1], hist[i]
                diff = sum(abs(curr[k] - prev[k]) for k in curr) / len(curr)
                diffs.append(diff)
        
            avg_recent_movement = sum(diffs[-3:]) / min(3, len(diffs))
        
            return avg_recent_movement < 1.0
        
        # --- Top-7 Stability Check ---
        def top_k_stable(k=7, window=4):
            hist = st.session_state.rating_history
        
            if len(hist) < window:
                return False
        
            top_sets = []
        
            for snapshot in hist[-window:]:
                sorted_trips = sorted(snapshot.items(), key=lambda x: x[1], reverse=True)
                top_sets.append(tuple([trip for trip, _ in sorted_trips[:k]]))
        
            return all(ts == top_sets[0] for ts in top_sets)
 
    # ------------------ Ranking UI ------------------
 
        pair = smart_pair()
        no_more_pairs = (pair is None or pair == (None, None))
        stable = check_convergence()
        top7_stable = top_k_stable(7)
 
        if no_more_pairs:
			
            if st.session_state.mode == "full" and st.session_state.full_history:
                st.session_state.ratings = batch_refine(
                    st.session_state.ratings,
                    st.session_state.full_history,
                    steps=200  # more steps for cleaner convergence
                )
            
            n = len(st.session_state.trip_choices)
 
            st.markdown("**PROGRESS**")
            st.progress(1.0)
 
            reset_col1, reset_col2 = st.columns(2)
            with reset_col1:
                if st.button("↺ Start Over (Same Trips)"):
                    for k in ["initialized", "ratings", "match_counts", "comparisons",
                              "total_rounds", "rating_history", "full_history", "ids", "all_pairs",
							 "last_lefts", "last_pair", "current_pair"]:
                        st.session_state.pop(k, None)
                    st.session_state.initialized = False
                    st.session_state.completed = False
                    st.rerun()
            with reset_col2:
                if st.button("↺ Full Reset (Choose New Trips)"):
                    for k in ["begin", "completed", "initialized", "trip_choices", "ratings",
                              "match_counts", "comparisons", "total_rounds", "rating_history",
                              "full_history", "ids", "all_pairs", "mode", "last_lefts", "last_pair", "current_pair"]:
                        st.session_state.pop(k, None)
                    st.rerun()
 
            st.success("Ranking complete!")
            st.session_state.completed = True
 
            sorted_items = sorted(
                st.session_state.ratings.items(),
                key=lambda x: x[1],
                reverse=True
            )
 
            normalized = normalize_ratings(st.session_state.ratings)
 
            ranking_rows = []
            for i, (trip_id, rating) in enumerate(sorted_items, 1):
                df = st.session_state.trip_choices[trip_id]
                trip_name = df["Trip Name"].iloc[0]
                norm_score = normalized[trip_id]
                ranking_rows.append((i, trip_name, norm_score))
 
            rank_col, chart_col = st.columns([1, 2])
 
            with rank_col:
                st.subheader("Final Ranking")
                for rank, name, score in ranking_rows:
                    st.write(f"{rank}. {name} — {score} / 10")
 
            with chart_col:
                bar_names = [row[1] for row in ranking_rows][::-1]
                bar_scores = [row[2] for row in ranking_rows][::-1]
 
                bar_fig = go.Figure(go.Bar(
                    x=bar_scores,
                    y=bar_names,
                    orientation='h',
                    marker=dict(
                        color=bar_scores,
                        colorscale=[[0, 'rgba(139,0,0,0.3)'], [1, '#8B0000']],
                        showscale=False
                    ),
                    text=[f"{s} / 10" for s in bar_scores],
                    textposition='outside'
                ))
 
                bar_fig.update_layout(
                    xaxis=dict(range=[0, 11], showticklabels=False, showgrid=False, zeroline=False),
                    yaxis=dict(automargin=True),
                    margin=dict(l=10, r=60, t=30, b=10),
                    height=max(250, len(ranking_rows) * 50),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(bar_fig, use_container_width=True)
 
            st.stop()
 
 
        if len(st.session_state.trip_choices) >= 2:
    
            st.markdown("""**Select your preferred trip:**""")
            btn_col1, btn_col2, btn_col3 = st.columns(3)

            left_id, right_id = pair
 
            left = st.session_state.trip_choices[left_id]
            right = st.session_state.trip_choices[right_id]
    
            def handle(score_left, score_right, _left_id=left_id, _right_id=right_id):
                # Always record the result
                st.session_state.match_counts[_left_id] += 1
                st.session_state.match_counts[_right_id] += 1
                st.session_state.comparisons.add(tuple(sorted((_left_id, _right_id))))
                st.session_state.total_rounds += 1
                st.session_state.current_pair = None
                st.session_state.full_history.append((_left_id, _right_id, score_left, score_right))
            
                if st.session_state.mode == "full":
                    # Don't do incremental Elo — batch solve at the end instead
                    st.session_state.rating_history.append(st.session_state.ratings.copy())
                else:
                    # Incremental Elo for random/adaptive modes
                    r1 = st.session_state.ratings[_left_id]
                    r2 = st.session_state.ratings[_right_id]
                    st.session_state.ratings[_left_id] = elo_update(r1, r2, score_left)
                    st.session_state.ratings[_right_id] = elo_update(r2, r1, score_right)
                    st.session_state.rating_history.append(st.session_state.ratings.copy())
            
                    if st.session_state.total_rounds % 20 == 0:
                        st.session_state.ratings = batch_refine(
                            st.session_state.ratings,
                            st.session_state.full_history
                        )
            
                st.rerun()

            with btn_col1:
                st.markdown("""
                <style>
                div.stButton > button {
                    background-color: #8B0000;
                    color: white;
                    border: none;
                }
    
                div.stButton > button:hover {
                    background-color: #A30000;
                    color: white;
                }
                </style>
                """, unsafe_allow_html=True)
                if st.button(f"{left['Trip Name'].iloc[0]} - {left['Number of Days'].iloc[0]} days / {left['Price'].iloc[0]}", key=f"leftbutton_{left_id}_{st.session_state.total_rounds}"):
                    handle(1, 0)

            with btn_col2:
                if st.button("I can't decide", key=f"tiebutton_{st.session_state.total_rounds}"):
                    handle(0.5, 0.5)

            with btn_col3:
                if st.button(f"{right['Trip Name'].iloc[0]} - {right['Number of Days'].iloc[0]} days / {right['Price'].iloc[0]}", key=f"rightbutton_{right_id}_{st.session_state.total_rounds}"):
                    handle(0, 1)
 
            n_prog = len(st.session_state.trip_choices)
            st.write("")
            st.caption("PROGRESS")

            if st.session_state.mode == "full":
                total_possible = n_prog * (n_prog - 1) // 2
                progress = len(st.session_state.comparisons) / total_possible
            else:
                target = int(n_prog * (4 if n_prog <= 20 else 5))
                progress = min(st.session_state.total_rounds / target, 1.0)
            st.progress(progress)
 
            reset_col1, reset_col2 = st.columns(2)
            with reset_col1:
                if st.button("↺ Start Over (Same Trips)"):
                    for k in ["initialized", "ratings", "match_counts", "comparisons",
                              "total_rounds", "rating_history", "full_history", "ids", "all_pairs"]:
                        st.session_state.pop(k, None)
                    st.session_state.initialized = False
                    st.session_state.completed = False
                    st.rerun()
            with reset_col2:
                if st.button("↺ Full Reset (Choose New Trips)"):
                    for k in ["begin", "completed", "initialized", "trip_choices", "ratings",
                              "match_counts", "comparisons", "total_rounds", "rating_history",
                              "full_history", "ids", "all_pairs", "mode"]:
                        st.session_state.pop(k, None)
                    st.rerun()
        
            colsa = st.columns([50,1,50])
        
            with colsa[0]:
        
                with st.container(border=True):
                    trip_name = left['Trip Name'].iloc[0]
                    st.markdown(f"**{trip_name}**")
 
                    styled_df = (left[['Start Date','End Date','Number of Days','Price']]).style.set_table_styles([
                        {'selector': 'th', 'props': [('background-color', '#8B0000'), ('color', 'white')]}
                    ])
                    st.table(styled_df, hide_index=True)
        
                    styled_df = (left[['Random Walk Website Link', 'Itinerary Link']]).style.set_table_styles([
                        {'selector': 'th', 'props': [('background-color', '#8B0000'), ('color', 'white')]}
                    ])
                    st.table(styled_df, hide_index=True)
 
                    lefttrip_categories = left[categories].copy()
    
                    for col in categories:
                        lefttrip_categories[col] = lefttrip_categories[col].astype(int).astype(str)
    
                    styled_df = lefttrip_categories.style.set_table_styles([
                        {'selector': 'th', 'props': [('background-color', '#8B0000'), ('color', 'white')]}
                    ])
                    st.table(styled_df, hide_index=True)
        
                    st.write(left['Trip Description'].iloc[0])
        
                cols2 = st.columns([1,3,1])
        
                with cols2[1]:
        
                    row = left.iloc[0]
        
                    values = row[categories].tolist()
                    trip = row['Trip Name']
        
                    values += values[:1]
                    categories_closed = categories + categories[:1]
        
                    fig = go.Figure()
        
                    fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=categories_closed,
                    fill='toself',
                    line=dict(color="#8B0000"),
                    fillcolor='rgba(139, 0, 0, 0.2)',
                    name='Observation'
                    ))
        
                    fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, showticklabels=False)),
                    showlegend=False,
                    width=400,
                    height=400
                    )
                    st.plotly_chart(fig, key=f'{trip}2')
        
            with colsa[2]:
        
                with st.container(border=True):
                    
                    trip_name = right['Trip Name'].iloc[0]
                    st.markdown(f"**{trip_name}**")
        
                    styled_df = (right[['Start Date','End Date','Number of Days','Price']]).style.set_table_styles([
                        {'selector': 'th', 'props': [('background-color', '#8B0000'), ('color', 'white')]}
                    ])
                    st.table(styled_df, hide_index=True)
        
                    styled_df = (right[['Random Walk Website Link', 'Itinerary Link']]).style.set_table_styles([
                        {'selector': 'th', 'props': [('background-color', '#8B0000'), ('color', 'white')]}
                    ])
                    st.table(styled_df, hide_index=True)
    
                    righttrip_categories = right[categories].copy()
    
                    for col in categories:
                        righttrip_categories[col] = righttrip_categories[col].astype(int).astype(str)
    
                    styled_df = righttrip_categories.style.set_table_styles([
                        {'selector': 'th', 'props': [('background-color', '#8B0000'), ('color', 'white')]}
                    ])
                    st.table(styled_df, hide_index=True)
 
                    st.write(right['Trip Description'].iloc[0])
        
                cols2 = st.columns([1,3,1])
        
                with cols2[1]:
        
                    row = right.iloc[0]
        
                    values = row[categories].tolist()
                    trip = row['Trip Name']
        
                    values += values[:1]
                    categories_closed = categories + categories[:1]
        
                    fig = go.Figure()
        
                    fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=categories_closed,
                    fill='toself',
                    line=dict(color="#8B0000"),
                    fillcolor='rgba(139, 0, 0, 0.2)',
                    name='Observation'
                    ))
        
                    fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, showticklabels=False)),
                    showlegend=False,
                    width=400,
                    height=400
                    )
                    st.plotly_chart(fig, key=f'{trip}2')
 
        else:
            st.write("Please select at least two trips.")

                
