import os
import pandas as pd

def importfiles():
    files_list = [file for file in os.listdir('./Data/csse_covid_19_daily_reports/') if file.endswith('.csv')]

    COVID_DATA_df = pd.DataFrame(columns = ['Province/State', 'Country/Region', 'Last Update', 'Confirmed', 'Deaths', 'Recovered'])
    
    for file in files_list:
        file_path = './Data/csse_covid_19_daily_reports/' + file
        temp_df = pd.read_csv(file_path)
        temp_df.columns = temp_df.columns.str.replace('Province_State', 'Province/State')
        temp_df.columns = temp_df.columns.str.replace('Country_Region', 'Country/Region')
        temp_df.columns = temp_df.columns.str.replace('Last_Update', 'Last Update')
        temp_df = temp_df.fillna(0)
        temp_df['Country/Region'] = temp_df['Country/Region'].replace('Mainland China','China')
        temp_df = temp_df[['Province/State', 'Country/Region', 'Last Update', 'Confirmed', 'Deaths', 'Recovered']]
        temp_df['Last Update'] = str(file.split('.')[0])
        COVID_DATA_df = pd.concat([COVID_DATA_df,temp_df], ignore_index=True, axis=0)
    return COVID_DATA_df

def cities_usa_importfiles():
    files_list = [file for file in os.listdir('./Data/csse_covid_19_daily_reports/') if file.endswith('.csv')]

    COVID_DATA_df = pd.DataFrame(columns = ['Province/State', 'Country/Region', 'Last Update', 'Confirmed', 'Deaths', 'Recovered','Admin2'])
    
    index_pos = files_list.index('03-22-2020.csv')
    for file in files_list[index_pos:]:
        file_path = './Data/csse_covid_19_daily_reports/' + file
        temp_df = pd.read_csv(file_path,dtype={"FIPS": str})
        temp_df.columns = temp_df.columns.str.replace('Province_State', 'Province/State')
        temp_df.columns = temp_df.columns.str.replace('Country_Region', 'Country/Region')
        temp_df.columns = temp_df.columns.str.replace('Last_Update', 'Last Update')
        temp_df = temp_df[temp_df['Country/Region']=='US']
        temp_df = temp_df.fillna(0)
        temp_df['Country/Region'] = temp_df['Country/Region'].replace('Mainland China','China')
        temp_df = temp_df[['FIPS','Province/State', 'Country/Region', 'Last Update', 'Confirmed', 'Deaths', 'Recovered','Admin2']]
        temp_df['Last Update'] = str(file.split('.')[0])
        COVID_DATA_df = pd.concat([COVID_DATA_df,temp_df], ignore_index=True, axis=0)
    COVID_DATA_df.columns = COVID_DATA_df.columns.str.replace('Admin2', 'City')
    return COVID_DATA_df
