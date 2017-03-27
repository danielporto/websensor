#!/bin/python
import sensors
from flask import Flask, jsonify

app = Flask(__name__)

def topology_core_id():
    cpu_core_id = {'cpu0': "/sys/devices/system/cpu/cpu0/topology/core_id",
                     'cpu1': "/sys/devices/system/cpu/cpu1/topology/core_id",
                     'cpu2': "/sys/devices/system/cpu/cpu2/topology/core_id",
                     'cpu3': "/sys/devices/system/cpu/cpu3/topology/core_id",
                     'cpu4': "/sys/devices/system/cpu/cpu4/topology/core_id",
                     'cpu5': "/sys/devices/system/cpu/cpu5/topology/core_id",
                     'cpu6': "/sys/devices/system/cpu/cpu6/topology/core_id",
                     'cpu7': "/sys/devices/system/cpu/cpu7/topology/core_id"}
    data_dict=dict()
    for e,f in cpu_core_id.iteritems():
        with open(f,'r') as content:
            # print e, f
            data_dict[e]=content.readline().strip()

    return {"topology_core_id":data_dict}

def topology_core_siblings():
    cpu_core_siblings = {'cpu0': "/sys/devices/system/cpu/cpu0/topology/core_siblings_list",
                     'cpu1': "/sys/devices/system/cpu/cpu1/topology/core_siblings_list",
                     'cpu2': "/sys/devices/system/cpu/cpu2/topology/core_siblings_list",
                     'cpu3': "/sys/devices/system/cpu/cpu3/topology/core_siblings_list",
                     'cpu4': "/sys/devices/system/cpu/cpu4/topology/core_siblings_list",
                     'cpu5': "/sys/devices/system/cpu/cpu5/topology/core_siblings_list",
                     'cpu6': "/sys/devices/system/cpu/cpu6/topology/core_siblings_list",
                     'cpu7': "/sys/devices/system/cpu/cpu7/topology/core_siblings_list"}
    data_dict=dict()
    for e,f in cpu_core_siblings.iteritems():
        with open(f,'r') as content:
            # print e, f
            data_dict[e]=content.readline().strip()

    return {"topology_core_siblings":data_dict}


def topology_thread_siblings():
    cpu_thread_siblings = {'cpu0': "/sys/devices/system/cpu/cpu0/topology/thread_siblings_list",
                     'cpu1': "/sys/devices/system/cpu/cpu1/topology/thread_siblings_list",
                     'cpu2': "/sys/devices/system/cpu/cpu2/topology/thread_siblings_list",
                     'cpu3': "/sys/devices/system/cpu/cpu3/topology/thread_siblings_list",
                     'cpu4': "/sys/devices/system/cpu/cpu4/topology/thread_siblings_list",
                     'cpu5': "/sys/devices/system/cpu/cpu5/topology/thread_siblings_list",
                     'cpu6': "/sys/devices/system/cpu/cpu6/topology/thread_siblings_list",
                     'cpu7': "/sys/devices/system/cpu/cpu7/topology/thread_siblings_list"}
    data_dict=dict()
    for e,f in cpu_thread_siblings.iteritems():
        with open(f,'r') as content:
            # print e, f
            data_dict[e]=content.readline().strip()
    return {"topology_thread_siblings":data_dict}

def read_cpufreq():
    cpu_curr_freq = {'cpu0':"/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq",
            'cpu1':"/sys/devices/system/cpu/cpu1/cpufreq/scaling_cur_freq",
            'cpu2':"/sys/devices/system/cpu/cpu2/cpufreq/scaling_cur_freq",
            'cpu3':"/sys/devices/system/cpu/cpu3/cpufreq/scaling_cur_freq",
            'cpu4':"/sys/devices/system/cpu/cpu4/cpufreq/scaling_cur_freq",
            'cpu5':"/sys/devices/system/cpu/cpu5/cpufreq/scaling_cur_freq",
            'cpu6':"/sys/devices/system/cpu/cpu6/cpufreq/scaling_cur_freq",
            'cpu7':"/sys/devices/system/cpu/cpu7/cpufreq/scaling_cur_freq"}
    data_dict=dict()
    for e,f in cpu_curr_freq.iteritems():
        with open(f,'r') as content:
            # print e, f
            data_dict[e]=content.readline().strip()
    return {"cpu": data_dict}




def read_core_thermal_throttle_count():
    cpu_thermal_throttle_count = {'cpu0':"/sys/devices/system/cpu/cpu0/thermal_throttle/core_throttle_count",
            'cpu1':"/sys/devices/system/cpu/cpu1/thermal_throttle/core_throttle_count",
            'cpu2':"/sys/devices/system/cpu/cpu2/thermal_throttle/core_throttle_count",
            'cpu3':"/sys/devices/system/cpu/cpu3/thermal_throttle/core_throttle_count",
            'cpu4':"/sys/devices/system/cpu/cpu4/thermal_throttle/core_throttle_count",
            'cpu5':"/sys/devices/system/cpu/cpu5/thermal_throttle/core_throttle_count",
            'cpu6':"/sys/devices/system/cpu/cpu6/thermal_throttle/core_throttle_count",
            'cpu7':"/sys/devices/system/cpu/cpu7/thermal_throttle/core_throttle_count"}
    data_dict=dict()
    for e,f in cpu_thermal_throttle_count.iteritems():
        with open(f,'r') as content:
            # print e, f
            data_dict[e]=content.readline().strip()
    return {"read_core_thermal_throttle_count": data_dict}

def read_pkg_thermal_throttle_count():
    pkg_thermal_throttle_count = {'cpu0':"/sys/devices/system/cpu/cpu0/thermal_throttle/package_throttle_count",
            'cpu1':"/sys/devices/system/cpu/cpu1/thermal_throttle/package_throttle_count",
            'cpu2':"/sys/devices/system/cpu/cpu2/thermal_throttle/package_throttle_count",
            'cpu3':"/sys/devices/system/cpu/cpu3/thermal_throttle/package_throttle_count",
            'cpu4':"/sys/devices/system/cpu/cpu4/thermal_throttle/package_throttle_count",
            'cpu5':"/sys/devices/system/cpu/cpu5/thermal_throttle/package_throttle_count",
            'cpu6':"/sys/devices/system/cpu/cpu6/thermal_throttle/package_throttle_count",
            'cpu7':"/sys/devices/system/cpu/cpu7/thermal_throttle/package_throttle_count"}
    data_dict=dict()
    for e,f in pkg_thermal_throttle_count.iteritems():
        with open(f,'r') as content:
            # print e, f
            data_dict[e]=content.readline().strip()
    return {"read_pkg_thermal_throttle_count":data_dict}





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


topology_info = list()
topology_info.append(topology_core_id())
topology_info.append(topology_core_siblings())
topology_info.append(topology_thread_siblings())

@app.route('/sensors', methods=['GET'])
def get_sensordata():
    sensor = read_sensors()
    sensor.append(read_cpufreq())
    sensor.append(read_core_thermal_throttle_count())
    sensor.append(read_pkg_thermal_throttle_count())
    sensor.append(topology_info)
    return jsonify(sensor)


# def index():
# 	return "Hello World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    # topology_core_siblings()
    # topology_core_id()
    # topology_thread_siblings()
    #print(read_cpufreq())
    # read_core_thermal_throttle_count()
    # read_pkg_thermal_throttle_count()
    #print(read_sensors())
    # l = read_sensors()
    # l.append(read_cpufreq())
    # print l