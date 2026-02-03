import random
num = random.randint(1,100)

flag = True
count = 0
while flag:
    number = int(input("请输入你猜测的数字:"))
    count = count + 1
    if number == num:
        flag = False
        print(f"恭喜你在猜测{count}次后猜测成功了")
    else:
        if(num > number):
            print("你猜测的数字小了")
        else:
            print("你猜测的数字大了")

