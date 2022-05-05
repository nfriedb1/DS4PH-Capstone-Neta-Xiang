
#######################################################################
# Asthma predictions in Baltimore City
# Xiang Xiang Fang and Neta Friedberg
# See the README file for more info.
#######################################################################

import streamlit as st
import pandas as pd
import numpy as np

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
    ('Asthma', 'Lung cancer', 'Coronary artery disease', 'Low birth weight'))
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
st.write("The census tract is: ", ct)

#######################################################################
# SHOW MAP WITH ADDRESS (by Neta)
#######################################################################

# label as location
with column1:
    st.subheader("Your Location:")

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

with column2:
    st.dataframe(df) #(temporary)

# get Y value depending on health_select
if health_select == 'Asthma':
    y = df['asthmavalue']
elif health_select == 'Lung cancer':
    y = df['lungCAvalue']
elif health_select == 'Coronary artery disease':
    y = df['CADvalue']
elif health_select == 'Low birth weight':
    y = df['LBWvalue']

# set up X values


