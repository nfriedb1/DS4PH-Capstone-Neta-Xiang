
#######################################################################
# Asthma predictions in Baltimore City
# Xiang Xiang Fang and Neta Friedberg
# See the README file for more info.
#######################################################################

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats as stats
sns.set()
from sklearn.metrics import accuracy_score, roc_curve, auc
import sklearn
from sklearn import linear_model
import sklearn.linear_model as lm
from sklearn.linear_model import LinearRegression
import seaborn as sns
import sklearn as skl
import statsmodels.formula.api as smf
import torch
import time

# Use censusgeocode for census tract info
# https://pypi.org/project/censusgeocode/
import censusgeocode as cg

st.set_page_config(page_title='Bmore Health', page_icon="🏥", layout = 'wide')
st.sidebar.header('HEALTH PREDICTIONS BY CENSUS TRACT IN BALTIMORE CITY')
column1, column2 = st.columns([1,1])

#######################################################################
# GET CENSUS TRACT DATA FROM ADDRESS (by Neta)
#######################################################################

# user input address, but if nothing's entered yet, use default
st.sidebar.subheader("Please enter an address: ")
street = st.sidebar.text_input("Street Address: ", value = '615 N Wolfe Street')
city = st.sidebar.text_input("City: ", value = 'Baltimore')
state = st.sidebar.text_input("State Abbreviation: ", value = 'MD')
zipcode = st.sidebar.text_input("5-Digit Zip Code: ", value = '21205')

##### finish the sidebar, while I'm at it #############################
st.sidebar.subheader("Please select a health outcome: ")
health_select = st.sidebar.selectbox(
    'Options:',
    ('Asthma', 'Lung cancer', 'Heart disease', 'Low birth weight'))
st.sidebar.subheader("ABOUT")
st.sidebar.write("Code: [GitHub](https://github.com/nfriedb1/DS4PH-Capstone-Neta-Xiang)") # eventually replace with Streamlit Share App (when hosted)
st.sidebar.write("Authors: [Xiang Xiang Fang](https://www.linkedin.com/in/xiangxiangfang1/) & [Neta Friedberg](https://www.linkedin.com/in/neta-friedberg/)")
#######################################################################

# a function to get a coordinate pair from an address
def getcoord(street, city, state, zipcode):
    geocode_result_fromaddress = cg.address(street, city = city, state = state, zipcode = zipcode, returntype = 'locations')[0]
    coords_full = geocode_result_fromaddress.get('coordinates') 
    lat = coords_full.get('y') # pro tip, the US census has these REVERSED on their website which is why y comes before x
    long = coords_full.get('x')
    return lat, long

# a function to get the census tract from a coordinate pair
def getcensus(lat, long):
    geocode_result_fromcoord = cg.coordinates(long, lat) # more US census shenanignas for why long comes first
    ct_full = geocode_result_fromcoord.get('Census Tracts')[0]
    ct = ct_full.get('GEOID')
    return ct

# get census tract from address
coord_tuple = getcoord(street, city, state, zipcode) # these are the CORRECT orientation, unlike what the airheads at the census want
ct = getcensus(coord_tuple[0], coord_tuple[1])

# show census tract (temporary)
#st.write("The census tract is: ", ct)

#######################################################################
# SHOW MAP WITH ADDRESS (by Neta)
#######################################################################

# label as location
with column1:
    st.subheader("Your Location:", anchor = None)

# make dataframe for map easy peasy
location_df = pd.DataFrame(coord_tuple, index = ['lat', 'lon']).swapaxes("index", "columns")

with column1:
    st.map(location_df, 13) 

#######################################################################
# GET COORDINATES FROM MAP CLICK (optional????)
#######################################################################

#######################################################################
# DATA SETUP (by Xiang Xiang)
#######################################################################

df = pd.read_csv("https://raw.githubusercontent.com/nfriedb1/DS4PH-Capstone-Neta-Xiang/main/DSPH_Capstone_Data.csv")
df = df.drop(df.loc[:, 'Unnamed: 12':'Unnamed: 23'].columns, axis = 1)
df = df.drop(["GEOID", "PTRAF"], axis = 1)
df = df.drop_duplicates(subset=None, keep='first', ignore_index=False)
df = df.drop(labels=[120, 403, 575], axis=0) #deleted rows with NA 


# get Y value depending on health_select
if health_select == 'Asthma':
    y = df['asthmavalue']
elif health_select == 'Lung cancer':
    y = df['lungCAvalue']
elif health_select == 'Heart disease':
    y = df['CADvalue']
elif health_select == 'Low birth weight':
    y = df['LBWvalue']

# set up X values
x = df[["svi_ptile", "transit_ptile"]]

# make final dataframe (need?)
df_final = pd.concat([x, y], axis=1)

x_withcensus = df[["ct", "svi_ptile", "transit_ptile"]]

fit2 = LinearRegression().fit(x, y)
yhat2 = fit2.predict(x)

#######################################################################
# GET PREDICTION (by Neta)
#######################################################################

def getPrediction(ct):
    ct = str(ct)
    #prediction = '0'
    for i in range(len(x_withcensus)):
        if str(x_withcensus['ct'].iloc[i]) == ct:
            x_svi = x_withcensus['svi_ptile'].iloc[i]
            x_transit = x_withcensus['transit_ptile'].iloc[i]
            x_pred = pd.DataFrame({'svi_ptile': [x_svi], 'transit_ptile': [x_transit]})
            prediction = fit2.predict(x_pred)
    if prediction is not None:
        prediction = np.array2string(prediction)[1:-1]
        prediction = float(prediction)
        prediction = round(prediction, 4)
        prediction = str(prediction)
        return(prediction)

prediction = getPrediction(ct)

percentile_pred = str(float(prediction) * 100)

# if we have time make this prettier
if health_select == 'Asthma':
    with column1:
        st.subheader("We predict "+ percentile_pred+ "% of adults in your census tract have asthma.", anchor = None)
        
    with column2: 
        st.title('What is Asthma?', anchor=None)
        st.markdown(""" Asthma is a chronic (long-term) condition that affects the airways in the lungs. With asthma, airways are swollen and inflamed,  making it difficult to carry air in and out of the lungs. The most common risk factors for developing asthma are family history, viral respiratory infections during childhood, allergies, smoking, and air pollution. Asthma symptoms vary from person to person. **Common signs and symptoms include:**
    
- Shortness of breath
    
- Chest tightness or pain
    
- Wheezing
    
- Trouble sleeping due to shortness of breath, coughing or wheezing
    
Asthma can worsen when certain triggers are present. Asthma attacks have been linked to triggers such as pollen, exercise, viral infections, cold weather, dust, smoke, and pet dander. Asthma cannot be cured but symptoms can be controlled by medications, avoiding triggers, and lifestyle changes. """)
elif health_select == 'Lung cancer':
    with column1:
        st.subheader("We predict "+ prediction+ " lung cancer cases in your census tract.", anchor = None) # figure out per X number of people if we have time
        
    with column2:
        st.title('What is Lung Cancer?', anchor=None)
        st.markdown(""" Lung cancer is a cancer that forms in the tissues of the lung. Common risk factors for developing asthma include smoking, family history, radiation exposure, air pollution, and HIV infection.  **Some symptoms of lung cancer include:**

- Chest pain or discomfort 

- Cough that doesn’t go away or gets worse over time 

- Trouble breathing 

- Wheezing 

- Trouble swallowing  

- Swelling in face or veins in the neck  

Treatment of lung cancer will depend on the type of lung cancer and how far it has spread. Common treatments include surgery, chemotherapy, immunotherapy and laser therapy. """)
elif health_select == 'Heart disease':
    with column1:
        st.subheader("We predict that your census tract is at the "+ percentile_pred+ "th percentile for number of patients released from a hospital after a heart attack.", anchor = None)
        
    with column2:
        st.title('What is Lung Cancer?', anchor=None)
        st.markdown(""" Heart disease is the leading cause of death in the U.S. The most common type of heart disease is coronary artery disease (CAD) which can lead to a heart attack. Risk factors for developing heart disease include diabetes, overweight and obesity, smoking, and environmental factors (air pollution, secondhand smoke).  **Symptoms of heart disease:**

- Chest pain, chest tightness, chest pressure 

- Shortness of breath  

- Pain, numbness, weakness or coldness in legs or arms  

- Pain in neck, jaw, throat, upper abdomen or back  

Treatment for heart disease includes lifestyle changes, medications, or medical procedure/surgery. """)
elif health_select == 'Low birth weight':
    with column1:
        st.subheader("We predict that your census tract is at the "+ percentile_pred+ "th percentile for number of babies born at a low birthweight, compared to the state of Maryland.", anchor = None)

#######################################################################
# GET MEANS OF ALL HEALTH OUTCOMES - FOR COMPARISON TO BMORE AVG (by Neta)
#######################################################################

lungmean = df['lungCAvalue'].mean()
asthmamean = df['asthmavalue'].mean() * 100
CADmean = df['CADvalue'].mean() * 100
LBWmean = df['LBWvalue'].mean() * 100