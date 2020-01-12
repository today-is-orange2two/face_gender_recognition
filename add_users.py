
# coding: utf-8

# In[ ]:


"""
추가 사용자 등록을 할 경우 여기서부터 실행

"""

import sqlite3
import cv2
import numpy as np 
import sqlite3
import os
from PIL import Image
import glob
from keras.models import load_model



def add_users():
    conn = sqlite3.connect('database.db')
    if not os.path.exists('./dataset'):
        os.makedirs('./dataset')

    # Connection를 얻으면 cursor() 객체를 만들어야 excute()메서드 호출가능
    c = conn.cursor()
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(0)
    uname = input("Enter your name: ")

    c.execute('INSERT INTO users (name) VALUES (?)', (uname,))

    # 읽기전용 어트리뷰트로 마지막으로 수정된 행의 rowid() 제공
    # excute() 메서드를 사용하여 insert나 replace를 실행했을때만 설정
    uid = c.lastrowid
    print("\n [NOTICE] Initializing face capture. Look the camera and wait a few moment")
    count = 0
    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            count = count+1
            cv2.imwrite("dataset/"+str(uname)+"."+str(uid)+"."+str(count)+".jpg",gray[y:y+h,x:x+w])
            cv2.rectangle(img, (x,y), (x+w, y+h), (255,255,255), 2)
            cv2.waitKey(100)
        cv2.imshow('img',img)
        if cv2.waitKey(1)==13 or count == 50:
            break
    print("\n [NOTICE] Exiting camera and cleanup stuff")
    cap.release()
    cv2.destroyAllWindows()


    caltech_dir = './dataset'

    image_w = 64
    image_h = 64

    pixels = image_h * image_w * 3

    X = []
    filenames = []

    files = glob.glob(caltech_dir+"/"+uname+"*.*")
    for i, f in enumerate(files):
        img = Image.open(f)
        img = img.convert("RGB")
        img = img.resize((image_w, image_h))
        data = np.asarray(img)
        filenames.append(f)
        X.append(data)

    X = np.array(X)
    X = X.astype(float) / 255
    model = load_model('./model/male_female_classify.model')#학습시킨 모델

    prediction = model.predict(X)

    cnt = 0
    cnt_m = 0
    cnt_f = 0
    for i in prediction:
        if i >= 0.5: #여자일때
            cnt_f +=1
        else:        #남자일때
            cnt_m +=1
        cnt += 1

    if cnt_m > cnt_f:
        sql = "UPDATE users SET gender=(?) WHERE name=(?)"
        c.execute(sql,("male",uname)) 
        print(f"\n [NOTICE] {uname} is male")
    else:
        sql = "UPDATE users SET gender=(?) WHERE name=(?)"
        c.execute(sql,("female",uname))
        print(f"\n [NOTICE] {uname} is female")

    print("\n [NOTICE] be close the registration program")

    conn.commit()
    conn.close()

