import re
from playwright.sync_api import Playwright, sync_playwright, expect
from dotenv import load_dotenv
from datetime import datetime
import time
import paho.mqtt.client as mqtt
import os
import json


load_dotenv()
def run(playwright: Playwright) -> None:
    usuario = os.getenv('PANAPASS_NUMBER')
    contrasena = os.getenv('PANAPASS_PASSWORD')
    mqtt_user = os.getenv('MQTT_USER')
    mqtt_password = os.getenv('MQTT_PASSWORD')
    mqtt_server = os.getenv('MQTT_BROKER')
    mqtt_port = int(os.getenv('MQTT_PORT'))
    mqtt_topic = os.getenv('MQTT_TOPIC')

    
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.enarecargas.com/maxipista/private#!HomeView")
    page.get_by_role("textbox", name="Nº Panapass").fill(usuario)
    page.get_by_role("textbox", name="Nº Panapass").press("Tab")
    page.get_by_label("Contraseña*").fill(contrasena)
    page.get_by_role("button", name="Identificarse").click()
    page.get_by_text("Saldo de la Cuenta: $").click()
    monto = page.query_selector('//*[@id="sheetSummary"]/div/div/div/div[2]/div[2]/div/div').text_content()
    monto = monto.replace("Saldo de la Cuenta: $", "")
    page.get_by_role("button", name="Desconectar").click()
    #print(monto)

    # ---------------------
    context.close()
    browser.close()

    delay = 1
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, mqtt_user)
    client.username_pw_set(mqtt_user, mqtt_password)
    client.connect(mqtt_server, mqtt_port)
    client.loop_start()
    xpayload = json.dumps({"state": str(monto), "updated_ts": str(int(time.time())), "updated_dt": str(datetime.now()) }, sort_keys=True, default=str)
    client.publish(topic=mqtt_topic, payload=xpayload, qos=0, retain=False)
    
    time.sleep(delay)

with sync_playwright() as playwright:
    run(playwright)
