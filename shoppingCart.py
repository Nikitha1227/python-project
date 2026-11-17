product=[]

def add():
    p=input('Enter product name:')
    product.append(p)
    print('product is added')
def remove():
    p=input('Enter product name to remove:')
    if p in product:
        product.remove(p)
        print('product is removed')
    else:
        print('no such product')
def display():
    print("\n---Products in cart----")
    for p in product:
        print(p)
        

for i in range(50):
    print('-----shopping cart------')
    print('1:Add product')
    print('2:remove product')
    print('3:display')
    print('4:exit')
    ch=int(input('Enter your choice:'))
    if ch==1:
        add()
    elif ch==2:
        remove()
    elif ch==3:
        display()
    elif ch==4:
        print('exit')
        break
    else:
        print('invalid choice')




