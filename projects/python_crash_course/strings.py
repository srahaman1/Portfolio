### Strings
message = "Hello Python World!" # Set a variable
# print(message)

message = "Hello Python Crash Course" # Overwrite the variable
# print(message)

my_name = 'shoaib rahaman'
# print(my_name.title()) #transform to titlecase
# print(my_name.upper()) #transform to titlecase
# print(my_name.lower()) #transform to titlecase

first_name = 'shoaib'
last_name = 'rahaman'
full_name = f'{first_name} {last_name}' #use f string to combine name and store as variable
# print(full_name)
# print(full_name.title()) # Titlecase of varible containing f string
message = f'Hello {full_name.title()}!'
# print(message)

# print('\tPython') # adding \t at the beginning of the string tabs it
# print('\nPython') # adding \n at the beginning of the string adds a newline
# print('Subjects:\n\tMath\n\tHistory\n\tEnglish')

favorite_language = ' python '
# print(favorite_language.strip()) # strips whitespace
# print(favorite_language.rstrip()) # strips right side whitespace
# print(favorite_language.lstrip()) # strips left side whitespace
favorite_language = favorite_language.strip() # overwrite variable to make transformation permanent
# print(favorite_language)

url = 'https://rapid7.com'
simple_url = url.removeprefix('https://')
# print(simple_url)