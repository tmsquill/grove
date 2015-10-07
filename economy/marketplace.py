__author__ = 'Zivia'

import supplycrate.endpoints.v2.items as it

item_ids = []

class Commerce:

    def __init__(self):

        self.items = it.items(item_ids)

    def search(self, ids=None):

        return []

    def buy(self, agent=None, id=None, quantity=None):

        item = self.items[id]

        if len(item.listings) >= quantity:

            pass

    def sell(self, agent=None, id=None, quantity=None):

        pass


recipe_ids = []

class Crafting:

    def __init__(self):

        self.recipes = it.recipes(recipe_ids)

    def craft(self, agent=None, id=None, quantity=None):

        pass

    def progress(self, agent=None, id=None):

        pass

class Item:

    def __init__(self, item=None):

        self.item = item
        self.listings = {}
