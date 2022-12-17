from marshmallow import Schema, fields, validate

class MotionSensorSchema(Schema):
    Detection = fields.Integer(required=True)

