
import numpy as np

from models.models import Rect

import time
from functools import wraps

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper

class CalcArea:
    def __init__(self, image, rect_list):
        height, width, channel = image.shape
        self.init_mask = np.zeros((height, width), dtype=bool)
        self.rect_list = [Rect(rect) for rect in rect_list]
    
    @timeit
    def calculate(self):
        for rect in self.rect_list:
            self.apply_rect_mask(rect)
    
    def apply_rect_mask(self, rect):
        rect_mask = rect.area_mask()
        mask_startpoint_x, mask_startpoint_y = rect.startpoint
        mask_endpoint_x, mask_endpoint_y = rect.endpoint 
        self.init_mask[mask_startpoint_y:mask_endpoint_y,mask_startpoint_x:mask_endpoint_x] = rect_mask

    @timeit
    def composite_area(self):
        return np.count_nonzero(self.init_mask)
