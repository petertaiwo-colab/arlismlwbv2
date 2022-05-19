# # import os
# # s1 = os.popen('~/.local/bin/kaggle datasets list -s cat,dog').read().splitlines()
# # print(s1)

# #  Import pandas package 
# import pandas as pd 
    
# # making data frame 
# data = pd.read_csv("https://media.geeksforgeeks.org/wp-content/uploads/nba.csv") 
    
# # calling head() method  
# # storing in new variable 
# data_top = data.head() 
    
# # display 
# # print(data_top)

# # # Import pandas package 
# # import pandas as pd 
    
# # # making data frame 
# # data = pd.read_csv("nba.csv") 
  
# # iterating the columns
# B="<tr><th></th>"
# for col in data_top.columns:
#     B += "<th>"+col+"</th>"
# B += "</tr>"
# print(B)

# print(data.columns[0])

# for i in range(len(data_top.index)):
#     A="<tr><th>"+str(i)+"</th>"
#     for j in range(len(data_top.columns)):
#        A += "<td>"+str(data_top._get_value(i,data.columns[j]))+"</td>"
#     A += "</tr>"
#     print(A)
    

# to join see below
# print(len(data_top.index))

# # df.get_value(10, 'Salary')
# # ndex = df.index

# # number_of_rows = len(index)
# print(data_top._get_value(3,"Salary"))

# # find length of index
# print([i for i in range(3)])

# # print(number_of_rows)

# >>> ''.join(['first', 'second', 'other'])
# 'firstsecondother'

# is what you want.

# If you do it in a for loop, it's going to be inefficient as string "addition"/concatenation doesn't scale well (but of course it's possible):

# >>> mylist = ['first', 'second', 'other']
# >>> s = ""
# >>> for item in mylist:
# ...    s += item
# ...
# >>> s
# 'firstsecondother'
import os

os.environ['KAGGLE_USERNAME'] = "petertaiwo"
os.environ['KAGGLE_KEY'] = "463e53d7143fadf6c40abbab2d8f0135"
os.system("kaggle datasets list -s 'cats'") 
# pip install kaggle