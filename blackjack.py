# Blackjack - A text-based thrill-ride
# Copyright 2015 Jeff Walters
#
#
#   This is my first actual program.
#   It's a valiant attempt at a text version of blackjack.
#   Please do not laugh too hard at any of this.
#   We all have to start somewhere!

# I'm starting out by trying to make a list that contains embedded tuples
# which represent each card and its corresponding value.


""" Version history/changes:
       1.00 (10/08/15) Initial game (incomplete logic for Aces)
       1.01 (10/15/15)
                -- Fixed the behavior of Aces so that they can equal 1 or 11, based on the hand's point total
                -- Wrapped the display of player and opponent hand into a function, and call the function each draw

    To-Do:
            -- Allow for a Jack/Ace combo to win automatically ("Blackjack")
            -- Allow for a wallet and betting on each hand
"""


import random
# for shuffling



deck = [('Ace of Clubs', 11, 1), ('Ace of Spades', 11, 1), ('Ace of Diamonds', 11, 1), ('Ace of Hearts', 11, 1),
('Two of Clubs', 2), ('Two of Spades', 2), ('Two of Diamonds', 2), ('Two of Hearts', 2),
('Three of Clubs', 3), ('Three of Spades', 3), ('Three of Diamonds', 3), ('Three of Hearts', 3),
('Four of Clubs', 4), ('Four of Spades', 4), ('Four of Diamonds', 4), ('Four of Hearts', 4),
('Five of Clubs', 5), ('Five of Spades', 5), ('Five of Diamonds', 5), ('Five of Hearts', 5),
('Six of Clubs', 6), ('Six of Spades', 6), ('Six of Diamonds', 6), ('Six of Hearts', 6),
('Seven of Clubs', 7), ('Seven of Spades', 7), ('Seven of Diamonds', 7), ('Seven of Hearts', 7),
('Eight of Clubs', 8), ('Eight of Spades', 8), ('Eight of Diamonds', 8), ('Eight of Hearts', 8),
('Nine of Clubs', 9), ('Nine of Spades', 9), ('Nine of Diamonds', 9), ('Nine of Hearts', 9),
('Ten of  Clubs', 10), ('Ten of Spades', 10), ('Ten of Diamonds', 10), ('Ten of Hearts', 10),
('Jack of Clubs', 10), ('Jack of Spades', 10), ('Jack of Diamonds', 10), ('Jack of Hearts', 10),
('Queen of Clubs', 10), ('Queen of Spades', 10), ('Queen of Diamonds', 10), ('Queen of Hearts', 10),
('King of Clubs', 10), ('King of Spades', 10), ('King of Diamonds', 10), ('King of Hearts', 10)]
# Create list of every card in a deck, with possible values as second component,
# in a tuple.  Aces all have a third item in the tuple as the alternate low value.

def handDisplay():
    print('\n\n', dash,'\nYour hand:\n', sep='')
    for x in player_hand:
        print(space, x[0])
    print("\n\nDealer's hand:\n")
    print(space, opponent_hand[0][0])
    print(space, 'Unknown')
    print(dash)

def fullhandDisplay():
    print('\n\n', dash,'\nYour hand:\n', sep='')
    for x in player_hand:
        print(space, x[0])
    print("\n\nDealer's hand:\n")
    for x in opponent_hand:
        print(space, x[0])
    print(dash)

while True:
# Wrap everything in a while loop

    game_deck = deck.copy()
# Create clean copy of deck to be used for game.

    player_hand = []
    opponent_hand = []
# Initiate empty hands for player and dealer.

    random.shuffle(game_deck)
# Begin by shuffling entire deck.


    for x in 'xx':
        player_hand.append(game_deck.pop(0))

    for x in 'xx':
        opponent_hand.append(game_deck.pop(0))
# Take 4 cards away from game deck, two to player, and the other two to dealer.
    dash = '-' * 50
    space = ' ' * 25
    handDisplay()

    l = []
    for x in range(len(player_hand)):
        l.append(player_hand[x][1])

    if sum(l) > 21:
        l.sort()
        if l[-1] == 11:
            l[-1] = 1

    m = []
    for x in range(len(opponent_hand)):
        m.append(opponent_hand[x][1])

    if sum(m) > 21:
        m.sort()
        if m[-1] == 11:
            m[-1] = 1

    L = sum(l)
    M = sum(m)


# Look at values of each card in both sides' hands, build them into lists, and
# then sum the lists.

    print('\n\nYour hand is worth', L, 'points.')
    print('\nDealer\'s hand so far shows', opponent_hand[0][1], 'points.')

    while L < 22:
        decision = input('\nType "H" to hit.  Type "S" to stand.')
        if decision.upper() == 'H':
            player_hand.append(game_deck.pop(0))
            print('\nYou draw', player_hand[-1][0])
            if player_hand[-1][1] == 11:
                if L > 12:
                    l.append(player_hand[-1][2])
                else:
                    l.append(player_hand[-1][1])
            else:
                l.append(player_hand[-1][1])
            if sum(l) > 21:
                l.sort()
                if l[-1] == 11:
                    l[-1] = 1
                                                          
            L = sum(l)
            handDisplay()
            print('\nYour hand is now worth', L, 'points.')
        elif decision.upper() == 'S':
            print('\nStanding with:', L, 'points.')
            input('Press enter to continue...')
            break
        L = sum(l)
 # The above code prompts the player to hit or to stay.  If the player elects to hit, another card is popped off
 # the game deck and put into the player's hand.  There are "if tests" to detect if the card is an Ace.  If the
 # card is detected as being an Ace, it is set to a low Ace if the current hand points total is higher than 12,
 # to avoid busting.





    if L > 21:
        print('With', L, 'points, you bust!')
 # If, after all of the preceding events have left a player with a hand over 21, this prints a "losing" message.       



        
    else:
        print('\nDealer\'s other card is a', opponent_hand[1][0])
        fullhandDisplay()
        print('Dealer\'s full hand shows', M, 'points.')
        print('\n')
        input('Press enter to continue...')

        print('\n')

        while M < 22:
            if M > 17:
                print('Dealer stands.')
                print('Dealer\'s final hand shows', M, 'points against your hand of', L, 'points.')
                break
            elif M > 21:
                print('Dealer busts!')
                break
            opponent_hand.append(game_deck.pop(0))
            print('Dealer draws', opponent_hand[-1][0])
            fullhandDisplay()
            if opponent_hand[-1][1] == 11:
                if M > 12:
                    m.append(opponent_hand[-1][2])
                else:
                    m.append(opponent_hand[-1][1])
            else:
                m.append(opponent_hand[-1][1])

            if sum(m) > 21:
                m.sort()
                if m[-1] == 11:
                    m[-1] = 1
                
            M = sum(m)
            print('Dealer\'s hand now shows', M, 'points against your hand of', L, 'points.')
            input('\nPress enter to continue...\n')
# This section of code evaluates and prints out pertinent details of the dealer's hand.  The dealer will hit on hands
# below 18.  This code also accounts for low and high values of aces, and will adjust them accordingly for the highest point
# total possible without busting.

         
    if 22 > L == M:
        print('\nPush!')
    elif 22 > L > M:
        print('\nYou win!!!')
    elif 22 > M > L:
        print('\nYou lose...')
    elif L > 21:
        print('\nYou lose...')
    elif M > 21:
        print('\nDealer busts! You win!!!')
# This code evaluates final scores once more and prints an appropriate message.        

    another = input('\nWant to quit? If so, type "Q".  Press enter to continue with another game.')
    if another.upper() == 'Q':
        print('Thanks for playing!')
        break
# Finally, the game asks if you wish to continue and exits on a 'q' or a 'Q'.
        
