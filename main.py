# connecting to mongodb
import isodate as ISODate
import pymongo as pymongo
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_objectid_converter import ObjectIDConverter
from pymongo.server_api import ServerApi
import datetime as dt
from Schemas import MotionSensorSchema

# loading private connection information from environment variables

# loading private connection information from environment variables
from dotenv import load_dotenv

load_dotenv()
import os

MONGODB_LINK = os.environ.get("MONGODB_LINK")
MONGODB_USER = os.environ.get("MONGODB_USER")
MONGODB_PASS = os.environ.get("MONGODB_PASS")

# connecting to mongodb
client = pymongo.MongoClient(f"mongodb+srv://{MONGODB_USER}:{MONGODB_PASS}@{MONGODB_LINK}/?retryWrites=true&w=majority",
                             server_api=ServerApi('1'))
db = client.MotionDetection
if 'MotionSensor' not in db.list_collection_names():
    db.create_collection("MotionSensor",
                         timeseries={'timeField': 'timestamp', 'metaField': 'sensorId', 'granularity': 'minutes'})

def getTimeStamp():
    return dt.datetime.today().replace(microsecond=0)



app = Flask(__name__)
# adding an objectid type for the URL fields instead of treating it as string
# this is coming from a library we are using instead of building our own custom type
app.url_map.converters['objectid'] = ObjectIDConverter

app.config['DEBUG'] = True

# making our API accessible by any IP
CORS(app)



#############################################################



@app.route("/motion")
def get_all_motions():
    query = db.collection.find()
    ListofMotion = {}

    for x in query:
        ListofMotion = {'motions':x}

    data = list(db.MotionSensor.aggregate([
        {
            '$match': ListofMotion
        }, {
            '$group': {
                '_id': '$sensorId',
                'MotionSensor': {
                    '$push': {
                        'timestamp': '$timestamp',
                        'Detection': '$Detection'
                    }
                }
            }
        }
    ]))
    return data










#######################################################################


@app.route("/sensors/<int:sensorId>/motion", methods = ["GET"])
def get_by_sensorID_motion(sensorId):
    start = request.args.get("start")
    end = request.args.get("end")

    query = {"sensorId": sensorId}
    if start is None and end is not None:
        try:
            end = dt.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
        except Exception as e:
            return {"error": "timestamp not following format %Y-%m-%dT%H:%M:%S"}, 400

        query.update({"timestamp": {"$lte": end}})

    elif end is None and start is not None:
        try:
            start = dt.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
        except Exception as e:
            return {"error": "timestamp not following format %Y-%m-%dT%H:%M:%S"}, 400

        query.update({"timestamp": {"$gte": start}})
    elif start is not None and end is not None:
        try:
            start = dt.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
            end = dt.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")

        except Exception as e:
            return {"error": "timestamp not following format %Y-%m-%dT%H:%M:%S"}, 400

        query.update({"timestamp": {"$gte": start, "$lte": end}})

    data = list(db.MotionSensor.aggregate([
        {
            '$match': query
        }, {
            '$group': {
                '_id': '$sensorId',
                'SumDect': {
                    '$sum': '$Detection'
                },
                'MotionSensor': {
                    '$push': {
                        'sensorID':'$sensorID',
                        'timestamp': '$timestamp',
                        'Detection': '$Detection'
                    }
                }
            }
        }
    ]))

    if data:
        data = data[0]
        if "_id" in data:
            del data["_id"]
            data.update({"sensorId": sensorId})

        for motion in data['MotionSensor']:
            motion["timestamp"] = motion["timestamp"].strftime("%Y-%m-%dT%H:%M:%S")

        return data
    else:
        return {"error": "id not found"}, 404







##########################################################################


@app.route("/sensors/<int:sensorId>/motion", methods=["POST"])
def add_motion_detection(sensorId):
    error = MotionSensorSchema().validate(request.json)
    if error:
        return error, 400

    data = request.json
    data.update({ "sensorId": sensorId,"timestamp": getTimeStamp()})

    db.MotionSensor.insert_one(data)

    data["_id"] = str(data["_id"])
    data["timestamp"] = data["timestamp"].strftime("%Y-%m-%dT%H:%M:%S")
    return data





if __name__ == "__main__":
    app.run(port=5001)