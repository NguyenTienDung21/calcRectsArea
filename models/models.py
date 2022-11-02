import numpy as np


class Rect:
    def __init__(self, rect) -> None:
        x1, y1, x2, y2 = rect
        self.startpoint = [x1, y1]
        self.endpoint = [x2,y2]
        self.width = x2-x1 
        self.height = y2-y1 

    def area_mask(self):
        return np.full((self.height, self.width),True)
