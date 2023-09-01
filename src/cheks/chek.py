import logging


# Проверка на условия что все игроки использовали всю power, для завершения игры.
# Checking for conditions that all players have used all power, to complete the game.
def check_all_players_power_off(players):
    players_zero_power = 0
    for player in players:
        if player.power <= 0:
            players_zero_power += 1
    if players_zero_power == len(players):
        logging.info("ALL Player power off!!")
        return True
    return False

# Проверка на условия что все игроки умерли, для завершения игры.
# Check for the condition that all players are dead, to end the game.
def check_all_players_die(players):
    players_die = 0
    for player in players:
        if player.die is True:
            players_die += 1
    if players_die == len(players):
        logging.info("ALL DIE!!")
        return True
    return False

# Проверка позиций игроков, в случае если в одном блоке стоит более одного игрока.
# Check players' positions in case there is more than one player in one block.
def check_players_positions(players, player):
    for each_player in players:
        if player.position == each_player.position and player is not each_player:
            return each_player
    return False