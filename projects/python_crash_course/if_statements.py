countries = ['canada','us','puerto rico']
# print('Unlimited talk and text in:')
# for country in countries:
#     if country == 'us':
#         print(country.upper())
#     else:
#         print(country.title())

country = 'canada'
# print(country == 'us')

# if country != 'puerto rico':
#     print('Press 1 for English')

bmi = 20
# if bmi == 20:
#     print('healthy')
# elif bmi > 20:
#     print('high bmi')
# else:
#     print('low bmi')

age_0 = 18
age_1 = 25
# if age_0 >= 18 and age_1 >= 25:
#     print(True)
# else:
#     print(False)

# if age_0 >= 18 or age_1 >= 25:
#     print(True)
# else:
#     print(False)

# print('us' in countries)
# print('mexico' not in countries)

# if 'Mexico' not in countries:
    # print(f'Country not covered under this plan')

# requested_toppings = ['mushrooms','chicken','buffalo sauce']
# for topping in requested_toppings:
#     print(f'Adding {topping}...')
# print('\nFinished making your pizza!')

# if 'mushrooms' in requested_toppings:
#     print('\nadding mushrooms...')
# if 'chicken' in requested_toppings:
#     print('adding chicken...')
# if 'buffalo sauce' in requested_toppings:
#     print('adding buffalo sauce...')
# if 'extra cheese' not in requested_toppings:
#     print('Would you like extra cheese?')

available_toppings = ['mushrooms', 'olives', 'green peppers', 'pineapple','extra cheese', 'chicken']
requested_toppings = ['pineapple','olives','chili oil']

for requested_topping in requested_toppings:
    if requested_topping in available_toppings:
        print(f'adding {requested_topping}')
    else:
        print(f"Sorry, we don't have {requested_topping}")
print('\nFinished making your pizza')