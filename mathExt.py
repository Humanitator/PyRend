# This file hosts extended math
# i.e. extended infinity support

# Positive infinity
INF = float("INF")

# Get the sign of the number (returns -1 if negative, 1 if positive and 0 if 0)
def sign(num):
    if num > 0:
        return 1
    if num < 0:
        return -1
    return 0


# divide with infinity support (eg. 1 / 0 = infinity)
def div(num1, num2):
    # Check if both numbers are infinity or zero
    if abs(num1) == abs(num2) and (abs(num1) == INF or num1 == 0):
        if sign(num1) == sign(num2):
            return 1
        else:
            return -1
    elif num2 == 0:
        if sign(num1) == sign(num2):
            return INF
        else:
            return -INF
    else:
        return num1 / num2
    
# Multiply with infinity support (eg. infinity * 0 = 0)
def mul(num1, num2):
    if (abs(num1) == INF and num2 == 0) or (num1 == 0 and abs(num2) == INF):
        return 0
    else:
        return num1 * num2

# Sum with infinity support (eg. infinity - infinity = 0)
def sum(num1, num2):
    if num1 == INF and num2 == INF:
        if sign(num1) != sign(num2):
            return 0
    else:
        return num1 + num2
    
# Subtract with infinity support (eg. infinity - infinity = 0)
def sub(num1, num2):
    if num1 == INF and num2 == INF:
        if sign(num1) == sign(num2):
            return 0
    else:
        return num1 - num2