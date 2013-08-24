
class DebugChallenge(Challenge):

    name = 'debug'

    def __init__(self, mode, input_sources):
        super(DebugChallenge, self).__init__(mode, input_sources)

        self.font = crowd.resource.font.default

        self.blah = []

    def update(self, time_elapsed):


        states = [(ins, ins.next_frame()) for ins in self.input_sources]

        def list_buttons(state):
            return ", ".join( k for k, v in state.keys.items() if v )

        self.blah = [
            (ins.player + ": " + list_buttons(state) , ins.color)
            for ins, state in states
        ]


        for ins, state in states:
            if state.a and state.b and state.up and state.down:
                self.mode.next_challenge()

    def render(self):

        self.mode.game.screen.fill((64, 64, 64))

        for i, b in enumerate(self.blah):
            txt, clr = b

            fr = self.font.render(txt, True, clr)
            self.mode.game.screen.blit(fr, (0,i * 20))

