import cv2 as cv
import numpy as np
import pytesseract
import yaml
import paho.mqtt.client as paho
import base64
import json


def on_message(client, userdata, msg):
    npimg = np.frombuffer(base64.b64decode(msg.payload), dtype=np.uint8)
    original = cv.imdecode(npimg, cv.IMREAD_GRAYSCALE)

    image = cv.GaussianBlur(original, (3, 3), 0)
    image = cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 3)

    cv.rectangle(image, (242, 40), (249, 50), (255, 255, 255), -1)  # remove the dot. Dot added manually then

    kernel = np.ones((3, 3), np.uint8)
    image = cv.morphologyEx(image, cv.MORPH_CLOSE, kernel)

    custom_config = r'--oem 1 --psm 6 -c tessedit_char_whitelist=0123456789-'
    result = pytesseract.image_to_string(image, lang='lets', config=custom_config)
    result = result.replace(" ", "") # if there is 1 at the end it is incorrectly interpreted via whitespaces

    print(result)

    if result.isnumeric():
        result = float(result) / 10
    else:
        result = 0

    print(result)
    data = {
        'value': result,
        'image': (base64.b64encode(cv.imencode('.jpg', image)[1])).decode('utf-8')
    }

    json_data = json.dumps(data, indent=4, sort_keys=True)
    mqttClient.publish(cfg['mqtt']['out-topic'], json_data)


with open("config/energer.conf", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.SafeLoader)

print('Initializing energer...')
print('Connecting to mqtt broker...')

mqttClient = paho.Client('energer')
mqttClient.on_message = on_message

mqttClient.username_pw_set(cfg['mqtt']['user'], cfg['mqtt']['password'])
mqttClient.connect(cfg['mqtt']['broker'], cfg['mqtt']['port'])
mqttClient.subscribe(cfg['mqtt']['in-topic'])

print("Initialized and waiting for image to process... ")

mqttClient.loop_forever()
print('Done.')
