#!/usr/bin/env python
import crowd
import optparse
import sys

if __name__ == '__main__':

    parser = optparse.OptionParser()
    parser.add_option('-u', '--no-upload', dest='upload', default=True, action='store_false', help="Don't upload replay data")

    opt, args = parser.parse_args()

    game = crowd.Game(upload=opt.upload)

    import crowd.modes.action.challenges.race
    import crowd.modes.action.challenges.jump
    import crowd.modes.action.challenges.gather

    challenges = [
        (crowd.modes.action.challenges.race.RaceChallenge,),
        (crowd.modes.action.challenges.jump.JumpChallenge,),
        (crowd.modes.action.challenges.gather.GatherChallenge,)
    ]

    game.mode = crowd.modes.action.ActionMode(game, challenges)
    game.mode.on_finish = lambda: sys.exit()

    game.loop()
