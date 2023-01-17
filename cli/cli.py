import time
import cv2
import numpy as np
import face_recognition
import requests
import nfc
import base64
from nfc.clf import RemoteTarget


def encode_image(current_image):
    encoded_image = face_recognition.face_encodings(
        cv2.cvtColor(current_image, cv2.COLOR_BGR2RGB))[0]
    return encoded_image


def take_picture():
    cap = cv2.VideoCapture(0)
    _, image, = cap.read()
    cap.release()
    img_resized = image
    return img_resized


def recognition(encoded_image):
    for i in range(5):
        img_resized = take_picture()

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
    while (True):
        target = clf.sense(RemoteTarget('106A'), RemoteTarget(
            '106B'), RemoteTarget('212F'))

        if target is not None:
            rfid_tag = nfc.tag.activate(clf, target)
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
    cv2.imwrite("tmp.jpg", picture)

    with open("tmp.jpg", "rb") as img:
        img_encoded = "".join([hex(x)[2:].zfill(2) for x in img.read()])

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
    clf = nfc.ContactlessFrontend()
    assert clf.open("usb:04e6:5591") is True

    # Init face detection
    model = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    API_URL = "http://localhost:3000/api"

    main()
