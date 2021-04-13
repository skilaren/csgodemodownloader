class Map:

    """
    Attributes:

        name: in-game name of map
        z_point: zero point of the map
        scale: size of real map / size of mini-map
    """

    def __init__(self, name, x, y, scale):
        """

        :param name: in-game name of map
        :param x: x coord of zero point
        :param y: y coord of zero point
        :param scale:
        """
        self.name = name
        self.z_point = ZPoint(x, y)
        self.scale = scale

    def translate_scale(self, x, y):
        """
        Transforms (x, y) to (xS, yS) where xS and yS are coordinates one the mini-map of the map

        :param x: x coordinate from map position
        :param y: y coordinate from map position
        :return: scaled x, y which are the mini-map coordinates of input map position
        """
        x, y = self.translate(x, y)
        return x / self.scale, y / self.scale

    def translate(self, x, y):
        """
        Zeroing the coordinates

        :param x: initial x
        :param y: initial y
        :return: x, y adjusted to zero point of particular map
        """
        return x - self.z_point.x, self.z_point.y - y

    def translate_trajectory(self, trajectory):
        """
        Translates the list of points (which are considered as a trajectory) within map parameters

        :param trajectory: list of points
        :return: coordinates of trajectory for mini-map of map
        """
        for i in range(len(trajectory)):
            trajectory[i] = (self.translate_scale(trajectory[i][0], trajectory[i][1]))
        return trajectory


class ZPoint:

    def __init__(self, x, y):
        self.x = x
        self.y = y


cache = Map('de_cache', -2000, 3250, 5.5)
dust2 = Map('de_dust2', -2476, 3239, 4.4)
inferno = Map('de_inferno', -2087, 3870, 4.9)
mirage = Map('de_mirage', -3230, 1713, 5)
nuke = Map('de_nuke', -3453, 2887, 7)
overpass = Map('de_overpass', -4831, 1781, 5.2)
train = Map('de_train', -2477, 2392, 4.7)
vertigo = Map('de_vertigo', -3168, 1762, 4)

map_mappings = {
    'de_cache': cache,
    'de_dust2': dust2,
    'de_inferno': inferno,
    'de_mirage': mirage,
    'de_nuke': nuke,
    'de_overpass': overpass,
    'de_train': train,
    'de_vertigo': vertigo,
}