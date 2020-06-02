import boto3
from pprint import pprint
import pyscreenshot as ImageGrab
import time
import urllib.request
import datetime
import os
import sys
import firebase_admin
from datetime import datetime
from firebase_admin import credentials
from database.firebase_interface import FirebaseInterface

cred = credentials.Certificate('database/credentials.json')
firebase_admin.initialize_app(cred)
interface = FirebaseInterface()


def sendDataToFirebase(num_people):
    docTitle = datetime.today().strftime('%Y-%m-%d')
    currentHour = datetime.today().strftime('%H:%M:%S')
    docData = {currentHour: {"num_people": num_people}}
    interface.addOrUpdateData("kitchen_data", docTitle, docData)


client = boto3.client('rekognition')

count = 0

url = 'http://192.168.15.38:8080/shot.jpg'

while True:
    img_name = './assets/fullscreen' + str(count) + '.jpg'
    urllib.request.urlretrieve(url, img_name)

    with open(img_name, 'rb') as source_image:
        source_bytes = source_image.read()

    response = client.detect_labels(Image={'Bytes': source_bytes})

    resp = response['Labels']

    index = 0
    people = 0

    while index < len(resp):
        if resp[index]['Name'] == 'Person':
            people = resp[index]
        index += 1

    if people == 0:
        print(people)
    else:
        people = str(people).count("BoundingBox")
        print(people)

    sendDataToFirebase(people)

    count += 1
    time.sleep(4)
