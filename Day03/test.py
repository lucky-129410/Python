import random
money = 10000
for i in range(1,21):

    if money <=0:
        print("工资发完了 下个月再领取吧")
        break

    score = random.randint(1, 10)
    if score>=5:
        money = money - 1000
        print(f"员工{i}发放工资1000元,账户余额还剩{money}元")
    else:
        print(f"员工{i}绩效分{score},低于5,不发工资,下一位")
        continue
