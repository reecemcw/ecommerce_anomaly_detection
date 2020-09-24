# Dependencies
import pandas as pd
import numpy as np
from adtk.detector import ThresholdAD
from adtk.visualization import plot
from adtk.data import validate_series

# Import ecommerce data and specify date column for datetime indexing
DATE_COL = 'date'
csv_data = 'ecommerce_data.csv'


def load_data():
    global data
    data = pd.read_csv(csv_data)
    data[DATE_COL] = pd.to_datetime(data[DATE_COL])
    return data


load_data()


# NOT NEEDED AS ADTK HANDLES DATETIME INDEXING
# # data vis
# chart_data = data[['date', 'sessions']]
# chart_data.head


# # Convert df date colum to pd.Datetime and swap out date for datetime index in df2
# datetime_series = pd.to_datetime(chart_data['date'])
# datetime_index = pd.DatetimeIndex(datetime_series.values)
# df2=data.set_index(datetime_index)
# df2.drop('date',axis=1,inplace=True)

# # validate and data vis
# chart_data = df2[['sessions']]
# print(chart_data)



data = pd.read_csv(csv_data, index_col=DATE_COL, parse_dates=True)
s = data['sessions']
s = validate_series(s)

# Threshhold analysis
threshold_ad = ThresholdAD(high=100000, low=60000)
anomalies = threshold_ad.detect(s)

# Visualise threshold AD
plot(s, anomaly=anomalies, ts_linewidth=1, ts_markersize=3, anomaly_markersize=5, anomaly_color='red', anomaly_tag="marker");