import numpy as np
import matplotlib.pyplot as plt

DECAY_RATE = .99999992
# if some random number is less than epsilon, a random number is chosen
epsilon_minimum = .1
# learning rate
alpha = .0001
N = 20000000

def pickAction(x_hand, y_hand, Q_x, Q_y, epsilon):
    rand = np.random.rand(8)
    # the first two if statements are for x_bet and y_call
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
#        if np.argmax(Q_x[x_hand][:2]) == True:
        if np.argmax(Q_x[x_hand][-3:]) == 1:
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
        if np.argmax(Q_y[y_hand][:2]) == True:
            y_call = True
        else:
            y_call = False
    
    
    # these second two if statements are for x_call and y_bet
    # take random action if some random number < epsilon
    if rand[4] < epsilon:
#        print("random")
        if rand[5] > .5:
            x_call = True
        else:
            x_call = False
    # take action with highest q value if some random number > epsilon
    else:
#        print("not random")
        if np.argmax(Q_x[x_hand][-2:]) == True:
            x_call = True
        else:
            x_call = False
    
    # take random action if some random number < epsilon
    if rand[6] < epsilon:
#        print("random")
        if rand[7] > .5:
            y_bet = True
        else:
            y_bet = False
    # take action with highest q value if some random number > epsilon
    else:
#        print("not random")
        if np.argmax(Q_y[y_hand][-2:]) == True:
            y_bet = True
        else:
            y_bet = False
    return x_bet, y_call, x_call, y_bet

def showDown(x_hand, x_stack, y_hand, y_stack, p):
    if x_hand > y_hand:
        x_stack += p
    elif y_hand > x_hand:
        y_stack += p
    return x_stack, y_stack

def updateQ(x_stack, y_stack, x_hand, y_hand, x_bet, y_call, x_call, y_bet, Q_x, Q_y):
    if x_bet:
        Q_x[x_hand][x_bet] = Q_x[x_hand][x_bet] + alpha * (x_stack - Q_x[x_hand][x_bet])
        Q_y[y_hand][y_call] = Q_y[y_hand][y_call] + alpha * (y_stack - Q_y[y_hand][y_call])
    elif not x_bet:
        Q_x[x_hand][x_bet] = Q_x[x_hand][x_bet] + alpha * (x_stack - Q_x[x_hand][x_bet])
        Q_x[x_hand][x_call + 2] = Q_x[x_hand][x_call + 2] + alpha * (x_stack - Q_x[x_hand][x_call + 2])
        Q_y[y_hand][y_bet + 2] = Q_y[y_hand][y_bet + 2] + alpha * (y_stack - Q_y[y_hand][y_bet + 2])
    pass

def printResults(Q_x, Q_y):
    for i in range(100):
        print(Q_x[i])
    print("\n\n")
    for i in range(100):
        print(Q_y[i])
#    hand_axis = []
#    action_axis_x_bet = []
#    action_axis_y_call = []
#    action_axis_x_call = []
#    action_axis_y_bet = []
#    for i in range(100):
#        hand_axis.append(i)
#        action_axis_x_bet.append(np.argmax(Q_x[i][:2]))
#        action_axis_y_call.append(np.argmax(Q_y[i][:2]))
#        action_axis_x_call.append(np.argmax(Q_x[i][-2:]))
#        action_axis_y_bet.append(np.argmax(Q_y[i][-2:]))
#    plt.plot(hand_axis, action_axis_x_bet, label='x bet')
#    plt.plot(hand_axis, action_axis_y_call, label='y call')
#    plt.plot(hand_axis, action_axis_x_call, label='x call')
#    plt.plot(hand_axis, action_axis_y_bet, label='y bet')
#    plt.legend()
#    plt.show()
    
    hand_axis = []
#    q_axis_x_check = []
    q_axis_x_bet = []
    q_axis_x_fold = []
    q_axis_x_call = []
    for i in range(100):
        hand_axis.append(i)
#        q_axis_x_check.append(Q_x[i][0])
        q_axis_x_bet.append(Q_x[i][1])
        q_axis_x_fold.append(Q_x[i][2])
        q_axis_x_call.append(Q_x[i][3])
#    plt.plot(hand_axis, q_axis_x_check, label='x check')
    plt.plot(hand_axis, q_axis_x_bet, label='x bet')
    plt.plot(hand_axis, q_axis_x_fold, label='x check/fold')
    plt.plot(hand_axis, q_axis_x_call, label='x check/call')
    plt.legend()
    plt.show()
    
    hand_axis = []
    q_axis_y_fold = []
    q_axis_y_call = []
    q_axis_y_check = []
    q_axis_y_bet = []
    for i in range(100):
        hand_axis.append(i)
        q_axis_y_fold.append(Q_y[i][0])
        q_axis_y_call.append(Q_y[i][1])
        q_axis_y_check.append(Q_y[i][2])
        q_axis_y_bet.append(Q_y[i][3])
    plt.plot(hand_axis, q_axis_y_fold, label='y fold')
    plt.plot(hand_axis, q_axis_y_call, label='y call')
    plt.plot(hand_axis, q_axis_y_check, label='y check')
    plt.plot(hand_axis, q_axis_y_bet, label='y bet')
    plt.legend()
    plt.show()
    
    pass

def main():
    epsilon = 1
    # ev of bet and check (and call and fold) for different states
#    Q_x = [[ev of check, ev of bet, ev of fold, ev of call], ...]
#    Q_y = [[ ev of fold, ev of call, ev of check, ev of bet], ...]
    Q_x = [[9.5 for i in range(4)] for j in range(100)]
    Q_y = [[9.5 for i in range(4)] for j in range(100)]
    
    for n in range(N):
        s = 10
        p = 1
        b = 1
        x_stack, y_stack = s - .5 * p, s - .5 * p
        x_hand = np.random.randint(0, 100)
        while True:
            y_hand = np.random.randint(0, 100)
            if y_hand != x_hand:
                break
        x_bet, y_call, x_call, y_bet = pickAction(x_hand, y_hand, Q_x, Q_y, epsilon)
        if x_bet:
            if y_call:
#                print("bet/call")
                p += 2 * b
                x_stack -= b
                y_stack -= b
                x_stack, y_stack = showDown(x_hand, x_stack, y_hand, y_stack, p)
            elif not y_call:
#                print("bet/fold")
                x_stack += p
        elif not x_bet:
            if y_bet:
                if x_call:
#                    print("check/bet/call")
                    p += 2 * b
                    x_stack -= b
                    y_stack -= b
                    x_stack, y_stack = showDown(x_hand, x_stack, y_hand, y_stack, p)
                if not x_call:
#                    print("check/bet/fold")
                    y_stack += p
            elif not y_bet:
#                print("check/check")
                x_stack, y_stack = showDown(x_hand, x_stack, y_hand, y_stack, p)
#        input()
        updateQ(x_stack, y_stack, x_hand, y_hand, x_bet, y_call, x_call, y_bet, Q_x, Q_y)
        epsilon = max(epsilon * DECAY_RATE, epsilon_minimum)
        if n % 200000 == 0:
            print("%d / %d" % (n/10000, N/10000))
            print("exploration: ", epsilon)
    printResults(Q_x, Q_y)
main()