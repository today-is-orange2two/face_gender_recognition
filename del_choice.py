
# coding: utf-8

# In[ ]:


"""
이 코드를 실행하면 선택된 회원의 DB 삭제 
data 폴더에 저장된 선택된 회원의 모든 이미지파일 삭제

"""

import sqlite3
import os
import shutil
import glob


def del_choice():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    uname = input("Enter your name: ")


    c.execute("SELECT * FROM users WHERE name=(?)",(uname,))
    result = c.fetchone()

    try:
        if uname in result:
            c.execute("DELETE FROM users WHERE name=(?)",(uname,)) 
            os.system('rm ' + './dataset/' + uname + '*' + '.jpg')
            print("Successfully deleted")
    except TypeError: 
        print("not exists, please check your id")


    conn.commit()
    conn.close()

