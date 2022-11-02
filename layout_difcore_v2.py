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

def get_y1(rect):
    _, y1, _, _ = rect
    return y1

def get_y2(rect):
    _, _, _, y2 = rect
    return y2

def get_x1(rect):
    x1, _, _, _ = rect
    return x1

def get_x2(rect):
    _, _, x2, _ = rect
    return x2

def segment_rect_list(rects):
    yset = set()
    for rect in rects:
        yset.add(get_y1(rect))
        yset.add(get_y2(rect))
    ylist = list(yset)
    ylist.sort()
    return ylist

def calc_total_width(rects):
    xlist = []
    xlist.extend(map(lambda rect: (get_x1(rect), 1), rects))
    xlist.extend(map(lambda rect: (get_x2(rect), 0), rects))
    xlist.sort()
    cont, last, total = 0, 0, 0
    for x in xlist:
        if cont > 0: total += x[0] - last
        if x[1] == 1: cont += 1
        if x[1] == 0: cont -= 1
        last = x[0]
    return total

@timeit
def calc_total_area(rects):
    rects.sort(reverse = False, key = get_y1)
    ylist = segment_rect_list(rects)
    last, area = 0, 0
    in_queue_rects = []
    for i in range(len(ylist)-1):
        y1, y2 = ylist[i], ylist[i+1]
        while (last < len(rects) and 
                y2 > get_y1(rects[last]) and 
                y2 <= get_y2(rects[last])):
            in_queue_rects.append(rects[last])
            last += 1
        for rect in in_queue_rects:
            if get_y2(rect) <= y1: in_queue_rects.remove(rect)
        total_with = calc_total_width(in_queue_rects)
        area += total_with * (y2 - y1)
    return area

def extract_rect_from_diff_zone(diff_zones):
    rect_list = []
    for zone in diff_zones:
        if zone['type'] == 'diff_match':
            rect_list.append((zone['img1']['startpoint'][0], 
                    zone['img1']['startpoint'][1], 
                    zone['img1']['endpoint'][0], 
                    zone['img1']['endpoint'][1]))
        if zone['type'] == 'non_match':
            if zone['img1'] != None:
                rect_list.append((zone['img1']['startpoint'][0], 
                    zone['img1']['startpoint'][1], 
                    zone['img1']['endpoint'][0], 
                    zone['img1']['endpoint'][1]))
    return rect_list

def layout_diff_score_calc(zone_list, height, width):
    rect_list = extract_rect_from_diff_zone(zone_list)
    diff_area = calc_total_area(rect_list)
    diff_score = diff_area / (height * width) * 100
    return diff_score