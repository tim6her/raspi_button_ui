#!/usr/bin/python
# -*- coding: utf-8

"""A simple UI for a internet radio based on Squeezbox
using physical buttons and LEDs in the following curcuit.

  #19     #21     #22      #23     #24     #26
  GPIO10  GPIO09  GPIO25   GPIO11  GPIO08  GPIO07
  toggle  phono   vol down vol up  status  phono
    |       |       |        |       |       |
    |       |       |        |      +-+     +-+
    |       |       |        |      | |     | |
    |       |       |        |      +-+     +-+
    |       |       |        |       |       |
    /       /       /        /      ---     ---
 +-/     +-/     +-/      +-/       \ / =>  \ / =>
    |       |       |        |      ---     ---
    |       |       |        |       |       |
----+-------+-------+--------+-------+---+---+----
                                         |
                                        --- #25 GND
                                         -
"""

import RPi.GPIO as GPIO
import time
import threading
import subprocess
import socket
import Queue

import adafruit
import gpioio
import lmsio

def thread_connecting_to_player(queue):
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

    thread_connect = threading.Thread(target=queue_connect,
                                      name="connect_to_player",
                                      args=[queue, PLAYER, SERVER],
                                     )
    thread_connect.start()
    return thread_connect

def thread_for_adafruit():
    thread_cartridge = threading.Thread(target=adafruit.main,
                                        name='cartridge'
                                       )
    thread_cartridge.start()
    return thread_cartridge


# Set name of server and player here
SERVER = 'salonmaster'
PLAYER = 'salonmaster'

# Player thread
queue = Queue.Queue()
thread_connect = thread_connecting_to_player(queue)

# Cartridge thread
thread_cartridge = thread_for_adafruit()

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
                if not thread_connect.is_alive():
                    print 'Thread connecting to LMS is dead'
                    thread_connect = thread_connecting_to_player(queue)

        if not thread_cartridge.is_alive():
            thread_cartridge = thread_for_adafruit()

        if toggle_but and vol_down_but:
            subprocess.call(['sudo', ' halt'])

        if toggle_but and vol_up_but:
            subprocess.call(['sudo', 'reboot'])

        if toggle_but and player != None:
            old_mode = player.get_mode()
            for i in range(3):
                player.toggle()
                new_mode = player.get_mode()
                time.sleep(.1)
                if old_mode != new_mode:
                    break

        if vol_up_but and player != None:
            player.volume_up()

        if vol_down_but and player != None:
            player.volume_down()

        if phono_but:
            p = lmsio.phono(player, p)

        phono_led.state = p != None and p.poll != None

        time.sleep(.2)
finally:
    GPIO.cleanup()
