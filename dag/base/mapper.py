class Mapper:
    def __init__(self):
        self.map_ = dict()

    def map(self, k1: str, k2: str):
        self.map_[k1] = k2
        return self
