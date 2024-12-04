#!/usr/bin/python

import os
import csv
import zipfile
import requests
import openpyxl

from bs4 import BeautifulSoup

zip_file_path = 'archive/hist_budget.zip'

def retrieve_zip():
    '''
        Downloades zip data to archive directory
    '''
    origin = 'https://www.whitehouse.gov/omb/budget/historical-tables/'
    response = requests.get(origin)
    soup = BeautifulSoup(response.text, 'html.parser')
    select_href_by_selector = soup.select('#content > article > section > div > div > p:nth-child(4) > a')
    zip_url = select_href_by_selector[0].get('href')
    download = requests.get(zip_url)
    with open(zip_file_path, 'wb') as f:
        f.write(download.content)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # Iterate through the files in the zip
        for file in zip_ref.namelist():
            # Check if the file is 'hist05z2.xlsx' or 'hist05z4.xlsx'
            if file.endswith('hist05z2.xlsx'):
                # Extract and rename to 'budget.xlsx'
                zip_ref.extract(file, 'archive')
                os.rename(os.path.join('archive', file), os.path.join('archive', 'budget.xlsx'))
                print(f'Extracted and renamed: {file} to budget.xlsx')
                
            elif file.endswith('hist05z4.xlsx'):
                # Extract and rename to 'discretionary-budget.xlsx'
                zip_ref.extract(file, 'archive')
                os.rename(os.path.join('archive', file), os.path.join('archive', 'discretionary-budget.xlsx'))
                print(f'Extracted and renamed: {file} to discretionary-budget.xlsx')

    # Remove the ZIP file after extraction and renaming
    os.remove(zip_file_path)

def update_gdp():
    source = 'https://raw.githubusercontent.com/datasets/gdp/refs/heads/main/data/gdp.csv'
    response = requests.get(source)
    with open('archive/gdp.csv', 'w') as f:
        f.write(response.text)

def csv_from_excel():
    '''
        Converts excel file to csv
    '''
    wb = openpyxl.load_workbook('archive/budget.xlsx')
    sh = wb.active  # Get the first sheet

    # Open the CSV file to write
    with open('archive/budget.csv', 'w', newline='') as budget:
        wr = csv.writer(budget, quoting=csv.QUOTE_ALL)
        
        # Loop through rows starting from the third row (index 2)
        for row in sh.iter_rows(min_row=3, values_only=True):
            # Write each row to the CSV file
            wr.writerow(row)

def process_budget():
    # un-pivot the table
    fo = open('archive/budget.csv')
    lines = [ row for row in csv.reader(fo) ]
    headings = lines[0]
    lines = lines[1:]

    outheadings = ['Name','Year', 'Value']
    outlines = []

    for row in lines:
        for idx, year in enumerate(headings[1:]):
            if row[idx+1]:
                value = row[idx+1]
                if year != 'TQ':
                    if "estimate" not in year and ".........." not in value:
                        outlines.append(row[:1] + [int(year), value])
                    else:
                        year = year.replace(' estimate', '')
                        value = value.replace('..........', '')
                        outlines.append(row[:1] + [int(year), value])
    writer = csv.writer(open('data/budget.csv', 'w'))
    writer.writerow(outheadings)
    writer.writerows(outlines)


def process_budget_education():
    # un-pivot the table
    fo = open('archive/budget.csv')
    lines = [ row for row in csv.reader(fo) ]
    headings = lines[0]
    lines = lines[1:]

    outheadings = ['Year', 'Value']
    outlines = []

    for row in lines:
        for idx, year in enumerate(headings[1:]):
            if row[idx+1]:
                value = row[idx+1]
                if row[0] == 'Department of Education' and year !='TQ':
                    outlines.append([str(year), value])
    writer = csv.writer(open('data/budget-education.csv', 'w'))
    writer.writerow(outheadings)
    writer.writerows(outlines)

def process():
    with open('data/budget-education.csv', 'r') as inp1, open('archive/gdp.csv', 'r') as inp2, open('data/data.csv', 'w') as out:
        writer = csv.writer(out)
        reader1 = csv.reader(inp1)
        reader2 = csv.reader(inp2)
        next(reader1, None)  # skip the headers
        reader1_list = list(reader1)
        reader2_list = list(reader2)
        writer.writerow(('YEAR','BUDGET_ON_EDUCATION','GDP','RATIO'))
        for row in reader1_list:
            for row1 in reader2_list:
                if row[0] == row1[2] and row1[1] == 'USA':
                    row.append(round((float(row1[3])/1000000), 2))
                    row.append(round((float(row[1])/float(row[2])), 5) * 100)
                    writer.writerow(row)

def process():
    print('Processing data...')
    
    print('Updating GDP data...')
    update_gdp()
    print('Extracting data...')
    retrieve_zip()
    print('Converting excel to csv...')
    csv_from_excel()
    print('Processing budget data...')
    process_budget()
    print('Processing budget education data...') 
    process_budget_education()
    print('Done!')

if __name__ == '__main__':
    process()