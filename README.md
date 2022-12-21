# MotionSensorFinal
## Project Introduction
    It is a new product that can be used in different sitations.
    It can be used in different situations. It can help to improve security, 
    protection, and privacy in users' lives. This is possible since Bip Tech 
    uses a monitor sensor, a light, and a buzzer. It is also possible to see 
    the data afterwards because it is stored in a database.

## Target Audience
    Our product has different targets since security is important for everyone.
    For example, a museum can use this product to prevent a thief from happening,
    a seller can make their store more secure, and people can feel more protected
    in their houses. This product can also help sellesr to know how many people were
    present at a certain time in their store.

## Hardware
![img_4.png](img_4.png)

## MongoDB Schema Design
![img_5.png](img_5.png)

## API endpoints
#### GET: /motion

This GET request allows us to see and select all the values that will be in the database and
that will be captured by the motion sensor in the different locations.

---------

#### GET: /sensors/<<int:sensorId>>/motion

This GET request allows us to see and select the data for a specific sensor Id. The sensor Id
represents the location of the motion sensor. It will first match and then group by sensorId
and will finally sum the number of detections for that specific sensor.

-----------

#### POST: /sensors/<<int:sensorId>>/motion
This POST request allows us to create and insert new values for a specific sensorId.