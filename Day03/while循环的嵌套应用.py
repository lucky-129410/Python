"""
print("hello",end = " ")
这样就不会换行 不然默认自动换行


print("hello\tworld")
print("itheima\tbest")

这样就会自动对齐
"""

#打印九九乘法表
i = 1
while i<=9:
    j = 1
    while j<=9:
        print(f"{i*j}\t",end = " ")
        j+=1
    i = i+1
    print()
