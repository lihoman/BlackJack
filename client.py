import socket
import time
from Cards import *
from additional_functions import *

sock_client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)
sock_client.connect(('localhost', 10000))

while True:
    player_name = input('Welcome in BlackJack. What is your name?: ')  # give info about player
    sock_client.send(info_in_json(player_name))  # sending player name to server to create a player
    player_count = info_from_json(sock_client.recv(1024))  # receive info about player count in game
    print(player_count)

    while True > 0:
        if player_count == 0:
            # Ending the game if player has not money
            break

        player_rate = input("Please, make your bet: ")  # player rate in game

        while not player_rate.isdigit() or int(player_rate) < 0:
            print('The rate must be a number more than zero')
            player_rate = input("Please, make your bet: ")

        sock_client.send(info_in_json(player_rate))  # sending info about player rate to server

        if int(player_rate) > player_count:
            data = info_from_json(sock_client.recv(1024))  # ending the game if rate more than total money in count
            print(data)
            break

        data = info_from_json(sock_client.recv(1024))  # receive info what cards has client
        player_cards = [Card(data[0], data[1]), Card(data[2], data[3])]  # create objects with cards
        player_result = data[4]
        print(player_cards, f'{player_name} result: {player_result}', sep='\n')
        answer = input('Do you want to take one more card? (y/n): ').upper()
        sock_client.send(info_in_json(answer))

        while answer == 'Y':
            data = info_from_json(sock_client.recv(1024))  # give info about card and result in number
            player_cards.append(Card(data[0], data[1]))  # adding this card in common list with cards
            player_result = data[2]
            print(player_cards, f'{player_name} result: {player_result}', sep='\n')
            answer = input('Do you want to take one more card? (y/n): ').upper()
            sock_client.send(info_in_json(answer))

        print("It's a dealer's time now")
        time.sleep(1)
        data = info_from_json(sock_client.recv(1024))  # giving info about start dealer's cards
        dealer_cards = [Card(data[0], data[1]), Card(data[2], data[3])]  # create objects with dealer's cards
        dealer_result = data[4]
        print(dealer_cards, f'Dealer result: {dealer_result}', sep='\n')

        time.sleep(1)
        sock_client.send(info_in_json("Get dealer's cards"))  # send lighthouse that client can go next
        data = info_from_json(sock_client.recv(1024))  # giving new dealer's card or text that dealer ended the game

        while data != "End dealer's game":
            dealer_cards.append(Card(data[0], data[1]))
            dealer_result = data[2]
            print(dealer_cards, f'Dealer result: {dealer_result}', sep='\n')
            sock_client.send(info_in_json("Get one more dealer's card"))  # lighthouse to server
            data = info_from_json(sock_client.recv(1024))

        sock_client.send(info_in_json("Get all dealer's cards"))  # lighthouse that client sees all dealer's cards

        game_result, player_count = info_from_json(sock_client.recv(1024))  # giving result who is winner
        print(game_result, f'Your count: {player_count}', sep='\n')

    sock_client.send(info_in_json('The end'))
    result = info_from_json(sock_client.recv(1024))
    print(result)
    sock_client.close()
    break
