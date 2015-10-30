# Blackjack - A text-based thrill-ride
# Copyright 2015 Jeff Walters


# for shuffling
import random


# Create list of every card in a deck, with possible values as second component,
# in a tuple.  Aces all have a third item in the tuple as the alternate low value.
suits = ['Clubs', 'Spades', 'Diamonds', 'Hearts']
cards = [('Ace', 11, 1), ('Two', 2, 2), ('Three', 3, 3), ('Four', 4, 4),
         ('Five', 5, 5), ('Six', 6, 6), ('Seven', 7, 7), ('Eight', 8, 8),
         ('Nine', 9, 9), ('Ten', 10, 10), ('Jack', 10, 10), ('Queen', 10, 10),
         ('King', 10, 10)]
deck = [(card[0] + ' of '+ suit, card[1], card[2]) for
        card in cards for suit in suits]


# Create line of dashes
LINE_OF_DASHES = '-' * 50
    
# Create spacing
LINE_OF_SPACES = ' ' * 25


# Create function to print player's opening hand as well as the dealer's hand
# (only one dealer card turned over)
def handDisplay():
    print('\n\n', LINE_OF_DASHES,'\nYour hand:\n', sep='')
    for x in player_hand:
        print(LINE_OF_SPACES, x[0])
    print("\n\nDealer's hand:\n")
    print(LINE_OF_SPACES, opponent_hand[0][0])
    print(LINE_OF_SPACES, 'Unknown')
    print(LINE_OF_DASHES)

# Create function to print player's full hand as well as the dealer's full
# hand
def fullhandDisplay():
    print('\n\n', LINE_OF_DASHES,'\nYour hand:\n', sep='')
    for x in player_hand:
        print(LINE_OF_SPACES, x[0])
    print("\n\nDealer's hand:\n")
    for x in opponent_hand:
        print(LINE_OF_SPACES, x[0])
    print(LINE_OF_DASHES)
    
    
# Wrap everything in a while loop
while True:

    # Create clean copy of deck to be used for game.
    game_deck = deck.copy()


    # Initiate empty hands for player and dealer.
    player_hand = []
    opponent_hand = []

    # Begin by shuffling entire deck.
    random.shuffle(game_deck)


    # Take 4 cards away from game deck, two to player, and the other two to dealer.
    for _ in range(2):
        player_hand.append(game_deck.pop(0))
        opponent_hand.append(game_deck.pop(0))
   
    
    # Print opening hands for both sides
    handDisplay()


    # Look at values of each card in both sides' hands, build them into lists, and
    # then sum the lists.
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




    print('\n\nYour hand is worth', L, 'points.')
    print('\nDealer\'s hand so far shows', opponent_hand[0][1], 'points.')



    # This code prompts the player to hit or to stay.  If the player elects to hit, another card is popped off
    # the game deck and put into the player's hand.  There are "if tests" to detect if the card is an Ace.  If the
    # card is detected as being an Ace, it is set to a low Ace if the current hand points total is higher than 12,
    # to avoid busting.
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


    # If, after all of the preceding events have left a player with a hand over 21, this prints a "losing" message.  
    if L > 21:
        print('With', L, 'points, you bust!')
     
        
    else:
        print('\nDealer\'s other card is a', opponent_hand[1][0])
        fullhandDisplay()
        print('Dealer\'s full hand shows', M, 'points.')
        print('\n')
        input('Press enter to continue...')

        print('\n')


        # This section of code evaluates and prints out pertinent details of the dealer's hand.  The dealer will hit on hands
        # below 18.  This code also accounts for low and high values of aces, and will adjust them accordingly for the highest point
        # total possible without busting.
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


    # This code evaluates final scores once more and prints an appropriate message.       
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
       
    # Finally, the game asks if you wish to continue and exits on a 'q' or a 'Q'.
    another = input('\nWant to quit? If so, type "Q".  Press enter to continue with another game.')
    if another.upper() == 'Q':
        print('Thanks for playing!')
        break

        
