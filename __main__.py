from CalcArea import CalcArea
import cv2

from CalcArea import timeit
from layout_difcore_v2 import calc_total_area, extract_rect_from_diff_zone

@timeit
def read_image():
    return cv2.imread('/Users/dung.tnguyen/Documents/Project/rnd_x_img_diff/data/demo/checkpoint-keyes-image6.png')

@timeit
def main():

    image1 = read_image()
    rect_list = [(129, 174, 857, 264), (648, 500, 948, 750), (648, 1136, 948, 1386), (28, 2012, 757, 2103),(0,0,1,1),(1,1,2,2),(3,3,4,4),(5,5,7,7),
    (12,12,17,16),  (12,12,17,16)]
    areaCalculator = CalcArea(image1,rect_list)
    areaCalculator.calculate()
    print(areaCalculator.composite_area())
    calc_total_area(rect_list)
   

if __name__ == "__main__":
    main()