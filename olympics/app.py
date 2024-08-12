import streamlit as st
import pandas as pd
import preprocessor,helper
import pandas
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff


st.sidebar.header('Olymic Analysis')
df=preprocessor.preprocess(pd.read_csv('Olympic_Athlete_Event_Results.csv'),pd.read_csv('Olympic_Athlete_Bio.csv'),pd.read_csv('Olympics_Country.csv'),pd.read_csv('Olympics_Games.csv'))
user_menu=st.sidebar.radio(
    'Select an Option',('Medal Tally','Overall Analysis','Country-wise analysis','Athelete-wise analysis')
)

if user_menu=='Medal Tally':
    st.sidebar.header('Medal Tally')
    years,country=helper.country_year_list(df)
    selected_year=st.sidebar.selectbox('Year',years)
    selected_country = st.sidebar.selectbox('Country', country)
    medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year=='Overall' and selected_country=='Overall':
        st.title("Overall Tally")
    elif selected_year=='Overall' and selected_country!='Overall':
        st.title(f"Performance of {selected_country}")
    elif selected_year!='Overall' and selected_country=='Overall':
        st.title(f"Performance of countries in {selected_year}")
    else:
        st.title(f"Performance of {selected_country} in {selected_year}")
    st.dataframe(medal_tally)

if user_menu == 'Overall Analysis':

    st.header("Editions")
    editions = df['Year'].unique().shape[0] - 1
    cities = df['city'].unique().shape[0]
    sports = df['sport'].unique().shape[0]
    events = df['event'].unique().shape[0]
    athletes = df['name'].unique().shape[0]
    nations = df['country'].unique().shape[0]
    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)
    nations_over_time = helper.data_over_time(df, 'country')
    fig = px.line(nations_over_time, x="Edition", y="country")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)
    events_over_time = helper.data_over_time(df, 'event')
    fig = px.line(events_over_time, x="edition", y="event")
    st.title("Events over the years")
    st.plotly_chart(fig)
    athlete_over_time = helper.data_over_time(df, 'name')
    fig = px.line(athlete_over_time, x="edition", y="name")
    st.title("Athletes over the years")
    st.plotly_chart(fig)
    st.title("No. of Events over time(Every Sport)")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'sport', 'event'])
    ax = sns.heatmap(
        x.pivot_table(index='sport', columns='Year', values='event', aggfunc='count').fillna(0).astype('int'),
        annot=True)
    st.pyplot(fig)
    st.title("Most successful Athletes")
    sport_list = df['sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    x = helper.most_successful(df, selected_sport)
    st.table(x)