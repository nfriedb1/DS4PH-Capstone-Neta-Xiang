# Health Outcome Predictions by Census Tract
### Xiang Xiang Fang and Neta Friedberg

#### Find the app online here (desktop only): https://share.streamlit.io/nfriedb1/ds4ph-capstone-neta-xiang/main/asthma.py

### Background

Our app asks for a Baltimore City address and gives a prediction about each of the following health outcomes at the census tract level: asthma, heart disease, lung cancer, and low birh weight. It is an informational app intended for use by Baltimore residents that are interested in their health.
Our project is based on the Baltimore Transit Equity Coalition (BTEC) & JHU report, which found areas in Baltimore city that are in greatest need of transit improvements, based on four indicator groups: transit, health, social vulnerability, and air pollution.
The full report can be found here:
https://americanhealth.jhu.edu/news/transit-equity-environmental-health-baltimore

### Prediction models

We tried several different models for each outcome and compared the MSE of each model. For all outcomes we tried linear regression and a basic neural network with one hidden layer with two nodes. For lung cancer counts, we tried a Poisson model.
For all outcomes, the linear regression model had the lowest MSE, so we used it for our model. However, this model was only a strong predictor for asthma (R^2 = 0.7), while the model did not show good correlation with the other health outcomes (R^2 = 0.1 or lower). 
When building our linear regression model, we considered several different predictors relating to access to transportation, air pollution, and social vulnerability. Our air pollution variable (traffic density) was highly collinear with the other variables, so we excluded it from our model. Our final linear regression model included 2 covariates: Social Vulnerability Index (svi_ptile) and Access to Transit (transit_ptile). These variables were used in the BTEC & JHU report above. 

All of our models can be found in DataSetUp.ipynb.

### Individual Contributions

Xiang Xiang set up the data, built the prediction models, and assembled health information about each of the outcomes.
Xiang Xiang's video can be found here: https://youtu.be/Rqixjw5a5hw

Neta built the majority of the Streamlit app, hosted it online, and ensured functionality of the sidebar, map, and outputs. 
Neta's video can be found here: https://youtu.be/eAiqN6DPzkI (Unfortunately it is bad quality and for some reason clipped the left edge of the screen. Luckily you can access the app and try it yourself!)

### System & Library requirements

Find app dependencies in Pipfile. App runs on Python 3.7. Other supplementary files may require other dependencies, but does not alter the functionality of the app.

