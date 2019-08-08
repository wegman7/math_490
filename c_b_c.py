import numpy as np
import matplotlib.pyplot as plt

DECAY_RATE = .99999991
# if some random number is less than epsilon, a random number is chosen
epsilon_minimum = .1
# learning rate
alpha = .0001
N = 10000000

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
        if np.argmax(Q_x[x_hand][:2]) == True:
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
#    # we do this so that x picks from the best option of either a bet, or the weighted average of the ev of check/fold and check/call
#    count = 0
#    total_ev_check_fold = 0
#    total_ev_check_call = 0
#    count2 = 0
#    for i in range(len(Q_x)):
#        if np.argmax(Q_x[i][-2:]) == 0:
#            total_ev_check_fold += Q_x[i][2]
#            count += 1
#        else:
#            total_ev_check_call += Q_x[i][3] # this shouldn't ever change
#            count2 += 1
#    print(Q_x[0][2], Q_x[0][3])
#    print(count)
#    print(count2)
#    percentage_check_fold = count / len(Q_x)
#    percentage_check_call = 1 - percentage_check_fold
#    print(total_ev_check_fold * percentage_check_fold, total_ev_check_call * percentage_check_call)
#    if total_ev_check_fold * percentage_check_fold > total_ev_check_call * percentage_check_call:
#        best_future_action = 2
#    else:
#        best_future_action = 3
#    print("best future action = ", best_future_action)
##    input()
#    Q_x[x_hand][0] = max(Q_x[x_hand][2], Q_x[x_hand][best_future_action])
    pass

def printResults(Q_x, Q_y):
    hand_axis = []
    action_axis_x_bet = []
    action_axis_y_call = []
    action_axis_x_call = []
    action_axis_y_bet = []
    for i in range(100):
        hand_axis.append(i)
        action_axis_x_bet.append(np.argmax(Q_x[i][:2]))
        action_axis_y_call.append(np.argmax(Q_y[i][:2]))
        action_axis_x_call.append(np.argmax(Q_x[i][-2:]))
        action_axis_y_bet.append(np.argmax(Q_y[i][-2:]))
    plt.plot(hand_axis, action_axis_x_bet, label='x bet')
    plt.plot(hand_axis, action_axis_y_call, label='y call')
    plt.plot(hand_axis, action_axis_x_call, label='x call')
    plt.plot(hand_axis, action_axis_y_bet, label='y bet')
    plt.legend()
    plt.show()
    print(Q_x)
    print("\n\n")
    print(Q_y)
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