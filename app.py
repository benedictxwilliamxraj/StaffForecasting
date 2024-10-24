import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from model import model as ml_model
from util import preprocess



# Sidebar for input
# st.sidebar.title("")
# input_data = {
#     'Month': [st.sidebar.number_input("Month", min_value=0, max_value=12)],
#     'week': [st.sidebar.number_input("Week", min_value=0, max_value=53)],
#     'TASKNAME': [st.sidebar.number_input("Task Name")],
#     'PROJECTNAME': [st.sidebar.number_input("Project Name")],  
# }

# input_df = pd.DataFrame(input_data)
#Hardcoded for now
def loadData():
    data = pd.read_csv('data/UB_Project_Data_csv.csv')
    return data

# if st.button("Predict"):
#     prediction = ml_model.predict(input_df, model)
#     st.write(f"Prediction: {int(prediction[0])}")

if __name__=="__main__":
    st.set_page_config(layout="wide")
    #Load data 
    raw_data = loadData()
    clean_df = preprocess.Cleandata(raw_data)
    stf_yearly, stf_monthly = preprocess.AggStaffbyPT(df=clean_df)
    
    # Catplot for Employee Count per Project Over the Years
    st.title("Employee Count per Project Over the Years")
    cat_plot = sns.catplot(x="Year",y="count", hue="PROJECTNAME", kind="bar", data=stf_yearly,height=7,aspect=2)
    
    st.pyplot(cat_plot, )

    # Catplot for Employee Count per Project for next year
    # set of Tasknames and Project Names
    projects = pd.DataFrame(clean_df['PROJECTNAME'].unique(), columns=['PROJECTNAME'])
    tasks = pd.DataFrame(clean_df['TASKNAME'].unique(), columns=['TASKNAME'])
    projects['key'] = 1
    tasks['key'] = 1
    # Perform a cross join using merge on the key column
    projtask_df = pd.merge(tasks, projects, on='key').drop('key', axis=1)
    # Load the trained model
    emp_year_model = ml_model.load_yearly_model()
    projtask_df['predicted_count'] = ml_model.predict(projtask_df, emp_year_model)
    projtask_df['predicted_count'] = projtask_df['predicted_count'].astype(int)
    
    # st.title("Employee Count per Project For next Years")
    # cat_plot = sns.catplot(x="PROJECTNAME",y="predicted_count", hue="TASKNAME", kind="bar", data=projtask_df,height=7,aspect=2)
    # st.pyplot(cat_plot)

    # For each project => task will have count
    data_container = st.container()
    for i in range(len(projects)):
        fdf = projtask_df[projtask_df['PROJECTNAME'] == projects.iloc[i]['PROJECTNAME']]
        
        with data_container:
            st.title(f'Employee Count of Project {projects.iloc[i]['PROJECTNAME']} for next Year')
            table, plot = st.columns(2)
            with table:
                #st.table(data=fdf)
                st.dataframe(fdf, height=300)
            with plot:
                cat_plot = sns.catplot(x="TASKNAME",y="predicted_count", kind="bar", data=fdf,height=7,aspect=2)
                st.pyplot(cat_plot)

    # Table for Monthly prediction of Employee foc next year
