myString="ABCDEFGHIJKLMNOPQRSTUVWXY"
width=4
res=""
for i in range(len(myString)):
    res+=myString[i]
    if i>0 and (i+1)%width==0:
        print(res)
        res=''
print(res)
