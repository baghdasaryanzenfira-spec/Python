#!/usr/bin/python3
'''1-2-3
nums=[]
for i in range(3):
    n=int(input(f"Input number {i+1}/3: "))
    nums.append(n)
print(nums)
print(f"max_num = {max(nums)}")
print(f"min_num = {min(nums)}")
print(f"min to max = {sorted(nums)}")
'''
'''1-2-3
a=int(input("Mutqagrir tiv 1/3: "))
b=int(input("Mutqagrir tiv 2/3: "))
c=int(input("Mutqagrir tiv 3/3: "))
small=min(a,b,c)
big=max(a,b,c)
print(f"max_num = {big}")
print(f"min_num = {small}")
if a<=b and a<=c:
    if b<=c:
        print(f"max to min = {a,b,c}")
    else:
        print(f"max to min = {a,c,b}")
elif b<=a and b<=c:
    if a<=c:
        print(f"max to min = {b,a,c}")
    else: 
        print(f"max to min = {b,c,a}")
else:
    if a<=b:
        print(f"max to min = {c,a,b}")
    else:
        print(f"max to min = {c,b,a}")
'''
'''4
num=input("Input a number: ")
if num.isdigit():
    num=int(num)
    if num%3==0 and num%5==0:
        print("FizzBuzz")
    elif num%3==0:
        print("Fizz")
    elif num%5==0:
        print("Buzz")
    else:
        print("Try a different number: ")
else:
    print("Icorrect input!!")
'''
'''5
num=input("Enter a three-digit num: ")
if num.isdigit():
    if len(num)==3:
        if num[0]<num[-1]:
            print("Yes")
        elif num[0]==num[-1]:
            print("Yes-No")
        else:
            print("No")
    else:
        print("I said three-digit! ")
else:
    print("I said a number")
'''   

