#!/bin/python
from flask import Flask, jsonify
import argparse
import time
app = Flask(__name__)



def last_log(file_path):
    global header
    global nelements

    logline=list()
    with open(file_path,'r') as fobj: #only care about the most recent value
        for content in fobj:
            #print content[:3]
            if content[:3] == '>> ':
                logline = content[3:]
                #print logline

    if not logline:
        return

    if not header:
        header = data_header(file_path)
        nelements=len(header)-1 #remove the last element which is empty

    values = [v.strip() for v in logline.split(';')]
    #print values
    data = list()
    for index in range(nelements):
        v = {"SensorName": header[index], "SensorValue": values[index]}
        #print v
        data.append(v)

    return data

def data_header(file_path):
    content = open(file_path).readlines()
    for line in content:
        if line[:3] == '>>!':
            header = [h.strip() for h in line[3:].split(';')]
            return header


def read_data(log):
    global nelements
    llog = last_log(log)
    service_timestamp = ""
    v = [{'SensorName': 'Timestamp', 'SensorValue': ''},
         {'SensorName': 'Throughput (op/sec)', 'SensorValue': ''},
         {'SensorName': 'Max Throughput', 'SensorValue': ''},
         {'SensorName': 'Total latency(us)', 'SensorValue': ''},
         {'SensorName': 'Err Total latency', 'SensorValue': ''},
         {'SensorName': 'Consensus latency (us)', 'SensorValue': ''},
         {'SensorName': 'Err Consensus latency', 'SensorValue': ''},
         {'SensorName': 'Pre-consensus latency (us)', 'SensorValue': ''},
         {'SensorName': 'Err Pre-consensus latency', 'SensorValue': ''},
         {'SensorName': 'Pos-consensus latency (us)', 'SensorValue': ''},
         {'SensorName': 'Err Pos-consensus latency', 'SensorValue': ''},
         {'SensorName': 'Propose latency (us)', 'SensorValue': ''},
         {'SensorName': 'Err Propose latency', 'SensorValue': ''},
         {'SensorName': 'Write latency (us)', 'SensorValue': ''},
         {'SensorName': 'Err Write latency', 'SensorValue': ''},
         {'SensorName': 'Accept latency (us)', 'SensorValue': ''},
         {'SensorName': 'Err Accept latency', 'SensorValue': ''}]

    #no sensor info
    if not llog:
        return v

    #timely sensor info
    curr_timestamp = time.time() #time in seconds to compare with the java time
    for s in llog:
        if s['SensorName']=='Timestamp':
            service_timestamp = str(int(s['SensorValue'])/1000.0)
            s['SensorValue']=service_timestamp
            break
    #print llog
    #print service_timestamp
    #print curr_timestamp

    # old sensor info
    if curr_timestamp - service_timestamp > 1.5:
        v[0] ={'SensorName': 'Timestamp', 'SensorValue': service_timestamp}
        return v

    return llog


@app.route('/sensors', methods=['GET'])
def get_sensordata():
    data = list()
    data.extend(read_data(args['log']))
    return jsonify(data)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default="", help="port for the sevice", required=True)
    parser.add_argument("--log", default="", help="name of log to read from", required=True)


    args = vars(parser.parse_args())
    header = ""
    nelements= ""
    app.run(host='0.0.0.0', port=int(args['port']), debug=True)

