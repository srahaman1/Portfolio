# message = input('Type something to echo: ')
# print(message)

# name = input('please enter name: ')
# print(f'\nHello, {name.title()}')

prompt = 'Welcome to Hongdae!'
prompt += '\nTell me, are you "open-minded" ?'

# answer = input(prompt)

# age =  input('How old are you? ')
# age = int(age) # inputs are strings, so they must be converted according to the functional datatype

# height = input('How tall are you, in inches? ')
# height = int(height)

# if height >= 48:
    # print("\nYou're tall enough to ride!")
# else:
    # print('\nSorry, you must be at least 48 inches tall to ride.')

# print(4%2)
# print(834%23)
# print(900%13)

number = input("enter a number to check if odd or even: ")
number =  int(number)

if number % 2 == 0:
    print(f'\nThe number {number} is even.')
else:
    print(f'\nThe number {number} is odd.')