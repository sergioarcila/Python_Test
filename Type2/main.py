import argparse
import requests
import csv
import statistics
from io import StringIO
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument("--kpi_list", help="KPI List", nargs="*")
parser.add_argument("--start", help="start date from the database")
parser.add_argument("--stop", help="stop date from the database")
args = parser.parse_args()

print("Start date", args.start)
print("Stop date", args.start)
print("KPI List ", args.kpi_list)

def call_api(start_date, stop_date, kpi_list):
    r = requests.get('http://lameapi-env.ptqft8mdpd.us-east-2.elasticbeanstalk.com/data')
    result_json = r.json()
    # reading CSV string
    f = StringIO(result_json['data'])
    reader = csv.reader(f)
    # make dict_list
    return_dict = []
    start_date_object = datetime.strptime(start_date, '%m/%d/%y')
    stop_date_object = datetime.strptime(stop_date + " 23:59:59", '%m/%d/%y %H:%M:%S')
    i = 0
    for row in reader:
        if i != 0:
            csv_date = datetime.strptime(row[0], '%m/%d/%y %H:%M')
            if csv_date >= start_date_object and csv_date <= stop_date_object:
                return_dict.append({
                    "date": row[0],
                    "temperature": float(row[1]),
                    "humidity": float(row[2]),
                    "light": float(row[3]),
                    "co2": float(row[4]),
                    "humidityRatio": float(row[5]),
                    "occupancy": float(row[6])
                })
        i += 1
    return return_dict
    

def KPI_derive(start_date, stop_date, kpi_list):
    data_list = call_api(start_date, stop_date, kpi_list)
    # if there is no response from the API
    if len(data_list) == 0:
        return {"ok": False}

    # convert data_list to list of list of each kpis it will be helpful for calculation
    list_list = []
    i = 0
    for kpi in kpi_list:
        buffer_list = []
        for dt in data_list:
            buffer_list.append(dt[kpi])
        list_list.append(buffer_list)
        i += 1

    # calculation
    return_dict = []
    
    i = 0 
    for kpi in kpi_list:
        return_dict.append({
            'KPI': kpi,
            'lowest': min(list_list[i]),
            'highest': max(list_list[i]),
            'average': sum(list_list[i]) / len(list_list[i]),
            'median': statistics.median(list_list[i]),
            'first_value': list_list[i][0],
            'last_value': list_list[i][-1]
        })
        i += 1
       

    return return_dict

print(KPI_derive(args.start, args.stop, args.kpi_list))
        