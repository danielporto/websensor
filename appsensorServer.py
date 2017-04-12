#!/bin/python
from flask import Flask, jsonify
import argparse
import time
app = Flask(__name__)



def last_log(file_path):
    global header
    global nelements

    logline=list()
    with open(file_path,'r') as content: #only care about the most recent value
        if content[:3] == '>> ':
            logline = content[3:]

    if not logline:
        return

    if not header:
        header = data_header(file_path)
        nelements=len(header)

    values = [v.strip() for v in logline.split(';')]
    data = dict()
    for index in range(nelements):
        v = {"SensorName": header[index], "SensorValue": values[index]}
        data.append(v)

    return data

def data_header(file_path):
    content = open(file_path).readlines()
    for line in content:
        if line[:3] == '>>!':
            header = [h.strip() for h in line[3:].split(';')]
            return header


def read_data():
    llog = last_log(args['log'])
    sensor_tm = 0
    for s in last_log():
        if s['SensorName']=='Timestamp':
            sensor_tm = int(s['SensorValue'])
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
    data.extend(read_data())
    return jsonify(data)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default="", help="port for the sevice", required=True)
    parser.add_argument("--log", default="", help="name of log to read from", required=True)


    args = vars(parser.parse_args())

    app.run(host='0.0.0.0', port=int(args['port']), debug=True)

