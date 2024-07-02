import os
import face_recognition
import cv2
import numpy as np
import pickle
import timeit

baseExecFolder = "faceRecognition"
baseTrainedPicklePath = os.path.join(baseExecFolder,"trainedPickleFiles")
savedPickleFile = "gmitDB.pkl"
savedPicklePath = os.path.join(baseTrainedPicklePath,savedPickleFile)

from faceRecognition.trainImages import TrainImages


def _testImg_(tImg):

    if (tImg is None):
        print(f"Image does not exist!")
        return False

    rgb_testImg = cv2.cvtColor(tImg, cv2.COLOR_RGB2BGR)
    testImgLocations = face_recognition.face_locations(tImg)
    test_img_encoding = face_recognition.face_encodings(rgb_testImg, testImgLocations,)
    test_img_encoding = test_img_encoding[0]

    if test_img_encoding is None:
        print(f"Image contains NO Face or Face is not identifiable!")
        return False

    with open(savedPicklePath, 'rb') as file:
        trainedData = pickle.load(file)
        trainedFaceEncodings,trainedFaceNames = trainedData
        # print(trainedFaceNames)

    matches = face_recognition.face_distance(trainedFaceEncodings, test_img_encoding)
    matchedIndex = np.argmin(matches)
    results = [trainedFaceNames[matchedIndex] if matches[matchedIndex] < 0.55 else f"unknown"]
    print(f"{results}")
    return (True,testImgLocations,results)

def testStoredImg(imgPath):

    #Comparing
    testImg = cv2.imread(imgPath)
    exec,fl,fnames = _testImg_(testImg)
    print(f"{exec}\n{fnames}")
    return exec,fl,fnames[0]

# Live video
def LiveVideo():

    foundUser = "unknown"
    print("Live Video!")
    cv2.namedWindow("VideoAuthenticate")
    video_capture = cv2.VideoCapture(1)

    if not video_capture.isOpened():
        print("Error: Could not open video device.")
    else:
        print("Camera initialized.")

    FRAME_SKIP = 5
    frameCount = 0
    while True:
        ret, frame = video_capture.read()
        frameCount += 1
        face_locations = []
        face_names = []

        start = timeit.default_timer()
        if frameCount%FRAME_SKIP != 0:
            # Identifiying person ,Prediction:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            x = _testImg_(rgb_small_frame)
            if not x:
                print(f"{x}")
            else:
                execution,face_locations,face_names=x
                foundUser = face_names[0]

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Display the resulting image
            cv2.imshow('VideoAuthenticate', frame)

        # cv2.imshow('Video', frame)
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # return foundUser
            break

    return foundUser

if __name__ == "__main__":
    LiveVideo()
