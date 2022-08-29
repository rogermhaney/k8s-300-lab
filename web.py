#! /usr/bin/env python3

import os
from flask import Flask, render_template, request, redirect
import json
import requests
from datetime import datetime
import socket

# Global variables used for web server template files
APP_NAME = ""
APP_ACCESS = "" # http or https (use http)
APP_URL = "" # DNS name or IP Address of web server service
APP_PORT = "" # TCP port to access of web server service
BASE_URL = "" # Calculated from the above for web service
# Global variables used for api/db server template files
API_ACCESS = "" # http or https (use http)
API_URL = "" # DNS name or IP Address of api/db server service
API_PORT = "" # TCP port to access of api/db server service
API_BASE_URL = "" # Calculated from the above for api/db service

app = Flask(__name__)
app.debug = True

def get_environment():
    # Get environment variables and build the base url
    global APP_NAME, APP_ACCESS, APP_URL, APP_PORT, BASE_URL, API_ACCESS, API_URL, API_PORT, API_BASE_URL
    try:
        APP_NAME = os.environ['APP_NAME']
        APP_ACCESS = os.environ['APP_ACCESS']
        APP_URL = os.environ['APP_URL']
        APP_PORT = os.environ['APP_PORT']
        BASE_URL = f"{APP_ACCESS}://{APP_URL}:{APP_PORT}"
        API_ACCESS = os.environ['API_ACCESS']
        API_URL = os.environ['API_URL']
        API_PORT = os.environ['API_PORT']
        API_BASE_URL = f"{API_ACCESS}://{API_URL}:{API_PORT}"
    except:
        print (f"All environment variables must be set in the container. (APP_NAME, APP_ACCESS, APP_URL, APP_PORT, API_ACCESS, API_URL, API_PORT)")
        exit()

@app.route('/', methods=['GET'])
def root():
    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(socket.gethostname())
    time_stamp = datetime.now()
    app_name = APP_NAME
    return render_template('/index.html', hostname=hostname, ip_addr=ip_addr, time_stamp=time_stamp, app_name=app_name, base_url = BASE_URL)

@app.route('/index', methods=['GET'])
def index():
    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(socket.gethostname())
    time_stamp = datetime.now()
    app_name = APP_NAME
    return render_template('/index.html', hostname=hostname, ip_addr=ip_addr, time_stamp=time_stamp, app_name=app_name, base_url = BASE_URL)

@app.route('/entry', methods=['GET', 'POST'])
def entry():
    # clear variables
    c_first_name = ""
    c_last_name = ""
    c_address = ""
    c_city = ""
    c_state = ""
    c_zip = ""
    c_company = ""
    c_email = ""
    c_phone = ""

    # if POST set variables from form and call API endpoint
    if request.method == 'POST':
        c_first_name = request.form['C_FName']
        c_last_name = request.form['C_LName']
        c_address = request.form['C_Addr']
        c_city = request.form['C_City']
        c_state = request.form['C_State']
        c_zip = request.form['C_Zip']
        c_email = request.form['C_Email']
        c_phone = request.form['C_Phone']
        c_company = request.form['C_Company']
        c_record = {
            'c_first_name': c_first_name,
            'c_last_name': c_last_name,
            'c_address': c_address,
            'c_city': c_city,
            'c_state': c_state,
            'c_zip': c_zip,
            'c_company': c_company,
            'c_email': c_email,
            'c_phone': c_phone
        }
        # Request call to API endpoint to add record to contestant database
        api_url = API_BASE_URL + "/api/v1/entry"
        c_response_post = requests.post(api_url, json=c_record)
        print(c_response_post)

    return render_template('/entry.html', base_url = BASE_URL)

@app.route('/dbview', methods=['GET'])
def dbview():
    return render_template('/dbview.html', base_url = BASE_URL)

@app.route('/admin', methods=['GET'])
def admin():
    # Just displays page
    return render_template('/admin.html', base_url = BASE_URL)    


@app.route('/10_records', methods=['GET'])
def ten_records():
    api_url = API_BASE_URL + "/api/v1/view10"
    t_prizes_response_get = requests.get(api_url)
    return_data = t_prizes_response_get.content.decode('utf-8')
    return_data = json.loads(return_data)
    return render_template('/10_records.html', data=(return_data), base_url = BASE_URL)

@app.route('/25_records', methods=['GET'])
def twentyfive_records():
    api_url = API_BASE_URL + "/api/v1/view25"
    t_prizes_response_get = requests.get(api_url)
    return_data = t_prizes_response_get.content.decode('utf-8')
    return_data = json.loads(return_data)
    return render_template('/25_records.html', data=(return_data), base_url = BASE_URL)

@app.route('/50_records', methods=['GET'])
def fifty_records():
    api_url = API_BASE_URL + "/api/v1/view50"
    t_prizes_response_get = requests.get(api_url)
    return_data = t_prizes_response_get.content.decode('utf-8')
    return_data = json.loads(return_data)
    return render_template('/50_records.html', data=(return_data), base_url = BASE_URL)


@app.route('/dump_tables', methods=['GET'])
def dump_tables():
    api_url = BASE_URL + "/api/v1/admin/drop"
    t_dump_response_get = requests.get(api_url)
    return_data = t_dump_response_get.status_code
    return render_template('/dump_tables.html', data=return_data, base_url = BASE_URL)



if __name__ == '__main__':
    get_environment()
    app.run(host='0.0.0.0', port=APP_PORT)
