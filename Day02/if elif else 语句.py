"""
判断条件有多个

"""
height = int(input("请输入身高:"))
vip_level = int(input("请输入vip等级:"))
day = int(input("请输入今天几号:"))
if height < 120:
    print("可以免费游玩")
elif vip_level > 3:
    print("可以免费游玩")
elif day == 1:
    print("今天是一号 可以免费游玩")
else:
     print("条件都不满足，需要买票十元")

# ctrl+/加注释

