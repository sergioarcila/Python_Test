import urllib.request, json, csv, argparse
from datetime import datetime

def get_content_data():
    content_data = ''
    while len(content_data) < 10: # not a valid data
        try:
            content_data = json.loads(urllib.request.urlopen("http://lameapi-env.ptqft8mdpd.us-east-2.elasticbeanstalk.com/data").read())['data']
        except:
            pass
    return content_data

def get_result(kpi_list, start, stop):
    content_data = get_content_data()
    records = content_data.splitlines()[1:] # skip header
    real_data = []
    start_date = datetime.strptime(start, '%m/%d/%y')
    stop_date = datetime.strptime(stop, '%m/%d/%y')
    result_data = {}
    for kpi_item in kpi_list:
        result_data[kpi_item] = {
            'percent_change': 0,
            'last_value': None,
            'first_value': None,
            'lowest': None,
            'highest': None,
            'mode': None,
            'average': None,
            'median': None,
        }
    for record in records:
        date, temperature, humidity, light, co2, humidity_ratio, occupancy = record.split(',')
        date = datetime.strptime(date, '%m/%d/%y %H:%M')
        if not (start_date <= date <= stop_date):
            continue
        record_data = {
            'date': date,
            'temperature': float(temperature),
            'humidity': float(humidity),
            'light': float(light),
            'co2': float(co2),
            'humidity_ratio': float(humidity_ratio),
            'occupancy': int(occupancy),
        }
        print('bingo')
        real_data.append(record_data)
        for kpi_item in kpi_list:
            if result_data[kpi_item]['first_value'] is None:
                result_data[kpi_item]['first_value'] = record_data[kpi_item]

            result_data[kpi_item]['last_value'] = record_data[kpi_item]

            if result_data[kpi_item]['lowest'] is None or result_data[kpi_item]['lowest'] > record_data[kpi_item]:
                result_data[kpi_item]['lowest'] = record_data[kpi_item]

            if result_data[kpi_item]['highest'] is None or result_data[kpi_item]['highest'] < record_data[kpi_item]:
                result_data[kpi_item]['highest'] = record_data[kpi_item]

    return result_data

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process data.')
    parser.add_argument('--start', dest='start')
    parser.add_argument('--stop', dest='stop')
    parser.add_argument('--kpi_list', dest='kpi_list')
    args = parser.parse_args()
    start = args.start
    stop = args.stop
    kpi_list = args.kpi_list
    if not start or not stop or not kpi_list:
        parser.print_help()
        exit()
    kpi_list = kpi_list.split(',')
    results = get_result(kpi_list=kpi_list, start=start, stop=stop)
    print('result = ', results)
    # results = get_result(kpi_list=["light", "occupancy"], start="2/2/15 14:37", stop="2/3/15 0:15")

