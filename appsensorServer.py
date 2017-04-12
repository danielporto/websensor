#!/bin/python
import sensors
from flask import Flask, jsonify
import argparse

app = Flask(__name__)


def read_data():

    while True:
	print "opening file", args['pipe']
        with open(args['pipe'],'r') as f:
            l = f.readline()
	    print l
	    
	    v =  {"SensorName": 'linha', "SensorValue": l}
	    return v
            if l[:3]=='>>!': #find the header
		print l
		exit(0)
                keys = l.split(';')
                l2= f.readline()
                values = l2.split(';')
                data = list()
                for i in range(1,len(2)):
                    print keys
                    print values
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
    parser.add_argument("--pipe", default="", help="name of pipe to read from", required=True)


    args = vars(parser.parse_args())
    app.run(host='0.0.0.0', port=int(args['port']), debug=True)

