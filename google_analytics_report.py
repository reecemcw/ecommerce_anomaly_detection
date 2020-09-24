# Import dependencies
import pandas as pd
from apiclient.discovery import build
from datetime import datetime, timedelta
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
import socket
import pandas_gbq
from google.cloud import bigquery


# Authentication for Google Analytics Reporting API calls
scope = 'https://www.googleapis.com/auth/analytics.readonly'
credentials = service_account.Credentials.from_service_account_file('client_secret.json')
service = build('analytics', 'v3', credentials=credentials)


# Date variables -- Used for specifying date range of data pull
today = datetime.now().date()
yesterday = today - timedelta(days=1)


#b Builds query based on arguments specified
def analytics_query(client_id, index, start_date, end_date, dimensions, metrics): 	
	# 7 dimensions, 10 metrics limit. This formats the user input later on to work with the Reporting API
	data = service.data().ga().get(
		ids='ga:' + client_id,
		start_date=start_date,
		end_date=end_date,
		metrics=metrics,
		dimensions=dimensions,
		start_index=index,
		max_results=10000).execute()

	return data


# Pulls data with Reporting API
def analytics_get_report(client_id, start_date, end_date, dimensions, metrics):
	
	index = 1
	totalResults = 2
	output = []

	while totalResults > index:
		a = analytics_api_query(client_id, index, start_date, end_date, dimensions, metrics)
		totalResults = a.get('totalResults')
		index = index + 10000

		try:
			for row in a.get('rows'):
				output.append(row)
		except:
			pass

	return output




def main(client_id):

	base_df = pd.DataFrame()
	columns = traffic_columns

    # Specify report start date here
	start_date = '2020-01-01' 
	start_date = datetime.strptime(start_date , '%Y-%m-%d').date()

	print('Running Google Analytics Report.')
	
	
	# Change the locator based on the list of metrics/dimensions below. The locator should capture the grouped positions of metrics and dimensions (eg up to row 1 = dimensions; after row 1 = metrics). 
	dimensions = 'ga:'+(',ga:'.join(columns[:1]))
	metrics = 'ga:'+(',ga:'.join(columns[1:]))
	
	results = analytics_get_report(client_id, str(start_date), str(yesterday), dimensions, metrics)
	df = pd.DataFrame(results, columns=columns)

	df['view_id'] = client_id
	base_df = base_df.append(df)

	base_df = base_df.applymap(str)

    # Clean data where date is undefined
	base_df = base_df[base_df.date != '(other)'] 
    #format date
	base_df['date'] = pd.to_datetime(base_df['date'], format='%Y%m%d') 
	
	# Powershell output
	print(base_df.head())

	# csv output
	base_df.to_csv('FILENAME.csv') #change to desired file path / file name



# See https://ga-dev-tools.appspot.com/dimensions-metrics-explorer/ for metric/dimension API naming conventions 
traffic_columns = [
	'date', #dimension
	'transactions', # metric
	'sessions' #metric
	] 


# JBL - EMEA - All Brands
main('189866410') #GA View Id
