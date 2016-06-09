#!/usr/bin/python
# -*- coding: utf-8

import time
import RPi.GPIO as GPIO

class Pin(object):
    def __init__(self, channel, is_input, **kargs):
        self.channel = channel
        self._state = False
        direction = GPIO.IN if is_input else GPIO.OUT	

        GPIO.setup(channel=channel, direction=direction, **kargs)

    @property
    def state(self):
        return self._state

    def __nonzero__(self):
        return bool(self.state)

class Button(Pin):
    def __init__(self, channel, led=None):
        super(Button, self).__init__(channel=channel,
                is_input=True, pull_up_down=GPIO.PUD_UP)
        self.led = led

    @property
    def state(self):
	# Button is pulled up!
        state = not bool(GPIO.input(self.channel))
        if self.led != None and state:
            self.led.blink()
        self._state = state
        return self._state

class LED(Pin):
    def __init__(self, channel):
        super(LED, self).__init__(channel=channel,
                is_input=False)

    @property
    def state(self):
        self._state = bool(GPIO.input(self.channel))
	return self._state

    @state.setter
    def state(self, state):
        self._state = bool(state)
	GPIO.output(self.channel, self._state)

    def blink(self, n=1):
        for i in range(n):
            self.state = not self.state
            time.sleep(0.1)
            self.state = not self.state


def main():
    GPIO.setmode(GPIO.BOARD)
    
    but_chans = [19, 21, 22, 23]
    led_chans = [24, 26]

    buts = [Button(c) for c in but_chans]
    leds = [LED(c) for c in led_chans]

    while True:
        for i, but in enumerate(buts):
            if but:
                leds[0].state = i % 2
                leds[1].state = (i // 2) % 2

if __name__ == '__main__':
    try:
        main()
    finally:
        print 'cleaning up'
        GPIO.cleanup()
