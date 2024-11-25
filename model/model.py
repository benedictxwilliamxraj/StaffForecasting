import pickle
from darts.models import Prophet
from darts import TimeSeries
import streamlit as st

@st.cache_data
def load_model(df, project):
    series = TimeSeries.from_dataframe(df, time_col='Year-week', value_cols='NUMBERREGISTERED',fill_missing_dates=True, freq='W')
    model = Prophet( weekly_seasonality=True, seasonality_mode='multiplicative', seasonality_prior_scale=8)
    model.fit(series)
    #changepoint_prior_scale=0.2)
    return model

# Function to load the model
# def load_model(project):
#     model_path=f'model/md_{project}.pkl'
#     with open(model_path, 'rb') as f:
#         model = pickle.load(f)
#     return model

# Example prediction function
def predict(model,input_data):
    return model.predict(input_data)