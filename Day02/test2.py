import random
num = random.randint(1,10)
guess_number = int(input("请输入你第一次猜的数字"))
if num!=guess_number:
    if num<guess_number:
        print("猜大了 重新猜")
        guess_number = int(input("请输入你第二次猜的数字"))
        if guess_number!=num:
            if num < guess_number:
                print("猜大了 重新猜")
                guess_number = int(input("请输入你第三次猜的数字"))
                if guess_number!=num:
                    print(f"sorry 三次都猜错了 挑战失败 要猜测的数字时{num}")
                else:
                    print(f"恭喜你猜对了 数字是{num}")
            else:
                print("猜小了 重新猜测")
                guess_number = int(input("请输入你第三次猜的数字"))
                if guess_number != num:
                    print(f"sorry 三次都猜错了 挑战失败 要猜测的数字时{num}")
                else:
                    print(f"恭喜你猜对了 数字是{num}")
        else:
            print(f"恭喜你猜对了 数字是{num}")
    else:
        print("猜小了 重新猜")
        guess_number = int(input("请输入你第二次猜的数字"))
        if guess_number != num:
            if num < guess_number:
                print("猜大了 重新猜")
                guess_number = int(input("请输入你第三次猜的数字"))
                if guess_number != num:
                    print(f"sorry 三次都猜错了 挑战失败 要猜测的数字时{num}")
                else:
                    print(f"恭喜你猜对了 数字是{num}")
            else:
                print("猜小了 重新猜测")
                guess_number = int(input("请输入你第三次猜的数字"))
                if guess_number != num:
                    print(f"sorry 三次都猜错了 挑战失败 要猜测的数字时{num}")
                else:
                    print(f"恭喜你猜对了 数字是{num}")
        else:
            print(f"恭喜你猜对了 数字是{num}")


else:
    print(f"恭喜你猜对了 数字是{num}")