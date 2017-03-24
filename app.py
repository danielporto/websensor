#!/bin/python
import sensors
from flask import Flask, jsonify

app = Flask(__name__)

def read_sensors():
    sensors.init()
    sensor_data = list()
    try:
        for chip in sensors.iter_detected_chips():
            #print '%s at %s' % (chip, chip.adapter_name)
            source = '%s at %s'% (chip, chip.adapter_name)
            data_list = list()
            for feature in chip:
             #   print '  %s: %.2f' % (feature.label, feature.get_value())
                data_list.append({feature.label:feature.get_value()})
            sensor_data .append({source:data_list})

    finally:
        sensors.cleanup()

    return sensor_data



@app.route('/sensors', methods=['GET'])
def get_sensordata():
    sensor = read_sensors()
    return jsonify(sensor)


# def index():
# 	return "Hello World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)



