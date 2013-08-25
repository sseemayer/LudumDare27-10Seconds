#!/usr/bin/env python
import crowd
import optparse
import sys

if __name__ == '__main__':

    parser = optparse.OptionParser()
    parser.add_option('-u', '--no-upload', dest='upload', default=True, action='store_false', help="Don't upload replay data")
    parser.add_option('-m', '--no-music', dest='music', default=True, action='store_false', help="Don't play music")

    opt, args = parser.parse_args()

    game = crowd.Game(upload=opt.upload, music=opt.music)

    #import crowd.modes.action
    #game.mode = crowd.modes.action.ActionMode(game, [(c,) for c in crowd.modes.action.AVAILABLE_CHALLENGES])

    import crowd.modes.menu
    game.mode = crowd.modes.menu.MenuMode(game)

    game.mode.on_finish = lambda: sys.exit()
    game.loop()
