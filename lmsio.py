#!/usr/bin/python
# -*- coding: utf-8
"""Interface functions for the communication with a Squeezebox
Server"""

__author__ = 'Tim B. Herbstrith'

from pylms.server import Server
import time
import re
import subprocess
import os

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

    server.connect()
    players = [ply for ply in server.get_players() if ply.name ==
                playername]
    if len(players) < 1:
        raise RuntimeError(('No player named %s connected to '
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
        arecord = subprocess.Popen(['arecord', '-l'], stdout=subprocess.PIPE)
        hw = arecord.communicate()[0]
	print hw
        try:
            pat_dev = r'card (\d+):'
            device = re.search(pat_dev, hw).groups(1)[0]
            pat_sub = r'Subdevice #(\d+):'
            subdev = re.search(pat_sub, hw).groups(1)[0]
        except AttributeError:
            return
        path = os.path.split(os.path.realpath(__file__))[0]
        cfg_in_fn = os.path.join(path, 'darkice.cfg')
	pwd_fn = os.path.join(path, 'pwd.txt')
        cfg_out_fn = os.path.join(path, '.cfg')

        with open(cfg_in_fn, 'r') as cfg_in:
            cfg = cfg_in.read()
        with open(pwd_fn, 'r') as pwd_file:
            pwd = pwd_file.read()
        with open(cfg_out_fn, 'w') as cfg_out:
            cfg_out.write(cfg.format(dev=device, sub=subdev, pwd=pwd))

        p = subprocess.Popen(['sudo', 'darkice', '-c', cfg_out_fn])
        return p
    else:
        p.kill()
