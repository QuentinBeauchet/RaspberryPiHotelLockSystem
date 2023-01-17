import time
import serial
import cv2
import numpy as np
import face_recognition
import requests
import nfc
import sys
from nfc.clf import RemoteTarget

ser = serial.Serial("/dev/rfcomm0", 9600)
clf = nfc.ContactlessFrontend()
assert clf.open('usb:04e6:5591') is True

API_URL = "http://localhost:3000/api"


def encode_image(current_image):
    encoded_image = face_recognition.face_encodings(
        cv2.cvtColor(current_image, cv2.COLOR_BGR2RGB))[0]
    return encoded_image


def recognition(encoded_image):
    for i in range(5):
        cap = cv2.VideoCapture(0)
        success, image, = cap.read()
        cap.release()
        img_resized = cv2.resize(image, (0, 0), None, 0.25, 0.25)
        img_resized = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)

        encode_face = face_recognition.face_encodings(img_resized)
        if len(encode_face) != 0:
            matches = face_recognition.compare_faces(
                encoded_image, encode_face, 0.5)
            face_dis = face_recognition.face_distance(
                encoded_image, encode_face)
            match_index = np.argmin(face_dis)

            if matches[match_index]:
                return True
    return False


def getRFIDIdentifier():
    target = clf.sense(RemoteTarget('106A'), RemoteTarget(
        '106B'), RemoteTarget('212F'))
    identifier = None
    if target is not None:
        rfid_tag = nfc.tag.activate(clf, target)
        identifier = rfid_tag.identifier.hex()

    time.sleep(1)
    return identifier


def fetch_user(tag, DOOR_ID):
    response = requests.get(f'{API_URL}/user?rfid={tag}&door_id={DOOR_ID}')
    if (response.status_code != 200):
        return None

    user = response.json()

    return {"rfid": user["rfid"],
            "name": f'{user["first name"]}_{user["last name"]}',
            "picture": cv2.imdecode(np.fromiter(user["picture"]["data"], np.uint8), cv2.IMREAD_COLOR)}


def check_door_status(DOOR_ID):
    response = requests.get(f'{API_URL}/status?door_id={DOOR_ID}')
    if (response.status_code != 200):
        return None

    status = response.json()
    return status["status"].lower() == "true"


def open_door():
    ser.write(b"1")                 # Send Signal to open the door
    while ser.inWaiting() == 0:
        pass                        # Wait 5 seconds for the door to close 
    data = ser.readline().decode()
    if(data[:-1] == "0"):
        print("Door Locked")


def run_door_multifactor_authentication(DOOR_ID):
    while True:
        if check_door_status(DOOR_ID):
            print("Admin Opening the Door.")
            open_door()
        else:
            print("Waiting for RFID contact")
            tag = getRFIDIdentifier()
            # tag = input("Enter Your Badge: ")

            if tag is None:
                time.sleep(1)
                continue

            if tag.lower() == "exit":
                break

            user = fetch_user(tag, DOOR_ID)

            if user is None:
                print("No Match Found in the database")
            else:
                encodings = encode_image(user["picture"])
                if encodings is not None:
                    matching_image = recognition(encodings)
                    if matching_image:
                        print(user["name"])
                        print("Door Opens")
                        open_door()
                    else:
                        print("No Match Found")


if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print("Missing DOOR_ID: python Multifactor_Authentication.py DOOR_ID")
        sys.exit(1)
        
    DOOR_ID = sys.argv[1]
    run_door_multifactor_authentication(DOOR_ID)
