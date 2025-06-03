alien_0 = {'color':'green','points':5}
# print(alien_0)
# print(alien_0['color'])

alien_0['x-position'] = 0
alien_0['y-position'] = 25
# print(alien_0)

alien_0 = {} # empty dictionary
alien_0['color'] = 'green'
alien_0['points'] = 'green'
# print(alien_0)

alien_0['color'] = 'yellow' # overwrite value in key
# print(alien_0)

alien_0 = {'x_position':0, 'y_position':25, 'speed':'medium'}
# print(f'Original Position: {alien_0["x_position"]}')

if alien_0['speed'] == 'slow':
    x_increment = 1
elif alien_0['speed'] == 'medium':
    x_increment = 2
else:
    x_increment = 3

alien_0['x_position'] = alien_0['x_position'] + x_increment
# print(f'New Position: {alien_0["x_position"]}')

alien_0 = {'color':'green','points':5}
del alien_0['points']
# print(alien_0)

# print(alien_0['points']) # points no longer exists
# print(alien_0.get('points','No point value assigned'))

user_0 ={
    'username': 'efermi',
    'first':'enrico',
    'last':'fermi'
}

# for key,value in user_0.items():
#     print(f'\nKey: {key}')
#     print(f'Value: {value}')

# for k,v in user_0.items():
#     print(f'\nKey: {k}')
#     print(f'Value: {v}')

favorite_languages = {
    'jen': 'python',
    'sarah': 'c',
    'edward': 'rust',
    'phil': 'python'
}

# for n,l in favorite_languages.items():
    # print(f"{n.title()}'s favorite language is {l.title()}.")

# print(favorite_languages.keys())
# for name in favorite_languages.keys():
    # print(name.title())

# for language in sorted(favorite_languages.values()):
#     print(f'{language.title()}')

# for language in set(favorite_languages.values()): #set() pulls unique items in collection
#     print(f'\n{language.title()}')

# Using dictionaries in a loop
aliens = []

for alien_number in range(30):
    new_alien = {'color':'green','points':5,'speed':'slow'}
    aliens.append(new_alien)

for alien in aliens[:5]:
    if alien['color'] == 'green':
        alien['color'] = 'yellow'
        alien['points'] = 10
        alien['speed'] = 'medium'

# print(len(aliens))
# print(aliens[:3])

# Using a list in a dictionary
favorite_languages = {
    'jen': ['python','rust'],
    'sarah': ['c'],
    'edward': ['rust','go'],
    'phil': ['python','haskell']
}

# for name,languages in favorite_languages.items():
#     if len(languages) > 1:
#         print(f"\n{name.title()}'s favorite languages are:")
#     else:
#         print(f"\n{name.title()}'s favorite language is:")
#     for language in languages:
#         print(f'\t{language.title()}')

# Using a dictionary in a dictionary

users = {
    'aeinstein': {
        'first': 'albert',
        'last': 'einstein',
        'location': 'princeton'
    },

    'mcurie': {
        'first': 'marie',
        'last': 'curie',
        'location': 'paris'
    }
}

for username, user_info in users.items():
    print(f'\nUsername: {username}')
    full_name = f'{user_info['first']}{user_info['last']}'
    location = user_info['location']

    print(f'\tFull name: {full_name.title()}')
    print(f'\tLocation: {location.title()}')