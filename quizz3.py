import requests
import json
import sqlite3

api_key = "75FeHbC7BWqlMGCYXc0GyIzxf08RcAQG4pE7bq0c"
url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"

response = requests.get(url)

print(f"Status Code: {response.status_code}")

print(f"Headers: {response.headers}")

data = response.json()
print(f"JSON Data: {json.dumps(data, indent=4)}")

with open('apod_data.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

title = data.get('title', 'No Title')
date = data.get('date', 'No Date')
explanation = data.get('explanation', 'No Explanation')
url = data.get('url', 'No URL')

print(f"Title: {title}")
print(f"Date: {date}")
print(f"Explanation: {explanation}")
print(f"URL: {url}")

nasa_base = "nasa.sqlt"
connection = sqlite3.connect(nasa_base)
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS apod (
    date TEXT PRIMARY KEY,
    title TEXT,
    explanation TEXT,
    url TEXT
)
''')

print(f"Data to be inserted: date={date}, title={title}, explanation={explanation}, url={url}")

try:

    cursor.execute('''
    INSERT OR REPLACE INTO apod (date, title, explanation, url)
    VALUES (?, ?, ?, ?)
    ''', (date, title, explanation, url))


    connection.commit()


    cursor.execute('SELECT * FROM apod')


    rows = cursor.fetchall()
    for row in rows:
        print(row)
except sqlite3.ProgrammingError as e:
    print(f"SQLite Programming Error: {e}")

connection.close()
