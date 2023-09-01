import logging


# Прочие условия игры не связанные с перемещением.
# Other non-movement related game conditions.
def conditions(blocks, next_num_block, player, my_map, players):
    # Если не призовой блок, то перемещение к нему стоит 1 power
    # If not a prize block, moving to it costs 1 power
    if blocks[next_num_block].prize_block is False:
        player.power -= 1
    # Если блок сердца, то пополняет жизни
    # If a heart block, it replenishes lives
    if blocks[next_num_block].hart_block is True:
        player.life = 5
        logging.info(f"player {player.name} in on 'heart' block his life is {player.life}")
    # Если блок с огнем то отнимает жизнь и в случае если у игрока есть ключ, то выподает ключ в блок.
    # If the block with fire, it takes away life and if the player has a key, the key comes out in the block.
    if blocks[next_num_block].flame_block is True:
        player.life -= 1
        logging.info(f"player {player.name} in on 'flame' block, lose 1 life and have {player.life} life")
        blocks[next_num_block].flame_block = False
        if player.life == 0 and player.have_key is True:
            player.have_key = False
            player.die = True
            logging.info(f"player {player.name} has key, and key is dropped in block {player.position}")
            my_map.blocks[player.position].key_block = True
            my_map.delete_player(blocks, blocks[player.position], player)
            my_map.add_key(my_map.blocks[player.position])
            player.position = -1
        elif player.life == 0 and player.have_key is False:
            my_map.delete_player(blocks, blocks[player.position], player)
            player.die = True
            player.position = -1
    # Если вернулся к уже пройденым блокам, то гирой умирает от страха. Также если у героя был ключ то ключ
    # выпадет в блок
    # If you return to the already passed blocks, the gyro dies of fear. Also, if the hero had a key, the key
    # will fall into the block
    if player.position in player.last_position and blocks[player.last_position[-1]].prize_block is False:
        logging.info(f"PLAYER {player.name} scary and die.")
        player.move_state = False
        player.life = 0
        logging.info(f"player {player.name} life: {player.life}")
        player.die = True
        player.position = -1
        if player.have_key is True:
            player.have_key = False
            my_map.blocks[player.last_position[-1]].key_block = True
            my_map.delete_player(blocks, blocks[player.position], player)
            my_map.add_key(my_map.blocks[player.last_position[-1]])
        return player.move_state
    # Если игрок дошел до последнего блока с ключем то вигрышь и завершение игры. Иначе игрок погибает.
    # If the player reaches the last block with the key, the player wins and the game ends. Otherwise the player dies.
    if blocks[next_num_block].end_block is True and player.have_key is True:
        logging.info(f"PLAYER {player.name} WIN!")
        player.move_state = False
        player.win = True
        return player.move_state
    elif blocks[next_num_block].end_block is True and player.have_key is False:
        player.move_state = False
        player.life = 0
        player.die = True
        player.position = -1
        logging.info(f"PLAYER {player.name} KILL! \n player {player.name} life: {player.life}")
        my_map.delete_player(blocks, blocks[player.position], player)
        return player.move_state