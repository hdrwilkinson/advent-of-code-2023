import math
from typing import List, Tuple

def parse_data_challenge_one(data: str) -> Tuple[List[int], List[int]]:
    """
    Parses the input data for Challenge 1 to extract time and distance information.

    Args:
        data (str): A string containing the puzzle input data.

    Returns:
        Tuple[List[int], List[int]]: 
        - A list of time values.
        - A list of distance values.
    """
    lines = data.split('\n')
    time_info = lines[0].split(':')[1].split()
    distance_info = lines[1].split(':')[1].split()
    time = [int(item) for item in time_info]
    distance = [int(item) for item in distance_info]

    return time, distance

def calculate_result_range(time: List[int], distance: List[int]) -> int:
    """
    Calculates the product of the ranges for each time and distance pair for Challenge 1.

    For each pair of time and distance, it finds the earliest and latest time
    at which the distance is less than the product of the time and its complement.
    The difference of these times plus one gives the range for each pair.

    Args:
        time (List[int]): A list of time values.
        distance (List[int]): A list of distance values.

    Returns:
        int: The product of the result ranges for each time and distance pair.
    """
    results = 1
    for i, t in enumerate(time):
        d = distance[i]
        result_range = []
        # Forwards pass to find the earliest time
        for j in range(1, t):
            if d < j * (t - j):
                result_range.append(j)
                break
        # Backwards pass to find the latest time
        for j in reversed(range(1, t)):
            if d < j * (t - j):
                result_range.append(j)
                break
        # Calculating the range and updating the overall result
        result = result_range[1] - result_range[0] + 1
        results *= result
    return results

def parse_data_challenge_two(data: str) -> Tuple[int, int]:
    """
    Parses the input data for Challenge 2 to extract a single time and distance value.

    Args:
        data (str): A string containing the puzzle input data.

    Returns:
        Tuple[int, int]:
        - A single time value.
        - A single distance value.
    """
    lines = data.split('\n')
    time = int(lines[0].split(':')[1].replace(' ', ''))
    distance = int(lines[1].split(':')[1].replace(' ', ''))

    return time, distance

def find_bounds(time: int, distance: int, left: bool = True) -> int:
    """
    Finds the bounds for a given time and distance for Challenge 2.

    This function uses a binary search approach to find the lower or upper bound
    at which the product of the time and its complement meets the distance criteria.

    Args:
        time (int): The time value.
        distance (int): The distance value.
        left (bool, optional): Flag to determine the direction of bound calculation. Defaults to True.

    Returns:
        int: The calculated bound based on the time and distance.
    """
    lower_bound = 0
    upper_bound = time
    while upper_bound - lower_bound > 1:
        pointer = (upper_bound + lower_bound) // 2
        this_distance = pointer * (time - pointer)
        if (this_distance > distance) == left:
            upper_bound = pointer
        else:
            lower_bound = pointer

    # Adjusting the pointer based on the final comparison
    return pointer + (1 if this_distance < distance and left else 0) - (1 if this_distance >= distance and not left else 0)

def find_range(data: str) -> int:
    """
    Finds the range for given time and distance data for Challenge 2.

    Args:
        data (str): The input data containing time and distance information.

    Returns:
        int: The calculated range based on the time and distance data.
    """
    time, distance = parse_data_challenge_two(data)
    lower_bound = find_bounds(time, distance)
    upper_bound = find_bounds(time, distance, False)

    return upper_bound - lower_bound + 1

def main():
    """
    Main function to execute the challenges.
    """
    # Loading data from a text file
    with open('data.txt', 'r', encoding='utf-8') as file:
        string = file.read()

    # Solving the first challenge
    time, distance = parse_data_challenge_one(string)
    challenge_one_result = calculate_result_range(time, distance)
    print(f"Challenge One Answer: {challenge_one_result}")

    # Solving the second challenge
    challenge_two_result = find_range(string)
    print(f"Challenge Two Answer: {challenge_two_result}")

if __name__ == "__main__":
    main()
