from pwn import *
import re

server = process(['python3','server.py'])

def get_hand(server):
    server.recvuntil(b'Your hand is ')
    hand = server.recvuntil(b'\t-->').decode().strip()
    return hand

def get_score(hand):
    score_dict = {
        'Royal Flush': 9,
        'Straight Flush': 8,
        'Four of a kind': 7,
        'Full House': 6,
        'Flush': 5,
        'Straight': 4,
        'Three of a kind': 3,
        'Two pair': 2,
        'One pair': 1,
        'High card': 0
    }
    for key, value in score_dict.items():
        if key in hand:
            return value
    return -1

def play_game(server):
    server.recvuntil(b'Your hand is ')
    my_hand = get_hand(server)
    my_score = get_score(my_hand)

    server.sendline(b'1')
    server.recvuntil(b'Your hand is ')
    your_hand = get_hand(server)
    your_score = get_score(your_hand)

    if my_score > your_score:
        return True
    elif my_score < your_score:
        return False
    else:
        return None

def main():
    wins = 0
    for i in range(1000):
        result = play_game(server)
        if result is True:
            wins += 1
        elif result is False:
            wins -= 1
    print(f'Wins: {wins}')

if __name__ == '__main__':
    main()