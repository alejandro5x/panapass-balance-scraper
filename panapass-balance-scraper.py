import re
from playwright.sync_api import Playwright, sync_playwright, expect, TimeoutError
from dotenv import load_dotenv
from datetime import datetime
import time
import paho.mqtt.client as mqtt
import os
import json

load_dotenv()
panapass_user = os.getenv('PANAPASS_NUMBER')
panapass_password = os.getenv('PANAPASS_PASSWORD')
mqtt_user = os.getenv('MQTT_USER')
mqtt_password = os.getenv('MQTT_PASSWORD')
mqtt_server = os.getenv('MQTT_BROKER')
mqtt_port = int(os.getenv('MQTT_PORT'))
mqtt_topic = os.getenv('MQTT_TOPIC')
mqtt_error_topic = os.getenv('MQTT_ERROR_TOPIC')  # Separate Topic for errors

def run(playwright: Playwright) -> None:

    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.enarecargas.com/maxipista/private#!HomeView")

    try:
        page.get_by_role("textbox", name="Nº Panapass").fill(panapass_user)
        page.get_by_role("textbox", name="Nº Panapass").press("Tab")
        page.get_by_label("Contraseña*").fill(panapass_password)
        page.get_by_role("button", name="Identificarse").click()
        page.get_by_text("Saldo de la Cuenta: $").click()

        # Getting balance
        balance_element = page.query_selector('//*[@id="sheetSummary"]/div/div/div/div[2]/div[2]/div/div')
        if balance_element is None:
            raise ValueError("Element for balance not found.")
        
        balance = balance_element.text_content()
        balance = balance.replace("Saldo de la Cuenta: $", "")

        send_mqtt_data(mqtt_server, mqtt_port, mqtt_user, mqtt_password, mqtt_topic, balance)
        send_mqtt_error(mqtt_server, mqtt_port, mqtt_user, mqtt_password, mqtt_error_topic, "")
    except (TimeoutError, ValueError) as e:
        error_message = f"Error getting balance: {str(e)}"
        send_mqtt_error(mqtt_server, mqtt_port, mqtt_user, mqtt_password, mqtt_error_topic, error_message)
        balance = "Error"
    finally:
        page.get_by_role("button", name="Desconectar").click()
        context.close()
        browser.close()


def send_mqtt_data(server, port, user, password, topic, balance):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, mqtt_user)
    client.username_pw_set(user, password)
    client.connect(server, port)
    client.loop_start()
    
    xpayload = json.dumps({
        "state": str(balance),
        "updated_ts": str(int(time.time())),
        "updated_dt": str(datetime.now())
    }, sort_keys=True, default=str)
    
    client.publish(topic=topic, payload=xpayload, qos=0, retain=False)
    time.sleep(1)
    client.loop_stop()

def send_mqtt_error(server, port, user, password, topic, error_message):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, mqtt_user)
    client.username_pw_set(user, password)
    client.connect(server, port)
    client.loop_start()
    
    xpayload = json.dumps({
        "error": error_message,
        "updated_ts": str(int(time.time())),
        "updated_dt": str(datetime.now())
    }, sort_keys=True, default=str)
    
    client.publish(topic=topic, payload=xpayload, qos=0, retain=False)
    time.sleep(1)
    client.loop_stop()

with sync_playwright() as playwright:
    run(playwright)
