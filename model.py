#!/usr/bin/env python3 .11 
# -*- coding: utf-8 -*-
"""
@author: noob
"""

import cv2
import copy
from faker import Faker
import tkinter as tk
import os
from mtcnn import MTCNN
import face_recognition


def on_close(event):
    window.destroy()

def handle_input(event):
    # Check if the input is '0' and close the window if true
    if event.char == '0':
        window.destroy()


def get_image_names(folder_path):
    # Check if the folder path exists
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return []
    all_files = os.listdir(folder_path)
    image_files = [file for file in all_files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    return image_files



class Person:
    def __init__(self,face_encode,name=None):
        # result = value_if_true if condition else value_if_false
        self.name = Faker().name if name is None else name
        self.mainface = face_encode
    

                
    def showMeInIMGs(self,connections):
        print("Person  : "+str(self.name)+"\n")
        for connection in  connections:
            if connection.Person == self:
                connection.ImageObj.selectface(connection.facebox,str(self.name))

    

class img_obj:
    def __init__(self,image_path):
        self.image_path = image_path
        self.image = face_recognition.load_image_file(dir+'/'+image_path)
        # FOR PERSENTATION
        #self.image=cv2.resize(self.image, (800,600))
        self.faces = self.detect_faces()
        self.boxs_mtcnn = [tuple(d['box']) for d in self.faces]
        self.boxs = self.convertMTCNNT2FRT(self.boxs_mtcnn)
        print("I: I am going to calculate Encoding , it will take time")
        self.encodes  = face_recognition.face_encodings(self.image,self.boxs,num_jitters=100)
        if self.encodes:
            print("I: DOne PRO")
        
        
    def detect_faces(self):
        detector = MTCNN(steps_threshold=[0.8, 0.9, 0.9])
        return detector.detect_faces(self.image)
    
    def detect_show(self,mode):
        # mode 1 = MTCNN
        # mode 2 = face_recognition
        tmp = self.getimage_copy()
        tmp = cv2.cvtColor(tmp, cv2.COLOR_BGR2RGB)
        if mode == 1:
            for left, top, rightp, bottomP in  self.boxs_mtcnn:
                cv2.rectangle(tmp, (left, top), (left+rightp, top+bottomP), (0, 255, 0), 2)
        elif mode == 2:
            for top, right, bottom, left in self.boxs:
              cv2.rectangle(tmp, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.imshow('Detected Faces', tmp)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

            
    
    def getimage_copy(self):
        return copy.deepcopy(self.image)
    
    def convertMTCNNT2FRT(self,boxes):
        myboxs = []
        for left, top, rightp, bottomP in boxes:
            # face_recognition : top, right, bottom, left
            # MTCNN : left top Rightp(width) bottomP(height) 
            right = left+rightp
            bottom = top+bottomP
            myboxs.append((top,right,bottom,left)) 
        return myboxs
    
    def getfaceinpic(self,box,index=0):
        tmp = self.getimage_copy()
        tmp = cv2.cvtColor(tmp, cv2.COLOR_BGR2RGB)
        top, right, bottom, left = box
        cv2.rectangle(tmp, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.imshow('Detected Face '+str(index), tmp)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    def selectface(self,face_boxs,person_name):
        tmp = self.getimage_copy()
        tmp = cv2.cvtColor(tmp, cv2.COLOR_BGR2RGB)
        top, right, bottom, left = face_boxs
        cv2.rectangle(tmp, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.imshow(person_name, tmp)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        
  



class Person_Image_Faces:
    def __init__(self,Person,ImageObj,Person_box):
        self.Person = Person
        self.ImageObj = ImageObj
        self.facebox = Person_box

dir = "photos"
listImage = get_image_names(dir)

imgList = []
for filename in listImage:
    imgList.append(img_obj(filename))


for imgObj in imgList:
    imgObj.detect_show(mode=2)


PersonList = []
ConnectioList =[]

for i in range(len(imgList[0].encodes)):
    PersonList.append(Person(face_encode=imgList[0].encodes[i]))
    ConnectioList.append(Person_Image_Faces(PersonList[-1],imgList[0],Person_box=imgList[0].boxs[i]))
    
if len(imgList) > 1 :
    for imgObj in imgList[1:]:
        for encode, box in zip(imgObj.encodes, imgObj.boxs):
            flag = False
            for person in PersonList:
                res = face_recognition.compare_faces([person.mainface], encode,tolerance=0.5)[0]
                if res:
                    ConnectioList.append(Person_Image_Faces(person,imgObj,Person_box=box))
                    flag = True
                    break
            if not flag:
                PersonList.append(Person(face_encode=encode))
                ConnectioList.append(Person_Image_Faces(PersonList[-1],imgObj,Person_box=box))


counter = 0
for person in PersonList:
    counter = counter +1
    window = tk.Tk()
    window.title("Person Images")
    message = """ Peson """ + str(counter)
    label = tk.Label(window, text=message, font=("Arial", 12))
    label.pack(padx=10, pady=10)
    window.protocol("WM_DELETE_WINDOW", on_close)
    window.bind('<Key>', handle_input)
    window.mainloop()
    person.showMeInIMGs(ConnectioList)
