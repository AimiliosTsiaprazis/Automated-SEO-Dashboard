import pandas
import matplotlib.pyplot as plt
from datetime import datetime

# Excel Datei die aus seo_dashboard.py generiert wurde unter 'excel_file' einfügen
excel_file = ''
# Excel Datei für die ganze SEO Historie bis jetzt unter 'excel_file_history' einfügen
excel_file_history = ''

dataframe = pandas.read_excel(excel_file)
dataframe_history = pandas.read_excel(excel_file_history)

# Daten bereinigen und fertigstellen für die excel_file
dataframe.columns = dataframe.columns.str.strip()
dataframe['Keyword'] = dataframe['Keyword'].str.strip()
dataframe['Seite'] = dataframe['Seite'].str.strip()
dataframe['Datum'] = pandas.to_datetime(dataframe['Datum'])

for col in ['Klicks', 'Impressionen', 'Position']:
    dataframe[col] = pandas.to_numeric(dataframe[col], errors='coerce').fillna(0)
    
dataframe = dataframe.sort_values(['Keyword', 'Datum'])

# Daten bereinigen und fertigstellen fuer die excel_file_history
dataframe_history.columns = dataframe_history.columns.str.strip()
dataframe_history['Keyword'] = dataframe_history['Keyword'].str.strip()
dataframe_history['Seite'] = dataframe_history['Seite'].str.strip()
dataframe_history['Datum'] = pandas.to_datetime(dataframe_history['Datum'])
dataframe_history['Monat'] = dataframe_history['Datum'].dt.to_period('M')

for col in ['Klicks', 'Impressionen', 'Position']:
    dataframe_history[col] = pandas.to_numeric(dataframe_history[col], errors='coerce').fillna(0)
    
dataframe_history = dataframe_history.sort_values(['Keyword', 'Datum'])

# Datum für heute erstellen
today = datetime.today().strftime('%d-%m-%Y')

# Diagramm für die SEO Historie (Entwicklung von Klicks & Impressionen)

# Sum von alle Keywords für jeden Tag durch die Historie
daily_totals_history = (
    dataframe_history.groupby('Datum')[['Klicks', 'Impressionen', 'Position']]
    .agg({
        'Klicks': 'sum',
        'Impressionen': 'sum',
        'Position': 'mean'
    })
    .reset_index()
)

plt.figure(figsize=(12, 9))
plt.plot(daily_totals_history['Datum'], daily_totals_history['Klicks'], marker='o', label='Klicks', color='#4295d1')
plt.title('SEO Dashboard History - Gesamtentwicklung (Klicks)')
plt.xlabel('Datum')
plt.ylabel('Klicks')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig(f'SEO_Dashboard_history_gesamtentwicklung_klicks_{today}.webp')
plt.savefig(f'SEO_Dashboard_history_gesamtentwicklung_klicks_{today}.pdf')
plt.show()

# Sum von alle Keywords für jeden Monat durch die Historie
monthly_totals_history = (
    dataframe_history.groupby('Monat')[['Klicks', 'Impressionen', 'Position']]
    .agg({
        'Klicks': 'sum',
        'Impressionen': 'sum',
        'Position': 'mean'
    })
    .reset_index()
)

# Summe von Klicks für jeden einzelnen Monat
monthly_totals_history['Monat_str'] = monthly_totals_history['Monat'].astype(str)

plt.figure(figsize=(12, 9))
plt.plot(monthly_totals_history['Monat_str'], monthly_totals_history['Klicks'], marker='o', label='Klicks', color='#4295d1')
plt.title('SEO Dashboard History - Gesamtentwicklung (Klicks)')
plt.xlabel('Datum')
plt.ylabel('Klicks')
plt.xticks(rotation=45)
plt.text(0.5, -0.2, f'Summe von Klicks: {monthly_totals_history["Klicks"].sum()}', ha='center', transform=plt.gca().transAxes, fontsize=13, color='black')
plt.grid(True)
for i, row in monthly_totals_history.iterrows():
    plt.text(row['Monat_str'], row['Klicks'] + 5,
             f"{row['Klicks']}", 
             ha='center', fontsize=12, color='#4295d1')
plt.tight_layout()
plt.savefig(f'SEO_Dashboard_history_gesamtentwicklung_klicks_{today}.webp')
plt.savefig(f'SEO_Dashboard_history_gesamtentwicklung_klicks_{today}.pdf')
plt.show()

# Kuchendiagramm mit Summe von Impressionen & Klicks und als Prozentansicht
labels = ['Impressionen', 'Klicks']
sizes = [dataframe['Impressionen'].sum(), dataframe['Klicks'].sum()]
plt.figure(figsize=(12, 8))
plt.title(f'SEO Dashboard - Kuchendiagramm - {today}')
plt.figtext(0.5, 0.08, f'Summe von Impressionen: {dataframe["Impressionen"].sum()}', ha='center')
plt.figtext(0.5, 0.04, f'Summe von Klicks: {dataframe["Klicks"].sum()}', ha='center')
plt.pie(sizes, labels=labels, autopct='%1.2f%%', colors=['#4295d1', '#a9db4c'], textprops={'fontsize': 14, 'color': 'black'})
plt.savefig(f'SEO_Dashboard_Kuchendiagramm_{today}.webp')
plt.savefig(f'SEO_Dashboard_Kuchendiagramm_{today}.pdf')
plt.show()

# Top 10 Keywords für jedes Wert (Klicks, Impressionen, Positionen)

top_keywords_by_clicks = (
    dataframe.groupby('Keyword')['Klicks']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .index
)

top_keywords_by_impressions = (
    dataframe.groupby('Keyword')['Impressionen']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .index
)

top_keywords_by_positions = (
    dataframe.groupby('Keyword')['Position']
    .mean()
    .sort_values(ascending=True)
    .head(10)
    .index
)

dataframe_top_clicks = dataframe[dataframe['Keyword'].isin(top_keywords_by_clicks)]
dataframe_top_impressions = dataframe[dataframe['Keyword'].isin(top_keywords_by_impressions)]
dataframe_top_positions = dataframe[dataframe['Keyword'].isin(top_keywords_by_positions)]

## Top_10 Keywords mit Klicks (Diagramm 1)

plt.figure(figsize=(12, 8))
for keyword in top_keywords_by_clicks:
    subset = dataframe_top_clicks[dataframe_top_clicks['Keyword'] == keyword]
    plt.plot(subset['Datum'], subset['Klicks'], marker='o', label=keyword)
plt.title('SEO Dashboard - Klicks (Top 10 Keywords)')
plt.xlabel('Datum')
plt.ylabel('Klicks')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
plt.tight_layout()
plt.savefig(f'SEO_Dashboard_Top10_Klicks_{today}.webp')
plt.savefig(f'SEO_Dashboard_Top10_Klicks_{today}.pdf')
plt.show()

## Top_10 Keywords mit Impressionen (Diagramm 2)

plt.figure(figsize=(12, 8))
for keyword in top_keywords_by_impressions:
    subset = dataframe_top_impressions[dataframe_top_impressions['Keyword'] == keyword]
    plt.plot(subset['Datum'], subset['Impressionen'], marker='o', label=keyword)
plt.title('SEO Dashboard - Impressionen (Top 10 Keywords)')
plt.xlabel('Datum')
plt.ylabel('Impressionen')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
plt.tight_layout()
plt.savefig(f'SEO_Dashboard_Top10_Impressionen_{today}.webp')
plt.savefig(f'SEO_Dashboard_Top10_Impressionen_{today}.pdf')
plt.show()

## Top_10 Keywords mit Position (Diagramm 3)

plt.figure(figsize=(12, 8))
for keyword in top_keywords_by_positions:
    subset = dataframe_top_positions[dataframe_top_positions['Keyword'] == keyword]
    plt.plot(subset['Datum'], subset['Position'], marker='o', label=keyword)
plt.title('SEO Dashboard - Positionen (Top 10 Keywords, beste Positionen)')
plt.xlabel('Datum')
plt.ylabel('Durchschnittliche Position')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
plt.tight_layout()
plt.savefig(f'SEO_Dashboard_Top10_Positionen_{today}.webp')
plt.savefig(f'SEO_Dashboard_Top10_Positionen_{today}.pdf')
plt.show()

# Sum von alle Keywords für jedes Tag
daily_totals = (
    dataframe.groupby('Datum')[['Klicks', 'Impressionen', 'Position']]
    .agg({
        'Klicks': 'sum',
        'Impressionen': 'sum',
        'Position': 'mean'
    })
    .reset_index()
)

## Sum - Gesamtentwicklung von Klicks
plt.figure(figsize=(12, 8))
plt.plot(daily_totals['Datum'], daily_totals['Klicks'], label='Gesamt Klicks', marker='o', color='#4295d1')
plt.title('SEO Dashboard - Gesamtentwicklung (Klicks)')
plt.xlabel('Datum')
plt.ylabel('Werte')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(f'SEO_Dashboard_gesamtentwicklung_klicks_{today}.webp')
plt.savefig(f'SEO_Dashboard_gesamtentwicklung_klicks_{today}.pdf')
plt.show()

## Sum - Gesamtentwicklung von Impressionen
plt.figure(figsize=(12, 8))
plt.plot(daily_totals['Datum'], daily_totals['Impressionen'], label='Gesamt Impressionen', marker='x', color='#4295d1')
plt.title('SEO Dashboard - Gesamtentwicklung (Impressionen)')
plt.xlabel('Datum')
plt.ylabel('Werte')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(f'SEO_Dashboard_gesamtentwicklung_impressionen_{today}.webp')
plt.savefig(f'SEO_Dashboard_gesamtentwicklung_impressionen_{today}.pdf')
plt.show()


## Durchschnittliche Position
plt.figure(figsize=(12, 8))
plt.plot(daily_totals['Datum'], daily_totals['Position'], color='#4295d1', marker='s')
plt.title('SEO Dashboard - Durchschnittliche Position (Gesamt)')
plt.xlabel('Datum')
plt.ylabel('Durchschnittliche Position')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig(f'SEO_Dashboard_durchschnittliche_Position_{today}.webp')
plt.savefig(f'SEO_Dashboard_durchschnittliche_Position_{today}.pdf')
plt.show()

# 3 Diagramme mit alle Keywords aus der Excel Datei (unübersichtlich)

# Diagramm 1: Datum mit Klicks (alle Keywords)

plt.figure(figsize=(12,10))

keywords = dataframe['Keyword'].unique()
for keyword in keywords:
    keyword_data = dataframe[dataframe['Keyword'] == keyword]
    plt.plot(keyword_data['Datum'], keyword_data['Klicks'], marker='o', label=keyword)
    
plt.title('SEO Dashboard - Klicks pro Keyword')
plt.xlabel('Datum')
plt.ylabel('Klicks')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
plt.tight_layout()
#plt.savefig(f'SEO_Dashboard_Klicks_{today}.webp')
#plt.savefig(f'SEO_Dashboard_Klicks_{today}.pdf')
plt.show()

# Diagramm 2: Datum mit Impressionen (alle Keywords)

plt.figure(figsize=(12,10))

keywords = dataframe['Keyword'].unique()
for keyword in keywords:
    keyword_data = dataframe[dataframe['Keyword'] == keyword]
    plt.plot(keyword_data['Datum'], keyword_data['Impressionen'], marker='o', label=keyword)

plt.title('SEO Dashboard - Impressionen pro Keyword')
plt.xlabel('Datum')
plt.ylabel('Impressionen')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
plt.tight_layout()
#plt.savefig(f'SEO_Dashboard_Impressionen_{today}.webp')
#plt.savefig(f'SEO_Dashboard_Impressionen_{today}.pdf')
plt.show()

# Diagramm 3: Datum mit Positionen (alle Keywords)

plt.figure(figsize=(12,10))

keywords = dataframe['Keyword'].unique()
for keyword in keywords:
    keyword_data = dataframe[dataframe['Keyword'] == keyword]
    plt.plot(keyword_data['Datum'], keyword_data['Position'], marker='o', label=keyword)

plt.title('SEO Dashboard - Positionen pro Keyword')
plt.xlabel('Datum')
plt.ylabel('Positionen')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
plt.tight_layout()
#plt.savefig(f'SEO_Dashboard_Positionen_{today}.webp')
#plt.savefig(f'SEO_Dashboard_Positionen_{today}.pdf')
plt.show()