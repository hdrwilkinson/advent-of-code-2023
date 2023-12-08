import re
from typing import Dict, List, Tuple

def power_card_replacement(data: str, challenge: int = 1) -> str:
    """
    Replace specific characters in a string according to the challenge rules.

    Args:
        data (str): The string representing card data.
        challenge (int): The challenge number (1 or 2) determining the replacement rules.

    Returns:
        str: The modified string after applying the replacement rules.
    """
    if challenge == 2:
        replacements = {'T': 'A', 'J': '1', 'Q': 'C', 'K': 'D', 'A': 'E'}
    else:
        replacements = {'T': 'A', 'J': 'B', 'Q': 'C', 'K': 'D', 'A': 'E'}
    regex = re.compile('|'.join(re.escape(key) for key in replacements.keys()))
    return regex.sub(lambda x: replacements[x.group()], data)


def parse_data(data: str, challenge: int = 1) -> Dict[str, Dict[str, int]]:
    """
    Parse the provided data to extract and align card hands.

    Args:
        data (str): Raw string data containing card hands and bids.
        challenge (int): The challenge number affecting the data parsing logic.

    Returns:
        Dict[str, Dict[str, int]]: A dictionary containing parsed and processed card hand data.
    """
    lines = data.split('\n')
    hands = {}
    for line in lines:
        parts = line.split()
        unsorted_hand, bid = parts[0], int(parts[1])
        aligned_hand = power_card_replacement(unsorted_hand, challenge)
        sorted_hand = ''.join(sorted(aligned_hand))
        hands[unsorted_hand] = {
            'aligned_hand': aligned_hand, 
            'sorted_hand': sorted_hand, 
            'bid': bid,
            'jokers': unsorted_hand.count('J'),
        }
    return hands

def calculate_hand_streaks(hands: Dict[str, Dict[str, int]], challenge: int = 1) -> Dict[str, List[str]]:
    """
    Calculate streaks for each hand and categorize them by hand type.

    Args:
        hands (Dict[str, Dict[str, int]]): Dictionary of hands with their details.
        challenge (int): The challenge number affecting the streak calculation.

    Returns:
        Dict[str, List[str]]: A dictionary categorizing hands by their hand type.
    """
    max_streaks = {
        'High Card': [],
        'One Pair': [],
        'Two Pair': [],
        'Three of a Kind': [],
        'Full House': [],
        'Four of a Kind': [],
        'Five of a kind': [],
    }
    for unsorted_hand, hand_info in hands.items():
        hand = hand_info['sorted_hand']
        previous_card = '0'
        streaks = []
        streak = 1
        for card in hand:
            if card == '1':
                continue
            elif card == previous_card:
                streak += 1
            else:
                if streak > 1:
                    streaks.append(streak)
                streak = 1
            previous_card = card
        # Adding final potential streak
        if streak > 1:
            streaks.append(streak)
        streaks = sorted(streaks, reverse=True)
        # Calculating the number of streaks
        if challenge == 2:
            if streaks != []:
                streaks[0] += hand_info['jokers']
            # Edge case: Hand is all Jokers
            elif hand == '11111':
                streaks.append(hand_info['jokers'])
            # Edge case: Turning high card into pair, three of a kind, etc. if joker is present
            elif hand_info['jokers'] > 0:
                streaks.append(1 + hand_info['jokers'])
        num_streaks = len(streaks)
        # print(f'Hand: {unsorted_hand}, streaks: {streaks}, num_streaks: {num_streaks}')
        # Determining the hand type
        if num_streaks == 0:
            max_streaks['High Card'].append(unsorted_hand)
        elif num_streaks == 1:
            if streaks[0] == 2:
                max_streaks['One Pair'].append(unsorted_hand)
            elif streaks[0] == 3:
                max_streaks['Three of a Kind'].append(unsorted_hand)
            elif streaks[0] == 4:
                max_streaks['Four of a Kind'].append(unsorted_hand)
            elif streaks[0] == 5:
                max_streaks['Five of a kind'].append(unsorted_hand)
        elif num_streaks == 2:
            if streaks[0] == 2 and streaks[1] == 2:
                max_streaks['Two Pair'].append(unsorted_hand)
            elif streaks[0] == 3 and streaks[1] == 2:
                max_streaks['Full House'].append(unsorted_hand)
    return max_streaks

def compare_hands(hand1: str, hand2: str) -> int:
    """
    Compares two hands based on reverse alphabetical and numerical order.

    Args:
        hand1 (str): The first hand to compare.
        hand2 (str): The second hand to compare.

    Returns:
        int: -1 if hand1 is stronger, 1 if hand2 is stronger, 0 if equal.
    """
    for c1, c2 in zip(hand1, hand2):
        if c1 != c2:
            return -1 if c1 > c2 else 1
    return 0

def order_hands(max_streaks: Dict[str, List[str]], hands: Dict[str, Dict[str, int]], challenge: int = 1) -> List[str]:
    """
    Order hands based on their type and strength.

    Args:
        max_streaks (Dict[str, List[str]]): Dictionary categorizing hands by type.
        hands (Dict[str, Dict[str, int]]): Dictionary of hands with their details.
        challenge (int): The challenge number affecting the ordering logic.

    Returns:
        List[str]: An ordered list of hands based on their strength.
    """
    ordered_hands = []
    for hand_type in max_streaks:
        if len(max_streaks[hand_type]) == 1:
            ordered_hands += max_streaks[hand_type]
        elif challenge == 1:
            ordered_hands += sorted(max_streaks[hand_type], key=lambda x: [compare_hands(hands[x]['aligned_hand'], hands[y]['aligned_hand']) for y in max_streaks[hand_type]], reverse=True)
        elif challenge == 2:
            ordered_hands += sorted(max_streaks[hand_type], key=lambda x: [compare_hands(hands[x]['aligned_hand'], hands[y]['aligned_hand']) for y in max_streaks[hand_type]], reverse=True)

    return ordered_hands

def calculating_score(ordered_hands: List[str], hands: Dict[str, Dict[str, int]]) -> int:
    """
    Calculate the total score for the ordered hands.

    Args:
        ordered_hands (List[str]): The list of hands ordered by strength.
        hands (Dict[str, Dict[str, int]]): Dictionary of hands with their details.

    Returns:
        int: The total score calculated.
    """
    score = 0
    for i, hand in enumerate(ordered_hands):
        score += (i + 1) * hands[hand]['bid']
        # print(hand, hands[hand]["bid"])
        # print(f'Hand {i}: {hand}, rank is {(i + 1)}, score is {hands[hand]["bid"]}, total score: {(i + 1) * hands[hand]["bid"]}')
    return score

def main():
    """
    Main function to execute the challenges.
    """
    # Loading data from a text file
    with open('data.txt', 'r', encoding='utf-8') as file:
        data = file.read()

    test_data = '''2345A 1
    Q2KJJ 13
    Q2Q2Q 19
    T3T3J 17
    T3Q33 11
    2345J 3
    J345A 2
    32T3K 5
    T55J5 29
    KK677 7
    KTJJT 34
    QQQJA 31
    JJJJJ 37
    JAAAA 43
    AAAAJ 59
    AAAAA 61
    2AAAA 23
    2JJJJ 53
    JJJJ2 41'''

    # Solving the first challenge
    hands = parse_data(data)
    max_streaks = calculate_hand_streaks(hands)
    ordered_hands = order_hands(max_streaks, hands)
    challenge_one_score = calculating_score(ordered_hands, hands)
    
    # Solving the second challenge
    hands = parse_data(data, challenge=2)
    max_streaks = calculate_hand_streaks(hands, challenge=2)
    ordered_hands = order_hands(max_streaks, hands)
    challenge_two_score = calculating_score(ordered_hands, hands)

    # Printing the results
    print(f"Challenge One Answer: {challenge_one_score}")
    print(f"Challenge Two Answer: {challenge_two_score}")

if __name__ == "__main__":
    main()
