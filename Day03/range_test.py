num = int(input("请输入一个整数:"))

count = 0

for i in range(1,num):
    if i % 2 == 0:
        count += 1


print(f"从1到{num}不包含{num}总共有{count}个偶数")