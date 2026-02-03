"""
continue->跳过当前循环
break->终端该循环语句
"""

for i in range(1,5):
    if i == 2:
        continue
    else:
        print(i)


for j in range(1,5):
    if j == 2:
        break
    else:
        print(j)


