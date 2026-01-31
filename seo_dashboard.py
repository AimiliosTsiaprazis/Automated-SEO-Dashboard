import pandas
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime

# Google API credentials
Service_Account_File = ''
Scopes = ['https://www.googleapis.com/auth/webmasters.readonly']

# Verbindung zur API
credentials = service_account.Credentials.from_service_account_file(
    Service_Account_File, scopes=Scopes)
service = build('searchconsole', 'v1', credentials=credentials)

# Website URL für die SEO Analyse
Site_URL = ''

# Abfrage der letzten Woche -> je nachdem kann man es anpassen
start_date = '2025-11-03'
end_date = '2025-11-07'

# Abfrage der gesamten SEO Historie -> Anfang Juni 2025 -> Ende immer aktuell halten
start_date_history = '2025-06-01'
end_date_history = '2025-11-07'

request = {
    'startDate': start_date,
    'endDate': end_date,
    'dimensions': ['query', 'page', 'date'],
    'rowLimit': 5000
}

request_history = {
    'startDate': start_date_history,
    'endDate': end_date_history,
    'dimensions': ['query', 'page', 'date'],
    'rowLimit': 5000
}

response = service.searchanalytics().query(siteUrl=Site_URL, body=request).execute()
response_history = service.searchanalytics().query(siteUrl=Site_URL, body=request_history).execute()

# Daten holen und in DataFrame umwandeln
data = []
for row in response.get('rows', []):
    data.append({
        'Keyword': row['keys'][0],
        'Seite': row['keys'][1],
        'Datum': row['keys'][2],
        'Klicks': row.get('clicks',0),
        'Impressionen': row.get('impressions',0),
        'Position': round(row.get('position',0), 1)
    })
    
# Daten für die gesamte Historie
data_history = []
for row in response_history.get('rows', []):
    data_history.append({
        'Keyword': row['keys'][0],
        'Seite': row['keys'][1],
        'Datum': row['keys'][2],
        'Klicks': row.get('clicks',0),
        'Impressionen': row.get('impressions',0),
        'Position': round(row.get('position',0), 1)
    })

dataframe = pandas.DataFrame(data)
dataframe['Datum'] = pandas.to_datetime(dataframe['Datum'])
dataframe = dataframe.sort_values(['Keyword', 'Datum'])

dataframe_history = pandas.DataFrame(data_history)
dataframe_history['Datum'] = pandas.to_datetime(dataframe_history['Datum'])
dataframe_history = dataframe_history.sort_values(['Keyword', 'Datum'])

# Speichern der Daten in Excel-Dateien
today = datetime.today().strftime('%Y-%m-%d')
dataframe.to_excel(f'seo_dashboard_{today}.xlsx', index=False)
dataframe_history.to_excel(f'seo_dashboard_history_{today}.xlsx', index=False)
print("Excel Dateien wurden erfolgreich erstellt.")