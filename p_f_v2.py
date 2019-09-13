import numpy as np

DECAY_RATE = .9999995
# if some random number is less than epsilon, a random number is chosen
epsilon_minimum = .1
# learning rate
alpha = .001
N = 1

def readFile():
    equity_data = np.loadtxt('equity.dat')
    return equity_data

def dealHands():
    x_hand, y_hand = [[], []], [[], []]
    
    # suits
    highest_suit = 1
    x_hand[0].append(0)
    rand = 4 * np.random.rand(3)
    for i in range(len(rand)):
        rand[i] = int(rand[i])
    
    if rand[0] == highest_suit:
        x_hand[1].append(rand[0])
    else:
        x_hand[1].append(highest_suit)
        highest_suit += 1
    
    for i in range(highest_suit):
        if rand[1] == i:
            y_hand[0].append(rand[1])
            highest_suit += 1
            break
        if i == highest_suit - 1:
            y_hand[0].append(highest_suit)
            highest_suit += 1
    
    for i in range(highest_suit):
        if rand[2] == i:
            y_hand[1].append(rand[2])
            break
        if i == highest_suit - 1:
            y_hand[1].append(highest_suit)
    
    # ranks
    rand = 13 * np.random.rand(4)
    for i in range(len(rand)):
        rand[i] = int(rand[i])
    x_hand[0].insert(0, rand[0])
    x_hand[1].insert(0, rand[1])
    y_hand[0].insert(0, rand[2])
    y_hand[1].insert(0, rand[3])
    if x_hand[0] == x_hand[1] or x_hand[0] == y_hand[0] or x_hand[0] == y_hand[1]:
        return dealHands()
    if x_hand[1] == y_hand[0] or x_hand[1] == y_hand[1]:
        return dealHands()
    if y_hand[0] == y_hand[1]:
        return dealHands()
    return x_hand, y_hand

def makeFeatures(z_hand, z_action):
    if z_hand[0][1] == z_hand[1][1]:
        z_suited = True
    else:
        z_suited = False
    phi = [1,
           z_hand[0][0]/13,
           z_hand[1][0]/13,
           (z_hand[0][0] - z_hand[1][0])**2,
           1 if z_suited else 0,
           1 if z_action else 0]
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
        return z_action, z_phi_aggressive

def computeEquity(equity_data, x_hand, y_hand):
    count = 0
    x_equity = 0
    for i in range(len(equity_data)):
        for j in range(0, 8, 2):
            if x_hand[0][0] == equity_data[i][j] and x_hand[0][1] == equity_data[i][j + 1] and \
               x_hand[1][0] == equity_data[i][j + 2] and x_hand[1][1] == equity_data[i][j + 3] or \
               x_hand[0][0] == equity_data[i][j + 2] and x_hand[0][1] == equity_data[i][j + 3] and \
               x_hand[1][0] == equity_data[i][j] and x_hand[1][1] == equity_data[i][j + 1]:
                for k in range(0, 8, 2):
                    if y_hand[0][0] == equity_data[i][k] and y_hand[0][1] == equity_data[i][k + 1] and \
                       y_hand[1][0] == equity_data[i][k + 2] and y_hand[1][1] == equity_data[i][k + 3] or\
                       y_hand[0][0] == equity_data[i][k + 2] and y_hand[0][1] == equity_data[i][k + 3] and \
                       y_hand[1][0] == equity_data[i][k] and y_hand[1][1] == equity_data[i][k + 1]:
#                        print(equity_data[i])
#                        print(x_hand)
#                        print(y_hand)
#                        print("\n")
#                        print(equity_data[i][8], equity_data[i][9], equity_data[i][10])
                        count += 1
                        if x_hand[0][0] == equity_data[i][0] or x_hand[0][0] == equity_data[i][2]:
                            x_equity = equity_data[i][8]/(equity_data[i][8] + equity_data[i][9] + equity_data[i][10])
                        else:
                            x_equity = equity_data[i][9]/(equity_data[i][8] + equity_data[i][9] + equity_data[i][10])
    print(count)
    return x_equity

def createEquityLookup(equity_data):
    n = 0
    hands = []
    for i in range(13):
        for j in range(4):
            for k in range(13):
                for l in range(4):
                    for m in range(13):
                        for o in range(4):
                            for p in range(13):
                                for q in range(4):
                                    hands.append([i, j, k, l, m, o, p, q])
                                    n += 1
    print("n = ", n)
#    return equity_lookup

def showDown(x_equity, x_stack, y_stack, p):
    rand = np.random.rand(1)
    print("x_equity = ", x_equity)
    if x_equity > rand[0]:
        x_stack += p
    else:
        y_stack += p
    return x_stack, y_stack

def updateTheta(x_theta, y_theta, x_phi, y_phi, x_stack, y_stack):
    Q_x = computeSum(x_theta, x_phi)
    Q_y = computeSum(y_theta, y_phi)
    
    x_theta += alpha * (x_stack - Q_x) * x_phi
    y_theta += alpha * (y_stack - Q_y) * y_phi
    return x_theta, y_theta

def main():
    epsilon = 1
    equity_data = readFile()
    x_theta = np.ones(6)
    y_theta = np.ones(6)
    for n in range(N):
        s = 10
        p = 1.5
        x_stack, y_stack = 9.5, 9
        
        x_hand, y_hand = dealHands()
        print("x_hand, y_hand = ", x_hand, y_hand)
        x_equity = computeEquity(equity_data, x_hand, y_hand)
        
        x_push, x_phi = pickAction(x_hand, x_theta, epsilon)
        y_call, y_phi = pickAction(y_hand, y_theta, epsilon)
        print(x_push, y_call)
        x_push, y_call = True, True
        if x_push:
            if y_call:
                p = 2 * s
                x_stack, y_stack = 0, 0
                x_stack, y_stack = showDown(x_equity, x_stack, y_stack, p)
            else:
                x_stack += p
        else:
            y_stack += p
        
        x_theta, y_theta = updateTheta(x_theta, y_theta, x_phi, y_phi, x_stack, y_stack)
        print(x_theta, y_theta)
        print(x_stack, y_stack)

#main()

def tester():
    equity_data = readFile()
#    x_hand, y_hand = dealHands()
#    print(x_hand, y_hand)
#    equity = computeEquity(equity_data, x_hand, y_hand)
#    print(equity)
    createEquityLookup(equity_data)
tester()


