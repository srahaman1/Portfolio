# The Two Sum problem asks us to find two numbers in an array that
# sum up to a given target value. We need to return the **indices** of 
# these two numbers.

target = 7 # Set target
numbers = [value for value in range(1,5)] # Set list
not_found=True # This flag was created in case nothing in the array adds to the target
n = len(numbers) # Find the length of the array as this tells us the number of positions in the array

for i in range(n-1): # For each position in the array, offsetting the total number of positions by one bc python counts starts at 0
    # print(i)
    for j in range(i+1,n): # Offset i by 1 to get the accurate position to call in the array, limited by the length of the array
        if numbers[i] + numbers[j] == target: # Add the values of the two positions i and j, which are offset from each other by 1. For each i, add values i+1 (aka j).
            print([i,j])
            print(numbers[i],numbers[j], numbers[i] + numbers[j])
            not_found=False
if not_found == True:
    print('Not found')

'''
# Review

The question is layered, it is asking you to:
    1. Find pairs of numbers that add to the target
    2. Return the indices/positions of where the matching pairs
       in the array.

''' 
