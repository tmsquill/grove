def on_border(agent=None, environment=None):

    return agent.body.left == environment.body.left or \
           agent.body.top == environment.body.top or \
           agent.body.right == environment.body.right or \
           agent.body.bottom == environment.body.bottom


def on_nest(agent=None, environment=None):

    return nest.body.contains(agent.body)

"""
On food?
On nest?
"""

def holding_food():

    pass