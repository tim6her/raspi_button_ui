#! /usr/bin/env python

import os
import time

import Adafruit_IO as aio
import requests

import cartridge

def main():
    path = os.path.split(os.path.realpath(__file__))[0]
    log_fn = os.path.join(path, 'cartridge.log')
    ada_fn = os.path.join(path, 'adafruit.txt')
    webhooks_fn = os.path.join(path, 'webhooks.txt')
    with open(ada_fn, 'r') as ada:
        client = aio.Client(ada.read().strip('\n'))
    with open(webhooks_fn, 'r') as wh_file:
        wh_url = wh_file.read().strip('\n')

    old_id = None
    startup = True
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

        if old_id != new_id and not startup:
            usage = cartridge.usage_list(log_fn, realtime=True)
            use = cartridge.usetime(usage)
            ok = cartridge.MAX_USE > use
            value2 = 'OK' if ok else 'Please change!'
            data = dict(value1='%.2f' % (use / 60. / 60.),
                        value2=value2)
            requests.post(wh_url, data)


        old_id = new_id
        startup = False

if __name__ == "__main__":
    main()
