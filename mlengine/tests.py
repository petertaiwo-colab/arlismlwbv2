# from django.test import TestCase
# import os, subprocess
# # from MLWB.MLWB.models import Usersessn, Admintrack
# # Create your tests here.

# # def opennb(port):
# #     os.system('jupyter notebook --no-browser --ip 0.0.0.0 --port='+port) 

# # opennb('8897')
# def opennb(port):
#     # cmd = ['ls', '-l']
#     cmd = ['jupyter', 'notebook', '--no-browser', '--ip', '192.168.1.214', '--port='+port]
#     subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     # cmd2 = ['jupyter', 'notebook', 'list|grep', ':'+port]

# def geturl(port):
#     cmd1 = ['jupyter', 'notebook', 'list']
#     p1 = subprocess.run(cmd1, capture_output=True, text=True)
#     cmd2 = ['grep', port]
#     p2 = subprocess.run(cmd2, capture_output=True, text=True, input=p1.stdout)
#     return p2.stdout.split()[0]

#     # out, err = p1.communicate()
    
# # opennb('8898')

# import random

# S=[]
# # m = max(S)

# ninS = random.choice([x for x in range(8880,8899) if x not in S])

# url1 = geturl('8898')
# print(url1)
# print(ninS)
# S.append(ninS)
# print(S)
# try:
#     S.remove(10)
# except:
#     print('item not in list')
# print(S)

import pyperclip
    pyperclip.copy("abcdbka;jgj p")  # now the clipboard content will be string "abc"
    pyperclip.paste()  # text will have the content of clipboard
