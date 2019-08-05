import sys
import numpy as np
#np.set_printoptions(threshold=sys.maxsize)

DECAY_RATE = .9999993
# if some random number is less than epsilon, a random number is chosen
epsilon_minimum = .1
# learning rate
alpha = .00001
N = 3000000

def readFile():
    file_data = np.loadtxt('equity.dat')
    # converts data into the format of 0-12 suits and 0-3 ranks, as well as equities into percentages
    for i in range(len(file_data)):
        file_data[i][0] -= 2
        file_data[i][1] -= 1
        file_data[i][2] -= 2
        file_data[i][3] -= 1
        file_data[i][4] -= 2
        file_data[i][5] -= 1
        file_data[i][6] -= 2
        file_data[i][7] -= 1
        temp1 = file_data[i][8]/(file_data[i][8] + file_data[i][9] + file_data[i][10])
        temp2 = file_data[i][9]/(file_data[i][8] + file_data[i][9] + file_data[i][10])
        file_data[i][10] = file_data[i][10]/(file_data[i][8] + file_data[i][9] + file_data[i][10])
        file_data[i][8] = temp1
        file_data[i][9] = temp2
    file_data_with_duplicates = []
    for i in range(len(file_data)):
        file_data_with_duplicates.append(file_data[i])
        temp = [file_data[i][0], file_data[i][1], file_data[i][2], file_data[i][3], file_data[i][6], \
                file_data[i][7], file_data[i][4], file_data[i][5], file_data[i][8], file_data[i][9], file_data[i][10]]
        file_data_with_duplicates.append(temp)
    file_data_with_duplicates = np.array(file_data_with_duplicates)
    return file_data_with_duplicates

def dealHands():
    x_hand, y_hand = [], []
    # deal 4 multually exclusive hands from 0-51
    while True:
        rand0, rand1, rand2, rand3 = np.random.randint(52), np.random.randint(52), np.random.randint(52), np.random.randint(52)
        if rand0 != rand1 and rand0 != rand2 and rand0 != rand3:
            if rand1 != rand2 and rand1 != rand3:
                if rand2 != rand3:
                    break
    card0, card1, card2, card3 = [rand0 % 13, rand0 % 4], [rand1 % 13, rand1 % 4], [rand2 % 13, rand2 % 4], [rand3 % 13, rand3 % 4]
    # set first card suit to 0
    if card0[1] != 0:
            suit = card0[1]
            card0[1] = 0
            if card1[1] == 0:
                card1[1] = suit
            elif card1[1] == suit:
                card1[1] = 0
            if card2[1] == 0:
                card2[1] = suit
            elif card2[1] == suit:
                card2[1] = 0
            if card3[1] == 0:
                card3[1] = suit
            elif card3[1] == suit:
                card3[1] = 0
#    if the suit of card1 isn't 0 or 1, change its suit to 1
    if card1[1] > 1:
        suit = card1[1]
        card1[1] = 1
        if card2[1] == 1:
            card2[1] = suit
        elif card2[1] == suit:
            card2[1] = 1
        if card3[1] == 1:
            card3[1] = suit
        elif card3[1] == suit:
            card3[1] = 1
    # if suited and rank of card0 > card1, swap cards
    if card0[1] == card1[1]:
        if card0[0] > card1[0]:
            temp_card = card0
            card0 = card1
            card1 = temp_card
    # if not suited and rank of card0 < card1, swap cards
    if card0[1] != card1[1]:
        if card0[0] < card1[0]:
            temp_card = card0
            card0 = card1
            card1 = temp_card
            card0[1] = 0
            card1[1] = 1
            if card2[1] == 0:
                card2[1] = 1
            elif card2[1] == 1:
                card2[1] = 0
            if card3[1] == 0:
                card3[1] = 1
            elif card3[1] == 1:
                card3[1] = 0
    # if the rank of card2 > card3, swap cards
    if card2[0] > card3[0]:
        temp_card = card2
        card2 = card3
        card3 = temp_card
    # if the suit of card2 > card3 and the ranks are equal, swap cards
    if card2[0] == card3[0] and card2[1] > card3[1]:
        temp_card = card2
        card2 = card3
        card3 = temp_card
    x_hand.append(card0)
    x_hand.append(card1)
    y_hand.append(card2)
    y_hand.append(card3)
    return x_hand, y_hand

def createHandNumber(z_hand):
    hand_matrix = [[0 for j in range(13)] for i in range(13)]
    if z_hand[0][1] == z_hand[1][1]:
        hand_matrix[max(z_hand[0][0], z_hand[1][0])][min(z_hand[0][0], z_hand[1][0])] = 1
    else:
        hand_matrix[min(z_hand[0][0], z_hand[1][0])][max(z_hand[0][0], z_hand[1][0])] = 1
    n = 0
    for i in range(12, -1, -1):
        for j in range(12, -1, -1):
            if hand_matrix[i][j] == 1:
                return n
            n += 1

def pickAction(hand_number, Q_z, epsilon):
    rand = np.random.rand(2)
    # take random action if some random number < epsilon
    if rand[0] < epsilon:
#        print("random")
        if rand[1] > .5:
            z_action = True
        else:
            z_action = False
    # take action with highest q value if some random number > epsilon
    else:
#        print("not random")
        z_action = np.argmax(Q_z[hand_number])
    return z_action

# creates a table mapped from a line number
def createTable():
    n = 0
    table = []
    for i in range(13):
        for j in range(4):
            for k in range(13):
                for l in range(4):
                    for m in range(13):
                        for o in range(4):
                            for p in range(13):
                                for q in range(4):
                                    table.append([i, j, k, l, m, o, p, q])
                                    n += 1
    return table

# given any hand (formatted corrected), function returns its line number from the table
def lineLookup(hands):
    line = (hands[0] * 4 * 13 * 4 * 13 * 4 * 13 * 4) + \
           (hands[1] * 13 * 4 * 13 * 4 * 13 * 4) + \
           (hands[2] * 4 * 13 * 4 * 13 * 4) + \
           (hands[3] * 13 * 4 * 13 * 4) + \
           (hands[4] * 4 * 13 * 4) + \
           (hands[5] * 13 * 4) + \
           (hands[6] * 4) + \
           (hands[7])
    return line

def createEquityFunctions(file_data, N):
    x_win = [0 for i in range(N)]
    y_win = [0 for i in range(N)]
    tie = [0 for i in range(N)]
    for i in range(len(file_data)):
        line = int(lineLookup(file_data[i][:-3]))
        x_win[line] = file_data[i][8]
        y_win[line] = file_data[i][9]
        tie[line] = file_data[i][10]
    return x_win, y_win, tie

def showDown(x_equity, y_equity, x_stack, y_stack, p):
    # where either player can win the entire pot
#    rand = np.random.rand(1)
#    if rand[0] < x_equity:
#        x_stack += p
#    elif rand[0] > x_equity and rand[0] < x_equity + y_equity:
#        y_stack += p
#    else:
#        x_stack += .5 * p
#        y_stack += .5 * p
    # where each player takes his equity share of the pot (this might make convergence faster)
    x_stack += x_equity * p + .5 * (1 - (x_equity + y_equity))
    y_stack += y_equity * p + .5 * (1 - (x_equity + y_equity))
    return x_stack, y_stack

def updateQ(Q_z, z_stack, z_hand_number, action):
    Q_z[z_hand_number][action] += alpha * (z_stack - Q_z[z_hand_number][action])
    return Q_z

def createVisualization(Q_z):
    n = 0
    for i in range(13):
        print("")
        for j in range(13):
            print(np.argmax(Q_z[n]), end = " ")
            n += 1
    print("")
    total_aggressive = 0
    for i in range(len(Q_z)):
        if np.argmax(Q_z[i]) == 1:
            total_aggressive += 1
    print(total_aggressive/len(Q_z))
    pass

def printUpdate(Q_x, Q_y, epsilon, n):
    print("\n\n")
    print("%d / %d" %(n/100, N/100))
    print("exploration: ", epsilon)
#    print("Q_x = ", Q_x)
#    print("Q_y = ", Q_y)
    pass

def main():
    epsilon = 1
    Q_x = [[9 for j in range(2)] for i in range(169)]
    Q_y = [[9 for j in range(2)] for i in range(169)]
    file_data = readFile()
    table = createTable()
    x_win, y_win, tie = createEquityFunctions(file_data, len(table))
    for n in range(N):
        s = 10
        p = 1.5
        x_stack, y_stack = 9.5, 9
        
        x_hand, y_hand = dealHands()
        x_hand_number = createHandNumber(x_hand)
        y_hand_number = createHandNumber(y_hand)
        hands = x_hand[0] + x_hand[1] + y_hand[0] + y_hand[1]
        x_equity = x_win[lineLookup(hands)]
        y_equity = y_win[lineLookup(hands)]
#        tie_equity = tie[lineLookup(hands)]
        x_push = pickAction(x_hand_number, Q_x, epsilon)
        y_call = pickAction(y_hand_number, Q_y, epsilon)
        if x_push:
            if y_call:
                p = 2 * s
                x_stack, y_stack = 0, 0
                x_stack, y_stack = showDown(x_equity, y_equity, x_stack, y_stack, p)
            else:
                x_stack += p
        else:
            y_stack += p
        
        Q_x = updateQ(Q_x, x_stack, x_hand_number, x_push)
        Q_y = updateQ(Q_y, y_stack, y_hand_number, y_call)
        epsilon = epsilon * DECAY_RATE
        epsilon = max(epsilon, epsilon_minimum)
        if n % 100000 == 0:
            printUpdate(Q_x, Q_y, epsilon, n)
            createVisualization(Q_x)
            createVisualization(Q_y)

main()