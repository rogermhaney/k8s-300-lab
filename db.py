import os
from flask import Flask, render_template, request, redirect, jsonify
import json
import redis
import requests
from datetime import datetime
from operator import itemgetter

app = Flask(__name__)
app.debug = True

'''     
API Call Table (@route points):
    /api/v1/entry - Method: POST pushes user, address & points information into redis db in { json body }
    /api/v1/view10 - Method: GET returns table of last 10 customers in DB
    /api/v1/view25 - Method: GET returns table of last 25 customers in DB
    /api/v1/view50 - Method: GET returns table of last 50 customers in DB
    /api/v1/admin/{ task } - Method(s): GET, POST, DELETE - list and modify db tables
                    /drop - Method: GET? drops existing tables and creates new tables using v1 schema
'''
# Global variables used for api/db server template files
API_PORT = "" # TCP port to access of api/db server service

def get_environment():
    # Get environment variables and build the base url
    global API_PORT
    try:
        API_PORT = os.environ['API_PORT']
    except:
        print (f"API_PORT environment variable must be set in the Container")
        exit()

## Render staic info page
@app.route('/', methods=['GET'])
def root():

    return render_template('/apisvc.html')

@app.route('/apisvc', methods=['GET'])
def index():

    return render_template('/apisvc.html')

@app.route('/api/v1/entry', methods=['POST'])
def c_entry_v1():
    # Method: POST pushes user, address & points information into redis db in { json body } for v1
    if request.method == 'POST':
        if not request.json:
            return jsonify({'result': False})
        c_dict = request.json
        c_first_name = c_dict.get("c_first_name")
        c_last_name = c_dict.get("c_last_name")
        c_address = c_dict.get("c_address")
        c_city = c_dict.get("c_city")
        c_state = c_dict.get("c_state")
        c_zip = c_dict.get("c_zip")
        c_email = c_dict.get("c_email")
        c_phone = c_dict.get("c_phone")
        c_company = c_dict.get("c_company")

        # connect to redis db - table 'contestants' - error wrap!
        rdb = redis.Redis(host='localhost', port=6379, db=0)

        time_obj = datetime.now()
        time_str = time_obj.strftime("%Y%m%d%H%M%S%f")
        hash_name = "id:" + time_str
        c_record = {
            'First_Name': c_first_name,
            'Last_Name': c_last_name,
            'Address': c_address,
            'City': c_city,
            'State': c_state,
            'Zip': c_zip,
            'Email': c_email,
            'Phone': c_phone,
            'Company': c_company
        }
        rdb.hmset(hash_name, c_record)
        rdb.lpush('c_key_list', hash_name)
        rdb.close()
        return jsonify({'result': True})
    else:   
        return render_template('/error_db.html')

@app.route('/api/v1/admin/drop', methods=['GET'])
def admin_drop():
    # Method: GET drops existing tables from each db
    if request.method == 'GET':
        rdb = redis.Redis(host='localhost', port=6379, db=0)
        rdb.flushall()
        rdb.close()
        rdb = redis.Redis(host='localhost', port=6379, db=1)
        rdb.flushall()
        rdb.close()
        rdb = redis.Redis(host='localhost', port=6379, db=2)
        rdb.flushall()
        rdb.close()
        return jsonify({'result': True})
    else: 
        return render_template('/error_db.html')

@app.route('/api/v1/view10', methods=['GET'])
def view10():
    # Method: GET returns list of entries in customer table
    # if request.method == 'GET':
    rdb = redis.Redis(host='localhost', port=6379, db=0, charset='utf-8', decode_responses=True)
    list_length = rdb.llen('c_key_list')
    if list_length > 10:
        list_length = 10
    xportnames = []
    temp = ''
    for i in range(list_length):
        x = i-1
        hash_name = rdb.lindex('c_key_list', x)
        temp = rdb.hgetall(hash_name)
        xportnames.append(temp)
    rdb.close()
    # Return API endpoint to pull last 10 customers
    return jsonify(xportnames)


@app.route('/api/v1/view25', methods=['GET'])
def view25():
    # Method: GET returns list of entries in customer table
    # if request.method == 'GET':
    rdb = redis.Redis(host='localhost', port=6379, db=0, charset='utf-8', decode_responses=True)
    list_length = rdb.llen('c_key_list')
    if list_length > 25:
        list_length = 25
    xportnames = []
    temp = ''
    for i in range(list_length):
        x = i-1
        hash_name = rdb.lindex('c_key_list', x)
        temp = rdb.hgetall(hash_name)
        xportnames.append(temp)
    rdb.close()
    # Return API endpoint to pull last 25 customers
    return jsonify(xportnames)


@app.route('/api/v1/view50', methods=['GET'])
def view50():
    # Method: GET returns list of entries in customer table
    # if request.method == 'GET':
    rdb = redis.Redis(host='localhost', port=6379, db=0, charset='utf-8', decode_responses=True)
    list_length = rdb.llen('c_key_list')
    if list_length > 50:
        list_length = 50
    xportnames = []
    temp = ''
    for i in range(list_length):
        x = i-1
        hash_name = rdb.lindex('c_key_list', x)
        temp = rdb.hgetall(hash_name)
        xportnames.append(temp)
    rdb.close()
    # Return API endpoint to pull last 50 customers
    return jsonify(xportnames)



if __name__ == '__main__':
    get_environment()
    app.run(host='0.0.0.0', port=API_PORT)
