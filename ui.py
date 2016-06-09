#!/usr/bin/python
# -*- coding: utf-8

import lmsio
import gpioio
import time
import subprocess

# Set name of server and player here
SERVER = 'salonmaster'
PLAYER = 'salonmaster'

player = lmsio.connect_to_player_at_server(PLAYER, SERVER)

control_led = gpioio.LED()
phono_led = gpioio.LED()

toggle_but = gpioio.Button(led=control_led)
vol_up_but = gpioio.Button(led=control_led)
vol_down_but = gpioio.Button(led=control_led)
phono_but = gpioio.Button(led=control_led)

control_led.state = True

while True:
    print 'Shutdown?'
    if toggle_but and vol_down_but:
        subprocess.call(['sudo', ' halt'])

    print 'Reboot?'
    if toggle_but and vol_up_but:
        subprocess.call(['sudo', 'reboot'])

    print 'Toggle?'
    if toggle_but:
        player.toggle()

    print 'Vol up?'
    if vol_up_but:
        player.volume_up()

    print 'Vol down?'
    if vol_down_but:
        player.volume_down()

    print 'Phono?'
    if phono_but:
        phono_led.state = not phono_led.state
        pass

    print 'Control: ' + str(control_led.state)
    print 'Phono: ' + str(phono_led.state)
    time.sleep(.5)
