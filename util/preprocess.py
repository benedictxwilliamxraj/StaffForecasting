import pandas as pd
from datetime import date
import datetime
import streamlit as st

@st.cache_data
def addattributesdata(data, datecol):
    pd.options.mode.copy_on_write = True
    data[datecol] = pd.to_datetime(data[datecol], format='%m/%d/%Y')
    data.loc[:, 'Year'] = data[datecol].dt.year
    data.loc[:, 'Month']  = data[datecol].dt.month
    data.loc[:, 'week'] = data[datecol].dt.isocalendar().week
    return data

@st.cache_data
def Cleandata(data):
    # dropping projects
    # PROJECTNAME: 25,15,35,36
    df_filtered = data[~data['PROJECTNAME'].isin([25,15,35,36])]
    return df_filtered

def AggHoursbyPT(data):
    # Yearly, weekly
    agg_data = data.groupby(['Year','week','PROJECTNAME']).agg({'EMPLOYEENUMBER': 'unique','NUMBERREGISTERED':'sum'}).reset_index()
    agg_data['emp_cnt'] = agg_data['EMPLOYEENUMBER'].apply(len)
    agg_data.loc[:,'Year-week'] = agg_data.apply(lambda r:get_sunday_of_week(r['Year'],r['week']), axis=1)
    agg_data.drop(agg_data[agg_data['week']==53].index, inplace=True)
    cols_req = ['Year','week','PROJECTNAME','NUMBERREGISTERED','emp_cnt','Year-week']
    agg_data = agg_data[(agg_data['Year']<date.today().year)]
    agg_data = agg_data[cols_req]
    return agg_data


def get_sunday_of_week(y,w):
    year = int(y)  # Extract year (e.g., '2023')
    week = int(w)  # Extract week number (e.g., '05' -> 5)

    # Start from January 1st of the specified year
    start_of_year = datetime.datetime(year, 1, 1)

    # Calculate the start of the specified week
    start_of_week = start_of_year + datetime.timedelta(weeks=week - 1)

    # Adjust to get the Sunday of that week
    sunday_of_week = start_of_week + datetime.timedelta(days=(6 - start_of_week.weekday()))
    return sunday_of_week

def assigncat(categorynumber):
    if categorynumber == '10':
        cat = 'Intern'
    elif (categorynumber == '11') or (categorynumber == '27'):
        cat = 'DC'
    elif (categorynumber == '13') or (categorynumber == '14'):
        cat = 'SU'
    elif (categorynumber == '15') or (categorynumber == '16'):
        cat = 'SEN'
    else:
        cat = 'MAN'
    return cat