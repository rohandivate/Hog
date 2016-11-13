"""CS 61A Presents The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.
dice_swap = False

######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS>0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return the
    number of 1's rolled.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    "*** REPLACE THIS LINE ***"
    count, total, ones = 0, 0, 0
    count_ones = False
    while count < num_rolls:
        num = dice()
        if count_ones == True and num == 1:
                ones += 1
        elif num == 1:
            count_ones = True
            ones += 1
        elif count_ones == False:
            total += num
        count += 1
    if count_ones == True:
        return ones
    else:
        return total
    # END PROBLEM 1


def free_bacon(opponent_score):
    """Return the points scored from rolling 0 dice (Free Bacon)."""
    # BEGIN PROBLEM 2
    pig_score = 0
    if opponent_score%10 == opponent_score:
        pig_score = 1 + opponent_score
    else:
        digit = opponent_score%10
        opponent_score //= 10
        digit2 = opponent_score%10
        pig_score = 1 + max(digit, digit2)
    if is_prime(pig_score):
        pig_score = next_prime(pig_score)
    return pig_score


# Write your prime functions here!
def is_prime(n):
    c = 2
    if n == 1:
        return False
    while c*c <= n:
        if n%c == 0:
            return False
        c += 1
    return True

def next_prime(p):
    found = False
    count = 1
    while found == False:
        test = p + count
        if is_prime(test):
            return test
            found = True
        count += 1

def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player. Also
    implements the Hogtimus Prime and When Pigs Fly rules.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2

    score, limit = 0, 25 - num_rolls
    if num_rolls == 0:
        score = free_bacon(opponent_score)
        if score > limit:
            return limit
        return score
    else:
        score = roll_dice(num_rolls, dice)
        if is_prime(score):
            score = next_prime(score)
        if score > limit:
            return limit
        return score


def reroll(dice):
    """Return dice that return even outcomes and re-roll odd outcomes of DICE."""
    def rerolled():
        # BEGIN PROBLEM 3
        "*** REPLACE THIS LINE ***"
        sum = dice()
        if sum % 2 == 0:
            return sum
        else:
            sum = dice()
            return sum

        # END PROBLEM 3
    return rerolled


def select_dice(score, opponent_score, dice_swapped):
    """Return the dice used for a turn, which may be re-rolled (Hog Wild) and/or
    swapped for four-sided dice (Pork Chop).

    DICE_SWAPPED is True if and only if four-sided dice are being used.
    """
    # BEGIN PROBLEM 4
    "*** REPLACE THIS LINE ***"
    if dice_swapped:
        dice = four_sided
    else:
        dice = six_sided
    # Replace this statement
    # END PROBLEM 4
    if (score + opponent_score) % 7 == 0:
        dice = reroll(dice)

    return dice


def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player

def is_swap(score0, score1):
    if score1 == 2*score0 or score0 == 2*score1:
        return True
    else:
        return False

def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    dice_swapped = False  # Whether 4-sided dice have been swapped for 6-sided
    # BEGIN PROBLEM 5
    "*** REPLACE THIS LINE ***"
    while score0<goal and score1<goal:
        if player == 0:
            num_rolls = strategy0(score0, score1)
            if num_rolls == -1:
                dice_swapped = not dice_swapped
                score0 += 1
            else:
                score0 += take_turn(num_rolls, score1, select_dice(score0, score1, dice_swapped))
        else:
            num_rolls = strategy1(score1, score0)
            if num_rolls == -1:
                dice_swapped = not dice_swapped
                score1+=1
            else:
                score1 += take_turn(num_rolls, score0, select_dice(score1, score0, dice_swapped))

        if is_swap(score0, score1):
            score0, score1 = score1, score0

        player = other(player)
    return score0, score1




    # END PROBLEM 5



#######################
# Phase 2: Strategies #
#######################

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def check_strategy_roll(score, opponent_score, num_rolls):
    """Raises an error with a helpful message if NUM_ROLLS is an invalid
    strategy output. All strategy outputs must be integers from -1 to 10.

    >>> check_strategy_roll(10, 20, num_rolls=100)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(10, 20) returned 100 (invalid number of rolls)

    >>> check_strategy_roll(20, 10, num_rolls=0.1)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(20, 10) returned 0.1 (not an integer)

    >>> check_strategy_roll(0, 0, num_rolls=None)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(0, 0) returned None (not an integer)
    """
    msg = 'strategy({}, {}) returned {}'.format(
        score, opponent_score, num_rolls)
    assert type(num_rolls) == int, msg + ' (not an integer)'
    assert -1 <= num_rolls <= 10, msg + ' (invalid number of rolls)'


def check_strategy(strategy, goal=GOAL_SCORE):
    """Checks the strategy with all valid inputs and verifies that the
    strategy returns a valid input. Use `check_strategy_roll` to raise
    an error with a helpful message if the strategy returns an invalid
    output.

    >>> def fail_15_20(score, opponent_score):
    ...     if score != 15 or opponent_score != 20:
    ...         return 5
    ...
    >>> check_strategy(fail_15_20)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(15, 20) returned None (not an integer)
    >>> def fail_102_115(score, opponent_score):
    ...     if score == 102 and opponent_score == 115:
    ...         return 100
    ...     return 5
    ...
    >>> check_strategy(fail_102_115)
    >>> fail_102_115 == check_strategy(fail_102_115, 120)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(102, 115) returned 100 (invalid number of rolls)
    """
    # BEGIN PROBLEM 6
    "*** REPLACE THIS LINE ***"
    #assert -1 <= strategy <= 10
    score = 0
    opponent_score = 0
    while score<=goal:
        while opponent_score<=goal:
            num_rolls = strategy(score, opponent_score)
            check_strategy_roll(score, opponent_score, num_rolls)
            opponent_score += 1
        score += 1
        opponent_score = 0
    # END PROBLEM 6



# Experiments

def make_averaged(fn, num_samples=10):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    """
    # BEGIN PROBLEM 7
    "*** REPLACE THIS LINE ***"
    def average_nums(*args):
        total = 0
        count = num_samples
        while count > 0:
            total += fn(*args)
            count -= 1
        return total/num_samples
    return average_nums

    # END PROBLEM 7


def max_scoring_num_rolls(dice=six_sided, num_samples=100):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN PROBLEM 8
    "*** REPLACE THIS LINE ***"
    num_dice, best_dice, max_average = 1, 1, 0
    averaged = make_averaged(roll_dice, num_samples)
    while num_dice <= 10:
        temp_average = averaged(num_dice, dice)
        if temp_average > max_average:
            max_average = temp_average
            best_dice = num_dice
        num_dice+=1
    return best_dice


    # END PROBLEM 8


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(4)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        rerolled_max = max_scoring_num_rolls(reroll(six_sided))
        print('Max scoring num rolls for re-rolled dice:', rerolled_max)

    if True:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if True:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if True:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))
    print ("LOL ", max_scoring_num_rolls(four_sided, 1000))
    "*** You may add additional experiments as you wish ***"


# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 9
    "*** REPLACE THIS LINE ***"
    pig_score = free_bacon(opponent_score)
    if pig_score>= margin:
        return 0
    else:
        return num_rolls

      # Replace this statement
    # END PROBLEM 9
#check_strategy(bacon_strategy)


def swap_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points. Otherwise, it rolls
    NUM_ROLLS.
    """
    # BEGIN PROBLEM 10
    "*** REPLACE THIS LINE ***"
    pig_score = free_bacon(opponent_score) + score
    if is_swap(pig_score, opponent_score) and pig_score<opponent_score:
        return 0
    else:
        return bacon_strategy(score, opponent_score, margin, num_rolls)

    # END PROBLEM 10
#check_strategy(swap_strategy)


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.
    The goal of this strategy is to slow down the game enough so that the player
    has more chances to swap against the strategy always_roll(4). We know that
    the opponent's strategy will not use Pork Chop or Free Bacon, so it is to
    our advantage to maximize the use of those strategies. The initial if
    statement sets up four dice for the rest of the game (inducing more swaps).
    Then swap_strategy is used to utilize Free Bacon and Swine Swap to gain the
    most points in any situation.
    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN PROBLEM 11
    if score == 0 or opponent_score == 0:
        return -1
    return swap_strategy(score, opponent_score, 6, 6)

    "*** REPLACE THIS LINE ***"

     # Replace this statement
    # END PROBLEM 11
#check_strategy(final_strategy)


##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()

dice = make_test_dice(1, 2, 2, 2, 2, 2, 2, 2)
print(max_scoring_num_rolls(dice, num_samples=1000))
