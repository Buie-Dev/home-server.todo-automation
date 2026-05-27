import json
import logging
import time

import paho.mqtt.client as mqtt

from config import config

logger = logging.getLogger(__name__)

TOPIC_SUB_HEALTH_CHECK_REQUEST = "healthcheck/request"
TOPIC_PUB_HEALTH_CHECK_RESPONSE = "healthcheck/response"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to MQTT broker")
        client.subscribe(TOPIC_SUB_HEALTH_CHECK_REQUEST)
    else:
        logger.error("MQTT connection failed with code %s", rc)


def on_message(client, userdata, msg):
    try:
        if msg.topic == TOPIC_SUB_HEALTH_CHECK_REQUEST:
            payload = json.dumps({"device": config.DEVICE_NAME})
            client.publish(TOPIC_PUB_HEALTH_CHECK_RESPONSE, payload)
            logger.info("Healthcheck response sent")
    except Exception as e:
        logger.error("Error handling MQTT message: %s", e)


def run_mqtt():
    client = mqtt.Client()
    client.username_pw_set(config.MQTT_USERNAME, config.MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    while True:
        try:
            logger.info("Connecting to MQTT broker %s:%s...", config.MQTT_BROKER, config.MQTT_PORT)
            client.connect(config.MQTT_BROKER, config.MQTT_PORT, 60)
            break
        except Exception as e:
            logger.error("MQTT connect failed: %s — retrying in 5s", e)
            time.sleep(5)
    client.loop_start()
    return client
