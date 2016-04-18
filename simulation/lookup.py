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