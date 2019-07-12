import numpy as np

input_table_u = np.zeros((9,9)).astype(np.int8)
input_table_u.fill(0)
# print(input_table)

# input_line give the known values: the i-th list in it represents the i-th 3*3 block, in the sublist,
# first number is the index (1-9: left to right, up to down), second number is the corresponding value.
# test example
input_line = [[5,7,6,4,7,3],
              [4,2,5,8,9,7],
              [2,2,5,6,6,1],
              [1,1,5,4,9,5],
              [1,5,9,6],
              [1,7,5,9,9,3],
              [4,5,5,2,8,6],
              [1,8,5,3,6,4],
              [3,2,4,9,5,8]]
# second expert test example (hard to resolve)
# input_line = [[5,7,6,4,7,3],
#               [4,2,5,8,9,7],
#               [2,2,5,6,6,1],
#               [1,1,5,4,9,5],
#               [1,5,9,6],
#               [1,7,5,9,9,3],
#               [4,5,5,2,8,6],
#               [1,8,5,3,6,4],
#               [3,2,4,9,5,8]]
# an expert test example
# input_line = [[1,5,6,6,8,4,9,8],
#               [1,6,2,8,6,4,9,7],
#               [2,2,7,3],
#               [2,5,3,3,9,9],
#               [3,1,7,8],
#               [1,2,7,4,8,5],
#               [3,7,8,6],
#               [1,5,4,9,8,2,9,3],
#               [1,1,2,3,4,8,9,9]]
# a hard test example
# input_line = [[5,4,6,7,7,8,8,1,9,5],
#               [3,7,4,2],
#               [5,3,7,6,9,2],
#               [1,6,4,5,7,4],
#               [3,2,5,8,7,3],
#               [3,1,6,3,9,5],
#               [1,3,3,6,5,5],
#               [6,8,7,9],
#               [1,5,2,8,3,4,4,9,5,2]]
# a simple test example
# input_line = [[3,5,6,9,9,7],
#               [5,7,6,2,7,8,8,4,9,6],
#               [1,4,6,1,7,5,9,2],
#               [2,8,3,4],
#               [2,3,8,2],
#               [7,9,8,1],
#               [1,7,3,3,4,9,9,8],
#               [1,2,2,6,3,4,4,1,5,8],
#               [1,1,4,3,7,6]]
for i in range(9):
    index = [input_line[i][l] for l in range(len(input_line[i])) if l % 2 == 0 ]
    # print(index)
    value = [input_line[i][l] for l in range(len(input_line[i])) if l % 2 == 1 ]
    # print(value)
    for j,k in enumerate(index):
        # print(f"{((k-1) // 3) + (i // 3) * 3, ((k-1) % 3) + ((i % 3) * 3)}")
        input_table_u[((k-1) // 3) + (i // 3) * 3, ((k-1) % 3) + ((i % 3) * 3)] = value[j]
        # print(value[j])

# input table: unknown value is 0, known value is filled
input_table = input_table_u
# print(input_table)
# print(input_table[1,2])


