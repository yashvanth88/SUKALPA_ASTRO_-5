import os
import face_recognition
import cv2
import pickle

# Train or Get Encodings
BasePath = "faceRecognition"
PickleFilePath = os.path.join(BasePath,"trainedPickleFiles/gmitDB.pkl")

# trainData = [[],[]]
# with open(PickleFilePath,'wb') as file:
#     pickle.dump(trainData,file)
# print(f"Pickle Dump is successful!")

def TrainImages(username=None):

    trainedFaceEncodings = []
    trainedFaceNames = []

    baseTrainFolder = os.path.join(BasePath,"train")
    allTrainImagesWExt = os.listdir(baseTrainFolder)
    allImageNames = []

    for ip in allTrainImagesWExt:
        filename,ext = os.path.splitext(ip)
        allImageNames.append(filename)

    # if username is not None:
    #     with open(PickleFilePath, 'rb') as file:
    #         trainedData = pickle.load(file)
    #         trainedFaceEncodings,trainedFaceNames = trainedData
    #         # print(trainedFaceNames)


    for imgPath,imgName in zip(allTrainImagesWExt,allImageNames):
        fImgPath = os.path.join(baseTrainFolder,imgPath)
        img1 = cv2.imread(fImgPath)
        rgb_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)

        # if  username is None or imgName==username:
        img_locations1 = face_recognition.face_locations(rgb_img1,model="hog")
        img_encoding1 = face_recognition.face_encodings(rgb_img1, img_locations1,2,model="large")[0]

        if img_locations1 is None or img_encoding1 is None:
            return False,"Unable to Identify Face in this!"
        
        trainedFaceEncodings.append(img_encoding1)
        trainedFaceNames.append(imgName)


    trainData = [trainedFaceEncodings, trainedFaceNames]
    with open(PickleFilePath,'wb') as file:
        pickle.dump(trainData,file)

    print(f"Pickle Dump is successful!")
    print(f"{trainedFaceNames}")

    return True,"New User Added and Saved Successfully!"



if __name__ == "__main__":
    # BasePath = ""
    # PickleFilePath = os.path.join(BasePath,"trainedPickleFiles","gmitDB.pkl")
    TrainImages()
    pass