import streamlit as st
import pandas as pd
import preprocessor,helper
import pandas
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.ticker as ticker


st.sidebar.header('Olymic Analysis')
df=preprocessor.preprocess(pd.read_csv('Olympic_Athlete_Event_Results.csv'),pd.read_csv('Olympic_Athlete_Bio.csv'),pd.read_csv('Olympics_Country.csv'),pd.read_csv('Olympics_Games.csv'))
user_menu=st.sidebar.radio(
    'Select an Option',('Medal Tally','Overall Analysis','Country-wise analysis','Athlete-wise analysis')
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
    fig = px.line(nations_over_time, x="edition", y="country")
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
if user_menu == 'Country-wise analysis':
    st.sidebar.title('Country-wise Analysis')

    country_list = df['country'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)

if user_menu == 'Athlete-wise analysis':
    athlete_df = df.drop_duplicates(subset=['name', 'country'])

    x1 = athlete_df['age'].dropna()
    x2 = athlete_df[athlete_df['medal'] == 'Gold']['age'].dropna()
    x3 = athlete_df[athlete_df['medal'] == 'Silver']['age'].dropna()
    x4 = athlete_df[athlete_df['medal'] == 'Bronze']['age'].dropna()
    data1= x1.tolist()
    data2 = x2.tolist()
    data3 = x3.tolist()
    data4 = x4.tolist()

    fig = ff.create_distplot([data1, data2, data3, data4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)

    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Athletics', 'Boxing', 'Diving', 'Rugby', 'Shooting', 'Swimming',
       'Rowing', 'Tennis', 'Artistic Gymnastics', 'Cycling Track',
       'Fencing', 'Wrestling', 'Art Competitions', 'Cycling Road',
       'Artistic Swimming', 'Judo', 'Sailing', 'Weightlifting',
       'Taekwondo', 'Archery', 'Golf', 'Canoe Sprint',
       'Cycling Mountain Bike', 'Modern Pentathlon', 'Handball',
       'Triathlon', 'Basketball', 'Roller Hockey', 'Beach Volleyball',
       'Hockey', 'Football', 'Badminton', 'Rhythmic Gymnastics',
       'Equestrian Jumping', 'Wushu', 'Canoe Slalom', 'Karate',
       'Table Tennis']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['sport'] == sport]
        gold_ages = temp_df[temp_df['medal'] == 'Gold']['age'].dropna()

        if not gold_ages.empty:  # Check if the series is not empty
            x.append(gold_ages)
            name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    temp_df = temp_df.sort_values(by='weight')
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x=temp_df['weight'],y=temp_df['height'],hue=temp_df['medal'],style=temp_df['sex'],s=30, alpha=0.7)
    plt.xticks(rotation=90)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=10))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(20))
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)