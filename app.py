from flask import Flask,request,jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from faceRecognition import apis
import base64
from datetime import datetime
from Crypto.Cipher import AES
from secretKey import secretKey
from flask_mail import Mail 
import random

# MAIL_USERNAME = 'karan1234iyer@gmail.com'
# MAIL_PASSWORD = 'karan1234'

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://admin:N7TQ0vJNl2JxNFGK@learnmongo.qmo7ywz.mongodb.net/gmitDB"


# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_USERNAME'] = MAIL_USERNAME
# app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
# app.config['MAIL_DEFAULT_SENDER'] = MAIL_USERNAME

mail = Mail(app)
CORS(app)
db = PyMongo(app).db

def unpad(s):
    return s[:-ord(s[len(s)-1:])]

def decrypt_password(encrypted_password, secret_key):
    encrypted_password_bytes = base64.b64decode(encrypted_password)
    cipher = AES.new(secret_key, AES.MODE_ECB)
    decrypted_bytes = cipher.decrypt(encrypted_password_bytes)
    decrypted_bytes_unpadded = unpad(decrypted_bytes)
    decrypted_password = decrypted_bytes_unpadded.decode('utf-8')
    return decrypted_password


@app.route('/')
def welcome():
    return "hello world!"
    # return render_template("./index.html")


@app.route('/signup',methods=["POST"])
def signup():
    print(f"Singup route\n")

    res = {
        "message":""
    }
    # print(f"{request.data}")
    firstname = request.json.get("firstName")
    lastname = request.json.get("lastName")
    username = request.json.get("username")
    password = request.json.get("password")
    image_data = request.json.get("image")
    print(f"{firstname}\n{lastname}\n{username}\n{password}")
    decryptPassword = decrypt_password(password,secretKey)
    print(f"{decryptPassword}")


     # Ensure image_data is a string and then convert it to bytes
    if isinstance(image_data, str):
        # Remove the base64 header if it exists
        if image_data.startswith('data:image'):
            image_data = image_data.split(',', 1)[1]
        image_bytes = base64.b64decode(image_data)
    else:
        res["message"] = "Invalid image data format"
        return jsonify(res),400
    
    # with open(f'{username}.jpg', 'wb') as jpg_file:
    #     jpg_file.write(image_bytes)

    IMG_PATH = f'faceRecognition/train/{username}.png'
    with open(IMG_PATH, 'wb') as png_file:
        png_file.write(image_bytes)

    # print(f"{firstname}\n{lastname}\n{username}\n")

    if not (firstname and lastname and username and password and image_data):
        res = {"message" : "InValid SignUp details"}
        print(f"{res}")
        return jsonify(res)
    
    # Find if this user exists before with same username!

    #Finding user in Db
    userFromDb = db.register.find_one({
        "username":username,
    })

    if userFromDb is not None:
        res["message"] = "Existing User! Please Login!!"
        return jsonify(res),400

    # Find if this user exists before with same face!
    exec,fl,userFromFr = apis.testStoredImg(IMG_PATH)
    if not exec:
        res["message"] = "Unable to identify Face/User"
        return res,400

    if userFromFr != "unknown":
        res["message"] = "A user exists!"
        return res,400
    
    #train the model!
    trainRes,msg = apis.TrainImages(username)

    if not trainRes:
        res["message"] = msg
        return res
    
    name = firstname + " " + lastname
    db.register.insert_one({
        "username":username,
        "name":name,
        "username":username,
        "password":decryptPassword,
        "lastLoginTime":datetime.now()
    })
    
    res = {"message":"success"}
    return jsonify(res)

@app.route('/signin',methods=["POST"])
def signin():
    
    print(f"SignIn route\n")

    res = {
        "message":"",
        "status":"fail"
    }

    # print(f"{request.data}")
    username = request.json.get("username")
    password = request.json.get("password")
    image_data = request.json.get("image")
    decryptPassword = decrypt_password(password,secretKey)

    print(f"{username}\n{password}\n{decryptPassword}")

     # Ensure image_data is a string and then convert it to bytes
    if isinstance(image_data, str):
        # Remove the base64 header if it exists
        if image_data.startswith('data:image'):
            image_data = image_data.split(',', 1)[1]
        image_bytes = base64.b64decode(image_data)
    else:
        res["message"] = "Invalid image data format"
        print(f"{res}")
        return (jsonify(res),200)
    
    # with open(f'{username}.jpg', 'wb') as jpg_file:
    #     jpg_file.write(image_bytes)

    authImage = f'authLogin/{username}.jpg'
    with open(f'{authImage}','wb') as png_file :
        png_file.write(image_bytes)

    if not (username and password and image_data):
        res = {"message" : "InValid Login input details"}
        print(f"{res}")
        return jsonify(res),200
    
    
    #Finding user in Db
    userFromDb = db.register.find_one({
        "username":username,
        "password":decryptPassword
    })

    # print(f"userFromDb = {userFromDb}")

    if userFromDb is None:
        res["message"] = "InValid Login Details! "
        print(f"{res}")
        return jsonify(res),200

    timeDiff = (datetime.now() - userFromDb["lastLoginTime"]).seconds

    userFromDb["lastLoginTime"] = datetime.now()
    db.register.replace_one({"_id": userFromDb["_id"]}, userFromDb)

    if timeDiff < 30:
        print(f"Rate Limit Applied, Restriction on Login")
        res["message"] = "Rate Limit Applied, Restriction on Login"
        print(f"{res}")
        return res,200

    execution,fl,userFromFr = apis.testStoredImg(authImage)
    print(f"{execution}\n{userFromFr}")

    if not execution or userFromFr=="unknown":
        res["message"] = "Unable to identify Face/User"
        print(f"{res}")
        return jsonify(res),200
    
    # Delete the stored image


    if userFromDb["username"] != userFromFr:
        res["message"] = "Username and Face misMatch!"
        print(f"{res}")
        return jsonify(res),200
    
    
    res["message"] = "successfull"
    res["status"] = "pass"
    print(f"{res}")
    return jsonify(res)


def generate_numeric_otp(length=6):
    digits = "0123456789"
    otp = "".join(random.choice(digits) for _ in range(length))
    return otp

# # Example usage:
# six_digit_otp = generate_numeric_otp ()
# print("Random 6-digit OTP:", six_digit_otp)

# userOtps = []
# @app.route('/verifyEmail',methods=["GET","POST"])
# def veirfyEmail():
#     print(f"verifyEmail POST request\n")
#     if request.method == "POST":
#         print(f"verifyEmail POST request\n")
#         res = {
#             "message":""
#         }

#         username = request.json.get("username")
#         type = request.json.get("type")

#         if type == "send-otp":
#             if not (username):
#                 res = {"message" : "InValid Login input details"}
#                 print(f"{res}")
#                 return jsonify(res),200
        
#             #Finding user in Db
#             userFromDb = db.register.find_one({
#                 "username":username,
#             })

#             if userFromDb is None:
#                 res["message"] = "InValid Login Details! "
#                 print(f"{res}")
#                 return jsonify(res),200
            
#             for u in userOtps:
#                 if u.get("username") == username:
#                     if (datetime.now() - u["time"]).seconds < 30:
#                         print(f"Rate Limit Applied, Restriction on Login")
#                         res["message"] = "Rate Limit Applied, Restriction on Email VeriFication"
#                         print(f"{res}")
#                         return res,200
            
#             userOtp = {
#                 "uesrname":username,
#                 "otp":generate_numeric_otp(),
#                 "time":datetime.now(),
#             }
#             # Send Email
#             print(f"{userOtps}")
#             userOtps.append(userOtp)

#             mail.send_message("OTP verification for GMIT-HACKATHON!",
#             sender = MAIL_USERNAME,
#             recipients = username,
#             body = f"OTP verification for GMIT-HACKATHON!,\nYour OTP is {userOtp['otp']}!!",
#             )
#             res["message"] = "Email Sent SuccessFully!!"
#             print(f"{res}")
#             return jsonify(res),200


#     userOtps.append(userOtp)



if __name__=='__main__':
    # apis.TrainImages()
    app.run(debug=True)