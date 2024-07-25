import numpy as np
import pandas as pd

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country


def data_over_time(df, col):
    """Generate a DataFrame showing the count of unique values in `col` over the years."""
    data = df.drop_duplicates(['Year', col])
    counts = data.groupby('Year')[col].count().reset_index()
    counts.columns = ['Year', 'Counts']
    counts = counts.sort_values('Year').reset_index(drop=True)
    return counts


import pandas as pd  # Ensure this import is included

def most_successful_till_date(df, sport):
    # Check if the dataframe is empty
    if df.empty:
        return pd.DataFrame({'Name': ['No Data'], 'Medal Count': [0]})

    if sport == 'Overall':
        # Calculate the most successful athletes overall
        most_successful = df.groupby('Name')['Medal'].count().reset_index()
    else:
        # Filter by specific sport and calculate
        sport_df = df[df['Sport'] == sport]
        most_successful = sport_df.groupby('Name')['Medal'].count().reset_index()

    # Check if the resulting dataframe is empty
    if most_successful.empty:
        return pd.DataFrame({'Name': ['No Data'], 'Medal Count': [0]})

    # Sort and return top 10 athletes
    most_successful = most_successful.sort_values(by='Medal', ascending=False)
    return most_successful.head(10).reset_index(drop=True)


def most_successful(df, selected_country):
    """Get the most successful athletes for a selected country"""

    # Filter data for the selected country (region)
    temp_df = df[df['region'] == selected_country]

    if temp_df.empty:
        # Handle case where there is no data for the selected country
        return pd.DataFrame({'Name': ['No Data'], 'Medal Count': [0]})

    # Count the number of medals per athlete
    athlete_medals = temp_df.groupby('Name')['Medal'].count().reset_index()
    athlete_medals.columns = ['Name', 'Medal Count']

    # Sort athletes by the number of medals in descending order
    top_athletes = athlete_medals.sort_values('Medal Count', ascending=False).head(10).reset_index(drop=True)

    # Check if we have fewer than 10 athletes
    if top_athletes.shape[0] < 10:
        top_athletes = top_athletes.append(pd.DataFrame({'Name': ['No Data'] * (10 - top_athletes.shape[0]), 'Medal Count': [0] * (10 - top_athletes.shape[0])}), ignore_index=True)

    # Start index from 1
    top_athletes.index += 1

    # Merge with the original DataFrame to get additional details (optional)
    top10_df = top_athletes.merge(df[['Name', 'Sport']].drop_duplicates(), on='Name', how='left').drop_duplicates()

    return top10_df




def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final
