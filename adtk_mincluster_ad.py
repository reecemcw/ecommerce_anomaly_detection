# Multivariate Anomaly Detection
# To detect anomalous relationships between high level user metrics (sessions) and lower-level user-actions (transactions)
# Good for tracking two features at once and inferring a change in user's behaviour (either organic, or loss/gain of analytics)

# Import dependencies
from adtk.detector import MinClusterDetector
from sklearn.cluster import KMeans

# Specify date column in data. When pulled with Google Analytics Reporting API, the date format is not compatible with ADTK and must be converted to datetime (py)
DATE_COL = 'date'

# Specify data
csv_data = 'FILENAME.csv'

# Read to Pandas; parse dates as datetime
df = pd.read_csv(csv_data, index_col=DATE_COL, parse_dates=True)

# Get sub-division of data and write to dF. Specify desired columns
df2 = df[['sessions', 'transactions']]

# Validate for ADTK
df2 = validate_series(df2)

# Perform MinCluster analysis
min_cluster_detector = MinClusterDetector(KMeans(n_clusters=8))
anomalies = min_cluster_detector.fit_detect(df2)
plot(df2, anomaly=anomalies, ts_linewidth=1, ts_markersize=3, anomaly_color='red', anomaly_alpha=0.3, curve_group='all');

# Plot anomalies
plot(df2, curve_group=[["sessions", "transactions"]])

