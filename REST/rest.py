#!/usr/bin/env python3

from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
from influxdb import InfluxDBClient
import json

dbUser = 'root'
dbPass = 'root'
dbName = 'detectorCounts'
client = InfluxDBClient('localhost', 8086, dbUser, dbPass, dbName)

def queryDatabase(client):
    data = client.query('SELECT count(count)/60 FROM Counts WHERE time > now() - 1h')
    return(data)

app = Flask(__name__)
api = Api(app)

class countsPerMinute(Resource):
    def get(self):
        result = queryDatabase(client)
        data = result.raw["series"][0]["values"][0][1]
        return data, 200
    pass
    
api.add_resource(countsPerMinute, '/cpm')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)

