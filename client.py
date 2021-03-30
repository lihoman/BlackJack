import socket
import json
import time
from Cards import *


def info_from_json(json_info):
    return json.loads(json_info.decode('utf-8'))


def info_in_json(info):
    info = json.dumps(info)
    return info.encode('utf-8')


sock_client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)
sock_client.connect(('localhost', 10000))

while True:
    player_name = input('Welcome in BlackJack. What is your name?: ')  # give info about client
    sock_client.send(info_in_json(player_name))  # sending client name to server to create a player
    player_count = info_from_json(sock_client.recv(1024))  # receive info about client count in game
    print(player_count)
    player_rate = input("Please, make your bet: ")  # client rate in game
    sock_client.send(info_in_json(player_rate))  # sending info about client rate to server
    data = info_from_json(sock_client.recv(1024))  # receive info what cards has client
    player_cards = [Card(data[0], data[1]), Card(data[2], data[3])]
    player_result = data[4]
    print(player_cards, f'{player_name} result: {player_result}', sep='\n')
    answer = input('Do you want to take one more card? (y/n): ').upper()
    sock_client.send(info_in_json(answer))
    while answer == 'Y':
        sock_client.send(info_in_json(answer))
        data = info_from_json(sock_client.recv(1024))
        player_cards.append(Card(data[0], data[1]))
        player_result = data[2]
        print(player_cards, f'{player_name} result: {player_result}', sep='\n')
        answer = input('Do you want to take one more card? (y/n): ').upper()
        sock_client.send(info_in_json(answer))
    print("It's a dealer's time now")
    time.sleep(1)
    data = info_from_json(sock_client.recv(1024))
    dealer_cards = [Card(data[0], data[1]), Card(data[2], data[3])]
    dealer_result = data[4]
    print(dealer_cards, f'Dealer result: {dealer_result}', sep='\n')
    time.sleep(1)
    sock_client.send(info_in_json("OK"))
    data = info_from_json(sock_client.recv(1024))
    while data != "End dealer's game":
        dealer_cards.append(Card(data[0], data[1]))
        dealer_result = data[2]
        print(dealer_cards, f'Dealer result: {dealer_result}', sep='\n')
        sock_client.send(info_in_json("OK"))
        data = info_from_json(sock_client.recv(1024))

    sock_client.send(info_in_json("OK"))
    game_result, player_count = info_from_json(sock_client.recv(1024))
    print(game_result, f'Your count: {player_count}', sep='\n')


# sock_client.close()
