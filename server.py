import socket
import datetime
from GameRound_for_server import *
from additional_functions import *

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)
server.bind(('', 10000))
server.listen(1)

while True:
    client_sock, client_address = server.accept()

    write_info_about_game(f'Client {client_address[0]} connected at {datetime.datetime.now()}')

    while True:
        player_name = info_from_json(client_sock.recv(1024))  # receive info about client name
        write_info_about_game(player_name)
        game = GameRound(player_name)  # create player and dealer
        client_sock.send(info_in_json(game.player.count))  # send info about how much money client has
        write_info_about_game(game.player.count)

        while game.player.count > 0:
            if game.player.count == 0:
                # Ending the game if player has not money
                break

            player_rate = info_from_json(client_sock.recv(1024))  # receive info about client's rate

            if int(player_rate) > game.player.count:
                # Ending the game if player's rate more than total money in his count
                client_sock.send(info_in_json(game.player.get_rate(player_rate, 'Dealer')))
                break

            game.player.my_cards = game.player.generate_start_cards()  # start cards for client

            # Sending info about suit and value of cards, not class objects
            player_card_1_suit, player_card_1_value = game.player.my_cards[0].suit, game.player.my_cards[0].value
            player_card_2_suit, player_card_2_value = game.player.my_cards[1].suit, game.player.my_cards[1].value
            game.player_result = game.player.finish_result()  # view in number which client has result
            client_sock.send(info_in_json((player_card_1_suit, player_card_1_value,
                                           player_card_2_suit, player_card_2_value,
                                           game.player_result)))
            while True:
                answer = info_from_json(client_sock.recv(1024))  # giving answer from client to adding one more card
                if answer != 'Y':
                    # if client doesn't want to take card, dealer starts his game
                    break
                game.player_result = game.one_more_card(player_name, answer)  # adding the card to client
                new_card_suit = game.player.my_cards[-1].suit
                new_card_value = game.player.my_cards[-1].value
                client_sock.send(info_in_json((new_card_suit, new_card_value, game.player_result)))

            # Dealer's game
            game.dealer.my_cards = game.dealer.generate_start_cards()  # generate dealer's start cards
            dealer_card_1_suit, dealer_card_1_value = game.dealer.my_cards[0].suit, game.dealer.my_cards[0].value
            dealer_card_2_suit, dealer_card_2_value = game.dealer.my_cards[1].suit, game.dealer.my_cards[1].value
            game.dealer_result = game.dealer.finish_result()  # generate dealer's result in number (not only in cards)
            client_sock.send(info_in_json((dealer_card_1_suit, dealer_card_1_value,
                                           dealer_card_2_suit, dealer_card_2_value,
                                           game.dealer_result)))
            client_sock.recv(1024)  # info to server to going next

            while game.dealer_result <= 17:
                # dealer takes cards while result less than 17
                game.dealer_result = game.one_more_card(game.dealer.name, 'Y')  # adding one card
                new_card_suit, new_card_value = game.dealer.my_cards[-1].suit, game.dealer.my_cards[-1].value
                client_sock.send(info_in_json((new_card_suit, new_card_value, game.dealer_result)))  # send this info
                client_sock.recv(1024)

            client_sock.send(info_in_json("End dealer's game"))  # send info that dealer ended his game
            client_sock.recv(1024)

            # Comparison result who is winner
            if game.player_result <= 21 and game.dealer_result <= 21:
                game_result = game.compare_results(game.player_result, game.dealer_result)
                finally_count = game.player.get_rate(player_rate, game_result)  # get rate and give finally count
                client_sock.send(info_in_json((game_result, finally_count)))
                write_info_about_game(game.player.count)
            else:
                game_result = game.compare_results(game.dealer_result, game.player_result)
                finally_count = game.player.get_rate(player_rate, game_result)
                client_sock.send(info_in_json((game_result, finally_count)))
                write_info_about_game(game.player.count)

            game.player.game_deck = Deck(52)  # creating new full deck for new game

        client_sock.recv(1024)
        write_info_about_game(game.player.count)
        client_sock.send(info_in_json('Thanks for the good game. See you next time!'))
        client_sock.close()  # close connection with client
        break
