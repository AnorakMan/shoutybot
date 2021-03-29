print('hello')
clientList=[]

clientList.append('first')
clientList.append('second')

item2 = 'third'

if (item2 not in clientList):
    clientList.append(item2)

print(clientList)