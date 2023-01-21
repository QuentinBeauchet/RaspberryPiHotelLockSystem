import time
import cv2
import numpy as np
import face_recognition
import requests
import nfc
from nfc.clf import RemoteTarget


def encodeImage(current_image):
    encoding = face_recognition.face_encodings(
        cv2.cvtColor(current_image, cv2.COLOR_BGR2RGB))[0].tobytes()

    return "".join([hex(x)[2:].zfill(2) for x in encoding])


def take_picture():
    cap = cv2.VideoCapture(0)
    _, image, = cap.read()
    cap.release()
    img_resized = image
    return img_resized


def getRFIDIdentifier():
    while (True):
        if CLF is None:
            return input("No RFID detection avalaible, type the RFID manually: ")

        target = CLF.sense(RemoteTarget('106A'), RemoteTarget(
            '106B'), RemoteTarget('212F'))

        if target is not None:
            rfid_tag = nfc.tag.activate(CLF, target)
            identifier = rfid_tag.identifier.hex()
            return identifier

        time.sleep(1)


def cropImage(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = model.detectMultiScale(gray, 1.3, 4)

    img = None
    max_area = 0
    for i, (x, y, w, h) in enumerate(faces):
        area = w*h
        if area > max_area:
            img = image[y:y + h, x:x + w]
            max_area = area

    return img


def insertUser(first_name, last_name, rfid, picture):
    img_encoded = encodeImage(picture)

    response = requests.post(url=f'{API_URL}/user/add',
                             json={"first name": first_name, "last name": last_name, "rfid": rfid, "picture": img_encoded})

    if response.status_code == 200:
        print("User Inserted into the DB")
    else:
        print("The server is not avalaible")


def addUser():
    first_name = input("First name: ")
    last_name = input("Last name: ")
    print("Please scan your card: ")
    rfid = getRFIDIdentifier()
    picture = None
    while True:
        print("Don't move a picture will be taken...")
        for i in range(3, 0, -1):
            print(i, "...")
            time.sleep(1)
        print("Cheese !!!")
        picture = cropImage(take_picture())
        if picture is not None:
            break

        print("No face detected")
        ans = input("Do you want to retry ? (y/n)")
        if ans == "n":
            break

    print("Sending user informations to the Database")
    insertUser(first_name, last_name, rfid, picture)


def main():
    print("What do you want to do ?")
    print("1. Add user")
    print("2. Edit user")
    print("3. Delete user")
    print("4. Exit")

    cmd = input("-> ")

    if cmd == "1":
        addUser()
    else:
        print("Command not implemented yet")


if __name__ == '__main__':
    # Init RFID
    CLF = None
    try:
        CLF = nfc.ContactlessFrontend()
        assert CLF.open('usb:04e6:5591') is True
    except:
        CLF = None
        print("USB RFID detector not found")

    # Init face detection
    model = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    API_URL = "http://localhost:3000/api"

    main()
