#!/usr/bin/env python3

from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
from influxdb import InfluxDBClient

dbUser = 'root'
dbPass = 'root'
dbName = 'detectorCounts'
client = InfluxDBClient('localhost', 8086, dbUser, dbPass, dbName)

result = client.query('SELECT count(count)/60 FROM Counts WHERE time > now() - 1h')
countsPerMinute = result.get_points()

app = Flask(__name__)
api = Api(app)

class Users(Resource):
    def get(self):
        data = pd.read_csv('users.csv')
        data = data.to_dict()
        return {'data': data}, 200
    pass

class Locations(Resource):
    
    pass

api.add_resource(Users, '/users')
api.add_resource(Locations, '/locations')

if __name__ == '__main__':
    app.run(host="0.0.0.0")

