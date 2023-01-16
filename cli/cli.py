import time
import cv2
import numpy as np
import face_recognition
import requests
import nfc
from nfc.clf import RemoteTarget
import matplotlib.pyplot as plt


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

    if len(faces) != 1:
        return cv2.resize(image, (0, 0), None, 0.25, 0.25)

    (x, y, w, h) = faces[0]
    return image[y:y + h, x:x + w]


def fetch_user(tag):
    response = requests.get(f'{API_URL}/user?rfid={tag}&door_id={DOOR_ID}')
    if (response.status_code != 200):
        return None

    user = response.json()

    return {"id": user["id"],
            "name": f'{user["first name"]}_{user["last name"]}',
            "picture": cv2.imdecode(np.fromiter(user["picture"]["data"], np.uint8), cv2.IMREAD_COLOR)}


def main():
    print("Waiting for RFID contact")
    while True:
        tag = getRFIDIdentifier()
        #tag = input("Enter Your Badge: ")

        if tag is None:
            time.sleep(1)
            continue

        if tag.lower() == "exit":
            break

        user = fetch_user(tag)

        if user is None:
            print("No Match Found in the database")
        else:
            encodings = encode_image(user["picture"])
            if encodings is not None:
                matching_image = recognition(encodings)
                if matching_image:
                    # print(fetched_data[1])
                    print("Door Opens")
                else:
                    print("No Match Found")

        print("Waiting for RFID contact")


if __name__ == '__main__':
    model = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    picture = take_picture()

    cv2.imwrite("img.png", cropImage(picture))

    # Init RFID
    clf = nfc.ContactlessFrontend()
    assert clf.open("usb:04e6:5591") is True

    # Init face detection
    model = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    print("What do you want to do ?")
    print("1. Add user")
    print("2. Edit user")
    print("3. Delete user")
    print("4. Exit")

    cmd = input("-> ")

    if cmd == "1":
        first_name = input("First name: ")
        last_name = input("Last name: ")
        print("Please scan your card: ")
        rfid = getRFIDIdentifier()
        print("Don't move a picture will be taken...")
        for i in range(3, 0, -1):
            print(i, "...")
            time.sleep(1)
        print("Cheese !!!")
        picture = take_picture()

        cv2.imwrite("img.png", cropImage(picture, model))
