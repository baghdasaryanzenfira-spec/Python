#!/usr/bin/python3
#1
#sentence=input("Input a sentence: (with numbers): ")
#count=0
#for i in sentence:
#    if i.isdigit():
#        count+=int(i)
#print(count)


#2
#sentence=input("Input a sentence: (with numbers): ")
#nstr=""
#for i in sentence:
#    if i.isalpha():
#        if i.isupper():
#            nstr+=i
#print(nstr)

#3
#count=0
#for i in range(100,1000):
#        i=str(i)
#        if i==i[::-1]:
#            count+=1
#print(count)

#4
#n=int(input("Enter a num: "))
#m=int(input("Enter a num: "))
#if n>m:
#    n,m=m,n
#print(f"[n,m]={n,m}")
#count=0
#for i in range(n,m+1):
#    if i%2==0:
#        count+=i
#print(f"Even_sum={count}")

#5
sentence=input("Input a sentence: ").lower()
count=0
index=0
while index<len(sentence):
    i=sentence[index]
    if i.isalpha():
        if i in "aeiou":
            index+=1
            continue
        count+=1
    index+=1
print(count)
