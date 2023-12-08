''' Main file for day8 challenges. '''

import math
from typing import Dict, List, Tuple

def parse_data(data: str) -> Tuple[str, List[str]]:
    """
    Parses the input data into instructions and a list of node mappings.

    This function splits the input data based on newline characters. The first line is treated as 
    the instructions string, and the remaining lines are considered as node mappings.

    Args:
        data (str): The raw string data containing instructions and node mappings.

    Returns:
        Tuple[str, List[str]]: A tuple containing instructions and a list of node mappings.
    """
    lines = data.split('\n')
    return lines[0], lines[2:]

def map_to_dictionary(map_list: List[str]) -> Dict[str, Dict[str, str]]:
    """
    Converts a list of node mappings into a dictionary format.

    Each line in the list is split into key-value pairs, where the key is the node name, and the value is 
    another dictionary with keys 'L' and 'R' representing left and right node names respectively.

    Args:
        map_list (List[str]): A list of strings representing node mappings.

    Returns:
        Dict[str, Dict[str, str]]: A dictionary representation of node mappings.
    """
    mapping = {}
    for line in map_list:
        parts = line.split(' = ')
        node = parts[0]
        left, right = parts[1][1:-1].split(', ')
        mapping[node] = {'L': left, 'R': right}
    return mapping

def find_start_nodes(mapping: Dict[str, Dict[str, str]]) -> Dict[int, str]:
    """
    Identifies the starting nodes in the mapping.

    Starting nodes are defined as those whose names end with 'A'. The function enumerates through the keys
    of the mapping and selects those ending in 'A'.

    Args:
        mapping (Dict[str, Dict[str, str]]): The mapping of nodes.

    Returns:
        Dict[int, str]: A dictionary mapping index to starting node names.
    """
    start_nodes = {}
    for i, node in enumerate(mapping.keys()):
        if node[-1] == 'A':
            start_nodes[i] = node
    return start_nodes

def start_to_end(instructions: str, mapping: Dict[str, Dict[str, str]], start_node: str = 'AAA') -> int:
    """
    Calculates the number of steps to reach a specific end node from a start node.

    The function iterates through the instructions and moves through the nodes as per the instruction until
    the end node ('ZZZ') is reached.

    Args:
        instructions (str): A string of instructions dictating the path to follow.
        mapping (Dict[str, Dict[str, str]]): A dictionary representing the node mappings.
        start_node (str): The node from which to start. Defaults to 'AAA'.

    Returns:
        int: The number of steps required to reach the end node.
    """
    instruction_length = len(instructions)
    node = start_node
    distance = 0
    while True:
        distance += 1
        instruction_pointer = distance % instruction_length - 1
        instruction = instructions[instruction_pointer]
        node = mapping[node][instruction]
        if node == 'ZZZ':
            return distance

def start_to_end_two(instructions: str, mapping: Dict[str, Dict[str, str]], start_nodes: Dict[int, str]) -> int:
    """
    Calculates the number of steps until all paths from multiple start nodes end at nodes ending with 'Z'.

    The function simultaneously follows paths from all start nodes and stops when all paths end at nodes
    ending with 'Z'. The least common multiple of all path lengths is returned.

    Args:
        instructions (str): A string of instructions dictating the path to follow.
        mapping (Dict[str, Dict[str, str]]): A dictionary representing the node mappings.
        start_nodes (Dict[int, str]): A dictionary mapping indices to starting node names.

    Returns:
        int: The least common multiple of the steps required for all paths to end at nodes ending with 'Z'.
    """
    instruction_length = len(instructions)
    end_distances = []
    for _, start_node in start_nodes.items():
        distance = 0
        node = start_node
        while node[-1] != 'Z' or distance < instruction_length:
            distance += 1
            instruction_pointer = distance % instruction_length - 1
            instruction = instructions[instruction_pointer]
            node = mapping[node][instruction]
        end_distances.append(distance)
    return math.lcm(*end_distances)

def main():
    """
    Main function to execute the challenges.

    The function reads input data, parses it, and solves the given challenges.
    """
    # Loading data from a text file
    with open('data.txt', 'r', encoding='utf-8') as file:
        data = file.read()

    # Loading test data for challenge one
    test_data_one = '''LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)'''

    # Loading test data for challenge two
    test_data_two = '''LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)'''

    # Solving the first challenge
    instructions, map = parse_data(data)
    mapping = map_to_dictionary(map)
    challenge_one_score = start_to_end(instructions, mapping)
    
    # Solving the second challenge
    instructions, map = parse_data(data)
    mapping = map_to_dictionary(map)
    start_nodes = find_start_nodes(mapping)
    challenge_two_score = start_to_end_two(instructions, mapping, start_nodes)



    # Printing the results
    print(f"Challenge One Answer: {challenge_one_score}")
    print(f"Challenge Two Answer: {challenge_two_score}")

if __name__ == "__main__":
    main()
