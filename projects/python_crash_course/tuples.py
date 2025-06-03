# Tuples are similar to lists but are immutable
# The contents cannot be changed/modified
bank_deposits = (200,20,50,100)
print(bank_deposits)
# bank_deposits[0]=250 #Overwriting the value give an error

for deposit in bank_deposits:
    print(deposit)