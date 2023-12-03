import json
import os
from datetime import datetime
import pytz
import paho.mqtt.client as mqtt
import logging


logging.basicConfig(
    filename='read_airtag.log', 
    encoding='utf-8',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')



def init_mqtt():
    client = mqtt.Client()
    client.connect("192.168.1.5", 1883, 60)
    return client


def send_data(items_data):
    tz = pytz.timezone('Europe/Oslo')
    mqtt_client = init_mqtt()
    mqtt_client.loop_start()
    for item in items_data:
        item_name = item["name"]
        location = item["location"]
        logging.info(f"{item_name}: {location}")
        mqtt_client.publish(f"find-my/item/{item_name}", json.dumps(location))

    mqtt_client.loop_stop()


def main():
    items_file = "/Users/ola/Library/Caches/com.apple.findmy.fmipcore/Items.data"
    with open(items_file, "rb") as f:
        items_data = json.load(f)
    
    previous_items_file = "previous_items.json"
    if not os.path.isfile(previous_items_file):
        print("creating file")
        with open(previous_items_file, "w", encoding="utf-8") as f:
            json.dump(items_data, f, ensure_ascii=False, indent=4)
        send_data(items_data)
        return
        
    with open(previous_items_file, "rb") as f:
        previous_items_data = json.load(f)
    
    if previous_items_data == items_data:
        print("EQUAL")
        return

    print("NOT EQUAL")
    with open(previous_items_file, "w", encoding="utf-8") as f:
        json.dump(items_data, f, ensure_ascii=False, indent=4)

    send_data(items_data)
    





if __name__ == "__main__":
    main()