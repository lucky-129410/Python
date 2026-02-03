age = int(input("请输入你的年龄:"))
if 18 <= age:
    if 30 >= age:
        time = int(input("请输入入职时间:"))
        level = int(input("请输入级别:"))
        if time>2:
            print("入职时间和年龄都满足 可以领取")
        elif level>3:
            print("级别大于三 可以领取")
        else:
            print("入职时间不满足大于等于两年且级别小于等于三 不能领取")

    else:
        print("你的年龄超过三十 不能领取")
else:
    print("你的年龄不在限制范围内 不能领取")
