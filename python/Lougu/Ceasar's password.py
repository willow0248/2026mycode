"""蒟蒻虽然忘记密码，但他还记得密码是由一个字符串组成。
密码是由原文字符串（由不超过 50 个小写字母组成）中每个字母向后移动 n 位形成的。
z 的下一个字母是 a
如此循环。他现在找到了移动前的原文字符串及 n
请你求出密码。"""

c=int(input())
original=input()
password=""
for i in original:
    new=chr((ord(i)-ord('a')+c)%26+ord('a'))
    password+=new
print(password)