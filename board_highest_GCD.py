import math 
from itertools import permutations
import time
from datetime import datetime
import json
import tqdm
from collections import Counter


with open("boards_with_gcds_9.json", "r") as file:
    completed_boards = json.load(file)


# find max gcd 
max_gcd = 0
for i in range(len(completed_boards)):
    gcd = int(completed_boards[i]['gcd'])
    if gcd > max_gcd:
        max_gcd = gcd
        max_gcd_index = i
        
max_boards = []
for i in range(len(completed_boards)):
    gcd = int(completed_boards[i]['gcd'])
    if gcd == max_gcd:
        max_boards.append(i)
        
print(max_boards)

print(len(completed_boards))
max_board = completed_boards[26]['board']

for i in range(9):
    print(max_board[i][:])