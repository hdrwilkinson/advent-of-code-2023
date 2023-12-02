import math
from typing import Dict, Optional

def per_game_challenge_one(id: str, games_info_string: str, max_cubes: Dict[str, int]) -> int:
    """
    Calculates if a game challenge is possible based on the max number of cubes of each color.

    Args:
        id (str): The unique identifier of the game.
        games_info_string (str): String containing information about the game's cubes and their colors.
        max_cubes (Dict[str, int]): A dictionary mapping colors to the maximum number of cubes allowed.

    Returns:
        int: The id as an integer if the game is possible, otherwise 0.
    """
    # Splitting the info string into individual games
    games_info = games_info_string.split(";")
    # For loop through the individual games
    for game_info_string in games_info:
        # Splitting the individual game into it's colour information
        game_info = game_info_string.split(",")
        # Looping per cube
        for cube in game_info:
            # Separating via the number of cubes and their coloud
            _, num_cubes, colour = cube.split(' ')
            # Chacking (for the colour) the max number vs the proposed number
            if max_cubes[colour] < int(num_cubes):
                # If impossible, return 0
                return 0
    # Else, return the id
    return int(id)

def per_game_challenge_two(games_info_string: str) -> int:
    """
    Calculates the product of the maximum number of cubes of each color from game information.

    Args:
        games_info_string (str): String containing information about the game's cubes and their colors.

    Returns:
        int: The product of the maximum number of cubes of each color.
    """
    cube_maxes = {
        'red': 1,
        'green': 1,
        'blue': 1,
    }
    # Splitting the info string into individual games
    games_info = games_info_string.split(";")
    # For loop through the individual games
    for game_info_string in games_info:
        # Splitting the individual game into it's colour information
        game_info = game_info_string.split(",")
        # Looping per cube
        for cube in game_info:
            # Separating via the number of cubes and their coloud
            _, num_cubes, colour = cube.split(' ')
            # Checking (for the colour) the max number vs the proposed number
            if int(num_cubes) > cube_maxes[colour]:
                # If larger than the current max, replace it
                cube_maxes[colour] = int(num_cubes)
    # Returning the product of the max values
    return math.prod(cube_maxes.values())

def total_game_calculation(data: str, max_cubes: Optional[Dict[str, int]] = None) -> int:
    """
    Calculates the total score of all game challenges based on the provided data.

    Args:
        data (str): String containing multiple lines of game data.
        max_cubes (Optional[Dict[str, int]]): A dictionary mapping colors to the maximum number of cubes allowed.

    Returns:
        int: The total score calculated from all game challenges.
    """
    # Separating lines in string into list of lines
    lines = data.split("\n")
    # Setting total_count
    total_count = 0
    # Looping for each line
    for line in lines:
        # If line is empty, move to next line
        if line == '':
           continue
        # Separting the line information into round and game specific
        id_info, games_info_string = line.split(":")
        # Isolating the ID
        id = id_info[5:]
        if max_cubes is not None:
            # Return the ID if impossible, else returning 0
            round_total = per_game_challenge_one(id, games_info_string, max_cubes)
        else:
            # Return the product of the 
            round_total = per_game_challenge_two(games_info_string)
        # Adding to the total count
        total_count += round_total
    # Returning the total count
    return total_count

if __name__ == "__main__":
    # Loading the data
    with open('data.txt', 'r', encoding='utf-8') as file:
        string = file.read()

    # Dictionary for number conversion
    max_cubes = {
        'red': 12,
        'green': 13,
        'blue': 14,
    }

    # Gathering results
    challenge_one_total = total_game_calculation(string, max_cubes)
    challenge_two_total = total_game_calculation(string)

    # Printing results
    print(f"Challenge One Answer: {challenge_one_total}")
    print(f"Challenge Two Answer: {challenge_two_total}")