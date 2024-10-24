import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import pickle
import os


# Loading data
data = pd.read_csv('../data/UB_Project_Data_csv.csv')
data['ENTRYDATE'] = pd.to_datetime(data['ENTRYDATE'], format='%d/%m/%Y')
# aggregate data weekly
para = ['ENTRYDATE','EMPLOYEENUMBER','EMPLOYEECATEGORYNUMBER','PROJECTNAME','JOBNUMBER','TASKNAME','NUMBERREGISTERED']
df = data[para]
#df.dtypes
df['Year'] = df['ENTRYDATE'].dt.year
df['Month'] = df['ENTRYDATE'].dt.month
df['week'] = df['ENTRYDATE'].dt.isocalendar().week

stf = df.groupby([df.Year,df.Month,df.week, df.TASKNAME,df.PROJECTNAME]).agg({'NUMBERREGISTERED':'sum','EMPLOYEENUMBER':'nunique'}).reset_index().rename(columns={"EMPLOYEENUMBER": "count"})

# Define features and target
X = stf[['Month', 'week', 'TASKNAME', 'PROJECTNAME']]  
y = stf['count']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf_model = RandomForestRegressor(n_estimators=100, random_state=50)
rf_model.fit(X_train, y_train)

dir = 'C://Users/Yellowflash/Desktop/MSBA/Project Clinic/CTBK/dashboard/model'

with open('saved_model.pkl', 'wb') as file:
    pickle.dump(rf_model, file)
        #st.write("Model loaded successfully!")

