print('guess any number:')
min=0
max=100
n=max+1//2
for i in range(max):
    m=input(f"is you number {n}(yes,greater,lesser)")
    if (m=='greater'):
        max=n
        n=(min+max)//2
    elif(m=='lesser'):
        max=n
        n=(min+max)//2
    else:
        print('yes')
    
