import sys
sys.path.append('../src/')
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
from src import DataFormatting as daf
from src import CurrentDate

def country_wise_count_plot(COVID_DATA_df, country=None, state=None, city=None):
    plt.figure(figsize=(10,5), dpi=100)
    if city is not None:
        selection_column = 'City'
        df = daf.country_wise_count(COVID_DATA_df, country,state, city)
        if isinstance(city,list):
            x_label_value = '-'.join(city)
            end_label = ' in cities of ' + '-'.join(city)
        else:
            x_label_value = city + ' Cities'
            end_label = ' in top 5 cities of ' + city
    elif state is not None:
        selection_column = 'Province/State'
        df = daf.country_wise_count(COVID_DATA_df, country,state)
        if isinstance(state,list):
            x_label_value = '-'.join(state)
            end_label = ' in states of ' + '-'.join(state)
        else:
            x_label_value = state + ' States'
            end_label = ' in top 5 states of ' + state
    elif country is not None:
        selection_column = 'Country/Region'
        df = daf.country_wise_count(COVID_DATA_df, country)
        if isinstance(country,list):
            x_label_value = '-'.join(country) + ' Countries'
            end_label = ' in countries of ' + '-'.join(country)
        else:
            x_label_value = country + ' Countries'
            end_label = ' in top 5 states of ' + country
    else:
        selection_column = 'Country/Region'
        df = daf.country_wise_count(COVID_DATA_df)
        x_label_value = 'Countries'
        end_label = ' in top 5 countries in the world'
    
    df = df[:5]
    ax = sns.pointplot(x=selection_column, y='Confirmed', data=df, join=False, label='Confirmed')
    sns.pointplot(x=selection_column, y='Recovered', data=df, join=False, color='green', ax=ax, label='Recovered')
    sns.pointplot(x=selection_column, y='Deaths', data=df, join=False, color='red', ax=ax, label='Deaths')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.set_title('Cases of CoronaVirus as on '+ CurrentDate.DATE_UPDATE + end_label)
    ax.set(xlabel=x_label_value, ylabel='Count')
    blue_patch = mpatches.Patch(color='blue', label='Confirmed')
    green_patch = mpatches.Patch(color='green', label='Recovered')
    red_patch = mpatches.Patch(color='red', label='Deaths')
    plt.legend(handles=[blue_patch, green_patch, red_patch])
    plt.show()
    df = 0


def plot_timeline_total(COVID_DATA_df, country=None, state=None, city=None):
    if city is not None:
        selection_column = 'City'
        df = daf.timeline_total(COVID_DATA_df, country, state, city)
        if isinstance(city,list):
            x_label_value = '-'.join(city) + ' Cities'
        else:
            x_label_value = city + ' City'
    elif state is not None:
        selection_column = 'Province/State'
        df = daf.timeline_total(COVID_DATA_df, country, state)
        if isinstance(state,list):
            x_label_value = '-'.join(state) + ' States'
        else:
            x_label_value = state + ' State'
    elif country is not None:
        selection_column = 'Country/Region'
        df = daf.timeline_total(COVID_DATA_df, country)
        if isinstance(country,list):
            x_label_value = '-'.join(country) + ' Countries'
        else:
            x_label_value = country + ' Country'
    else:
        selection_column = 'Country/Region'
        df = daf.timeline_total(COVID_DATA_df)
        x_label_value = 'World'

    df = df[df['Last Update'].isin(CurrentDate.time_list)]
    df['Confirmed'] = df['Confirmed']/1000
    df['Deaths'] = df['Deaths']/1000
    df['Recovered'] = df['Recovered']/1000
    plt.figure(figsize=(10,5), dpi=100)
    line_plot_ax = sns.lineplot(x='Last Update',y='Confirmed',data=df, label='Confirmed')
    line_plot_ax = sns.lineplot(x='Last Update',y='Deaths',data=df, color='red', ax = line_plot_ax, label='Deaths')
    line_plot_ax = sns.lineplot(x='Last Update',y='Recovered',data=df, color='green', ax = line_plot_ax, label='Recovered')
    line_plot_ax.set_title('Cases of Corona Virus in '+ x_label_value)
    line_plot_ax.set_xlabel('Time - Weekly')
    line_plot_ax.set_ylabel('Count in 1000\'s')
    plt.xticks(rotation=90)
    df = 0

def line_plotting_function(df,selection_column,x_label_value, x_value, y_value):
    df = df[df['Last Update'].isin(CurrentDate.time_list)]
    plt.figure(figsize=(10,5), dpi=100)
    line_plot_ax = sns.lineplot(x=x_value,y=y_value,data=df,hue=selection_column)
    line_plot_ax.set_title(y_value + ' Cases of Corona Virus in ' + x_label_value)
    line_plot_ax.set_xlabel('Time - Weekly')
    line_plot_ax.set_ylabel('Count')
    line_plot_ax.legend(loc='right', bbox_to_anchor=(1.15, 0.5), ncol=1, fontsize=8)
    plt.xticks(rotation=90)
    df = 0

def plot_timeline_countrywise_CONFIRMED(COVID_DATA_df, country=None, state=None, city=None):
    selection_column, df, x_label_value = daf.line_plot_initatizing_data(COVID_DATA_df, country, state, city)
    
    line_plotting_function(df,selection_column,x_label_value, 'Last Update', 'Confirmed')

def plot_timeline_countrywise_RECOVERED(COVID_DATA_df, country=None, state=None, city=None):
    selection_column, df, x_label_value = daf.line_plot_initatizing_data(COVID_DATA_df, country, state, city)
    
    line_plotting_function(df,selection_column,x_label_value, 'Last Update', 'Recovered')
    
def plot_timeline_countrywise_DEATHS(COVID_DATA_df, country=None, state=None, city=None):
    selection_column, df, x_label_value = daf.line_plot_initatizing_data(COVID_DATA_df, country, state, city)
    
    line_plotting_function(df,selection_column,x_label_value, 'Last Update', 'Deaths')

def plot_timeline_countrywise_ACTIVE(COVID_DATA_df, country=None, state=None, city=None):
    selection_column, df, x_label_value = daf.line_plot_initatizing_data(COVID_DATA_df, country, state, city)
    
    line_plotting_function(df,selection_column,x_label_value, 'Last Update', 'Active Cases')

def plot_timeline__new_cases_countrywise_CONFIRMED(COVID_DATA_df, country=None, state=None, city=None):
    selection_column, df, x_label_value = daf.line_plot_new_cases_initatizing_data(COVID_DATA_df, country, state, city)
    
    line_plotting_function(df,selection_column,x_label_value, 'Last Update', 'New Confirmed')

def plot_timeline__new_cases_countrywise_RECOVERED(COVID_DATA_df, country=None, state=None, city=None):
    selection_column, df, x_label_value = daf.line_plot_new_cases_initatizing_data(COVID_DATA_df, country, state, city)
    
    line_plotting_function(df,selection_column,x_label_value, 'Last Update', 'New Recovered')

def plot_timeline__new_cases_countrywise_DEATHS(COVID_DATA_df, country=None, state=None, city=None):
    selection_column, df, x_label_value = daf.line_plot_new_cases_initatizing_data(COVID_DATA_df, country, state, city)
    
    line_plotting_function(df,selection_column,x_label_value, 'Last Update', 'New Deaths')
