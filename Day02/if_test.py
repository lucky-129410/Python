from pandas.io.stata import excessive_string_length_error
print("欢迎来到黑马儿童乐园，儿童免费，成人收费")
age = int(input("请输入年龄:"))
if age >= 18:
    print("您已经成年，请补票十元")
else:
    print("你未成年 可以免费游玩")
print("祝你游玩愉快")

#else 不需要判断条件 需要冒号和缩进