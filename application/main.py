import numpy as np
import cv2
import pickle
import time
from tkinter import *
import tkMessageBox
import os
from face_train import train

# running the face train algorithm
train()

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascades/haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier('cascades/data/haarcascades/haarcascade_eye.xml')
recognizer= cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainner.yml")

labels = {"person_name":1}
with open("labels.pickle", 'rb') as f:
    # dump the label ids to a file
    og_labels = pickle.load(f)
    labels = {v:k for k,v in og_labels.items()}

cap = cv2.VideoCapture(0)

match=0
mismatch=0

timeout = time.time() + 10

while(True):
    if time.time()> timeout:
        break
    # Capturing the frames
    ret, frame = cap.read()

    # display the time in the screen
    font = cv2.FONT_HERSHEY_SIMPLEX
    name = "Authenticating.."+str(timeout-time.time())
    color = (0, 0, 255)
    stroke = 2
    cv2.putText(frame, name, (25, 25), font, 1, color, stroke, cv2.LINE_AA)

    # too identify the face movements a gray frame is needed
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(gray,scaleFactor=1.5,minNeighbors=5)

    for(x,y,w,h) in faces:
        #print(x,y,w,h)

        #taking the grey view oof the frame
        interested_region=gray[y:y+h,x:x+w]
        interested_region_color=frame[y:y+h,x:x+w]

        id_,conf = recognizer.predict(interested_region)
        print conf,labels[id_]

        # if the users are identical conf value is less. if we checked the conf level for more accuracy.

        if conf >= 25:
            #print(id_)
            print(labels[id_])
            font= cv2.FONT_HERSHEY_SIMPLEX
            #name=labels[id_]
            name = "Not Recognized"
            color=(255,255,255)
            stroke=2
            cv2.putText(frame,name,(x,y),font,1,color,stroke,cv2.LINE_AA)
            mismatch+=1
        else:
            font = cv2.FONT_HERSHEY_SIMPLEX
            #name = "New User"
            name = "Recognized"
            color = (0, 0, 255)
            stroke = 2
            cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
            match+=1
        interested_image="user-image.png"
        cv2.imwrite(interested_image,interested_region)

        # mark the eye region
        color = (0,200,20)
        thickness = 4
        ending_cordinatex = x+w
        ending_cordinatey = y+h
        cv2.rectangle(frame, (x,y),(ending_cordinatex,ending_cordinatey),color,thickness)
        eyes=eye_cascade.detectMultiScale(interested_region)
        for(ex,ey,ew,eh) in eyes:
            cv2.rectangle(interested_region_color,(ex,ey),(ex+ew,ey+eh),(255,0,0),2)

    # Display the frame to the user
    cv2.imshow('frame',frame)
    # Display the grey frame

    # cv2.imshow('gray',gray)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# releasing the capture at last
cap.release()
cv2.destroyAllWindows()


# if the user is detected deny the register
if match <= mismatch:
    print(match/(mismatch+match))
    print "not-recognized"
    window = Tk()
    window.withdraw()
    tkMessageBox.showerror('Error', 'Error Login ?')
    def createFolder(directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print ('Error: Creating directory. ' + directory)

    def show_name():
        print(e1.get())
        new_user = e1.get()
        file_path = 'images/'+new_user
        createFolder('./'+file_path+'/')

        # taking photos and save them in the new folder
        cap = cv2.VideoCapture(0)

        photoframe=0
        photo_timeout = time.time() + 5
        while (True):
            if time.time() > photo_timeout:
                break
            photoframe+=1
            # Capture frame-by-frame

            ret, frame = cap.read()
            # Our operations on the frame come here
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = "Identifying the face..."+str(photo_timeout - time.time())
            color = (0, 0, 255)
            stroke = 2
            cv2.putText(frame, name, (25, 25), font, 1, color, stroke, cv2.LINE_AA)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Display the resulting frame
            cv2.imshow('frame', frame)

            # take photographs of the new user
            if photoframe == 10:
                cv2.imwrite(os.path.join(file_path, 'pic1.png'), frame)
            elif photoframe == 20:
                cv2.imwrite(os.path.join(file_path, 'pic2.png'), frame)
            elif photoframe == 30:
                cv2.imwrite(os.path.join(file_path, 'pic3.png'), frame)
            elif photoframe == 40:
                cv2.imwrite(os.path.join(file_path, 'pic4.png'), frame)
            elif photoframe == 50:
                cv2.imwrite(os.path.join(file_path, 'pic5.png'), frame)
            elif photoframe == 60:
                cv2.imwrite(os.path.join(file_path, 'pic6.png'), frame)
            elif photoframe == 60:
                cv2.imwrite(os.path.join(file_path, 'pic7.png'), frame)
            elif photoframe == 60:
                cv2.imwrite(os.path.join(file_path, 'pic8.png'), frame)
            elif photoframe == 60:
                cv2.imwrite(os.path.join(file_path, 'pic9.png'), frame)
            elif photoframe == 60:
                cv2.imwrite(os.path.join(file_path, 'pic10.png'), frame)
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()


    # display the register window
    window = Tk()
    window.title("Register")
    window.geometry("275x100")
    window.configure(background="#D7BDE2")

    Label(window, text="First Name").grid(row=0, column=6, padx=5, pady=5)

    e1 = Entry(window)

    e1.grid(row=3, column=6)

    Button(window, text='Register', command=show_name, fg="white", bg="#F5B7B1").grid(row=4, column=0, sticky=W, pady=4)

    mainloop()

else:
    print(mismatch/(match+mismatch))
    print "recognized"
    # creating a blank window

    # create a folder using the user name
