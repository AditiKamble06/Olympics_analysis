import pandas as pd
import numpy as np
import preprocessor
import streamlit as st

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(
        subset=['sport', 'event', 'isTeamSport', 'country', 'medal', 'result_id', 'pos', 'Year'])
    flag = 0
    temp_df = medal_df
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['country'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['country'] == country)]
    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('country').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                       ascending=False).reset_index()

    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['Total'] = x['Total'].astype('int')
    return x
def medal_tally(df):
    medal_df = df.drop_duplicates(subset=['sport','event','isTeamSport','country','medal','result_id','pos','Year'])
    medal_tally=medal_df.groupby('country').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['Total'] = medal_tally['Total'].astype('int')
    return medal_tally
def country_year_list(df):
    years= df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')
    country=np.unique(df['country'].dropna().values).tolist()
    country.sort()
    country.insert(0,'Overall')
    return years,country
def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['country'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country

def data_over_time(df,col):
    st.dataframe(df)
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'Year': 'edition', 'count': col}, inplace=True)
    return nations_over_time


def most_successful(df, sport):
    temp_df = df.dropna(subset=['medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['sport'] == sport]


    x = temp_df['name'].value_counts().head(15).reset_index().merge(df, left_on='name',right_on='name',how='left')[
        ['name', 'sport', 'country']].drop_duplicates('name')
    x.rename(columns={'name_x': 'name', 'count': 'medals'}, inplace=True)
    return x

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['medal'])
    temp_df.drop_duplicates(subset=['sport','event','isTeamSport','country','medal','result_id','pos','Year'],inplace=True)

    new_df = temp_df[temp_df['country'] == country]
    final_df = new_df.groupby('Year').count()['medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['medal'])
    temp_df.drop_duplicates(subset=['sport','event','isTeamSport','country','medal','result_id','pos','Year'],inplace=True)
    new_df = temp_df[temp_df['country'] == country]

    pt = new_df.pivot_table(index='sport', columns='Year', values='medal', aggfunc='count').fillna(0)
    return pt


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['medal'])

    temp_df = temp_df[temp_df['country'] == country]


    x = temp_df['name'].value_counts().reset_index().head(10).merge(df, left_on='name', right_on='name', how='left')[
        ['count', 'name', 'sport','Year']].drop_duplicates('name')
    x.rename(columns={'name': 'name', 'count': 'medals'}, inplace=True)
    return x

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['name', 'country'])
    athlete_df['medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['name', 'country'])

    men = athlete_df[athlete_df['sex'] == 'M'].groupby('Year').count()['name'].reset_index()
    women = athlete_df[athlete_df['sex'] == 'F'].groupby('Year').count()['name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'name_x': 'Male', 'name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final

