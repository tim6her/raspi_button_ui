#!/usr/bin/python
# -*- coding: utf-8

import lmsio
import RPi.GPIO as GPIO
import gpioio
import time
import subprocess

# Set name of server and player here
SERVER = 'salonmaster'
PLAYER = 'salonmaster'

player = lmsio.connect_to_player_at_server(PLAYER, SERVER)

try:
    GPIO.setmode(GPIO.BOARD)

    control_led = gpioio.LED(26)
    phono_led = gpioio.LED(24)

    toggle_but = gpioio.Button(19, led=control_led)
    vol_up_but = gpioio.Button(23, led=control_led)
    vol_down_but = gpioio.Button(22, led=control_led)
    phono_but = gpioio.Button(21, led=control_led)

    control_led.state = True

    while True:
        if toggle_but and vol_down_but:
            subprocess.call(['sudo', ' halt'])

        if toggle_but and vol_up_but:
            subprocess.call(['sudo', 'reboot'])

        if toggle_but:
            player.toggle()

        if vol_up_but:
            player.volume_up()

        if vol_down_but:
            player.volume_down()

        if phono_but:
            phono_led.state = not phono_led.state
            pass

        time.sleep(.5)
finally:
    GPIO.cleanup()
