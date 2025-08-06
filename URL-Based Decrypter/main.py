import requests
import pandas as pd
from bs4 import BeautifulSoup


rowLength = 0
columnHeight = 0
secretMessage = []

# Example URL: https://docs.google.com/document/d/e/2PACX-1vTER-wL5E8YC9pxDx43gk8eIds59GtUUk4nJo_ZWagbnrH0NFvMXIw6VWFLpf5tWTZIT9P9oLIoFJ6A/pub

google_doc_url = input("Provide a Google Doc URL: ")
modified_url = google_doc_url.replace("/edit?usp=sharing", "/export?format=html")

try:
    response = requests.get(modified_url)
    response.raise_for_status()  # Checks that the url is a valid address

    # BeautifulSoup decodes Unicode
    soup = BeautifulSoup(response.content, 'html.parser')

    tables = soup.find_all('table')

    # gets data from every given table within the URL document
    if tables:
        for i, table in enumerate(tables):

            # Data extraction using pandas
            df = pd.read_html(str(table))[0]

            # Iterates through the DataFrame to access each datapoint within a table
            for row_index, row in df.iterrows():
                column = 0
                for cell_value in row.values:

                    if row_index > 0:   # passes header

                        if rowLength <= int(row.values[0]):
                            while rowLength <= int(row.values[0]):  # adds column to message
                                newColumn = []
                                for y in range(columnHeight):
                                    newColumn.append("░")
                                secretMessage.append(newColumn)
                                rowLength += 1

                        if columnHeight <= int(row.values[2]):
                            while columnHeight <= int(row.values[2]):   # adds row to message
                                for x in range(rowLength):
                                    secretMessage[x].append("░")
                                columnHeight += 1

                        secretMessage[int(row.values[0])][int(row.values[2])] = row.values[1]   # assigns Unicode to index

    else:
        print("No tables found in the Google Doc URL.")

except requests.exceptions.RequestException as e:
    print(f"Error fetching the document: {e}")
except Exception as e:
    print(f"Error parsing tables: {e}")


# prints message with 0,0 in the bottem left instead of top right:
for y in range(columnHeight):
    for x in range(rowLength):
        print(secretMessage[x][columnHeight-1-y], end="")
    print()
