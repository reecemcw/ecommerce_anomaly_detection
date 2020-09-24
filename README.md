# Ecommerce Anomaly Detection
Example project merging a Google Analytics Reporting query to fetch sample Ecommerce marketing data and passing it to ADTK to perform anomaly detections based on use cases.

Anomaly detections include:

### 1) Threshold Anomalies
_univariate_  
**sessions only**
A high level engagement metric (web sessions) is measured against upper and lower threshold. Outliers to the threshold are plotted and returned in a anomaly dF. Useful for when the norm is known and idetifying gradual drops in traffic or unexpected peaks (bots/spam)


### 2) Minimum Cluster Analysis 
_multivariate_
**session & transactions**
Takes two web traffic variables and measures for anomalies based on localised descrepancies between the two compared to the entire dataset. Useful for seeing anomalous user behaviour which cannot be inferred from each individual variable, eg. declining conversion rate despite session increase / broken ecommerce funnels / sales upticks 
