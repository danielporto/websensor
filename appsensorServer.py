#!/bin/python
import sensors
from flask import Flask, jsonify
import argparse

app = Flask(__name__)


def read_data():

    while True:
        with open(args['pipe'],'rw') as f
            l = f.readline()
            if l[:3]=='>>!': #find the header
                keys = l.split(';')
                l2= f.readline()
                values = l2.split(';')
                data = list()
                for i in range(1,len(2)):
                    # print e, f
                    v = {"SensorName": keys[i], "SensorValue": values[i].strip()}
                    data.append(v)
                return data

    return data


@app.route('/sensors', methods=['GET'])
def get_sensordata():
    data = list()
    data.extend(read_data())
    return jsonify(data)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default="", help="port for the sevice", required=True)
    parser.add_argument("--pip", default="", help="name of pipe to read from", required=True)


    args = vars(parser.parse_args())
    app.run(host='0.0.0.0', port=args['port'], debug=True)

