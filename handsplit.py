# Start by placing the player_hand in a container interable, then put all of the
# ensuing logic in a "for x in container", so that either one or multiple hands
# can be processed by the ensuing logic.  If the initial hand is split,
# additional hands are put into additional places in the container, and a
# continue command brings things back to the beginning of the logic.

# Upon the choice to split a hand, check to see the name of the hand, and create
# two new names that adds an integer to the hand (e.g., player_hand gets split
# and the names player_hand_1 and player_hand_2 are created).  Create these
# names at the global level.

# Pass those new hand into a splitter function to change it.

def handSplit(hand):
    player_hand1 = []
    player_hand2 = []
    player_hand1.append(hand.pop(0))
    player_hand2.append(hand.pop(0))