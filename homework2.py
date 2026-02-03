#!/usr/bin/python3 
#1
#for i in range(0,100,2):
#    print(i)

'''2
count=1
for i in range(1,100):
    count*=i
print(count)
'''
'''3
sentence=input("Input a sentence: ")
if not sentence.replace(" ","").isalpha():
    print("I said a sentence!!!")
    exit()
sentence=str(sentence)
vowels="aeiou"
count=0
for i in sentence:
    if i in vowels:
        count+=1
if count>0:
    print(count)
else:
    print("There is no!!!")
'''
'''4
for i in range(0,100):
    if i%15==0:
        print(f"{i} = FizzBuzz(15)")
    elif i%3==0:
        print(f"{i} = Fizz(3)")
    elif i%5==0:
        print(f"{i} = Buzz(5)")
'''
'''5
number=input("Enter a phone number: ")
missing=""
for i in range(0,10):
    if str(i) not in number:
        missing+=str(i)+" "
print(missing)
'''
