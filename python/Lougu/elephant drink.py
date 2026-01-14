import math
h,r=map(int,input().split())
v=h*3.14*r*r
n=math.ceil(20*1000/v)
#向上取整的函数
print(n)