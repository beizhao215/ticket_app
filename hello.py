from flask import Flask, render_template, request, jsonify, g
import happybase
import geohash
import mzgeohash
from datetime import datetime
from time import strftime

app = Flask(__name__, template_folder=".", static_url_path='/static')

@app.route("/")
def mapview():
    return render_template('templates/layout.html')

@app.route("/_add_numbers")
# def connect_db():
#     connection = happybase.Connection('107.22.78.179')
#     # table = connection.table('ticket')
#     return connection
#
# def get_db():
#     connection = getattr(g, '_database', None)
#     if connection is None:
#         g._database = connect_db()
#         connection = connect_db()
#     return connection

def add_numbers():
    lat = request.args.get('a', 0, type=float)
    lon = request.args.get('b', 0, type=float)
    ghash = geohash.encode(float(lat), float(lon), precision=9)

    # connection = get_db()
    connection = happybase.Connection('54.165.137.212')
    table = connection.table('ticket')
    precision_9 = ghash  ## 2 meters
    precision_8 = ghash[:-1]  ## 20 meters
    precision_7 = ghash[:-2]  ## 76 meters
    precision_6 = ghash[:-3]  ## 610 meters

    precision_9_neighbors = [precision_9]
    precision_9_neighbors_dict = mzgeohash.neighbors(precision_9)
    for key in precision_9_neighbors_dict:
        precision_9_neighbors.append(precision_9_neighbors_dict[key])

    precision_8_neighbors = [precision_8]
    precision_8_neighbors_dict = mzgeohash.neighbors(precision_8)
    for key in precision_8_neighbors_dict:
        precision_8_neighbors.append(precision_8_neighbors_dict[key])

    precision_7_neighbors = [precision_7]
    precision_7_neighbors_dict = mzgeohash.neighbors(precision_7)
    for key in precision_7_neighbors_dict:
        precision_7_neighbors.append(precision_7_neighbors_dict[key])

    # precision_6_neighbors = [precision_6]
    # precision_6_neighbors_dict = mzgeohash.neighbors(precision_6)
    # for key in precision_6_neighbors_dict:
    #     precision_6_neighbors.append(precision_6_neighbors_dict[key])

    counter9 = counter8 = counter7 = counter6 = 0
    counter9_time1h = counter8_time1h = counter7_time1h = counter6_time1h = 0
    counter9_time2h = counter8_time2h = counter7_time2h = counter6_time2h = 0
    counter9_time3h = counter8_time3h = counter7_time3h = counter6_time3h = 0

    current_time = strftime("%H%M")
    current_time_object = datetime.strptime(current_time, '%H%M')
    for each in precision_9_neighbors:
        for key,value in table.scan(row_prefix=each[3:]):
            counter9 += 1
            timestring = str(value['infraction:time'])
            while len(timestring) < 4:
                timestring = "0" + timestring
            date_object = datetime.strptime(timestring, '%H%M')
            if date_object > current_time_object:
                diff = (date_object-current_time_object).seconds
            else:
                diff = (current_time_object-date_object).seconds
            if diff < 1800:
                counter9_time1h += 1
                counter9_time2h += 1
                counter9_time3h += 1
            elif 1800 <= diff <= 3600:
                counter9_time2h += 1
                counter9_time3h += 1
            elif 3600 < diff < 5400:
                counter9_time3h += 1

    for each in precision_8_neighbors:
        for key,value in table.scan(row_prefix=each[3:]):
            counter8 += 1
            timestring = str(value['infraction:time'])
            while len(timestring) < 4:
                timestring = "0" + timestring
            date_object = datetime.strptime(timestring, '%H%M')
            if date_object > current_time_object:
                diff = (date_object-current_time_object).seconds
            else:
                diff = (current_time_object-date_object).seconds
            if diff < 1800:
                counter8_time1h += 1
                counter8_time2h += 1
                counter8_time3h += 1
            elif 1800 <= diff <= 3600:
                counter8_time2h += 1
                counter8_time3h += 1
            elif 3600 < diff < 5400:
                counter8_time3h += 1

    for each in precision_7_neighbors:
        for key,value in table.scan(row_prefix=each[3:]):
            counter7 += 1
            timestring = str(value['infraction:time'])
            while len(timestring) < 4:
                timestring = "0" + timestring
            date_object = datetime.strptime(timestring, '%H%M')
            if date_object > current_time_object:
                diff = (date_object-current_time_object).seconds
            else:
                diff = (current_time_object-date_object).seconds
            if diff < 1800:
                counter7_time1h += 1
                counter7_time2h += 1
                counter7_time3h += 1
            elif 1800 <= diff <= 3600:
                counter7_time2h += 1
                counter7_time3h += 1
            elif 3600 < diff < 5400:
                counter7_time3h += 1
    # for each in precision_6_neighbors:
    #     for key,value in table.scan(row_prefix=each[3:]):
    #         counter6 += 1
    #         timestring = str(value['infraction:time'])
    #         while len(timestring) < 4:
    #             timestring = "0" + timestring
    #         date_object = datetime.strptime(timestring, '%H%M')
    #         if date_object > current_time_object:
    #             diff = (date_object-current_time_object).seconds
    #         else:
    #             diff = (current_time_object-date_object).seconds
    #         if diff < 1800:
    #             counter6_time1h += 1
    #             counter6_time2h += 1
    #             counter6_time3h += 1
    #         elif 1800 <= diff <= 3600:
    #             counter6_time2h += 1
    #             counter6_time3h += 1
    #         elif 3600 < diff < 5400:
    #             counter6_time3h += 1
    result_list = [counter7,counter8,counter9, counter7_time1h, counter8_time1h, counter9_time1h,
                   counter7_time2h, counter8_time2h, counter9_time2h, counter7_time3h, counter8_time3h, counter9_time3h]
    return jsonify(result=result_list)

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == "__main__":
    app.run(debug=True)