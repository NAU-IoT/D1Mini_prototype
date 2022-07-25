"""
py script setting up bridge between sensor data gathered
from MQTT to InfluxDB instance hosted on RPI4
"""

import re
from typing import NamedTuple
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

# INFLUXDB configs created in influx cli
INFLUXDB_ADDRESS = '192.168.1.10'
INFLUXDB_USER = 'akiel'
INFLUXDB_PASSWORD = 'password'
INFLUXDB_DATABASE = 'climate_indicator'

# MQTT configs (see the arduino file and get_MQTT_data.py)
MQTT_ADDRESS = '192.168.1.10'
MQTT_USER = 'akiel'
MQTT_PASSWORD = 'password'
MQTT_TOPIC = 'home/+/+'
MQTT_REGEX = 'home/([^/]+)/([^/]+)'
#MQTT_CLIENT_ID = 'client_area'

influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)

"""
sensor_data class defining location, measurement, and val
create named tuple for correct datatype
"""
class sensor_data_class(NamedTuple):
    location: str
    measurement: str
    value: float
    
"""
function for when our client connects 
prints result code when connected and listens for our mqtt topic
"""
def on_connect(client, userdata, flags, result_code):
    # The callback for when the client receives a CONNACK response from the server
    print('Connected with result code ' + str(result_code))
    # listen for define mosquitto topic
    client.subscribe(MQTT_TOPIC)

"""
reads variables from topic path struct and identifies vars 
returning them as the a named tuple
"""
def _parse_mqtt_message(topic, payload):
    # create match var = to first match of two vars passed in
    match = re.match(MQTT_REGEX, topic)
    # return named tuple if match 
    if match:
        location = match.group(1)
        measurement = match.group(2)
        if measurement == 'status':
            return None
        return sensor_data_class(location, measurement, float(payload))
    else:
        return None

"""
recieves variables as named tuple and creates json struct
we can later use for visualizing our data too
    - measurement saved directly
    - location stored in tag struct with nested val
    - sensor value saved under field 
    - write json struct to influx instance
"""
def _send_sensor_data_to_influxdb(sensor_data):
    json_body = [
        {
            'measurement': sensor_data.measurement,
            'tags': {
                'location': sensor_data.location
            },
            'fields': {
                'value': sensor_data.value
            }
        }
    ]
    influxdb_client.write_points(json_body)

"""
call this function everytime a topic is published
msg topic and payload are saved to two vars and printed to std out
"""
def on_message(client, userdata, msg):
    # The callback for when a PUBLISH message is received from the server
    print(msg.topic + ' ' + str(msg.payload))
    # set var = to our named tuple vals 
    sensor_data = _parse_mqtt_message(msg.topic, msg.payload.decode('utf-8'))
    # is sensor data is not empty store data in influx
    if sensor_data is not None:
        _send_sensor_data_to_influxdb(sensor_data)

"""
function to initialize influx db 
"""
def _init_influxdb_database():
    # set var = to get list of DBs
    databases = influxdb_client.get_list_database()
    # if the db does not exist it will be created
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        influxdb_client.create_database(INFLUXDB_DATABASE)
    influxdb_client.switch_database(INFLUXDB_DATABASE)

"""
main driver function
"""
def main():
    # intialize DB
    _init_influxdb_database()
    
    # create client object, set credentials, 
    # define what is to be ran on connect and msg
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    # connect to broker with IP and PORT
    mqtt_client.connect(MQTT_ADDRESS, 1883)
    # loop forever
    mqtt_client.loop_forever()

if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()


