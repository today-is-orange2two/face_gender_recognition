
# coding: utf-8

# In[ ]:


"""
이 코드를 실행하면 선택된 회원의 DB 이름 변경
data 폴더에 저장된 선택된 회원의 모든 이미지파일 이름 변경

"""

import sqlite3
import os
import shutil

def edit_user():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    uname = input("Enter your name: ")
    sname = input("Enter your nane to change: ")


    c.execute("SELECT * FROM users WHERE name=(?)",(uname,))
    result = c.fetchone()

    try:
        if uname in result:
            sql = "UPDATE users SET name=(?) WHERE name=(?)"
            c.execute(sql,(sname,uname)) 

            print("Successfully changed")

            # 현재 위치(./dataset)의 파일을 모두 가져온다. 
            path = "./dataset"
            for filename in os.listdir(path): 

                # 파일 확장자가 (jpg)인 것만 처리 
                if filename.endswith("jpg"): 

                    # 파일명에서 uname를 sname로 변경하고 파일명 수정 
                    new_filename = filename.replace(uname, sname) 
                    os.rename(path+"/"+filename, path+"/"+new_filename)
    except TypeError: 
        print("not exists, please check your id")

    conn.commit()
    conn.close()

