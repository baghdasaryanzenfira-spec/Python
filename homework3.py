#!/usr/bin/python3
sentence=input("Input a sentence: (with numbers): ")
count=0
for i in sentence:
    if i.isdigit():
        count+=int(i)
print(count)
        
