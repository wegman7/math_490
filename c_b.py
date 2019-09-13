import numpy as np
import matplotlib.pyplot as plt

DECAY_RATE = .99999991
# if some random number is less than epsilon, a random number is chosen
epsilon_minimum = .1
# learning rate
alpha = .0001
N = 10000000

def pickAction(x_hand, y_hand, Q_x, Q_y, epsilon):
    rand = np.random.rand(4)
    # take random action if some random number < epsilon
    if rand[0] < epsilon:
#        print("random")
        if rand[1] > .5:
            x_bet = True
        else:
            x_bet = False
    # take action with highest q value if some random number > epsilon
    else:
#        print("not random")
        if np.argmax(Q_x[x_hand]) == True:
            x_bet = True
        else:
            x_bet = False
    
    # take random action if some random number < epsilon
    if rand[2] < epsilon:
#        print("random")
        if rand[3] > .5:
            y_call = True
        else:
            y_call = False
    # take action with highest q value if some random number > epsilon
    else:
#        print("not random")
        if np.argmax(Q_y[y_hand]) == True:
            y_call = True
        else:
            y_call = False
    return x_bet, y_call

def showDown(x_hand, x_stack, y_hand, y_stack, p):
    if x_hand > y_hand:
        x_stack += p
    elif y_hand > x_hand:
        y_stack += p
    else:
        x_stack += .5 * p
        y_stack += .5 * p
    return x_stack, y_stack

def updateQ(x_stack, y_stack, x_hand, y_hand, x_bet, y_call, Q_x, Q_y):
    Q_x[x_hand][x_bet] = Q_x[x_hand][x_bet] + alpha * (x_stack - Q_x[x_hand][x_bet])
    Q_y[y_hand][y_call] = Q_y[y_hand][y_call] + alpha * (y_stack - Q_y[y_hand][y_call])
    return Q_x, Q_y

def printResults(Q_x, Q_y):
    hand_axis = []
    action_axis_x = []
    action_axis_y = []
    for i in range(100):
        hand_axis.append(i)
        action_axis_x.append(np.argmax(Q_x[i]))
        action_axis_y.append(np.argmax(Q_y[i]))
    
    plt.plot(hand_axis, action_axis_x, label='bet/check')
    plt.plot(hand_axis, action_axis_y, label='call/fold')
    plt.legend()
    plt.show()
        
    print(Q_x)
    print("\n\n")
    print(Q_y)
#    for i in range(len(Q_x)):
#        print(i, np.argmax(Q_x[i]))
#    print("\n\n")
#    for i in range(len(Q_x)):
#        print(i, np.argmax(Q_y[i]))
    pass

def main():
    epsilon = 1
    # ev of bet and check (or call and fold) for different states
#    Q_x = [[ev of bet, ev of check], ...]
    Q_x = [[10 for i in range(2)] for j in range(100)]
    Q_y = [[10 for i in range(2)] for j in range(100)]
    
    for n in range(N):
        s = 10
        p = 1
        b = 1
        x_stack, y_stack = s - .5 * p, s - .5 * p
        x_hand = np.random.randint(0, 100)
        y_hand = np.random.randint(0, 100)
        x_bet, y_call = pickAction(x_hand, y_hand, Q_x, Q_y, epsilon)
        if x_bet:
            if y_call:
                p += 2 * b
                x_stack -= b
                y_stack -= b
                x_stack, y_stack = showDown(x_hand, x_stack, y_hand, y_stack, p)
            elif not y_call:
                x_stack += p
        elif not x_bet:
            x_stack, y_stack = showDown(x_hand, x_stack, y_hand, y_stack, p)
        Q_x, Q_y = updateQ(x_stack, y_stack, x_hand, y_hand, x_bet, y_call, Q_x, Q_y)
        epsilon = max(epsilon * DECAY_RATE, epsilon_minimum)
#        print(epsilon)
        if n % 50000 == 0:
            print("%d / %d" % (n/10000, N/10000))
            print("exploration: ", epsilon)
    printResults(Q_x, Q_y)
main()