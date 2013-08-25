import crowd.modes
import crowd.modes.dialog
import crowd.resource
import crowd.input

import collections

import sys
import py2d.Math
import crowd.modes.action

import pygame

class MenuMode(crowd.modes.GameMode):

    def __init__(self, game):
        super(MenuMode, self).__init__(game)

        self.logo = crowd.resource.image.logo
        self.logo_size = py2d.Math.Vector(*self.logo.get_size())

        self.font_subtitle = crowd.resource.font.default
        self.font_menu = crowd.resource.font.menu

        self.last_input = game.input.keys

        def back_to_menu():
            self.game.mode = self

        def start_game():

            def finish_game():
                self.game.mode = crowd.modes.dialog.DialogMode(self.game, "Game Over", [
                    'you have scored a total of',
                    '{0} points'.format(self.game.score),
                    '',
                    'congratulations!',
                    '',
                    'press ENTER for main menu'
                ])

                self.game.mode.on_finish = back_to_menu

            def finish_name():
                import crowd.modes.action
                self.game.mode = crowd.modes.action.ActionMode(game, [(c,) for c in crowd.modes.action.AVAILABLE_CHALLENGES])
                self.game.mode.on_finish = finish_game


            #self.game.mode.on_finish = finish

            import crowd.modes.name
            self.game.mode = crowd.modes.name.NameEnterMode(self.game)

            self.game.mode.on_finish = finish_name

        def highscores():
            pass

        def manual():

            self.game.mode = crowd.modes.dialog.DialogMode(self.game, "Manual", [
                "Crowd is controlled using",
                "the arrow keys.",
                "",
                "Other than that, the intro",
                "texts to the challenges give",
                "helpful hints.",
                "",
                "",
                "Press RETURN for main menu"
            ])

            self.game.mode.on_finish = back_to_menu

        def quit():
            sys.exit(0)

        self.menu_options = [
                ('start game', start_game),
                ('highscores', highscores),
                ('manual', manual),
                ('quit', quit)
        ]

        self.menu_padding = 30
        self.menu_sel = 0

    def update(self, time_elapsed):
        input = self.game.input.keys

        update = {k: v for k, v in input.items() if self.last_input[k] != v and v}

        if 'down' in update:
            crowd.resource.sound.select.play()
            self.menu_sel += 1

        if 'up' in update:
            crowd.resource.sound.select.play()
            self.menu_sel -= 1

        self.menu_sel = (self.menu_sel + len(self.menu_options)) % len(self.menu_options)


        if 'a' in update:
            crowd.resource.sound.coin.play()
            self.menu_options[self.menu_sel][1]()


        self.last_input = input.copy()


    def render(self):
        screen_size = py2d.Math.Vector(*crowd.constants.SCREEN_SIZE)

        self.game.screen.fill((0,0,0))
        self.game.screen.blit(self.logo, (screen_size.x/2 - self.logo_size.x /2, 50))

        n_challenges = len(crowd.modes.action.AVAILABLE_CHALLENGES)
        subtitle = self.font_subtitle.render('{0} challenges, 10 seconds each. you and the rest of the world.'.format(n_challenges), True, (255, 255, 255))
        subtitle_size = py2d.Math.Vector(*subtitle.get_size())
        self.game.screen.blit(subtitle, (screen_size.x / 2 - subtitle_size.x / 2, 50 + self.logo_size.y + 20))

        menu_surfs = [self.font_menu.render(entry[0], True, (0,0,0) if i == self.menu_sel else (255, 255, 255)) for i, entry in enumerate(self.menu_options)]


        total_width = max(s.get_size()[0] for s in menu_surfs)
        total_height = self.menu_padding * len(self.menu_options)

        menu_pos = py2d.Math.Vector(screen_size.x / 2, screen_size.y / 2 - total_height / 2 + 100)

        pygame.draw.rect(self.game.screen, (255, 255, 255), ((0, menu_pos.y + self.menu_sel * self.menu_padding), (crowd.constants.SCREEN_SIZE[0], self.menu_padding)))

        for i, surf in enumerate(menu_surfs):
            self.game.screen.blit(surf, (menu_pos.x - surf.get_size()[0] / 2, menu_pos.y + i * self.menu_padding))

