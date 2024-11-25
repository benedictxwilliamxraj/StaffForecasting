import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from model import model as ml_model
from util import preprocess, employee_alloc
import plotly.express as px
import os
import plotly.graph_objects as go




def loadData():
    data = pd.read_csv('data/UB_Project_Data_V2.csv')
    return data


if __name__=="__main__":
    st.set_page_config(layout="wide")
    st.title("Employee Resource Planning")
    #Load data 
    raw_data = loadData()
    new_df = preprocess.addattributesdata(raw_data,'ENTRYDATE')
    clean_df = preprocess.Cleandata(new_df)
    #agg_data
    agg_data = preprocess.AggHoursbyPT(clean_df)

    #Sidebar Filer options
    st.sidebar.title("CTBK: Chiampou Travis Besaw & Kershner")
    project = st.sidebar.selectbox("Project", options=agg_data['PROJECTNAME'].unique(),index=0)
    #week = st.sidebar.selectbox("Week", options=agg_data['week'].unique(),index=0)
    st.sidebar.subheader("Forecast")
    forecast_week = st.sidebar.number_input("Week",min_value=1, max_value=52, step=1, value=50)
    #Efficiency of employee
    st.sidebar.subheader("Efficiency")
    eff_percent = st.sidebar.number_input("in %",min_value=0, max_value=100, step=1, value=30)
    # Employee count
    st.sidebar.subheader("CATEGORY")
    man_count = st.sidebar.number_input("MAN",min_value=0, max_value=100, step=1, value=74)
    intern_count = st.sidebar.number_input("INTERN",min_value=0, max_value=100, step=1, value=19)
    dc_count = st.sidebar.number_input("DC",min_value=0, max_value=100, step=1, value=9)
    sen_count = st.sidebar.number_input("SEN",min_value=0, max_value=100, step=1, value=42)
    su_count = st.sidebar.number_input("SU",min_value=0, max_value=100, step=1, value=47)

    max_empcnt = {'MAN': man_count, 'Intern':intern_count, 'DC': dc_count, 'SEN': sen_count, 'SU':su_count}

    # Filter the project data
    agg_proj = agg_data[(agg_data['PROJECTNAME']==project)]
    st.subheader(f"Hours registered for Project {project}")

    if not agg_proj.empty:
        fig = px.line(agg_proj, x='Year-week', y='NUMBERREGISTERED',title="Hours registered over the years", markers=True)
        st.plotly_chart(fig)
    else:
        st.warning("No data available for the selected filters.")

    # Load model
    seasonal_projects = [10,11,12,14,17,18,19,24]
    if project in seasonal_projects:
        st.subheader('Forecasted Hours')
        model = ml_model.load_model(agg_proj, project)
        hrs = model.predict(52)
        predict_df = hrs.pd_dataframe().reset_index()
        fig = px.line(predict_df, x='Year-week', y='NUMBERREGISTERED',title=f"Forecasted Hours for 52 weeks ", markers=True)
        st.plotly_chart(fig)
        #st.write(predict_df)

    else:
        predict_df = agg_proj.groupby(['week']).agg({'NUMBERREGISTERED':'mean'}).reset_index()

        fig = px.line(predict_df, x='week', y='NUMBERREGISTERED',title=f"Avg Hours for 52 weeks", markers=True)
        st.plotly_chart(fig)


    col1, col2 = st.columns(2)
    with col1:
    # pie chart
        if project in seasonal_projects:
            pred_df = preprocess.addattributesdata(predict_df,'Year-week')
        else:
            pred_df = predict_df
        completed_df = pred_df[(pred_df['week'] <= forecast_week)]
        completed_hrs = completed_df['NUMBERREGISTERED'].sum()
        total_hrs = pred_df['NUMBERREGISTERED'].sum()
        data = pd.DataFrame({
            'Hours': ['Completed', 'Remaining'],
            'Values': [completed_hrs, total_hrs-completed_hrs]
        })
        fig = px.pie(data, values='Values', names='Hours', title='Project Completion')
        st.plotly_chart(fig)
    # Table to show employee cnt categorically
    ut = pd.read_csv('data/StdHourscsv.csv')
    #billable hours weekl
    billhrs = {}
    for i in range(len(ut)):
       intern = ut.iloc[i]['Intern']
       billhrs.setdefault(ut.iloc[i]['Week Number'],{'Intern':intern, 'DC': ut.iloc[i]['DC'],'SEN':ut.iloc[i]['SEN'],'SU':ut.iloc[i]['SU'], 'MAN':ut.iloc[i]['MAN']})

    eff = eff_percent/100

    with col2:
        actual_billhrs ={key_value: round(billhrs[forecast_week][key_value]*eff,2) for key_value in billhrs[forecast_week]}
        #st.subheader("Hours Required")
        subcol1, subcol2 = st.columns(2)
        with subcol1:
            st.metric(label="Hours Required", value=round(pred_df.iloc[forecast_week-1]['NUMBERREGISTERED'],2))
        with subcol2:
            st.metric(label="Week", value=forecast_week)
        emp_cat = employee_alloc.allocate_employees(pred_df.iloc[forecast_week-1]['NUMBERREGISTERED'], actual_billhrs, max_empcnt)
        emp_cat_df = pd.DataFrame(emp_cat, index=[0])
        actual_billhrs_df = pd.DataFrame(actual_billhrs, index=[0])
        # table
        table1 = go.Figure(data=[go.Table(
            header=dict(values=list(emp_cat_df.columns),
                        fill_color='lightblue',
                        align='center',
                        font=dict(size=14, color='black')),
            cells=dict(values=[emp_cat_df[col] for col in emp_cat_df.columns],
                       fill_color='white',
                       align='center',
                       font=dict(size=12, color='black'))
        )])

        table2 = go.Figure(data=[go.Table(
                    header=dict(values=list(actual_billhrs_df.columns),
                                fill_color='lightblue',
                                align='center',
                                font=dict(size=14, color='black')),
                    cells=dict(values=[actual_billhrs_df[col] for col in actual_billhrs_df.columns],
                               fill_color='white',
                               align='center',
                               font=dict(size=12, color='black'))
                )])
        st.subheader("Employee Assigned")
        table1.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=100,showlegend=False,template='plotly_white')  # Remove margin
        table2.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=100,showlegend=False,template='plotly_white')
        st.plotly_chart(table1, use_container_width=True)
        #st.markdown("---")  # Add a horizontal line to separate the tables
        st.subheader("Hours Billed")
        st.plotly_chart(table2, use_container_width=True)
#         st.write(emp_cat_df)
#         st.write(actual_billhrs_df)
    # Employee count
