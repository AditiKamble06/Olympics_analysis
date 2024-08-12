import pandas as pd
def preprocess(df,df2,df3,df4):
    df['Season'] = df['edition'].str.extract(r'(Summer|Winter)')
    merged_df = pd.merge(df, df2, on='athlete_id', how='left')
    merged_df = merged_df.rename(columns={'country_noc_x': 'country_noc'})
    merged_df.drop(['country_noc_y'], axis=1, inplace=True)
    merged_df = merged_df[merged_df['Season'] == 'Summer']
    merged_df['Year'] = merged_df['edition'].str.extract(r'(\d{4})')
    merged_df.drop(['edition'], axis=1, inplace=True)
    merged_df.isTeamSport = merged_df.isTeamSport.apply(lambda X: 1 if X == True else 0)
    merged_df.drop(['athlete'], axis=1, inplace=True)
    merged_df.sex = merged_df.sex.apply(lambda X: 'M' if X == 'Male' else 'F')
    merged_df = merged_df.rename(columns={'country_noc': 'noc'})
    merged_df1 = pd.merge(merged_df, df3, on='noc', how='left')
    merged_df1.drop(['country_x'], axis=1, inplace=True)
    merged_df1 = merged_df1.rename(columns={'country_y': 'country'})
    merged_df1.drop(['description', 'special_notes','Season'], axis=1, inplace=True)
    merged_df1['Year of birth'] = merged_df1['born'].str.extract(r'(\d{4})')
    merged_df1['Year of birth'] = pd.to_numeric(merged_df1['Year of birth'], errors='coerce')
    merged_df1['Year'] = pd.to_numeric(merged_df1['Year'], errors='coerce')
    merged_df1['age'] = merged_df1['Year'] - merged_df1['Year of birth']
    merged_df1 = pd.merge(merged_df1, df4[['city', 'edition_id']], on='edition_id', how='left')
    merged_df1 = merged_df1.drop_duplicates()
    merged_df1 = pd.concat([merged_df1, pd.get_dummies(merged_df1['medal'], dtype='int8')], axis=1)
    return merged_df1
