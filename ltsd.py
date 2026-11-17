#List
fruits=['apple','banana','orange']
fruits.insert(0,'mango')
fruits.remove('banana')
fruits[1]='grapes'
print(fruits)
print(fruits[-2])

#tuple
contact=('nikitha',20,'student')
name,age,designation=contact
print(name)
print(age)

#set
fruit={'orange','mango','apple'}
fruit.add('grapes')
fruit.discard('apple')
print(fruit)

#dic
student={
    'name':'nikitha',
    'dept':'cse',
    'age':20,
    'marks':85
}
print(student)
print(student.get('name'))
print(student["dept"])
student['city']='bangalore'
student.pop('marks')
print(student)
for key,value in student.items():
    print(key,":",value)
print(student.keys())
print(student.values())

#slicing
marks=[20,25,30,35,40]
print(marks[1:3])
print(marks[2:])
print(marks[::-1])