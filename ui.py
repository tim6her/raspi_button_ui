#!/usr/bin/python
# -*- coding: utf-8

import lmsio
import RPi.GPIO as GPIO
import gpioio
import time
import threading
import subprocess
import socket
import Queue

def queue_connect(queue, *args):
    while True:
        try:
            player = lmsio.connect_to_player_at_server(*args)
        except EOFError:
            print 'Could not connect'
            time.sleep(5)
        else:
            break
    queue.put(player)

# Set name of server and player here
SERVER = 'salonmaster'
PLAYER = 'salonmaster'

queue = Queue.Queue()
thread_ = threading.Thread(
                target=queue_connect,
                name="Thread1",
                args=[queue, PLAYER, SERVER],
                )
thread_.start()
player = None
p = None

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
	if player == None:
            try:
                player = queue.get_nowait()
            except Queue.Empty:
                player = None
                phono_led.blink()
                if not thread_.is_alive():
                    print 'Thread connecting to LMS is dead'
                    thread_ = threading.Thread(
                                target=queue_connect,
                                name="Thread1",
                                args=[queue, PLAYER, SERVER],
                                )
                    thread_.start()

        if toggle_but and vol_down_but:
            subprocess.call(['sudo', ' halt'])

        if toggle_but and vol_up_but:
            subprocess.call(['sudo', 'reboot'])

        if toggle_but and player != None:
            player.toggle()

        if vol_up_but and player != None:
            player.volume_up()

        if vol_down_but and player != None:
            player.volume_down()

        if phono_but:
            p = lmsio.phono(p)

        phono_led.state = p != None and p.poll != None

        time.sleep(.5)
finally:
    GPIO.cleanup()
