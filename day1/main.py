from collections import defaultdict
from typing import Dict, List

class TrieNode:
    """A node in the Trie structure.

    Attributes:
        children (defaultdict): A dictionary of children nodes.
        is_end_of_word (int): Flag to check if it's the end of a word.
    """
    def __init__(self):
        self.children = defaultdict(TrieNode)
        self.is_end_of_word = 0

def search_trie(root: TrieNode, word: str) -> int:
    """Searches for a word in a trie.

    Args:
        root (TrieNode): The root node of the trie.
        word (str): The word to search for.

    Returns:
        int: Status of the search (0, 1, or 2).
    """
    node = root
    for char in word:
        if char not in node.children:
            return 2
        node = node.children[char]
    if node.children:
        return 0
    else:
        return node.is_end_of_word

def build_trie(keys: List[str]) -> TrieNode:
    """Builds a trie from a list of words.

    Args:
        keys (List[str]): A list of words to build the trie.

    Returns:
        TrieNode: The root node of the built trie.
    """
    root = TrieNode()
    for key in keys:
        node = root
        for char in key:
            node = node.children[char]
        node.is_end_of_word = 1
    return root

'''
This code finds the first and last number in a given line of text
'''
def find_number(line: str, conversion_dict: Dict[str, int], trie: TrieNode) -> int:
    """Finds numbers in a string line based on a trie.

    Args:
        line (str): The string line to search numbers in.
        conversion_dict (Dict[str, int]): A dictionary for number conversion.
        trie (TrieNode): The trie to use for searching.

    Returns:
        int: The total of the numbers found.
    """
    start_pointer, end_pointer = 0, 0
    start_number, end_number = "", ""
    searching = False # If searching for extended word
    while end_pointer < len(line):
        # Use the pointers to slice characters from the string
        word = line[start_pointer:end_pointer+1]
        # Search trie
        result = search_trie(trie, word)
        # If we have a match
        if result == 1:
            # Check if this is the first number
            if start_number == "":
                # Add as starting number
                start_number = conversion_dict[word]
            # Insert or replace end number every time
            end_number = conversion_dict[word]
            # If match was found whilst searching a word
            if searching:
                # Only increment start pointer by 1
                start_pointer += 1
                end_pointer = start_pointer
                searching = False
            # If match was found wasn't searching
            else:
                # Set starter pointer and end pointer to 1 beyond current search
                end_pointer += 1
                start_pointer = end_pointer
        # If we don't have a match, but we haven't finished the search
        elif result == 0:
            # Extend the search, add 1 to searching
            end_pointer += 1
            searching = True
        # Not a match, but was searching
        elif searching:
            # Reset search, set starting pointer 1 beyond, set end pointer to start pointer
            searching = False
            start_pointer += 1
            end_pointer = start_pointer
        # Not a match and wasn't searching
        else:
            # Set starter pointer and end pointer to 1 beyond current search
            end_pointer += 1
            start_pointer = end_pointer
    total = start_number + end_number
    if total == 0:
        print("Empty string!!!")
    return total

def sum_strings(string: str, conversion_dict: Dict[str, int], trie: TrieNode) -> int:
    """Sums up numbers in a multiline string based on a trie.

    Args:
        string (str): The multiline string to process.
        conversion_dict (Dict[str, int]): Dictionary for number conversion.
        trie (TrieNode): The trie to use for finding numbers.

    Returns:
        int: The sum of all numbers found in the string.
    """
    # Separating string into lines
    lines = string.strip().split('\n')
    # Variable for total count
    total = 0
    # Loop to calculate totals
    for i, line in enumerate(lines):
        number_as_string = find_number(line, conversion_dict, trie)
        total += int(number_as_string)

    return total

if __name__ == "__main__":
    # Loading the data
    with open('data.txt', 'r', encoding='utf-8') as file:
        string = file.read()

    # Dictionary for number conversion
    number_conversion = {
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9",
    }

    # Generating the trie for the number only version
    number_trie = build_trie(number_conversion.keys())

    # Dictionary for number and string conversion
    number_and_string_conversion = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9",
    }

    # Generating the trie for the number and string version
    number_and_string_trie = build_trie(number_and_string_conversion.keys())

    # Results
    number_total_test_prediction = sum_strings(string, number_conversion, number_trie)
    number_and_string_total_test_prediction = sum_strings(string, number_and_string_conversion, number_and_string_trie)
    
    # Printing results
    print("Number Total Test Prediction:", number_total_test_prediction)
    print("Number and String Total Test Prediction:", number_and_string_total_test_prediction)