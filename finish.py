# python code to solve shudu game

from config import input_table
import numpy as np
from copy import deepcopy
from itertools import product
import time
import multiprocessing

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

def wrong(value_table):
    for i in range(9):
        if len(set(value_table[i])) != 9:
            return True
        if len(set(value_table[:,i])) != 9:
            return True
        bi = i
        r_range = range((bi // 3) * 3, (bi // 3) * 3 + 3)
        # c_range_start = (bi % 3) * 3
        c_range = range((bi % 3) * 3, (bi % 3) * 3 + 3)
        block_i = value_table[r_range[0]:r_range[0]+3, c_range[0]:c_range[0]+3].reshape((-1,))
        if len(set(block_i)) != 9:
            return True
    return False

def check(start, element_list):
    element_list_np = np.array(element_list)
    try_value_table = element_list_np.reshape((9, 9))
    if not wrong(try_value_table):
        print(f"finish table:\n {try_value_table}")
        end = time.time()
        print(f"finish time:\n {end - start}")
    del try_value_table



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
    # print(set_table)

    while True:
        if not terminate(value_table):
            # update set_table in simple way, i.e. not try one element in a multi-set
            set_table_next = new_set_table(value_table, set_table)
            print(f"set_table_next:\n {set_table_next}")

            #update value_table
            value_table_next = new_value_table(set_table_next)
            print(f"value_table_next:\n {value_table_next}")
            # print(f"now value_table:\n {value_table}")
            if np.all(value_table == value_table_next):
                print(f"terminate_bug_table:\n {value_table}")
                break

            set_table = set_table_next
            value_table = value_table_next
            del set_table_next
            del value_table_next
        else:
            break

    # now try all possible cases, if not wrong, terminate right
    # pool = multiprocessing.Pool(processes=1)
    for element_list in product(*list(set_table.reshape((-1,)))):
        # pool.apply_async(check, (start, element_list))
        check(start, element_list)
    # pool.close()
    # pool.join()

    end_last = time.time()
    print(f"last finish time:\n {end_last - start}")



