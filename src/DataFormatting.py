import sys
sys.path.append('../src/')
import pandas as pd
from datetime import date
from datetime import timedelta
from src import CurrentDate
from src import ReadData as rd


def country_wise_count(COVID_DATA_df, country=None, state=None, city=None):
    df = COVID_DATA_df[COVID_DATA_df['Last Update'].str.contains(CurrentDate.DATE_UPDATE)]
    if city is not None:
        selection_column = 'City'
        if not isinstance(city,list):
            city = [city]
        df = df[df['City'].isin(city)]
    elif state is not None:
        selection_column = 'Province/State'
        if not isinstance(state,list):
            state = [state]
        df = df[df['Province/State'].isin(state)]
    elif country is not None:
        selection_column = 'Country/Region'
        if not isinstance(country,list):
            country = [country]
        df = df[df['Country/Region'].isin(country)]
    else:
        selection_column = 'Country/Region'

    df = df.groupby([selection_column]).agg({'Confirmed':['sum'], 'Deaths':['sum'], 'Recovered':['sum']})
    df = df.reset_index()
    df.columns = df.columns.droplevel(1)
    df = df.sort_values(by=['Confirmed'], ascending=False)
    return df


def timeline_total(COVID_DATA_df, country=None, state=None, city=None):
    if city is not None:
        if not isinstance(city,list):
            city = [city]
        df = COVID_DATA_df[COVID_DATA_df['City'].isin(city)]
    elif state is not None:
        if not isinstance(state,list):
            state = [state]
        df = COVID_DATA_df[COVID_DATA_df['Province/State'].isin(state)]
    elif country is not None:
        if not isinstance(country,list):
            country = [country]
        df = COVID_DATA_df[COVID_DATA_df['Country/Region'].isin(country)]
    else:
        df = COVID_DATA_df
    
    df = df.sort_values(by=['Last Update'])
    df = df.groupby(['Last Update']).agg({'Confirmed':['sum'], 'Recovered':['sum'], 'Deaths':['sum']})
    df = df.reset_index()
    df.columns = df.columns.droplevel(1)
    df = df.sort_values(by=['Last Update'])
    return df


def timeline_countrywise(COVID_DATA_df, country=None, state=None, city=None):
    if city is not None:
        selection_column = 'City'
        temp_df = country_wise_count(COVID_DATA_df, country,state, city) 
    elif state is not None:
        selection_column = 'Province/State'
        temp_df = country_wise_count(COVID_DATA_df, country,state) 
    elif country is not None:
        selection_column = 'Country/Region'
        temp_df = country_wise_count(COVID_DATA_df, country)
    else:
        selection_column = 'Country/Region'
        temp_df = country_wise_count(COVID_DATA_df)
    
    temp_df = temp_df[:5]
    top_countries = temp_df[selection_column].tolist()
    df = COVID_DATA_df[COVID_DATA_df[selection_column].isin(top_countries)]
    df = df.sort_values(by=[selection_column, 'Last Update'])
    df = df.groupby([selection_column, 'Last Update']).agg({'Confirmed':['sum'], 'Recovered':['sum'], 'Deaths':['sum']})
    df = df.reset_index()
    df.columns = df.columns.droplevel(1)
    df = df.sort_values(by=['Last Update'])
    return df

def line_plot_initatizing_data(COVID_DATA_df, country, state, city=None):
    if city is not None:
        selection_column = 'City'
        df = timeline_countrywise(COVID_DATA_df, country, state, city)
        if isinstance(city,list):
            x_label_value = '-'.join(city) + ' Cities'
        else:
            x_label_value = city + ' City'
    elif state is not None:
        selection_column = 'Province/State'
        df = timeline_countrywise(COVID_DATA_df, country, state)
        if isinstance(state,list):
            x_label_value = '-'.join(state) + ' States'
        else:
            x_label_value = state + ' State'
    elif country is not None:
        selection_column = 'Country/Region'
        df = timeline_countrywise(COVID_DATA_df, country)
        if isinstance(country,list):
            x_label_value = '-'.join(country) + ' Countries'
        else:
            x_label_value = country + ' Country'
    else:
        selection_column = 'Country/Region'
        df = timeline_countrywise(COVID_DATA_df)
        x_label_value = 'top 5 Countries'
    
    return selection_column, df, x_label_value

def new_cases_diff(df,country_list, selection_column):
    diff_df = pd.DataFrame(columns = [selection_column, 'Last Update', 'Confirmed', 'Deaths', 'Recovered'])
    for country in country_list:
        temp_df = df[df[selection_column] ==country]
        temp_df["New Confirmed"] = temp_df["Confirmed"].diff(periods=1)
        temp_df["New Recovered"] = temp_df["Recovered"].diff(periods=1)
        temp_df["New Deaths"] = temp_df["Deaths"].diff(periods=1)
        diff_df = pd.concat([diff_df,temp_df], ignore_index=True, axis=0, sort=True)
    return diff_df
    
def timeline_new_cases_countrywise(COVID_DATA_df, country=None, state=None, city=None):
    if city is not None:
        selection_column = 'City'
        df = timeline_countrywise(COVID_DATA_df, country, state, city)
        top_countries = country_wise_count(COVID_DATA_df, country, state, city)[selection_column].tolist()
    elif state is not None:
        selection_column = 'Province/State'
        df = timeline_countrywise(COVID_DATA_df, country, state)
        top_countries = country_wise_count(COVID_DATA_df, country, state)[selection_column].tolist()
    elif country is not None:
        selection_column = 'Country/Region'
        df = timeline_countrywise(COVID_DATA_df, country)
        top_countries = country_wise_count(COVID_DATA_df, country)[selection_column].tolist()
    else:
        selection_column = 'Country/Region'
        df = timeline_countrywise(COVID_DATA_df)
        top_countries = country_wise_count(COVID_DATA_df)[selection_column].tolist()
    
    top_countries = top_countries[:5]
    #Getting the differences
    diff_df = new_cases_diff(df,top_countries, selection_column)
    
    diff_df = diff_df.sort_values(by=['Last Update'])
    diff_df = diff_df.fillna(0)
    return diff_df

def line_plot_new_cases_initatizing_data(COVID_DATA_df, country, state, city):
    if city is not None:
        selection_column = 'City'
        df = timeline_new_cases_countrywise(COVID_DATA_df, country, state, city)
        if isinstance(city,list):
            x_label_value = '-'.join(city) + ' Cities'
        else:
            x_label_value = city + ' Cities'
    elif state is not None:
        selection_column = 'Province/State'
        df = timeline_new_cases_countrywise(COVID_DATA_df, country, state)
        if isinstance(state,list):
            x_label_value = '-'.join(state) + ' States'
        else:
            x_label_value = state + ' State'
    elif country is not None:
        selection_column = 'Country/Region'
        df = timeline_new_cases_countrywise(COVID_DATA_df, country)
        if isinstance(country,list):
            x_label_value = '-'.join(country) + ' Countries'
        else:
            x_label_value = country + ' Country'
    else:
        selection_column = 'Country/Region'
        df = timeline_new_cases_countrywise(COVID_DATA_df)
        x_label_value = 'Top 5 Countries'
        
    return selection_column, df, x_label_value

def corona_table(COVID_DATA_df):
    countries = list(set(country_wise_count(COVID_DATA_df)['Country/Region'].tolist()))
    temp_df = COVID_DATA_df.groupby(['Country/Region', 'Last Update']).agg({'Confirmed':['sum'], 'Recovered':['sum'], 'Deaths':['sum']})
    temp_df = temp_df.reset_index()
    temp_df.columns = temp_df.columns.droplevel(1)
    temp_df = new_cases_diff(temp_df,countries, 'Country/Region')
    temp_df = temp_df[temp_df['Last Update'].str.contains(CurrentDate.DATE_UPDATE)]
    temp_df = temp_df.sort_values(by=['Confirmed'], ascending=False)

    pop_df = rd.import_population()
    temp_df = pd.merge(temp_df, pop_df, on='Country/Region', how='inner')
    temp_df['Tot Cases/ 1M Pop'] = (temp_df['Confirmed']*1000000) / temp_df['Population']
    temp_df['Deaths/ 1M Pop'] = (temp_df['Deaths']*1000000) / temp_df['Population']
    temp_df['Active Cases'] = temp_df['Confirmed'] - temp_df['Deaths'] - temp_df['Recovered']
    temp_df = temp_df[['Country/Region','Confirmed','New Confirmed','Deaths','New Deaths','Recovered','Active Cases','Tot Cases/ 1M Pop','Deaths/ 1M Pop']]
    pd.set_option('display.max_rows', temp_df.shape[0]+1)
    return temp_df
