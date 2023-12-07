import numpy as np
from typing import List, Tuple

def structure_data_one(data: str) -> Tuple[List[int], List[List[List[int]]], List[str]]:
    """
    Processes the input data to extract seeds, mapping data, and mapping names.

    The function splits the input data into separate sections, parses seed numbers,
    and organizes mapping data into a structured format for further processing.

    Args:
        data (str): A string containing the puzzle input data.

    Returns:
        Tuple[List[int], List[List[List[int]]], List[str]]:
        - A list of seed numbers.
        - A list of lists of lists containing the mapping data.
        - A list of mapping names.
    """
    # Splitting input data into sections
    items = data.split('\n\n')
    # Extracting seeds
    _, seeds = items[0].split(':')
    seeds_list = [int(seed) for seed in seeds.split()]
    # Organizing mapping data
    mapping_data = [[list(map(int, item.split())) for item in mapping_item.split('\n')[1:]]
                    for mapping_item in (item.split(':')[1] for item in items[1:])]
    mapping_names = [item.split(':')[0].split()[0] for item in items[1:]]

    return seeds_list, mapping_data, mapping_names

def seed_to_location(seeds_list: List[int], mapping_data: List[List[List[int]]]) -> int:
    """
    Determines the minimum location value for a list of seeds based on mapping data.

    The function iteratively maps each seed number through various stages
    to find its corresponding location number, and then returns the minimum location number.

    Args:
        seeds_list (List[int]): A list of seed numbers.
        mapping_data (List[List[List[int]]]): Mapping data for seed conversion.

    Returns:
        int: The minimum location number that corresponds to any of the seed numbers.
    """
    location_list = []
    for seed in seeds_list:
        pointer = seed
        for stage in mapping_data:
            for mapping in stage:
                source_lower_bound, destination_lower_bound, range_length = mapping
                source_upper_bound = source_lower_bound + range_length
                if source_lower_bound <= pointer < source_upper_bound:
                    pointer = destination_lower_bound + (pointer - source_lower_bound)
                    break
        location_list.append(pointer)

    return min(location_list)


def structure_data_two(data: str) -> Tuple[np.ndarray, List[np.ndarray]]:
    """
    Processes the input data for the second part of the challenge.

    This function is similar to `structure_data_one` but organizes the seeds
    and mapping data into NumPy arrays, which are more suitable for handling ranges of seed numbers.

    Args:
        data (str): A string containing the puzzle input data.

    Returns:
        Tuple[np.ndarray, List[np.ndarray]]:
        - A NumPy array of seed ranges.
        - A list of NumPy arrays containing the mapping data.
    """
    items = data.split('\n\n')
    _, seeds = items[0].split(':')
    seeds_list = [int(seed) for seed in seeds.split()]
    seeds_array = np.array(seeds_list).reshape(-1, 2)
    mapping_array = [np.array([[int(item) for item in mapping_row.split()] for mapping_row in mapping_item.split('\n')[1:]])
                     for mapping_item in (test_item.split(':')[1] for test_item in items[1:])]
    mapping_array = [np.array(sorted(inner_array, key=lambda x: x[0])) for inner_array in mapping_array]

    return seeds_array, mapping_array

def location_to_seed(seeds_array: np.ndarray, mapping_array: List[np.ndarray], checker: int = 1000000) -> int:
    """
    Finds the location number for a given range of seed numbers.

    This function iterates through various locations to find the one that corresponds
    to a seed number within the specified ranges.

    Args:
        seeds_array (np.ndarray): An array containing ranges of seed numbers.
        mapping_array (List[np.ndarray]): A list of NumPy arrays with mapping data.
        checker (int, optional): A value to print progress. Defaults to 1000000.

    Returns:
        int: The location number that corresponds to any of the initial seed numbers.
    """
    location = 80000000
    while True:
        pointer = location
        for stage in reversed(mapping_array):
            for item in stage:
                source_lower_bound, destination_lower_bound, range_length = item
                source_upper_bound = source_lower_bound + range_length
                if source_lower_bound <= pointer < source_upper_bound:
                    pointer = destination_lower_bound + (pointer - source_lower_bound)
                    break

        for seed_span in seeds_array:
            seed_lower_bound, range_length = seed_span
            seed_upper_bound = seed_lower_bound + range_length
            if seed_lower_bound <= pointer < seed_upper_bound:
                return location
        if location % checker == 0:
            print(f"Checked location {location}")
        location += 1

if __name__ == "__main__":
    # Loading data from a text file
    with open('data.txt', 'r', encoding='utf-8') as file:
        string = file.read()

    # Solving the first challenge
    seeds_list, mapping_data, _ = structure_data_one(string)
    challenge_one_result = seed_to_location(seeds_list, mapping_data)

    # Solving the second challenge
    seeds_array, mapping_array = structure_data_two(string)
    challenge_two_result = location_to_seed(seeds_array, mapping_array)

    # Displaying results
    print(f"Challenge One Answer: {challenge_one_result}")
    print(f"Challenge Two Answer: {challenge_two_result}")