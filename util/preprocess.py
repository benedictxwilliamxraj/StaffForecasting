import pandas as pd 

def Cleandata(data):
    pd.options.mode.copy_on_write = True
    para = ['ENTRYDATE','EMPLOYEENUMBER','EMPLOYEECATEGORYNUMBER','PROJECTNAME','JOBNUMBER','TASKNAME','NUMBERREGISTERED']
    # Changing ENTRYDATE type
    data['ENTRYDATE'] = pd.to_datetime(data['ENTRYDATE'], format='%d/%m/%Y')
    df = data[para]
    #df.dtypes
    # Adding other dimensions
    df.loc[:, 'Year'] = df['ENTRYDATE'].dt.year
    df.loc[:, 'Month']  = df['ENTRYDATE'].dt.month
    df.loc[:, 'week'] = df['ENTRYDATE'].dt.isocalendar().week
    return df


def AggStaffbyPT(df):
    # Monthly and weekly
    stf_monthly = df.groupby([df.Year,df.Month,df.week, df.TASKNAME,df.PROJECTNAME]).agg({'NUMBERREGISTERED':'sum','EMPLOYEENUMBER':'nunique'}).reset_index().rename(columns={"EMPLOYEENUMBER": "count"})
    stf_yearly = df.groupby([df.Year, df.TASKNAME,df.PROJECTNAME]).agg({'NUMBERREGISTERED':'sum','EMPLOYEENUMBER':'nunique'}).reset_index().rename(columns={"EMPLOYEENUMBER": "count"})

    return stf_monthly, stf_yearly

