current_number = 0

# while current_number <= 5:
#     print(current_number)
#     current_number += 1

#while loops with inputs
prompt = "\n*Bawk* I'm Polly the Parrot! I repeat after you."
prompt += '\n*Bawk* What should I say?'
prompt += "\n Say quit it and I'll stop.\t"

message = ''
active = True
# while active:
#     message = input(prompt)
#     if message.lower() != 'quit it':
#         print(f'\n\t{message}')
#     else:
#         active = False

# break to exit loop
# while active:
#     message = input(prompt)

#     if message.lower() == 'quit it':
#         break
#     else:
#         print(f'\n\t{message}')

# continue in loops
current_number = 0
while current_number < 10:
    current_number += 1
    if current_number % 2 == 0:
        continue # continue tells python to ignore the rest of the loop and start from the beginning. Almost like a skip.
    print(current_number)

# While loops + Lists & Dictionaries
uncheckedin = ['alice','brian','candace']
checkedin = []

# while uncheckedin: # should be able to simulate queueing, first come, first serve
#     current_passenger = uncheckedin.pop()
#     print(f'Checking in Passenger: {current_passenger.title()}')
#     checkedin.append(current_passenger)
# print(f'\nThe following passengers have been checked in:')
# for passenger in checkedin:
#     print(f'\t{passenger.title()}')

