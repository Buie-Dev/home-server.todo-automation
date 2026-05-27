import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    API_URL = os.getenv("API_URL")
    MQTT_BROKER = os.getenv("MQTT_BROKER")
    MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
    MQTT_USERNAME = os.getenv("MQTT_USERNAME")
    MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
    DEVICE_NAME = os.getenv("DEVICE_NAME", "todo-automation")


config = Config()
