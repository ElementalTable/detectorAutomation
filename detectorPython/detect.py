#!/usr/bin/env python3

import RPi.GPIO as gpio
import time
from influxdb import InfluxDBClient
from datetime import datetime, timezone

dbUser = 'root'
dbPass = 'root'
dbName = 'detectorCounts'
startTime = datetime.now(timezone.utc).astimezone()

def setupInfluxDB():
    client = InfluxDBClient('localhost', 8086, dbUser, dbPass, dbName)
    client.create_database('detectorCounts')
    return client

def startListening(client):
    gpio.setmode(gpio.BCM)
    gpio.setup(18, gpio.IN)
    gpio.add_event_detect(18, gpio.RISING, callback = lambda pin: detectorTrip(client))
    while True:
        time.sleep(10)

def detectorTrip(client):
    local_time = datetime.now(timezone.utc).astimezone()
    json_body = [
    {
        "measurement": "Counts",
        "tags": {
            "location": "rm2212",
        },
        "time": local_time.isoformat(),
        "fields": {
            "count": 1,
            "startUpTime": startTime.isoformat()
        }
    }]
    client.write_points(json_body)


startListening(setupInfluxDB())

