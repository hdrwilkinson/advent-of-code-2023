import re
from collections import defaultdict

def separate_data(data):
    """
    Splits the input data into lines, excluding the first and last lines, and processes each line.

    Args:
    data (str): A string containing multiple lines of data.

    Returns:
    list: A list of processed lines, where each line is prefixed and suffixed with a period.
    """
    lines = data.split('\n')
    return ['.' + line + '.' for line in lines]

''' Challenge 1 Code '''

def find_special_character_positions(data):
    """
    Finds the positions of special characters in the data and their surrounding positions.

    Args:
    data (list of str): A list of strings, each representing a line of data.

    Returns:
    dict: A dictionary with tuples (row, column) as keys, representing the positions surrounding special characters.
    """
    # Dictionary to hold the row:column for special character locations
    boundaries = {}
    # Regex to test for special characters
    pattern = re.compile('[^0-9.]') # pattern = ['#', '*', ..., '%']
    # Offset pairs for surrounding elements
    offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    # Iterating through each line
    for row, line in enumerate(data):
        # Iterating through each character
        for column, character in enumerate(line):
            # If character is a special character store position in a dictionary
            if pattern.match(character): # if character in pattern:
                # Add surrounding elements
                for row_offset, col_offset in offsets:
                    new_row, new_col = row + row_offset, column + col_offset
                    # You might want to check if new_row and new_col are within your desired bounds
                    boundaries[(new_row, new_col)] = 0
    return boundaries

def calculate_sum_of_numbers(data, boundaries):
    """
    Calculates the sum of numbers in the data that are near special characters.

    Args:
    data (list of str): A list of strings, each representing a line of data.
    boundaries (dict): A dictionary with keys as tuples (row, column) indicating positions near special characters.

    Returns:
    int: The total sum of numbers found near special characters.
    """
    # Counter for total
    total_count = 0
    # Iterating through each line
    for row, line in enumerate(data):
        # Setting empty string for number
        number = ''
        # List to hold row number positions
        number_positions = []
        # Bool for checking if number set to false initially
        is_number = False
        # Iterating through each character
        for column, character in enumerate(line):
            # If character is a number
            if character.isdigit():
                # Setting bool to true
                is_number = True
                # Increment number string
                number += character
                # Add position to number_poistions
                number_positions.append((row, column))
            # If not a number, but has last character was a number, then we have the end of a number string
            elif is_number:
                # Looping over number positions
                for position in number_positions:
                    # If the position is near a special character
                    if position in boundaries:
                        total_count += int(number)
                        break
                # Resetting
                is_number = False
                number = ''
                number_positions = []
    return total_count

''' Challenge 2 Code '''

def find_gears(data):
    """
    Identifies gears and their boundaries in the data.

    Args:
    data (list of str): A list of strings, each representing a line of data.

    Returns:
    tuple: A tuple containing two dictionaries, one for gears and one for their boundaries.
    """
    # Dictionary to hold the row:column for special character boundaries
    boundaries = {}
    # Dictionary to hold the row:column for special character locations
    gears = {}
    # Regex to test for special characters
    pattern = re.compile('[^0-9.]')
    # Offset pairs for surrounding elements
    offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    # ID for each unique gear
    gear_id = 0
    # Iterating through each line
    for row, line in enumerate(data):
        # Iterating through each character
        for column, character in enumerate(line):
            # If character is a special character store position in a dictionary
            if character == '*':
                # Add surrounding elements
                for row_offset, col_offset in offsets:
                    # Generate offsets
                    new_row, new_col = row + row_offset, column + col_offset
                    # Create position as element in special_character_boundaries dictionary
                    boundaries.setdefault((new_row, new_col), []).append(gear_id)
                # Add gear_id to special_characters dictionary and incrementing it
                gears[gear_id] = []
                gear_id += 1
    return gears, boundaries

def add_numbers_to_gears(data, gears, boundaries):
    """
    Adds numbers from the data to the corresponding gears based on their proximity to special characters.

    Args:
    data (list of str): A list of strings, each representing a line of data.
    gears (dict): A dictionary of gears identified in the data.
    boundaries (dict): A dictionary of boundaries around gears.

    Returns:
    dict: The updated gears dictionary with numbers added to each gear.
    """
    # Iterating through each line
    for row, line in enumerate(data):
        # Setting empty string for number
        number = ''
        # List to hold row number positions
        number_positions = []
        # Bool for checking if number set to false initially
        is_number = False
        # Iterating through each character
        for column, character in enumerate(line):
            # If character is a number
            if character.isdigit():
                # Setting bool to true
                is_number = True
                # Increment number string
                number += character
                # Add position to number_poistions
                number_positions.append((row, column))
            # If not a number, but has last character was a number, then we have the end of a number string
            elif is_number:
                used_gears = []
                # Looping over number positions
                for position in number_positions:
                    # If the position is near a special character
                    if position in boundaries:
                        # Add number to gear position list
                        gear_ids = boundaries[position]
                        # Loop through gear IDs stores in boundaries at this position
                        for gear_id in gear_ids:
                            # If gear_id not already used
                            if gear_id not in used_gears:
                                # Add number to gear
                                gears[gear_id].append(int(number))
                            # Add gear_id to used gears
                            used_gears.append(gear_id)
                # Resetting
                is_number = False
                number = ''
                number_positions = []
    return gears

def score_double_gears(gears):
    """
    Calculates the total score by multiplying pairs of numbers associated with each gear.

    Args:
    gears (dict): A dictionary containing gears and their associated numbers.

    Returns:
    int: The total score calculated by multiplying pairs of numbers for each gear.
    """
    total_count = 0
    for _, numbers in gears.items():
        if len(numbers) == 2:
              total_count += numbers[0] * numbers[1]
    return total_count

if __name__ == "__main__":
    # Loading the data
    with open('data.txt', 'r', encoding='utf-8') as file:
        string = file.read()

    # Dictionary for number conversion
    lines = separate_data(string)

    # Challenge 1 results
    boundaries = find_special_character_positions(lines)
    challenge_one_total = calculate_sum_of_numbers(lines, boundaries)

    # Challenge 2 results
    gears, boundaries = find_gears(lines)
    gears = add_numbers_to_gears(lines, gears, boundaries)
    challenge_two_total = score_double_gears(gears)

    # Printing results
    print(f"Challenge One Answer: {challenge_one_total}")
    print(f"Challenge Two Answer: {challenge_two_total}")