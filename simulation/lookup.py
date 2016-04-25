import preconditions as pc
import behaviors as b

pc = {
    0: pc.on_border,
    1: pc.on_nest,
    2: pc.on_food,
    3: pc.holding_food
}

b = {
    0: b.move_north,
    1: b.move_east,
    2: b.move_south,
    3: b.move_west,
    4: b.pickup_food,
    5: b.drop_food,
    6: b.random_walk,
    7: b.return_home
}

a = {

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
