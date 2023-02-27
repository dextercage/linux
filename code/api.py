from flask import Flask, request, jsonify, send_from_directory, render_template, send_file
from flask_mysqldb import MySQL
from randomuser import RandomUser
import redis, json, os, socket
from werkzeug.datastructures import FileStorage

local_ip = socket.gethostbyname(socket.gethostname())

app = Flask(__name__)
app.config['MYSQL_HOST']=local_ip
app.config['MYSQL_PASSWORD']='12344321ab'
app.config['MYSQL_USER']='root'
mysql = MySQL(app)

def insert(a):
    if a==1:
        # uuid, fistname, lastname, description, email, phone, username
        user_list = RandomUser.generate_users(20, {'nat': 'US'})
        conn = mysql.connection.cursor()
        for i in range(20):
            user_data = [i, user_list[i].get_first_name(), user_list[i].get_last_name(), user_list[i].get_full_name(), user_list[i].get_email(), user_list[i].get_cell(), user_list[i].get_username()]
            query = f"INSERT INTO datastore.user VALUES ("
            query += ', '.join('"'+str(user_data[j])+'"' for j in range(len(user_data)))
            query += ")"
            conn.execute(query)
            mysql.connection.commit()
        conn.close()

    if a==2:
        # uuid, name, category, company, release_year, country
        user_list = RandomUser.generate_users(20, {'nat': 'US'})
        conn = mysql.connection.cursor()
        for i in range(20):
            user_data = [i, user_list[i].get_first_name(), user_list[i].get_city(), user_list[i].get_state(), user_list[i].get_dob()[:4], user_list[i].get_nat()]
            query = f"INSERT INTO datastore.application VALUES ("
            query += ', '.join('"'+str(user_data[j])+'"' for j in range(len(user_data)))
            query += ")"
            print(query)
            conn.execute(query)
            mysql.connection.commit()
        conn.close()

    if a==3:
        #redis
        user_list = RandomUser.generate_users(21, {'nat': 'US'})
        # sentinel = redis.StrictRedis(host=local_ip, port=26379)
        # master_ip, master_port = sentinel.sentinel_get_master_addr_by_name('mymaster')
        # redis_connection = redis.Redis(host=master_ip, port=master_port)
        redis_connection = redis.Redis(host=local_ip, port=6379)
        for i in range(1, 21):
            user_data = [f'film:{i}', user_list[i].get_first_name()]
            redis_connection.set(user_data[0], user_data[1])


@app.route('/database/<path:tbl>', methods=['GET', 'POST'])
def database(tbl):
    if request.method == 'GET':
        conn = mysql.connection.cursor()
        query = f'select * from datastore.{tbl}'
        conn.execute(query)
        result = conn.fetchall()
        mysql.connection.commit()
        conn.close()
        return jsonify(result)

    if request.method == 'POST':
        conn = mysql.connection.cursor()
        data = request.json
        for record in data:
            query = f'INSERT INTO datastore.{tbl} VALUES ('
            query += ', '.join('"'+record[i]+'"' for i in range(len(record)))
            query += ')'
            conn.execute(query)
            mysql.connection.commit()
        conn.close()
        return jsonify("tbl has been inserted!")

@app.route('/redis/<path:key>', methods=['GET', 'POST'])
def redisapp(key):
    if request.method == 'GET':
        # sentinel = redis.StrictRedis(host=local_ip, port=26379)
        # master_ip, master_port = sentinel.sentinel_get_master_addr_by_name('mymaster')
        # redis_connection = redis.Redis(host=master_ip, port=master_port)
        redis_connection = redis.Redis(host=local_ip, port=6379)
        return redis_connection.get(key)

    if request.method == 'POST':
        redis_connection = redis.Redis(host=local_ip, port=6379)
        data = request.json
        redis_connection.set(key, data['value'])
        return "key value has been inserted!"


@app.route('/filestorage/<path:file_name>', methods=['GET', 'POST'])
def filestorage(file_name):
    if request.method=='GET':
        file = file_name.split('/')[-1]
        path = f'/mnt/filestorage/{file}'
        return send_file(path)

    if request.method=='POST':
        file = file_name.split('/')[-1]
        path = f'/mnt/filestorage/{file}'
        data = request.files['file']
        data.save(path)
        return jsonify('File has been uploaded')



if __name__=="__main__":
    print("Starting")
    insert(3)
    app.run(host='0.0.0.0', port='80')

