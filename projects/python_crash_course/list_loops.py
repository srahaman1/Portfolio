names = ['kevin','athena','mike','joe','steven','shoaib']

# for name in names:
    # print(name)
    # print(f'{name.title()} works on the CDATA team.\n')
# print(f'These are the members of the CDATA team')

# for value in range(1,6):
    # print(value)ß

numbers = list(range(1,6))
# print(numbers)
odd_numbers = list(range(1,6,2)) #the third variable is step size and offsets the counts by that ammount, default is 1: n1 + offset
# print(odd_numbers)

squares = []
for value in range(1, 11):
    square = value ** 2
    squares.append(square) #append each value into the list
# print(squares)

digits = []
for value in range(0,10): # 0-9
    digits.append(value)

# print(min(digits))
# print(max(digits))
# print(sum(digits))

squares = [value**2 for value in range(1,11)] # called list comprehension, the append is automated
# print(squares)

digits = [value for value in range(0,10)]
# print(digits[0:6])
# print(digits[:6])
# print(digits[6:])
# print(digits[-6])
# print(digits[:-6])
# print(digits[-6:])
# print(digits[0:10:2]) # a third digit in the index is an offset

# for peer in names[0:3]:  #loop through a slice
    # print(peer.title())

### Mini Check - Top Three Scores
scores = [value for value in range(90,101)]
# print(sorted(scores[-3:],reverse=True)) # Technically works bc list is pre-sorted from loop; won't work with random positions
# scores.sort(reverse=True)
# print(scores[:3]) # alternative method; sort first, then slice
 
my_flowers = ['sunflower','rose','lily','carnation']
friend_flowers = my_flowers[:]
# print(f'My favorite flowers are: {my_flowers}\nMy friend"s favorite flowers are: {friend_flowers}\n')
my_flowers.append('rododendrum')
friend_flowers.append("angel's breath")
# print(f'My favorite flowers are: {my_flowers}\nMy friend"s favorite flowers are: {friend_flowers}\n')
friend_flowers = my_flowers
# print(f'My favorite flowers are: {my_flowers}\nMy friend"s favorite flowers are: {friend_flowers}\n')