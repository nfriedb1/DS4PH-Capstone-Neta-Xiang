
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

st.title('Asthma Predictions by Census Tract in Baltimore City') 

#######################################################################
# GET CENSUS TRACT DATA FROM ADDRESS (by Neta)
#######################################################################

# user input address, but if nothing's entered yet, use default
street = st.text_input("Street Address: ", value = '615 N Wolfe Street')
city = st.text_input("City: ", value = 'Baltimore')
state = st.text_input("State Abbreviation: ", value = 'MD')
zipcode = st.text_input("5-Digit Zip Code: ", value = '21205')

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
st.header("Your Location:")
          
# make dataframe for map easy peasy
location_df = pd.DataFrame(coord_tuple, index = ['lat', 'lon']).swapaxes("index", "columns")
st.map(location_df, 13)

#######################################################################
# GET COORDINATES FROM MAP CLICK (optional????)
#######################################################################




