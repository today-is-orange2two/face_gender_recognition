
# coding: utf-8

# In[ ]:


"""
상시 실행 후 얼굴 분석 후 결과값 도출
나온 결과값으로 성별 확인

"""

#### 사용자 인증 ####

import cv2
import numpy as np 
import sqlite3
import os

from PIL import Image
import glob
from keras.models import load_model


def identi_user():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    fname = "recognizer/trainingData.yml"
    if not os.path.isfile(fname):
        print("Please train the data first")
        exit(0)

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(fname)

    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,128,0),3)
            ids,conf = recognizer.predict(gray[y:y+h,x:x+w])
            c.execute("SELECT name FROM users WHERE id = (?);", (ids,))

            # 쿼리문 질의 결과의 모든 행을 가져와서 리스트를 반환, 행이 없으면 빈 리스트가 반환
            result = c.fetchall()
            name = result[0][0]
            if conf < 50:
                cv2.putText(img, name, (x+3,y+h-3), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,0),2)
            else:
                cv2.putText(img, 'No Match', (x+3,y+h-3), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,220),2)
        cv2.imshow('DTWORESOURCE',img)
        k = cv2.waitKey(30) & 0xff
        if k == 27: # esc 키 누르면 종료
            break

    print(f" [NOTICE] {name.upper()}, Identify confirmation")
    print(f"\n [NOTICE] Welcome {name.upper()}") 
    cap.release()
    cv2.destroyAllWindows()

    #### 성별 확인 ####

    c.execute("SELECT gender FROM users WHERE name=(?)",(name,))
    # 쿼리문 질의 결과의 단일 행을 가져와서 리스트를 반환
    gen = c.fetchone()

    if "male" in gen:
        gen = "남성"
    elif "female" in gen:
        gen = "여성"

    print(f"\n [NOTICE] {name}의 성별은 {gen}입니다.")

