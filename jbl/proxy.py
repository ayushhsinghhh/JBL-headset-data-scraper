# import csv
#
# # Open the CSV file for reading
# with open('Free_Proxy_List.csv', 'r') as csv_file:
#     # Create a CSV reader object
#     csv_reader = csv.reader(csv_file)
#
#     # Open a text file for writing
#     with open('proxy.txt', 'w') as txt_file:
#         # Iterate over each row in the CSV file
#         for row in csv_reader:
#             # Write the first column of each row to the text filelll
#             txt_file.write(row[0] + '\n')


import requests
from bs4 import BeautifulSoup

# Define a header to send with the request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Send a GET request to the webpage with the defined header
url = "https://hidemyname.io/en/proxy-list/?type=hs#list"
response = requests.get(url, headers=headers)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find all table rows
rows = soup.find_all('tr')[1:]

# Open a text file for writing
with open('proxy.txt', 'w') as txt_file:
    # Extract the first element of each row and write it to the text file
    for row in rows:
        # Get the first cell of the row
        first_cell = row.find('td')
        if first_cell:
            txt_file.write(first_cell.text.strip() + '\n')
