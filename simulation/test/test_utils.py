from simulation.utils import Point, Rectangle


def test_rectangle_contains_point():

    p1 = Point(3, 4)
    r1 = Rectangle(top_left=Point(1, 4), bottom_right=Point(4, 0))
    r2 = Rectangle(top_left=Point(-4, 5), bottom_right=Point(-2, 1))

    assert r1.contains_point(p1) is True
    assert r2.contains_point(p1) is False


def test_rectangle_contains_rectangle():

    r1 = Rectangle(top_left=Point(1, 7), bottom_right=Point(7, 1))
    r2 = Rectangle(top_left=Point(2, 5), bottom_right=Point(5, 2))
    r3 = Rectangle(top_left=Point(2, 5), bottom_right=Point(7, 1))

    assert r1.contains_rectangle(r2) is True
    assert r1.contains_rectangle(r3) is True
    assert r2.contains_rectangle(r3) is False


def test_rectangle_expand():

    r = Rectangle(top_left=Point(2, 2), bottom_right=Point(4, 0))
    r.expand(amount=1)

    assert r.top_left.position[0] == 1 and r.top_left.position[1] == 3 and r.bottom_right.position[0] == 5 and r.bottom_right.position[1] == -1


def test_rectangle_contract():

    r = Rectangle(top_left=Point(2, 2), bottom_right=Point(4, 0))
    r.contract(amount=1)

    assert r.top_left.position[0] == 3 and r.top_left.position[1] == 1 and r.bottom_right.position[0] == 3 and r.bottom_right.position[1] == 1
