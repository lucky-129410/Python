""""
True->1 真
False->0 假
比较运算符：== ！= > < >= <=
"""

result1 = 1>2
print(result1,"类型为%s"%type(result1))

result2 = "lucky"=="lucky"
#字符串可以直接进行比价
print(result2,"类型为%s"%type(result2))

result3 = "lucky"!="zlg"
print(result3,"类型为%s"%type(result3))

num1 = 10
num2 = 20
print(f"10==10的结果为{num1==num2}")

num1 = "itcast"
num2 = "ith"
print(f"itcast<=ith的结果是{num1<=num2}")

