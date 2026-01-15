# 字典示例
person ={
    'name':'lishu',
    'id':12,
    'age':18,
}
print(person['name'])
print(person.keys())
print(person.values())
print(person.items())

for k,v in person.items():
    print(k,":",v)

#元组（不可更改）
arr=(1,2,3)
#列表
arr=[1,2,3,4]