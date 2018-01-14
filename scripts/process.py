#!/usr/bin/python

import urllib.request
import os
import datetime
import csv
import xlrd


def retrieve():
    '''Downloades xls data to archive directory
    
    '''
    source_budget = 'https://www.whitehouse.gov/sites/whitehouse.gov/files/omb/budget/fy2018/hist05z2.xls'
    source_discretionary_bugdet= 'https://www.whitehouse.gov/sites/whitehouse.gov/files/omb/budget/fy2018/hist05z4.xls'
    source_gdp_usa = 'http://datahub.io/core/gdp/r/gdp.csv'
    
    budget_dest = os.path.join('archive', 'budget.xls')
    urllib.request.urlretrieve(source_budget, budget_dest)
    discretionary_bugdet_dest = os.path.join('archive', 'discretionary-bugdet.xls')
    urllib.request.urlretrieve(source_discretionary_bugdet, discretionary_bugdet_dest)
    
    return budget_dest, discretionary_bugdet_dest

def csv_from_excel():
    '''

    '''
    wb = xlrd.open_workbook('archive/budget.xls')
    sh = wb.sheet_by_index(0)
    budget = open('archive/budget.csv', 'w')
    wr = csv.writer(budget, quoting=csv.QUOTE_ALL)

    for rownum in range(2, sh.nrows):
        wr.writerow(sh.row_values(rownum))
    budget.close()

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

retrieve()
csv_from_excel()
process_budget()
process_budget_education()
process()