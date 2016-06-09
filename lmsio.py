#!/usr/bin/python
# -*- coding: utf-8

from pylms.server import Server

def connect_to_player_at_server(playername, hostname):
    server = Server(hostname=hostname)
    server.connect()
    players = [ply for ply in server.get_players() if ply.name ==
            playername]
    if len(players) < 1:
        raise NameError(('No player named %s connected to '
            'server named %s') % (playername, hostname))

    return players[0]
