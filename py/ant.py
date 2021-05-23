from tsp_util import get_desirability_from_city


class Ant:
    def __init__(self, city_index):
        self.city = city_index
        self.path = [self.city]
        self.desirability = get_desirability_from_city(self.city, self.path)
        self.done = False
