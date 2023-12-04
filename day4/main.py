# Function for per line calculation
def pre_line_calculation_one(line):
    """
    Processes a single line of data to calculate and return the score based on winners and elves' numbers.

    Args:
        line (str): A string representing a line of data in the format 'card_id: winners | elfs'.

    Returns:
        int: The calculated score for the line. Returns 0 if the score is less than 1.
    """
    # Remove card_id_info
    _, card_info = line.split(': ')
    # Split into winners and elfs numbers
    winners, elfs = card_info.split(' | ')
    winners_dict = {int(winning_number):0 for winning_number in winners.split()}
    elfs_list =  [int(elfs_number) for elfs_number in elfs.split()]
    # Adding matched numbers to winners dictionary
    for elfs_number in elfs_list:
        if elfs_number in winners_dict:
            winners_dict[elfs_number] = 1
    # Calculating the lines score
    score = 2**(sum(winners_dict.values()) - 1)
    # Return correct score
    if score < 1:
        return 0
    else:
        return score

def calculate_winnings_one(data):
    """
    Calculates the total score from multiple lines of data.

    Args:
        data (str): A string containing multiple lines of data, each line in the format 'card_id: winners | elfs'.

    Returns:
        int: The total score calculated from all lines.
    """
    # Separating data into lines
    lines = data.split('\n')
    # Total score calculator
    total_score = 0
    # Calculate the score per line
    for line in lines:
        total_score += pre_line_calculation_one(line)
    return total_score

def pre_line_calculation_two(line):
    """
    Processes a single line of data to calculate the number of matched numbers between winners and elves.

    Args:
        line (str): A string representing a line of data in the format 'card_id: winners | elfs'.

    Returns:
        int: The count of matched numbers between winners and elves.
    """
    # Remove card_id_info
    _, card_info = line.split(': ')
    # Split into winners and elfs numbers
    winners, elfs = card_info.split(' | ')
    winners_dict = {int(winning_number):0 for winning_number in winners.split()}
    elfs_list =  [int(elfs_number) for elfs_number in elfs.split()]
    # Adding matched numbers to winners dictionary
    for elfs_number in elfs_list:
        if elfs_number in winners_dict:
            winners_dict[elfs_number] = 1
    # Calculating the lines score
    return sum(winners_dict.values())

def calculate_winnings_two(data):
    """
    Calculates a modified total score from multiple lines of data, factoring in a cumulative effect based on line scores.

    Args:
        data (str): A string containing multiple lines of data, each line in the format 'card_id: winners | elfs'.

    Returns:
        int: The cumulative total score calculated from all lines.
    """
    # Separating data into lines
    lines = data.split('\n')
    # Total score calculator
    scratch_cards = {i:1 for i in range(len(lines))}
    # Calculate the score per line
    for i, line in enumerate(lines):
        line_score = pre_line_calculation_two(line)
        for j in range(line_score):
            scratch_cards[i+j+1] += scratch_cards[i]
    return sum(scratch_cards.values())

if __name__ == "__main__":
    # Loading the data
    with open('data.txt', 'r', encoding='utf-8') as file:
        string = file.read()

    # Results
    challenge_one_total = calculate_winnings_one(string)
    challenge_two_total = calculate_winnings_two(string)

    # Printing results
    print(f"Challenge One Answer: {challenge_one_total}")
    print(f"Challenge Two Answer: {challenge_two_total}")