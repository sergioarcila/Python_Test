import requests
import json
import csv
from io import StringIO
import sys
import statistics


def getopts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts


def main(argv):
    if argv:

        opts = getopts(argv)
        if ',' in opts['-kpi_list']:
            kpi_list = opts['-kpi_list'].split(',')
        else:
            kpi_list = [opts['-kpi_list']]

        res = evaluate_kpi(kpi_list, start=opts['-start'], stop=opts['-stop'])
    else:
        res = evaluate_kpi()
    return res


def evaluate_kpi(kpi_list=["Light", "Occupancy"], start="2/2/15 14:37", stop="2/3/15 0:15"):

    # The given API is not showing the data every time. I downloaded it and use as file input
    with open('data.json') as json_file:
        data = json.load(json_file)
        csv_data = StringIO(data['data'])
        reader = csv.DictReader(csv_data)
        data = {header: [] for header in kpi_list}

        # read CSV line by line
        for row in reader:
            if row['date'] > start and row['date'] < stop:  # Check the time condition
                for header, value in row.items():  # if more than one KPIs
                    if header in kpi_list:
                        data[header].append(float(value))
    result = {}

    for kpi, value in data.items():
        if value:
            # percent_change = ((max(value) - min(value)) / abs(min(value)))*100 if min(value)!=0 else max(value)*100
            result[kpi] = {'percent_change': ((max(value) - min(value)) / abs(min(value)))*100 if min(value)!=0 else max(value)*100,
                           'lowest': min(value),
                           'highest': max(value),
                           'last_val': value[len(value) - 1],
                           'first_val': value[0],
                           'average': sum(value) / len(value),
                           'median_val': statistics.median(value)}
        else:
            result[kpi] = 'Data Not Available'

    print(result)
    return result

if __name__ == "__main__":
    res = main(sys.argv[1:])
