fruits = ['apple','pear','banana','pen']
# print(fruits)
# print(fruits[1]) # indexing - returns item in that position in the list, python starts counting at 0
# print(fruits[0])
# print(fruits[0].title()) #string manipulation can work here
# print(fruits[-1]) #python allows for negative retrieval, starting from back of list
# print(fruits[-5]) # but it must be within list range

message = f'I have a {fruits[-1].title()}. I have a {fruits[0].title()}. {fruits[-1].title()}{fruits[0].title()}. {fruits[0].title()}{fruits[-1].title()}.'
# print(message)

### Modifying a list
cars = ['toyota', 'honda', 'subaru']
# print(cars)
# cars[2] = 'fiat' # overwrite value in list
# print(cars)

cars.append('fiat') # adds to end of list
# print(cars)

cars = [] #lists can start empty
# print(cars)
cars.append('toyota')
cars.append('honda')
cars.append('subaru')
# print(cars) 

cars.insert(3,'fiat') # inserts at given position
# print(cars)

# del cars[0] # delete item in list based on position
# print(cars)

# non_jp_cars = cars.pop() #pop removes last item in list
# print(cars)
# print(non_jp_cars)

first_car = cars.pop(0)
# print(f'My first car ever was a {first_car.title()}.')

cars.sort() # permanent sort - alphabetic order
# print(cars)
cars.sort(reverse=True) # permanent sort - reverse alphabetic order
# print(cars)

# print(sorted(cars)) # temp sort - alphabetic order
# print(sorted(cars,reverse=True)) # temp sort - reverse alphabetic order

cars.reverse() # reverses the order of the list
# print(cars) 

print(len(cars))