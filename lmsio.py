#!/usr/bin/python
# -*- coding: utf-8

from pylms.server import Server
import socket
import time
import subprocess

def connect_to_player_at_server(playername, hostname):
    server = Server(hostname=hostname)
    
    while True:
        try:
            server.connect()
            players = [ply for ply in server.get_players() if ply.name ==
                    playername]
            if len(players) < 1:
                raise socket.gaierror(('No player named %s connected to '
                    'server named %s') % (playername, hostname))

            return players[0]
        except socket.gaierror:
            time.sleep(5)

def phono(p=None):
    if p == None:
        p = subprocess.Popen(['sudo', 'darkice'])
        return p
    else:
        p.kill()
