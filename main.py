
# coding: utf-8

# In[1]:


import add_users
import del_all
import del_choice
import edit_user
import identi_users
import numpy_data

help ="""
0    : 도움말
1    : 사용자식별
444  : 종료
1111 : 사용자등록
2222 : 사용자삭제(선택된 사용자)
3333 : 사용자정보변경
9999 : 사용자삭제(전체초기화)
"""

def main():
    num = input("Enter a number (need help '0') >> ")
    
    if num == "0": #도움말
        print(help)
        return main()
    elif num == "1": #사용자식별
        identi_users.identi_user()
        exit()
    elif num == "444": #종료
        print("[NOTICE] Shut down")
        exit()        
    elif num == "1111": #사용자등록
        add_users.add_users()
        numpy_data.numpy_data()
        return main() 
    elif num == "2222": #사용자삭제
        del_choice.del_choice()
        return main() 
    elif num == "3333": #사용자정보변경
        edit_user.edit_user()
        return main() 
    elif num == "9999": #사용자삭제(전체초기화)
        del_all.del_all()
        return main() 
    else:
        print("\nSelect a number again")
        return main()     
    
if __name__=='__main__':
    main()

