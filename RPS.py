import random

# Global state
opponent_history = []
my_history = []
round_num = 0

def beats(move):
    return {'R': 'P', 'P': 'S', 'S': 'R'}[move]

def most_common(history):
    return max(['R', 'P', 'S'], key=history.count)

def counter_quincy():
    # Quincy cycles R → P → S
    cycle = ['R', 'P', 'S']
    if not opponent_history:
        return 'P'
    last = opponent_history[-1]
    next_index = (cycle.index(last) + 1) % 3
    return beats(cycle[next_index])

def counter_abbey():
    # Abbey mimics your previous move
    if not my_history:
        return 'R'
    return beats(my_history[-1])

def counter_kris():
    # Kris favors one move more often
    if not opponent_history:
        return 'R'
    freq = most_common(opponent_history)
    return beats(freq)

def counter_mrugesh():
    # Mrugesh uses last 3 opponent moves to predict next
    if len(opponent_history) < 3:
        return random.choice(['R', 'P', 'S'])
    last3 = ''.join(opponent_history[-3:])
    patterns = {}
    for i in range(len(opponent_history) - 3):
        key = ''.join(opponent_history[i:i+3])
        next_move = opponent_history[i+3]
        patterns[key] = patterns.get(key, {'R':0, 'P':0, 'S':0})
        patterns[key][next_move] += 1
    prediction = max(patterns.get(last3, {'R':0, 'P':0, 'S':0}), key=patterns.get(last3, {'R':0, 'P':0, 'S':0}).get)
    return beats(prediction)

def detect_bot():
    # Heuristic detection based on first 50 rounds
    if len(opponent_history) < 50:
        return 'default'
    recent = opponent_history[:50]
    if recent == ['R', 'P', 'S'] * 16 + ['R', 'P']:
        return 'quincy'
    if all(move == my_history[i-1] for i, move in enumerate(opponent_history[1:], start=1)):
        return 'abbey'
    if recent.count('R') > recent.count('P') and recent.count('R') > recent.count('S'):
        return 'kris'
    return 'mrugesh'

def player(prev_play, opponent_history_local=[]):
    global opponent_history, my_history, round_num
    round_num += 1

    if prev_play:
        opponent_history.append(prev_play)

    bot_type = detect_bot()

    if bot_type == 'quincy':
        move = counter_quincy()
    elif bot_type == 'abbey':
        move = counter_abbey()
    elif bot_type == 'kris':
        move = counter_kris()
    elif bot_type == 'mrugesh':
        move = counter_mrugesh()
    else:
        move = random.choice(['R', 'P', 'S'])

    my_history.append(move)
    return move