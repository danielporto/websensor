#!/bin/python
from flask import Flask, jsonify
import argparse
import pyinotify
import re
import os
app = Flask(__name__)



class EventHandler (pyinotify.ProcessEvent):

    def __init__(self, file_path, *args, **kwargs):
        super(EventHandler, self).__init__(*args, **kwargs)
        self.file_path = file_path
        self._last_position = 0
        logpats = r'I2G\(JV\)'
        self._logpat = re.compile(logpats)

    def process_IN_MODIFY(self, event):
        print "File changed: ", event.pathname
        if self._last_position > os.path.getsize(self.file_path):
            self._last_position = 0
        with open(self.file_path) as f:
            f.seek(self._last_position)
            loglines = f.readlines()
            self._last_position = f.tell()
            groups = (self._logpat.search(line.strip()) for line in loglines)
            for g in groups:
                if g:
                    print g.string



def read_data():
    v =  {"SensorName": 'linha', "SensorValue": 'valor'}



	 #    return v
    #         if l[:3]=='>>!': #find the header
		# print l
		# exit(0)
    #             keys = l.split(';')
    #             l2= f.readline()
    #             values = l2.split(';')
    #             data = list()
    #             for i in range(1,len(2)):
    #                 print keys
    #                 print values
    #                 v = {"SensorName": keys[i], "SensorValue": values[i].strip()}
    #                 data.append(v)
    #             return data
    #
    # return data


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

    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_MODIFY

    handler = EventHandler(args['log'])
    notifier = pyinotify.Notifier(wm, handler)

    wm.add_watch(handler.file_path, mask)
    notifier.loop()

    app.run(host='0.0.0.0', port=int(args['port']), debug=True)

