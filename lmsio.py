#!/usr/bin/python
# -*- coding: utf-8
"""Interface functions for the communication with a Squeezebox
Server"""

__author__ = 'Tim B. Herbstrith'

from pylms.server import Server
import subprocess

def connect_to_player_at_server(playername, hostname):
    """Connects to a Squeezbox player connected to a server by
    their name.

    Args:
        playername (string): name of player
        hostname (string): hostname of Squeezbox server

    Returns:
        pylms.player.Player
    """
    server = Server(hostname=hostname)

    while True:
        server.connect()
        players = [ply for ply in server.get_players() if ply.name ==
                    playername]
        if len(players) < 1:
            raise socket.gaierror(('No player named %s connected to '
                        'server named %s') % (playername, hostname))

        return players[0]

def phono(p=None):
    """Runs or stops *darkice*

    If `p` is `None` a new subprocess running *darkice* is
    created. If `p` is a subprocess it is killed.

    Args:
        p (subprocess.Popen): Process running *darkice* or `None`,
            defaults to `None`
    Returns:
        subprocess.Popen / `None`: subprocess running *darkice* or
            `None` if the subprocess has been killed.
    """
    if p == None:
        p = subprocess.Popen(['sudo', 'darkice'])
        return p
    else:
        p.kill()
