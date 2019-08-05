import sys
import numpy as np
#np.set_printoptions(threshold=sys.maxsize)

DECAY_RATE = .99999993
# if some random number is less than epsilon, a random number is chosen
epsilon_minimum = .1
# learning rate
alpha = .00004
N = 50000000

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

def makeFeatures(z_hand, z_action):
    if z_hand[0][1] == z_hand[1][1]:
        z_suited = True
    else:
        z_suited = False
    phi = [1,
           z_hand[0][0]/13 if z_action else 0,
           z_hand[1][0]/13 if z_action else 0,
           (z_hand[0][0] - z_hand[1][0])**2 if z_action else 0,
           1 if (z_suited and z_action) else 0,
           1 if (z_action and z_action) else 0,
           1 if z_hand[0][0] == z_hand[1][0] and z_action else 0]
    return np.array(phi)

def computeSum(theta_z, phi_z):
    return np.sum(theta_z * phi_z)

def pickAction(z_hand, theta_z, epsilon):
    z_phi_aggressive = makeFeatures(z_hand, True)
    z_phi_passive = makeFeatures(z_hand, False)
    
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
        z_action = computeSum(theta_z, z_phi_aggressive) > computeSum(theta_z, z_phi_passive)
    if z_action == True:
        return z_action, z_phi_aggressive
    else:
        return z_action, z_phi_passive

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

def updateTheta(x_theta, y_theta, x_phi, y_phi, x_stack, y_stack):
    Q_x = computeSum(x_theta, x_phi)
    Q_y = computeSum(y_theta, y_phi)
    
    x_theta += alpha * (x_stack - Q_x) * x_phi
    y_theta += alpha * (y_stack - Q_y) * y_phi
    return x_theta, y_theta

def createVisualization(z_hand, z_theta):
    z_visualize = [[0 for j in range(13)] for i in range(13)]
    for i in range(13):
        for j in range(13):
            z_phi_aggressive, z_phi_passive = makeFeatures([[i, 1], [j, i > j]], True), \
                                              makeFeatures([[i, 1], [j, i > j]], False)
            z_EV_push, z_EV_fold = computeSum(z_phi_aggressive, z_theta), \
                                   computeSum(z_phi_passive, z_theta)
            if z_EV_push > z_EV_fold:
                z_visualize[i][j] = 1
#            if x_EV_push > x_EV_fold:
#                x_visualize[12 - i][12 - j] = 1
#            if y_EV_call > y_EV_fold:
#                y_visualize[12 - i][12 - j] = 1
#    for i in range(13):
#        print(x_visualize[i])
#    print("\n\n")
#    for i in range(13):
#        print(y_visualize[i])
    for i in range(12, -1, -1):
        print("")
        for j in range(12, -1, -1):
            print(z_visualize[i][j], end = " ")
    print("")
    pass

def printUpdate(x_theta, y_theta, epsilon, n):
    print("\n")
    print("%d / %d" %(n/10000, N/10000))
    print("exploration: ", epsilon)
    print("x_theta = ", x_theta)
    print("y_theta = ", y_theta)
    pass
    

def main():
    epsilon = 1
    x_theta = np.ones(7)
    y_theta = np.ones(7)
    file_data = readFile()
    table = createTable()
    x_win, y_win, tie = createEquityFunctions(file_data, len(table))
    for n in range(N):
        s = 10
        p = 1.5
        x_stack, y_stack = 9.5, 9
        
        x_hand, y_hand = dealHands()
        hands = x_hand[0] + x_hand[1] + y_hand[0] + y_hand[1]
        x_equity = x_win[lineLookup(hands)]
        y_equity = y_win[lineLookup(hands)]
#        tie_equity = tie[lineLookup(hands)]
        x_push, x_phi = pickAction(x_hand, x_theta, epsilon)
        y_call, y_phi = pickAction(y_hand, y_theta, epsilon)
#        x_push, y_call = True, True
        if x_push:
            if y_call:
                p = 2 * s
                x_stack, y_stack = 0, 0
                x_stack, y_stack = showDown(x_equity, y_equity, x_stack, y_stack, p)
            else:
                x_stack += p
        else:
            y_stack += p
        
        x_theta, y_theta = updateTheta(x_theta, y_theta, x_phi, y_phi, x_stack, y_stack)
        epsilon = epsilon * DECAY_RATE
        epsilon = max(epsilon, epsilon_minimum)
        if n % 200000 == 0:
            printUpdate(x_theta, y_theta, epsilon, n)
            createVisualization(x_hand, x_theta)
            createVisualization(y_hand, y_theta)

main()