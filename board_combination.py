import json
import math 
from itertools import permutations
import time
from datetime import datetime
import tqdm



def find_gcd_all(n):
    def find_gcd(x, y):
        while(y):
            x, y = y, x % y

        return x
    
    gcd = find_gcd(n[0], n[1])
    for i in range(2, len(n)):
        gcd = find_gcd(gcd, n[i])
    
    return gcd


def set_first_row(board):
    entries = list(range(9))  # Original digits 0–8
    all_valid_permutations = []

    # Replace digits, ensuring 2, 0, and 5 are not replaced
    for i in range(9):  # 9 positions for substitution
        if i in [2, 0, 5]:  # Skip positions corresponding to 2, 0, or 5
            continue
        modified_entries = entries[:]
        modified_entries[i] = 9  # Replace the i-th digit with 9

        # Generate all permutations of the modified set
        all_permutations = permutations(modified_entries)

        # Apply constraints
        valid_permutations = [
            list(perm) for perm in all_permutations
            if perm[-2] == 2 and  # Second-to-last entry is 2
               perm[2] != 0 and perm[2] != 2 and  # Third entry is not 0 or 2
               perm[4] != 0 and  # Fifth entry is not 0
               perm[6] != 5 and  # Seventh entry is not 5
               perm[-1] != 5  # Last entry is not 5
        ]

        all_valid_permutations.extend(valid_permutations)  # Add to the overall list

    # Modify the first row of the board with each valid permutation
    for i in range(len(all_valid_permutations)):
        all_valid_permutations[i] = [[str(perm) for perm in all_valid_permutations[i]]] + board[1:]

    return all_valid_permutations


def set_second_row(boards):
    all_boards_with_gcd = []

    for board in tqdm.tqdm(boards):
        # Get the unique values from the first row
        unique_values = set(map(int, board[0]))
        unique_values = list(unique_values)  # Convert to list for permutation generation

        # Generate permutations using the unique values of the first row
        all_permutations = permutations(unique_values)

        # Apply constraints for the second row
        valid_permutations = [
            list(perm) for perm in all_permutations
            if perm[-1] == 5 and  # Last entry is 5
               perm[4] == 2 and  # Fifth entry is 2
               perm[0] not in map(int, board[0][:3]) and  # First column conflicts
               perm[1] not in map(int, board[0][:3]) and  # Second column conflicts
               perm[2] not in map(int, board[0][:3]) and perm[2] != 0 and  # Third column conflicts
               perm[3] not in map(int, board[0][3:6]) and  # Fourth column conflicts
               perm[5] not in map(int, board[0][3:6]) and  # Sixth column conflicts
               perm[6] not in map(int, board[0][6:]) and  # Seventh column conflicts
               perm[7] not in map(int, board[0][6:])  # Eighth column conflicts
        ]

        # Assemble new boards and calculate GCD
        for valid_perm in valid_permutations:
            new_board = [board[0]] + [valid_perm] + board[2:]
            # Convert the first two rows into integers for GCD calculation
            row_integers = [
                int(''.join(map(str, row))) for row in new_board[:2]
            ]
            gcd_value = find_gcd_all(row_integers)
            if gcd_value >= 1000:
                all_boards_with_gcd.append((new_board, gcd_value))

    return all_boards_with_gcd


initial_board = [
    [".",".",".",".",".",".",".","2","."],
    [".",".",".",".","2",".",".",".","5"],
    [".","2",".",".",".",".",".",".","."],
    [".",".","0",".",".",".",".",".","."],
    [".",".",".",".",".",".",".",".","."],
    [".",".",".","2",".",".",".",".","."],
    [".",".",".",".","0",".",".",".","."],
    [".",".",".",".",".","2",".",".","."],
    [".",".",".",".",".",".","5",".","."]
]


boards = set_first_row(initial_board)
data_to_save = []
for board in tqdm.tqdm(boards):
    data_to_save.append(board)


# Save data to a file
with open("boards_with_gcds1.json", "w") as file:
    json.dump(data_to_save, file, indent=4)

with open("boards_with_gcds1.json", "r") as file:
    boards = json.load(file)

all_boards = set_second_row(boards)

data_to_save = []
for board, gcd in tqdm.tqdm(all_boards):
    data_to_save.append({
        "board": board,  # Nested list representing the board
        "gcd": gcd       # Associated GCD
    })


# Save data to a file
with open("boards_with_gcds2.json", "w") as file:
    json.dump(data_to_save, file, indent=4)


with open("boards_with_gcds2.json", "r") as file:
    loaded_data = json.load(file)


def convert_to_strings(data):
    if isinstance(data, list):
        return [convert_to_strings(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_to_strings(value) for key, value in data.items()}
    else:
        return str(data)  # Convert the element to a string

loaded_data = convert_to_strings(loaded_data)


# find max gcd 
max_gcd = 0
for i in range(len(loaded_data)):
    gcd = int(loaded_data[i]['gcd'])
    if gcd > max_gcd:
        max_gcd = gcd
        max_gcd_index = i
        

reduced_boards = []
for i in range(len(loaded_data)):
    if int(loaded_data[i]['gcd']) >= 1000:
        reduced_boards.append(loaded_data[i]['board'])
        


def set_third_row(boards):
    all_boards_with_gcd = []

    for board in tqdm.tqdm(boards):
        # Get the unique values from the first two rows
        unique_values = set(map(int, board[0]))
        unique_values = list(unique_values)  # Convert to list for permutation generation

        # Generate permutations using the unique values of the first two rows
        all_permutations = permutations(unique_values)

        # Apply constraints for the third row
        valid_permutations = [
            list(perm) for perm in all_permutations
            if perm[0] not in [int(board[0][0]), int(board[1][0]), int(board[0][1]), int(board[1][1]), int(board[0][2]), int(board[1][2])] and  # First column conflicts
               perm[1] == 2 and  # Second column conflicts
               perm[2] not in [int(board[0][0]), int(board[1][0]), int(board[0][1]), int(board[1][1]), int(board[0][2]), int(board[1][2])] and 
               perm[3] not in [int(board[0][3]), int(board[1][3]), int(board[0][4]), int(board[1][4]), int(board[0][5]), int(board[1][5])] and  # Fourth column conflicts
               perm[4] not in [int(board[0][3]), int(board[1][3]), int(board[0][4]), int(board[1][4]), int(board[0][5]), int(board[1][5])] and  # Fifth column conflicts
               perm[5] not in [int(board[0][3]), int(board[1][3]), int(board[0][4]), int(board[1][4]), int(board[0][5]), int(board[1][5])] and  # Sixth column conflicts
               perm[6] not in [int(board[0][6]), int(board[1][6]), int(board[0][7]), int(board[1][7]), int(board[0][8]), int(board[1][8])] and  # Seventh column conflicts
               perm[7] not in [int(board[0][6]), int(board[1][6]), int(board[0][7]), int(board[1][7]), int(board[0][8]), int(board[1][8])] and  # Eighth column conflicts
               perm[8] not in [int(board[0][6]), int(board[1][6]), int(board[0][7]), int(board[1][7]), int(board[0][8]), int(board[1][8])]  # Ninth column conflicts
        ]

        # Assemble new boards and calculate GCD
        for valid_perm in valid_permutations:
            new_board = board[:2] + [[str(perm) for perm in valid_perm]] + board[3:]
            # Convert the first three rows into integers for GCD calculation
            row_integers = [int(''.join(map(str, row))) for row in new_board[:3]]
            gcd_value = find_gcd_all(row_integers)
            if gcd_value >= 1000:
                all_boards_with_gcd.append((new_board, gcd_value))

    return all_boards_with_gcd


third_row_boards = set_third_row(reduced_boards)

data_to_save = []
for board, gcd in tqdm.tqdm(third_row_boards):
    data_to_save.append({
        "board": board,  # Nested list representing the board
        "gcd": gcd       # Associated GCD
    })


# Save data to a file
with open("boards_with_gcds_32.json", "w") as file:
    json.dump(data_to_save, file, indent=4)



def set_fourth_row(boards):
    all_boards_with_gcd = []

    for board in tqdm.tqdm(boards):
        # Get the unique values from the first two rows
        unique_values = set(map(int, board[0]))
        unique_values = list(unique_values)  # Convert to list for permutation generation

        # Generate permutations using the unique values of the first two rows
        all_permutations = permutations(unique_values)

        # Apply constraints for the third row
        valid_permutations = [
            list(perm) for perm in all_permutations
            if perm[0] not in [int(board[0][0]), int(board[1][0]), int(board[2][0])] and  # First column conflicts
               perm[1] not in [int(board[0][1]), int(board[1][1]), int(board[2][1])] and  # Second column conflicts
               perm[2] == 0 and 
               perm[3] not in [int(board[0][3]), int(board[1][3]), int(board[2][3])] and  # Fourth column conflicts
               perm[4] not in [int(board[0][4]), int(board[1][4]), int(board[2][4])] and  # Fifth column conflicts
               perm[5] not in [int(board[0][5]), int(board[1][5]), int(board[2][5])] and  # Sixth column conflicts
               perm[6] not in [int(board[0][6]), int(board[1][6]), int(board[2][6])] and  # Seventh column conflicts
               perm[7] not in [int(board[0][7]), int(board[1][7]), int(board[2][7])] and  # Eighth column conflicts
               perm[8] not in [int(board[0][8]), int(board[1][8]), int(board[2][8])] # Ninth column conflicts
        ]

        # Assemble new boards and calculate GCD
        for valid_perm in valid_permutations:
            new_board = board[:3] + [[str(perm) for perm in valid_perm]] + board[4:]
            # Convert the first three rows into integers for GCD calculation
            row_integers = [int(''.join(map(str, row))) for row in new_board[:4]]
            gcd_value = find_gcd_all(row_integers)
            if gcd_value >= 100:
                all_boards_with_gcd.append((new_board, gcd_value))

    return all_boards_with_gcd


with open("boards_with_gcds_3.json", "r") as file:
    third_row_boards = json.load(file)



reduced_boards = []
for i in range(len(third_row_boards)):
    if int(third_row_boards[i]['gcd']) >= 100:
        reduced_boards.append(third_row_boards[i]['board'])


fourth_row_boards = set_fourth_row(reduced_boards)

data_to_save = []
for board, gcd in tqdm.tqdm(fourth_row_boards):
    data_to_save.append({
        "board": board,  # Nested list representing the board
        "gcd": gcd       # Associated GCD
    })


# Save data to a file
with open("boards_with_gcds_4.json", "w") as file:
    json.dump(data_to_save, file, indent=4)



def set_fifth_row(boards):
    all_boards_with_gcd = []

    for board in tqdm.tqdm(boards):
        # Get the unique values from the first two rows
        unique_values = set(map(int, board[0]))
        unique_values = list(unique_values)  # Convert to list for permutation generation

        # Generate permutations using the unique values of the first two rows
        all_permutations = permutations(unique_values)

        # Apply constraints for the third row
        valid_permutations = [
            list(perm) for perm in all_permutations
            if perm[0] not in [int(board[0][0]), int(board[1][0]), int(board[2][0]), int(board[3][0]), int(board[3][1]), int(board[3][2])] and  # First column conflicts
               perm[1] not in [int(board[0][1]), int(board[1][1]), int(board[2][1]), int(board[3][1]), int(board[3][0]), int(board[3][2])] and  # Second column conflicts
               perm[2] not in [int(board[0][2]), int(board[1][2]), int(board[2][2]), int(board[3][2]), int(board[3][1]), int(board[3][0])] and 
               perm[3] not in [int(board[0][3]), int(board[1][3]), int(board[2][3]), int(board[3][3]), int(board[3][4]), int(board[3][5])] and  # Fourth column conflicts
               perm[4] not in [int(board[0][4]), int(board[1][4]), int(board[2][4]), int(board[3][4]), int(board[3][3]), int(board[3][5])] and  # Fifth column conflicts
               perm[5] not in [int(board[0][5]), int(board[1][5]), int(board[2][5]), int(board[3][5]), int(board[3][4]), int(board[3][3])] and  # Sixth column conflicts
               perm[6] not in [int(board[0][6]), int(board[1][6]), int(board[2][6]), int(board[3][6]), int(board[3][7]), int(board[3][8])] and  # Seventh column conflicts
               perm[7] not in [int(board[0][7]), int(board[1][7]), int(board[2][7]), int(board[3][7]), int(board[3][6]), int(board[3][8])] and  # Eighth column conflicts
               perm[8] not in [int(board[0][8]), int(board[1][8]), int(board[2][8]), int(board[3][8]), int(board[3][7]), int(board[3][6])] # Ninth column conflicts
        ]

        # Assemble new boards and calculate GCD
        for valid_perm in valid_permutations:
            new_board = board[:4] + [[str(perm) for perm in valid_perm]] + board[5:]
            # Convert the first three rows into integers for GCD calculation
            row_integers = [int(''.join(map(str, row))) for row in new_board[:5]]
            gcd_value = find_gcd_all(row_integers)
            if gcd_value >= 100:
                all_boards_with_gcd.append((new_board, gcd_value))

    return all_boards_with_gcd

with open("boards_with_gcds_4.json", "r") as file:
    fourth_row_boards = json.load(file)

reduced_boards = []
for i in range(len(fourth_row_boards)):
    if int(fourth_row_boards[i]['gcd']) >= 1000:
        reduced_boards.append(fourth_row_boards[i]['board'])

fifth_row_boards = set_fifth_row(reduced_boards)

data_to_save = []
for board, gcd in tqdm.tqdm(fifth_row_boards):
    data_to_save.append({
        "board": board,  # Nested list representing the board
        "gcd": gcd       # Associated GCD
    })


# Save data to a file
with open("boards_with_gcds_5.json", "w") as file:
    json.dump(data_to_save, file, indent=4)



with open("boards_with_gcds_5.json", "r") as file:
    fifth_row_boards = json.load(file)


def set_sixth_row(boards):
    all_boards_with_gcd = []

    for board in tqdm.tqdm(boards):
        # Get the unique values from the first two rows
        unique_values = set(map(int, board[0]))
        unique_values = list(unique_values)  # Convert to list for permutation generation

        # Generate permutations using the unique values of the first two rows
        all_permutations = permutations(unique_values)

        # Apply constraints for the third row
        valid_permutations = [
            list(perm) for perm in all_permutations
            if perm[0] not in [int(board[3][0]), int(board[3][1]), int(board[3][2]), int(board[4][0]), int(board[4][1]), int(board[4][2]), int(board[0][0]), int(board[1][0]), int(board[2][0]), int(board[3][0]), int(board[4][0])] and  # First column conflicts
               perm[1] not in [int(board[3][0]), int(board[3][1]), int(board[3][2]), int(board[4][0]), int(board[4][1]), int(board[4][2]), int(board[0][1]), int(board[1][1]), int(board[2][1]), int(board[3][1]), int(board[4][1])] and  # Second column conflicts
               perm[2] not in [int(board[3][0]), int(board[3][1]), int(board[3][2]), int(board[4][0]), int(board[4][1]), int(board[4][2]), int(board[0][2]), int(board[1][2]), int(board[2][2]), int(board[3][2]), int(board[4][2])] and 
               perm[3] == 2 and  # Fourth column conflicts
               perm[4] not in [int(board[3][3]), int(board[3][4]), int(board[3][5]), int(board[4][3]), int(board[4][4]), int(board[4][5]), int(board[0][4]), int(board[1][4]), int(board[2][4]), int(board[3][4]), int(board[4][4])] and  # Fifth column conflicts
               perm[5] not in [int(board[3][3]), int(board[3][4]), int(board[3][5]), int(board[4][3]), int(board[4][4]), int(board[4][5]), int(board[0][5]), int(board[1][5]), int(board[2][5]), int(board[3][5]), int(board[4][5])] and  # Sixth column conflicts
               perm[6] not in [int(board[3][6]), int(board[3][7]), int(board[3][8]), int(board[4][6]), int(board[4][7]), int(board[4][8]), int(board[0][6]), int(board[1][6]), int(board[2][6]), int(board[3][6]), int(board[4][6])] and  # Seventh column conflicts
               perm[7] not in [int(board[3][6]), int(board[3][7]), int(board[3][8]), int(board[4][6]), int(board[4][7]), int(board[4][8]), int(board[0][7]), int(board[1][7]), int(board[2][7]), int(board[3][7]), int(board[4][7])] and  # Eighth column conflicts
               perm[8] not in [int(board[3][6]), int(board[3][7]), int(board[3][8]), int(board[4][6]), int(board[4][7]), int(board[4][8]), int(board[0][8]), int(board[1][8]), int(board[2][8]), int(board[3][8]), int(board[4][8])] # Ninth column conflicts
        ]

        # Assemble new boards and calculate GCD
        for valid_perm in valid_permutations:
            new_board = board[:5] + [[str(perm) for perm in valid_perm]] + board[6:]
            # Convert the first three rows into integers for GCD calculation
            row_integers = [int(''.join(map(str, row))) for row in new_board[:6]]
            gcd_value = find_gcd_all(row_integers)
            if gcd_value >= 100:
                all_boards_with_gcd.append((new_board, gcd_value))

    return all_boards_with_gcd


reduced_boards = []
for i in range(len(fifth_row_boards)):
    if int(fifth_row_boards[i]['gcd']) >= 100:
        reduced_boards.append(fifth_row_boards[i]['board'])

sixth_row_boards = set_sixth_row(reduced_boards)

data_to_save = []
for board, gcd in tqdm.tqdm(sixth_row_boards):
    data_to_save.append({
        "board": board,  # Nested list representing the board
        "gcd": gcd       # Associated GCD
    })


# Save data to a file
with open("boards_with_gcds_6.json", "w") as file:
    json.dump(data_to_save, file, indent=4)
    

    
with open("boards_with_gcds_6.json", "r") as file:
    sixth_row_boards = json.load(file)


def set_seventh_row(boards):
    all_boards_with_gcd = []

    for board in tqdm.tqdm(boards):
        # Get the unique values from the first two rows
        unique_values = set(map(int, board[0]))
        unique_values = list(unique_values)  # Convert to list for permutation generation

        # Generate permutations using the unique values of the first two rows
        all_permutations = permutations(unique_values)

        # Apply constraints for the third row
        valid_permutations = [
            list(perm) for perm in all_permutations
            if perm[0] not in [int(board[0][0]), int(board[1][0]), int(board[2][0]), int(board[3][0]), int(board[4][0]), int(board[5][0])] and  # First column conflicts
               perm[1] not in [int(board[0][1]), int(board[1][1]), int(board[2][1]), int(board[3][1]), int(board[4][1]), int(board[5][1])] and  # Second column conflicts
               perm[2] not in [int(board[0][2]), int(board[1][2]), int(board[2][2]), int(board[3][2]), int(board[4][2]), int(board[5][2])] and 
               perm[3] not in [int(board[0][3]), int(board[1][3]), int(board[2][3]), int(board[3][3]), int(board[4][3]), int(board[5][3])] and  # Fourth column conflicts
               perm[4] == 0 and  # Fifth column conflicts
               perm[5] not in [int(board[0][5]), int(board[1][5]), int(board[2][5]), int(board[3][5]), int(board[4][5]), int(board[5][5])] and  # Sixth column conflicts
               perm[6] not in [int(board[0][6]), int(board[1][6]), int(board[2][6]), int(board[3][6]), int(board[4][6]), int(board[5][6])] and  # Seventh column conflicts
               perm[7] not in [int(board[0][7]), int(board[1][7]), int(board[2][7]), int(board[3][7]), int(board[4][7]), int(board[5][7])] and  # Eighth column conflicts
               perm[8] not in [int(board[0][8]), int(board[1][8]), int(board[2][8]), int(board[3][8]), int(board[4][8]), int(board[5][8])] # Ninth column conflicts
        ]

        # Assemble new boards and calculate GCD
        for valid_perm in valid_permutations:
            new_board = board[:6] + [[str(perm) for perm in valid_perm]] + board[7:]
            # Convert the first three rows into integers for GCD calculation
            row_integers = [int(''.join(map(str, row))) for row in new_board[:7]]
            gcd_value = find_gcd_all(row_integers)
            if gcd_value >= 100:
                all_boards_with_gcd.append((new_board, gcd_value))

    return all_boards_with_gcd


reduced_boards = []
for i in range(len(sixth_row_boards)):
    if int(sixth_row_boards[i]['gcd']) >= 100:
        reduced_boards.append(sixth_row_boards[i]['board'])

seventh_row_boards = set_seventh_row(reduced_boards)

data_to_save = []
for board, gcd in tqdm.tqdm(seventh_row_boards):
    data_to_save.append({
        "board": board,  # Nested list representing the board
        "gcd": gcd       # Associated GCD
    })


# Save data to a file
with open("boards_with_gcds_7.json", "w") as file:
    json.dump(data_to_save, file, indent=4)
    

    
with open("boards_with_gcds_7.json", "r") as file:
    seventh_row_boards = json.load(file)


def set_eighth_row(boards):
    all_boards_with_gcd = []

    for board in tqdm.tqdm(boards):
        # Get the unique values from the first two rows
        unique_values = set(map(int, board[0]))
        unique_values = list(unique_values)  # Convert to list for permutation generation

        # Generate permutations using the unique values of the first two rows
        all_permutations = permutations(unique_values)

        # Apply constraints for the third row
        valid_permutations = [
            list(perm) for perm in all_permutations
            if perm[0] not in [int(board[6][0]), int(board[6][1]), int(board[6][2]), int(board[0][0]), int(board[1][0]), int(board[2][0]), int(board[3][0]), int(board[4][0]), int(board[5][0]), int(board[6][0])] and  # First column conflicts
               perm[1] not in [int(board[6][0]), int(board[6][1]), int(board[6][2]), int(board[0][1]), int(board[1][1]), int(board[2][1]), int(board[3][1]), int(board[4][1]), int(board[5][1]), int(board[6][1])] and  # Second column conflicts
               perm[2] not in [int(board[6][0]), int(board[6][1]), int(board[6][2]), int(board[0][2]), int(board[1][2]), int(board[2][2]), int(board[3][2]), int(board[4][2]), int(board[5][2]), int(board[6][2])] and 
               perm[3] not in [int(board[6][3]), int(board[6][4]), int(board[6][5]), int(board[0][3]), int(board[1][3]), int(board[2][3]), int(board[3][3]), int(board[4][3]), int(board[5][3]), int(board[6][3])] and  # Fourth column conflicts
               perm[4] not in [int(board[6][3]), int(board[6][4]), int(board[6][5]), int(board[0][4]), int(board[1][4]), int(board[2][4]), int(board[3][4]), int(board[4][4]), int(board[5][4]), int(board[6][4])] and   # Fifth column conflicts
               perm[5] == 2 and  # Sixth column conflicts
               perm[6] not in [int(board[6][6]), int(board[6][7]), int(board[6][8]), int(board[0][6]), int(board[1][6]), int(board[2][6]), int(board[3][6]), int(board[4][6]), int(board[5][6]), int(board[6][6])] and  # Seventh column conflicts
               perm[7] not in [int(board[6][6]), int(board[6][7]), int(board[6][8]), int(board[0][7]), int(board[1][7]), int(board[2][7]), int(board[3][7]), int(board[4][7]), int(board[5][7]), int(board[6][7])] and  # Eighth column conflicts
               perm[8] not in [int(board[6][6]), int(board[6][7]), int(board[6][8]), int(board[0][8]), int(board[1][8]), int(board[2][8]), int(board[3][8]), int(board[4][8]), int(board[5][8]), int(board[6][8])] # Ninth column conflicts
        ]

        # Assemble new boards and calculate GCD
        for valid_perm in valid_permutations:
            new_board = board[:7] + [[str(perm) for perm in valid_perm]] + board[8:]
            # Convert the first three rows into integers for GCD calculation
            row_integers = [int(''.join(map(str, row))) for row in new_board[:8]]
            gcd_value = find_gcd_all(row_integers)
            if gcd_value >= 111:
                all_boards_with_gcd.append((new_board, gcd_value))

    return all_boards_with_gcd


reduced_boards = []
for i in range(len(seventh_row_boards)):
    if int(seventh_row_boards[i]['gcd']) >= 10:
        reduced_boards.append(seventh_row_boards[i]['board'])

eighth_row_boards = set_eighth_row(reduced_boards)

data_to_save = []
for board, gcd in tqdm.tqdm(eighth_row_boards):
    data_to_save.append({
        "board": board,  # Nested list representing the board
        "gcd": gcd       # Associated GCD
    })


# Save data to a file
with open("boards_with_gcds_8.json", "w") as file:
    json.dump(data_to_save, file, indent=4)
    


with open("boards_with_gcds_8.json", "r") as file:
    eighth_row_boards = json.load(file)


def set_ninth_row(boards):
    all_boards_with_gcd = []

    for board in tqdm.tqdm(boards):
        # Get the unique values from the first two rows
        unique_values = set(map(int, board[0]))
        unique_values = list(unique_values)  # Convert to list for permutation generation

        # Generate permutations using the unique values of the first two rows
        all_permutations = permutations(unique_values)

        # Apply constraints for the third row
        valid_permutations = [
            list(perm) for perm in all_permutations
            if perm[0] not in [int(board[6][0]), int(board[6][1]), int(board[6][2]), int(board[7][0]), int(board[7][1]), int(board[7][2]), int(board[0][0]), int(board[1][0]), int(board[2][0]), int(board[3][0]), int(board[4][0]), int(board[5][0]), int(board[6][0])] and  # First column conflicts
               perm[1] not in [int(board[6][0]), int(board[6][1]), int(board[6][2]), int(board[7][0]), int(board[7][1]), int(board[7][2]), int(board[0][1]), int(board[1][1]), int(board[2][1]), int(board[3][1]), int(board[4][1]), int(board[5][1]), int(board[6][1])] and  # Second column conflicts
               perm[2] not in [int(board[6][0]), int(board[6][1]), int(board[6][2]), int(board[7][0]), int(board[7][1]), int(board[7][2]), int(board[0][2]), int(board[1][2]), int(board[2][2]), int(board[3][2]), int(board[4][2]), int(board[5][2]), int(board[6][2])] and 
               perm[3] not in [int(board[6][3]), int(board[6][4]), int(board[6][5]), int(board[7][3]), int(board[7][4]), int(board[7][5]), int(board[0][3]), int(board[1][3]), int(board[2][3]), int(board[3][3]), int(board[4][3]), int(board[5][3]), int(board[6][3])] and  # Fourth column conflicts
               perm[4] not in [int(board[6][3]), int(board[6][4]), int(board[6][5]), int(board[7][3]), int(board[7][4]), int(board[7][5]), int(board[0][4]), int(board[1][4]), int(board[2][4]), int(board[3][4]), int(board[4][4]), int(board[5][4]), int(board[6][4])] and   # Fifth column conflicts
               perm[5] not in [int(board[6][3]), int(board[6][4]), int(board[6][5]), int(board[7][3]), int(board[7][4]), int(board[7][5]), int(board[0][5]), int(board[1][5]), int(board[2][5]), int(board[3][5]), int(board[4][5]), int(board[5][5]), int(board[6][5])] and  # Sixth column conflicts
               perm[6] == 5 and  # Seventh column conflicts
               perm[7] not in [int(board[6][6]), int(board[6][7]), int(board[6][8]), int(board[7][6]), int(board[7][7]), int(board[7][8]), int(board[0][7]), int(board[1][7]), int(board[2][7]), int(board[3][7]), int(board[4][7]), int(board[5][7]), int(board[6][7])] and  # Eighth column conflicts
               perm[8] not in [int(board[6][6]), int(board[6][7]), int(board[6][8]), int(board[7][6]), int(board[7][7]), int(board[7][8]), int(board[0][8]), int(board[1][8]), int(board[2][8]), int(board[3][8]), int(board[4][8]), int(board[5][8]), int(board[6][8])] # Ninth column conflicts
        ]

        # Assemble new boards and calculate GCD
        for valid_perm in valid_permutations:
            new_board = board[:8] + [[str(perm) for perm in valid_perm]]
            # Convert the first three rows into integers for GCD calculation
            row_integers = [int(''.join(map(str, row))) for row in new_board]
            gcd_value = find_gcd_all(row_integers)
            if gcd_value >= 100:
                all_boards_with_gcd.append((new_board, gcd_value))

    return all_boards_with_gcd


reduced_boards = []
for i in range(len(eighth_row_boards)):
    if int(eighth_row_boards[i]['gcd']) >= 10:
        reduced_boards.append(eighth_row_boards[i]['board'])

ninth_row_boards = set_ninth_row(reduced_boards)

data_to_save = []
for board, gcd in tqdm.tqdm(ninth_row_boards):
    data_to_save.append({
        "board": board,  # Nested list representing the board
        "gcd": gcd       # Associated GCD
    })


# Save data to a file
with open("boards_with_gcds_9.json", "w") as file:
    json.dump(data_to_save, file, indent=4)
    