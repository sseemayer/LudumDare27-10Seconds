#!/usr/bin/env python
import crowd

if __name__ == '__main__':
    game = crowd.Game()


    import crowd.modes.action

    challenges = [
        (crowd.modes.action.DebugChallenge,)
    ]

    game.mode = crowd.modes.action.ActionMode(game, challenges)

    game.loop()
