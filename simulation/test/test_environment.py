from environment import Environment


class TestEnvironment:

    env = Environment()

    def test_expand(self):

        self.env.expand(amount=3)

        tl = self.env.body.top_left()
        br = self.env.body.bottom_right()

        assert tl.x == -3 and tl.y == -3 and br.x == 23 and br.y == 23

    def test_contract(self):

        self.env.contract(amount=3)

        tl = self.env.body.top_left()
        br = self.env.body.bottom_right()

        assert tl.x == 0 and tl.y == 0 and br.x == 20 and br.y == 20
