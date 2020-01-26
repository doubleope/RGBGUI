import json
import sys
import os

from flask_influxdb import InfluxDB
from flask import Flask, render_template, jsonify, request, flash
from werkzeug.utils import secure_filename, redirect

import RGB_L1
import RGB_L2
import RGB_L3
import RGB_Telemetry
import RGB_Checker

UPLOAD_FOLDER = '/home/ope/PyEMD/Documents/Projects/RGB-GUI/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
influx_db = InfluxDB(app=app)


def get_info(client):
    db_data = client.query('SELECT * FROM clusters')
    data_points = list(db_data.get_points())
    return data_points


@app.route('/upload_file')
def upload_file():
    client = influx_db.connection
    client.switch_database('cluster_info_db')

    with open('uploads/JSON_test_file') as json_file:
        file = json.load(json_file)
    client.write_points([
        {
            "fields": {
                'cluster_name': file["cluster_name"],
                'cluster_type': file["cluster_type"],
                'ip': file["ip"],
                'port': file["port"],
                'mac_address': file["mac_address"]
            },
            "measurement": "clusters"
        }
    ])
    return jsonify(get_info(client))


@app.route('/post_cluster_info')
def post_cluster_info():
    client = influx_db.connection
    client.switch_database('cluster_info_db')

    client.write_points([
        {
            "fields": {
                'cluster_name': request.args.get('cluster_name'),
                'cluster_type': request.args.get('cluster_type'),
                'ip': request.args.get('ip'),
                'port': request.args.get('port'),
                'mac_address': request.args.get('mac_address')
            },
            "measurement": "clusters"
        }
    ])

    return jsonify(get_info(client))


@app.route('/show_data_center_info', methods=['GET'])
def show_data_center_info():
    client = influx_db.connection
    client.switch_database('cluster_info_db')
    return jsonify(get_info(client))


@app.route('/result1')
def result1():
    client = influx_db.connection
    client.switch_database('cluster_info_db')
    res1 = RGB_L1.runGreenTest(get_info(client))
    return jsonify(res1)


@app.route('/result2')
def result2():
    client = influx_db.connection
    client.switch_database('cluster_info_db')
    res2 = RGB_L2.runGreenTest(get_info(client))
    return jsonify(res2)


@app.route('/result3')
def result3():
    client = influx_db.connection
    client.switch_database('cluster_info_db')
    res3 = RGB_L3.runGreenTest(get_info(client))
    return jsonify(res3)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/level1', methods=['GET', 'POST'])
def level1():
    if request.method == 'POST':
        file = request.files['file']
        client = influx_db.connection
        client.switch_database('cluster_info_db')

        file = json.load(file)
        for i in file:
            client.write_points([
                {
                    "fields": {
                        'cluster_name': i['cluster_name'],
                        'cluster_type': i['cluster_type'],
                        'ip': i['ip'],
                        'port': i['port'],
                        'mac_address': i['mac_address']
                    },
                    "measurement": "clusters"
                }
            ])
    level_type = "Level One"
    return render_template('measurement-results-page.html', level_type=level_type)


@app.route('/level2')
def level2():
    if request.method == 'POST':
        file = request.files['file']
        client = influx_db.connection
        client.switch_database('cluster_info_db')

        file = json.load(file)
        for i in file:
            client.write_points([
                {
                    "fields": {
                        'cluster_name': i['cluster_name'],
                        'cluster_type': i['cluster_type'],
                        'ip': i['ip'],
                        'port': i['port'],
                        'mac_address': i['mac_address']
                    },
                    "measurement": "clusters"
                }
            ])
    level_type = "Level Two"
    return render_template('measurement-results-page.html', level_type=level_type)


@app.route('/level3')
def level3():
    if request.method == 'POST':
        file = request.files['file']
        client = influx_db.connection
        client.switch_database('cluster_info_db')

        file = json.load(file)
        for i in file:
            client.write_points([
                {
                    "fields": {
                        'cluster_name': i['cluster_name'],
                        'cluster_type': i['cluster_type'],
                        'ip': i['ip'],
                        'port': i['port'],
                        'mac_address': i['mac_address']
                    },
                    "measurement": "clusters"
                }
            ])
    level_type = "Level Three"
    return render_template('measurement-results-page.html', level_type=level_type)


if __name__ == '__main__':
    app.run()
