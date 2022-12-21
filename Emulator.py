import pymongo
import datetime as dt
from time import sleep
from pymongo.server_api import ServerApi
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


num = 1
isSensorOn = True

if 'MotionSensor' not in db.list_collection_names():
    db.create_collection("MotionSensor",
                         timeseries={'timeField': 'timestamp', 'metaField': 'sensorId', 'granularity': 'minutes'})


if __name__ == "__main__":
    while isSensorOn:
        Detection = num
        sensorID = 1

        db.motionSensor.insert_one({
            'timestamp': dt.datetime.now(),
            'sensorId': sensorID,
            'Detection': Detection
        })
        sleep(2)