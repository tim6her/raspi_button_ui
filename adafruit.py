#! /usr/bin/env python

import os
import time

import Adafruit_IO as aio

import cartridge

def main():
    path = os.path.split(os.path.realpath(__file__))[0]
    log_fn = os.path.join(path, 'cartridge.log')
    ada_fn = os.path.join(path, 'adafruit.txt')
    with open(ada_fn, 'r') as ada:
        client = aio.Client(ada.read().strip('\n'))

    old_id = None
    while True:
        time.sleep(5)

        try:
            data = client.receive('salonmaster')
        except aio.errors.RequestError:
            data = None
            new_id = old_id
            next

        if data:
            new_id = data.id

        if old_id != new_id:
            usage = cartridge.usage_list(log_fn, realtime=True)
            use = cartridge.usetime(usage)
            client.send('cartridge', '%.2f' % (use / 60. / 60.))

        old_id = new_id

if __name__ == "main":
    main()
