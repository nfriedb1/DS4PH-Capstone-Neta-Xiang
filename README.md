# Health Outcome Predictions by Census Tract
### Xiang Xiang Fang and Neta Friedberg

Our app asks for a Baltimore City address and gives a prediction about each of the following health outcomes at the census tract level: asthma, heart disease, lung cancer, and low birh weight.
Our project is based on the Baltimore Transit Equity Coalition (BTEC) & JHU report, which found areas in Baltimore city that are in greatest need of transit improvements, based on four indicator groups: transit, health, social vulnerability, and air pollution.
The full report can be found here:
https://americanhealth.jhu.edu/news/transit-equity-environmental-health-baltimore

### Prediction models

We tried several different models for each outcome and compared the MSE of each model. For all outcomes we tried linear regression and a basic neural network with one hidden layer with two nodes. For lung cancer counts, we tried a Poisson model.
For all outcomes, the linear regression model had the lowest MSE, so we used it for our model. However, this model was only a strong predictor for asthma (R^2 = 0.7), while the model did not show good correlation with the other health outcomes (R^2 = 0.1 or lower). 
When building our linear regression model, we considered several different predictors relating to access to transportation, air pollution, and social vulnerability. Our air pollution variable (traffic density) was highly collinear with the other variables, so we excluded it from our model. Our final linear regression model included 2 covariates: Social Vulnerability Index (svi_ptile) and Access to Transit (transit_ptile). These variables were used in the BTEC & JHU report above. 

All of our models can be found in DataSetUp.ipynb.

### Individual Contributions

Xiang Xiang set up the data and build the prediction models, and assembled health information about each of the outcomes.
Xiang Xiang's video can be found here:

Neta built the majority of the Streamlit app, hosted it online, and ensured functionality of the sidebar, map, and outputs. 
Neta's video can be found here:

### System requirements

Python 3.7

### Library requirements

streamlit, pandas, numpy, matplotlib

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
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

