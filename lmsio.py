#!/usr/bin/python
# -*- coding: utf-8

from pylms.server import Server
import socket
import time
import re
import os
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
	cfg_out_fn = os.path.join(path, '.cfg')

        with open(cfg_in_fn, 'r') as cfg_in:
            cfg = cfg_in.read()
        with open(cfg_out_fn, 'w') as cfg_out:
            cfg_out.write(cfg.format(dev=device, sub=subdev))

        p = subprocess.Popen(['sudo', 'darkice', '-c', cfg_out_fn])
        return p
    else:
        p.kill()
