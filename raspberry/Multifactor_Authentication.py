import time
import serial
import cv2
import numpy as np
import face_recognition
import requests
import nfc
import sys
import re
from nfc.clf import RemoteTarget


def recognition(encoded_image):
    for i in range(5):
        print(f"Taking Picture, try n°{i+1}")
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
    if CLF is None:
        return input("No RFID detection avalaible, type the RFID manually: ")
    target = CLF.sense(RemoteTarget('106A'), RemoteTarget(
        '106B'), RemoteTarget('212F'))
    identifier = None
    if target is not None:
        rfid_tag = nfc.tag.activate(CLF, target)
        identifier = rfid_tag.identifier.hex()

    time.sleep(1)
    return identifier


def fetch_user(tag):
    try:
        response = requests.get(f'{API_URL}/user?rfid={tag}&door_id={DOOR_ID}')
    except requests.exceptions.ConnectionError:
        return None

    if (response.status_code != 200):
        return None

    user = response.json()

    return {"rfid": user["rfid"],
            "name": f'{user["first name"]}_{user["last name"]}',
            "picture": np.frombuffer(bytes(user["picture"]["data"]))}


def check_door_status():
    try:
        response = requests.get(f'{API_URL}/status?door_id={DOOR_ID}')
    except requests.exceptions.ConnectionError:
        return False

    if (response.status_code != 200):
        return False

    status = response.json()

    return status["status"]


def get_admins_tags():
    try:
        response = requests.get(f'{API_URL}/admins')
    except requests.exceptions.ConnectionError:
        return []

    if (response.status_code != 200):
        return []

    admins = response.json()

    return [user["rfid"] for user in admins]


def open_door():
    print("Opens door")
    if ARDUINO_SERIAL is not None:
        ARDUINO_SERIAL.write(b"1")      # Send Signal to open the door
        while ARDUINO_SERIAL.inWaiting() == 0:
            pass                        # Wait 5 seconds for the door to close
        data = ARDUINO_SERIAL.readline().decode()
        if (data[:-1] == "0"):
            print("Door Locked")


def run_door_multifactor_authentication():
    ADMINS = get_admins_tags()
    print("Waiting for RFID contact")
    while True:
        if check_door_status():
            print(
                f'{COLOR["GREEN"]}=> Admin Opening the Door from API{COLOR["RESET"]}')
            open_door()
        else:
            tag = getRFIDIdentifier()

            if tag is None:
                time.sleep(0.5)
                continue

            if tag.lower() == "exit":
                break

            print(f'{COLOR["BLUE"]}RFID: {tag}{COLOR["RESET"]}')

            if tag in ADMINS:
                print(
                    f'{COLOR["GREEN"]}=> Admin Opening the Door manually{COLOR["RESET"]}')
                open_door()
                continue

            user = fetch_user(tag)

            if user is None:
                print(
                    f'{COLOR["RED"]}=> No Match Found in the database{COLOR["RESET"]}')
            else:
                encodings = user["picture"]
                if encodings is not None:
                    matching_image = recognition(encodings)
                    if matching_image:
                        print(
                            f'{COLOR["GREEN"]}=> Detected: {user["name"]}{COLOR["RESET"]}')
                        "Opens door"
                        open_door()
                    else:
                        print(
                            f'{COLOR["RED"]}=> User does not match{COLOR["RESET"]}')
        print("Waiting for RFID contact")


if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print("Missing DOOR_ID: python Multifactor_Authentication.py DOOR_ID")
        sys.exit(1)

    COLOR = {"GREEN": "\033[92m", "RED": "\033[91m",
             "BLUE": "\033[94m", "RESET": "\033[0m"}

    ARDUINO_SERIAL = None
    try:
        # command to run on a separet shell to establish the bluetooth connection:
        # sudo rfcomm connect hci0 98:D3:51:F9:46:0D 1
        ARDUINO_SERIAL = serial.Serial("/dev/rfcomm0", 9600)
    except serial.serialutil.SerialException:
        print("Bluetooth is not connected to serial port")

    CLF = None
    try:
        CLF = nfc.ContactlessFrontend()
        assert CLF.open('usb:04e6:5591') is True
    except:
        CLF = None
        print("USB RFID detector not found")

    DOOR_ID = sys.argv[1]
    API_URL = "http://localhost:3000/api"

    run_door_multifactor_authentication()
