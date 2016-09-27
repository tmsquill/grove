import behaviors as b
import preconditions as pc

pc = {
    0: pc.on_border,
    1: pc.on_nest,
    2: pc.on_food,
    3: pc.holding_food
}

b = {
    0: b.pickup_food,
    1: b.drop_food,
    2: b.random_walk,
    3: b.return_home
}

prob = {
    0: 0.001,
    1: 0.005,
    2: 0.01,
    3: 0.025,
    4: 0.05,
    5: 0.075,
    6: 0.1,
    7: 1.0
}
