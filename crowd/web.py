import urllib2
import urllib

import crowd.input
import crowd.constants
import json
import struct

def color_hex_to_tuple(hex):
    # adapted from http://stackoverflow.com/a/4296263

    if hex.startswith("#"):
        hex = hex[1:]

    return struct.unpack('BBB', hex.decode('hex'))


def color_tuple_to_hex(tuple):
    # adapted from http://stackoverflow.com/a/4296263
    return '#' + struct.pack('BBB', *tuple).encode('hex')

def get_challenge_replays(game, challenge_name):

    res = urllib2.urlopen(crowd.constants.URL_REPLAYS_GET.format(challenge=challenge_name))
    data = json.load(res)

    def convert_replay(replay):
        cache = json.loads(replay['replay'])
        return crowd.input.CachedInputSource(game, replay['player'], color_hex_to_tuple(replay['color']), challenge_name, cache)

    return [ convert_replay(replay) for replay in data['replays'] ]

def post_challenge_replay(live_input_source):
    lis = live_input_source

    data = urllib.urlencode({
        'challenge': lis.challenge,
        'player': lis.player,
        'color': color_tuple_to_hex(lis.color),
        'replay': json.dumps(lis.updates)
    })

    res = urllib2.urlopen(crowd.constants.URL_REPLAYS_POST, data)

    print(res.read())
