def calcElo(Rating1, Rating2, score):
    K = 32
    score2 = 0.5
    if (score == 1):
        score2 = 0
    elif (score == 0):
        score2 = 1
    
    expected1 = 1/(1+(10 ** ((Rating2 - Rating1)/400)))
    expected2 = 1/(1+(10 ** ((Rating1 - Rating2)/400)))


    elo1 = Rating1 + K * (score - expected1)
    elo2 = Rating2 + K * (score2 - expected2)

    if (score == 1):
        print (f'Player 1 won, and their elo increased from {Rating1} to {elo1}. Player 2 lost, and their elo decreased from {Rating2} to {elo2}.')
    elif (score == 0):
        print (f'Player 2 won, and their elo increased from {Rating2} to {elo2}. Player 2 lost, and their elo decreased from {Rating1} to {elo1}.')
    elif (score == 0.5):
        print (f'The game ended in a draw. Player 1\'s elo changed from {Rating1} to {elo1}, while Player 2\'s elo changed from {Rating2} to {elo2}.')
    else:
        print('something is wrong.')

    boop = [elo1, elo2]
    print(boop)
    return [int(elo1), int(elo2)]

def requestelo():
    R1 = float(input('What was player 1\'s elo before the match?\n'))
    R2 = float(input('What was player 2\'s elo before the match?\n'))
    score = float(input('what was the outcome of the game?\n'))
    calcElo(R1, R2, score)

def lalala():
    print('ooooooo')

#while True:
 #   requestelo()