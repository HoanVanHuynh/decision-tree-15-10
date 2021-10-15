
# Python continue statement 
# The continue statement is used to skip the rest of the code inside a loop
# for the current iteration only. 
# Loop does not terminate but continues on with the next iteration. 

# for var in sequence:
#     # codes inside for loop
#     if condition:
#         continue 
#     # codes inside for loop 
# # codes outside for loop 

i = 0
for var in 'string':
    i += 1
    print('i: ', i)
    if var == 'i':
        continue
    print(var) 

print('The end')