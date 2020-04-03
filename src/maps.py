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

def mapping_plot(TYPE_DF, df, maptype, title_desc):
    fig, ax = plt.subplots(1, figsize=(20,8.5))
    ax.axis('off')
    ax.set_title(title_desc)
    TYPE_DF.plot(ax=ax, column=maptype, legend=True,scheme='fisher_jenks')
    
    #Emptying memory
    df = 0
    TYPE_DF = 0

def mapping_world(COVID_DATA_df,maptype):
    df = daf.country_wise_count(COVID_DATA_df)
    df.columns = df.columns.str.replace('Country/Region', 'COUNTRY')
    df['COUNTRY'] = df['COUNTRY'].replace('US','United States')
    df['COUNTRY'] = df['COUNTRY'].replace('Taiwan*','Taiwan')
    df['COUNTRY'] = df['COUNTRY'].replace('Congo (Kinshasa)','Democratic Republic of the Congo')
    df['COUNTRY'] = df['COUNTRY'].replace('Congo (Brazzaville)','Congo')
    
    world_country = gpd.read_file('./SHP-Files/World/World_Countries.shp')
    world_country = world_country[(world_country['COUNTRY'] != 'Antarctica')]
    world_country = pd.merge(world_country, df, on='COUNTRY', how='inner')
    title_desc = str(maptype + ' cases of Corona Virus in the World as on ' + CurrentDate.DATE_UPDATE)
    mapping_plot(world_country, df,maptype, title_desc)
    
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
    title_desc = str(maptype + ' cases of Corona Virus in US as on ' + CurrentDate.DATE_UPDATE)
    mapping_plot(us_states, df,maptype, title_desc)

def mapping_europe(COVID_DATA_df, maptype):
    df = daf.country_wise_count(COVID_DATA_df)
    df.columns = df.columns.str.replace('Country/Region', 'NAME')

    europe_continent = gpd.read_file('./SHP-Files/Europe/Europe.shp')
    europe_continent = pd.merge(europe_continent, df, on='NAME', how='inner')
    title_desc = str(maptype + ' cases of Corona Virus in Europe as on ' + CurrentDate.DATE_UPDATE)
    mapping_plot(europe_continent, df,maptype, title_desc)
    
def mapping_australia(COVID_DATA_df, maptype):
    df = COVID_DATA_df[COVID_DATA_df['Last Update'].str.contains(CurrentDate.DATE_UPDATE)]
    df = df[['Confirmed','Province/State','Deaths','Recovered']]
    df.columns = df.columns.str.replace('Province/State', 'NAME')
    
    australia_continent = gpd.read_file('./SHP-Files/Australia/Australia.shp')
    australia_continent = pd.merge(australia_continent, df, on='NAME', how='inner')
    title_desc = str(maptype + ' cases of Corona Virus in Australia as on ' + CurrentDate.DATE_UPDATE)
    mapping_plot(australia_continent, df,maptype, title_desc)

def mapping_americas(COVID_DATA_df, maptype):
    df = daf.country_wise_count(COVID_DATA_df)
    df.columns = df.columns.str.replace('Country/Region', 'COUNTRY')
    df['COUNTRY'] = df['COUNTRY'].replace('US','United States')
    
    americas_continent = gpd.read_file('./SHP-Files/Americas/Americas.shp')
    americas_continent = pd.merge(americas_continent, df, on='COUNTRY', how='inner')
    title_desc = str(maptype + ' cases of Corona Virus in Americas as on ' + CurrentDate.DATE_UPDATE)
    mapping_plot(americas_continent, df,maptype, title_desc)