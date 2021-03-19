import streamlit as st
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
import category_encoders as ce 
from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler

st.header("Data Preprocessing App")


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    



local_css("style.css")
remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

# dataset_name = st.sidebar.selectbox(
#     'Select Dataset',
#     ('Real Estate', 'Position Salaries','Google PlayStore', 'StartUp')
# )
# st.write(f"### {dataset_name} Dataset")





# def dataset(name):
#             if name == 'Real Estate':
#                 data = pd.read_csv(r'/Users/Naila/Documents/Datasets/Real estate.csv')
#             elif name == 'Position Salaries':
#                 data = pd.read_csv(r'/Users/Naila/Documents/Datasets/Position_Salaries.csv')
#             elif name == 'Google PlayStore':
#                 data = pd.read_csv(r'/Users/Naila/Documents/Datasets/googleplaystore.csv')
#             else:
#                 data = pd.read_csv(r'/Users/Naila/Documents/Datasets/50_Startups (2).csv')
#             return data
# def get_dataset(name):
#     data = None
#     if name == 'Real Estate':
#         data = pd.read_csv(r'/Users/Naila/Documents/Datasets/Real estate.csv')
#         X = data.iloc[:,:3].values
#         y = data.iloc[:,-1].values
    
#     elif name == 'Position Salaries':
#             data = pd.read_csv(r'/Users/Naila/Documents/Datasets/Position_Salaries.csv')
#             X = data.iloc[:, 1:-1].values
#             y = data.iloc[:, -1].values 
#     else:
#         data = pd.read_csv(r'/Users/Naila/Documents/Datasets/50_Startups (2).csv')
#         X = data.iloc[:, :-1].values
#         y = data.iloc[:, -1].values
#     return X,y
# X, y = get_dataset(dataset_name)













def main():
    data_file = st.sidebar.file_uploader("Upload CSV or Excel file",type=["csv","xls","xlsx"])
    if data_file is not None:
        file_details = {"filename":data_file.name,
                            "filetype":data_file.type, 
                            "filesize":data_file.size}
        #st.write(file_details)
        if data_file.type=="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            df = pd.read_excel(data_file)
        else:
            df = pd.read_csv(data_file)
            
        return df
        
data = main()       


dataset_choosing = st.sidebar.selectbox(
    'Show  Dataset',
    ('No', 'Yes')
)

try:
    if dataset_choosing == 'Yes':
         st.write('Shape of dataset:', data.shape)
         st.dataframe(data)
except:
    pass

#Encoding
choose_encoding= st.sidebar.selectbox(
    'Encoding',
    ('No','Yes')
    
)


def data_encoding(data,ohe,le,be,col_name_0,col_name_1,col_name_2):    
    if ohe:
        for i in range(0,len(col_name_0)):
            data=pd.get_dummies(data,prefix=[col_name_0[i]],columns=[col_name_0[i]])
            
    if le:
        for i in range(0,len(col_name_1)):
            data[col_name_1[i]]=LabelEncoder().fit_transform(data[col_name_1[i]])
            
    if be:
        for i in range(0,len(col_name_2)):
            encoder=ce.BinaryEncoder(cols=[col_name_2[i]]) 
            data_bin=encoder.fit_transform(data[col_name_2[i]])
            data=pd.concat([data,data_bin],axis=1)
            del data[col_name_2[i]]
            
    return data 


if choose_encoding == 'Yes':
    data_copy=data
    ohe=False
    le=False
    be=False
    choose_column_2=None
    choose_column_3=None
    choose_column_4= None
    if st.sidebar.checkbox('One Hot Encoding'):
        ohe=True
        choose_column_2 = st.sidebar.multiselect('Select Columns for One Hot Encoding', data_copy.columns)
        data_copy=data_copy.drop(choose_column_2,axis=1)
        if len(choose_column_2)>0:
            if st.sidebar.checkbox('Show Unique Values of Selected Columns'):
                for i in range(0,len(choose_column_2)):
                    st.write(f"#### Unique values of '{choose_column_2[i]}' :")
                    st.write(data[choose_column_2[i]].unique())
    if st.sidebar.checkbox('Label Encoding'):
        le=True
        choose_column_3 = st.sidebar.multiselect('Select Columns for Label Encoding', data_copy.columns)
        data_copy=data_copy.drop(choose_column_3,axis=1)
        
    if st.sidebar.checkbox('Binary Encoding'):
        be=True
        choose_column_4 = st.sidebar.multiselect('Select Columns for Binary Encoding', data_copy.columns)
        data_copy=data_copy.drop(choose_column_4,axis=1)
try:
    data=data_encoding(data,ohe,le,be,choose_column_2,choose_column_3,choose_column_4)
    
except:
    pass


#Feature Scaling
choose_scaling= st.sidebar.selectbox(
    'Feauture Scaling',
    ('No','Yes')
    
)
def feature_scale(data,min_max,standard,col_0,col_1):
    if min_max:
        scaler = MinMaxScaler()
        result=scaler.fit_transform(data[col_0])
        
        for i in range(0,len(col_0)):
            data[col_0[i]]=result[:,i]
    if standard:
        sc = StandardScaler()
        result=sc.fit_transform(data[col_1])
        
        for i in range(0,len(col_1)):
            data[col_1[i]]=result[:,i]
    return data


if choose_scaling == 'Yes':
    data_copy=data
    min_max=False
    standard=False
    choose_column_2=0
    choose_column_3=0
    if st.sidebar.checkbox('Min-Max Scalar'):
        min_max=True
        choose_column_2 = st.sidebar.multiselect('Select Columns for Min-Max Scalar', data_copy.select_dtypes(exclude=['object']).columns)
        data_copy=data_copy.drop(choose_column_2,axis=1)
    if st.sidebar.checkbox('Standard Scalar'):
        standard=True
        choose_column_3 = st.sidebar.multiselect('Select Columns for Standard Scalar', data_copy.select_dtypes(exclude=['object']).columns)
        data_copy=data_copy.drop(choose_column_3,axis=1)
try:
    data=feature_scale(data,min_max,standard,choose_column_2,choose_column_3)
except:
    pass        






    



if st.sidebar.button("Show Dataset"):
    st.table(data.head(10))

