# https://mntolia.com/mqtt-python-with-paho-mqtt-client/
import time
import paho.mqtt.client as mqtt
import json, math
import random
import string
import logging
import os.path


# create logger
logger = logging.getLogger("mqtt-log")
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


def read_mqtt_config():
    # local_config = False
    local_config = "config/mqtt_local.json"
    # local_config = "config/mqtt_hive.json"

    load_config = "config/mqtt.json"
    if os.path.isfile(local_config):
        load_config = local_config
    f = open(load_config, "r")
    d = f.read()
    f.close()
    return json.loads(d)


# the callback function
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True  # set connected flag
        print(f"Connected OK Returned code={rc}")

        topicAll = f"{mqtt_root_topic}/#"
        print("Subscribing to topic: ", topicAll)
        client.subscribe(topicAll)

    else:
        print(f"Bad connection Returned code={rc}")


def on_disconnect(client, userdata, rc):
    print(f"Disconnected From Broker code ={rc}")


def on_message(client, userdata, message):
    print(message.payload.decode())
    print(message.topic)


def on_publish(client, userdata, mid):
    print("mid:{}".format(mid))


config = read_mqtt_config()
mqtt_host = str(config["mqtt_host"])
mqtt_port = int(config["mqtt_port"])
mqtt_use_tls = bool(int(config["mqtt_use_tls"]))
mqtt_clientid_prefix = str(config["mqtt_clientid_prefix"])
mqtt_username = config.get("mqtt_username")
mqtt_password = config.get("mqtt_password")
mqtt_root_topic = str(config["mqtt_root_topic"])
mqtt_transport = "websockets" if bool(int(config.get("mqtt_use_ws", 0))) else "tcp"

client_unique_ident = "".join(
    random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(3)
)
mqtt_clientid = mqtt_clientid_prefix + client_unique_ident
print("client id >", mqtt_clientid)

# create MQTT Client object
client = mqtt.Client(mqtt_clientid, transport=mqtt_transport)
client.connected_flag = False

# Assigning the object attribute to the Callback Function
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.on_publish = on_publish

if mqtt_use_tls:
    client.tls_set()

if mqtt_username:
    print("using username >", mqtt_username)
    client.username_pw_set(username=mqtt_username, password=mqtt_password)

client.enable_logger(logger=logger)
# Connect
print("connecting to >", mqtt_transport, mqtt_host, mqtt_port)
client.connect(mqtt_host, mqtt_port)


client.loop_start()  # start the loop

while not client.connected_flag:  # wait in loop
    time.sleep(1)


print("Publishing message to topic: ", mqtt_root_topic)

client.publish(
    mqtt_root_topic, f"Hello I'm {mqtt_clientid}"
)  # topic, message (value) to publish
time.sleep(1)

# print("message from url test >")
# # urlMess = "https://octopusengine.org/api/mess.json"
# urlMess = "http://octopusengine.org/api/mess.json"
# mess = "octopus test"
# oldmess = mess


# def getMess():
#     global mess, oldmess
#     try:
#         response = httpx.get(urlMess)
#         url_json = json.loads(response.text)
#         print(str(url_json))
#         mess = url_json.get("message")
#         print(mess)
#     except:
#         print("Err.loadCloudConfig() - connect? json exist?")


# mqtt_scroll_topic = mqtt_root_topic + "/" + id_scroll + "/8x8mtx/scroll"
# print("> scroll test: ", mqtt_scroll_topic)
# client.publish(mqtt_scroll_topic, "eee-python")  # topic, message (value) to publish
# time.sleep(5)

# mqtt_keypad_topic = mqtt_root_topic + "/" + id_keypad + "/wsled/rainbow"
# print("> rainbow test: ", mqtt_keypad_topic)
# client.publish(mqtt_keypad_topic, "")  # topic, message (value) to publish
# time.sleep(3)

# print("> message scroll test: ", mqtt_scroll_topic)
# getMess()
# client.publish(mqtt_scroll_topic, mess)
# time.sleep(1)

# print("client.loop_forever() >")
# client.loop_forever()

print("> main loop ")
client.loop_forever()  # start the loop

# loo = 0
# while True:
#     getMess()
#     # client.publish(mqtt_scroll_topic, mess)
#     time.sleep(2)
#     loo = loo + 1
#     print("loop > " + str(loo))
