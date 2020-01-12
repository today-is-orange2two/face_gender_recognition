
# coding: utf-8

# In[ ]:


"""
이 코드를 실행하면 DB에 저장된 모든 테이블 삭제 
data 폴더에 저장된 모든 이미지파일 삭제

"""

import sqlite3
import os
import shutil


def del_all():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    sql = """
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
               id integer unique primary key autoincrement,
               name text,
               gender text
    );
    """
    c.executescript(sql) # 한번의 호출로 여러 SQL문을 실행할때 사용

    if os.path.exists("./dataset"):
        shutil.rmtree("./dataset")
    else:
        os.mkdir("./dataset")
    
    print("[NOTICE] System initialization")
    conn.commit()
    conn.close()

