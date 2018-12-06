import cv2
import numpy as np

def extract_objects_rects(mask, size_constraints):

    return find_cars_bounding_rects(mask, size_constraints)

def intersection(rect_a, rect_b):
    x = max(rect_a[0], rect_b[0])
    y = max(rect_a[1], rect_b[1])
    w = min(rect_a[0]+rect_a[2], rect_b[0]+rect_b[2]) - x
    h = min(rect_a[1]+rect_a[3], rect_b[1]+rect_b[3]) - y

    if w < 0 or h < 0:
        return None

    return (x, y, w, h)

def find_cars_bounding_rects(foreground_mask, size_constraints):

    rects = []
    _, contours, _ = cv2.findContours(foreground_mask.copy(), cv2.RETR_TREE,
                                      cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        rect = cv2.boundingRect(contour)
        if rect[2] > size_constraints[0] and rect[3] > size_constraints[1]:
            #if check_stopline_crossing(rect, stopline_coords):
            rects.append(rect)
    return rects
