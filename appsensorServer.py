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
                print logline

    if not logline:
        return

    if not header:
        header = data_header(file_path)
        nelements=len(header)-1 #remove the last element which is empty

    values = [v.strip() for v in logline.split(';')]
    print values
    data = list()
    for index in range(nelements):
        v = {"SensorName": header[index], "SensorValue": values[index]}
        print v
        data.append(v)

    return data

def data_header(file_path):
    content = open(file_path).readlines()
    for line in content:
        if line[:3] == '>>!':
            header = [h.strip() for h in line[3:].split(';')]
            return header


def read_data(log):
    llog = last_log(log)
    sensor_tm = 0
    for s in llog:
        if s['SensorName']=='Timestamp':
            sensor_tm = int(s['SensorValue'])/1000
            break

    log_timestamp = time.time()
    print llog
    print sensor_tm
    print log_timestamp
    #v =  {"SensorName": 'linha', "SensorValue": 'valor'}
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

