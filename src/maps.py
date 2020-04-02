import sys
sys.path.append('./')
import pandas as pd
import geopandas as gpd
import pysal
import descartes
from matplotlib import pyplot as plt
from src import DataFormatting as daf
from src import CurrentDate
import warnings
warnings.filterwarnings("ignore")

def world_mapping(COVID_DATA_df,maptype):
    df = daf.country_wise_count(COVID_DATA_df)
    df.columns = df.columns.str.replace('Country/Region', 'COUNTRY')
    df['COUNTRY'] = df['COUNTRY'].replace('US','United States')
    df['COUNTRY'] = df['COUNTRY'].replace('Taiwan*','Taiwan')
    df['COUNTRY'] = df['COUNTRY'].replace('Congo (Kinshasa)','Democratic Republic of the Congo')
    df['COUNTRY'] = df['COUNTRY'].replace('Congo (Brazzaville)','Congo')
    
    world_country = gpd.read_file('./SHP-Files/World/World_Countries.shp')
    world_country = world_country[(world_country['COUNTRY'] != 'Antarctica')]
    world_country = pd.merge(world_country, df, on='COUNTRY', how='inner')
    fig, ax = plt.subplots(1, figsize=(20,8.5))
    ax.axis('off')
    world_country.plot(ax=ax, column='Confirmed', legend=True)
    
    #Emptying memory
    df = 0
    world_country = 0

def mapping_usa(US_COVID_DATA_df, maptype):
    df = US_COVID_DATA_df[US_COVID_DATA_df['Last Update'].str.contains(CurrentDate.DATE_UPDATE)]
    df = df[['FIPS','Confirmed','Province/State','Deaths','Recovered']]
    df.columns = df.columns.str.replace('Province/State', 'NAME')
    df = df.groupby(['NAME']).agg({'Confirmed':['sum'], 'Deaths':['sum'], 'Recovered':['sum']})
    df = df.reset_index()
    df.columns = df.columns.droplevel(1)
    df = df.sort_values(by=['Confirmed'], ascending=False)
    
    us_states = gpd.read_file('./SHP-Files/US/USStates.shp')
    us_states = us_states[(us_states['NAME'] != 'Alaska') 
                & (us_states['NAME'] != 'Hawaii')
                & (us_states['NAME'] != 'Puerto Rico')
                & (us_states['NAME'] != 'Virgin Islands')
                & (us_states['NAME'] != 'Guam')]

    projection = "+proj=laea +lat_0=30 +lon_0=-95"
    us_states = us_states.to_crs(projection)
    us_states = pd.merge(us_states, df, on='NAME', how='inner')
    fig, ax = plt.subplots(1, figsize=(15,8.5))
    ax.axis('off')
    ax.set_title(maptype + ' cases of Corona Virus in US as on ' + CurrentDate.DATE_UPDATE)
    us_states.plot(ax=ax, column=maptype, legend=True)
    
    #Emptying memory
    df = 0
    us_states = 0
