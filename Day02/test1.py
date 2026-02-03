number = 10

if number == int(input("请输入第一次猜想的数字:")):
    print("恭喜你猜对了")
elif number == int(input("不对，再猜一次:")):
    print("恭喜你猜对了")
else:
    print(f"sorry 全部猜错了 我猜想的数字是{number}")