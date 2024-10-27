import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from plotly.figure_factory import create_distplot
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
df = preprocessor.preprocess(df,region_df)
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athelete-wise Analysis')
)
# st.dataframe(df)
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country",country)
    medal_tally = helper.fetch_data(df,selected_year,selected_country)

    if selected_year=='Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_year=='Overall' and selected_country != 'Overall':
        st.title('Overall Performace of '+str(selected_country))
    if selected_year!='Overall' and selected_country == 'Overall':
        st.title('Medal Tally in '+str(selected_year)+' Olympics')
    if selected_year!='Overall' and selected_country != 'Overall':
        st.title(str(selected_country)+' Performance in '+str(selected_year)+' Olympics')
        
    st.table(medal_tally)


if user_menu=='Overall Analysis':
    st.title("Total Statistics")
    Editions = df['Year'].unique().shape[0]-1
    Athletes = int(df['Name'].unique().shape[0])
    Country = df['region'].unique().shape[0]
    Venue = df['City'].unique().shape[0]
    Sports = df['Sport'].unique().shape[0]
    Events = df['Event'].unique().shape[0]

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(Editions)
    with col2:
        st.header('Athletes')
        st.title(Athletes)
    with col3:
        st.header('Nations')
        st.title(Country)


    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Venues')
        st.title(Venue)
    with col2:
        st.header('Sports')
        st.title(Sports)
    with col3:
        st.header('Events')
        st.title(Events)

    st.title('Participating Nations Over Time in Olympics')
    nation_over_time = helper.data_over_time(df,'region')
    fig = px.line(nation_over_time,x='Editions',y = 'region')
    st.plotly_chart(fig)


    st.title('No. Of Events Over Time in Olympics')
    events_over_time = helper.data_over_time(df,'Event')
    fig = px.line(events_over_time,x='Editions',y = 'Event')
    st.plotly_chart(fig)


    st.title('No. Of Athletes Over Time in Olympics')
    athletes_over_time = helper.data_over_time(df,'Name')
    fig = px.line(athletes_over_time,x='Editions',y = 'Name')
    st.plotly_chart(fig)

    st.title('No. Of Events Over Time(Every Sports)')
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year','Sport','Event'])
    ax = sns.heatmap(x.pivot_table(index = 'Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype(int),annot=True)

    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

    
if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Conuntry-Wise Analysis')
    country_table = df['region'].dropna().unique().tolist()
    country_table.sort()
    selected_country = st.sidebar.selectbox('Select a Country',country_table)
    country_df = helper.yearwise_medal_tally(df,str(selected_country))
    fig = px.line(country_df,x='Year',y='Medal')
    st.title(selected_country+" Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " Performance in each sports over the years")
    pt = helper.country_analysis(df,selected_country)
    fig,ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pt,annot=True)

    st.pyplot(fig)

    st.title("Top 15 Athletes of "+selected_country)
    temp_df = helper.most_successful_athlete(df,selected_country)
    st.table(temp_df)

if user_menu == 'Athelete-wise Analysis':
    athlete_df = df.drop_duplicates(subset = ['Name','region'])
    x = athlete_df['Age'].dropna()
    x1 = athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()
    st.title("Distribution of Age")
    fig = create_distplot([x,x1,x2,x3],['Age Distribution','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist = False, show_rug = False)
    st.plotly_chart(fig)


    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    st.pyplot(fig)


    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

    