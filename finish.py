# python code to solve shudu game

from config import input_table
import numpy as np
from copy import deepcopy
from itertools import product
import time
import sys

def new_set_table(value_table, set_table):
    set_table_next = deepcopy(set_table)
    block_table = np.array([set()] * 9)

    # same row and same column, no repeated element
    for i in range(9):
        for j in range(9):
            value = value_table[i,j]
            if value != 0:
                block_index = (i // 3) * 3 + j // 3
                block_table[block_index] = block_table[block_index] | {value_table[i,j]}
                for k in range(9):
                    if k != j:
                        set_table_next[i,k] = set_table_next[i,k] - {value_table[i,j]}
                    if k != i:
                        set_table_next[k,j] = set_table_next[k,j] - {value_table[i,j]}

    # same 3*3 block, no repeated element
    for si in range(9):
        for sj in range(9):
            if value_table[si,sj] == 0:
                block_index = (si // 3) * 3 + sj // 3  # block_index in 0-8, left-up to right-down order
                set_table_next[si, sj] = set_table_next[si, sj] - block_table[block_index]

    # same row, must have one element in 1-9
    for ri in range(9):
        row_i = set_table_next[ri]
        for num in range(1,10):
            arg_num = [num in aset for aset in row_i]
            if arg_num.count(True)==1:
                index_num = arg_num.index(True)
                set_table_next[ri, index_num] = {num}

    # same column, must have one element in 1-9
    for ci in range(9):
        col_i = set_table_next[:, ci]
        for num in range(1,10):
            arg_num = [num in aset for aset in col_i]
            if arg_num.count(True)==1:
                index_num = arg_num.index(True)
                set_table_next[index_num, ci] = {num}

    # same 3*3 block, must have one elment in 1-9
    for bi in range(9):
        # r_range_start = (bi // 3) * 3
        r_range = range((bi // 3) * 3, (bi // 3) * 3 + 3)
        # c_range_start = (bi % 3) * 3
        c_range = range((bi % 3) * 3, (bi % 3) * 3 + 3)
        block_i = set_table_next[r_range[0]:r_range[0]+3, c_range[0]:c_range[0]+3].reshape((-1,))
        for num in range(1,10):
            arg_num = [num in aset for aset in block_i]
            if arg_num.count(True)==1:
                index_num = arg_num.index(True)
                r_range_add = index_num // 3
                c_range_add = index_num % 3
                r_num = r_range[0] + r_range_add
                c_num = c_range[0] + c_range_add
                set_table_next[r_num, c_num] = {num}

    return set_table_next

def new_value_table(set_table):
    value_table_next = np.zeros((9, 9)).astype(np.int8)
    for i in range(9):
        for j in range(9):
            if len(set_table[i,j]) == 1:
                value_table_next[i,j] = list(set_table[i,j])[0]
    return value_table_next

def terminate(value_table):
    if 0 in np.unique(value_table):
        return False
    return True

def wrong_value(value_table):
    for i in range(9):
        if not len(set(value_table[i])-{0}) == 0 \
                and len(set(value_table[i])-{0}) != list((value_table[i] != 0).reshape((-1,))).count(True):
            return True
        if not len(set(value_table[:,i])-{0}) == 0 \
                and len(set(value_table[:,i]) - {0}) != list((value_table[:,i] != 0).reshape((-1,))).count(True):
            return True
        bi = i
        r_range = range((bi // 3) * 3, (bi // 3) * 3 + 3)
        # c_range_start = (bi % 3) * 3
        c_range = range((bi % 3) * 3, (bi % 3) * 3 + 3)
        block_i = value_table[r_range[0]:r_range[0]+3, c_range[0]:c_range[0]+3].reshape((-1,))
        if not len(set(block_i) - {0}) == 0 \
                and len(set(block_i) - {0}) != list((block_i != 0).reshape((-1,))).count(True):
            return True
    return False

def wrong_set(set_table):
    if set() in np.unique(set_table):
        return True
    else:
        return False

def try_mode(set_table, value_table, start):
    row, column = find_try_position(set_table, value_table)
    try_set = set_table[row, column]
    for value in try_set:
        try_set_table = deepcopy(set_table)
        try_value_table = deepcopy(value_table)
        try_set_table[row, column] = {value}
        try_value_table[row, column] = value
        while True:
            if not terminate(try_value_table):
                try_set_table_next = new_set_table(try_value_table, try_set_table)
                if wrong_set(try_set_table_next):
                    break

                #update value_table
                try_value_table_next = new_value_table(try_set_table_next)
                if wrong_value(try_value_table_next):
                    break

                if np.all(try_value_table == try_value_table_next):
                    try_mode(try_set_table_next, try_value_table_next, start)
                    break

                try_set_table = try_set_table_next
                try_value_table = try_value_table_next
                del try_set_table_next
                del try_value_table_next
            else:
                print(f"finish table:\n {try_value_table}")
                if not wrong_value(try_value_table):
                    print("check result: True")
                end_last = time.time()
                print(f"last finish time: {end_last - start}")
                sys.exit(0)

def find_try_position(set_table, value_table):
    rows_columns = np.where(value_table==0)
    set_table_multi = set_table[rows_columns]
    len_list = [len(set_) for set_ in set_table_multi]
    min_index = len_list.index(min(len_list))
    row, column = rows_columns[0][min_index], rows_columns[1][min_index]
    return row, column

if __name__ == "__main__":
    start = time.time()
    print(f"input_table:\n {input_table}")

    # initialize value_table
    value_table = input_table

    #initialize set_table
    set_table = np.array([[set()] * 9] * 9)
    for i in range(9):
        for j in range(9):
            if value_table[i, j] == 0:
                set_table[i, j] = {i + 1 for i in range(9)}
            else:
                set_table[i, j] = {value_table[i, j]}

    while True:
        if not terminate(value_table):
            # update set_table in simple way, i.e. not try one element in a multi-set
            set_table_next = new_set_table(value_table, set_table)

            #update value_table
            value_table_next = new_value_table(set_table_next)

            if np.all(value_table == value_table_next):
                try_mode(set_table_next, value_table_next, start)
                break

            set_table = set_table_next
            value_table = value_table_next
            del set_table_next
            del value_table_next
        else:
            print(f"finish table:\n {value_table}")
            if not wrong_value(value_table):
                print("check result: True")
            end_last = time.time()
            print(f"last finish time: {end_last - start}")
            sys.exit(0)






