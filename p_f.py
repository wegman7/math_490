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

def dealHand():
    x_hand, y_hand = [[], []], [[], []]
    while True:
        rand = 52 * np.random.rand(4)
        if int(rand[0]) != int(rand[1]) and int(rand[0]) !=  int(rand[2]) and int(rand[0]) !=  int(rand[3]):
            if int(rand[1]) != int(rand[2]) and int(rand[1]) != int(rand[3]):
                if int(rand[2]) != int(rand[3]):
                    break
    # first card for each player
    x_hand[0].append(int(rand[0]) % 13 + 2)
    x_hand[0].append(int(rand[0]) % 4 + 1)
    y_hand[0].append(int(rand[1]) % 13 + 2)
    y_hand[0].append(int(rand[1]) % 4 + 1)
    # second card for each player
    x_hand[1].append(int(rand[2]) % 13 + 2)
    x_hand[1].append(int(rand[2]) % 4 + 1)
    y_hand[1].append(int(rand[3]) % 13 + 2)
    y_hand[1].append(int(rand[3]) % 4 + 1)
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
#    equity_lookup = [[-1 for i in range(13)]]
#    equity_lookup.append([-1 for j in range(4)])
#    equity_lookup.append([-1 for k in range(13)])
#    equity_lookup.append([-1 for l in range(4)])
    
    equity_lookup = []
    for i in range(13):
        equity_lookup.append([])
        for j in range(4):
            equity_lookup[i].append([])
            for k in range(13):
                equity_lookup[i][j].append([])
                for l in range(4):
                    equity_lookup[i][j][k].append(-1)
                    
    print(equity_lookup)
    for i in range(len(equity_data)):
        equity_lookup[equity_data[i][0] - 2][equity_data[i][1] - 1][equity_data[i][2] - 2][equity_data[i][3] - 1]\
        [equity_data[i][4] - 2][equity_data[i][5] - 1][equity_data[i][6] - 2][equity_data[i][7] - 1] = \
                equity_data[i][9]/(equity_data[i][9] + equity_data[i][10] + equity_data[i][11])
    return equity_lookup

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
        
        x_hand, y_hand = dealHand()
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
    equity_lookup = createEquityLookup(equity_data)
tester()


