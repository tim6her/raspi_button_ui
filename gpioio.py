#!/usr/bin/python
# -*- coding: utf-8

import time

class Pin(object):
    def __init__(self, is_input):
        self.is_input = bool(is_input)
        self._state = False

    @property
    def state(self):
        return self._state

    def __nonzero__(self):
        return bool(self.state)

class Button(Pin):
    def __init__(self, led=None):
        super(Button, self).__init__(True)
        self.pressed = False
        self.led = led

    @property
    def state(self):
        state = bool(raw_input('Pressed? '))
        if state:
            self.led.blink()
        self._state = state
        return self._state

class LED(Pin):
    def __init__(self):
        super(LED, self).__init__(False)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = bool(state)
        print int(self._state)

    def blink(self, n=1):
        for i in range(n):
            self.state = not self.state
            time.sleep(0.1)
            self.state = not self.state
