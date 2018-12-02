import cv2

def extract_objects_rects(frame, size_constraints, background_subtractor):

    foreground_mask = background_subtraction(frame.copy(), background_subtractor)
    return find_cars_bounding_rects(foreground_mask, size_constraints)

def intersection(rect_a, rect_b):
    x = max(rect_a[0], rect_b[0])
    y = max(rect_a[1], rect_b[1])
    w = min(rect_a[0]+rect_a[2], rect_b[0]+rect_b[2]) - x
    h = min(rect_a[1]+rect_a[3], rect_b[1]+rect_b[3]) - y

    if w < 0 or h < 0:
        return None

    return (x, y, w, h)

def background_subtraction (frame, background_subtractor):

    foreground_mask = background_subtractor.apply(frame)
    cv2.imshow('mask', foreground_mask)
    return foreground_mask

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

def check_stopline_crossing(rect, stopline_coords):

    x, y, w, h = rect
    
    if x >= stopline_coords[0]:
        ideal_rect = (stopline_coords[0], y, w, h)
        intersection_rect = intersection(rect, ideal_rect)
    
        if intersection_rect != None and intersection_rect[2] * intersection_rect[3] >= 0.9 * rect[2] * rect[3]:
            return True
        else:
            return False
    else:
        False


