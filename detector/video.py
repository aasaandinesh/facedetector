#!/usr/bin/env python
import cv2
import imutils
import time
import sys
import argparse
import base64
import simplejson as json
import requests

from detector.models import FaceDetectionHistory

NUMBER_OF_FRAMES = 100


def get_faces_str(imagestring):
    face_check_url = "http://localhost:8080/facebox/check"
    post_data = {"faceprint": False, "base64": imagestring}
    r = requests.post(url=face_check_url, data=post_data)
    response = r.json()
    print(response)
    return response['faces']


def draw_face_identifiers(faces, frame, cv2):
    for face in faces:
        print("Printing face instead of drawing")
        print(face)
        face_rect = face['rect']
        print(face_rect)
        cv2.rectangle(frame
                      , (face_rect['left'], face_rect['top'])
                      , (face_rect['left'] + face_rect['width'], face_rect['top'] + face_rect['height'])
                      , (0, 255, 0)
                      , 2
                      )

        if face.get('name'):
            # Commenting the code of saving the history
            # face_detection_history = FaceDetectionHistory()
            # face_detection_history.name = face.get('name')
            # face_detection_history.face_id = face.get('id')
            # face_detection_history.save()
            confidence = face['confidence']
            confidence = str(confidence.__round__(2))
            cv2.putText(frame
                        , face['name']+"--"+confidence +"%"
                        , (face_rect['left'], face_rect['top'] - 10)
                        , cv2.FONT_HERSHEY_SIMPLEX
                        , 1
                        , (0, 255, 0)
                        , 1
                        , cv2.LINE_AA
                        )


class FaceDetector:

    def __init__(self, path):
        self.path = path
        self.stream = cv2.VideoCapture(path)

    path = None
    stream = None
    current_frame = None
    faces = []
    counter = 0

    def get_frame(self, frame):
        image = frame
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def videoStreamer(self, width=800, height=400, skip=None):

        stream = self.stream
        if skip is None:
            skip = 10
        for i in range(skip):
            stream.grab()
        (grabbed, frame) = stream.read()
        if not grabbed:
            self.current_frame = -1
            return -1
        frame = imutils.resize(frame, width=width, height=height)
        res = bytearray(cv2.imencode(".jpeg", frame)[1])
        if self.counter % 10 == 0:
            self.faces = get_faces_str(base64.b64encode(res))
        draw_face_identifiers(self.faces, frame, cv2)
        self.counter += 1
        return self.get_frame(frame)
