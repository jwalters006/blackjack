# Import tkinter/ttk
from tkinter import *
from tkinter import ttk

# Import pygame and initialize pygame mixer for sound effects
import pygame
pygame.mixer.init()
soundpath = 'Sounds\\'
winsound = pygame.mixer.Sound(soundpath+"win2.wav")
losesound = pygame.mixer.Sound(soundpath+"lose2.wav")
pushsound = pygame.mixer.Sound(soundpath+"push.wav")
coinsound = pygame.mixer.Sound(soundpath+"COIN.wav")
fireworksound = pygame.mixer.Sound(soundpath+"firework1.wav")

# To store high scores and data
import shelve

# For shuffling
import random

# Create player class
class Player:
    def __init__(self, name, score=0, wallet=100, win=0, loss=0):
        self.name = name
        self.score = score
        self.wallet = wallet
        self.win = win
        self.loss = loss
        
# Create card class
class Card:
    def __init__(self, title, image, value1, value2):
        self.title = title
        self.image = image
        self.value1 = value1
        self.value2 = value2
        
# Create function to output text to main textbox display area
def text(*args):
    textoutput.configure(state='normal')
    textoutput.see('end')
    for arg in args:
        textoutput.insert('end', arg)
    textoutput.configure(state='disabled')
   
# Create function to update player's top single-session score and
# cumulative wallet amount and save to a database file.  Also update
# displayed amounts for wallet and score of dealer's hand.
def updateDb():
    global wallet, tally
    db = shelve.open('highscores')
    if player.score < tally:
        player.score = tally
    player.wallet = int(wallet)
    walletamount.set(int(wallet))
    db[name] = player
    db.close()
    fullhandDisplay()
    dealerscore.set(M)
    betamount.set('')

# Create function to display player history and scores
def displayDb():
    db = shelve.open('highscores')
    player_objects = [(db[x].name, db[x].wallet, db[x].win, db[x].loss, db[x].score) for x in db]
    try:
        sorted_player_objects = sorted(player_objects, key=lambda x: x[2], reverse=True)
        text('\n', LINE_OF_DASHES, '\nPlayers that have played:\n')
        for x in sorted_player_objects:
            text('Player name: ', x[0], '\t\t\tWallet: ', int(x[1]), '\tWins: ', x[2], '\tLosses: ', x[3], '\n')
        text(LINE_OF_DASHES, '\n')
    except:
        text('Currently this part of the script is under construction due to "Division by 0 error" issues.\n')
        
# Create functions to update running gain/loss tally and wallet, win, lose, or draw
def updateWin():
    global wallet, tally, bet, player_blackjack
    if player_blackjack == True:
        bet = bet * 1.5
    wallet += int(bet)
    tally += int(bet)
    text('You win! Your wallet increased by $', int(bet), '!\n')
    text('Your current sessions winnings(losses) are $', int(tally), '.\n')
    player.win += 1
    if player_blackjack == True:
        fireworksound.play()
    else:
        winsound.play()
    if player_blackjack == True:
        textoutput.image_create('end', image=bjgraphics)
    else:
        textoutput.image_create('end', image=wingraphics)
    updateDb()
    hitbutton.state(['disabled'])
    standbutton.state(['disabled'])
    dbldownbutton.state(['disabled'])
    startGame()

def updateLose():
    global wallet, tally, bet, player
    wallet -= int(bet)
    tally -= int(bet)
    text('Your wallet decreased by $', int(bet), '!\n')
    text('Your current sessions winnings(losses) are $', int(tally), '.\n')
    player.loss += 1
    losesound.play()
    textoutput.image_create('end', image=losegraphics)
    updateDb()
    hitbutton.state(['disabled'])
    standbutton.state(['disabled'])
    dbldownbutton.state(['disabled'])
    if wallet < 1:
        emptyWallet()
    else:
        startGame()

def updateDraw():
    global wallet, tally
    text('You draw, so your wallet remains at $', int(wallet), '.\n')
    text('Your current sessions winnings(losses) are $', int(tally), '.\n')
    hitbutton.state(['disabled'])
    standbutton.state(['disabled'])
    dbldownbutton.state(['disabled'])
    pushsound.play()
    textoutput.image_create('end', image=pushgraphics)
    updateDb()
    startGame()

# Create function for depleted wallet message
def emptyWallet():
    text('You have nothing left in your wallet. \nThe bouncer will now show you to the door...\n')
    text('\nThanks for playing ', name, '!\n')
    hitbutton.state(['disabled'])
    standbutton.state(['disabled'])
    dbldownbutton.state(['disabled'])
    updateDb()
    displayDb()
    

# Define command functions
def hit(*args):
    global l, L
    text('\nYou hit!\n')
    dbldownbutton.state(['disabled'])
    player_hand.append(game_deck.pop(0))
    if player_hand[-1].value1 == 11:
        if L > 12:
            l.append(player_hand[-1].value2)
        else:
            l.append(player_hand[-1].value1)
    else:
        l.append(player_hand[-1].value1)
    if sum(l) > 21:
        l.sort()
        if l[-1] == 11:
            l[-1] = 1
   
    L = sum(l)
    playerscore.set(L)    
    handDisplay()
    text('Your hand is now worth ', L, ' points.\n')
    if int(playerscore.get()) > 21:
        text('You busted... You lose!!\n')
        updateLose()

    
def doubleDown(*args):
    global bet, wallet, l, L
    if (int(bet) * 2) > wallet:
        text("Can't double down: doing so would exceed current wallet.\n")
        dbldownbutton.state(['disabled'])
    else:
        bet = int(bet * 2)
        betamount.set(bet)
        player_hand.append(game_deck.pop(0))
        if player_hand[-1].value1 == 11:
            if L > 12:
                l.append(player_hand[-1].value2)
            else:
                l.append(player_hand[-1].value1)
        else:
            l.append(player_hand[-1].value1)
        if sum(l) > 21:
            l.sort()
            if l[-1] == 11:
                l[-1] = 1
        L = sum(l)
        playerscore.set(L)    
        handDisplay()
        text('You doubled down, and your hand is now worth ', L, ' points.\n')
        dbldownbutton.state(['disabled'])
        if int(playerscore.get()) > 21:
            text('You busted... You lose!!\n')
            updateLose()
        else:
            stand()

def stand(*args):
    text('You end your turn with ', L, ' points!\n')
    global M, l, m
    while M < 22:
        if M > 17:
            text('Dealer stands with ', M, ' points.\n')
            text('Dealer\'s final hand shows ', M, ' points against your hand of ', L, ' points.\n')
            break
        elif M > 21:
            text('Dealer busts!\n')
            break
        opponent_hand.append(game_deck.pop(0))
        text('Dealer draws ', opponent_hand[-1].title, '.\n')
        if opponent_hand[-1].value1 == 11:
            if M > 12:
                m.append(opponent_hand[-1].value2)
            else:
                m.append(opponent_hand[-1].value1)
        else:
            m.append(opponent_hand[-1].value1)

        if sum(m) > 21:
            m.sort()
            if m[-1] == 11:
                m[-1] = 1
                  
        M = sum(m)
        dealerscore.set(M)
        fullhandDisplay()
        text('Dealer\'s hand now shows ', M, ' points against your hand of ', L, ' points.\n')

    if 22 > L == M:
        text('\nPush!\n')
        fullhandDisplay()
        updateDraw()
    elif 22 > L > M:
        text('\nYou win!!!\n')
        fullhandDisplay()
        updateWin()
    elif 22 > M > L:
        text('\nYou lose...\n')
        fullhandDisplay()
        updateLose()
    elif M > 21:
        text('\nDealer busts! You win!!!\n')
        fullhandDisplay()
        updateWin()
def quitButton():
    root.destroy()
    
# Define procedural functions
def begin(*args):
    try:
        global name, playerstart
        name = playernmentry.get()
        playernm.set(name)
        name_entry.state(['disabled'])
        beginbutton.state(['disabled'])
        startGame()
    except:
        pass

def startGame():
    global name, wallet, surrender, firstgame, player
    
    bet_entry.state(['!disabled'])
    betbutton.state(['!disabled'])
    bet_entry.focus()
    root.bind('<Return>', betfunc)
    surrender = None
    db = shelve.open('highscores')
    if firstgame == False:
        pass
    else:
        if name not in list(db.keys()):
            player = Player(name)
            text('Welcome, ', name, '!\n')
            wallet = int(player.wallet)
            text('As a new player, your wallet will start at: $', int(wallet), '.\n')
            walletamount.set(int(wallet))
        else:
            player = db[name]
            text('Welcome back, ', name, '!\n')
            wallet = int(player.wallet)
            if wallet == 0:
                wallet = 50
                text('OK - looks like you\'ve depleted your wallet.  Here\'s another $50 to get your started.\n')
                walletamount.set(int(wallet))
            else:
                text('Carrying over from last time, your wallet is: $', int(wallet), '.\n')
                walletamount.set(int(wallet))
        db.close()
    db.close()
    firstgame = False
    text('Please enter a bet.\n')
    bet_entry.delete(0, 'end')

def betfunc(*args):
    global bet, wallet
    for x in range(2, len(playercardlabel)):
        playercardlabel[str(x)].grid_forget()
    for x in range(2, len(dealercardlabel)):
        dealercardlabel[str(x)].grid_forget()
    betamount.set(betamountentry.get())
    bettest = betamount.get()
    if (bettest.isdecimal() == False):
        text('Please enter a digit between 1 and your current wallet.\n')
        bet_entry.delete(0, 'end')
        betamount.set('')
    elif int(betamount.get()) < 1 or int(betamount.get()) > wallet:
        text('Your current wallet is $', int(wallet), '.\n')
        text('Please enter a digit between 1 and your current wallet.\n')
        bet_entry.delete(0, 'end')
        betamount.set('')
    else:
        bet = int(betamount.get())
        bet_entry.state(['disabled'])
        betbutton.state(['disabled'])
        text('Ok - you have just bet $', int(bet), '\nSee the cards above.\n')
        coinsound.play()
        hitbutton.state(['!disabled'])
        standbutton.state(['!disabled'])
        dbldownbutton.state(['!disabled'])
        deal()    

def deal(*args):
    global game_deck, deck, player_hand, opponent_hand, l, L, m, M, player_blackjack, opponent_blackjack
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

    # Look at values of each card in both sides' hands, build them into lists, and
    # then sum the lists.
    l = []
    for x in range(len(player_hand)):
        l.append(player_hand[x].value1)

    if sum(l) > 21:
        l.sort()
        if l[-1] == 11:
            l[-1] = 1

    m = []
    for x in range(len(opponent_hand)):
        m.append(opponent_hand[x].value1)

    if sum(m) > 21:
        m.sort()
        if m[-1] == 11:
            m[-1] = 1

    L = sum(l)
    M = sum(m)

    # Update player score display value to reflect newly computed player hand value and
    # update displayed dealer hand value to reflect score of the first (shown) card in dealer hand.
    playerscore.set(L)
    dealerscore.set(m[0])
    
    # Look for blackjack in player and dealer hands.  Respond accordingly in one or both
    # hands is a blackjack (instant win/loss/draw) and update all cards and update score
    # displays.  If no blackjacks, partially update hand scores and card faces.  
    player_blackjack = False
    opponent_blackjack = False
    
    if L == 21:
        player_blackjack = True

    if M == 21:
        opponent_blackjack = True

    if player_blackjack and opponent_blackjack:
        fullhandDisplay()
        dealerscore.set(M)
        text('All hands are blackjack... Push!!!\n')
        updateDraw()
        
    elif player_blackjack:
        fullhandDisplay()
        dealerscore.set(M)
        text('You win with a blackjack!  You get a 1.5x bonus!!!\n')
        updateWin()
        
    elif opponent_blackjack:
        fullhandDisplay()
        dealerscore.set(M)
        text('Dealer has blackjack... you lose!!!\n')
        updateLose()
        
    else:
        #Print opening hands for both sides
        handDisplay()
        text('\nYour hand is worth ', L, ' points.\n')
        text('Dealer\'s hand so far shows ', opponent_hand[0].value1, ' points.\n')

# Create value for default width of textbox and create line of dashes variable
textwidth = 65
LINE_OF_DASHES = '-' * textwidth
    
# Set initial game state (initializing tally and setting first-game flag)
firstgame = True
tally = 0

# Initialize and title root frame and create content frame
root = Tk()
root.title('Blackjack - by Jeff Walters')
main = ttk.Frame(root, width=800, height=600, padding=(3, 3, 12, 12))
root.resizable(width=False, height=False)

# Add various images
graphicspath = 'Graphics\\'
wingraphics = PhotoImage(file=graphicspath+'win.png').subsample(6,6)
losegraphics = PhotoImage(file=graphicspath+'lose.png').subsample(6,6)
pushgraphics = PhotoImage(file=graphicspath+'push.png').subsample(6,6)
bjgraphics = PhotoImage(file=graphicspath+'blackjack.png').subsample(6,6)

# Create variables for text labels
playernmentry = StringVar()
playernm = StringVar()
playernm.set('(Unnamed player)')
dealerscore = StringVar()
playerscore = StringVar()
walletamount = StringVar()
betamount = StringVar()
betamountentry = StringVar()

# Create entry fields for inputting player name ane betting amounts
name_entry = ttk.Entry(main, width=15, textvariable=playernmentry)
bet_entry = ttk.Entry(main, width=15, textvariable=betamountentry, state='disabled')

# Create small text labels
dealerlbl = ttk.Label(main, text='Dealer')
playerlbl = ttk.Label(main, textvariable=playernm)
scorelbl = ttk.Label(main, text='Score')
dealerscorelbl = ttk.Label(main, textvariable=dealerscore)
playerscorelbl = ttk.Label(main, textvariable=playerscore)
walletlbl = ttk.Label(main, text='Current wallet: ')
walletamountlbl = ttk.Label(main, textvariable=walletamount)
betlbl = ttk.Label(main, text='Bet amount: ')
betamountlbl = ttk.Label(main, textvariable=betamount)
enterbetlbl = ttk.Label(main, text='Enter amount to bet: ')

# Create main text output frame and field
textoutput = Text(main, width=textwidth, height=15, wrap='word', state='disabled')

# Create command buttons
hitbutton = ttk.Button(main, text='Hit', command=hit, state=(['disabled']))
dbldownbutton = ttk.Button(main, text='Double Down', command=doubleDown, state=(['disabled']))
standbutton = ttk.Button(main, text='Stand', command=stand, state=(['disabled']))
quitbutton = ttk.Button(main, text='Quit', command=quitButton)
beginbutton = ttk.Button(main, text='Confirm name and begin', command=begin)
displaybutton = ttk.Button(main, text='Hall of Fame', command=displayDb)
betbutton = ttk.Button(main, text='Confirm bet', command=betfunc, state='disabled')

# Contruct deck with list of class objects containing card title, value/alternate
# value, and corresponding image file
imagepath = 'PNG-cards-1.3\\'
suits = ['clubs', 'spades', 'diamonds', 'hearts']
cards = [('ace', 11, 1), ('2', 2, 2), ('3', 3, 3), ('4', 4, 4),
         ('5', 5, 5), ('6', 6, 6), ('7', 7, 7), ('8', 8, 8),
         ('9', 9, 9), ('10', 10, 10), ('jack', 10, 10), ('queen', 10, 10),
         ('king', 10, 10)]
deck = [Card((card[0] + '_of_'+ suit), PhotoImage(file=imagepath+card[0]+'_of_'+suit+'.png').subsample(6,6),
             card[1], card[2]) for card in cards for suit in suits]

# Create hand display functions that link card images to playing card labels
def handDisplay():
    global dimage, pimage, wallet
    walletamount.set(wallet)
    pimage = {}
    dimage = {}
    count = 0
    for x in range(0, 2):
        dimage[str(x)] = opponent_hand[x].image
        pimage[str(x)] = player_hand[x].image
        dealercardlabel[str(x)]['image'] = dimage[str(x)]
        playercardlabel[str(x)]['image'] = pimage[str(x)]
    dealercardlabel['1']['image'] = defimage

    while count < len(player_hand):
        pimage[str(count)] = player_hand[count].image
        playercardlabel[str(count)]['image'] = pimage[str(count)]
        playercardlabel[str(count)].grid(column=count+3, row=3)
        count+=1
        
def fullhandDisplay():
    global dimage, pimage, wallet
    walletamount.set(wallet)
    count = 0
    for x in range(0, 2):
        dimage[str(x)] = opponent_hand[x].image
        pimage[str(x)] = player_hand[x].image
        dealercardlabel[str(x)]['image'] = dimage[str(x)]
        playercardlabel[str(x)]['image'] = pimage[str(x)]

    while count < len(opponent_hand):
        dimage[str(count)] = opponent_hand[count].image
        dealercardlabel[str(count)]['image'] = dimage[str(count)]
        dealercardlabel[str(count)].grid(column=count+3, row=2)
        count+=1
            
# Create playing card labels
defimage = PhotoImage(file=imagepath+'red_joker.png').subsample(6,6)
dealercardlabel = {}
playercardlabel = {}
for x in range(0, 20):
    dealercardlabel[str(x)] = ttk.Label(main, background='red', image=defimage)
    playercardlabel[str(x)] = ttk.Label(main, background='blue', image=defimage)

# Display prompt in main textbox display
text('Please enter your name in the entry box above.\n')

# Grid all widgets
main.grid(column=0, row=0, sticky='nsew')
name_entry.grid(column=1, row=1, sticky='w')
dealerlbl.grid(column=1, row=2, sticky='e')
playerlbl.grid(column=1, row=3, sticky='e')
walletlbl.grid(column=1, row=5)
betlbl.grid(column=1, row=6)
enterbetlbl.grid(column=1, row=7)
beginbutton.grid(column=2, row=1, sticky='w')
textoutput.grid(column=2, columnspan=15, row=4, sticky='nswe')
walletamountlbl.grid(column=2, row=5)
betamountlbl.grid(column=2, row=6)
bet_entry.grid(column=2, row=7)
betbutton.grid(column=3, row=7)
hitbutton.grid(column=13, row=6, sticky='nswe')
dbldownbutton.grid(column=14, row=6, sticky='nswe')
scorelbl.grid(column=15, row=1, sticky='nswe')
dealerscorelbl.grid(column=15, row=2, sticky='nswe')
playerscorelbl.grid(column=15, row=3, sticky='nswe')
standbutton.grid(column=15, row=6, sticky='nswe')
displaybutton.grid(column=16, row=1, sticky='nswe')
quitbutton.grid(column=16, row=6, sticky='nswe')
dealercardlabel['0'].grid(column=3, row=2)
dealercardlabel['1'].grid(column=4, row=2)
playercardlabel['0'].grid(column=3, row=3)
playercardlabel['1'].grid(column=4, row=3)

# Configure scalability for window
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
main.columnconfigure(0, weight=3)
main.columnconfigure(1, weight=3)
main.columnconfigure(2, weight=3)
main.columnconfigure(3, weight=1)
main.columnconfigure(4, weight=1)
main.columnconfigure(5, weight=1)
main.columnconfigure(6, weight=1)
main.columnconfigure(7, weight=1)
main.columnconfigure(8, weight=1)
main.columnconfigure(9, weight=1)
main.columnconfigure(10, weight=1)
main.columnconfigure(11, weight=1)
main.rowconfigure(1, weight=1)

# Set default name entry command for return key
name_entry.focus()
root.bind('<Return>', begin)

# Execute main loop
root.mainloop()
