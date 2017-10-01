#! /usr/bin/env python

import os
import time

import Adafruit_IO as aio
import pushbullet

import cartridge

def main():
    path = os.path.split(os.path.realpath(__file__))[0]
    log_fn = os.path.join(path, 'cartridge.log')
    ada_fn = os.path.join(path, 'adafruit.txt')
    pb_fn = os.path.join(path, 'pushbullet.txt')
    with open(ada_fn, 'r') as ada:
        client = aio.Client(ada.read().strip('\n'))
    with open(pb_fn, 'r') as pbf:
        pb = pushbullet.Pushbullet(pbf.read().strip('\n'))

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
            title = 'CARTRIDE USAGE'
            body = 'Your cartridge operated %.2f hours.' % (use / 60. / 60.)
            pb.push_note(title, body)

        old_id = new_id
        startup = False

if __name__ == "__main__":
    main()
